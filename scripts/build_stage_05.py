from __future__ import annotations

import ast
import csv
import hashlib
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.evidence_scoring import (  # noqa: E402
    COMPONENT_ORDER,
    GENERATING_PROCESS,
    coursework_exception_gate_from_evidence,
    funding_hard_gate_from_evidence,
    load_rubric,
    score_program,
    split_ids,
)
from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    PROGRAM_SCORE_COLUMNS_V2,
    SCORE_EVIDENCE_COLUMNS_V2,
)

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
SCORES_PATH = OUTPUT_DIR / "program_scores.csv"
EVIDENCE_PATH = OUTPUT_DIR / "score_evidence.csv"
REPORT_PATH = REPO_ROOT / "reports/pass2/05_scoring_and_calibration.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_05.json"
RUBRIC_PATH = REPO_ROOT / "config/scoring_rubric.yaml"
LATEST_REENTRY_PATH = OUTPUT_DIR / "stage_03_reentry_03_verification.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": row_count(path),
    }


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()


def _source_index() -> dict[str, dict[str, str]]:
    sources: dict[str, dict[str, str]] = {}
    for row in read_csv(OUTPUT_DIR / "program_sources.csv"):
        sources[row["stage3_source_id"]] = row
    for row in read_csv(OUTPUT_DIR / "professor_sources.csv"):
        sources[row["stage4_source_id"]] = row
    return sources


def _institution_score_constant_hits() -> list[str]:
    hits: list[str] = []
    roots = (REPO_ROOT / "src", REPO_ROOT / "scripts", REPO_ROOT / "evidence")
    for root in roots:
        for path in root.rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    names = {target.id.casefold() for target in targets if isinstance(target, ast.Name)}
                    if names & {"scores", "score_map", "program_scores", "institution_scores"}:
                        value = node.value
                        if isinstance(value, ast.Dict) and any(isinstance(key, ast.Constant) and isinstance(key.value, str) for key in value.keys):
                            hits.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{node.lineno}:named score map")
                if isinstance(node, ast.Dict):
                    for key, value in zip(node.keys, node.values):
                        key_text = key.value if isinstance(key, ast.Constant) and isinstance(key.value, str) else ""
                        institution_key = (
                            key_text.startswith(("us:", "ca:", "ror:"))
                            or any(token in key_text for token in ("University", "College", "Institute"))
                        )
                        numeric_tuple = isinstance(value, (ast.Tuple, ast.List)) and len(value.elts) >= 2 and all(
                            isinstance(item, ast.Constant) and isinstance(item.value, (int, float))
                            for item in value.elts
                        )
                        if institution_key and numeric_tuple:
                            hits.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{node.lineno}:institution numeric score tuple")
    return sorted(set(hits))


def _dense_rank(rows: list[dict[str, str]]) -> None:
    eligible = sorted(
        (row for row in rows if row["all_hard_gates_pass"] == "true"),
        key=lambda row: (-int(row["overall_score"]), row["program_id"]),
    )
    last_score: int | None = None
    rank = 0
    for row in eligible:
        score = int(row["overall_score"])
        if score != last_score:
            rank += 1
            last_score = score
        row["evidence_rank"] = str(rank)


def build() -> dict[str, object]:
    calculated_at = now()
    rubric = load_rubric(RUBRIC_PATH)
    profile = yaml.safe_load((REPO_ROOT / "config/applicant_profile.yaml").read_text(encoding="utf-8"))
    programs = [
        row for row in read_csv(OUTPUT_DIR / "program_verification.csv")
        if row["faculty_review_ready"] == "yes"
    ]
    latest_reentry_ids = {
        row["candidate_program_id"]
        for row in read_csv(LATEST_REENTRY_PATH)
        if row["faculty_review_ready"] == "yes"
    }
    candidates_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    retained_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(OUTPUT_DIR / "professor_candidates_evaluated.csv"):
        candidates_by_program[row["program_id"]].append(row)
    for row in read_csv(OUTPUT_DIR / "professor_matches_retained.csv"):
        retained_by_program[row["program_id"]].append(row)
    sources_by_id = _source_index()

    scores: list[dict[str, str]] = []
    score_evidence: list[dict[str, str]] = []
    for program in programs:
        program_id = program["candidate_program_id"]
        score_row, evidence_rows = score_program(
            program,
            candidates_by_program[program_id],
            retained_by_program[program_id],
            sources_by_id,
            profile,
            rubric,
            calculated_at,
        )
        scores.append(score_row)
        score_evidence.extend(evidence_rows)
    _dense_rank(scores)
    scores.sort(
        key=lambda row: (
            row["all_hard_gates_pass"] != "true",
            -int(row["overall_score"]),
            row["institution_name"],
            row["program_name"],
        )
    )
    rank_order = {row["program_id"]: index for index, row in enumerate(scores)}
    score_evidence.sort(key=lambda row: (rank_order[row["program_id"]], COMPONENT_ORDER.index(row["component"])))
    write_csv(SCORES_PATH, scores, PROGRAM_SCORE_COLUMNS_V2)
    write_csv(EVIDENCE_PATH, score_evidence, SCORE_EVIDENCE_COLUMNS_V2)

    evidence_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in score_evidence:
        evidence_by_program[row["program_id"]].append(row)
    programs_by_id = {row["candidate_program_id"]: row for row in programs}
    allowed_anchor_scores = {
        component: {int(anchor["score"]) for anchor in rubric["components"][component]["anchors"]}
        for component in COMPONENT_ORDER
    }
    source_ids = set(sources_by_id)
    forbidden_mutations_preserve_funding_gate = True
    for program in programs:
        baseline = funding_hard_gate_from_evidence(program, sources_by_id)
        for field, value in (
            ("verification_status", "excluded"),
            ("candidate_funnel_status", "screened_out"),
            ("screening_decision", "retained"),
            ("funding_gate", "pass"),
            ("recommendation", "Strong Apply"),
            ("overall_score", "100"),
            ("funding_score", "25"),
        ):
            changed = dict(program)
            changed[field] = value
            forbidden_mutations_preserve_funding_gate &= funding_hard_gate_from_evidence(changed, sources_by_id) == baseline
    coursework_fixture = {
        "candidate_program_id": "fixture:coursework",
        "degree_type": "Coursework or professional master's",
        "research_requirement": "Coursework only",
        "funding_source_ids": "",
    }
    constant_hits = _institution_score_constant_hits()
    assertions = {
        "entire_serious_program_pool_recalculated": bool(programs) and len(scores) == len(programs) and {row["program_id"] for row in scores} == {row["candidate_program_id"] for row in programs},
        "latest_reentry_03_fully_recalculated": (
            len(latest_reentry_ids) == 8
            and {row["program_id"] for row in scores if row["program_id"] in latest_reentry_ids}
            == latest_reentry_ids
            and all(len(evidence_by_program[program_id]) == len(COMPONENT_ORDER) for program_id in latest_reentry_ids)
        ),
        "exactly_six_components_per_program": len(score_evidence) == len(scores) * 6 and all({row["component"] for row in evidence_by_program[pid]} == set(COMPONENT_ORDER) for pid in evidence_by_program),
        "program_rows_reference_exact_component_evidence": all(
            set(split_ids(row["score_evidence_ids"]))
            == {item["score_evidence_id"] for item in evidence_by_program[row["program_id"]]}
            for row in scores
        ),
        "component_evidence_has_required_audit_metadata": all(
            row["rubric_anchor"]
            and row["rubric_anchor_description"]
            and row["reviewer_or_generating_process"]
            and row["verification_status"]
            and row["calculated_at"]
            and "uncertainty_or_conflict" in row
            for row in score_evidence
        ),
        "component_scores_use_rubric_anchors": all(int(row["component_score"]) in allowed_anchor_scores[row["component"]] for row in score_evidence),
        "rubric_avoids_unexplained_one_point_bands": all(
            all(higher - lower != 1 for lower, higher in zip(sorted(scores), sorted(scores)[1:]))
            for scores in allowed_anchor_scores.values()
        ),
        "overall_scores_are_component_sums": all(int(row["overall_score"]) == sum(int(item["component_score"]) for item in evidence_by_program[row["program_id"]]) for row in scores),
        "positive_components_have_resolving_evidence": all(int(row["component_score"]) == 0 or (split_ids(row["supporting_evidence_ids"]) and set(split_ids(row["supporting_evidence_ids"])).issubset(source_ids)) for row in score_evidence),
        "funding_gate_is_recomputed_from_direct_sources": all(
            (row["funding_hard_gate"] == "true")
            == funding_hard_gate_from_evidence(programs_by_id[row["program_id"]], sources_by_id)
            for row in scores
        ),
        "funding_gate_ignores_labels_recommendations_and_scores": forbidden_mutations_preserve_funding_gate,
        "one_professor_depth_cap_enforced": all(not (int(row["distinct_verified_strong_matches"]) <= 1 and int(row["faculty_depth_points"]) > 5) for row in scores),
        "duplicate_professors_do_not_inflate_depth": all(int(row["distinct_verified_strong_matches"]) == len({item["professor_id"] for item in retained_by_program[row["program_id"]]}) for row in scores),
        "missing_or_unverifiable_evidence_reduces_confidence": all(row["score_confidence"] == "low" for row in scores if row["funding_hard_gate"] == "false" or row["professor_hard_gate"] == "false"),
        "minimum_gpa_alone_never_creates_plausible": all(row["admission_plausibility"] in {"Insufficient evidence", "Eligibility concern", "Clearly ineligible"} for row in scores),
        "no_admission_percentages_emitted": all(not row["admission_probability"] and "%" not in row["admission_plausibility"] for row in scores),
        "coursework_only_without_exceptional_funding_fails": not coursework_exception_gate_from_evidence(coursework_fixture, sources_by_id),
        "only_hard_gate_survivors_receive_ranks": all(bool(row["evidence_rank"]) == (row["all_hard_gates_pass"] == "true") for row in scores),
        "tied_totals_share_dense_rank": all(a["evidence_rank"] == b["evidence_rank"] for a in scores for b in scores if a["all_hard_gates_pass"] == b["all_hard_gates_pass"] == "true" and a["overall_score"] == b["overall_score"]),
        "required_output_schemas_exact": list(scores[0]) == list(PROGRAM_SCORE_COLUMNS_V2) and list(score_evidence[0]) == list(SCORE_EVIDENCE_COLUMNS_V2),
        "no_institution_specific_score_constants": not constant_hits,
    }
    counts = {
        "serious_programs_scored": len(scores),
        "score_evidence_rows": len(score_evidence),
        "hard_gate_survivors": sum(row["all_hard_gates_pass"] == "true" for row in scores),
        "funding_gate_pass": sum(row["funding_hard_gate"] == "true" for row in scores),
        "professor_gate_pass": sum(row["professor_hard_gate"] == "true" for row in scores),
        "eligibility_gate_pass": sum(row["eligibility_hard_gate"] == "true" for row in scores),
        "zero_depth_programs": sum(row["faculty_depth_points"] == "0" for row in scores),
        "single_professor_dependencies": sum(row["single_professor_dependency"] == "true" for row in scores),
        "insufficient_admission_evidence": sum(row["admission_plausibility"] == "Insufficient evidence" for row in scores),
        "eligibility_concerns": sum(row["admission_plausibility"] == "Eligibility concern" for row in scores),
        "institution_score_constant_hits": len(constant_hits),
        "latest_reentry_programs": len(latest_reentry_ids),
        "latest_reentry_hard_gate_survivors": sum(
            row["program_id"] in latest_reentry_ids and row["all_hard_gates_pass"] == "true"
            for row in scores
        ),
        "latest_reentry_funding_gate_pass": sum(
            row["program_id"] in latest_reentry_ids and row["funding_hard_gate"] == "true"
            for row in scores
        ),
        "latest_reentry_professor_gate_pass": sum(
            row["program_id"] in latest_reentry_ids and row["professor_hard_gate"] == "true"
            for row in scores
        ),
    }
    return {
        "status": "PASS" if all(assertions.values()) else "FAIL",
        "assertions": assertions,
        "counts": counts,
        "constant_hits": constant_hits,
    }


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value).replace("|", "/") for value in row) + " |" for row in rows)
    return "\n".join(lines)


def write_report(result: dict[str, object]) -> None:
    scores = read_csv(SCORES_PATH)
    counts = result["counts"]
    survivors = [row for row in scores if row["all_hard_gates_pass"] == "true"]
    gate_counts = Counter(failure for row in scores for failure in split_ids(row["hard_gate_failures"]))
    lines = [
        "# Pass 2 Stage 5 — Evidence-based scoring and admission calibration",
        "",
        f"Generated: {now()}",
        "",
        f"Decision: **{result['status']}**",
        "",
        "## Outcome",
        "",
        (
            f"All {counts['serious_programs_scored']} serious Stage 4 programs were recalculated from six recorded "
            f"evidence components ({counts['score_evidence_rows']} component rows). Only "
            f"{counts['hard_gate_survivors']} programs clear the direct funding, verified-professor, eligibility, "
            "degree-structure, and coursework-exception gates. Gated-out rows retain diagnostic component totals but "
            "receive no evidence rank."
        ),
        "",
        "## Hard-gate result",
        "",
        table(
            ["Gate", "Programs passing", "Programs failing"],
            [
                ["Direct verified funding", counts["funding_gate_pass"], counts["serious_programs_scored"] - counts["funding_gate_pass"]],
                ["Verified strong professor", counts["professor_gate_pass"], counts["serious_programs_scored"] - counts["professor_gate_pass"]],
                ["Formal eligibility", counts["eligibility_gate_pass"], counts["serious_programs_scored"] - counts["eligibility_gate_pass"]],
                ["All hard gates", counts["hard_gate_survivors"], counts["serious_programs_scored"] - counts["hard_gate_survivors"]],
            ],
        ),
        "",
        "The funding gate is recomputed from exact-program source IDs whose source rows are official, verified, and explicitly funding-related. It never reads the Stage 3 retained/conditional label, a recommendation, total score, or funding score.",
        "",
        "## Evidence-ranked hard-gate survivors",
        "",
        table(
            ["Dense rank", "Institution", "Program", "Score", "Pattern", "Admission calibration"],
            [[row["evidence_rank"], row["institution_name"], row["program_name"], row["overall_score"], row["component_score_pattern"], row["admission_plausibility"]] for row in survivors]
            or [["—", "None", "—", "—", "—", "—"]],
        ),
        "",
        "Tied totals share the same dense rank. Prestige and institution identity are not scoring inputs or tie-breakers.",
        "",
        "## Admission calibration",
        "",
        (
            f"{counts['insufficient_admission_evidence']} rows are `Insufficient evidence`; "
            f"{counts['eligibility_concerns']} carry an `Eligibility concern`. The source ledger contains formal "
            "requirements but no official cohort/selectivity evidence adequate for a strategic Plausible/Reach category. "
            "Published GPA minimums remain in a separate field and never create plausibility. No admission percentage is emitted."
        ),
        "",
        "## Acceptance checks",
        "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in result["assertions"].items()]),
        "",
        "## Blockers",
        "",
        "None prevented Stage 5 completion.",
        "",
        "## Unresolved coverage",
        "",
        (
            f"- Stage 5 re-entry 03 recalculated {counts['latest_reentry_programs']} newly eligible routes. "
            f"All {counts['latest_reentry_professor_gate_pass']} pass the professor gate. The direct funding gate "
            f"passes for {counts['latest_reentry_funding_gate_pass']}, and "
            f"{counts['latest_reentry_hard_gate_survivors']} clear every hard gate."
        ),
        f"- {counts['serious_programs_scored'] - counts['funding_gate_pass']} programs lack direct source evidence strong enough for the funding hard gate.",
        f"- {counts['serious_programs_scored'] - counts['professor_gate_pass']} programs lack a fully verified strong professor with exact-route supervision authority.",
        f"- {counts['zero_depth_programs']} programs have zero verified faculty-depth points; {counts['single_professor_dependencies']} have only one verified strong match and remain capped at 5 points.",
        f"- {counts['insufficient_admission_evidence']} programs lack official cohort/selectivity evidence for strategic admission calibration.",
        "- Offer-specific net funding, fees, health insurance, summers, and duration remain incomplete where identified in the component evidence.",
        f"- The existing Stage 6 portfolio still covers the prior score pool; Stage 6 must be rebuilt against these {counts['serious_programs_scored']} scores.",
        "- Stage 6 must pressure-test only hard-gate survivors for a core portfolio; diagnostic totals cannot override a failed gate.",
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def input_paths() -> list[Path]:
    return [
        REPO_ROOT / "data/manifests/pass2/stage_04.json",
        REPO_ROOT / "config/applicant_profile.yaml",
        RUBRIC_PATH,
        OUTPUT_DIR / "program_verification.csv",
        LATEST_REENTRY_PATH,
        OUTPUT_DIR / "program_sources.csv",
        OUTPUT_DIR / "professor_candidates_evaluated.csv",
        OUTPUT_DIR / "professor_matches_retained.csv",
        OUTPUT_DIR / "professor_sources.csv",
        REPO_ROOT / "src/graduate_audit/evidence_scoring.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
    ]


def main() -> int:
    started_at = now()
    source_commit = git_head()
    result = build()
    write_report(result)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["5"] = "complete" if result["status"] == "PASS" else "failed"
    stage_status["5_reentry_01"] = "complete" if result["status"] == "PASS" else "failed"
    stage_status["5_reentry_02"] = "complete" if result["status"] == "PASS" else "failed"
    stage_status["5_reentry_03"] = "complete" if result["status"] == "PASS" else "failed"
    pass2.update({
        "current_stage": 5,
        "last_completed_stage": max(int(pass2.get("last_completed_stage", 0)), 5) if result["status"] == "PASS" else 4,
        "stage_status": stage_status,
        "next_stage": 6,
        "next_stage_authorized": result["status"] == "PASS",
        "stage_manifest": "data/manifests/pass2/stage_05.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_05_acceptance": result["status"],
        "stage_05_hard_gate_survivors": result["counts"]["hard_gate_survivors"],
        "stage_05_reentry_completed": 3 if result["status"] == "PASS" else 2,
        "stage_05_reentry_serious_programs": result["counts"]["serious_programs_scored"],
        "stage_05_reentry_latest_programs": result["counts"]["latest_reentry_programs"],
        "stage_05_reentry_required": False,
        "stage_06_reentry_required": result["status"] == "PASS",
        "stage_06_reentry_source_stage": 5,
    })
    update_progress(
        progress_path,
        current_phase="pass2_stage_05_reentry_03_complete" if result["status"] == "PASS" else "pass2_stage_05_reentry_03_failed",
        pass2=pass2,
    )

    counts = result["counts"]
    unresolved = [
        f"{counts['serious_programs_scored'] - counts['funding_gate_pass']} programs lack direct verified funding evidence strong enough for the hard gate.",
        f"{counts['serious_programs_scored'] - counts['professor_gate_pass']} programs lack a fully verified strong professor match.",
        f"{counts['zero_depth_programs']} programs have zero verified faculty depth and {counts['single_professor_dependencies']} are single-professor dependencies.",
        f"{counts['insufficient_admission_evidence']} programs lack official cohort/selectivity evidence for strategic admission calibration.",
        "Offer-specific net cost and coverage details remain incomplete where recorded in score evidence.",
        f"Stage 5 re-entry 03 produced {counts['latest_reentry_hard_gate_survivors']} hard-gate survivors from {counts['latest_reentry_programs']} newly scored routes; the others fail at least one hard gate.",
        f"The existing Stage 6 portfolio covers the prior score pool and must be rebuilt against the {counts['serious_programs_scored']} current score rows.",
    ]
    outputs = [SCORES_PATH, EVIDENCE_PATH, REPORT_PATH]
    artifacts = [
        RUBRIC_PATH,
        REPO_ROOT / "src/graduate_audit/evidence_scoring.py",
        REPO_ROOT / "src/graduate_audit/hard_gates.py",
        REPO_ROOT / "src/graduate_audit/pipeline.py",
        REPO_ROOT / "src/graduate_audit/portfolio.py",
        REPO_ROOT / "src/graduate_audit/finalize.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "src/graduate_audit/verify/apply_corrections.py",
        REPO_ROOT / "evidence/deep_review/us/build_deep_review.py",
        REPO_ROOT / "scripts/build_stage_05.py",
        REPO_ROOT / "tests/test_evidence_scoring.py",
        REPO_ROOT / "tests/test_hard_gates.py",
        progress_path,
        *outputs,
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 5,
        "run_type": "scoring_reentry_03",
        "name": "Evidence-based scoring and admission calibration — re-entry 03",
        "status": "complete" if result["status"] == "PASS" else "failed",
        "decision": result["status"],
        "source_commit_before_stage": source_commit,
        "triggered_by_stage": 4,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in input_paths()],
        "outputs": [file_record(path) for path in outputs],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": result["status"],
            "assertions": result["assertions"],
            "generating_process": GENERATING_PROCESS,
            "institution_specific_score_constant_hits": result["constant_hits"],
        },
        "counts": counts,
        "failures": [] if result["status"] == "PASS" else [name for name, passed in result["assertions"].items() if not passed],
        "blockers": [],
        "unresolved_coverage": unresolved,
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 5 manifest: {result['status']}")
    print(counts)
    if result["constant_hits"]:
        print("Institution-specific score constants:")
        print("\n".join(result["constant_hits"]))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
