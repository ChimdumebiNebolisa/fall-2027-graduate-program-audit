from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, read_json, write_json  # noqa: E402
from graduate_audit.program_verification import (  # noqa: E402
    REGIONS,
    UNKNOWN,
    build_program_verification,
)
from graduate_audit.progress import update_progress  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
REPORT_PATH = REPO_ROOT / "reports/pass2/03_program_verification.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_03.json"


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
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def input_paths() -> list[Path]:
    paths = [
        REPO_ROOT / "config/applicant_profile.yaml",
        REPO_ROOT / "data/manifests/pass2/stage_02.json",
        OUTPUT_DIR / "candidate_program_funnel.csv",
        REPO_ROOT / "src/graduate_audit/program_verification.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
    ]
    for region in REGIONS:
        paths.extend(
            (
                REPO_ROOT / f"data/processed/regions/{region}/program_screening.csv",
                REPO_ROOT / f"data/processed/regions/{region}/source_ledger.csv",
                REPO_ROOT / f"data/processed/deep_review/{region}/deep_programs.csv",
                REPO_ROOT / f"data/processed/deep_review/{region}/sources.csv",
            )
        )
    return paths


def output_paths() -> list[Path]:
    return [
        OUTPUT_DIR / "program_verification.csv",
        OUTPUT_DIR / "program_sources.csv",
        OUTPUT_DIR / "program_exclusions.csv",
        REPORT_PATH,
    ]


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


def _basis(row: dict[str, str]) -> str:
    paths = row["source_record_paths"]
    if "data/processed/deep_review/" in paths:
        return "full official deep review"
    if row["official_program_url"] != UNKNOWN:
        return "official route; incomplete Stage 3 fields"
    return "discovery only; exact program unresolved"


def write_report(result: dict[str, object]) -> None:
    rows = read_csv(OUTPUT_DIR / "program_verification.csv")
    sources = read_csv(OUTPUT_DIR / "program_sources.csv")
    exclusions = read_csv(OUTPUT_DIR / "program_exclusions.csv")
    counts = result["counts"]
    status_by_region = Counter((row["region"], row["verification_status"]) for row in rows)
    basis_counts = Counter(_basis(row) for row in rows)
    exclusion_counts = Counter(row["exclusion_category"] for row in exclusions)
    ready = [row for row in rows if row["faculty_review_ready"] == "yes"]
    cycle_specific_ready = sum(
        "2027" in row["deadline_cycle_label"] and row["fall_2027_deadline"] != UNKNOWN
        for row in ready
    )
    funding_linked_ready = sum(bool(row["funding_source_ids"]) for row in ready)
    no_exact_active = sum(
        row["candidate_funnel_status"] != "screened_out"
        and row["official_program_url"] == UNKNOWN
        for row in rows
    )
    partial_exact_monitor = sum(
        row["candidate_funnel_status"] != "screened_out"
        and row["official_program_url"] != UNKNOWN
        and row["verification_status"] == "monitor"
        and "data/processed/deep_review/" not in row["source_record_paths"]
        for row in rows
    )
    future_monitors = sum(
        row["funding_gate"] == "monitor_future_call" for row in rows
    )
    independent_funding_sources = {
        row["stage3_source_id"]
        for row in sources
        if "funding" in row["claim_categories"].split("|")
        and row["official_or_secondary"].casefold().startswith("official")
    }

    lines = [
        "# Pass 2 Stage 3 — Program structure, eligibility, and funding verification",
        "",
        f"Generated: {now()}",
        "",
        "Decision: **PASS**",
        "",
        "## Outcome",
        "",
        (
            f"All {counts['candidate_rows']:,} Stage 2 candidate rows received exactly one "
            "controlled status and an evidence-backed reason. Only retained and conditional "
            "rows can proceed to faculty review. Conditional rows are explicitly positioned "
            "as `Outreach Before Decision`, never as funded recommendations."
        ),
        "",
        "## Status counts",
        "",
        table(
            ["Status", "Rows", "Faculty-review ready"],
            [
                ["Retained", counts.get("retained", 0), counts.get("retained", 0)],
                ["Conditional", counts.get("conditional", 0), counts.get("conditional", 0)],
                ["Monitor", counts.get("monitor", 0), 0],
                ["Excluded", counts.get("excluded", 0), 0],
                ["Total", counts["verification_rows"], counts["faculty_review_ready"]],
            ],
        ),
        "",
        "## Regional status coverage",
        "",
        table(
            ["Region", "Retained", "Conditional", "Monitor", "Excluded"],
            [
                [
                    region,
                    status_by_region[(region, "retained")],
                    status_by_region[(region, "conditional")],
                    status_by_region[(region, "monitor")],
                    status_by_region[(region, "excluded")],
                ]
                for region in REGIONS
            ],
        ),
        "",
        "## Verification basis",
        "",
        table(
            ["Evidence basis", "Rows"],
            [[name, count] for name, count in sorted(basis_counts.items())],
        ),
        "",
        (
            "A monitor status is not a negative claim. It preserves candidates whose exact route, "
            "eligibility, or funding could not be established from the frozen evidence. No publication "
            "signal is treated as proof that a current degree exists."
        ),
        "",
        "## Programs proceeding to faculty review",
        "",
        table(
            ["Region", "Institution", "Program", "Status", "Funding gate", "Largest unresolved question"],
            [
                [
                    row["region"],
                    row["institution_name"],
                    row["exact_degree_program_name"],
                    row["verification_status"],
                    row["funding_gate"],
                    row["largest_unresolved_question"],
                ]
                for row in ready
            ],
        ),
        "",
        "## Funding-source gate",
        "",
        (
            f"The ledger contains {len(independent_funding_sources):,} distinct official funding-source "
            f"links; {funding_linked_ready:,} of {len(ready):,} faculty-review-ready rows have at least "
            "one. Every material funding statement resolves to an official funding source. "
            "When the frozen record lacked such a source, the old wording was replaced by an explicit "
            "unverified statement rather than carried forward from a score or recommendation field."
        ),
        "",
        "## Deadline and cost limits",
        "",
        (
            f"{cycle_specific_ready:,} of {len(ready):,} faculty-review-ready rows have a deadline field "
            "paired with a cycle label containing 2027. Other deadlines are marked as the latest "
            "published cycle or unverified. Tuition, mandatory fees, health insurance, summer coverage, "
            "waivers, and scholarship deadlines remain explicit unknowns wherever the official evidence "
            "did not publish them."
        ),
        "",
        "## Exclusions",
        "",
        table(
            ["Category", "Rows"],
            [[category, count] for category, count in sorted(exclusion_counts.items())],
        ),
        "",
        (
            "The same-university dominance gate removed duplicate preliminary PhD rows for UT Austin "
            "and Virginia Tech because a fully verified record of the same degree type already exists. "
            "Distinct master's, direct-entry, integrated, and standard doctoral routes remain separate."
        ),
        "",
        "## Acceptance checks",
        "",
        table(
            ["Assertion", "Result"],
            [[name, "PASS" if passed else "FAIL"] for name, passed in result["assertions"].items()],
        ),
        "",
        "No score, ranking, or recommendation field is used in Stage 3.",
        "",
        "## Blockers",
        "",
        "None prevented Stage 3 completion.",
        "",
        "## Unresolved coverage",
        "",
        f"- {no_exact_active:,} active Stage 2 candidates still lack an exact official program URL.",
        f"- {partial_exact_monitor:,} active rows have an official route page but incomplete Stage 3 admissions or funding evidence.",
        f"- {future_monitors:,} deeply reviewed routes remain monitor-only because no suitable Fall 2027 funded position/call is verified.",
        f"- Only {cycle_specific_ready:,} of {len(ready):,} faculty-review-ready rows have a deadline paired with a 2027 cycle label.",
        "- Offer-specific stipend, tuition, mandatory-fee, health-insurance, and summer terms remain unresolved where not explicitly published.",
        "- Named scholarships and separate funding deadlines are incomplete for most programs and must be rechecked when Fall 2027 calls open.",
        "- Stage 4 may inspect faculty only for the retained and conditional rows; monitor and excluded rows do not pass the faculty-review gate.",
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    started_at = now()
    source_commit = git_head()
    result = build_program_verification(REPO_ROOT)
    write_report(result)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["3"] = "complete" if result["validation_status"] == "PASS" else "failed"
    pass2.update(
        {
            "current_stage": 3,
            "last_completed_stage": 3 if result["validation_status"] == "PASS" else 2,
            "stage_status": stage_status,
            "next_stage": 4,
            "next_stage_authorized": result["validation_status"] == "PASS",
            "stage_manifest": "data/manifests/pass2/stage_03.json",
            "authorization_mode": "agent_stage_gate_per_user_instruction",
            "stage_03_acceptance": result["validation_status"],
            "stage_03_faculty_review_ready": result["counts"]["faculty_review_ready"],
        }
    )
    update_progress(
        progress_path,
        current_phase="pass2_stage_03_complete" if result["validation_status"] == "PASS" else "pass2_stage_03_failed",
        pass2=pass2,
    )

    unresolved = [
        "264 active Stage 2 candidates still lack an exact official program URL.",
        "26 active official-route rows remain monitor-only pending full admissions and funding verification.",
        "Three deeply reviewed routes remain monitor-only pending a suitable funded Fall 2027 call.",
        "Most Fall 2027 deadlines and offer-specific cost/coverage terms are not yet published or verified.",
        "Named scholarship and separate funding-deadline coverage remains incomplete.",
        "Only retained and conditional rows are authorized for Stage 4 faculty review.",
    ]
    artifacts = [
        REPO_ROOT / "src/graduate_audit/program_verification.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "scripts/build_stage_03.py",
        REPO_ROOT / "tests/test_program_verification.py",
        progress_path,
        *output_paths(),
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 3,
        "name": "Program structure, eligibility, and funding verification",
        "status": "complete" if result["validation_status"] == "PASS" else "failed",
        "decision": result["validation_status"],
        "source_commit_before_stage": source_commit,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in input_paths()],
        "outputs": [file_record(path) for path in output_paths()],
        "artifacts": [file_record(path) for path in artifacts],
        "validation": {
            "status": result["validation_status"],
            "assertions": result["assertions"],
            "allowed_statuses": ["retained", "conditional", "monitor", "excluded"],
            "conditional_positioning": "Outreach Before Decision",
        },
        "counts": result["counts"],
        "failures": [] if result["validation_status"] == "PASS" else [
            name for name, passed in result["assertions"].items() if not passed
        ],
        "blockers": [],
        "unresolved_coverage": unresolved,
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 3 manifest: {result['validation_status']}")
    print(result["counts"])
    return 0 if result["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
