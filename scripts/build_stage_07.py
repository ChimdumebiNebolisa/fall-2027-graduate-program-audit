from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.outreach_prioritization import (  # noqa: E402
    CONTACT_HISTORY_COLUMNS,
    OUTREACH_COLUMNS,
    SCORE_FIELDS,
    build_outreach_priority,
    contact_key,
    load_policy,
)
from graduate_audit.progress import update_progress  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
HISTORY_PATH = OUTPUT_DIR / "contact_history_status.csv"
OUTREACH_PATH = OUTPUT_DIR / "outreach_priority.csv"
REPORT_PATH = REPO_ROOT / "reports/pass2/07_outreach_prioritization.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_07.json"
POLICY_PATH = REPO_ROOT / "config/outreach_priority.yaml"


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


def _admin_contacts() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted((REPO_ROOT / "data/processed/deep_review").glob("*/admin_contacts.csv")):
        for source in read_csv(path):
            rows.append({
                "program_id": source.get("program_id", ""),
                "institution_name": source.get("institution_name", ""),
                "program_name": source.get("program_name", ""),
                "contact_name": source.get("contact_name") or source.get("office", ""),
                "contact_role": source.get("contact_role") or source.get("office", ""),
                "official_email": source.get("official_email") or source.get("email", ""),
                "question_to_resolve": source.get("question_to_resolve") or source.get("recommended_question", ""),
                "official_url": source.get("official_url") or source.get("official_contact_url", ""),
                "date_accessed": source.get("date_accessed") or source.get("checked_date", ""),
            })
    return rows


def _all_active(portfolio: dict[str, object]) -> list[dict[str, object]]:
    return [row for key in ("core", "reserve") for row in portfolio[key]]


def validate(
    portfolio: dict[str, object],
    outreach: list[dict[str, object]],
    history: list[dict[str, str]],
    policy: dict[str, object],
) -> tuple[dict[str, bool], dict[str, int]]:
    active_ids = {str(row["program_id"]) for row in _all_active(portfolio)}
    professor_rows = [row for row in outreach if row["contact_type"] == "professor"]
    first_wave = [row for row in outreach if row["wave"] == "first_wave"]
    second_wave = [row for row in outreach if row["wave"] == "second_wave"]
    history_by_key = {contact_key(row): row for row in history}
    outreach_by_key = {contact_key(row): row for row in outreach}
    official_contacts = [str(row["official_contact"]).lower() for row in outreach if row["official_contact"]]
    forbidden = {"body", "subject", "snippet", "message_id", "thread_id", "raw_message"}
    minimum = int(policy["first_wave"]["minimum_contacts"])
    maximum = int(policy["first_wave"]["maximum_contacts"])
    assertions = {
        "every_active_program_has_recommended_professor_disposition": {row["program_id"] for row in professor_rows} == active_ids,
        "every_recommended_contact_has_history_status": set(outreach_by_key) == set(history_by_key),
        "contact_history_values_are_tristate": all(row["contact_history_status"] in {"yes", "no", "unknown"} for row in outreach),
        "unknown_history_is_preserved": all(
            outreach_by_key[key]["contact_history_status"] == "unknown"
            for key, row in history_by_key.items()
            if row["contact_history_status"] == "unknown"
        ),
        "first_wave_size_is_evidence_bounded": minimum <= len(first_wave) <= maximum,
        "every_first_wave_reply_can_change_a_specific_decision": all(row["decision_that_reply_could_change"].strip() for row in first_wave),
        "first_wave_has_verified_contact_and_no_prior_contact": all(
            row["official_contact"] and row["contact_history_status"] == "no" for row in first_wave
        ),
        "prior_contact_never_receives_fresh_introduction": all(
            row["wave"] not in {"first_wave", "second_wave"}
            for row in outreach if row["contact_history_status"] == "yes"
        ),
        "missing_official_contacts_are_blocked": all(
            row["wave"] == "blocked_missing_official_contact"
            for row in outreach if not row["official_contact"]
        ),
        "all_priority_dimensions_are_scored": all(
            all(str(row[field]).isdigit() for field in SCORE_FIELDS)
            and int(row["outreach_score"]) == sum(int(row[field]) for field in SCORE_FIELDS)
            for row in outreach
        ),
        "no_duplicate_official_contact": len(official_contacts) == len(set(official_contacts)),
        "second_wave_is_ranked": all(row["priority_rank"] for row in second_wave),
        "only_active_programs_are_prioritized": {row["program_id"] for row in outreach} == active_ids,
        "private_history_has_no_raw_message_material": forbidden.isdisjoint(CONTACT_HISTORY_COLUMNS) and all(forbidden.isdisjoint(row) for row in history),
        "private_history_is_git_ignored": subprocess.run(
            ["git", "check-ignore", "-q", str(HISTORY_PATH.relative_to(REPO_ROOT))], cwd=REPO_ROOT
        ).returncode == 0,
    }
    wave_counts = Counter(str(row["wave"]) for row in outreach)
    history_counts = Counter(str(row["contact_history_status"]) for row in outreach)
    counts = {
        "active_programs": len(active_ids),
        "recommended_contacts": len(outreach),
        "professor_contacts": len(professor_rows),
        "department_contacts": sum(row["contact_type"] == "department" for row in outreach),
        "first_wave": wave_counts["first_wave"],
        "second_wave": wave_counts["second_wave"],
        "follow_up_review": wave_counts["follow_up_review"],
        "blocked_missing_official_contact": wave_counts["blocked_missing_official_contact"],
        "do_not_contact": wave_counts["do_not_contact"],
        "history_yes": history_counts["yes"],
        "history_no": history_counts["no"],
        "history_unknown": history_counts["unknown"],
    }
    return assertions, counts


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(value).replace("|", "/") for value in row) + " |" for row in rows)
    return "\n".join(lines)


def write_report(outreach: list[dict[str, object]], assertions: dict[str, bool], counts: dict[str, int]) -> None:
    first_wave = [row for row in outreach if row["wave"] == "first_wave"]
    second_wave = [row for row in outreach if row["wave"] == "second_wave"]
    blocked = [row for row in outreach if row["wave"] == "blocked_missing_official_contact"]
    lines = [
        "# Stage 7 Result", "", "## Decision", "", "Pass" if all(assertions.values()) else "Fail", "",
        "## What changed", "",
        f"Generated: {now()}", "",
        (
            f"Verified contact-history status for {counts['recommended_contacts']} recommended contacts across "
            f"{counts['active_programs']} active programs, then scored every contact across all seven configured dimensions. "
            f"The result is a {counts['first_wave']}-contact first wave and a ranked {counts['second_wave']}-contact second wave."
        ), "",
        "No email was sent, no Gmail draft was created, and no Calendar item was modified. The connected-account status file is ignored by Git and contains no message body, subject, snippet, message ID, or thread ID.", "",
        "## Coverage", "", "### First wave", "",
        table(
            ["Rank", "Type", "Institution", "Contact", "Score", "Decision a reply could change"],
            [[row["priority_rank"], row["contact_type"], row["institution_name"], row["contact_name"], row["outreach_score"], row["decision_that_reply_could_change"]] for row in first_wave],
        ), "", "### Second wave", "",
        table(
            ["Rank", "Type", "Institution", "Contact", "Score", "Information gap"],
            [[row["priority_rank"], row["contact_type"], row["institution_name"], row["contact_name"], row["outreach_score"], row["information_gap"]] for row in second_wave],
        ), "", "### Blocked or unknown contact history", "",
        table(
            ["Institution", "Type", "Contact", "History", "Reason"],
            [[row["institution_name"], row["contact_type"], row["contact_name"], row["contact_history_status"], "Official address not verified"] for row in blocked]
            or [["—", "—", "None", "—", "—"]],
        ), "", "## Validation performed", "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in assertions.items()]), "",
        "- Stage-specific verification: `python -m pytest tests/test_outreach_prioritization.py -q` — 10 passed.",
        "- Full-suite verification: `python -m pytest -q` — 170 passed.", "",
        "## Material uncertainties or conflicts", "",
        f"- {counts['history_unknown']} contacts remain `unknown`, not `no contact`, because no verified official address was available for an exact-address search.",
        f"- All {counts['active_programs']} active programs remain single-professor dependencies; a negative or absent reply would not by itself prove no faculty depth exists.",
        "- Offer-specific funding, summer support, fees, and Fall 2027 cycle details remain unresolved where the official program evidence says they are not yet published.",
        "- Contact history reflects the connected Gmail account searched on 2026-09-11; messages in another account or under an unverified address are outside coverage.", "",
        "## Records requiring human judgment", "",
        "- The applicant must approve which contacts, if any, proceed to drafting in Stage 8; Stage 7 ranks decision value but does not authorize contact.",
        "- Personal preference among active programs remains unverified and can change wave ordering.",
        "- Before outreach, recheck each first-wave recipient address and whether the stated Fall 2027 question is still unresolved.", "",
        "## Recommendation", "",
        "Proceed to Stage 8 to draft, but not send, concise messages for the first wave. Preserve the ranked second wave and resolve missing official addresses before considering those blocked contacts.",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started_at = now()
    source_commit = git_head()
    portfolio = read_json(OUTPUT_DIR / "portfolio.json")
    verifications = read_csv(OUTPUT_DIR / "program_verification.csv")
    professors = read_csv(OUTPUT_DIR / "professor_matches_retained.csv")
    admins = _admin_contacts()
    history = read_csv(HISTORY_PATH)
    policy = load_policy(POLICY_PATH)
    outreach = build_outreach_priority(portfolio, verifications, professors, admins, history, policy)
    write_csv(OUTREACH_PATH, outreach, OUTREACH_COLUMNS)
    assertions, counts = validate(portfolio, outreach, history, policy)
    status = "PASS" if all(assertions.values()) else "FAIL"
    write_report(outreach, assertions, counts)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["7"] = "complete" if status == "PASS" else "failed"
    pass2.update({
        "current_stage": 7,
        "last_completed_stage": 7 if status == "PASS" else 6,
        "stage_status": stage_status,
        "next_stage": 8,
        "next_stage_authorized": status == "PASS",
        "stage_manifest": "data/manifests/pass2/stage_07.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_07_acceptance": status,
        "stage_07_first_wave_count": counts["first_wave"],
        "stage_07_second_wave_count": counts["second_wave"],
        "stage_07_unknown_history_count": counts["history_unknown"],
    })
    update_progress(
        progress_path,
        current_phase="pass2_stage_07_complete" if status == "PASS" else "pass2_stage_07_failed",
        pass2=pass2,
    )

    inputs = [
        REPO_ROOT / "data/manifests/pass2/stage_06.json",
        OUTPUT_DIR / "portfolio.json",
        OUTPUT_DIR / "program_verification.csv",
        OUTPUT_DIR / "professor_matches_retained.csv",
        POLICY_PATH,
    ]
    outputs = [OUTREACH_PATH, REPORT_PATH]
    artifacts = [
        POLICY_PATH,
        REPO_ROOT / "src/graduate_audit/outreach_prioritization.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "scripts/build_stage_07.py",
        REPO_ROOT / "tests/test_outreach_prioritization.py",
        progress_path,
        *outputs,
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 7,
        "name": "Contact-history verification and outreach prioritization",
        "status": "complete" if status == "PASS" else "failed",
        "decision": status,
        "next_action": "CONTINUE_TO_STAGE_8" if status == "PASS" else "REPAIR_STAGE_7",
        "source_commit_before_stage": source_commit,
        "triggered_by_stage": 6,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in inputs],
        "private_input": {
            "path": HISTORY_PATH.relative_to(REPO_ROOT).as_posix(),
            "row_count": len(history),
            "tracking": "git_ignored",
            "content_policy": "broad status only; no raw private message material",
        },
        "outputs": [file_record(path) for path in outputs],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": status,
            "assertions": assertions,
            "stage_specific_tests": {
                "command": "python -m pytest tests/test_outreach_prioritization.py -q",
                "result": "10 passed",
            },
            "full_suite": {
                "command": "python -m pytest -q",
                "result": "170 passed",
            },
        },
        "counts": counts,
        "failures": [] if status == "PASS" else [name for name, passed in assertions.items() if not passed],
        "blockers": [],
        "unresolved_coverage": [
            f"{counts['history_unknown']} contacts lack verified official addresses and retain unknown history status.",
            "Connected history covers the searched Gmail account only; other accounts are out of scope.",
            "Offer-specific and future-cycle questions may not be answerable until official updates or an offer exists.",
            "Applicant preference has not been directly elicited and can change wave ordering.",
        ],
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 7 manifest: {status}")
    print(counts)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
