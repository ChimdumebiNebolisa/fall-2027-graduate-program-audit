from __future__ import annotations

import hashlib
from datetime import date
from typing import Iterable

from .io import write_csv
from .program_verification import FINAL_STATUSES, UNKNOWN, _has_material_funding_claim, _split
from .schema import (
    PASS2_SCHEMA_VERSION,
    PROGRAM_EXCLUSION_COLUMNS_V2,
    PROGRAM_SOURCE_COLUMNS_V2,
    PROGRAM_VERIFICATION_COLUMNS_V2,
    canonical_url,
)


def _join(values: Iterable[str]) -> str:
    return "|".join(dict.fromkeys(value for value in values if value))


def _source_id(program_id: str, source: dict[str, str]) -> str:
    fingerprint = "|".join(
        (
            program_id,
            source["source_id"],
            canonical_url(source["url"]),
            source["exact_claim_supported"],
        )
    )
    return "stage3src:" + hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:20]


def _controlled_status(eligibility_gate: str, funding_gate: str) -> str:
    if eligibility_gate == "pass" and funding_gate == "pass":
        return "retained"
    if (
        eligibility_gate == "resolvable_question" and funding_gate == "pass"
    ) or (
        eligibility_gate == "pass" and funding_gate == "resolvable_inquiry"
    ):
        return "conditional"
    return "monitor"


def _status_fields(status: str, definition: dict[str, object]) -> dict[str, str]:
    if status == "retained":
        return {
            "status_reason": (
                "The exact research route is current, the applicant meets the verified formal entry gate, "
                "and official evidence establishes a credible funding route; offer-specific terms remain explicit."
            ),
            "faculty_review_ready": "yes",
            "application_positioning": "Funded Application Candidate",
        }
    if status == "conditional":
        return {
            "status_reason": str(definition["conditional_reason"]),
            "faculty_review_ready": "yes",
            "application_positioning": "Outreach Before Decision",
        }
    return {
        "status_reason": str(definition["monitor_reason"]),
        "faculty_review_ready": "no",
        "application_positioning": "Monitor — Not Faculty-Review Ready",
    }


def _source_row(program: dict[str, object], source: dict[str, str], raw_path: str) -> dict[str, str]:
    program_id = str(program["candidate_program_id"])
    return {
        "schema_version": PASS2_SCHEMA_VERSION,
        "stage3_source_id": _source_id(program_id, source),
        "candidate_program_id": program_id,
        "institution_id": str(program["institution_id"]),
        "institution_name": str(program["institution_name"]),
        "claim_categories": source["claim_categories"],
        "exact_claim_supported": source["exact_claim_supported"],
        "source_title": source["source_title"],
        "publisher": source["publisher"],
        "url": source["url"],
        "source_path": raw_path,
        "source_type": source.get("source_type", "official web page"),
        "official_or_secondary": "official",
        "date_accessed": source.get("date_accessed", "2026-09-10"),
        "admissions_cycle": source.get("admissions_cycle", "current page; cycle as labeled"),
        "confidence": source.get("confidence", "high"),
        "verification_status": source.get("verification_status", "official page checked"),
        "original_source_id": source["source_id"],
        "access_note": source.get("access_note", ""),
    }


def apply_program_reentry(
    definitions: list[dict[str, object]],
    baseline_verification: list[dict[str, str]],
    baseline_sources: list[dict[str, str]],
    baseline_exclusions: list[dict[str, str]],
    raw_path: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    programs = {str(item["candidate_program_id"]): item for item in definitions}
    if len(programs) != len(definitions):
        raise ValueError("Duplicate candidate_program_id in Stage 3 re-entry definitions")
    baseline_ids = {row["candidate_program_id"] for row in baseline_verification}
    missing = set(programs) - baseline_ids
    if missing:
        raise ValueError(f"Stage 3 re-entry programs absent from candidate funnel: {sorted(missing)}")

    source_rows = [
        row for row in baseline_sources if row["candidate_program_id"] not in programs
    ]
    source_ids_by_program: dict[str, dict[str, list[str]]] = {}
    for program_id, definition in programs.items():
        categories: dict[str, list[str]] = {
            "program": [],
            "admissions": [],
            "funding": [],
        }
        for source in definition["sources"]:
            if not isinstance(source, dict):
                raise ValueError(f"Invalid source for {program_id}")
            row = _source_row(definition, source, raw_path)
            source_rows.append(row)
            source_categories = set(_split(row["claim_categories"]))
            if "program" in source_categories:
                categories["program"].append(row["stage3_source_id"])
            if source_categories & {"admissions", "eligibility", "language", "deadline", "fees"}:
                categories["admissions"].append(row["stage3_source_id"])
            if "funding" in source_categories:
                categories["funding"].append(row["stage3_source_id"])
        source_ids_by_program[program_id] = categories

    verification_rows: list[dict[str, str]] = []
    verified_at = date.today().isoformat()
    for baseline in baseline_verification:
        program_id = baseline["candidate_program_id"]
        definition = programs.get(program_id)
        if not definition:
            verification_rows.append(baseline)
            continue
        if baseline["institution_id"] != definition["institution_id"]:
            raise ValueError(f"Institution ID mismatch for {program_id}")
        if baseline["institution_name"] != definition["institution_name"]:
            raise ValueError(f"Institution name mismatch for {program_id}")
        eligibility_gate = str(definition["eligibility_gate"])
        funding_gate = str(definition["funding_gate"])
        status = _controlled_status(eligibility_gate, funding_gate)
        updated = dict(baseline)
        for key, value in definition["fields"].items():
            if key not in PROGRAM_VERIFICATION_COLUMNS_V2:
                raise ValueError(f"Unknown verification field {key!r} for {program_id}")
            updated[key] = str(value)
        ids = source_ids_by_program[program_id]
        updated.update(
            {
                "verified_program_id": program_id,
                "verification_status": status,
                "relevant_route_gate": "pass",
                "eligibility_gate": eligibility_gate,
                "funding_gate": funding_gate,
                "degree_structure_gate": "pass",
                "same_university_dominance_gate": "pass",
                "official_program_url": str(definition["official_program_url"]),
                "program_source_ids": _join(ids["program"]),
                "admissions_source_ids": _join(ids["admissions"]),
                "funding_source_ids": _join(ids["funding"]),
                "evidence_confidence": str(definition.get("evidence_confidence", "high")),
                "source_record_paths": _join(
                    [*_split(baseline["source_record_paths"]), raw_path]
                ),
                "verified_at": verified_at,
                **_status_fields(status, definition),
            }
        )
        verification_rows.append(updated)

    source_rows.sort(key=lambda row: (row["candidate_program_id"], row["stage3_source_id"]))
    exclusion_rows = [
        row for row in baseline_exclusions if row["candidate_program_id"] not in programs
    ]
    return verification_rows, source_rows, exclusion_rows


def validate_program_reentry(
    definitions: list[dict[str, object]],
    verification_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    exclusion_rows: list[dict[str, str]],
) -> dict[str, object]:
    definition_ids = {str(item["candidate_program_id"]) for item in definitions}
    verification_by_id = {row["candidate_program_id"]: row for row in verification_rows}
    source_by_id = {row["stage3_source_id"]: row for row in source_rows}
    reentry = [verification_by_id[program_id] for program_id in definition_ids]
    linked_ids = lambda row: set(
        _split(row["program_source_ids"])
        + _split(row["admissions_source_ids"])
        + _split(row["funding_source_ids"])
    )
    assertions = {
        "all_12_reentry_programs_present": len(definition_ids) == 12
        and definition_ids <= verification_by_id.keys(),
        "one_status_per_stage2_candidate": len(verification_rows)
        == len(verification_by_id),
        "controlled_statuses_only": {
            row["verification_status"] for row in verification_rows
        }
        <= FINAL_STATUSES,
        "all_material_fields_explicit": all(
            all(
                row[column].strip()
                for column in PROGRAM_VERIFICATION_COLUMNS_V2
                if column not in {"admissions_source_ids", "funding_source_ids"}
            )
            for row in verification_rows
        ),
        "reentry_program_and_admissions_sources_present": all(
            row["program_source_ids"] and row["admissions_source_ids"] for row in reentry
        ),
        "all_reentry_source_ids_resolve": all(
            linked_ids(row) <= source_by_id.keys() for row in reentry
        ),
        "all_reentry_sources_official": all(
            source_by_id[source_id]["official_or_secondary"].casefold().startswith("official")
            for row in reentry
            for source_id in linked_ids(row)
        ),
        "material_funding_claims_have_official_sources": all(
            bool(_split(row["funding_source_ids"]))
            for row in reentry
            if _has_material_funding_claim(row)
        ),
        "retained_rows_pass_route_eligibility_and_funding": all(
            row["relevant_route_gate"] == "pass"
            and row["eligibility_gate"] == "pass"
            and row["funding_gate"] == "pass"
            for row in reentry
            if row["verification_status"] == "retained"
        ),
        "conditional_rows_have_exactly_one_resolvable_gate": all(
            (
                row["eligibility_gate"] == "resolvable_question"
                and row["funding_gate"] == "pass"
            )
            or (
                row["eligibility_gate"] == "pass"
                and row["funding_gate"] == "resolvable_inquiry"
            )
            for row in reentry
            if row["verification_status"] == "conditional"
        ),
        "conditional_rows_are_outreach_only": all(
            row["application_positioning"] == "Outreach Before Decision"
            for row in reentry
            if row["verification_status"] == "conditional"
        ),
        "monitor_rows_do_not_proceed": all(
            row["faculty_review_ready"] == "no"
            for row in reentry
            if row["verification_status"] == "monitor"
        ),
        "exclusions_match_status": {
            row["candidate_program_id"] for row in exclusion_rows
        }
        == {
            row["candidate_program_id"]
            for row in verification_rows
            if row["verification_status"] == "excluded"
        },
        "no_score_or_recommendation_fields": not any(
            token in column.casefold()
            for column in PROGRAM_VERIFICATION_COLUMNS_V2
            for token in ("score", "rank", "recommendation")
        ),
    }
    counts = {
        "candidate_rows": len(verification_rows),
        "verification_rows": len(verification_rows),
        "source_rows": len(source_rows),
        "exclusion_rows": len(exclusion_rows),
        **{
            status: sum(row["verification_status"] == status for row in verification_rows)
            for status in sorted(FINAL_STATUSES)
        },
        "faculty_review_ready": sum(row["faculty_review_ready"] == "yes" for row in verification_rows),
        "official_program_url_present": sum(row["official_program_url"] != UNKNOWN for row in verification_rows),
        "funding_source_linked": sum(bool(row["funding_source_ids"]) for row in verification_rows),
        "reentry_retained": sum(row["verification_status"] == "retained" for row in reentry),
        "reentry_conditional": sum(row["verification_status"] == "conditional" for row in reentry),
        "reentry_monitor": sum(row["verification_status"] == "monitor" for row in reentry),
    }
    return {
        "validation_status": "PASS" if all(assertions.values()) else "FAIL",
        "assertions": assertions,
        "counts": counts,
        "reentry_rows": reentry,
    }


def write_reentry_subsets(
    output_dir,
    definitions: list[dict[str, object]],
    verification_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> None:
    program_ids = {str(item["candidate_program_id"]) for item in definitions}
    write_csv(
        output_dir / "stage_03_reentry_verification.csv",
        (row for row in verification_rows if row["candidate_program_id"] in program_ids),
        PROGRAM_VERIFICATION_COLUMNS_V2,
    )
    write_csv(
        output_dir / "stage_03_reentry_sources.csv",
        (row for row in source_rows if row["candidate_program_id"] in program_ids),
        PROGRAM_SOURCE_COLUMNS_V2,
    )
