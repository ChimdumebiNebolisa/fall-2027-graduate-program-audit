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


def _payload(round_number: int):
    return json.loads(
        (
            REPO_ROOT
            / f"data/raw/pass2/stage_02_reentry_{round_number:02d}.json"
        ).read_text(encoding="utf-8")
    )


def _audit_targets(payload):
    return {
        row["institution_id"]: (
            row["exclusion_reason_category"],
            row["original_supporting_evidence"],
        )
        for row in payload.get("false_negative_audits", [])
    } or None


def test_reentry_definitions_build_exact_auditable_routes():
    for round_number in (1, 2, 3, 4, 5):
        payload = _payload(round_number)
        reentry_id = f"stage_02_reentry_{round_number:02d}"
        candidates, sources = build_reentry_rows(
            payload["candidates"],
            _institutions(),
            f"data/raw/pass2/stage_02_reentry_{round_number:02d}.json",
            reentry_id=reentry_id,
        )

        assert len(candidates) == 12
        assert len(sources) >= 24
        assert {row["region"] for row in candidates} == {"us", "canada", "europe"}
        assert all(row["official_program_url"].startswith("https://") for row in candidates)
        assert all(row["official_institution_url"].startswith("https://") for row in candidates)
        assert all(row["funnel_status"] == "advance_to_stage_3" for row in candidates)
        assert all(row["unresolved_fields"] for row in candidates)
        assert {row["reentry_id"] for row in candidates} == {reentry_id}


def test_reentry_merge_is_idempotent_and_reaudits_confirmed_omissions(tmp_path):
    from graduate_audit.candidate_funnel import build_candidate_funnel

    baseline = build_candidate_funnel(REPO_ROOT, tmp_path)
    merged = read_csv(tmp_path / "candidate_program_funnel.csv")
    yields = read_csv(tmp_path / "discovery_source_yield.csv")
    audits = read_csv(tmp_path / "exclusion_sample_audit.csv")
    for round_number in (1, 2, 3, 4, 5):
        payload = _payload(round_number)
        prefix = f"reentry{round_number:02d}"
        candidates, sources = build_reentry_rows(
            payload["candidates"],
            _institutions(),
            f"data/raw/pass2/stage_02_reentry_{round_number:02d}.json",
            reentry_id=f"stage_02_reentry_{round_number:02d}",
        )
        first = merge_candidate_rows(merged, candidates)
        second = merge_candidate_rows(first, candidates)
        yields = augment_source_yield(
            yields, candidates, sources, reentry_label=f"{round_number:02d}"
        )
        audits = augment_exclusion_audit(
            audits,
            candidates,
            reentry_prefix=prefix,
            audit_targets=_audit_targets(payload),
        )

        assert first == second
        assert sum(
            row["audit_result"] == "false_negative_corrected"
            and row["sample_id"].startswith(f"{prefix}:")
            for row in audits
        ) == 2
        assert validate_reentry(
            candidates, sources, first, audits, reentry_prefix=prefix
        )["status"] == "PASS"
        merged = first

    assert len(merged) == baseline["counts"]["candidate_rows"] + 60
    assert all(int(row["candidate_rows_contributed"]) >= 0 for row in yields)
    assert sum(row["audit_result"] == "false_negative_corrected" for row in audits) == 10
