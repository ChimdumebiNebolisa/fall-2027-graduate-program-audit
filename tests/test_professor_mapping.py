from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from graduate_audit.io import read_csv
from graduate_audit.professor_mapping import FACULTY_ROSTERS
from graduate_audit.schema import RECRUITING_STATUSES


REPO_ROOT = Path(__file__).resolve().parents[1]


def _rows(name):
    return read_csv(REPO_ROOT / "data/processed/pass2" / name)


def test_roster_configuration_covers_every_serious_institution():
    programs = [
        row
        for row in _rows("program_verification.csv")
        if row["faculty_review_ready"] == "yes"
    ]
    assert set(FACULTY_ROSTERS) == {row["institution_name"] for row in programs}
    assert all(len(roster.alternatives) == 4 for roster in FACULTY_ROSTERS.values())
    assert all(roster.roster_url.startswith("https://") for roster in FACULTY_ROSTERS.values())


def test_reentry_02_evidence_exactly_covers_new_faculty_ready_routes():
    raw = json.loads(
        (REPO_ROOT / "data/raw/pass2/stage_04_reentry_02.json").read_text(encoding="utf-8")
    )
    newly_ready = {
        row["candidate_program_id"]
        for row in _rows("stage_03_reentry_02_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    professors = raw["professors"]
    assert {row["program_id"] for row in professors} == newly_ready
    assert len(professors) == len(newly_ready) == 8
    assert all(row["can_supervise_program"].casefold() == "yes" for row in professors)
    assert all(row["fit_strength"].casefold() == "strong" for row in professors)
    assert all(row["recent_work_1_url"].startswith("https://") for row in professors)
    assert all(row["recent_work_1_year"].isdigit() for row in professors)
    assert all(row["official_email"] for row in professors)
    assert all(row["recruiting_status"] in RECRUITING_STATUSES for row in professors)


def test_reentry_03_evidence_exactly_covers_new_faculty_ready_routes():
    raw = json.loads(
        (REPO_ROOT / "data/raw/pass2/stage_04_reentry_03.json").read_text(encoding="utf-8")
    )
    newly_ready = {
        row["candidate_program_id"]
        for row in _rows("stage_03_reentry_03_verification.csv")
        if row["faculty_review_ready"] == "yes"
    }
    professors = raw["professors"]
    assert {row["program_id"] for row in professors} == newly_ready
    assert len(professors) == len(newly_ready) == 8
    assert all(row["can_supervise_program"].casefold() == "yes" for row in professors)
    assert all(row["fit_strength"].casefold() == "strong" for row in professors)
    assert all(row["recent_work_1_url"].startswith("https://") for row in professors)
    assert all(row["recent_work_1_year"].isdigit() for row in professors)
    assert all(row["official_email"] or row["official_faculty_url"] for row in professors)
    assert all(row["recruiting_status"] in RECRUITING_STATUSES for row in professors)


def test_every_serious_program_has_five_evaluations_and_at_most_three_retained_matches():
    programs = [
        row
        for row in _rows("program_verification.csv")
        if row["faculty_review_ready"] == "yes"
    ]
    evaluated = _rows("professor_candidates_evaluated.csv")
    retained = _rows("professor_matches_retained.csv")
    evaluated_by_program = defaultdict(list)
    retained_by_program = defaultdict(list)
    for row in evaluated:
        evaluated_by_program[row["program_id"]].append(row)
    for row in retained:
        retained_by_program[row["program_id"]].append(row)
    serious_ids = {row["candidate_program_id"] for row in programs}
    assert set(evaluated_by_program) == serious_ids
    assert set(retained_by_program).issubset(serious_ids)
    assert all(len(rows) == 5 for rows in evaluated_by_program.values())
    assert all(len(retained_by_program[program_id]) <= 3 for program_id in serious_ids)
    assert all(row["good_faith_search_result"] for row in evaluated)


def test_retained_matches_meet_stage_four_evidence_gate():
    retained = _rows("professor_matches_retained.csv")
    assert retained
    for row in retained:
        assert "current" in row["appointment_status"].casefold()
        assert row["supervision_authority_status"].casefold() == "yes"
        assert row["fit_strength"].casefold() == "strong"
        assert row["verification_status"] == "verified_strong_match"
        assert int(row["recent_work_evidence_count"]) >= 1
        assert row["recent_work_1_url"].startswith("http")
        assert row["recent_work_1_year"].isdigit()
        assert row["recruiting_status"] in RECRUITING_STATUSES
        assert row["good_faith_search_result"]


def test_single_match_depth_cap_and_university_deduplication():
    evaluated = _rows("professor_candidates_evaluated.csv")
    retained = _rows("professor_matches_retained.csv")
    assert all(row["distinct_verified_strong_matches"] == "1" for row in retained)
    assert all(row["faculty_depth_points"] == "5" for row in retained)
    assert all(row["single_professor_dependency"] == "true" for row in retained)
    zero_match_rows = [row for row in evaluated if row["distinct_verified_strong_matches"] == "0"]
    assert zero_match_rows
    assert all(row["faculty_depth_points"] == "0" for row in zero_match_rows)
    assert all(row["single_professor_dependency"] == "false" for row in zero_match_rows)
    assert len({row["professor_id"] for row in retained}) <= len(retained)


def test_no_professor_score_and_every_evidence_reference_resolves():
    evaluated = _rows("professor_candidates_evaluated.csv")
    retained = _rows("professor_matches_retained.csv")
    sources = _rows("professor_sources.csv")
    assert not any("score" in column.casefold() for column in evaluated[0])
    assert not any("score" in column.casefold() for column in retained[0])
    source_ids = {row["stage4_source_id"] for row in sources}
    assert all(set(row["source_ids"].split("|")).issubset(source_ids) for row in evaluated)
    roster_programs = {
        row["program_id"]
        for row in sources
        if "current faculty roster" in row["claim_categories"]
        and row["official_or_secondary"] == "official"
        and row["verification_status"] == "verified"
    }
    assert roster_programs == {row["program_id"] for row in evaluated}


def test_unretained_candidates_preserve_uncertainty():
    evaluated = _rows("professor_candidates_evaluated.csv")
    unretained = [row for row in evaluated if row["candidate_disposition"] != "retained_strong"]
    assert unretained
    assert all(row["fit_strength"] == "Plausible — unscored" for row in unretained)
    assert all(row["supervision_authority_status"].casefold() != "yes" for row in unretained)
    assert all(row["recruiting_status"] in RECRUITING_STATUSES for row in unretained)
    assert all(
        row["recruiting_status"] == "Recruiting status unknown"
        for row in unretained
        if row["supervision_authority_status"] == "Unresolved for this specific program"
    )
    assert all("No professor score was assigned" in row["non_retention_reason"] for row in unretained)
