from __future__ import annotations

from collections import Counter
from pathlib import Path

from graduate_audit.io import read_csv, read_json
from graduate_audit.portfolio_pressure import (
    ACTIVE_STATUSES,
    PRESSURE_QUESTIONS,
    assign_portfolio_statuses,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def program(
    index: int,
    *,
    plausibility: str = "Plausible",
    score: int | None = None,
    institution_id: str | None = None,
    gates_pass: bool = True,
) -> dict[str, str]:
    return {
        "program_id": f"program:{index}",
        "institution_id": institution_id or f"institution:{index}",
        "institution_name": f"Institution {institution_id or index}",
        "program_name": "Computer Science PhD",
        "overall_score": str(score if score is not None else 95 - index),
        "professor_alignment_score": "20",
        "funding_net_viability_score": "20",
        "all_hard_gates_pass": str(gates_pass).lower(),
        "hard_gate_failures": "" if gates_pass else "funding",
        "admission_plausibility": plausibility,
    }


def test_quality_first_core_caps_at_sixteen_without_discarding_reserve():
    rows = [program(index) for index in range(20)]
    decisions, policy = assign_portfolio_statuses(rows, {})
    counts = Counter(item["portfolio_status"] for item in decisions.values())

    assert counts == {"core": 16, "reserve": 4}
    assert policy["return_to_candidate_discovery"] is False


def test_reach_and_lottery_share_never_exceeds_one_third_and_lottery_is_capped():
    rows = [program(index) for index in range(3)]
    rows += [program(10 + index, plausibility="Reach", score=80 - index) for index in range(2)]
    rows += [program(20 + index, plausibility="Lottery", score=70 - index) for index in range(2)]
    decisions, _ = assign_portfolio_statuses(rows, {})
    core_rows = [row for row in rows if decisions[row["program_id"]]["portfolio_status"] == "core"]
    stretch = [row for row in core_rows if row["admission_plausibility"] in {"Reach", "Lottery", "Plausible to reach"}]

    assert len(stretch) * 3 <= len(core_rows)
    assert sum(row["admission_plausibility"] == "Lottery" for row in core_rows) <= 1


def test_insufficient_admission_evidence_triggers_monitor_and_discovery_return():
    rows = [program(index, plausibility="Insufficient evidence") for index in range(7)]
    decisions, policy = assign_portfolio_statuses(rows, {})

    assert {item["portfolio_status"] for item in decisions.values()} == {"monitor"}
    assert policy["credible_core_candidates"] == 0
    assert policy["return_to_candidate_discovery"] is True


def test_failed_hard_gate_can_never_enter_an_active_list():
    rows = [program(1, gates_pass=False), program(2)]
    decisions, _ = assign_portfolio_statuses(rows, {})

    assert decisions["program:1"]["portfolio_status"] == "do_not_apply"
    assert decisions["program:2"]["portfolio_status"] in ACTIVE_STATUSES


def test_research_masters_is_preserved_without_prestige_filtering():
    row = program(1, plausibility="Plausible")
    row.update({
        "institution_name": "Regional Public University",
        "degree_type": "Thesis or research master's",
    })
    decisions, _ = assign_portfolio_statuses([row], {})

    assert decisions["program:1"]["portfolio_status"] == "core"


def test_second_program_requires_independent_strength_and_verified_simultaneous_rules():
    first = program(1, score=75, institution_id="shared")
    second = program(2, score=72, institution_id="shared")
    decisions, _ = assign_portfolio_statuses(
        [first, second],
        {"program:2": {"simultaneous_application_rules": "Not verified"}},
    )
    assert decisions["program:2"]["portfolio_status"] == "not_retained_alternate"

    decisions, _ = assign_portfolio_statuses(
        [first, second],
        {"program:2": {"simultaneous_application_rules": "Simultaneous applications are allowed"}},
    )
    assert decisions["program:2"]["portfolio_status"] == "core"
    assert decisions["program:2"]["second_program_rule_verified"] is True


def test_stage_six_artifact_covers_every_program_and_all_ten_questions():
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")
    evidence_ids = {
        row["score_evidence_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/score_evidence.csv")
    }
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
    ]
    hard_gate_survivors = [row for row in scores if row["all_hard_gates_pass"] == "true"]
    failed_gate_programs = [row for row in scores if row["all_hard_gates_pass"] != "true"]

    assert len(entries) == len(scores)
    assert {row["program_id"] for row in entries} == {row["program_id"] for row in scores}
    assert portfolio["decision"] == "RETURN_TO_CANDIDATE_DISCOVERY"
    assert len(portfolio["core"]) == 0
    assert len(portfolio["monitor"]) == len(hard_gate_survivors)
    assert len(portfolio["do_not_apply"]) == len(failed_gate_programs)
    for row in entries:
        assert len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) == 10
        for answer in row["pressure_test_answers"]:
            assert answer["answer"]
            assert set(answer["evidence_ids"]).issubset(evidence_ids)


def test_stage_six_reentry_02_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_02_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 8
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_03_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_03_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 8
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_04_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_04_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 9
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_05_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_05_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 3
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_06_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_06_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 6
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_07_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_07_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 7
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_08_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_08_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 4
    assert {row["program_id"] for row in entries} == latest_ids
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_09_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_09_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 6
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 60
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_10_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_10_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 5
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 50
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_11_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_11_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 9
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 90
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_12_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_12_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 6
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 60
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_13_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_13_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 5
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 50
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"monitor", "do_not_apply"}


def test_stage_six_reentry_14_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_14_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 5
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 50
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_15_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_15_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 7
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 70
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert sum(row["portfolio_status"] == "monitor" for row in entries) == 1
    assert sum(row["portfolio_status"] == "do_not_apply" for row in entries) == 6


def test_stage_six_reentry_16_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_16_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 8
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 80
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert {row["portfolio_status"] for row in entries} == {"do_not_apply"}


def test_stage_six_reentry_17_disposes_and_pressure_tests_every_new_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_17_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    portfolio = read_json(REPO_ROOT / "data/processed/pass2/portfolio.json")
    entries = [
        row
        for key in ("core", "reserve", "monitor", "do_not_apply", "not_retained_alternates")
        for row in portfolio[key]
        if row["program_id"] in latest_ids
    ]
    assert len(latest_ids) == len(entries) == 9
    assert {row["program_id"] for row in entries} == latest_ids
    assert sum(len(row["pressure_test_answers"]) for row in entries) == 90
    assert all(len(row["pressure_test_answers"]) == len(PRESSURE_QUESTIONS) for row in entries)
    assert sum(row["portfolio_status"] == "monitor" for row in entries) == 2
    assert sum(row["portfolio_status"] == "do_not_apply" for row in entries) == 7


def test_stage_six_report_uses_required_stage_template():
    report = (REPO_ROOT / "reports/pass2/06_portfolio_pressure_test.md").read_text(encoding="utf-8")
    assert report.startswith("# Stage 6 Result\n")
    for heading in (
        "## Decision",
        "## What changed",
        "## Coverage",
        "## Validation performed",
        "## Material uncertainties or conflicts",
        "## Records requiring human judgment",
        "## Files created or modified",
        "## Recommendation before the next stage",
    ):
        assert heading in report


def test_stage_six_manifest_passes_every_acceptance_assertion():
    manifest = read_json(REPO_ROOT / "data/manifests/pass2/stage_06.json")
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")

    assert manifest["decision"] == "PASS"
    assert manifest["counts"]["pressure_test_answers"] == len(scores) * len(PRESSURE_QUESTIONS)
    assert all(manifest["validation"]["assertions"].values())
