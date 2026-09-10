from __future__ import annotations

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

LEGACY_SCHEMA_VERSION = "1.0"
PASS2_SCHEMA_VERSION = "2.0"

INSTITUTION_STATUSES = {
    "indexed",
    "out_of_scope",
    "inactive",
    "not_recognized",
    "no_graduate_degree_authority",
    "no_relevant_graduate_field",
    "program_screened_out",
    "preliminary_fit",
    "deep_review",
    "retained",
    "excluded",
}

PROGRAM_TYPES = {
    "PhD",
    "Direct-entry PhD",
    "Integrated or structured doctorate",
    "PhD requiring a master's",
    "Thesis or research master's",
    "Project-based master's with substantial research",
    "Coursework or professional master's",
    "Unclear",
}

RECOMMENDATIONS = {
    "Strong Apply",
    "Likely Apply",
    "Outreach Before Decision",
    "Monitor for 2027 Position",
    "Investigate Further",
    "Deprioritize",
    "Do Not Apply",
}

ADMISSION_PLAUSIBILITY = {
    "Clearly ineligible",
    "Eligibility concern",
    "Plausible",
    "Plausible to reach",
    "Reach",
    "Insufficient evidence",
}

RECRUITING_STATUSES = {
    "Confirmed recruiting",
    "Evidence suggests possible recruiting",
    "Recruiting status unknown",
    "Explicitly not recruiting",
}

INSTITUTION_COLUMNS = (
    "institution_id", "institution_name", "alternate_names", "country", "region",
    "institution_type", "recognition_status", "active_status", "official_website",
    "source_database", "dataset_release", "access_date", "graduate_degree_authority",
    "relevant_graduate_field_signal", "screening_status", "exclusion_reason", "ror_id",
    "ipeds_unitid", "eter_id", "dli_number", "manual_verification", "notes",
)

PROGRAM_COLUMNS = (
    "program_id", "institution_id", "institution_name", "country", "program_name",
    "degree_type", "department", "official_program_url", "thesis_dissertation_requirement",
    "research_credit_requirement", "research_groups_labs", "direct_from_bachelors_eligible",
    "international_student_eligible", "language_of_instruction", "current_program_status",
    "preliminary_fit", "screening_decision", "exclusion_reason", "minimum_gpa",
    "minimum_gpa_policy", "prerequisite_coursework", "gre_policy", "english_requirement_waiver",
    "fall_2027_deadline", "deadline_cycle_status", "application_fee", "fee_currency",
    "fee_waiver_rules", "multiple_applications_allowed", "separate_fees_required",
    "admissions_model", "faculty_contact_expectation", "funding_model", "funding_status",
    "stipend_amount", "stipend_currency", "funding_duration_years", "tuition_coverage",
    "mandatory_fee_coverage", "health_insurance_coverage", "summer_funding",
    "funding_conditions", "supervisor_dependent_funding", "phd_funding", "masters_funding",
    "scholarships_fellowships", "professor_fit_score", "faculty_depth_score",
    "research_fit_score", "funding_score", "eligibility_score", "degree_admissions_score",
    "application_economics_score", "overall_score", "admission_plausibility",
    "recommendation", "final_decision", "biggest_risk", "unresolved_question", "single_professor_dependency",
    "verification_status", "notes",
)

PROFESSOR_COLUMNS = (
    "professor_id", "institution_id", "institution_name", "program_id", "program_name",
    "full_name", "department", "faculty_position", "appointment_status",
    "can_supervise_program", "official_faculty_url", "official_email", "research_themes",
    "fit_explanation", "fit_strength", "recent_work_1", "recent_work_1_url",
    "recent_work_1_year", "recent_work_2", "recent_work_2_url", "recent_work_2_year",
    "recent_work_3", "recent_work_3_url", "recent_work_3_year", "sustained_research_evidence",
    "recruiting_evidence", "recruiting_status", "prospective_student_instructions",
    "contacting_faculty_appropriate", "already_contacted", "last_contact_date",
    "previous_outcome", "outreach_priority", "outreach_score", "recommended_outreach_angle",
    "specific_question_goal", "openalex_author_id", "orcid", "verification_status", "notes",
)

EXCLUSION_COLUMNS = (
    "institution_id", "institution_name", "country", "program_id", "program_name",
    "stage_of_exclusion", "primary_exclusion_reason", "supporting_evidence", "source_url",
    "confidence", "manual_verification", "date_checked",
)

SOURCE_COLUMNS = (
    "source_id", "institution_id", "institution_name", "program_id", "program_or_professor",
    "claim_type", "exact_claim_supported", "source_title", "publisher", "publication_date",
    "url", "source_type", "official_or_secondary", "date_accessed", "admissions_cycle",
    "confidence", "verification_status", "access_note",
)

# Pass 2 uses additive schemas so the evidence columns can migrate without
# rewriting or silently reinterpreting the committed Pass 1 outputs.
INSTITUTION_COLUMNS_V2 = INSTITUTION_COLUMNS + (
    "schema_version", "regional_admissions_model", "unresolved_conflicts",
)

PROGRAM_COLUMNS_V2 = PROGRAM_COLUMNS + (
    "schema_version", "discovery_paths", "exact_research_fit_signal",
    "recognized_active_institution", "relevant_research_program",
    "bachelor_entry_or_research_masters_route", "compatible_degree_structure",
    "regional_admissions_model", "score_component_evidence",
    "evidence_completeness", "score_confidence",
    "distinct_verified_professor_count", "admission_plausibility_rationale",
    "funding_gate_status", "funding_gate_evidence", "unresolved_conflicts",
    "hard_gate_failures",
)

PROFESSOR_COLUMNS_V2 = PROFESSOR_COLUMNS + (
    "schema_version", "evidence_ids", "unresolved_conflicts",
)

SOURCE_COLUMNS_V2 = SOURCE_COLUMNS + ("schema_version",)

SCORE_COMPONENT_COLUMNS_V2 = (
    "schema_version", "program_id", "component", "score", "max_score",
    "rubric_anchor", "evidence_ids", "evidence_completeness",
    "score_confidence", "unresolved_conflicts",
)

OUTREACH_PRIORITY_COLUMNS_V2 = (
    "schema_version", "program_id", "institution_name", "contact_type",
    "contact_name", "official_contact", "information_gap",
    "outreach_status", "evidence_ids",
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url.strip())
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query) if not k.startswith("utm_")))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), query, ""))


def source_id(url: str) -> str:
    digest = hashlib.sha256(canonical_url(url).encode("utf-8")).hexdigest()[:16]
    return f"src:{digest}"


def program_id(institution_id: str, degree_type: str, program_name: str) -> str:
    return f"{institution_id}:program:{slugify(degree_type)}:{slugify(program_name)}"


def professor_id(institution_id: str, full_name: str) -> str:
    return f"{institution_id}:faculty:{slugify(full_name)}"
