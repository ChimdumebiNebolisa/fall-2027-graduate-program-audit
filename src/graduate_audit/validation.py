from __future__ import annotations

from collections import Counter
from pathlib import Path

from .io import read_csv
from .schema import INSTITUTION_STATUSES, RECRUITING_STATUSES


def validate_outputs(output_dir: str | Path) -> dict[str, object]:
    root = Path(output_dir)
    errors: list[str] = []
    warnings: list[str] = []

    institution_path = root / "institution_universe.csv"
    program_path = root / "program_screening.csv"
    exclusion_path = root / "exclusion_log.csv"
    professor_path = root / "professor_evidence.csv"

    institutions = read_csv(institution_path) if institution_path.exists() else []
    programs = read_csv(program_path) if program_path.exists() else []
    exclusions = read_csv(exclusion_path) if exclusion_path.exists() else []
    professors = read_csv(professor_path) if professor_path.exists() else []

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

    professor_programs = {row.get("program_id") for row in professors if row.get("can_supervise_program", "").lower() in {"yes", "true", "verified"}}
    for row_number, row in enumerate(programs, start=2):
        if row.get("screening_decision") == "retained":
            if not row.get("official_program_url"):
                errors.append(f"retained program row {row_number} has no official URL")
            if not row.get("funding_status"):
                errors.append(f"retained program row {row_number} has no funding determination")
            if not row.get("direct_from_bachelors_eligible"):
                errors.append(f"retained program row {row_number} has no eligibility determination")
            if row.get("program_id") not in professor_programs:
                errors.append(f"retained program row {row_number} has no verified supervisor match")

    for row_number, row in enumerate(professors, start=2):
        recruiting = row.get("recruiting_status")
        if recruiting and recruiting not in RECRUITING_STATUSES:
            errors.append(f"professor row {row_number} has invalid recruiting status {recruiting}")
        if recruiting == "Confirmed recruiting" and not row.get("recruiting_evidence"):
            errors.append(f"professor row {row_number} is confirmed recruiting without evidence")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "institutions": len(institutions),
            "programs": len(programs),
            "exclusions": len(exclusions),
            "professors": len(professors),
        },
    }

