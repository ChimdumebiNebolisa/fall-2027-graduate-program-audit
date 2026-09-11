from __future__ import annotations

import hashlib
from pathlib import Path
import re

import yaml


DRAFT_COLUMNS = (
    "schema_version", "draft_id", "priority_rank", "wave", "program_id",
    "institution_name", "program_name", "contact_type", "recipient_name",
    "recipient_email", "subject", "personalization_anchor",
    "personalization_source_url", "verified_applicant_background", "question",
    "draft_body", "contact_history_checked", "contact_history_status",
    "recipient_verified", "contact_appropriate", "factual_reference_verified",
    "one_clear_question", "no_internal_notes_or_placeholders", "natural_grammar",
    "required_signoff", "manual_read_through", "draft_ready", "send_status",
    "evidence_ids", "generated_by", "reviewed_at",
)

REQUIRED_SIGNOFF = "yours sincerely,\nChimdumebi Mitchell Nebolisa"
FORBIDDEN_MARKERS = (
    "[insert", "[name", "[university", "[paper", "<insert", "todo", "tbd",
    "placeholder", "drafting note", "internal instruction", "chatgpt",
)


def load_yaml(path: str | Path) -> dict[str, object]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _draft_id(program_id: str, recipient_email: str) -> str:
    payload = f"{program_id}|{recipient_email.lower()}".encode("utf-8")
    return f"draft:{hashlib.sha256(payload).hexdigest()[:16]}"


def _surname(full_name: str) -> str:
    cleaned = re.sub(r"\([^)]*\)", "", full_name).strip()
    return cleaned.split()[-1]


def _background(profile: dict[str, object], key: str) -> tuple[str, str]:
    identity = (
        f"I am {profile['name']}, an undergraduate studying computer science at {profile['current_institution']} "
        "graduating in May 2027."
    )
    statements = {
        "terraprobe": "TerraProbe, my research on LLM-based Terraform repair, has been accepted as a full paper at ICTAI 2026.",
        "evidex": "My Evidex research examines evidence-based claim verification and evaluation.",
        "both": "My research includes TerraProbe, an ICTAI 2026 full paper on LLM-based Terraform repair, and Evidex, which examines evidence-based claim verification and evaluation.",
    }
    return identity, statements[key]


def _review_by_id(manual_reviews: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("draft_id", ""): row for row in manual_reviews}


def build_drafts(
    priorities: list[dict[str, str]],
    professors: list[dict[str, str]],
    applicant_profile: dict[str, object],
    draft_briefs: dict[str, object],
    manual_reviews: list[dict[str, str]],
    reviewed_at: str,
) -> list[dict[str, object]]:
    first_wave = [row for row in priorities if row.get("wave") == "first_wave"]
    professor_by_key = {
        (row.get("program_id", ""), row.get("full_name", "")): row
        for row in professors
    }
    reviews = _review_by_id(manual_reviews)
    briefs = draft_briefs["briefs"]
    drafts: list[dict[str, object]] = []
    for priority in first_wave:
        if priority.get("contact_type") != "professor":
            raise ValueError(f"Stage 8 first-wave administrative drafting is not configured: {priority.get('contact_name')}")
        professor = professor_by_key[(priority["program_id"], priority["contact_name"])]
        brief = briefs[priority["contact_name"]]
        identity, background = _background(applicant_profile, brief["background"])
        anchor = professor["recent_work_1_title"].strip()
        source_url = professor["recent_work_1_url"].strip()
        question = str(brief["question"]).strip()
        if not question.endswith("?"):
            question += "?"
        body = (
            f"Dear Professor {_surname(priority['contact_name'])},\n\n"
            f"{identity} {background}\n\n"
            f"I was interested in your recent work titled \"{anchor}\". {brief['connection']}\n\n"
            f"{question}\n\n"
            f"{REQUIRED_SIGNOFF}"
        )
        draft_id = _draft_id(priority["program_id"], priority["official_contact"])
        review = reviews.get(draft_id, {})
        manual_read = review.get("manual_read_through", "no").lower() == "yes"
        one_question = body.count("?") == 1 and question.count("?") == 1
        no_markers = not any(marker in body.lower() for marker in FORBIDDEN_MARKERS)
        factual = bool(anchor and source_url and professor.get("verification_status", "").lower().startswith("verified"))
        ready_checks = {
            "contact_history_checked": priority.get("contact_history_status") in {"yes", "no", "unknown"},
            "recipient_verified": priority.get("verification_status") == "verified" and bool(priority.get("official_contact")),
            "contact_appropriate": int(priority.get("appropriateness_score", "0")) > 0,
            "factual_reference_verified": factual,
            "one_clear_question": one_question,
            "no_internal_notes_or_placeholders": no_markers,
            "natural_grammar": review.get("natural_grammar", "no").lower() == "yes",
            "required_signoff": body.endswith(REQUIRED_SIGNOFF),
            "manual_read_through": manual_read,
        }
        drafts.append({
            "schema_version": "2.0",
            "draft_id": draft_id,
            "priority_rank": priority["priority_rank"],
            "wave": "first_wave",
            "program_id": priority["program_id"],
            "institution_name": priority["institution_name"],
            "program_name": priority["program_name"],
            "contact_type": "professor",
            "recipient_name": priority["contact_name"],
            "recipient_email": priority["official_contact"],
            "subject": brief["subject"],
            "personalization_anchor": anchor,
            "personalization_source_url": source_url,
            "verified_applicant_background": f"{identity} {background}",
            "question": question,
            "draft_body": body,
            **{key: "yes" if value else "no" for key, value in ready_checks.items()},
            "contact_history_status": priority["contact_history_status"],
            "draft_ready": "yes" if all(ready_checks.values()) else "no",
            "send_status": "not_sent",
            "evidence_ids": priority["evidence_ids"],
            "generated_by": "graduate_audit.outreach_drafting:v1",
            "reviewed_at": reviewed_at if manual_read else "",
        })
    return drafts
