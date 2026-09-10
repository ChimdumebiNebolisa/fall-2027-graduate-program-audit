from __future__ import annotations

from pathlib import Path

from graduate_audit.io import read_csv
from graduate_audit.program_verification import (
    FINAL_STATUSES,
    _has_material_funding_claim,
    _positive_funding,
    _split,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"


def test_funding_classifier_is_conservative() -> None:
    assert _positive_funding("Guaranteed five-year support package")
    assert _positive_funding("Credible full-support commitment")
    assert not _positive_funding("Funding is not guaranteed")
    assert not _positive_funding("Most MSc students are funded")
    assert not _positive_funding("No independently sourced material funding claim retained")


def test_every_stage2_candidate_has_exactly_one_controlled_status() -> None:
    candidates = read_csv(OUTPUT_DIR / "candidate_program_funnel.csv")
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    assert len(verification) == len(candidates)
    assert len({row["candidate_program_id"] for row in verification}) == len(candidates)
    assert {row["verification_status"] for row in verification} <= FINAL_STATUSES
    assert {
        "exact_degree_program_name", "degree_type", "research_requirement",
        "department", "current_program_status", "bachelors_entry_eligibility",
        "international_student_eligibility", "language_of_instruction",
        "english_requirement_and_waiver", "minimum_gpa",
        "minimum_gpa_application", "prerequisite_coursework", "admissions_model",
        "faculty_contact_expectation", "fall_2027_deadline",
        "deadline_cycle_label", "application_fee", "fee_currency",
        "fee_waiver_rules", "simultaneous_application_rules",
        "separate_fees_required", "tuition", "mandatory_fees", "funding_model",
        "funding_status", "funding_duration", "funding_conditions",
        "funding_international_eligibility", "named_scholarships",
        "scholarship_deadlines", "summer_coverage", "health_insurance_coverage",
        "largest_unresolved_question",
    } <= verification[0].keys()


def test_sources_exclusions_and_faculty_gate_resolve() -> None:
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    sources = read_csv(OUTPUT_DIR / "program_sources.csv")
    exclusions = read_csv(OUTPUT_DIR / "program_exclusions.csv")
    source_ids = {row["stage3_source_id"] for row in sources}
    assert not any(row["official_or_secondary"] == "Primary scholarly source" for row in sources)
    assert all(set(_split(row["program_source_ids"])) <= source_ids for row in verification)
    assert {row["candidate_program_id"] for row in exclusions} == {
        row["candidate_program_id"]
        for row in verification
        if row["verification_status"] == "excluded"
    }
    assert all(
        (row["faculty_review_ready"] == "yes")
        == (row["verification_status"] in {"retained", "conditional"})
        for row in verification
    )
    assert all(
        row["application_positioning"] == "Outreach Before Decision"
        for row in verification
        if row["verification_status"] == "conditional"
    )


def test_material_funding_claims_have_official_funding_sources() -> None:
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    sources = {
        row["stage3_source_id"]: row
        for row in read_csv(OUTPUT_DIR / "program_sources.csv")
    }
    for row in verification:
        if not _has_material_funding_claim(row):
            continue
        funding_ids = _split(row["funding_source_ids"])
        assert funding_ids
        assert all(
            "funding" in _split(sources[source_id]["claim_categories"])
            and sources[source_id]["official_or_secondary"].casefold().startswith("official")
            for source_id in funding_ids
        )


def test_same_university_duplicate_routes_do_not_proceed() -> None:
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    duplicate_rows = [
        row
        for row in verification
        if row["same_university_dominance_gate"] == "fail_duplicate_route"
    ]
    assert {row["institution_name"] for row in duplicate_rows} == {
        "The University of Texas at Austin",
        "Virginia Polytechnic Institute and State University",
    }
    assert all(row["verification_status"] == "excluded" for row in duplicate_rows)


def test_stage3_output_has_no_score_or_recommendation_fields() -> None:
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    columns = verification[0].keys()
    assert not any(
        token in column.casefold()
        for column in columns
        for token in ("score", "rank", "recommendation")
    )
