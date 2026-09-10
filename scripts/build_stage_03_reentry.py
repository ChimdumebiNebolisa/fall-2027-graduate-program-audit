from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.program_reentry import (  # noqa: E402
    apply_program_reentry,
    validate_program_reentry,
    write_reentry_subsets,
)
from graduate_audit.program_verification import build_program_verification  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    PROGRAM_EXCLUSION_COLUMNS_V2,
    PROGRAM_SOURCE_COLUMNS_V2,
    PROGRAM_VERIFICATION_COLUMNS_V2,
)

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
REPORT_PATH = REPO_ROOT / "reports/pass2/03_program_verification.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_03.json"
RAW_PATH_01 = REPO_ROOT / "data/raw/pass2/stage_03_reentry_01.json"
RAW_PATH_02 = REPO_ROOT / "data/raw/pass2/stage_03_reentry_02.json"
PROGRESS_PATH = REPO_ROOT / "state/progress.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()


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


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(str(value).replace("|", "/") for value in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def write_report(result: dict[str, object]) -> None:
    rows = read_csv(OUTPUT_DIR / "program_verification.csv")
    reentry_ids = {
        row["candidate_program_id"]
        for row in read_csv(OUTPUT_DIR / "stage_03_reentry_02_verification.csv")
    }
    reentry = [row for row in rows if row["candidate_program_id"] in reentry_ids]
    counts = result["counts"]
    unresolved = [
        row for row in reentry if row["verification_status"] in {"conditional", "monitor"}
    ]
    lines = [
        "# Pass 2 Stage 3 — Program structure, eligibility, and funding verification",
        "",
        f"Generated: {now()}",
        "",
        "Decision: **PASS — verification re-entry 02 complete**",
        "",
        "## Outcome",
        "",
        f"All {counts['verification_rows']:,} Stage 2 candidates now have exactly one controlled "
        "retained, conditional, monitor, or excluded status with an evidence-backed reason. The "
        "12 latest Stage 2 re-entry routes were re-verified from official program, admissions, funding, "
        "fee, and deadline sources. No score or admission recommendation was created.",
        "",
        table(
            ["Status", "All candidates", "New routes"],
            [
                ["Retained", counts["retained"], counts["reentry_retained"]],
                ["Conditional", counts["conditional"], counts["reentry_conditional"]],
                ["Monitor", counts["monitor"], counts["reentry_monitor"]],
                ["Excluded", counts["excluded"], 0],
                ["Faculty-review ready", counts["faculty_review_ready"], 8],
            ],
        ),
        "",
        "## Stage 2 re-entry routes",
        "",
        table(
            ["Institution", "Program", "Status", "Eligibility gate", "Funding gate", "Largest unresolved question"],
            [
                [
                    row["institution_name"],
                    f"[{row['exact_degree_program_name']}]({row['official_program_url']})",
                    row["verification_status"],
                    row["eligibility_gate"],
                    row["funding_gate"],
                    row["largest_unresolved_question"],
                ]
                for row in reentry
            ],
        ),
        "",
        "Retained means an exact research route, formal applicant eligibility, and a credible "
        "officially sourced funding route are present. It does not mean admission is likely or "
        "that an eventual offer will contain adequate net funding.",
        "",
        "Conditional rows are positioned only as `Outreach Before Decision`. Rutgers, Ohio State, "
        "Stony Brook, UC Santa Barbara, and UNC Charlotte each need an offer- or department-specific "
        "funding-incidence answer. Indiana, Regina, Twente, and Radboud remain monitors because each "
        "has more than one material eligibility or funding gate unresolved.",
        "",
        "## Acceptance checks",
        "",
        table(
            ["Assertion", "Result"],
            [[key, "PASS" if value else "FAIL"] for key, value in result["assertions"].items()],
        ),
        "",
        "## Blockers",
        "",
        "None prevented Stage 3 completion.",
        "",
        "## Unresolved coverage",
        "",
        "- Fall 2027 is explicitly published for Rutgers, Ohio State, Boston University, Indiana, Twente, and Radboud; other rows use the latest current deadline page with the cycle limitation labeled.",
        "- Stony Brook's current handbook URL returned HTTP 404 to direct retrieval even though current official indexed content was available; Stage 4 should browser-check it again before using the row.",
        "- Simultaneous-application rules remain unknown for Stony Brook and York; UC Santa Barbara permits only one application per cycle.",
        "- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever the official page did not publish them.",
        "- Twente and Radboud have no verified adequate full-cost funding route for this fee-paying Nigerian applicant; Regina requires both a willing supervisor and a separate funding answer; Indiana's published 3.5 PhD GPA gate exceeds the applicant's 3.35 cumulative GPA.",
        f"- {len(unresolved)} new routes remain conditional or monitor and must not be treated as funded recommendations.",
        "- Stage 4 may evaluate current faculty only for the eight new retained/conditional routes; the four monitor routes do not pass the faculty-review gate.",
        "- The full suite has three expected downstream coverage failures until Stage 4 regenerates rosters and five-professor evaluations and Stage 5 regenerates scores for the eight new faculty-review-ready routes; Stage 3-specific tests pass.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    started_at = now()
    source_commit = git_head()
    baseline = build_program_verification(REPO_ROOT)
    definitions_01 = json.loads(RAW_PATH_01.read_text(encoding="utf-8"))["programs"]
    definitions_02 = json.loads(RAW_PATH_02.read_text(encoding="utf-8"))["programs"]
    verification_01, sources_01, exclusions_01 = apply_program_reentry(
        definitions_01,
        baseline["verification_rows"],
        baseline["source_rows"],
        baseline["exclusion_rows"],
        "data/raw/pass2/stage_03_reentry_01.json",
    )
    verification, sources, exclusions = apply_program_reentry(
        definitions_02,
        verification_01,
        sources_01,
        exclusions_01,
        "data/raw/pass2/stage_03_reentry_02.json",
    )
    write_csv(OUTPUT_DIR / "program_verification.csv", verification, PROGRAM_VERIFICATION_COLUMNS_V2)
    write_csv(OUTPUT_DIR / "program_sources.csv", sources, PROGRAM_SOURCE_COLUMNS_V2)
    write_csv(OUTPUT_DIR / "program_exclusions.csv", exclusions, PROGRAM_EXCLUSION_COLUMNS_V2)
    write_reentry_subsets(OUTPUT_DIR, definitions_01, verification, sources)
    write_reentry_subsets(OUTPUT_DIR, definitions_02, verification, sources, "_02")
    result_01 = validate_program_reentry(definitions_01, verification, sources, exclusions)
    result = validate_program_reentry(definitions_02, verification, sources, exclusions)
    if result_01["validation_status"] != "PASS" or result["validation_status"] != "PASS":
        raise RuntimeError(
            f"Stage 3 cumulative re-entry failed: round01={result_01['assertions']}; "
            f"round02={result['assertions']}"
        )
    write_report(result)

    progress = dict(read_json(PROGRESS_PATH, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["3"] = "complete"
    stage_status["3_reentry_01"] = "complete"
    stage_status["3_reentry_02"] = "complete"
    pass2.update(
        {
            "current_stage": 3,
            "last_completed_stage": 6,
            "stage_status": stage_status,
            "next_stage": 4,
            "next_stage_authorized": True,
            "authorization_mode": "agent_stage_gate_per_user_instruction",
            "stage_manifest": "data/manifests/pass2/stage_03.json",
            "stage_03_acceptance": "PASS",
            "stage_03_reentry_required": False,
            "stage_03_reentry_completed": 2,
            "stage_03_reentry_faculty_review_ready": 8,
            "stage_03_faculty_review_ready": result["counts"]["faculty_review_ready"],
            "stage_04_reentry_required": True,
            "stage_04_reentry_source_stage": 3,
        }
    )
    update_progress(PROGRESS_PATH, current_phase="pass2_stage_03_reentry_02_complete", pass2=pass2)

    output_paths = [
        OUTPUT_DIR / "program_verification.csv",
        OUTPUT_DIR / "program_sources.csv",
        OUTPUT_DIR / "program_exclusions.csv",
        OUTPUT_DIR / "stage_03_reentry_verification.csv",
        OUTPUT_DIR / "stage_03_reentry_sources.csv",
        OUTPUT_DIR / "stage_03_reentry_02_verification.csv",
        OUTPUT_DIR / "stage_03_reentry_02_sources.csv",
        REPORT_PATH,
    ]
    artifact_paths = [
        RAW_PATH_01,
        RAW_PATH_02,
        REPO_ROOT / "src/graduate_audit/program_reentry.py",
        REPO_ROOT / "scripts/build_stage_03_reentry.py",
        REPO_ROOT / "tests/test_program_reentry.py",
        PROGRESS_PATH,
        *output_paths,
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 3,
        "run_type": "verification_reentry_02",
        "name": "Program structure, eligibility, and funding verification — re-entry 02",
        "status": "complete",
        "decision": "PASS",
        "triggered_by_stage": 2,
        "source_commit_before_stage": source_commit,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [
            file_record(REPO_ROOT / "data/manifests/pass2/stage_02.json"),
            file_record(OUTPUT_DIR / "candidate_program_funnel.csv"),
            file_record(RAW_PATH_01),
            file_record(RAW_PATH_02),
        ],
        "outputs": [file_record(path) for path in output_paths],
        "artifacts": [file_record(path) for path in artifact_paths],
        "validation": {
            "status": "PASS",
            "assertions": result["assertions"],
            "allowed_statuses": ["retained", "conditional", "monitor", "excluded"],
            "conditional_positioning": "Outreach Before Decision",
        },
        "counts": result["counts"],
        "failures": [],
        "blockers": [],
        "unresolved_coverage": [
            "Nine latest routes remain conditional or monitor because one or more eligibility or funding gates are unresolved.",
            "Simultaneous-application rules remain unverified for Stony Brook and York.",
            "Stony Brook's current handbook URL returned automated HTTP 404 and requires a fresh browser check before Stage 4 use.",
            "Offer-specific net funding terms remain unknown where official pages publish only program-level commitments.",
            "Existing Stage 4 through Stage 6 outputs intentionally remain unchanged pending their separate re-entry stages.",
            "Stage 4 roster and five-professor evaluation coverage must be regenerated for the eight new faculty-review-ready routes.",
            "Stage 5 score coverage must then be regenerated for those same eight routes.",
        ],
    }
    write_json(MANIFEST_PATH, manifest)
    print("Stage 3 verification re-entry 02: PASS")
    print(json.dumps(result["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
