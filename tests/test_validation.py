from graduate_audit.io import write_csv
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
)
from graduate_audit.validation import validate_outputs


def test_potential_supervisor_is_not_treated_as_verified(tmp_path):
    write_csv(
        tmp_path / "institution_universe.csv",
        [{"institution_id": "institution:one", "screening_status": "retained"}],
        INSTITUTION_COLUMNS,
    )
    write_csv(
        tmp_path / "program_screening.csv",
        [
            {
                "institution_id": "institution:one",
                "program_id": "program:one",
                "screening_decision": "retained",
                "official_program_url": "https://example.edu/program",
                "funding_status": "unknown",
                "direct_from_bachelors_eligible": "yes",
                "international_student_eligible": "yes",
                "degree_type": "PhD",
            }
        ],
        PROGRAM_COLUMNS,
    )
    write_csv(tmp_path / "exclusion_log.csv", [], EXCLUSION_COLUMNS)
    write_csv(
        tmp_path / "professor_evidence.csv",
        [
            {
                "program_id": "program:one",
                "can_supervise_program": "potentially",
                "verification_status": "verified",
                "official_faculty_url": "https://example.edu/faculty/one",
            }
        ],
        PROFESSOR_COLUMNS,
    )
    write_csv(tmp_path / "source_ledger.csv", [], SOURCE_COLUMNS)

    result = validate_outputs(tmp_path)

    assert result["status"] == "FAIL"
    assert any("no verified supervisor match" in error for error in result["errors"])
