from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

import yaml


OUTREACH_COLUMNS = (
    "schema_version", "priority_rank", "wave", "portfolio_status", "program_id",
    "institution_name", "program_name", "contact_type", "contact_name",
    "official_contact", "contact_source_url", "contact_history_status",
    "last_relevant_contact_date", "reply_received", "follow_up_appropriate",
    "information_value_score", "research_match_score",
    "admission_supervisor_impact_score", "funding_supervisor_impact_score",
    "resolvable_uncertainty_score", "appropriateness_score", "timing_score",
    "outreach_score", "information_gap", "decision_that_reply_could_change",
    "recommended_outreach_angle", "evidence_ids", "scoring_process",
    "verification_status",
)

CONTACT_HISTORY_COLUMNS = (
    "schema_version", "program_id", "institution_name", "contact_type",
    "contact_name", "official_contact", "search_basis", "contact_history_status",
    "last_relevant_contact_date", "reply_received", "broad_outcome",
    "follow_up_appropriate", "checked_at", "source_scope",
)

SCORE_FIELDS = (
    "information_value_score", "research_match_score",
    "admission_supervisor_impact_score", "funding_supervisor_impact_score",
    "resolvable_uncertainty_score", "appropriateness_score", "timing_score",
)


def load_policy(path: str | Path) -> dict[str, object]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def split_ids(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace(";", "|").split("|") if item.strip()]


def verified_email(value: object) -> str:
    text = str(value or "").strip()
    return text if re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", text) else ""


def contact_key(row: dict[str, object]) -> str:
    email = verified_email(row.get("official_contact") or row.get("official_email"))
    if email:
        return f"email:{email.lower()}"
    return "name:" + "|".join(
        str(row.get(key, "")).strip().lower()
        for key in ("program_id", "contact_type", "contact_name")
    )


def _appropriate(value: object) -> bool:
    text = str(value or "").strip().lower()
    return text.startswith("yes") or "encourag" in text or "welcome" in text or "expected" in text


def _question(portfolio_row: dict[str, object]) -> str:
    answers = {int(row["question_number"]): row for row in portfolio_row.get("pressure_test_answers", [])}
    return str(answers.get(10, {}).get("answer") or portfolio_row.get("unresolved_conflicts") or "").strip()


def _reply_can_change(portfolio_row: dict[str, object]) -> bool:
    for answer in portfolio_row.get("pressure_test_answers", []):
        if int(answer.get("question_number", 0)) == 9:
            return str(answer.get("assessment", "")).lower() == "yes"
    return False


def _history_for(
    history_by_key: dict[str, dict[str, str]],
    candidate: dict[str, object],
) -> dict[str, str]:
    return history_by_key.get(
        contact_key(candidate),
        {
            "contact_history_status": "unknown",
            "last_relevant_contact_date": "",
            "reply_received": "unknown",
            "follow_up_appropriate": "unknown",
        },
    )


def _professor_scores(
    portfolio_row: dict[str, object],
    verification: dict[str, str],
    professor: dict[str, str],
) -> dict[str, int]:
    admissions = verification.get("admissions_model", "").lower()
    contact = verification.get("faculty_contact_expectation", "").lower()
    funding = verification.get("funding_model", "").lower()
    degree = verification.get("degree_type", "").lower()
    supervisor_led = "supervisor" in admissions or "supervisor" in contact or "master" in degree
    funding_dependent = "supervisor" in funding or "advisor funding" in funding
    confirmed = professor.get("recruiting_status", "").lower() == "confirmed recruiting"
    fit = professor.get("fit_strength", "").lower()
    return {
        "information_value_score": 25 if _reply_can_change(portfolio_row) else 10,
        "research_match_score": {"exceptional": 15, "strong": 15, "direct": 13, "adjacent": 8}.get(fit, 10),
        "admission_supervisor_impact_score": 15 if supervisor_led or confirmed else 10,
        "funding_supervisor_impact_score": 15 if funding_dependent or supervisor_led else 8,
        "resolvable_uncertainty_score": 15 if _question(portfolio_row) or professor.get("unresolved_question") else 5,
        "appropriateness_score": 10 if _appropriate(professor.get("contacting_faculty_appropriate")) else 0,
        "timing_score": 5 if confirmed or supervisor_led else 3,
    }


def _admin_scores(question: str, has_contact: bool) -> dict[str, int]:
    lower = question.lower()
    admission_terms = ("gpa", "eligib", "admission", "deadline", "application", "multiple")
    funding_terms = ("fund", "stipend", "summer", "fee", "insurance", "tuition", "support")
    future_only = "when the cycle" in lower or "in an offer" in lower or "offer-specific" in lower
    return {
        "information_value_score": 25,
        "research_match_score": 0,
        "admission_supervisor_impact_score": 15 if any(term in lower for term in admission_terms) else 5,
        "funding_supervisor_impact_score": 15 if any(term in lower for term in funding_terms) else 0,
        "resolvable_uncertainty_score": 15 if question else 0,
        "appropriateness_score": 10 if has_contact else 5,
        "timing_score": 2 if future_only else 5,
    }


def _base_row(
    portfolio_row: dict[str, object],
    contact_type: str,
    contact_name: str,
    official_contact: str,
    source_url: str,
    history: dict[str, str],
) -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "priority_rank": "",
        "wave": "pending",
        "portfolio_status": portfolio_row["portfolio_status"],
        "program_id": portfolio_row["program_id"],
        "institution_name": portfolio_row["institution_name"],
        "program_name": portfolio_row["program_name"],
        "contact_type": contact_type,
        "contact_name": contact_name,
        "official_contact": official_contact,
        "contact_source_url": source_url,
        "contact_history_status": history.get("contact_history_status", "unknown"),
        "last_relevant_contact_date": history.get("last_relevant_contact_date", ""),
        "reply_received": history.get("reply_received", "unknown"),
        "follow_up_appropriate": history.get("follow_up_appropriate", "unknown"),
        "information_gap": "",
        "decision_that_reply_could_change": "",
        "recommended_outreach_angle": "",
        "evidence_ids": "",
        "scoring_process": "graduate_audit.outreach_prioritization:v1",
        "verification_status": "verified",
    }


def build_outreach_priority(
    portfolio: dict[str, object],
    verifications: list[dict[str, str]],
    professors: list[dict[str, str]],
    admin_contacts: list[dict[str, str]],
    contact_history: list[dict[str, str]],
    policy: dict[str, object],
) -> list[dict[str, object]]:
    active = [row for key in ("core", "reserve") for row in portfolio.get(key, [])]
    portfolio_by_id = {str(row["program_id"]): row for row in active}
    verification_by_id = {row["candidate_program_id"]: row for row in verifications}
    professors_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in professors:
        professors_by_id[row["program_id"]].append(row)
    admin_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in admin_contacts:
        admin_by_id[row.get("program_id", "")].append(row)
    history_by_key = {contact_key(row): row for row in contact_history}
    candidates: list[dict[str, object]] = []

    for program_id, portfolio_row in portfolio_by_id.items():
        verification = verification_by_id[program_id]
        for professor in professors_by_id.get(program_id, []):
            official_contact = verified_email(professor.get("official_email"))
            lookup = {
                "program_id": program_id,
                "contact_type": "professor",
                "contact_name": professor.get("full_name", ""),
                "official_contact": official_contact,
            }
            history = _history_for(history_by_key, lookup)
            row = _base_row(
                portfolio_row,
                "professor",
                professor.get("full_name", ""),
                official_contact,
                professor.get("official_faculty_or_lab_url", ""),
                history,
            )
            row.update(_professor_scores(portfolio_row, verification, professor))
            row["information_gap"] = professor.get("unresolved_question") or _question(portfolio_row)
            row["decision_that_reply_could_change"] = (
                f"Retain or deprioritize {portfolio_row['program_name']} by confirming whether "
                f"{professor.get('full_name', 'the professor')} expects to supervise a funded Fall 2027 student in the verified overlap area."
            )
            row["recommended_outreach_angle"] = professor.get("fit_rationale") or professor.get("specific_overlap", "")
            row["evidence_ids"] = "|".join(dict.fromkeys(
                split_ids(professor.get("source_ids")) + [str(item) for item in portfolio_row.get("score_evidence_ids", [])]
            ))
            candidates.append(row)

        for admin in admin_by_id.get(program_id, []):
            official_contact = verified_email(admin.get("official_email"))
            contact_name = admin.get("contact_name") or admin.get("contact_role") or admin.get("office", "")
            lookup = {
                "program_id": program_id,
                "contact_type": "department",
                "contact_name": contact_name,
                "official_contact": official_contact,
            }
            history = _history_for(history_by_key, lookup)
            question = admin.get("question_to_resolve") or admin.get("recommended_question", "")
            row = _base_row(
                portfolio_row,
                "department",
                contact_name,
                official_contact,
                admin.get("official_url") or admin.get("official_contact_url", ""),
                history,
            )
            row.update(_admin_scores(question, bool(official_contact)))
            row["information_gap"] = question
            row["decision_that_reply_could_change"] = (
                f"Retain, defer, or remove {portfolio_row['program_name']} by resolving: {question}"
            )
            row["recommended_outreach_angle"] = "Ask only the unresolved administrative question; omit the research biography."
            row["evidence_ids"] = "|".join(str(item) for item in portfolio_row.get("score_evidence_ids", []))
            candidates.append(row)

    for row in candidates:
        row["outreach_score"] = sum(int(row[field]) for field in SCORE_FIELDS)
        if not row["official_contact"]:
            row["wave"] = "blocked_missing_official_contact"
            row["verification_status"] = "blocked"
        elif row["contact_history_status"] == "yes":
            row["wave"] = "follow_up_review"
        elif int(row["appropriateness_score"]) == 0:
            row["wave"] = "do_not_contact"

    eligible = [row for row in candidates if row["wave"] == "pending"]
    eligible.sort(key=lambda row: (-int(row["outreach_score"]), row["institution_name"], row["contact_name"]))
    first_wave = policy["first_wave"]
    target = min(int(first_wave["target_contacts"]), int(first_wave["maximum_contacts"]))
    target = max(target, int(first_wave["minimum_contacts"]))
    threshold = int(first_wave["minimum_score"])
    selected = [row for row in eligible if int(row["outreach_score"]) >= threshold][:target]
    selected_ids = {id(row) for row in selected}
    for row in eligible:
        row["wave"] = "first_wave" if id(row) in selected_ids else "second_wave"

    order = {"first_wave": 0, "second_wave": 1, "follow_up_review": 2, "blocked_missing_official_contact": 3, "do_not_contact": 4}
    candidates.sort(key=lambda row: (order[row["wave"]], -int(row["outreach_score"]), row["institution_name"], row["contact_name"]))
    for rank, row in enumerate(candidates, start=1):
        row["priority_rank"] = rank
    return candidates
