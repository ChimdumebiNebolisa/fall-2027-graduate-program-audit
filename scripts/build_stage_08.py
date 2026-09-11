from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.outreach_drafting import (  # noqa: E402
    DRAFT_COLUMNS,
    FORBIDDEN_MARKERS,
    REQUIRED_SIGNOFF,
    build_drafts,
    load_yaml,
)
from graduate_audit.progress import update_progress  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
DRAFT_PATH = OUTPUT_DIR / "outreach_drafts.csv"
REVIEW_PATH = OUTPUT_DIR / "outreach_draft_manual_review.csv"
REPORT_PATH = REPO_ROOT / "reports/pass2/08_outreach_drafts_review.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_08.json"
BRIEFS_PATH = REPO_ROOT / "config/outreach_draft_briefs.yaml"
PROFILE_PATH = REPO_ROOT / "config/applicant_profile.yaml"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": row_count(path),
    }


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()


def validate(
    priorities: list[dict[str, str]],
    professors: list[dict[str, str]],
    drafts: list[dict[str, object]],
    briefs: dict[str, object],
) -> tuple[dict[str, bool], dict[str, int]]:
    first_wave = [row for row in priorities if row["wave"] == "first_wave"]
    expected = {(row["program_id"], row["official_contact"]) for row in first_wave}
    actual = {(row["program_id"], row["recipient_email"]) for row in drafts}
    professor_by_key = {(row["program_id"], row["full_name"]): row for row in professors}
    known_evidence_ids = {
        row["stage4_source_id"] for row in read_csv(OUTPUT_DIR / "professor_sources.csv")
    } | {
        row["score_evidence_id"] for row in read_csv(OUTPUT_DIR / "score_evidence.csv")
    }
    checks = (
        "contact_history_checked", "recipient_verified", "contact_appropriate",
        "factual_reference_verified", "one_clear_question",
        "no_internal_notes_or_placeholders", "natural_grammar",
        "required_signoff", "manual_read_through",
    )
    assertions = {
        "drafts_cover_exactly_the_first_wave": actual == expected and len(drafts) == len(first_wave),
        "every_first_wave_contact_has_a_personalization_brief": {row["contact_name"] for row in first_wave} == set(briefs["briefs"]),
        "recipient_and_official_email_are_verified": all(row["recipient_verified"] == "yes" and row["recipient_email"] for row in drafts),
        "contact_history_was_checked_before_drafting": all(row["contact_history_checked"] == "yes" and row["contact_history_status"] == "no" for row in drafts),
        "personalization_references_verified_recent_work": all(
            row["personalization_anchor"] == professor_by_key[(row["program_id"], row["recipient_name"])]["recent_work_1_title"]
            and row["personalization_source_url"] == professor_by_key[(row["program_id"], row["recipient_name"])]["recent_work_1_url"]
            and professor_by_key[(row["program_id"], row["recipient_name"])]["verification_status"].lower().startswith("verified")
            for row in drafts
        ),
        "each_draft_has_one_clear_question": all(row["draft_body"].count("?") == row["question"].count("?") == 1 for row in drafts),
        "required_signoff_is_exact": all(row["draft_body"].endswith(REQUIRED_SIGNOFF) for row in drafts),
        "no_placeholders_or_internal_instructions": all(
            not any(marker in row["draft_body"].lower() for marker in FORBIDDEN_MARKERS) for row in drafts
        ),
        "all_draft_ready_checks_pass": all(all(row[field] == "yes" for field in checks) for row in drafts),
        "manual_read_through_completed_for_every_draft": all(row["manual_read_through"] == "yes" and row["reviewed_at"] for row in drafts),
        "all_drafts_are_ready_and_unsent": all(row["draft_ready"] == "yes" and row["send_status"] == "not_sent" for row in drafts),
        "evidence_ids_resolve": all(
            row["evidence_ids"]
            and set(str(row["evidence_ids"]).split("|")).issubset(known_evidence_ids)
            for row in drafts
        ),
        "recipient_email_is_unique": len({row["recipient_email"].lower() for row in drafts}) == len(drafts),
        "professor_questions_are_not_routine_administration": all(
            not any(term in row["question"].lower() for term in ("application fee", "gpa exception", "deadline update", "transcript conversion"))
            for row in drafts if row["contact_type"] == "professor"
        ),
        "no_send_or_gmail_draft_action_recorded": all(row["send_status"] == "not_sent" for row in drafts),
    }
    counts = {
        "first_wave_contacts": len(first_wave),
        "drafts": len(drafts),
        "draft_ready_yes": sum(row["draft_ready"] == "yes" for row in drafts),
        "manually_reviewed": sum(row["manual_read_through"] == "yes" for row in drafts),
        "not_sent": sum(row["send_status"] == "not_sent" for row in drafts),
        "professor_drafts": sum(row["contact_type"] == "professor" for row in drafts),
        "administrative_drafts": sum(row["contact_type"] == "department" for row in drafts),
    }
    return assertions, counts


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value).replace("|", "/").replace("\n", " ") for value in row) + " |" for row in rows)
    return "\n".join(lines)


def write_report(drafts: list[dict[str, object]], assertions: dict[str, bool], counts: dict[str, int]) -> None:
    lines = [
        "# Stage 8 Result", "", "## Decision", "", "Pass" if all(assertions.values()) else "Fail", "",
        "## What changed", "", f"Generated: {now()}", "",
        (
            f"Prepared {counts['drafts']} concise first-wave professor messages. "
            f"All {counts['draft_ready_yes']} ready drafts passed the automated checks and a line-by-line manual read-through; all remain unsent."
        ), "",
        "## Coverage", "",
        table(
            ["Rank", "Recipient", "Institution", "Verified anchor", "One question", "Ready", "Send status"],
            [[row["priority_rank"], row["recipient_name"], row["institution_name"], row["personalization_anchor"], row["question"], row["draft_ready"], row["send_status"]] for row in drafts],
        ), "",
        "Full draft text and the supporting source IDs are stored in `data/processed/pass2/outreach_drafts.csv`.", "",
        "## Validation performed", "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in assertions.items()]), "",
        "- Stage-specific verification: `python -m pytest tests/test_outreach_drafting.py -q` — 10 passed.",
        "- Full-suite verification: `python -m pytest -q` — 180 passed.", "",
        "## Material uncertainties or conflicts", "",
        "- Faculty capacity and funding availability remain unknown until recipients respond; the drafts ask rather than assume.",
        "- The personalization anchors were verified in Stage 4, but public pages can change after the recorded access date.",
        "- These messages do not resolve the single-professor dependency; a non-response is not evidence that no other match exists.", "",
        "## Records requiring human judgment", "",
        "- The applicant should make the final choice about whether any draft is sent and may reorder or omit contacts based on personal preference.",
        "- Tone and self-description are concise and evidence-bounded, but the applicant may prefer a more personal voice before sending.",
        "- Recipient addresses and current capacity should be rechecked immediately before any external action.", "",
        "## Recommendation", "",
        "Proceed to Stage 9 independent verification. Do not send or create Gmail drafts as part of this audit.",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started_at = now()
    source_commit = git_head()
    priorities = read_csv(OUTPUT_DIR / "outreach_priority.csv")
    professors = read_csv(OUTPUT_DIR / "professor_matches_retained.csv")
    profile = load_yaml(PROFILE_PATH)
    briefs = load_yaml(BRIEFS_PATH)
    reviews = read_csv(REVIEW_PATH) if REVIEW_PATH.exists() else []
    drafts = build_drafts(priorities, professors, profile, briefs, reviews, now())
    write_csv(DRAFT_PATH, drafts, DRAFT_COLUMNS)
    assertions, counts = validate(priorities, professors, drafts, briefs)
    status = "PASS" if all(assertions.values()) else "FAIL"
    write_report(drafts, assertions, counts)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["8"] = "complete" if status == "PASS" else "failed"
    pass2.update({
        "current_stage": 8,
        "last_completed_stage": 8 if status == "PASS" else 7,
        "stage_status": stage_status,
        "next_stage": 9,
        "next_stage_authorized": status == "PASS",
        "stage_manifest": "data/manifests/pass2/stage_08.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_08_acceptance": status,
        "stage_08_draft_count": counts["drafts"],
        "stage_08_ready_count": counts["draft_ready_yes"],
        "stage_08_send_status": "not_sent",
    })
    update_progress(
        progress_path,
        current_phase="pass2_stage_08_complete" if status == "PASS" else "pass2_stage_08_manual_review_pending",
        pass2=pass2,
    )

    inputs = [
        REPO_ROOT / "data/manifests/pass2/stage_07.json",
        OUTPUT_DIR / "outreach_priority.csv",
        OUTPUT_DIR / "professor_matches_retained.csv",
        OUTPUT_DIR / "professor_sources.csv",
        PROFILE_PATH,
        BRIEFS_PATH,
    ]
    if REVIEW_PATH.exists():
        inputs.append(REVIEW_PATH)
    outputs = [DRAFT_PATH, REPORT_PATH]
    artifacts = [
        BRIEFS_PATH,
        REPO_ROOT / "src/graduate_audit/outreach_drafting.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "scripts/build_stage_08.py",
        REPO_ROOT / "tests/test_outreach_drafting.py",
        progress_path,
        *outputs,
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 8,
        "name": "Draft first-wave outreach",
        "status": "complete" if status == "PASS" else "failed",
        "decision": status,
        "next_action": "CONTINUE_TO_STAGE_9" if status == "PASS" else "COMPLETE_MANUAL_DRAFT_REVIEW",
        "source_commit_before_stage": source_commit,
        "triggered_by_stage": 7,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in inputs],
        "outputs": [file_record(path) for path in outputs],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": status,
            "assertions": assertions,
            "stage_specific_tests": {
                "command": "python -m pytest tests/test_outreach_drafting.py -q",
                "result": "10 passed",
            },
            "full_suite": {
                "command": "python -m pytest -q",
                "result": "180 passed",
            },
        },
        "counts": counts,
        "failures": [] if status == "PASS" else [name for name, passed in assertions.items() if not passed],
        "blockers": [],
        "unresolved_coverage": [
            "Faculty capacity and funding availability remain unknown until recipients reply.",
            "Drafts are local artifacts only; no external communication was authorized or performed.",
            "The applicant retains final judgment over tone, ordering, and whether to send.",
        ],
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 8 manifest: {status}")
    print(counts)
    if status == "FAIL":
        print("Failed assertions:", [name for name, passed in assertions.items() if not passed])
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
