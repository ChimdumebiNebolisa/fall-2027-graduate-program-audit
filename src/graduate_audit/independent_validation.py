from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


CORE_CLAIM_FIELDS = {
    "program": "exact_degree_program_name",
    "funding": "funding_model",
    "eligibility": "bachelors_entry_eligibility",
    "deadline": "fall_2027_deadline",
}


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "yes", "1"}


def _source_ids(value: object) -> list[str]:
    return [item for item in str(value or "").split("|") if item]


def recalculate_scores(
    program_scores: Sequence[Mapping[str, object]],
    score_evidence: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Independently sum the six component rows and compare with recorded totals."""
    evidence_by_program: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in score_evidence:
        evidence_by_program[str(row["program_id"])].append(row)

    results: list[dict[str, object]] = []
    for score in program_scores:
        program_id = str(score["program_id"])
        evidence_rows = evidence_by_program.get(program_id, [])
        components = {str(row["component"]): int(row["component_score"]) for row in evidence_rows}
        independent_total = sum(components.values())
        recorded_total = int(score["overall_score"])
        results.append(
            {
                "program_id": program_id,
                "institution_name": score["institution_name"],
                "component_count": len(components),
                "recorded_total": recorded_total,
                "independent_total": independent_total,
                "difference": independent_total - recorded_total,
                "status": "pass" if len(components) == 6 and independent_total == recorded_total else "fail",
            }
        )
    return results


def verify_distinct_professor_counts(
    program_scores: Sequence[Mapping[str, object]],
    professor_matches: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Recount distinct verified strong professors without trusting the score output."""
    professors: dict[str, set[str]] = defaultdict(set)
    for row in professor_matches:
        if (
            str(row.get("verification_status", "")).lower().startswith("verified")
            and str(row.get("fit_strength", "")).lower() == "strong"
        ):
            professors[str(row["program_id"])].add(str(row["professor_id"]))

    results: list[dict[str, object]] = []
    for score in program_scores:
        program_id = str(score["program_id"])
        recorded = int(score["distinct_verified_strong_matches"])
        independent = len(professors.get(program_id, set()))
        results.append(
            {
                "program_id": program_id,
                "institution_name": score["institution_name"],
                "recorded_distinct_professors": recorded,
                "independent_distinct_professors": independent,
                "difference": independent - recorded,
                "status": "pass" if independent == recorded else "fail",
            }
        )
    return results


def cycle_label_is_safe(deadline: object, cycle_label: object) -> bool:
    """Require explicit labeling or an explicit caveat for every deadline claim."""
    deadline_text = str(deadline or "").lower()
    label = str(cycle_label or "").lower()
    if "not verified" in deadline_text or "not yet published" in deadline_text:
        return any(token in label for token in ("not", "latest", "current", "requires", "confirm"))
    explicit = "fall 2027" in label or "2027 graduate" in label
    caveated = any(
        token in label
        for token in ("recurring", "inferred", "not explicitly", "not separately", "specific calendar", "conflict", "confirm")
    )
    return explicit or caveated


def build_core_claim_rechecks(
    core_programs: Sequence[Mapping[str, object]],
    verification_rows: Sequence[Mapping[str, object]],
    program_sources: Sequence[Mapping[str, object]],
    professor_matches: Sequence[Mapping[str, object]],
    professor_sources: Sequence[Mapping[str, object]],
    live_rechecks: Mapping[str, Mapping[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Build a five-domain audit row set for every core program."""
    live_rechecks = live_rechecks or {}
    verification_by_id = {str(row["verified_program_id"]): row for row in verification_rows}
    program_source_by_id = {str(row["stage3_source_id"]): row for row in program_sources}
    program_sources_by_id: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for source in program_sources:
        if str(source.get("official_or_secondary", "")).lower() == "official":
            program_sources_by_id[str(source["candidate_program_id"])].append(source)
    professor_sources_by_id = {str(row["stage4_source_id"]): row for row in professor_sources}
    professors_by_program: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for professor in professor_matches:
        if str(professor.get("verification_status", "")).lower().startswith("verified"):
            professors_by_program[str(professor["program_id"])].append(professor)

    results: list[dict[str, object]] = []
    for core in core_programs:
        program_id = str(core["program_id"])
        verification = verification_by_id[program_id]
        for domain in ("program", "faculty", "funding", "eligibility", "deadline"):
            if domain == "faculty":
                selected: list[Mapping[str, object]] = []
                for professor in professors_by_program.get(program_id, []):
                    for source_id in _source_ids(professor.get("source_ids", "")):
                        source = professor_sources_by_id.get(source_id)
                        if source and str(source.get("official_or_secondary", "")).lower() == "official":
                            selected.append(source)
                claim = "; ".join(
                    sorted({str(row["full_name"]) for row in professors_by_program.get(program_id, [])})
                ) or "No verified strong professor"
                id_key, url_key = "stage4_source_id", "url"
            else:
                field = "funding_source_ids" if domain == "funding" else "program_source_ids" if domain == "program" else "admissions_source_ids"
                linked = [program_source_by_id[source_id] for source_id in _source_ids(verification.get(field, "")) if source_id in program_source_by_id]
                selected = [source for source in linked if domain in str(source.get("claim_categories", "")).lower().split("|")]
                if not selected:
                    selected = linked
                if not selected:
                    selected = [
                        source
                        for source in program_sources_by_id.get(program_id, [])
                        if domain in str(source.get("claim_categories", "")).lower().split("|")
                    ]
                claim = str(verification[CORE_CLAIM_FIELDS[domain]])
                id_key, url_key = "stage3_source_id", "url"

            # Do not treat duplicate URLs as independent sources.
            unique_sources: list[Mapping[str, object]] = []
            seen_urls: set[str] = set()
            for source in selected:
                url = str(source.get(url_key, ""))
                if url and url not in seen_urls:
                    unique_sources.append(source)
                    seen_urls.add(url)

            primary = unique_sources[0] if unique_sources else {}
            secondary = unique_sources[1] if len(unique_sources) > 1 else {}
            primary_url = str(primary.get(url_key, ""))
            live = live_rechecks.get(primary_url, {})
            live_status = str(live.get("status", "not_checked"))
            source_count = len(unique_sources)
            evidence_status = (
                "verified_two_source"
                if source_count >= 2
                else "verified_single_source"
                if source_count == 1
                else "missing_source"
            )
            if domain == "deadline" and not cycle_label_is_safe(
                verification["fall_2027_deadline"], verification["deadline_cycle_label"]
            ):
                evidence_status = "unsafe_cycle_label"
            results.append(
                {
                    "schema_version": "2.0",
                    "program_id": program_id,
                    "institution_name": core["institution_name"],
                    "domain": domain,
                    "recorded_claim": claim,
                    "primary_source_id": primary.get(id_key, ""),
                    "primary_url": primary_url,
                    "secondary_source_id": secondary.get(id_key, ""),
                    "secondary_url": secondary.get(url_key, ""),
                    "authoritative_source_count": source_count,
                    "second_source_status": "present" if source_count >= 2 else "not_in_ledger",
                    "live_access_status": live_status,
                    "cycle_label": verification["deadline_cycle_label"] if domain == "deadline" else "not_applicable",
                    "evidence_status": evidence_status,
                    "unresolved_question": verification["largest_unresolved_question"],
                }
            )
    return results


def build_recruiting_rechecks(
    professor_matches: Sequence[Mapping[str, object]],
    professor_sources: Sequence[Mapping[str, object]],
    live_rechecks: Mapping[str, Mapping[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Re-express every confirmed claim with its exact degree scope and live status."""
    live_rechecks = live_rechecks or {}
    source_by_id = {str(row["stage4_source_id"]): row for row in professor_sources}
    rows: list[dict[str, object]] = []
    for professor in professor_matches:
        if str(professor.get("recruiting_status")) != "Confirmed recruiting":
            continue
        candidates = [
            source_by_id[source_id]
            for source_id in _source_ids(professor.get("source_ids", ""))
            if source_id in source_by_id
            and any(
                token in str(source_by_id[source_id].get("claim_categories", "")).lower()
                for token in ("recruit", "prospective", "position", "hiring")
            )
        ]
        primary = candidates[0] if candidates else {}
        url = str(primary.get("url", "")) or str(professor.get("official_faculty_or_lab_url", ""))
        live = live_rechecks.get(url, {})
        program_name = str(professor["program_name"])
        degree_scope = "master_only" if "master" in str(professor["recruiting_evidence"]).lower() and "phd" not in str(professor["recruiting_evidence"]).lower() else "program_specific"
        rows.append(
            {
                "schema_version": "2.0",
                "professor_id": professor["professor_id"],
                "professor_name": professor["full_name"],
                "institution_name": professor["institution_name"],
                "program_id": professor["program_id"],
                "program_name": program_name,
                "degree_scope": degree_scope,
                "recorded_recruiting_evidence": professor["recruiting_evidence"],
                "source_id": primary.get("stage4_source_id", ""),
                "source_url": url,
                "live_access_status": live.get("status", "not_checked"),
                "recheck_status": "confirmed_with_exact_scope" if url else "missing_source",
                "unresolved_question": professor["unresolved_question"],
            }
        )
    return rows


def portfolio_economics(core: Sequence[Mapping[str, object]], reserve: Sequence[Mapping[str, object]]) -> dict[str, object]:
    active = list(core) + list(reserve)
    numeric_fees: dict[str, float] = defaultdict(float)
    known_fee_count = 0
    unknown_fee_count = 0
    for program in active:
        try:
            amount = float(program["application_fee"])
            numeric_fees[str(program.get("fee_currency", "Unknown"))] += amount
            known_fee_count += 1
        except (TypeError, ValueError):
            unknown_fee_count += 1
    return {
        "active_programs": len(active),
        "core_programs": len(core),
        "reserve_programs": len(reserve),
        "unique_institutions": len({str(row["institution_id"]) for row in active}),
        "degree_types": dict(Counter(str(row["degree_type"]) for row in active)),
        "regions": dict(Counter(str(row["region"]) for row in active)),
        "known_fee_programs": known_fee_count,
        "unknown_or_non_numeric_fee_programs": unknown_fee_count,
        "known_fee_totals_by_currency": dict(numeric_fees),
        "single_program_per_university": len({str(row["institution_id"]) for row in active}) == len(active),
        "all_hard_gates_pass": all(_truthy(row.get("all_hard_gates_pass")) for row in active),
    }
