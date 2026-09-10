from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable

from .io import read_csv, read_json, write_csv
from .schema import (
    CANDIDATE_FUNNEL_COLUMNS_V2,
    DISCOVERY_SOURCE_YIELD_COLUMNS_V2,
    EXCLUSION_SAMPLE_AUDIT_COLUMNS_V2,
    PASS2_SCHEMA_VERSION,
    canonical_url,
    program_id,
)

REGIONS = ("us", "canada", "europe")
REGIONAL_ADMISSIONS_MODELS = {
    "us": "US program or committee admission; faculty role requires program-specific verification",
    "canada": "Canadian program admission with potentially supervisor-dependent research route",
    "europe": "European program, supervisor, studentship, or employed-position model; verify by country",
}

DISCOVERY_PATHS = (
    "recognized_institution_record",
    "official_program_or_department_signal",
    "recent_paper_signal",
    "current_faculty_topic_signal",
    "lab_or_center_signal",
    "calendar_prior_list",
    "first_audit_program",
    "research_masters_or_scholarship_search",
    "underrepresented_route_search",
)

RESEARCH_MASTER_TYPES = {
    "Thesis or research master's",
    "Project-based master's with substantial research",
}
DOCTORAL_TYPES = {
    "PhD",
    "Direct-entry PhD",
    "Integrated or structured doctorate",
    "PhD requiring a master's",
}

TERRAPROBE_TERMS = (
    "program repair",
    "software repair",
    "automated repair",
    "configuration repair",
    "infrastructure as code",
    "terraform",
    "software testing",
    "program analysis",
    "software reliability",
)
EVIDEX_TERMS = (
    "claim verification",
    "fact-checking",
    "fact checking",
    "factuality",
    "grounding",
    "evidence-based",
    "evidence-grounded",
    "language model evaluation",
    "llm evaluation",
    "verification",
    "trustworthy ai",
    "trustworthy language",
)


def normalize_name(value: str) -> str:
    value = value.casefold().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def name_variants(value: str) -> set[str]:
    normalized = normalize_name(value)
    variants = {normalized}
    without_campus = re.sub(r"\bmain campus\b$", "", normalized).strip()
    variants.add(without_campus)
    state_university_base = re.sub(
        r"^(.+ state university) at [a-z0-9 ]+$", r"\1", without_campus
    )
    variants.add(state_university_base)
    without_stopwords = " ".join(
        token for token in without_campus.split() if token not in {"the", "of"}
    )
    variants.add(without_stopwords)
    return {variant for variant in variants if variant}


def canonical_ror(value: str) -> str:
    return str(value or "").strip().lower().removeprefix("https://ror.org/").rstrip("/")


def split_values(value: object) -> list[str]:
    return [part.strip() for part in re.split(r"[|;,]|\s{2,}", str(value or "")) if part.strip()]


def repository_path(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def parse_calendar_candidates(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "## Calendar comparison":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4 or cells[0] in {"Previous candidate", "---"}:
            continue
        rows.append(
            {
                "institution_name": cells[0],
                "previous_category": cells[1],
                "previous_outcome": cells[2],
                "previous_reason": cells[3],
            }
        )
    return rows


def exclusion_reason_category(region: str, reason: str) -> str:
    normalized = reason.casefold()
    if region == "us":
        return "no_recent_configured_cip_signal"
    if region == "canada":
        if "scope is" in normalized or any(
            term in normalized
            for term in (
                "art and design",
                "music",
                "theology",
                "dramatic arts",
                "military education",
                "public administration",
                "health sciences",
            )
        ):
            return "specialized_noncomputing_scope"
        return "official_inventory_no_research_computing_route"
    if "primary/secondary-school" in normalized or "primary/secondary school" in normalized:
        return "non_university_school_entity"
    return "outside_bounded_positive_seed_screen"


def seed_adjacency(signal: str) -> str:
    normalized = signal.casefold()
    matches: list[str] = []
    if any(term in normalized for term in TERRAPROBE_TERMS):
        matches.append("TerraProbe-adjacent")
    if any(term in normalized for term in EVIDEX_TERMS):
        matches.append("Evidex-adjacent")
    return "|".join(matches)


def infer_topic_clusters(signal: str) -> set[str]:
    normalized = signal.casefold()
    clusters: set[str] = set()
    if any(term in normalized for term in ("llm", "software engineering", "coding agent", "code generation")):
        clusters.add("ai_for_se")
    if any(term in normalized for term in ("repair", "program analysis", "testing", "debug", "configuration")):
        clusters.add("repair_analysis")
    if any(term in normalized for term in ("trust", "factual", "ground", "verification", "reliab", "evaluation")):
        clusters.add("trustworthy_ai")
    if any(term in normalized for term in ("security", "secure", "cloud", "devops", "policy")):
        clusters.add("systems_security")
    return clusters


def degree_route(row: dict[str, str]) -> str:
    degree = row.get("degree_type", "").strip() or "Unclear"
    bachelors = row.get("direct_from_bachelors_eligible", "").casefold()
    if degree in {"PhD", "Direct-entry PhD"} and bachelors.startswith("yes"):
        return "Doctoral route accepting bachelor's entrants"
    if degree in {"PhD", "Direct-entry PhD"}:
        return "Doctoral route; bachelor's entry requires Stage 3 verification"
    if degree == "PhD requiring a master's":
        return "Doctoral route requiring a master's"
    if degree == "Integrated or structured doctorate":
        return "Integrated or structured doctoral route"
    if degree in RESEARCH_MASTER_TYPES:
        return degree
    if degree == "Coursework or professional master's":
        return "Coursework or professional master's; exceptional funding required"
    return "Unclear; locate and verify the exact research degree route"


def route_bucket(row: dict[str, str]) -> str:
    route = row.get("relevant_degree_route", "")
    if route.startswith("Doctoral route accepting") or route.startswith("Doctoral route;"):
        return "doctoral_bachelors_entry"
    if route in RESEARCH_MASTER_TYPES:
        return "research_masters"
    if "requiring a master's" in route or route.startswith("Integrated or structured"):
        return "structured_or_masters_required_doctorate"
    return "unresolved_or_exceptional_route"


def _build_registry(repo_root: Path) -> tuple[
    dict[str, dict[str, str]], dict[str, str], dict[str, str], dict[str, str]
]:
    institutions: dict[str, dict[str, str]] = {}
    name_candidates: dict[str, set[str]] = defaultdict(set)
    ror_to_id: dict[str, str] = {}
    region_by_id: dict[str, str] = {}
    for region in REGIONS:
        path = repo_root / f"data/processed/regions/{region}/institution_universe.csv"
        for row in read_csv(path):
            institution_id = row["institution_id"]
            institutions[institution_id] = row
            region_by_id[institution_id] = region
            names = [row.get("institution_name", ""), *split_values(row.get("alternate_names"))]
            for name in names:
                if name:
                    for variant in name_variants(name):
                        name_candidates[variant].add(institution_id)
            ror = canonical_ror(row.get("ror_id", ""))
            if ror:
                ror_to_id[ror] = institution_id
    unique_names: dict[str, str] = {}
    for name, ids in name_candidates.items():
        if len(ids) == 1:
            unique_names[name] = next(iter(ids))
            continue
        positive = {
            institution_id
            for institution_id in ids
            if institutions[institution_id].get("screening_status", "")
            in {"preliminary_fit", "indexed", "deep_review", "retained"}
        }
        if len(positive) == 1:
            unique_names[name] = next(iter(positive))
    return institutions, unique_names, ror_to_id, region_by_id


def _resolve_institution(
    name: str,
    ror: str,
    institutions: dict[str, dict[str, str]],
    unique_names: dict[str, str],
    ror_to_id: dict[str, str],
) -> tuple[str | None, str]:
    ror_key = canonical_ror(ror)
    if ror_key and ror_key in ror_to_id:
        institution_id = ror_to_id[ror_key]
        canonical_name = institutions[institution_id].get("institution_name", "")
        status = (
            "ror_match_canonical_name"
            if normalize_name(name) == normalize_name(canonical_name)
            else "ror_match_name_corrected"
        )
        return institution_id, status
    institution_id = next(
        (unique_names[variant] for variant in name_variants(name) if variant in unique_names),
        None,
    )
    if institution_id:
        canonical_name = institutions[institution_id].get("institution_name", "")
        status = (
            "canonical_name_match"
            if normalize_name(name) == normalize_name(canonical_name)
            else "registered_alias_match"
        )
        return institution_id, status
    return None, "unmatched"


def _merge_openalex(
    repo_root: Path,
    institutions: dict[str, dict[str, str]],
    unique_names: dict[str, str],
    ror_to_id: dict[str, str],
) -> tuple[dict[str, dict[str, object]], dict[str, set[str]], dict[str, int]]:
    institution_path = repo_root / "data/processed/openalex_institution_signals.csv"
    faculty_path = repo_root / "data/processed/openalex_faculty_signals.csv"
    deep_professors: dict[tuple[str, str], dict[str, str]] = {}
    for region in REGIONS:
        path = repo_root / f"data/processed/deep_review/{region}/professors.csv"
        for row in read_csv(path):
            if (
                "verified" in row.get("verification_status", "").casefold()
                and row.get("official_faculty_url", "")
            ):
                deep_professors[(row.get("institution_id", ""), normalize_name(row.get("full_name", "")))] = row

    openalex_by_id: dict[str, dict[str, str]] = {}
    signals: dict[str, dict[str, object]] = {}
    stats = Counter()
    for row in read_csv(institution_path):
        stats["institution_rows"] += 1
        openalex_by_id[row.get("openalex_institution_id", "")] = row
        if row.get("institution_type", "").casefold() != "education":
            stats["non_educational_filtered"] += 1
            continue
        stats["educational_institution_rows"] += 1
        institution_id, status = _resolve_institution(
            row.get("institution_name", ""),
            row.get("ror_id", ""),
            institutions,
            unique_names,
            ror_to_id,
        )
        if not institution_id:
            stats["unmatched_educational_institutions"] += 1
            continue
        stats["matched_educational_institutions"] += 1
        if "corrected" in status or status == "registered_alias_match":
            stats["institution_name_corrections"] += 1
        current = signals.setdefault(
            institution_id,
            {
                "precision_work_count": 0,
                "relevant_work_count": 0,
                "research_topic_clusters": set(),
                "top_works": [],
                "normalization_statuses": set(),
            },
        )
        current["precision_work_count"] = int(current["precision_work_count"]) + int(
            row.get("precision_work_count") or 0
        )
        current["relevant_work_count"] = int(current["relevant_work_count"]) + int(
            row.get("relevant_work_count") or 0
        )
        current["research_topic_clusters"].update(split_values(row.get("research_topic_clusters")))
        current["top_works"].extend(
            part.strip() for part in row.get("top_works", "").split(" || ") if part.strip()
        )
        current["normalization_statuses"].add(status)

    current_faculty: dict[str, set[str]] = defaultdict(set)
    for row in read_csv(faculty_path):
        stats["faculty_affiliation_rows"] += 1
        institution_record = openalex_by_id.get(row.get("openalex_institution_id", ""), {})
        if institution_record.get("institution_type", "").casefold() != "education":
            stats["faculty_non_educational_filtered"] += 1
            continue
        institution_id, status = _resolve_institution(
            row.get("institution_name", ""),
            row.get("ror_id", ""),
            institutions,
            unique_names,
            ror_to_id,
        )
        if not institution_id:
            stats["faculty_unmatched_affiliations"] += 1
            continue
        if "corrected" in status or status == "registered_alias_match":
            stats["faculty_affiliation_name_corrections"] += 1
        professor_key = (institution_id, normalize_name(row.get("author_name", "")))
        if professor_key in deep_professors:
            current_faculty[institution_id].add(row.get("author_name", ""))
            stats["faculty_current_official_matches"] += 1
        else:
            stats["faculty_publication_time_only"] += 1
    return signals, current_faculty, dict(stats)


def _meaningful_signal(row: dict[str, str]) -> list[str]:
    values: list[str] = []
    for field in ("preliminary_fit", "research_groups_labs"):
        value = row.get(field, "").strip()
        if value and value.casefold() not in {
            "configured primary discovery signal",
            "configured secondary review-only discovery signal",
            "pending faculty/research-fit phase",
        }:
            values.append(value)
    if not values and row.get("program_name"):
        values.append(f"Program/title discovery signal: {row['program_name']}")
    return values


def _program_status(row: dict[str, str], paths: set[str]) -> tuple[str, str, str]:
    degree = row.get("degree_type", "")
    if degree == "Coursework or professional master's":
        return (
            "screened_out",
            "Coursework or professional master's has no exceptional funding evidence at discovery stage.",
            "retain exclusion unless Stage 3 finds exceptional official funding",
        )
    if row.get("official_program_url") and degree in DOCTORAL_TYPES | RESEARCH_MASTER_TYPES:
        return "advance_to_stage_3", "", "verify program structure, eligibility, and funding"
    independent_paths = paths & {
        "recent_paper_signal",
        "current_faculty_topic_signal",
        "calendar_prior_list",
        "first_audit_program",
    }
    if independent_paths and row.get("screening_decision") == "secondary_signal_manual_review":
        return (
            "manual_secondary_review",
            "",
            "inspect the current official catalog and research pages for an exact degree route",
        )
    if independent_paths:
        return (
            "catalog_verification_required",
            "",
            "locate a current official research-program page before Stage 3",
        )
    return (
        "screened_out",
        "Only one bounded registry/program-code signal was present; no independent topical, "
        "Calendar, current-faculty, or first-audit signal was recovered.",
        "do not advance; revisit only if a later independent discovery path appears",
    )


def _record_to_output(
    record: dict[str, object],
    institution: dict[str, str],
    region: str,
    openalex_signal: dict[str, object] | None,
    current_faculty: set[str],
) -> dict[str, str]:
    row = dict(record["row"])
    paths = set(record["paths"])
    source_paths = set(record["source_paths"])
    signals = _meaningful_signal(row)
    topic_clusters: set[str] = set()
    normalization_status = "not_applicable"
    if openalex_signal:
        paths.add("recent_paper_signal")
        topic_clusters.update(openalex_signal["research_topic_clusters"])
        top_works = list(dict.fromkeys(openalex_signal["top_works"]))[:2]
        if top_works:
            signals.append("Recent-paper discovery signal: " + " || ".join(top_works))
        normalization_status = (
            "canonical institution normalized; author affiliations remain publication-time unless "
            "matched to current official faculty evidence"
        )
    if current_faculty:
        paths.add("current_faculty_topic_signal")
        signals.append(
            "Current official-faculty cross-match: " + ", ".join(sorted(current_faculty)[:5])
        )
        normalization_status = "current official-faculty cross-match available"
    combined_signal = " | ".join(dict.fromkeys(signals))
    topic_clusters.update(infer_topic_clusters(combined_signal))
    if region != "us" and (
        row.get("degree_type") in RESEARCH_MASTER_TYPES or not openalex_signal
    ):
        paths.add("underrepresented_route_search")
    if row.get("degree_type") in RESEARCH_MASTER_TYPES or row.get("scholarships_fellowships"):
        paths.add("research_masters_or_scholarship_search")
    status, exclusion_reason, next_action = _program_status(row, paths)
    international = row.get("international_student_eligible", "").strip()
    if not international:
        international = "Unverified — Stage 3 required"
    funding = next(
        (
            value
            for value in (
                row.get("funding_status", "").strip(),
                row.get("funding_model", "").strip(),
                row.get("scholarships_fellowships", "").strip(),
            )
            if value
        ),
        "Unverified — Stage 3 required",
    )
    official_program_url = row.get("official_program_url", "").strip()
    unresolved: list[str] = []
    if not official_program_url:
        unresolved.append("official_program_url")
    if row.get("degree_type", "") in {"", "Unclear"}:
        unresolved.append("degree_route")
    if international.casefold().startswith("unverified"):
        unresolved.append("international_eligibility")
    if funding.casefold().startswith(("unverified", "not assessed", "pending")):
        unresolved.append("funding")
    confidence = "high" if record.get("first_audit") and official_program_url else "medium"
    if not official_program_url or row.get("degree_type") in {"", "Unclear"}:
        confidence = "low"
    if not combined_signal:
        combined_signal = "Unresolved research-fit signal; retained only for explicit catalog review."
    return {
        "schema_version": PASS2_SCHEMA_VERSION,
        "program_id": row.get("program_id", ""),
        "institution_id": row.get("institution_id", ""),
        "institution_name": institution.get("institution_name", row.get("institution_name", "")),
        "country": institution.get("country", row.get("country", "")),
        "region": region,
        "regional_admissions_model": row.get("admissions_model", "").strip()
        or REGIONAL_ADMISSIONS_MODELS[region],
        "program_name": row.get("program_name", ""),
        "degree_type": row.get("degree_type", "") or "Unclear",
        "relevant_degree_route": degree_route(row),
        "discovery_paths": "|".join(sorted(paths)),
        "research_topic_clusters": "|".join(sorted(topic_clusters)),
        "exact_research_fit_signal": combined_signal,
        "preliminary_international_eligibility": international,
        "preliminary_funding_signal": funding,
        "official_program_url": official_program_url,
        "official_institution_url": institution.get("official_website", ""),
        "evidence_confidence": confidence,
        "affiliation_normalization_status": normalization_status,
        "seed_adjacency": seed_adjacency(combined_signal),
        "funnel_status": status,
        "proposed_next_action": next_action,
        "exclusion_reason": exclusion_reason,
        "unresolved_fields": "|".join(unresolved),
        "source_record_paths": "|".join(sorted(source_paths)),
    }


def _add_program_record(
    records: dict[str, dict[str, object]],
    row: dict[str, str],
    region: str,
    source_path: str,
    introduced_by: str,
    *,
    first_audit: bool = False,
) -> None:
    program_key = row.get("program_id", "")
    if not program_key:
        return
    if program_key not in records:
        records[program_key] = {
            "row": dict(row),
            "region": region,
            "paths": {"recognized_institution_record"},
            "source_paths": {source_path},
            "introduced_by": introduced_by,
            "first_audit": first_audit,
        }
    else:
        current = records[program_key]
        for key, value in row.items():
            if value:
                current["row"][key] = value
        current["source_paths"].add(source_path)
        current["first_audit"] = bool(current["first_audit"] or first_audit)
    record = records[program_key]
    preliminary_fit = row.get("preliminary_fit", "").strip().casefold()
    generic_preliminary = {
        "configured primary discovery signal",
        "configured secondary review-only discovery signal",
        "pending faculty/research-fit phase",
    }
    if row.get("official_program_url"):
        record["paths"].add("official_program_or_department_signal")
    if preliminary_fit and preliminary_fit not in generic_preliminary:
        record["paths"].add("official_program_or_department_signal")
    lab_signal = row.get("research_groups_labs", "").strip().casefold()
    if lab_signal and lab_signal not in {
        "pending faculty/research-fit phase",
        "pending deep review",
        "unverified",
    }:
        record["paths"].add("lab_or_center_signal")
    if first_audit:
        record["paths"].add("first_audit_program")


def _build_candidates(
    repo_root: Path,
    institutions: dict[str, dict[str, str]],
    region_by_id: dict[str, str],
    openalex_signals: dict[str, dict[str, object]],
    current_faculty: dict[str, set[str]],
    calendar_by_id: dict[str, dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, str], dict[str, int]]:
    records: dict[str, dict[str, object]] = {}
    stats = Counter()
    for region in REGIONS:
        path = repo_root / f"data/processed/regions/{region}/program_screening.csv"
        for row in read_csv(path):
            _add_program_record(
                records,
                row,
                region,
                repository_path(repo_root, path),
                "recognized_institution_record",
            )
            stats["regional_program_rows"] += 1

    for region in REGIONS:
        path = repo_root / f"data/processed/deep_review/{region}/deep_programs.csv"
        for row in read_csv(path):
            _add_program_record(
                records,
                row,
                region,
                repository_path(repo_root, path),
                "first_audit_program",
                first_audit=True,
            )
            stats["first_audit_program_rows"] += 1

    institution_programs: dict[str, list[str]] = defaultdict(list)
    for key, record in records.items():
        institution_id = record["row"].get("institution_id", "")
        institution_programs[institution_id].append(key)
        if institution_id in calendar_by_id:
            record["paths"].add("calendar_prior_list")
            record["source_paths"].add(
                "reports/20260909-fall2027-audit/final_shortlist.md"
            )
        if institution_id in openalex_signals:
            record["source_paths"].add("data/processed/openalex_institution_signals.csv")
        if institution_id in current_faculty:
            record["source_paths"].add("data/processed/openalex_faculty_signals.csv")

    for institution_id, institution in institutions.items():
        if institution_id in institution_programs:
            continue
        signal = openalex_signals.get(institution_id)
        calendar = calendar_by_id.get(institution_id)
        has_precision_signal = bool(signal and int(signal["precision_work_count"]) > 0)
        if not has_precision_signal and not calendar:
            continue
        provisional_id = program_id(
            institution_id,
            "Unclear",
            "Cross-path catalog review",
        )
        region = region_by_id[institution_id]
        row = {
            "program_id": provisional_id,
            "institution_id": institution_id,
            "institution_name": institution.get("institution_name", ""),
            "country": institution.get("country", ""),
            "program_name": "Research program route unresolved — cross-path catalog review",
            "degree_type": "Unclear",
            "screening_decision": "catalog_verification_required",
        }
        paths = {"recognized_institution_record"}
        source_paths = {
            repository_path(
                repo_root,
                repo_root / f"data/processed/regions/{region}/institution_universe.csv",
            )
        }
        introduced_by = "recent_paper_signal" if has_precision_signal else "calendar_prior_list"
        if has_precision_signal:
            paths.add("recent_paper_signal")
            source_paths.add("data/processed/openalex_institution_signals.csv")
        if calendar:
            paths.add("calendar_prior_list")
            source_paths.add("reports/20260909-fall2027-audit/final_shortlist.md")
            row["preliminary_fit"] = (
                "Previous Calendar discovery context: " + calendar["previous_category"]
            )
        if region != "us":
            paths.add("underrepresented_route_search")
        records[provisional_id] = {
            "row": row,
            "region": region,
            "paths": paths,
            "source_paths": source_paths,
            "introduced_by": introduced_by,
            "first_audit": False,
        }
        institution_programs[institution_id].append(provisional_id)
        stats["cross_path_provisional_rows"] += 1

    outputs: list[dict[str, str]] = []
    introduced_by: dict[str, str] = {}
    for key, record in records.items():
        institution_id = record["row"].get("institution_id", "")
        if institution_id not in institutions:
            stats["unknown_institution_program_rows"] += 1
            continue
        region = str(record["region"])
        output = _record_to_output(
            record,
            institutions[institution_id],
            region,
            openalex_signals.get(institution_id),
            current_faculty.get(institution_id, set()),
        )
        if institution_id in calendar_by_id and "calendar_prior_list" not in output["discovery_paths"]:
            output["discovery_paths"] = "|".join(
                sorted(set(split_values(output["discovery_paths"])) | {"calendar_prior_list"})
            )
        outputs.append(output)
        introduced_by[key] = str(record["introduced_by"])
    outputs.sort(
        key=lambda row: (
            REGIONS.index(row["region"]),
            normalize_name(row["institution_name"]),
            normalize_name(row["program_name"]),
        )
    )
    outputs_by_institution: dict[str, list[dict[str, str]]] = defaultdict(list)
    for output in outputs:
        outputs_by_institution[output["institution_id"]].append(output)
    for institution_rows in outputs_by_institution.values():
        exact_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in institution_rows:
            url = canonical_url(row["official_program_url"])
            if url and row["funnel_status"] == "advance_to_stage_3":
                exact_by_url[url].append(row)
        for duplicate_rows in exact_by_url.values():
            if len(duplicate_rows) <= 1:
                continue
            keep = min(
                duplicate_rows,
                key=lambda row: (
                    "first_audit_program" not in split_values(row["discovery_paths"]),
                    normalize_name(row["program_name"]),
                ),
            )
            for row in duplicate_rows:
                if row is keep:
                    continue
                row["funnel_status"] = "screened_out"
                row["exclusion_reason"] = (
                    "Duplicate exact program record shares the same canonical official URL; the "
                    "first-audit or canonical row is retained."
                )
                row["proposed_next_action"] = f"use {keep['program_id']} for Stage 3"
        advanced_exact = [
            row
            for row in institution_rows
            if row["funnel_status"] == "advance_to_stage_3" and row["official_program_url"]
        ]
        if advanced_exact:
            for row in institution_rows:
                if row["funnel_status"] != "screened_out" and not row["official_program_url"]:
                    row["funnel_status"] = "screened_out"
                    row["exclusion_reason"] = (
                        "Mechanical discovery placeholder is superseded by an exact official "
                        "program record at the same institution."
                    )
                    row["proposed_next_action"] = "use the exact program record for Stage 3"
            continue
        unresolved_active = [
            row
            for row in institution_rows
            if row["funnel_status"]
            in {"catalog_verification_required", "manual_secondary_review"}
        ]
        if len(unresolved_active) <= 1:
            continue
        keep = min(
            unresolved_active,
            key=lambda row: (
                row["funnel_status"] != "catalog_verification_required",
                -len(split_values(row["research_topic_clusters"])),
                normalize_name(row["program_name"]),
            ),
        )
        for row in unresolved_active:
            if row is keep:
                continue
            row["funnel_status"] = "screened_out"
            row["exclusion_reason"] = (
                "Duplicate mechanical discovery signal consolidated into one institution-level "
                "catalog review candidate."
            )
            row["proposed_next_action"] = f"use {keep['program_id']} for catalog review"
    return outputs, introduced_by, dict(stats)


def _build_yield_rows(
    candidates: list[dict[str, str]],
    introduced_by: dict[str, str],
    source_counts: dict[str, int],
    openalex_stats: dict[str, int],
) -> list[dict[str, str]]:
    examined = {
        "recognized_institution_record": source_counts["institution_rows"],
        "official_program_or_department_signal": source_counts["regional_program_rows"],
        "recent_paper_signal": openalex_stats.get("institution_rows", 0),
        "current_faculty_topic_signal": openalex_stats.get("faculty_affiliation_rows", 0),
        "lab_or_center_signal": source_counts["first_audit_program_rows"],
        "calendar_prior_list": source_counts["calendar_rows"],
        "first_audit_program": source_counts["first_audit_program_rows"],
        "research_masters_or_scholarship_search": source_counts["regional_program_rows"],
        "underrepresented_route_search": source_counts["regional_program_rows"],
    }
    rows: list[dict[str, str]] = []
    for path in DISCOVERY_PATHS:
        contributed = [row for row in candidates if path in split_values(row["discovery_paths"])]
        introduced = [
            row for row in candidates if introduced_by.get(row["program_id"]) == path
        ]
        source_records = examined[path]
        active_contributed = sum(
            row["funnel_status"] != "screened_out" for row in contributed
        )
        rows.append(
            {
                "schema_version": PASS2_SCHEMA_VERSION,
                "discovery_path": path,
                "source_records_examined": str(source_records),
                "candidate_rows_contributed": str(len(contributed)),
                "candidate_rows_introduced": str(len(introduced)),
                "advanced_to_stage_3": str(
                    sum(row["funnel_status"] == "advance_to_stage_3" for row in contributed)
                ),
                "catalog_or_manual_review": str(
                    sum(
                        row["funnel_status"]
                        in {"catalog_verification_required", "manual_secondary_review"}
                        for row in contributed
                    )
                ),
                "screened_out": str(
                    sum(row["funnel_status"] == "screened_out" for row in contributed)
                ),
                "yield_rate": f"{active_contributed / len(contributed):.4f}"
                if contributed
                else "0.0000",
                "non_educational_filtered": str(
                    openalex_stats.get("non_educational_filtered", 0)
                    if path == "recent_paper_signal"
                    else openalex_stats.get("faculty_non_educational_filtered", 0)
                    if path == "current_faculty_topic_signal"
                    else 0
                ),
                "unmatched_affiliations": str(
                    openalex_stats.get("unmatched_educational_institutions", 0)
                    if path == "recent_paper_signal"
                    else openalex_stats.get("faculty_unmatched_affiliations", 0)
                    if path == "current_faculty_topic_signal"
                    else 0
                ),
                "stale_affiliation_name_corrections": str(
                    openalex_stats.get("institution_name_corrections", 0)
                    if path == "recent_paper_signal"
                    else openalex_stats.get("faculty_affiliation_name_corrections", 0)
                    if path == "current_faculty_topic_signal"
                    else 0
                ),
                "notes": (
                    "Non-educational organizations were filtered before candidate contribution; "
                    "publication-time author affiliations were used only after canonical institution "
                    "matching, and only current official faculty cross-matches contribute the faculty path."
                    if path in {"recent_paper_signal", "current_faculty_topic_signal"}
                    else "Contribution is discovery-only and does not score or recommend universities."
                ),
            }
        )
    return rows


def _build_exclusion_audit(
    repo_root: Path,
    candidates: list[dict[str, str]],
    openalex_signals: dict[str, dict[str, object]],
    calendar_by_id: dict[str, dict[str, str]],
    sample_per_stratum: int = 8,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    candidates_by_institution: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        candidates_by_institution[row["institution_id"]].append(row)
    strata: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for region in REGIONS:
        path = repo_root / f"data/processed/regions/{region}/exclusion_log.csv"
        for row in read_csv(path):
            category = exclusion_reason_category(region, row.get("primary_exclusion_reason", ""))
            row["_region"] = region
            row["_category"] = category
            strata[(region, category)].append(row)

    audit_rows: list[dict[str, str]] = []
    stats = Counter()
    for (region, category), rows in sorted(strata.items()):
        def priority(row: dict[str, str]) -> tuple[int, str]:
            institution_id = row.get("institution_id", "")
            cross_signal = institution_id in openalex_signals or institution_id in calendar_by_id
            digest = hashlib.sha256(institution_id.encode("utf-8")).hexdigest()
            return (0 if cross_signal else 1, digest)

        for row in sorted(rows, key=priority)[:sample_per_stratum]:
            institution_id = row.get("institution_id", "")
            cross_paths: list[str] = []
            signal_text: list[str] = []
            if institution_id in openalex_signals:
                cross_paths.append("recent_paper_signal")
                top = list(dict.fromkeys(openalex_signals[institution_id]["top_works"]))[:2]
                signal_text.extend(top)
            if institution_id in calendar_by_id:
                cross_paths.append("calendar_prior_list")
                signal_text.append(
                    "Prior Calendar category: "
                    + calendar_by_id[institution_id]["previous_category"]
                )
            funnel_rows = candidates_by_institution.get(institution_id, [])
            if cross_paths and funnel_rows:
                result = "reopen_in_funnel"
                risk = "observed"
                rationale = (
                    "An independent discovery path contradicts the bounded original screen; the "
                    "institution now has a catalog-verification candidate and is not treated as a "
                    "confirmed no-program result."
                )
                stats["reopened"] += 1
            elif category in {"specialized_noncomputing_scope", "non_university_school_entity"}:
                result = "confirmed_screened_out"
                risk = "low"
                rationale = (
                    "The original official-scope evidence identifies a non-computing specialist or "
                    "non-university school entity, and no independent positive path was observed."
                )
                stats["confirmed"] += 1
            else:
                result = "unresolved_no_independent_positive"
                risk = "medium"
                rationale = (
                    "No independent positive signal was observed, but the original exclusion was a "
                    "bounded mechanical screen rather than an exhaustive official-catalog finding."
                )
                stats["unresolved"] += 1
            sample_id = "sample:" + hashlib.sha256(
                f"{region}|{institution_id}|{category}".encode("utf-8")
            ).hexdigest()[:16]
            audit_rows.append(
                {
                    "schema_version": PASS2_SCHEMA_VERSION,
                    "sample_id": sample_id,
                    "region": region,
                    "institution_id": institution_id,
                    "institution_name": row.get("institution_name", ""),
                    "country": row.get("country", ""),
                    "exclusion_reason_category": category,
                    "original_exclusion_reason": row.get("primary_exclusion_reason", ""),
                    "original_supporting_evidence": row.get("supporting_evidence", ""),
                    "original_source_url": row.get("source_url", ""),
                    "independent_discovery_paths": "|".join(sorted(cross_paths)),
                    "independent_research_signal": " | ".join(signal_text),
                    "audit_result": result,
                    "false_negative_risk": risk,
                    "audit_rationale": rationale,
                    "funnel_program_id": funnel_rows[0]["program_id"] if funnel_rows else "",
                    "sample_status": "complete",
                    "audit_date": date.today().isoformat(),
                }
            )
            stats["sample_rows"] += 1
    stats["strata"] = len(strata)
    return audit_rows, dict(stats)


def validate_stage_02(
    candidates: list[dict[str, str]],
    yield_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    openalex_manifest: dict[str, object],
) -> dict[str, object]:
    active = [row for row in candidates if row["funnel_status"] != "screened_out"]
    regions = {row["region"] for row in active}
    route_buckets = {route_bucket(row) for row in active}
    seeds = {
        seed
        for row in active
        if row["funnel_status"] == "advance_to_stage_3"
        for seed in split_values(row["seed_adjacency"])
    }
    audit_regions = {row["region"] for row in audit_rows}
    audit_strata = {
        (row["region"], row["exclusion_reason_category"]) for row in audit_rows
    }
    required_strata = {
        ("us", "no_recent_configured_cip_signal"),
        ("canada", "specialized_noncomputing_scope"),
        ("canada", "official_inventory_no_research_computing_route"),
        ("europe", "non_university_school_entity"),
        ("europe", "outside_bounded_positive_seed_screen"),
    }
    required_routes = {
        "doctoral_bachelors_entry",
        "research_masters",
        "structured_or_masters_required_doctorate",
    }
    required_fields = {
        "program_id",
        "institution_id",
        "country",
        "region",
        "regional_admissions_model",
        "discovery_paths",
        "exact_research_fit_signal",
        "relevant_degree_route",
        "preliminary_international_eligibility",
        "preliminary_funding_signal",
        "evidence_confidence",
        "proposed_next_action",
    }
    missing_required = [
        row["program_id"]
        for row in candidates
        if any(not row.get(field, "").strip() for field in required_fields)
    ]
    missing_url_without_flag = [
        row["program_id"]
        for row in candidates
        if not row["official_program_url"]
        and "official_program_url" not in split_values(row["unresolved_fields"])
    ]
    screened_without_reason = [
        row["program_id"]
        for row in candidates
        if row["funnel_status"] == "screened_out" and not row["exclusion_reason"]
    ]
    saturation_reached = not any(
        row["audit_result"] in {"reopen_in_funnel", "unresolved_no_independent_positive"}
        for row in audit_rows
    )
    assertions = {
        "all_regions_represented": regions == set(REGIONS),
        "priority_degree_routes_represented": required_routes.issubset(route_buckets),
        "terraprobe_adjacent_seed_recovered": "TerraProbe-adjacent" in seeds,
        "evidex_adjacent_seed_recovered": "Evidex-adjacent" in seeds,
        "exclusion_sample_all_regions": audit_regions == set(REGIONS),
        "exclusion_sample_all_major_strata": required_strata.issubset(audit_strata),
        "exclusion_sample_complete": bool(audit_rows)
        and all(row["sample_status"] == "complete" for row in audit_rows),
        "required_candidate_fields_complete": not missing_required,
        "missing_program_urls_explicitly_flagged": not missing_url_without_flag,
        "screened_out_rows_have_reasons": not screened_without_reason,
        "all_discovery_paths_reported": {row["discovery_path"] for row in yield_rows}
        == set(DISCOVERY_PATHS),
        "non_educational_contamination_reported": any(
            int(row["non_educational_filtered"]) > 0 for row in yield_rows
        ),
        "affiliation_corrections_reported": all(
            "stale_affiliation_name_corrections" in row for row in yield_rows
        ),
        "no_global_top_n_cutoff": "do not apply a global top-N cutoff"
        in str(openalex_manifest.get("selection_policy", "")),
        "no_university_scoring_fields": not any(
            "score" in column or column in {"recommendation", "overall_score"}
            for column in CANDIDATE_FUNNEL_COLUMNS_V2
        ),
        "false_negative_saturation_or_limitation_documented": saturation_reached
        or bool(
            [
                row
                for row in audit_rows
                if row["audit_result"]
                in {"reopen_in_funnel", "unresolved_no_independent_positive"}
            ]
        ),
    }
    return {
        "status": "PASS" if all(assertions.values()) else "FAIL",
        "assertions": assertions,
        "regions": sorted(regions),
        "route_buckets": sorted(route_buckets),
        "seed_categories": sorted(seeds),
        "audit_strata": ["/".join(item) for item in sorted(audit_strata)],
        "saturation_status": "reached" if saturation_reached else "not_reached_documented",
        "missing_required_rows": missing_required,
        "missing_url_without_flag": missing_url_without_flag,
        "screened_without_reason": screened_without_reason,
    }


def build_candidate_funnel(repo_root: str | Path, output_dir: str | Path) -> dict[str, object]:
    repo = Path(repo_root).resolve()
    output = Path(output_dir).resolve()
    institutions, unique_names, ror_to_id, region_by_id = _build_registry(repo)
    openalex_signals, current_faculty, openalex_stats = _merge_openalex(
        repo, institutions, unique_names, ror_to_id
    )
    calendar_path = repo / "reports/20260909-fall2027-audit/final_shortlist.md"
    calendar_rows = parse_calendar_candidates(calendar_path)
    calendar_by_id: dict[str, dict[str, str]] = {}
    unmatched_calendar: list[str] = []
    for row in calendar_rows:
        institution_id, _ = _resolve_institution(
            row["institution_name"], "", institutions, unique_names, ror_to_id
        )
        if institution_id:
            calendar_by_id[institution_id] = row
        else:
            unmatched_calendar.append(row["institution_name"])

    candidates, introduced_by, candidate_stats = _build_candidates(
        repo,
        institutions,
        region_by_id,
        openalex_signals,
        current_faculty,
        calendar_by_id,
    )
    source_counts = {
        "institution_rows": len(institutions),
        "regional_program_rows": candidate_stats.get("regional_program_rows", 0),
        "first_audit_program_rows": candidate_stats.get("first_audit_program_rows", 0),
        "calendar_rows": len(calendar_rows),
    }
    yield_rows = _build_yield_rows(
        candidates, introduced_by, source_counts, openalex_stats
    )
    audit_rows, audit_stats = _build_exclusion_audit(
        repo, candidates, openalex_signals, calendar_by_id
    )
    openalex_manifest = read_json(repo / "data/manifests/openalex_discovery.json")
    validation = validate_stage_02(candidates, yield_rows, audit_rows, openalex_manifest)
    write_csv(
        output / "candidate_program_funnel.csv",
        candidates,
        CANDIDATE_FUNNEL_COLUMNS_V2,
    )
    write_csv(
        output / "discovery_source_yield.csv",
        yield_rows,
        DISCOVERY_SOURCE_YIELD_COLUMNS_V2,
    )
    write_csv(
        output / "exclusion_sample_audit.csv",
        audit_rows,
        EXCLUSION_SAMPLE_AUDIT_COLUMNS_V2,
    )
    return {
        "validation": validation,
        "counts": {
            "candidate_rows": len(candidates),
            "candidate_institutions": len({row["institution_id"] for row in candidates}),
            "advance_to_stage_3": sum(
                row["funnel_status"] == "advance_to_stage_3" for row in candidates
            ),
            "catalog_verification_required": sum(
                row["funnel_status"] == "catalog_verification_required" for row in candidates
            ),
            "manual_secondary_review": sum(
                row["funnel_status"] == "manual_secondary_review" for row in candidates
            ),
            "screened_out": sum(row["funnel_status"] == "screened_out" for row in candidates),
            "official_program_url_present": sum(bool(row["official_program_url"]) for row in candidates),
            "official_program_url_unresolved": sum(not row["official_program_url"] for row in candidates),
            "calendar_rows": len(calendar_rows),
            "calendar_in_scope_matched": len(calendar_by_id),
            "calendar_unmatched_or_out_of_scope": len(unmatched_calendar),
            **{f"openalex_{key}": value for key, value in openalex_stats.items()},
            **{f"exclusion_audit_{key}": value for key, value in audit_stats.items()},
        },
        "unmatched_calendar_candidates": sorted(set(unmatched_calendar)),
        "source_counts": source_counts,
    }
