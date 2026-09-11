from __future__ import annotations

import csv
import json
from pathlib import Path

from graduate_audit.outreach_drafting import DRAFT_COLUMNS, FORBIDDEN_MARKERS, REQUIRED_SIGNOFF
from graduate_audit.schema import OUTREACH_DRAFT_COLUMNS_V2


REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = REPO_ROOT / "data/processed/pass2/outreach_drafts.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_drafts_cover_exactly_the_approved_first_wave():
    priorities = read_csv(REPO_ROOT / "data/processed/pass2/outreach_priority.csv")
    expected = {(row["program_id"], row["official_contact"]) for row in priorities if row["wave"] == "first_wave"}
    drafts = read_csv(DRAFT_PATH)
    actual = {(row["program_id"], row["recipient_email"]) for row in drafts}
    assert actual == expected
    assert len(drafts) == 12


def test_all_drafts_are_ready_but_unsent():
    drafts = read_csv(DRAFT_PATH)
    assert all(row["draft_ready"] == "yes" for row in drafts)
    assert all(row["send_status"] == "not_sent" for row in drafts)


def test_every_draft_has_exactly_one_clear_question_and_exact_signoff():
    for row in read_csv(DRAFT_PATH):
        assert row["draft_body"].count("?") == 1
        assert row["question"].count("?") == 1
        assert row["draft_body"].endswith(REQUIRED_SIGNOFF)


def test_every_personalization_anchor_resolves_to_verified_recent_work():
    professors = {
        (row["program_id"], row["full_name"]): row
        for row in read_csv(REPO_ROOT / "data/processed/pass2/professor_matches_retained.csv")
    }
    for draft in read_csv(DRAFT_PATH):
        professor = professors[(draft["program_id"], draft["recipient_name"])]
        assert draft["personalization_anchor"] == professor["recent_work_1_title"]
        assert draft["personalization_source_url"] == professor["recent_work_1_url"]
        assert professor["verification_status"].lower().startswith("verified")


def test_no_draft_contains_placeholders_or_internal_instructions():
    for row in read_csv(DRAFT_PATH):
        lower = row["draft_body"].lower()
        assert not any(marker in lower for marker in FORBIDDEN_MARKERS)


def test_all_draft_ready_checks_are_explicitly_yes():
    checks = (
        "contact_history_checked", "recipient_verified", "contact_appropriate",
        "factual_reference_verified", "one_clear_question",
        "no_internal_notes_or_placeholders", "natural_grammar",
        "required_signoff", "manual_read_through",
    )
    for row in read_csv(DRAFT_PATH):
        assert all(row[field] == "yes" for field in checks)


def test_draft_schema_matches_the_pass_two_contract():
    drafts = read_csv(DRAFT_PATH)
    assert tuple(drafts[0]) == DRAFT_COLUMNS == OUTREACH_DRAFT_COLUMNS_V2


def test_no_administrative_question_is_sent_to_a_professor():
    administrative_terms = ("application fee", "gpa exception", "transcript conversion", "deadline update")
    for row in read_csv(DRAFT_PATH):
        assert row["contact_type"] == "professor"
        assert not any(term in row["question"].lower() for term in administrative_terms)


def test_stage_eight_manifest_acceptance_gate_passes():
    manifest = json.loads((REPO_ROOT / "data/manifests/pass2/stage_08.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "complete"
    assert manifest["decision"] == "PASS"
    assert all(manifest["validation"]["assertions"].values())


def test_stage_eight_report_uses_required_stage_template():
    report = (REPO_ROOT / "reports/pass2/08_outreach_drafts_review.md").read_text(encoding="utf-8")
    assert report.startswith("# Stage 8 Result\n")
    for heading in ("## Decision", "## What changed", "## Coverage", "## Validation performed", "## Material uncertainties or conflicts", "## Records requiring human judgment", "## Recommendation"):
        assert heading in report
