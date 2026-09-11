from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable

from .candidate_funnel import DISCOVERY_PATHS, REGIONAL_ADMISSIONS_MODELS, split_values
from .io import read_csv, write_csv
from .schema import (
    CANDIDATE_FUNNEL_COLUMNS_V2,
    DISCOVERY_SOURCE_YIELD_COLUMNS_V2,
    EXCLUSION_SAMPLE_AUDIT_COLUMNS_V2,
    PASS2_SCHEMA_VERSION,
    program_id,
)


REENTRY_SOURCE_COLUMNS = (
    "schema_version",
    "source_id",
    "institution_id",
    "program_name",
    "discovery_path",
    "evidence_role",
    "title",
    "publisher",
    "url",
    "accessed_date",
    "evidence_summary",
    "limitations",
)

REENTRY_CANDIDATE_COLUMNS = (
    *CANDIDATE_FUNNEL_COLUMNS_V2,
    "source_ids",
    "reentry_id",
)


def _pipe(values: Iterable[str]) -> str:
    return "|".join(dict.fromkeys(value.strip() for value in values if value.strip()))


def build_reentry_rows(
    definitions: list[dict[str, object]],
    institutions: dict[str, dict[str, str]],
    reentry_path: str,
    reentry_id: str = "stage_02_reentry_01",
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    candidates: list[dict[str, str]] = []
    sources: list[dict[str, str]] = []
    seen_sources: set[str] = set()
    for definition in definitions:
        institution_id = str(definition["institution_id"])
        if institution_id not in institutions:
            raise ValueError(f"Unknown institution_id in re-entry: {institution_id}")
        institution = institutions[institution_id]
        expected_name = institution.get("institution_name", "")
        supplied_name = str(definition["institution_name"])
        if supplied_name != expected_name:
            raise ValueError(
                f"Institution-name mismatch for {institution_id}: "
                f"{supplied_name!r} != {expected_name!r}"
            )
        region = str(definition["region"])
        degree_type = str(definition["degree_type"])
        name = str(definition["program_name"])
        source_rows = definition.get("sources", [])
        if not isinstance(source_rows, list) or len(source_rows) < 2:
            raise ValueError(f"At least two official sources required for {institution_id}")
        source_ids: list[str] = []
        for source in source_rows:
            if not isinstance(source, dict):
                raise ValueError(f"Invalid source record for {institution_id}")
            source_id = str(source["source_id"])
            if source_id in seen_sources:
                raise ValueError(f"Duplicate re-entry source_id: {source_id}")
            seen_sources.add(source_id)
            source_ids.append(source_id)
            source_path = str(source["discovery_path"])
            if source_path not in DISCOVERY_PATHS:
                raise ValueError(f"Unknown discovery path {source_path!r}")
            sources.append(
                {
                    "schema_version": PASS2_SCHEMA_VERSION,
                    "source_id": source_id,
                    "institution_id": institution_id,
                    "program_name": name,
                    "discovery_path": source_path,
                    "evidence_role": str(source["evidence_role"]),
                    "title": str(source["title"]),
                    "publisher": supplied_name,
                    "url": str(source["url"]),
                    "accessed_date": str(source.get("accessed_date", "2026-09-10")),
                    "evidence_summary": str(source["evidence_summary"]),
                    "limitations": str(source.get("limitations", "Stage 3 verification required")),
                }
            )
        paths = [str(source["discovery_path"]) for source in source_rows]
        paths.extend(str(value) for value in definition.get("additional_discovery_paths", []))
        candidates.append(
            {
                "schema_version": PASS2_SCHEMA_VERSION,
                "program_id": program_id(institution_id, degree_type, name),
                "institution_id": institution_id,
                "institution_name": supplied_name,
                "country": str(definition["country"]),
                "region": region,
                "regional_admissions_model": REGIONAL_ADMISSIONS_MODELS[region],
                "program_name": name,
                "degree_type": degree_type,
                "relevant_degree_route": str(definition["relevant_degree_route"]),
                "discovery_paths": _pipe(paths),
                "research_topic_clusters": _pipe(
                    str(value) for value in definition["research_topic_clusters"]
                ),
                "exact_research_fit_signal": str(definition["exact_research_fit_signal"]),
                "preliminary_international_eligibility": str(
                    definition["preliminary_international_eligibility"]
                ),
                "preliminary_funding_signal": str(definition["preliminary_funding_signal"]),
                "official_program_url": str(definition["official_program_url"]),
                "official_institution_url": str(
                    definition.get("official_institution_url", "")
                )
                or institution.get("official_website", ""),
                "evidence_confidence": str(definition.get("evidence_confidence", "medium")),
                "affiliation_normalization_status": "canonical institution registry match",
                "seed_adjacency": _pipe(str(value) for value in definition["seed_adjacency"]),
                "funnel_status": "advance_to_stage_3",
                "proposed_next_action": (
                    "verify current program, applicant eligibility, funding, faculty fit, and Fall 2027 cycle"
                ),
                "exclusion_reason": "",
                "unresolved_fields": _pipe(str(value) for value in definition["unresolved_fields"]),
                "source_record_paths": reentry_path,
                "source_ids": _pipe(source_ids),
                "reentry_id": reentry_id,
            }
        )
    if len({row["program_id"] for row in candidates}) != len(candidates):
        raise ValueError("Duplicate program_id in Stage 2 re-entry definitions")
    return candidates, sources


def merge_candidate_rows(
    baseline: list[dict[str, str]], additions: list[dict[str, str]]
) -> list[dict[str, str]]:
    addition_ids = {row["program_id"] for row in additions}
    merged = [row for row in baseline if row["program_id"] not in addition_ids]
    merged.extend(
        {column: row.get(column, "") for column in CANDIDATE_FUNNEL_COLUMNS_V2}
        for row in additions
    )
    return merged


def augment_source_yield(
    baseline: list[dict[str, str]],
    additions: list[dict[str, str]],
    sources: list[dict[str, str]],
    reentry_label: str = "01",
) -> list[dict[str, str]]:
    candidate_counts = Counter()
    for candidate in additions:
        candidate_counts.update(split_values(candidate["discovery_paths"]))
    source_counts = Counter(source["discovery_path"] for source in sources)
    rows: list[dict[str, str]] = []
    by_path = {row["discovery_path"]: row for row in baseline}
    for path in DISCOVERY_PATHS:
        row = dict(by_path[path])
        contribution = candidate_counts[path]
        row["source_records_examined"] = str(int(row["source_records_examined"]) + source_counts[path])
        row["candidate_rows_contributed"] = str(int(row["candidate_rows_contributed"]) + contribution)
        row["candidate_rows_introduced"] = str(int(row["candidate_rows_introduced"]) + contribution)
        row["advanced_to_stage_3"] = str(int(row["advanced_to_stage_3"]) + contribution)
        contributed = int(row["candidate_rows_contributed"])
        active = int(row["advanced_to_stage_3"]) + int(row["catalog_or_manual_review"])
        row["yield_rate"] = f"{active / contributed:.3f}" if contributed else "0.000"
        row["notes"] = (
            row["notes"].rstrip(". ")
            + f". Stage 2 re-entry {reentry_label} contributed {contribution} exact route(s) "
            f"from {source_counts[path]} official source record(s)."
        )
        rows.append(row)
    return rows


def augment_exclusion_audit(
    baseline: list[dict[str, str]],
    additions: list[dict[str, str]],
    reentry_prefix: str = "reentry01",
    audit_targets: dict[str, tuple[str, str]] | None = None,
) -> list[dict[str, str]]:
    targets = audit_targets or {
        "ca:dli:O18781994282": (
            "official_inventory_no_research_computing_route",
            "The original mechanical screen noted a relevant seed but failed to retain an exact official program page.",
        ),
        "ror:040wg7k59": (
            "outside_bounded_positive_seed_screen",
            "The original bounded screen left the exact route unresolved despite a current official research-master page.",
        ),
    }
    clean = [row for row in baseline if not row["sample_id"].startswith(f"{reentry_prefix}:")]
    by_institution = {row["institution_id"]: row for row in additions}
    for institution_id, (category, rationale) in targets.items():
        candidate = by_institution[institution_id]
        clean.append(
            {
                "schema_version": PASS2_SCHEMA_VERSION,
                "sample_id": f"{reentry_prefix}:{institution_id}",
                "region": candidate["region"],
                "institution_id": institution_id,
                "institution_name": candidate["institution_name"],
                "country": candidate["country"],
                "exclusion_reason_category": category,
                "original_exclusion_reason": "Exact route absent from the original Stage 2 funnel",
                "original_supporting_evidence": rationale,
                "original_source_url": candidate["official_institution_url"],
                "independent_discovery_paths": candidate["discovery_paths"],
                "independent_research_signal": candidate["exact_research_fit_signal"],
                "audit_result": "false_negative_corrected",
                "false_negative_risk": "confirmed",
                "audit_rationale": (
                    "Official program and research evidence now establishes a plausible exact route; "
                    "the candidate was added for Stage 3 verification."
                ),
                "funnel_program_id": candidate["program_id"],
                "sample_status": "complete",
                "audit_date": "2026-09-10",
            }
        )
    return clean


def write_reentry_outputs(
    output_dir: Path,
    candidates: list[dict[str, str]],
    sources: list[dict[str, str]],
    filename_suffix: str = "",
) -> None:
    write_csv(
        output_dir / f"stage_02_reentry{filename_suffix}_candidates.csv",
        candidates,
        REENTRY_CANDIDATE_COLUMNS,
    )
    write_csv(
        output_dir / f"stage_02_reentry{filename_suffix}_sources.csv",
        sources,
        REENTRY_SOURCE_COLUMNS,
    )


def validate_reentry(
    candidates: list[dict[str, str]],
    sources: list[dict[str, str]],
    merged: list[dict[str, str]],
    audits: list[dict[str, str]],
    reentry_prefix: str = "reentry01",
    prior_program_ids: set[str] | None = None,
) -> dict[str, object]:
    merged_by_id = {row["program_id"]: row for row in merged}
    source_ids = {row["source_id"] for row in sources}
    assertions = {
        "bounded_reentry_has_exact_routes": 10 <= len(candidates) <= 20,
        "reentry_covers_all_regions": {row["region"] for row in candidates} == {"us", "canada", "europe"},
        "research_masters_reentry_present": any(
            row["degree_type"] == "Thesis or research master's" for row in candidates
        ),
        "doctoral_reentry_present": any(row["degree_type"] == "PhD" for row in candidates),
        "all_candidates_advance_only_to_stage_3": all(
            row["funnel_status"] == "advance_to_stage_3" for row in candidates
        ),
        "all_candidates_have_exact_official_program_urls": all(
            row["official_program_url"].startswith("https://") for row in candidates
        ),
        "all_candidates_have_official_institution_urls": all(
            row["official_institution_url"].startswith("https://") for row in candidates
        ),
        "all_candidates_have_fit_and_preliminary_route_fields": all(
            row["exact_research_fit_signal"]
            and row["preliminary_international_eligibility"]
            and row["preliminary_funding_signal"]
            and row["unresolved_fields"]
            for row in candidates
        ),
        "all_candidate_source_ids_resolve": all(
            set(split_values(row["source_ids"])) <= source_ids for row in candidates
        ),
        "all_sources_are_official_https": all(
            row["url"].startswith("https://")
            and row["publisher"]
            and row["evidence_summary"]
            and row["limitations"]
            for row in sources
        ),
        "program_ids_unique_after_merge": len(merged_by_id) == len(merged),
        "all_reentry_routes_are_net_new": not (
            {row["program_id"] for row in candidates} & (prior_program_ids or set())
        ),
        "all_reentry_candidates_present_after_merge": all(
            row["program_id"] in merged_by_id for row in candidates
        ),
        "known_seed_adjacency_retained": all(row["seed_adjacency"] for row in candidates),
        "confirmed_false_negatives_reaudited": sum(
            row["audit_result"] == "false_negative_corrected"
            and row["sample_id"].startswith(f"{reentry_prefix}:")
            for row in audits
        ) >= 2,
        "no_scoring_fields_introduced": all(
            "score" not in column.casefold() for column in CANDIDATE_FUNNEL_COLUMNS_V2
        ),
    }
    return {
        "status": "PASS" if all(assertions.values()) else "FAIL",
        "assertions": assertions,
        "reentry_scope": "bounded_non_saturation_follow_up",
    }
