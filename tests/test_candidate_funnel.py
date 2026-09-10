import inspect
from pathlib import Path

import graduate_audit.research_fit.openalex_discovery as openalex_module
from graduate_audit.candidate_funnel import (
    build_candidate_funnel,
    exclusion_reason_category,
    name_variants,
    seed_adjacency,
)
from graduate_audit.io import read_csv, read_json
from graduate_audit.schema import CANDIDATE_FUNNEL_COLUMNS_V2


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_name_variants_cover_registered_campus_and_stopword_forms():
    assert "university virginia" in name_variants("University of Virginia-Main Campus")
    assert "kent state university" in name_variants("Kent State University at Kent")


def test_exclusion_categories_and_known_seed_detection():
    assert exclusion_reason_category("us", "No configured CIP signal") == (
        "no_recent_configured_cip_signal"
    )
    assert exclusion_reason_category("canada", "Official institutional scope is music") == (
        "specialized_noncomputing_scope"
    )
    assert seed_adjacency("automated program repair and claim verification") == (
        "TerraProbe-adjacent|Evidex-adjacent"
    )


def test_frozen_stage2_inputs_build_a_complete_high_recall_funnel(tmp_path):
    result = build_candidate_funnel(REPO_ROOT, tmp_path)

    assert result["validation"]["status"] == "PASS"
    assert all(result["validation"]["assertions"].values())
    assert result["counts"]["candidate_rows"] > result["source_counts"]["regional_program_rows"]
    assert result["counts"]["advance_to_stage_3"] > 0
    assert result["validation"]["saturation_status"] == "not_reached_documented"

    candidates = read_csv(tmp_path / "candidate_program_funnel.csv")
    source_yield = read_csv(tmp_path / "discovery_source_yield.csv")
    exclusions = read_csv(tmp_path / "exclusion_sample_audit.csv")
    assert {row["region"] for row in candidates} == {"us", "canada", "europe"}
    assert {row["discovery_path"] for row in source_yield} == {
        "recognized_institution_record",
        "official_program_or_department_signal",
        "recent_paper_signal",
        "current_faculty_topic_signal",
        "lab_or_center_signal",
        "calendar_prior_list",
        "first_audit_program",
        "research_masters_or_scholarship_search",
        "underrepresented_route_search",
    }
    assert all(row["sample_status"] == "complete" for row in exclusions)
    assert not any("score" in column for column in CANDIDATE_FUNNEL_COLUMNS_V2)


def test_openalex_export_has_no_global_top_n_truncation():
    manifest = read_json(REPO_ROOT / "data/manifests/openalex_discovery.json")
    institutions = read_csv(REPO_ROOT / "data/processed/openalex_institution_signals.csv")
    faculty = read_csv(REPO_ROOT / "data/processed/openalex_faculty_signals.csv")

    assert len(institutions) == manifest["counts"]["institutions_ranked"]
    assert len(faculty) == manifest["counts"]["author_institution_pairs"]
    source = inspect.getsource(openalex_module.discover)
    assert ".head(300)" not in source
    assert ".head(1000)" not in source
