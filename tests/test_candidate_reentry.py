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
    for round_number in range(1, 16):
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
    for round_number in range(1, 16):
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

    assert len(merged) == baseline["counts"]["candidate_rows"] + 180
    assert all(int(row["candidate_rows_contributed"]) >= 0 for row in yields)
    assert sum(row["audit_result"] == "false_negative_corrected" for row in audits) == 30


def test_reentry_11_has_the_intended_regional_and_route_mix():
    payload = _payload(11)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_11.json",
        reentry_id="stage_02_reentry_11",
    )

    assert len(candidates) == 12
    assert sum(row["region"] == "us" for row in candidates) == 6
    assert sum(row["region"] == "canada" for row in candidates) == 3
    assert sum(row["region"] == "europe" for row in candidates) == 3
    assert sum(row["degree_type"] == "PhD" for row in candidates) == 6
    assert sum(row["degree_type"] == "Thesis or research master's" for row in candidates) == 6
    assert len(sources) >= 24
    assert {row["accessed_date"] for row in sources} == {"2026-09-11"}
    assert len(payload["false_negative_audits"]) == 2


def test_reentry_12_has_the_intended_regional_and_route_mix():
    payload = _payload(12)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_12.json",
        reentry_id="stage_02_reentry_12",
    )

    assert len(candidates) == 12
    assert sum(row["region"] == "us" for row in candidates) == 6
    assert sum(row["region"] == "canada" for row in candidates) == 3
    assert sum(row["region"] == "europe" for row in candidates) == 3
    assert sum(row["degree_type"] == "PhD" for row in candidates) == 6
    assert sum(row["degree_type"] == "Thesis or research master's" for row in candidates) == 6
    assert len(sources) >= 24
    assert {row["accessed_date"] for row in sources} == {"2026-09-11"}
    assert len(payload["false_negative_audits"]) == 2


def test_reentry_13_has_the_intended_regional_and_route_mix():
    payload = _payload(13)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_13.json",
        reentry_id="stage_02_reentry_13",
    )

    assert len(candidates) == 12
    assert sum(row["region"] == "us" for row in candidates) == 6
    assert sum(row["region"] == "canada" for row in candidates) == 3
    assert sum(row["region"] == "europe" for row in candidates) == 3
    assert sum(row["degree_type"] == "PhD" for row in candidates) == 6
    assert sum(row["degree_type"] == "Thesis or research master's" for row in candidates) == 6
    assert len(sources) >= 24
    assert {row["accessed_date"] for row in sources} == {"2026-09-11"}
    assert len(payload["false_negative_audits"]) == 2


def test_reentry_14_has_the_intended_regional_and_route_mix():
    payload = _payload(14)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_14.json",
        reentry_id="stage_02_reentry_14",
    )

    assert len(candidates) == 12
    assert sum(row["region"] == "us" for row in candidates) == 6
    assert sum(row["region"] == "canada" for row in candidates) == 3
    assert sum(row["region"] == "europe" for row in candidates) == 3
    assert sum(row["degree_type"] == "PhD" for row in candidates) == 6
    assert sum(row["degree_type"] == "Thesis or research master's" for row in candidates) == 6
    assert len(sources) >= 24
    assert {row["accessed_date"] for row in sources} == {"2026-09-11"}
    assert len(payload["false_negative_audits"]) == 2


def test_reentry_15_has_the_intended_regional_and_route_mix():
    payload = _payload(15)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_15.json",
        reentry_id="stage_02_reentry_15",
    )

    assert len(candidates) == 12
    assert sum(row["region"] == "us" for row in candidates) == 6
    assert sum(row["region"] == "canada" for row in candidates) == 3
    assert sum(row["region"] == "europe" for row in candidates) == 3
    assert sum(row["degree_type"] == "PhD" for row in candidates) == 6
    assert sum(row["degree_type"] == "Thesis or research master's" for row in candidates) == 6
    assert len(sources) >= 24
    assert {row["accessed_date"] for row in sources} == {"2026-09-11"}
    assert len(payload["false_negative_audits"]) == 2


def test_reentry_validation_rejects_a_route_already_in_the_prior_funnel(tmp_path):
    from graduate_audit.candidate_funnel import build_candidate_funnel

    build_candidate_funnel(REPO_ROOT, tmp_path)
    baseline = read_csv(tmp_path / "candidate_program_funnel.csv")
    audits = read_csv(tmp_path / "exclusion_sample_audit.csv")
    payload = _payload(1)
    candidates, sources = build_reentry_rows(
        payload["candidates"],
        _institutions(),
        "data/raw/pass2/stage_02_reentry_01.json",
    )
    prior_ids = {row["program_id"] for row in baseline}
    merged = merge_candidate_rows(baseline, candidates)

    validation = validate_reentry(
        candidates,
        sources,
        merged,
        audits,
        prior_program_ids=prior_ids | {candidates[0]["program_id"]},
    )

    assert validation["status"] == "FAIL"
    assert validation["assertions"]["all_reentry_routes_are_net_new"] is False
