from __future__ import annotations

import csv
import json
from pathlib import Path

from graduate_audit.outreach_prioritization import OUTREACH_COLUMNS, SCORE_FIELDS
from graduate_audit.schema import OUTREACH_PRIORITY_COLUMNS_V2


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "data/processed/pass2/outreach_priority.csv"
PRIVATE_HISTORY = REPO_ROOT / "data/processed/pass2/contact_history_status.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_every_active_program_has_a_professor_contact_disposition():
    portfolio = json.loads((REPO_ROOT / "data/processed/pass2/portfolio.json").read_text(encoding="utf-8"))
    active_ids = {row["program_id"] for key in ("core", "reserve") for row in portfolio[key]}
    rows = read_csv(OUTPUT)
    professor_ids = {row["program_id"] for row in rows if row["contact_type"] == "professor"}
    assert professor_ids == active_ids


def test_first_wave_is_bounded_and_every_reply_has_a_specific_decision():
    rows = read_csv(OUTPUT)
    first_wave = [row for row in rows if row["wave"] == "first_wave"]
    assert 10 <= len(first_wave) <= 15
    assert all(row["decision_that_reply_could_change"].strip() for row in first_wave)
    assert all(row["official_contact"] and row["contact_history_status"] == "no" for row in first_wave)


def test_unknown_history_is_preserved_and_never_converted_to_no_contact():
    rows = read_csv(OUTPUT)
    history = read_csv(PRIVATE_HISTORY)
    unknown_keys = {(row["program_id"], row["contact_type"], row["contact_name"]) for row in history if row["contact_history_status"] == "unknown"}
    output_unknown = {(row["program_id"], row["contact_type"], row["contact_name"]) for row in rows if row["contact_history_status"] == "unknown"}
    assert unknown_keys
    assert unknown_keys == output_unknown
    assert all(row["wave"] == "blocked_missing_official_contact" for row in rows if row["contact_history_status"] == "unknown")


def test_no_fresh_introduction_is_recommended_after_prior_contact():
    rows = read_csv(OUTPUT)
    assert all(row["wave"] not in {"first_wave", "second_wave"} for row in rows if row["contact_history_status"] == "yes")


def test_each_score_is_component_based_and_bounded():
    rows = read_csv(OUTPUT)
    assert tuple(rows[0]) == OUTREACH_COLUMNS
    assert OUTREACH_COLUMNS == OUTREACH_PRIORITY_COLUMNS_V2
    for row in rows:
        assert int(row["outreach_score"]) == sum(int(row[field]) for field in SCORE_FIELDS)
        assert 0 <= int(row["outreach_score"]) <= 100


def test_prioritized_output_has_no_duplicate_official_address():
    emails = [row["official_contact"].lower() for row in read_csv(OUTPUT) if row["official_contact"]]
    assert len(emails) == len(set(emails))


def test_private_history_contains_no_raw_message_material():
    rows = read_csv(PRIVATE_HISTORY)
    forbidden = {"body", "subject", "snippet", "message_id", "thread_id", "raw_message"}
    assert forbidden.isdisjoint(rows[0])
    assert all(forbidden.isdisjoint(row) for row in rows)


def test_stage_seven_manifest_acceptance_gate_passes():
    manifest = json.loads((REPO_ROOT / "data/manifests/pass2/stage_07.json").read_text(encoding="utf-8"))
    assert manifest["decision"] == "PASS"
    assert manifest["status"] == "complete"
    assert all(manifest["validation"]["assertions"].values())


def test_contact_history_artifact_is_git_ignored():
    import subprocess

    result = subprocess.run(
        ["git", "check-ignore", "-q", str(PRIVATE_HISTORY.relative_to(REPO_ROOT))],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0


def test_stage_seven_report_uses_required_stage_template():
    report = (REPO_ROOT / "reports/pass2/07_outreach_prioritization.md").read_text(encoding="utf-8")
    assert report.startswith("# Stage 7 Result\n")
    for heading in ("## Decision", "## What changed", "## Coverage", "## Validation performed", "## Material uncertainties or conflicts", "## Records requiring human judgment", "## Recommendation"):
        assert heading in report
