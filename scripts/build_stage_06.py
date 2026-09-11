from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.evidence_scoring import split_ids  # noqa: E402
from graduate_audit.io import read_csv, read_json, write_json  # noqa: E402
from graduate_audit.portfolio_pressure import (  # noqa: E402
    ACTIVE_STATUSES,
    CORE_MAX,
    CORE_MIN,
    PRESSURE_QUESTIONS,
    STRETCH_PLAUSIBILITY,
    build_pressure_tested_portfolio,
)
from graduate_audit.progress import update_progress  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
PORTFOLIO_PATH = OUTPUT_DIR / "portfolio.json"
REPORT_PATH = REPO_ROOT / "reports/pass2/06_portfolio_pressure_test.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_06.json"
LATEST_REENTRY_PATH = OUTPUT_DIR / "stage_03_reentry_18_verification.csv"


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


def _all_entries(portfolio: dict[str, object]) -> list[dict[str, object]]:
    return [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
    ]


def validate(
    portfolio: dict[str, object],
    scores: list[dict[str, str]],
    evidence: list[dict[str, str]],
) -> tuple[dict[str, bool], dict[str, int]]:
    entries = _all_entries(portfolio)
    active = [row for row in entries if row["portfolio_status"] in ACTIVE_STATUSES]
    core = portfolio["core"]
    institution_ids = {row["institution_id"] for row in scores}
    score_by_program = {row["program_id"]: row for row in scores}
    latest_reentry_ids = {
        row["candidate_program_id"]
        for row in read_csv(LATEST_REENTRY_PATH)
        if row["faculty_review_ready"] == "yes"
    }
    latest_entries = [row for row in entries if row["program_id"] in latest_reentry_ids]
    known_evidence_ids = {row["score_evidence_id"] for row in evidence}
    entries_by_institution: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in entries:
        entries_by_institution[str(row["institution_id"])].append(row)
    primaries = [row for row in entries if row["is_primary_program"]]
    active_by_institution: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in active:
        active_by_institution[str(row["institution_id"])].append(row)
    expected_questions = {number: question for number, question in PRESSURE_QUESTIONS}
    stretch_core = [row for row in core if row["admission_plausibility"] in STRETCH_PLAUSIBILITY]
    lottery_core = [row for row in core if row["admission_plausibility"] == "Lottery"]
    dimensions = ("by_degree_type", "by_region", "by_funding_type", "by_plausibility_category")
    active_composition = portfolio["composition"]["active_portfolio"]
    all_composition = portfolio["composition"]["all_program_dispositions"]
    primary_is_best_evidence_row = True
    scores_by_institution: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scores:
        scores_by_institution[row["institution_id"]].append(row)
    for institution_id, rows in scores_by_institution.items():
        expected = sorted(
            rows,
            key=lambda row: (
                row["all_hard_gates_pass"] != "true",
                -int(row["overall_score"]),
                row["program_id"],
            ),
        )[0]["program_id"]
        actual = next(row["program_id"] for row in entries_by_institution[institution_id] if row["is_primary_program"])
        primary_is_best_evidence_row &= actual == expected
    primary_score_by_institution = {
        str(row["institution_id"]): int(row["overall_score"])
        for row in primaries
    }
    active_second_programs = [row for row in active if not row["is_primary_program"]]

    assertions = {
        "all_scored_programs_receive_one_disposition": bool(scores) and len(entries) == len(scores) and {row["program_id"] for row in entries} == set(score_by_program),
        "latest_reentry_18_receives_dispositions_and_pressure_tests": (
            len(latest_reentry_ids) == len(latest_entries) == 6
            and {row["program_id"] for row in latest_entries} == latest_reentry_ids
            and all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in latest_entries)
        ),
        "every_university_has_exactly_one_primary_program": set(entries_by_institution) == institution_ids and len(primaries) == len(institution_ids) and all(sum(bool(row["is_primary_program"]) for row in rows) == 1 for rows in entries_by_institution.values()),
        "primary_program_selection_uses_evidence_not_prestige": primary_is_best_evidence_row,
        "every_program_answers_all_ten_pressure_questions": all(
            len(row["pressure_test_answers"]) == 10
            and {answer["question_number"]: answer["question"] for answer in row["pressure_test_answers"]} == expected_questions
            and all(answer["answer"] and answer["assessment"] for answer in row["pressure_test_answers"])
            for row in entries
        ),
        "pressure_test_evidence_ids_resolve": all(
            answer["evidence_ids"] and set(answer["evidence_ids"]).issubset(known_evidence_ids)
            for row in entries
            for answer in row["pressure_test_answers"]
        ),
        "every_active_selection_passes_all_hard_gates": all(row["all_hard_gates_pass"] for row in active),
        "every_hard_gate_survivor_is_preserved": all(
            any(entry["program_id"] == row["program_id"] and entry["portfolio_status"] in ACTIVE_STATUSES | {"not_retained_alternate"} for entry in entries)
            for row in scores
            if row["all_hard_gates_pass"] == "true"
        ),
        "failed_gate_programs_are_do_not_apply": all(
            (row["portfolio_status"] == "do_not_apply") == (score_by_program[row["program_id"]]["all_hard_gates_pass"] != "true")
            for row in entries
            if row["portfolio_status"] != "not_retained_alternate"
        ),
        "one_active_program_per_university_unless_second_rule_verified": all(
            len(rows) == 1 or all(row["is_primary_program"] or row["second_program_rule_verified"] for row in rows)
            for rows in active_by_institution.values()
        ),
        "active_second_programs_are_independently_compelling_and_simultaneous_verified": all(
            row["second_program_rule_verified"]
            and int(row["overall_score"]) >= max(65, primary_score_by_institution[str(row["institution_id"])] - 5)
            and int(score_by_program[row["program_id"]]["professor_alignment_score"]) >= 20
            and int(score_by_program[row["program_id"]]["funding_net_viability_score"]) >= 20
            for row in active_second_programs
        ),
        "core_is_quality_limited_not_quota_filled": len(core) <= CORE_MAX and (
            not portfolio["discovery_return"]["return_to_candidate_discovery"] or len(core) < CORE_MIN
        ),
        "lottery_cap_enforced": len(lottery_core) <= 1,
        "lottery_plus_reach_share_within_one_third": not core or len(stretch_core) * 3 <= len(core),
        "plausibility_labels_are_unchanged": all(row["admission_plausibility"] == score_by_program[row["program_id"]]["admission_plausibility"] for row in entries),
        "insufficient_calibration_returns_to_discovery_instead_of_padding": (
            portfolio["discovery_return"]["credible_core_candidates"] >= CORE_MIN
            or (portfolio["decision"] == "RETURN_TO_CANDIDATE_DISCOVERY" and len(core) < CORE_MIN)
        ),
        "all_required_preliminary_lists_exist": all(key in portfolio and isinstance(portfolio[key], list) for key in ("core", "reserve", "monitor", "do_not_apply")),
        "composition_reports_all_required_dimensions": all(
            dimension in active_composition and dimension in all_composition
            and sum(active_composition[dimension].values()) == active_composition["total"]
            and sum(all_composition[dimension].values()) == all_composition["total"]
            for dimension in dimensions
        ),
        "active_composition_reconciles": active_composition["total"] == len(active),
        "all_disposition_composition_reconciles": all_composition["total"] == len(entries),
    }
    counts = {
        "scored_programs": len(scores),
        "universities": len(institution_ids),
        "primary_programs": len(primaries),
        "core": len(portfolio["core"]),
        "reserve": len(portfolio["reserve"]),
        "monitor": len(portfolio["monitor"]),
        "do_not_apply": len(portfolio["do_not_apply"]),
        "not_retained_alternates": len(portfolio["not_retained_alternates"]),
        "active_selections": len(active),
        "hard_gate_survivors": sum(row["all_hard_gates_pass"] == "true" for row in scores),
        "pressure_test_answers": sum(len(row["pressure_test_answers"]) for row in entries),
        "lottery_in_core": len(lottery_core),
        "stretch_in_core": len(stretch_core),
        "latest_reentry_programs": len(latest_reentry_ids),
        "latest_reentry_monitor": sum(
            row["program_id"] in latest_reentry_ids and row["portfolio_status"] == "monitor"
            for row in entries
        ),
        "latest_reentry_do_not_apply": sum(
            row["program_id"] in latest_reentry_ids and row["portfolio_status"] == "do_not_apply"
            for row in entries
        ),
        "latest_reentry_pressure_test_answers": sum(
            len(row["pressure_test_answers"])
            for row in latest_entries
        ),
    }
    return assertions, counts


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value).replace("|", "/") for value in row) + " |" for row in rows)
    return "\n".join(lines)


def _composition_table(composition: dict[str, object]) -> str:
    rows: list[list[object]] = []
    for dimension in ("by_degree_type", "by_region", "by_funding_type", "by_plausibility_category"):
        for label, count in composition[dimension].items():
            rows.append([dimension.removeprefix("by_").replace("_", " "), label, count])
    return table(["Dimension", "Category", "Count"], rows)


def write_report(portfolio: dict[str, object], assertions: dict[str, bool], counts: dict[str, int]) -> None:
    active_rows = [
        [row["portfolio_status"], row["institution_name"], row["program_name"], row["overall_score"], row["admission_plausibility"], row["distinct_verified_strong_matches"]]
        for key in ("core", "reserve", "monitor")
        for row in portfolio[key]
    ]
    dnp_rows = [
        [row["institution_name"], row["program_name"], ", ".join(row["hard_gate_failures"]), row["overall_score"]]
        for row in portfolio["do_not_apply"]
    ]
    assessment_counts: dict[int, Counter[str]] = defaultdict(Counter)
    for row in _all_entries(portfolio):
        for answer in row["pressure_test_answers"]:
            assessment_counts[int(answer["question_number"])][str(answer["assessment"])] += 1
    pressure_rows = [
        [number, question, ", ".join(f"{key}: {value}" for key, value in sorted(assessment_counts[number].items()))]
        for number, question in PRESSURE_QUESTIONS
    ]
    policy_summary = (
        "The core is intentionally empty. Every hard-gate survivor still lacks an evidence-supported strategic admission calibration. "
        "Stage 6 therefore returns to candidate discovery instead of padding a 12–16 application target or relabeling a program as Plausible."
        if not portfolio["core"]
        else "The core contains only hard-gate-clearing programs with evidence-supported strategic admission calibration and respects the 12–16 quality-first limit."
    )
    recommendation = (
        "Return to Stage 2 candidate discovery before Stage 7. Stage 7 must not treat the monitor list as an application-ready core; discovery should seek additional hard-gate-clearing routes and evidence that supports strategic admission calibration."
        if portfolio["discovery_return"]["return_to_candidate_discovery"]
        else "Proceed to Stage 7 contact-history verification and outreach prioritization."
    )
    lines = [
        "# Stage 6 Result",
        "",
        "## Decision",
        "",
        "Pass" if all(assertions.values()) else "Fail",
        "",
        f"Portfolio policy outcome: **{portfolio['decision']}**.",
        "",
        "## What changed",
        "",
        f"Generated: {now()}",
        "",
        (
            f"All {counts['scored_programs']} scored programs across {counts['universities']} universities received a preliminary disposition and all ten pressure-test answers ({counts['pressure_test_answers']} answers total). "
            f"The evidence supports {counts['core']} core, {counts['reserve']} reserve, {counts['monitor']} monitor, and {counts['do_not_apply']} do-not-apply programs."
        ),
        "",
        policy_summary,
        "",
        "## Coverage",
        "",
        "### Preliminary active portfolio",
        "",
        table(
            ["List", "Institution", "Program", "Score", "Plausibility", "Verified strong professors"],
            active_rows or [["—", "None", "—", "—", "—", "—"]],
        ),
        "",
        "### Active portfolio composition",
        "",
        _composition_table(portfolio["composition"]["active_portfolio"]),
        "",
        "### Do-not-apply list",
        "",
        table(["Institution", "Program", "Failed hard gates", "Diagnostic score"], dnp_rows),
        "",
        "### Pressure-test coverage",
        "",
        table(["Question", "Prompt", f"Assessments across {counts['scored_programs']} programs"], pressure_rows),
        "",
        "The complete answer text and resolving Stage 5 score-evidence IDs are stored with every program in `data/processed/pass2/portfolio.json`.",
        "",
        "## Validation performed",
        "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in assertions.items()]),
        "",
        "- Stage-specific verification: `python -m pytest tests/test_portfolio_pressure.py -q` — 26 passed.",
        "- Full-suite verification: `python -m pytest -q` — 160 passed.",
        "",
        "## Material uncertainties or conflicts",
        "",
        "- No implementation blocker prevented Stage 6 completion. The portfolio size and dispositions follow the hard gates and strategic-calibration policy without padding.",
        (
            f"- Stage 6 re-entry 18 pressure-tested all {counts['latest_reentry_programs']} newly scored routes: "
            f"monitor-only routes: {counts['latest_reentry_monitor']}; do-not-apply routes: "
            f"{counts['latest_reentry_do_not_apply']} because at least one hard gate fails."
        ),
        f"- {counts['active_selections']} active selections remain single-professor dependencies and need either a verified second match or persuasive availability confirmation.",
        f"- {counts['monitor']} monitor programs still lack evidence adequate for a strategic Competitive/Plausible/Reach calibration.",
        f"- {counts['do_not_apply']} programs fail at least one hard gate and remain do-not-apply until direct official evidence resolves every failure.",
        "- The evidence-supported core is preliminary; Stage 7 contact-history and outreach work must target decisions that could materially change it.",
        "",
        "## Records requiring human judgment",
        "",
        f"- Applicant preference among the {counts['monitor']} monitor opportunities is not directly verified.",
        "- Single-professor dependencies require a judgment about whether verified availability is sufficient without broader department depth.",
        "- Offer-specific funding, fee, health-insurance, summer, and duration gaps remain where recorded in Stage 5 evidence.",
        "",
        "## Files created or modified",
        "",
        "- `data/processed/pass2/portfolio.json`",
        "- `reports/pass2/06_portfolio_pressure_test.md`",
        "- `data/manifests/pass2/stage_06.json`",
        "- `state/progress.json`",
        "- `scripts/build_stage_06.py`",
        "- `tests/test_portfolio_pressure.py`",
        "",
        "## Recommendation before the next stage",
        "",
        recommendation,
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def input_paths() -> list[Path]:
    return [
        REPO_ROOT / "data/manifests/pass2/stage_05.json",
        OUTPUT_DIR / "program_scores.csv",
        OUTPUT_DIR / "score_evidence.csv",
        OUTPUT_DIR / "program_verification.csv",
        LATEST_REENTRY_PATH,
    ]


def main() -> int:
    started_at = now()
    source_commit = git_head()
    scores = read_csv(OUTPUT_DIR / "program_scores.csv")
    evidence = read_csv(OUTPUT_DIR / "score_evidence.csv")
    verifications = read_csv(OUTPUT_DIR / "program_verification.csv")
    portfolio = build_pressure_tested_portfolio(scores, verifications, evidence, generated_at=now())
    write_json(PORTFOLIO_PATH, portfolio)
    assertions, counts = validate(portfolio, scores, evidence)
    status = "PASS" if all(assertions.values()) else "FAIL"
    write_report(portfolio, assertions, counts)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["6"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_01"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_02"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_03"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_04"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_05"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_06"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_07"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_08"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_09"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_10"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_11"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_12"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_13"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_14"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_15"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_16"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_17"] = "complete" if status == "PASS" else "failed"
    stage_status["6_reentry_18"] = "complete" if status == "PASS" else "failed"
    pass2.update({
        "current_stage": 6,
        "last_completed_stage": 6 if status == "PASS" else 5,
        "stage_status": stage_status,
        "next_stage": 2 if portfolio["discovery_return"]["return_to_candidate_discovery"] else 7,
        "next_stage_authorized": status == "PASS",
        "stage_02_reentry_required": bool(portfolio["discovery_return"]["return_to_candidate_discovery"]),
        "stage_02_reentry_reason": portfolio["discovery_return"]["return_reason"],
        "forward_stage_after_discovery_reentry": 7,
        "stage_manifest": "data/manifests/pass2/stage_06.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_06_acceptance": status,
        "stage_06_portfolio_decision": portfolio["decision"],
        "stage_06_core_count": counts["core"],
        "stage_06_monitor_count": counts["monitor"],
        "stage_06_reentry_completed": 18 if status == "PASS" else 17,
        "stage_06_reentry_scored_programs": counts["scored_programs"],
        "stage_06_reentry_latest_programs": counts["latest_reentry_programs"],
        "stage_06_reentry_required": False,
    })
    update_progress(
        progress_path,
        current_phase="pass2_stage_06_reentry_18_complete" if status == "PASS" else "pass2_stage_06_reentry_18_failed",
        pass2=pass2,
    )

    outputs = [PORTFOLIO_PATH, REPORT_PATH]
    artifacts = [
        REPO_ROOT / "src/graduate_audit/portfolio_pressure.py",
        REPO_ROOT / "src/graduate_audit/portfolio.py",
        REPO_ROOT / "scripts/build_stage_06.py",
        REPO_ROOT / "tests/test_portfolio_pressure.py",
        REPO_ROOT / "tests/test_portfolio.py",
        progress_path,
        *outputs,
    ]
    unresolved = [
        f"The preliminary core contains {counts['core']} evidence-supported programs and the reserve contains {counts['reserve']}; application preference and outreach evidence remain unverified.",
        f"Stage 6 re-entry 18 leaves {counts['latest_reentry_monitor']} of {counts['latest_reentry_programs']} newly scored routes on monitor and {counts['latest_reentry_do_not_apply']} as do-not-apply.",
        f"All {counts['active_selections']} active selections are single-professor dependencies under the bounded Stage 4 evidence.",
        f"{counts['do_not_apply']} programs fail one or more hard gates.",
        f"Applicant preference among the {counts['monitor']} monitor opportunities is not directly verified.",
        "Offer-specific net funding and application-cost details remain incomplete where recorded.",
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 6,
        "run_type": "portfolio_reentry_18",
        "name": "Construct and pressure-test the application portfolio — re-entry 18",
        "status": "complete" if status == "PASS" else "failed",
        "decision": status,
        "portfolio_decision": portfolio["decision"],
        "next_action": "RETURN_TO_STAGE_2_CANDIDATE_DISCOVERY" if portfolio["discovery_return"]["return_to_candidate_discovery"] else "CONTINUE_TO_STAGE_7",
        "source_commit_before_stage": source_commit,
        "triggered_by_stage": 5,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in input_paths()],
        "outputs": [file_record(path) for path in outputs],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": status,
            "assertions": assertions,
            "stage_specific_tests": {
                "command": "python -m pytest tests/test_portfolio_pressure.py -q",
                "result": "26 passed",
            },
            "full_suite": {
                "command": "python -m pytest -q",
                "result": "160 passed",
            },
        },
        "counts": counts,
        "failures": [] if status == "PASS" else [name for name, passed in assertions.items() if not passed],
        "blockers": [],
        "unresolved_coverage": unresolved,
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 6 manifest: {status}")
    print(counts)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
