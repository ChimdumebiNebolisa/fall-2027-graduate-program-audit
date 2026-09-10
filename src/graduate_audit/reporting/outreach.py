from __future__ import annotations

import argparse
from pathlib import Path
import json

from graduate_audit.io import read_csv, write_csv
from graduate_audit.schema import PROFESSOR_COLUMNS

ADMIN_COLUMNS = (
    "Priority", "University", "Program", "Department", "Contact Name", "Contact Role",
    "Official Email", "Question to Resolve", "Why It Matters", "Already Contacted?",
    "Date Contacted", "Response", "Follow-Up Date", "Outcome", "Notes",
)
OUTREACH_COLUMNS = (
    "rank", "contact_type", "university", "program", "recipient", "recipient_email",
    "subject", "personalization_anchor", "body", "already_contacted", "outreach_score",
)


def _integer(value: object) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _yes(value: object) -> bool:
    return str(value or "").strip().lower().startswith(("yes", "required", "encouraged", "appropriate"))


def _combine_admin(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(root.glob("data/processed/deep_review/*/admin_contacts.csv")):
        for row in read_csv(path):
            normalized = {}
            for column in ADMIN_COLUMNS:
                snake = column.lower().replace("?", "").replace("-", "_").replace(" ", "_")
                normalized[column] = row.get(column) or row.get(snake) or ""
            normalized["University"] = normalized["University"] or row.get("institution_name", "")
            normalized["Program"] = normalized["Program"] or row.get("program_name", "")
            normalized["Department"] = normalized["Department"] or row.get("department", "")
            normalized["Priority"] = normalized["Priority"] or row.get("priority", "")
            normalized["Contact Name"] = normalized["Contact Name"] or row.get("contact_name", "")
            normalized["Contact Role"] = normalized["Contact Role"] or row.get("contact_role", "")
            normalized["Official Email"] = normalized["Official Email"] or row.get("official_email", "")
            normalized["Question to Resolve"] = normalized["Question to Resolve"] or row.get("question_to_resolve", "")
            normalized["Why It Matters"] = normalized["Why It Matters"] or row.get("why_it_matters", "")
            rows.append(normalized)
    return rows


def _merge_history(professors: list[dict[str, str]], private_history: Path) -> None:
    if not private_history.exists():
        return
    history = {row.get("official_email", "").lower(): row for row in read_csv(private_history)}
    for row in professors:
        prior = history.get(row.get("official_email", "").lower())
        if not prior:
            continue
        row["already_contacted"] = prior.get("already_contacted", "Yes")
        row["last_contact_date"] = prior.get("last_contact_date", "")
        row["previous_outcome"] = prior.get("previous_outcome", "Prior relevant contact found")


def _professor_draft(row: dict[str, str]) -> tuple[str, str]:
    surname = row.get("full_name", "Professor").split()[-1]
    degree = row.get("program_name", "graduate program")
    anchor = row.get("recent_work_1") or row.get("sustained_research_evidence") or row.get("research_themes")
    angle = row.get("recommended_outreach_angle") or row.get("fit_explanation")
    question = row.get("specific_question_goal") or f"Do you anticipate supervising a funded Fall 2027 student in {degree} whose work would examine reliable AI-assisted software engineering?"
    prior = str(row.get("already_contacted", "")).lower().startswith("yes")
    opening = "I am following up on my earlier message." if prior else "I am writing to ask about prospective Fall 2027 graduate supervision."
    body = (
        f"Dear Professor {surname},\n\n"
        f"{opening} I am Chimdumebi Mitchell Nebolisa, a Computer Science undergraduate at East Texas A&M University graduating in May 2027. "
        "My research includes TerraProbe, work on LLM-based Terraform repair accepted as a full paper at ICTAI 2026, and Evidex, work on evidence-based claim verification and evaluation.\n\n"
        f"I was especially interested in {anchor}. {angle}\n\n"
        f"{question.rstrip('?')}?\n\n"
        "yours sincerely,\n"
        "Chimdumebi Mitchell Nebolisa"
    )
    subject = f"Prospective Fall 2027 student — {row.get('research_themes') or 'reliable AI for software engineering'}"
    return subject[:150], body


def _admin_draft(row: dict[str, str]) -> tuple[str, str]:
    recipient = row.get("Contact Name") or row.get("Contact Role") or "Graduate Program Coordinator"
    greeting = recipient if recipient.lower().startswith(("dr", "professor")) else "Graduate Program Team"
    question = row.get("Question to Resolve", "").rstrip("?")
    body = (
        f"Dear {greeting},\n\n"
        f"I am an international applicant completing a U.S. B.S. in Computer Science in May 2027 and am considering the {row.get('Program')} at {row.get('University')}.\n\n"
        f"{question}?\n\n"
        "yours sincerely,\n"
        "Chimdumebi Mitchell Nebolisa"
    )
    return f"Fall 2027 {row.get('Program')} question", body


def prepare(repo_root: Path, output_root: Path, limit: int = 15) -> None:
    professors = read_csv(output_root / "professor_evidence.csv")
    _merge_history(professors, repo_root / "data/private/gmail_contact_history.csv")
    write_csv(output_root / "professor_evidence.csv", professors, PROFESSOR_COLUMNS)

    admins = _combine_admin(repo_root)
    write_csv(output_root / "admin_contacts.csv", admins, ADMIN_COLUMNS)

    portfolio = json.loads((output_root / "portfolio.json").read_text(encoding="utf-8"))
    core_ids = {row.get("program_id", "") for row in portfolio.get("core", [])}
    reserve_ids = {row.get("program_id", "") for row in portfolio.get("reserve", [])}
    program_rows = read_csv(output_root / "program_screening.csv")
    program_by_id = {row.get("program_id", ""): row for row in program_rows}
    route_by_name = {
        (row.get("institution_name", ""), row.get("program_name", "")): row.get("program_id", "")
        for row in program_rows
    }
    professor_candidates: list[tuple[int, str, dict[str, str]]] = []
    for row in professors:
        if not row.get("official_email") or not _yes(row.get("contacting_faculty_appropriate")):
            continue
        program_id = row.get("program_id", "")
        if program_id not in core_ids and program_id not in reserve_ids:
            continue
        score = _integer(row.get("outreach_score"))
        if score == 0:
            score = {"exceptional": 90, "direct": 84, "strong": 78, "adjacent": 60}.get(row.get("fit_strength", "").lower(), 50)
        score += 100 if program_id in core_ids else 80
        score += _integer(program_by_id.get(program_id, {}).get("overall_score"))
        if row.get("recruiting_status") == "Confirmed recruiting":
            score += 10
        professor_candidates.append((score, "Professor", row))
    admin_candidates: list[tuple[int, str, dict[str, str]]] = []
    for row in admins:
        program_id = route_by_name.get((row.get("University", ""), row.get("Program", "")), "")
        priority = row.get("Priority", "").lower()
        if program_id in reserve_ids and ("first" in priority or "high" in priority) and row.get("Official Email"):
            admin_candidates.append((185, "Admin", row))

    professor_candidates.sort(key=lambda item: item[0], reverse=True)
    admin_candidates.sort(key=lambda item: (item[2].get("University", ""), item[2].get("Program", "")))
    candidates = professor_candidates[: max(0, limit - min(3, len(admin_candidates)))] + admin_candidates[:3]
    candidates.sort(key=lambda item: item[0], reverse=True)
    selected: list[tuple[int, str, dict[str, str]]] = []
    used_email: set[str] = set()
    institution_counts: dict[str, int] = {}
    for score, contact_type, row in candidates:
        email = (row.get("official_email") if contact_type == "Professor" else row.get("Official Email", "")).lower()
        university = row.get("institution_name") if contact_type == "Professor" else row.get("University", "")
        if not email or email in used_email or institution_counts.get(university, 0) >= 2:
            continue
        selected.append((score, contact_type, row))
        used_email.add(email)
        institution_counts[university] = institution_counts.get(university, 0) + 1
        if len(selected) >= limit:
            break

    drafts: list[dict[str, object]] = []
    first_wave_professor_ids: set[str] = set()
    for rank, (score, contact_type, row) in enumerate(selected, start=1):
        if contact_type == "Professor":
            subject, body = _professor_draft(row)
            first_wave_professor_ids.add(row.get("professor_id", ""))
            university, program = row.get("institution_name", ""), row.get("program_name", "")
            recipient, email = row.get("full_name", ""), row.get("official_email", "")
            anchor = row.get("recent_work_1") or row.get("sustained_research_evidence", "")
            prior = row.get("already_contacted", "No")
        else:
            subject, body = _admin_draft(row)
            university, program = row.get("University", ""), row.get("Program", "")
            recipient, email = row.get("Contact Name") or row.get("Contact Role", ""), row.get("Official Email", "")
            anchor = row.get("Question to Resolve", "")
            prior = row.get("Already Contacted?", "No")
        drafts.append({
            "rank": rank, "contact_type": contact_type, "university": university,
            "program": program, "recipient": recipient, "recipient_email": email,
            "subject": subject, "personalization_anchor": anchor, "body": body,
            "already_contacted": prior, "outreach_score": score,
        })

    for row in professors:
        if row.get("professor_id", "") in first_wave_professor_ids:
            row["outreach_priority"] = "First wave"
        elif row.get("official_email") and _yes(row.get("contacting_faculty_appropriate")):
            row["outreach_priority"] = row.get("outreach_priority") or "Second wave"
    write_csv(output_root / "professor_evidence.csv", professors, PROFESSOR_COLUMNS)
    write_csv(output_root / "outreach_drafts.csv", drafts, OUTREACH_COLUMNS)
    print(f"Prepared {len(drafts)} unsent first-wave drafts and {len(admins)} admin rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()
    prepare(Path(args.repo_root).resolve(), Path(args.output_dir).resolve(), args.limit)


if __name__ == "__main__":
    main()
