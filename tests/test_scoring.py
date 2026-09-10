import pytest

from graduate_audit.scoring import calculate_score


def viable_row(**overrides):
    row = {
        "professor_fit_score": 27,
        "faculty_depth_score": 13,
        "funding_score": 23,
        "eligibility_score": 14,
        "degree_admissions_score": 9,
        "application_economics_score": 4,
        "recognized_active_institution": True,
        "relevant_research_program": True,
        "international_student_eligible": True,
        "bachelor_entry_or_research_masters_route": True,
        "verified_professor_match": True,
        "credible_funding_or_full_scholarship": True,
        "compatible_degree_structure": True,
        "funding_status": "verified",
        "verification_status": "verified",
    }
    row.update(overrides)
    return row


def test_strong_apply_and_research_subtotal():
    result = calculate_score(viable_row())
    assert result.overall_score == 90
    assert result.research_fit_score == 40
    assert result.recommendation == "Strong Apply"


def test_hard_gate_failure_overrides_score():
    result = calculate_score(viable_row(credible_funding_or_full_scholarship=False))
    assert result.recommendation == "Do Not Apply"
    assert "credible_funding_or_full_scholarship" in result.gate_failures


def test_out_of_range_score_fails():
    with pytest.raises(ValueError):
        calculate_score(viable_row(funding_score=26))

