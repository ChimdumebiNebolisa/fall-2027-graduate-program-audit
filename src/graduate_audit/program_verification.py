from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable

from .io import read_csv, write_csv
from .schema import (
    PASS2_SCHEMA_VERSION,
    PROGRAM_EXCLUSION_COLUMNS_V2,
    PROGRAM_SOURCE_COLUMNS_V2,
    PROGRAM_VERIFICATION_COLUMNS_V2,
    canonical_url,
)

REGIONS = ("us", "canada", "europe")
FINAL_STATUSES = {"retained", "conditional", "monitor", "excluded"}
RESEARCH_DEGREE_TYPES = {
    "PhD",
    "Direct-entry PhD",
    "Integrated or structured doctorate",
    "PhD requiring a master's",
    "Thesis or research master's",
    "Project-based master's with substantial research",
}
UNKNOWN = "Not verified in frozen evidence"


def _text(value: object, fallback: str = UNKNOWN) -> str:
    value = str(value or "").strip()
    return value or fallback


def _path(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _split(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split("|") if part.strip()]


def _join(values: Iterable[str]) -> str:
    return "|".join(dict.fromkeys(value for value in values if value))


def _source_categories(claim_type: str) -> list[str]:
    value = claim_type.casefold()
    categories: list[str] = []
    rules = (
        (
            "funding",
            (
                "fund", "scholar", "stipend", "tuition", "award", "support",
                "assistantship", "ta/ra", "offer to", "renewal", "benefits",
            ),
        ),
        ("fees", ("fee",)),
        ("deadline", ("deadline",)),
        ("language", ("english", "language")),
        ("eligibility", ("eligib", "international", "bachelor", "gpa", "credential", "prerequisite")),
        ("admissions", ("admission", "application", "contact", "supervisor")),
        (
            "program",
            ("program status", "degree", "vacancy", "research route", "active", "phd", "msc", "doctoral", "dissertation", "thesis"),
        ),
        ("institution", ("institution", "recognition", "authority")),
    )
    for category, terms in rules:
        if any(term in value for term in terms):
            categories.append(category)
    return categories or ["supporting_evidence"]


def _source_categories_for(source: dict[str, str]) -> list[str]:
    claim_type = source.get("claim_type", "")
    exact_claim = source.get("exact_claim_supported", "")
    if claim_type.casefold() == "program/admissions/funding/faculty evidence":
        return _source_categories(exact_claim)
    return _source_categories(f"{claim_type} {exact_claim}")


def _stage3_source_id(candidate_program_id: str, source: dict[str, str]) -> str:
    fingerprint = "|".join(
        (
            candidate_program_id,
            source.get("source_id", ""),
            canonical_url(source.get("url", "")),
            source.get("exact_claim_supported", ""),
        )
    )
    return "stage3src:" + hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:20]


def _is_official(source: dict[str, str]) -> bool:
    return source.get("official_or_secondary", "").casefold().startswith("official")


def _relevant_source(source: dict[str, str]) -> bool:
    categories = set(_source_categories_for(source))
    return bool(
        categories
        & {
            "program",
            "admissions",
            "eligibility",
            "language",
            "deadline",
            "fees",
            "funding",
            "institution",
        }
    )


def _material_funding_supported(source_rows: list[dict[str, str]]) -> bool:
    return any(
        _is_official(source)
        and "funding" in _source_categories_for(source)
        for source in source_rows
    )


def _positive_funding(value: str) -> bool:
    normalized = value.casefold()
    negative = (
        "not confirmed",
        "not verified",
        "not guaranteed",
        "no guarantee",
        "not an unconditional guarantee",
        "no funding",
        "no fall 2027",
        "no 2027",
        "unknown",
        "insufficiently precise",
        "unfunded",
        "no independently",
        "strives to",
        "generally available",
        "generally supported",
        "typically receive",
        "most msc",
        "selected admitted",
        "may offer",
    )
    positive = (
        "guaranteed",
        "guarantees support",
        "full support",
        "full-support",
        "fully funded",
        "receive a stipend",
        "receive stipend",
        "tuition waiver",
        "support package",
        "funding package",
        "all admitted",
        "all phd",
        "all full-time",
        "100% of admitted",
        "every fall phd admit",
        "program-level support",
        "department minimum",
    )
    return not any(term in normalized for term in negative) and any(
        term in normalized for term in positive
    )


def _has_material_funding_claim(row: dict[str, str]) -> bool:
    values = [
        row.get(column, "").casefold()
        for column in (
            "funding_model", "funding_status", "funding_duration",
            "funding_conditions", "funding_international_eligibility",
            "stipend_amount", "stipend_currency", "tuition_coverage",
            "mandatory_fee_coverage", "health_insurance_coverage",
            "summer_coverage", "named_scholarships", "scholarship_deadlines",
        )
    ]
    material_terms = (
        "guarantee",
        "stipend",
        "tuition waiver",
        "tuition covered",
        "health insurance",
        "package",
        "assistantship",
        "fellowship",
        "studentship",
        "scholarship",
        "annual",
        "academic year",
        "full support",
        "full-support",
        "fully funded",
        "funded",
    )
    uncertainty_only = (
        "not verified",
        "not separately published or verified",
        "no independently sourced material funding claim retained",
        "not assessed",
        "pending deep review",
        "preliminary only",
        "unknown",
    )
    return any(
        any(term in value for term in material_terms)
        and not any(marker in value for marker in uncertainty_only)
        for value in values
    )


def _eligibility_state(record: dict[str, str]) -> str:
    bachelor = record.get("direct_from_bachelors_eligible", "").casefold().strip()
    international = record.get("international_student_eligible", "").casefold().strip()
    if (
        bachelor.startswith("no")
        or "applicant lacks" in bachelor
        or international.startswith("no")
        or "non-eu no" in international
    ):
        return "fail"
    if bachelor.startswith("yes") and international.startswith("yes"):
        return "pass"
    if bachelor and international and "unverified" not in bachelor + international:
        return "resolvable_question"
    return "unverified"


def _future_or_position_only(record: dict[str, str]) -> bool:
    text = " ".join(
        (
            record.get("funding_status", ""),
            record.get("biggest_risk", ""),
            record.get("unresolved_question", ""),
        )
    ).casefold()
    return any(
        term in text
        for term in (
            "no fall 2027 vacancy",
            "no 2027 award",
            "no fall 2027 salary",
            "monitor 2028",
            "future vacancy",
        )
    )


def _dominant_deep_programs(
    candidates: list[dict[str, str]], deep_by_id: dict[str, dict[str, str]]
) -> set[str]:
    deep_types: dict[str, set[str]] = defaultdict(set)
    for candidate in candidates:
        deep = deep_by_id.get(candidate["program_id"])
        if deep:
            deep_types[candidate["institution_id"]].add(deep.get("degree_type", ""))
    duplicates: set[str] = set()
    for candidate in candidates:
        if candidate["program_id"] in deep_by_id:
            continue
        if candidate.get("degree_type", "") in deep_types.get(candidate["institution_id"], set()):
            duplicates.add(candidate["program_id"])
    return duplicates


def _source_row(
    candidate: dict[str, str], source: dict[str, str], source_path: str
) -> dict[str, str]:
    categories = (
        ["discovery"]
        if source.get("source_type") == "derived candidate record"
        else _source_categories_for(source)
    )
    return {
        "schema_version": PASS2_SCHEMA_VERSION,
        "stage3_source_id": _stage3_source_id(candidate["program_id"], source),
        "candidate_program_id": candidate["program_id"],
        "institution_id": candidate["institution_id"],
        "institution_name": candidate["institution_name"],
        "claim_categories": _join(categories),
        "exact_claim_supported": _text(source.get("exact_claim_supported")),
        "source_title": _text(source.get("source_title")),
        "publisher": _text(source.get("publisher")),
        "url": source.get("url", "").strip(),
        "source_path": source_path,
        "source_type": _text(source.get("source_type")),
        "official_or_secondary": _text(source.get("official_or_secondary"), "derived"),
        "date_accessed": _text(source.get("date_accessed")),
        "admissions_cycle": _text(source.get("admissions_cycle")),
        "confidence": _text(source.get("confidence")),
        "verification_status": _text(source.get("verification_status")),
        "original_source_id": source.get("source_id", "").strip(),
        "access_note": source.get("access_note", "").strip(),
    }


def _derived_source(candidate: dict[str, str], candidate_path: str) -> dict[str, str]:
    url = candidate.get("official_program_url") or candidate.get("official_institution_url", "")
    source = {
        "source_id": "derived:" + hashlib.sha256(candidate["program_id"].encode()).hexdigest()[:16],
        "claim_type": "stage2 discovery record",
        "exact_claim_supported": (
            "Stage 2 recorded this row as a discovery candidate; it does not independently "
            "verify an exact current research program, eligibility, or funding."
        ),
        "source_title": "Pass 2 Stage 2 candidate funnel",
        "publisher": "Graduate audit pipeline",
        "url": url,
        "source_type": "derived candidate record",
        "official_or_secondary": "derived",
        "date_accessed": date.today().isoformat(),
        "admissions_cycle": "Not cycle-specific",
        "confidence": candidate.get("evidence_confidence", "low"),
        "verification_status": "Discovery evidence only",
        "access_note": "Use the source_record_paths field to trace the underlying discovery inputs.",
    }
    return _source_row(candidate, source, candidate_path)


def _status_for(
    candidate: dict[str, str], record: dict[str, str], deep: bool,
    has_funding_source: bool, duplicate_program: bool,
) -> tuple[str, str, str, str, str, str, str]:
    if candidate["funnel_status"] == "screened_out":
        reason = candidate.get("exclusion_reason") or record.get("exclusion_reason") or (
            "Stage 2 screened this discovery record out before program verification."
        )
        return (
            "excluded", reason, "fail", "not_assessed", "not_assessed",
            "not_assessed", "Do Not Advance",
        )
    if duplicate_program:
        return (
            "excluded",
            "A fully verified research route of the same degree type at this university supersedes this duplicate preliminary record.",
            "pass", "not_assessed", "not_assessed", "fail_duplicate_route",
            "Do Not Advance",
        )
    research_route = record.get("degree_type", candidate.get("degree_type", "")) in RESEARCH_DEGREE_TYPES
    structure_gate = "pass" if deep and research_route else "preliminary" if research_route else "unverified"
    eligibility = _eligibility_state(record) if deep else "unverified"
    if deep and (record.get("screening_decision", "").casefold() == "excluded" or eligibility == "fail"):
        return (
            "excluded",
            record.get("biggest_risk") or record.get("exclusion_reason") or "Applicant does not meet the verified entry route.",
            structure_gate, eligibility, "fail", "pass", "Do Not Advance",
        )
    if not deep:
        if candidate.get("official_program_url") and research_route:
            return (
                "monitor",
                "An official research-route page was recorded, but the frozen evidence does not verify the full eligibility, funding, fee, language, and Fall 2027 fields required by this gate.",
                structure_gate, eligibility, "unverified", "pass", "Monitor — Not Faculty-Review Ready",
            )
        return (
            "monitor",
            "The discovery record does not establish an exact current research degree route, so eligibility and funding cannot yet be evaluated.",
            structure_gate, eligibility, "unverified", "pass", "Monitor — Exact Program Required",
        )
    if _future_or_position_only(record):
        return (
            "monitor",
            record.get("biggest_risk") or "No Fall 2027 funded position is verified.",
            structure_gate, eligibility, "monitor_future_call", "pass",
            "Monitor for 2027 Position",
        )
    credible_funding = has_funding_source and _positive_funding(record.get("funding_status", ""))
    if research_route and eligibility == "pass" and credible_funding:
        return (
            "retained",
            "Relevant research route, applicant entry eligibility, and an independently sourced credible funding route are all present; offer-specific terms remain explicit.",
            structure_gate, eligibility, "pass", "pass", "Funded Application Candidate",
        )
    if research_route and eligibility in {"pass", "resolvable_question"}:
        return (
            "conditional",
            "The research route is relevant and no hard eligibility failure is established, but one high-value inquiry must resolve funding or a bounded eligibility question before an application decision.",
            structure_gate, eligibility, "resolvable_inquiry", "pass",
            "Outreach Before Decision",
        )
    return (
        "monitor",
        "The route remains plausible, but more than one material eligibility, structure, or funding question is unresolved.",
        structure_gate, eligibility, "unverified", "pass", "Monitor — Not Faculty-Review Ready",
    )


def build_program_verification(repo_root: Path) -> dict[str, object]:
    candidate_path = repo_root / "data/processed/pass2/candidate_program_funnel.csv"
    candidates = read_csv(candidate_path)
    deep_rows: list[dict[str, str]] = []
    regional_rows: list[dict[str, str]] = []
    deep_sources: list[tuple[dict[str, str], str]] = []
    regional_sources: list[tuple[dict[str, str], str]] = []
    for region in REGIONS:
        deep_path = repo_root / f"data/processed/deep_review/{region}/deep_programs.csv"
        deep_source_path = repo_root / f"data/processed/deep_review/{region}/sources.csv"
        regional_path = repo_root / f"data/processed/regions/{region}/program_screening.csv"
        regional_source_path = repo_root / f"data/processed/regions/{region}/source_ledger.csv"
        deep_rows.extend(read_csv(deep_path))
        regional_rows.extend(read_csv(regional_path))
        deep_sources.extend((row, _path(repo_root, deep_source_path)) for row in read_csv(deep_source_path))
        regional_sources.extend((row, _path(repo_root, regional_source_path)) for row in read_csv(regional_source_path))

    deep_by_id = {row["program_id"]: row for row in deep_rows}
    regional_by_id = {row["program_id"]: row for row in regional_rows}
    deep_sources_by_program: dict[str, list[tuple[dict[str, str], str]]] = defaultdict(list)
    deep_funding_by_institution: dict[str, list[tuple[dict[str, str], str]]] = defaultdict(list)
    regional_sources_by_program: dict[str, list[tuple[dict[str, str], str]]] = defaultdict(list)
    for source, path in deep_sources:
        if source.get("program_id") and _relevant_source(source):
            deep_sources_by_program[source["program_id"]].append((source, path))
        if "funding" in _source_categories_for(source) and _is_official(source):
            deep_funding_by_institution[source.get("institution_id", "")].append((source, path))
    for source, path in regional_sources:
        if source.get("program_id") and _relevant_source(source):
            regional_sources_by_program[source["program_id"]].append((source, path))

    duplicate_programs = _dominant_deep_programs(candidates, deep_by_id)
    verification_rows: list[dict[str, str]] = []
    source_rows: list[dict[str, str]] = []
    exclusion_rows: list[dict[str, str]] = []
    verified_at = date.today().isoformat()

    for candidate in candidates:
        candidate_id = candidate["program_id"]
        deep = deep_by_id.get(candidate_id)
        regional = regional_by_id.get(candidate_id)
        record = deep or regional or candidate
        raw_sources = list(deep_sources_by_program.get(candidate_id, []))
        if not raw_sources:
            raw_sources = list(regional_sources_by_program.get(candidate_id, []))
        if deep and not _material_funding_supported([source for source, _ in raw_sources]):
            raw_sources.extend(deep_funding_by_institution.get(candidate["institution_id"], []))

        linked: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for source, path in raw_sources:
            key = (canonical_url(source.get("url", "")), source.get("exact_claim_supported", ""))
            if key in seen:
                continue
            seen.add(key)
            linked.append(_source_row(candidate, source, path))
        if not linked:
            linked.append(_derived_source(candidate, _path(repo_root, candidate_path)))
        source_rows.extend(linked)

        program_ids = [row["stage3_source_id"] for row in linked if "program" in _split(row["claim_categories"])]
        admissions_ids = [
            row["stage3_source_id"]
            for row in linked
            if set(_split(row["claim_categories"])) & {"admissions", "eligibility", "language", "deadline", "fees"}
        ]
        funding_ids = [
            row["stage3_source_id"]
            for row in linked
            if "funding" in _split(row["claim_categories"])
            and row["official_or_secondary"].casefold().startswith("official")
        ]
        has_funding_source = bool(funding_ids)
        status, reason, structure_gate, eligibility_gate, funding_gate, dominance_gate, positioning = _status_for(
            candidate, record, bool(deep), has_funding_source, candidate_id in duplicate_programs
        )

        if deep and not has_funding_source:
            funding_model = "Unverified in Stage 3; no independent funding source in frozen evidence"
            funding_status = "No independently sourced material funding claim retained"
            funding_duration = UNKNOWN
            funding_conditions = UNKNOWN
            stipend_amount = UNKNOWN
            stipend_currency = UNKNOWN
            tuition_coverage = UNKNOWN
            mandatory_fee_coverage = UNKNOWN
            health_coverage = UNKNOWN
            summer_coverage = UNKNOWN
            scholarships = UNKNOWN
        else:
            funding_model = _text(record.get("funding_model"))
            funding_status = _text(record.get("funding_status"))
            funding_duration = _text(record.get("funding_duration_years"))
            funding_conditions = _text(record.get("funding_conditions"))
            stipend_amount = _text(record.get("stipend_amount"))
            stipend_currency = _text(record.get("stipend_currency"))
            tuition_coverage = _text(record.get("tuition_coverage"))
            mandatory_fee_coverage = _text(record.get("mandatory_fee_coverage"))
            health_coverage = _text(record.get("health_insurance_coverage"))
            summer_coverage = _text(record.get("summer_funding"))
            scholarships = _text(record.get("scholarships_fellowships"))

        source_paths = _join(
            _split(candidate.get("source_record_paths", ""))
            + [row["source_path"] for row in linked]
        )
        verification = {
            "schema_version": PASS2_SCHEMA_VERSION,
            "candidate_program_id": candidate_id,
            "verified_program_id": record.get("program_id", candidate_id),
            "institution_id": candidate["institution_id"],
            "institution_name": candidate["institution_name"],
            "country": candidate["country"],
            "region": candidate["region"],
            "candidate_funnel_status": candidate["funnel_status"],
            "verification_status": status,
            "status_reason": reason,
            "exact_degree_program_name": _text(record.get("program_name", candidate.get("program_name"))),
            "degree_type": _text(record.get("degree_type", candidate.get("degree_type"))),
            "research_requirement": _text(
                record.get("thesis_dissertation_requirement")
                or record.get("research_credit_requirement")
            ),
            "department": _text(record.get("department")),
            "current_program_status": _text(record.get("current_program_status")),
            "bachelors_entry_eligibility": _text(record.get("direct_from_bachelors_eligible")),
            "international_student_eligibility": _text(record.get("international_student_eligible")),
            "language_of_instruction": _text(record.get("language_of_instruction")),
            "english_requirement_and_waiver": _text(record.get("english_requirement_waiver")),
            "minimum_gpa": _text(record.get("minimum_gpa")),
            "minimum_gpa_application": _text(record.get("minimum_gpa_policy")),
            "prerequisite_coursework": _text(record.get("prerequisite_coursework")),
            "admissions_model": _text(record.get("admissions_model") or candidate.get("regional_admissions_model")),
            "faculty_contact_expectation": _text(record.get("faculty_contact_expectation")),
            "fall_2027_deadline": _text(record.get("fall_2027_deadline")),
            "deadline_cycle_label": _text(record.get("deadline_cycle_status")),
            "application_fee": _text(record.get("application_fee")),
            "fee_currency": _text(record.get("fee_currency")),
            "fee_waiver_rules": _text(record.get("fee_waiver_rules")),
            "simultaneous_application_rules": _text(record.get("multiple_applications_allowed")),
            "separate_fees_required": _text(record.get("separate_fees_required")),
            "tuition": "Not separately published or verified in frozen evidence",
            "mandatory_fees": _text(record.get("mandatory_fee_coverage")),
            "funding_model": funding_model,
            "funding_status": funding_status,
            "funding_duration": funding_duration,
            "funding_conditions": funding_conditions,
            "funding_international_eligibility": (
                "International eligibility follows the cited funding terms; offer-specific coverage must be confirmed"
                if has_funding_source
                else UNKNOWN
            ),
            "stipend_amount": stipend_amount,
            "stipend_currency": stipend_currency,
            "tuition_coverage": tuition_coverage,
            "mandatory_fee_coverage": mandatory_fee_coverage,
            "health_insurance_coverage": health_coverage,
            "summer_coverage": summer_coverage,
            "named_scholarships": scholarships,
            "scholarship_deadlines": "Not separately published or verified in frozen evidence",
            "largest_unresolved_question": _text(
                record.get("unresolved_question")
                or candidate.get("unresolved_fields")
                or "No material unresolved question recorded"
            ),
            "relevant_route_gate": (
                "pass" if deep and record.get("degree_type") in RESEARCH_DEGREE_TYPES
                else "preliminary" if record.get("degree_type", candidate.get("degree_type")) in RESEARCH_DEGREE_TYPES
                else "unverified"
            ),
            "eligibility_gate": eligibility_gate,
            "funding_gate": funding_gate,
            "degree_structure_gate": structure_gate,
            "same_university_dominance_gate": dominance_gate,
            "faculty_review_ready": "yes" if status in {"retained", "conditional"} else "no",
            "application_positioning": positioning,
            "official_program_url": record.get("official_program_url") or candidate.get("official_program_url") or UNKNOWN,
            "program_source_ids": _join(program_ids) or linked[0]["stage3_source_id"],
            "admissions_source_ids": _join(admissions_ids),
            "funding_source_ids": _join(funding_ids),
            "evidence_confidence": (
                "high" if deep and program_ids else candidate.get("evidence_confidence", "low")
            ),
            "source_record_paths": source_paths,
            "verified_at": verified_at,
        }
        verification_rows.append(verification)
        if status == "excluded":
            exclusion_rows.append(
                {
                    "schema_version": PASS2_SCHEMA_VERSION,
                    "candidate_program_id": candidate_id,
                    "institution_id": candidate["institution_id"],
                    "institution_name": candidate["institution_name"],
                    "country": candidate["country"],
                    "region": candidate["region"],
                    "program_name": verification["exact_degree_program_name"],
                    "degree_type": verification["degree_type"],
                    "exclusion_category": (
                        "stage2_screened_out" if candidate["funnel_status"] == "screened_out"
                        else "duplicate_same_university_route" if candidate_id in duplicate_programs
                        else "verified_eligibility_or_route_failure"
                    ),
                    "evidence_backed_reason": reason,
                    "largest_unresolved_question": verification["largest_unresolved_question"],
                    "source_ids": verification["program_source_ids"],
                    "source_urls": _join(row["url"] for row in linked),
                    "source_record_paths": source_paths,
                    "excluded_at": verified_at,
                }
            )

    source_rows.sort(key=lambda row: (row["candidate_program_id"], row["stage3_source_id"]))
    write_csv(
        repo_root / "data/processed/pass2/program_verification.csv",
        verification_rows,
        PROGRAM_VERIFICATION_COLUMNS_V2,
    )
    write_csv(
        repo_root / "data/processed/pass2/program_sources.csv",
        source_rows,
        PROGRAM_SOURCE_COLUMNS_V2,
    )
    write_csv(
        repo_root / "data/processed/pass2/program_exclusions.csv",
        exclusion_rows,
        PROGRAM_EXCLUSION_COLUMNS_V2,
    )

    source_ids = {row["stage3_source_id"] for row in source_rows}
    status_counts = defaultdict(int)
    for row in verification_rows:
        status_counts[row["verification_status"]] += 1
    assertions = {
        "one_status_per_candidate": len(verification_rows) == len(candidates)
        and {row["candidate_program_id"] for row in verification_rows}
        == {row["program_id"] for row in candidates},
        "controlled_statuses_only": {row["verification_status"] for row in verification_rows}
        <= FINAL_STATUSES,
        "all_material_fields_explicit": all(
            all(
                str(row[column]).strip()
                for column in PROGRAM_VERIFICATION_COLUMNS_V2
                if column not in {"admissions_source_ids", "funding_source_ids"}
            )
            for row in verification_rows
        ),
        "all_rows_have_resolvable_sources": all(
            set(_split(row["program_source_ids"])) <= source_ids
            and bool(_split(row["program_source_ids"]))
            for row in verification_rows
        ),
        "material_funding_claims_have_independent_source": all(
            bool(_split(row["funding_source_ids"]))
            for row in verification_rows
            if _has_material_funding_claim(row)
        ),
        "conditional_funding_is_outreach_only": all(
            row["application_positioning"] == "Outreach Before Decision"
            for row in verification_rows
            if row["verification_status"] == "conditional"
        ),
        "faculty_review_gate_enforced": all(
            (row["faculty_review_ready"] == "yes")
            == (row["verification_status"] in {"retained", "conditional"})
            for row in verification_rows
        ),
        "exclusions_match_status": {row["candidate_program_id"] for row in exclusion_rows}
        == {
            row["candidate_program_id"]
            for row in verification_rows
            if row["verification_status"] == "excluded"
        },
        "no_score_or_recommendation_fields": not any(
            re.search(r"score|rank|recommendation", column, re.I)
            for column in PROGRAM_VERIFICATION_COLUMNS_V2
        ),
        "all_regions_represented": {row["region"] for row in verification_rows} == set(REGIONS),
        "retained_or_conditional_have_exact_official_route": all(
            row["official_program_url"] != UNKNOWN
            and row["degree_structure_gate"] == "pass"
            for row in verification_rows
            if row["verification_status"] in {"retained", "conditional"}
        ),
    }
    return {
        "verification_rows": verification_rows,
        "source_rows": source_rows,
        "exclusion_rows": exclusion_rows,
        "counts": {
            "candidate_rows": len(candidates),
            "verification_rows": len(verification_rows),
            "source_rows": len(source_rows),
            "exclusion_rows": len(exclusion_rows),
            **dict(status_counts),
            "faculty_review_ready": sum(row["faculty_review_ready"] == "yes" for row in verification_rows),
            "official_program_url_present": sum(row["official_program_url"] != UNKNOWN for row in verification_rows),
            "funding_source_linked": sum(bool(row["funding_source_ids"]) for row in verification_rows),
        },
        "assertions": assertions,
        "validation_status": "PASS" if all(assertions.values()) else "FAIL",
    }
