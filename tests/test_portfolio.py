from graduate_audit.portfolio import select_portfolio


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


def test_core_caps_reaches_at_five():
    rows = [program(i, plausibility="Reach") for i in range(10)]
    result = select_portfolio(rows)
    assert len(result["core"]) == 5
    assert len(result["reserve"]) == 5


def test_core_uses_one_program_per_institution():
    first = program(1)
    second = dict(first, program_id="program:alternate", program_name="Software Engineering", overall_score="80")
    result = select_portfolio([first, second])
    assert len(result["core"]) == 1
    assert len(result["reserve"]) == 1
