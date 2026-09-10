import pytest

from graduate_audit.io import write_csv
from graduate_audit.portfolio import score_programs, select_portfolio
from graduate_audit.schema import INSTITUTION_COLUMNS, PROFESSOR_COLUMNS, PROGRAM_COLUMNS


def program(index: int, *, recommendation: str = "Likely Apply", plausibility: str = "Plausible"):
    return {
        "institution_id": f"inst:{index}",
        "institution_name": f"Institution {index}",
        "program_id": f"program:{index}",
        "program_name": "Computer Science",
        "degree_type": "PhD",
        "overall_score": str(90 - index),
        "research_fit_score": "40",
        "funding_score": "22",
        "admission_plausibility": plausibility,
        "recommendation": recommendation,
    }


def test_core_is_not_padded_with_outreach_or_monitor_rows():
    rows = [program(1), program(2, recommendation="Outreach Before Decision"), program(3, recommendation="Monitor for 2027 Position")]
    result = select_portfolio(rows)
    assert len(result["core"]) == 1
    assert len(result["reserve"]) == 1
    assert len(result["monitor_for_2027_position"]) == 1


def test_reaches_do_not_create_a_core_without_non_stretch_programs():
    rows = [program(i, plausibility="Reach") for i in range(10)]
    result = select_portfolio(rows)
    assert len(result["core"]) == 0
    assert len(result["reserve"]) == 10


def test_core_uses_one_program_per_institution():
    first = program(1)
    second = dict(first, program_id="program:alternate", program_name="Software Engineering", overall_score="80")
    result = select_portfolio([first, second])
    assert len(result["core"]) == 1
    assert len(result["reserve"]) == 0
    assert len(result["not_retained_alternates"]) == 1


def test_legacy_rows_cannot_be_silently_rescored(tmp_path):
    institution_path = tmp_path / "institutions.csv"
    program_path = tmp_path / "programs.csv"
    professor_path = tmp_path / "professors.csv"
    write_csv(
        institution_path,
        [{"institution_id": "institution:one"}],
        INSTITUTION_COLUMNS,
    )
    write_csv(
        program_path,
        [{"institution_id": "institution:one", "program_id": "program:one"}],
        PROGRAM_COLUMNS,
    )
    write_csv(professor_path, [], PROFESSOR_COLUMNS)

    with pytest.raises(ValueError, match="migrate legacy rows"):
        score_programs(program_path, institution_path, professor_path)
