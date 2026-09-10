from graduate_audit.schema import (
    PROGRAM_COLUMNS,
    PROGRAM_COLUMNS_V2,
    SCORE_COMPONENT_COLUMNS_V2,
    canonical_url,
    program_id,
    source_id,
)


def test_source_id_ignores_tracking_parameters():
    clean = "https://example.edu/program"
    tracked = "https://example.edu/program/?utm_source=test"
    assert source_id(clean) == source_id(tracked)


def test_program_id_is_deterministic():
    assert program_id("us:ipeds:1", "PhD", "Computer Science") == program_id(
        "us:ipeds:1", "PhD", "Computer Science"
    )


def test_canonical_url_sorts_query_parameters():
    assert canonical_url("HTTPS://EXAMPLE.EDU/x/?b=2&a=1") == "https://example.edu/x?a=1&b=2"


def test_pass2_schema_is_additive_and_evidence_aware():
    assert PROGRAM_COLUMNS_V2[: len(PROGRAM_COLUMNS)] == PROGRAM_COLUMNS
    assert {
        "score_component_evidence",
        "evidence_completeness",
        "score_confidence",
        "distinct_verified_professor_count",
        "admission_plausibility_rationale",
        "funding_gate_evidence",
        "regional_admissions_model",
        "unresolved_conflicts",
    }.issubset(PROGRAM_COLUMNS_V2)
    assert {
        "rubric_anchor",
        "evidence_ids",
        "evidence_completeness",
        "score_confidence",
        "unresolved_conflicts",
    }.issubset(SCORE_COMPONENT_COLUMNS_V2)
