from __future__ import annotations

from collections import Counter
from pathlib import Path

from .io import read_csv
from .schema import INSTITUTION_STATUSES, RECRUITING_STATUSES

EXCLUDED_PROGRAM_DECISIONS = {"excluded", "screened_out", "do_not_apply"}
RETAINED_PROGRAM_DECISIONS = {"retained"}


def _explicit_supervision(row: dict[str, str]) -> bool:
    supervision = row.get("can_supervise_program", "").strip().lower()
    return supervision in {"yes", "true", "verified"} or supervision.startswith(
        ("yes -", "yes;", "verified;")
    )


def _verified_supervision(row: dict[str, str]) -> bool:
    verification = row.get("verification_status", "").strip().lower()
    return (
        _explicit_supervision(row)
        and "verified" in verification
        and bool(row.get("official_faculty_url", "").strip())
    )


def validate_outputs(output_dir: str | Path) -> dict[str, object]:
    root = Path(output_dir)
    errors: list[str] = []
    warnings: list[str] = []

    institution_path = root / "institution_universe.csv"
    program_path = root / "program_screening.csv"
    exclusion_path = root / "exclusion_log.csv"
    professor_path = root / "professor_evidence.csv"
    source_path = root / "source_ledger.csv"
    draft_path = root / "outreach_drafts.csv"

    institutions = read_csv(institution_path) if institution_path.exists() else []
    programs = read_csv(program_path) if program_path.exists() else []
    exclusions = read_csv(exclusion_path) if exclusion_path.exists() else []
    professors = read_csv(professor_path) if professor_path.exists() else []
    sources = read_csv(source_path) if source_path.exists() else []
    drafts = read_csv(draft_path) if draft_path.exists() else []

    ids = [row.get("institution_id", "") for row in institutions]
    duplicates = [key for key, count in Counter(ids).items() if key and count > 1]
    if duplicates:
        errors.append(f"duplicate institution IDs: {duplicates[:10]}")
    for row_number, row in enumerate(institutions, start=2):
        if not row.get("screening_status"):
            errors.append(f"institution row {row_number} has no screening status")
        elif row["screening_status"] not in INSTITUTION_STATUSES:
            errors.append(f"institution row {row_number} has invalid status {row['screening_status']}")
        if row.get("screening_status") in {"excluded", "inactive", "not_recognized", "no_graduate_degree_authority", "no_relevant_graduate_field", "program_screened_out"} and not row.get("exclusion_reason"):
            errors.append(f"excluded institution row {row_number} has no reason")

    for row_number, row in enumerate(exclusions, start=2):
        if not row.get("primary_exclusion_reason"):
            errors.append(f"exclusion row {row_number} has no reason")

    professor_programs = {
        row.get("program_id")
        for row in professors
        if _verified_supervision(row)
    }
    for row_number, row in enumerate(programs, start=2):
        decision = row.get("screening_decision", "").lower()
        if decision in EXCLUDED_PROGRAM_DECISIONS and not row.get("exclusion_reason"):
            errors.append(f"excluded program row {row_number} has no reason")
        if decision in RETAINED_PROGRAM_DECISIONS:
            if not row.get("official_program_url"):
                errors.append(f"retained program row {row_number} has no official URL")
            if not row.get("funding_status"):
                errors.append(f"retained program row {row_number} has no funding determination")
            if not row.get("direct_from_bachelors_eligible"):
                errors.append(f"retained program row {row_number} has no eligibility determination")
            if row.get("program_id") not in professor_programs:
                errors.append(f"retained program row {row_number} has no verified supervisor match")
            if not row.get("international_student_eligible"):
                errors.append(f"retained program row {row_number} has no international eligibility determination")
            if row.get("degree_type") == "Coursework or professional master's":
                errors.append(f"retained program row {row_number} is coursework-only")
            deadline = row.get("fall_2027_deadline", "")
            deadline_status = row.get("deadline_cycle_status", "")
            if deadline and not deadline_status:
                errors.append(f"retained program row {row_number} has an unlabeled deadline cycle")

    for row_number, row in enumerate(professors, start=2):
        recruiting = row.get("recruiting_status")
        if recruiting and recruiting not in RECRUITING_STATUSES:
            errors.append(f"professor row {row_number} has invalid recruiting status {recruiting}")
        if recruiting == "Confirmed recruiting" and not row.get("recruiting_evidence"):
            errors.append(f"professor row {row_number} is confirmed recruiting without evidence")
        if _explicit_supervision(row):
            if not row.get("official_faculty_url"):
                errors.append(f"supervisor row {row_number} has no official faculty URL")
            if not row.get("appointment_status"):
                errors.append(f"supervisor row {row_number} has no current-appointment check")

    for row_number, row in enumerate(sources, start=2):
        if not row.get("url") or not row.get("exact_claim_supported"):
            warnings.append(f"source row {row_number} lacks a URL or exact supported claim")

    required_signoff = "yours sincerely,\nChimdumebi Mitchell Nebolisa"
    for row_number, row in enumerate(drafts, start=2):
        body = (row.get("body") or row.get("draft") or "").strip()
        if not body.endswith(required_signoff):
            errors.append(f"outreach draft row {row_number} has an invalid sign-off")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "institutions": len(institutions),
            "programs": len(programs),
            "exclusions": len(exclusions),
            "professors": len(professors),
            "sources": len(sources),
            "outreach_drafts": len(drafts),
        },
    }
