from graduate_audit.hard_gates import evaluate_hard_gates


def viable_program(**overrides):
    row = {
        "program_id": "program:alpha",
        "recognized_active_institution": "true",
        "relevant_research_program": "true",
        "international_student_eligible": "true",
        "bachelor_entry_or_research_masters_route": "true",
        "compatible_degree_structure": "true",
        "funding_gate_status": "verified",
        "funding_gate_evidence": "src:funding",
    }
    row.update(overrides)
    return row


def verified_professor(**overrides):
    row = {
        "professor_id": "professor:one",
        "program_id": "program:alpha",
        "full_name": "Professor One",
        "can_supervise_program": "verified",
        "verification_status": "verified",
        "official_faculty_url": "https://example.edu/faculty/one",
        "evidence_ids": "src:professor-one",
    }
    row.update(overrides)
    return row


def test_funding_gate_requires_explicit_verified_evidence():
    result = evaluate_hard_gates(
        viable_program(
            funding_gate_status="unknown",
            funding_gate_evidence="",
            screening_decision="retained",
            funding_score="25",
            verification_status="verified",
        ),
        [verified_professor()],
    )

    assert result.gates["credible_funding_or_full_scholarship"] is False
    assert "credible_funding_or_full_scholarship" in result.failures


def test_potential_supervisor_does_not_satisfy_verified_gate():
    result = evaluate_hard_gates(
        viable_program(),
        [verified_professor(can_supervise_program="potentially", verification_status="incomplete")],
    )

    assert result.distinct_verified_professor_count == 0
    assert result.gates["verified_professor_match"] is False


def test_verified_professor_count_is_distinct():
    duplicate = verified_professor()
    second = verified_professor(
        professor_id="professor:two",
        full_name="Professor Two",
        official_faculty_url="https://example.edu/faculty/two",
        evidence_ids="src:professor-two",
    )

    result = evaluate_hard_gates(viable_program(), [duplicate, dict(duplicate), second])

    assert result.distinct_verified_professor_count == 2
    assert not result.failures
