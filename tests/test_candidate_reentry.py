import json
from pathlib import Path

from graduate_audit.candidate_reentry import (
    augment_exclusion_audit,
    augment_source_yield,
    build_reentry_rows,
    merge_candidate_rows,
    validate_reentry,
)
from graduate_audit.io import read_csv


REPO_ROOT = Path(__file__).resolve().parents[1]


def _institutions():
    rows = {}
    for region in ("us", "canada", "europe"):
        for row in read_csv(REPO_ROOT / f"data/processed/regions/{region}/institution_universe.csv"):
            rows[row["institution_id"]] = row
    return rows


def test_reentry_definitions_build_exact_auditable_routes():
    payload = json.loads(
        (REPO_ROOT / "data/raw/pass2/stage_02_reentry_01.json").read_text(encoding="utf-8")
    )
    candidates, sources = build_reentry_rows(
        payload["candidates"], _institutions(), "data/raw/pass2/stage_02_reentry_01.json"
    )

    assert len(candidates) == 12
    assert len(sources) >= 24
    assert {row["region"] for row in candidates} == {"us", "canada", "europe"}
    assert all(row["official_program_url"].startswith("https://") for row in candidates)
    assert all(row["official_institution_url"].startswith("https://") for row in candidates)
    assert all(row["funnel_status"] == "advance_to_stage_3" for row in candidates)
    assert all(row["unresolved_fields"] for row in candidates)


def test_reentry_merge_is_idempotent_and_reaudits_confirmed_omissions(tmp_path):
    from graduate_audit.candidate_funnel import build_candidate_funnel

    baseline = build_candidate_funnel(REPO_ROOT, tmp_path)
    payload = json.loads(
        (REPO_ROOT / "data/raw/pass2/stage_02_reentry_01.json").read_text(encoding="utf-8")
    )
    candidates, sources = build_reentry_rows(
        payload["candidates"], _institutions(), "data/raw/pass2/stage_02_reentry_01.json"
    )
    original = read_csv(tmp_path / "candidate_program_funnel.csv")
    first = merge_candidate_rows(original, candidates)
    second = merge_candidate_rows(first, candidates)
    yields = augment_source_yield(
        read_csv(tmp_path / "discovery_source_yield.csv"), candidates, sources
    )
    audits = augment_exclusion_audit(
        read_csv(tmp_path / "exclusion_sample_audit.csv"), candidates
    )

    assert first == second
    assert len(first) == baseline["counts"]["candidate_rows"] + 12
    assert all(int(row["candidate_rows_contributed"]) >= 0 for row in yields)
    assert sum(row["audit_result"] == "false_negative_corrected" for row in audits) == 2
    assert validate_reentry(candidates, sources, first, audits)["status"] == "PASS"
