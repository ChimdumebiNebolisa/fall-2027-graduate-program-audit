from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pytest

from graduate_audit.evidence_scoring import (
    COMPONENT_ORDER,
    calibrate_admission,
    coursework_exception_gate_from_evidence,
    funding_hard_gate_from_evidence,
    load_rubric,
)
from graduate_audit.io import read_csv, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]


def _funding_fixture():
    program = {
        "candidate_program_id": "fixture:program",
        "degree_type": "PhD",
        "research_requirement": "Dissertation",
        "funding_source_ids": "stage3src:funding",
        "verification_status": "retained",
        "screening_decision": "retained",
        "recommendation": "Strong Apply",
        "overall_score": "100",
        "funding_score": "25",
    }
    source = {
        "stage3_source_id": "stage3src:funding",
        "candidate_program_id": "fixture:program",
        "claim_categories": "funding|program",
        "exact_claim_supported": "Guaranteed five-year package with full tuition and stipend",
        "official_or_secondary": "Official",
        "verification_status": "Verified",
    }
    return program, {"stage3src:funding": source}


def test_rubric_has_six_anchored_components_summing_to_100():
    rubric = load_rubric(REPO_ROOT / "config/scoring_rubric.yaml")
    assert tuple(rubric["components"]) == COMPONENT_ORDER
    assert sum(component["weight"] for component in rubric["components"].values()) == 100
    for component in rubric["components"].values():
        anchor_scores = {anchor["score"] for anchor in component["anchors"]}
        assert min(anchor_scores) == 0
        assert max(anchor_scores) == component["weight"]


def test_funding_gate_ignores_labels_recommendations_and_scores():
    program, sources = _funding_fixture()
    assert funding_hard_gate_from_evidence(program, sources)
    for field, value in (
        ("verification_status", "excluded"),
        ("screening_decision", "excluded"),
        ("funding_gate", "resolvable_inquiry"),
        ("recommendation", "Do Not Apply"),
        ("overall_score", "0"),
        ("funding_score", "0"),
    ):
        changed = dict(program)
        changed[field] = value
        assert funding_hard_gate_from_evidence(changed, sources)


def test_funding_gate_requires_direct_official_verified_evidence():
    program, sources = _funding_fixture()
    for field, value in (
        ("official_or_secondary", "Secondary"),
        ("verification_status", "Incomplete"),
        ("verification_status", "Discovery evidence only"),
        ("verification_status", "Official program page checked; deep review pending"),
        ("claim_categories", "admissions"),
        ("candidate_program_id", "fixture:other-program"),
    ):
        changed_sources = {key: dict(row) for key, row in sources.items()}
        changed_sources["stage3src:funding"][field] = value
        assert not funding_hard_gate_from_evidence(program, changed_sources)


@pytest.mark.parametrize(
    "status",
    [
        "Verified",
        "official page checked",
        "opened/current",
        "opened; cycle limits recorded",
        "accessible or indexed official page",
        "Official indexed page content checked; automated direct retrieval returned HTTP 403",
    ],
)
def test_funding_gate_accepts_stage_three_verified_official_statuses(status):
    program, sources = _funding_fixture()
    sources["stage3src:funding"]["verification_status"] = status
    assert funding_hard_gate_from_evidence(program, sources)


def test_weak_funding_source_does_not_override_independent_verified_guarantee():
    program, sources = _funding_fixture()
    program["funding_source_ids"] += "|stage3src:weak"
    sources["stage3src:weak"] = {
        **sources["stage3src:funding"],
        "stage3_source_id": "stage3src:weak",
        "exact_claim_supported": "A competitive award may be offered to selected students.",
    }
    assert funding_hard_gate_from_evidence(program, sources)


def test_first_year_only_support_does_not_pass_funding_gate():
    program, sources = _funding_fixture()
    sources["stage3src:funding"]["exact_claim_supported"] = (
        "All incoming PhD students receive first-year support; later funding patterns are advisor-dependent."
    )
    assert not funding_hard_gate_from_evidence(program, sources)


def test_non_universal_guarantee_does_not_pass_funding_gate():
    program, sources = _funding_fixture()
    sources["stage3src:funding"]["exact_claim_supported"] = (
        "Many admitted students receive a four-year guarantee, but the page does not promise it to all admits."
    )
    assert not funding_hard_gate_from_evidence(program, sources)


def test_coursework_only_program_needs_research_and_exceptional_full_scholarship():
    program, sources = _funding_fixture()
    program["degree_type"] = "Coursework or professional master's"
    program["research_requirement"] = "Coursework only"
    assert not coursework_exception_gate_from_evidence(program, sources)
    program["research_requirement"] = "Substantial research thesis"
    sources["stage3src:funding"]["exact_claim_supported"] = "Verified full scholarship for the research route"
    assert coursework_exception_gate_from_evidence(program, sources)


def test_minimum_gpa_match_alone_does_not_create_plausible_assessment():
    program = {"minimum_gpa": "3.0", "largest_unresolved_question": ""}
    sources = [{"exact_claim_supported": "Published minimum GPA is 3.0"}]
    category, rationale = calibrate_admission(program, sources, eligibility_gate=True)
    assert category == "Insufficient evidence"
    assert "cohort/selectivity" in rationale


def test_stage_five_outputs_cover_all_programs_and_enforce_depth_deduplication():
    programs = [
        row
        for row in read_csv(REPO_ROOT / "data/processed/pass2/program_verification.csv")
        if row["faculty_review_ready"] == "yes"
    ]
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")
    evidence = read_csv(REPO_ROOT / "data/processed/pass2/score_evidence.csv")
    retained = read_csv(REPO_ROOT / "data/processed/pass2/professor_matches_retained.csv")
    expected_program_ids = {row["candidate_program_id"] for row in programs}
    assert {row["program_id"] for row in scores} == expected_program_ids
    assert len(scores) == len(programs)
    assert len(evidence) == len(programs) * len(COMPONENT_ORDER)
    evidence_by_program = defaultdict(list)
    retained_by_program = defaultdict(list)
    for row in evidence:
        evidence_by_program[row["program_id"]].append(row)
    for row in retained:
        retained_by_program[row["program_id"]].append(row)
    assert all({row["component"] for row in rows} == set(COMPONENT_ORDER) for rows in evidence_by_program.values())
    for row in scores:
        distinct = len({match["professor_id"] for match in retained_by_program[row["program_id"]]})
        assert int(row["distinct_verified_strong_matches"]) == distinct
        if distinct <= 1:
            assert int(row["faculty_depth_points"]) <= 5


def test_stage_five_reentry_02_scores_every_new_faculty_ready_route():
    latest_ids = {
        row["candidate_program_id"]
        for row in read_csv(REPO_ROOT / "data/processed/pass2/stage_03_reentry_02_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")
    evidence = read_csv(REPO_ROOT / "data/processed/pass2/score_evidence.csv")
    scored_latest = [row for row in scores if row["program_id"] in latest_ids]
    evidence_by_program = defaultdict(list)
    for row in evidence:
        if row["program_id"] in latest_ids:
            evidence_by_program[row["program_id"]].append(row)
    assert len(latest_ids) == len(scored_latest) == 8
    assert {row["program_id"] for row in scored_latest} == latest_ids
    assert set(evidence_by_program) == latest_ids
    assert all(len(rows) == len(COMPONENT_ORDER) for rows in evidence_by_program.values())
    assert all(row["professor_hard_gate"] == "true" for row in scored_latest)


def test_missing_gate_evidence_reduces_confidence_and_blocks_rank():
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")
    incomplete = [
        row for row in scores
        if row["funding_hard_gate"] == "false" or row["professor_hard_gate"] == "false"
    ]
    assert incomplete
    assert all(row["score_confidence"] == "low" for row in incomplete)
    assert all(not row["evidence_rank"] for row in incomplete)


def test_no_probability_and_no_institution_specific_score_constants():
    scores = read_csv(REPO_ROOT / "data/processed/pass2/program_scores.csv")
    manifest = read_json(REPO_ROOT / "data/manifests/pass2/stage_05.json")
    assert all(not row["admission_probability"] for row in scores)
    assert all(row["admission_plausibility"] in {"Insufficient evidence", "Eligibility concern"} for row in scores)
    assert manifest["validation"]["institution_specific_score_constant_hits"] == []
    assert manifest["validation"]["assertions"]["no_institution_specific_score_constants"] is True
