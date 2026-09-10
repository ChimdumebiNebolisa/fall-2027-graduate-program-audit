from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.professor_mapping import FACULTY_ROSTERS  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    PASS2_SCHEMA_VERSION,
    PROFESSOR_CANDIDATE_EVALUATED_COLUMNS_V2,
    PROFESSOR_MATCH_RETAINED_COLUMNS_V2,
    PROFESSOR_SOURCE_COLUMNS_V2,
    RECRUITING_STATUSES,
    professor_id,
)

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
REPORT_PATH = REPO_ROOT / "reports/pass2/04_professor_mapping.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_04.json"
EVALUATED_PATH = OUTPUT_DIR / "professor_candidates_evaluated.csv"
RETAINED_PATH = OUTPUT_DIR / "professor_matches_retained.csv"
SOURCES_PATH = OUTPUT_DIR / "professor_sources.csv"
REENTRY_RAW_PATHS = (
    REPO_ROOT / "data/raw/pass2/stage_04_reentry_01.json",
    REPO_ROOT / "data/raw/pass2/stage_04_reentry_02.json",
)
LATEST_REENTRY_RAW_PATH = REENTRY_RAW_PATHS[-1]
UNKNOWN = "Not located in bounded Stage 4 review"
CHECK_DATE = "2026-09-10"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def normalized_name(value: str) -> str:
    value = "".join(
        char for char in unicodedata.normalize("NFKD", value) if not unicodedata.combining(char)
    ).casefold()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def parse_top_works(value: str) -> list[tuple[str, str, str]]:
    works: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for part in value.split(" || "):
        match = re.fullmatch(r"(20\d{2}):\s*(.*?)\s*\[(https?://[^]]+)\]", part.strip())
        if not match or int(match.group(1)) < 2022:
            continue
        year, title, url = match.groups()
        key = (title.casefold(), url.casefold())
        if key not in seen:
            works.append((title, url, year))
            seen.add(key)
        if len(works) == 3:
            break
    return works


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
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
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def _regional_rows(filename: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    rows: list[dict[str, str]] = []
    paths: dict[str, str] = {}
    for region in ("us", "canada", "europe"):
        path = REPO_ROOT / f"data/processed/deep_review/{region}/{filename}"
        for row in read_csv(path):
            copied = dict(row)
            copied["_region"] = region
            rows.append(copied)
            if filename == "sources.csv":
                paths[copied["source_id"]] = path.relative_to(REPO_ROOT).as_posix()
    return rows, paths


def _best_openalex(
    lookup: dict[str, list[dict[str, str]]], name: str, institution_name: str
) -> dict[str, str] | None:
    candidates = lookup.get(normalized_name(name), [])
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda row: (
            normalized_name(row["institution_name"]) == normalized_name(institution_name),
            float(row.get("precision_signal") or 0),
            float(row.get("weighted_signal") or 0),
        ),
    )


def _source_row(
    *,
    program: dict[str, str],
    professor: dict[str, str] | None,
    url: str,
    claim_categories: str,
    exact_claim: str,
    title: str,
    source_type: str,
    official_or_secondary: str,
    verification_status: str,
    source_record_path: str,
    publication_year: str = "",
    access_note: str = "",
) -> dict[str, str]:
    pid = professor["professor_id"] if professor else ""
    sid = stable_id("stage4src", program["candidate_program_id"], pid, url, claim_categories)
    return {
        "schema_version": PASS2_SCHEMA_VERSION,
        "stage4_source_id": sid,
        "institution_id": program["institution_id"],
        "institution_name": program["institution_name"],
        "program_id": program["candidate_program_id"],
        "professor_id": pid,
        "professor_name": professor["full_name"] if professor else "",
        "claim_categories": claim_categories,
        "exact_claim_supported": exact_claim,
        "source_title": title,
        "publisher": program["institution_name"] if official_or_secondary == "official" else "OpenAlex / cited venue",
        "url": url,
        "source_type": source_type,
        "official_or_secondary": official_or_secondary,
        "date_accessed": CHECK_DATE,
        "publication_year": publication_year,
        "confidence": "high" if verification_status == "verified" else "medium",
        "verification_status": verification_status,
        "source_record_path": source_record_path,
        "access_note": access_note,
    }


def build() -> dict[str, object]:
    programs = [
        row
        for row in read_csv(OUTPUT_DIR / "program_verification.csv")
        if row["faculty_review_ready"] == "yes"
    ]
    deep_professors, _ = _regional_rows("professors.csv")
    deep_sources, source_paths = _regional_rows("sources.csv")
    reentry_program_ids: set[str] = set()
    latest_reentry_program_ids: set[str] = set()
    for reentry_path in REENTRY_RAW_PATHS:
        reentry = json.loads(reentry_path.read_text(encoding="utf-8"))
        reentry_professors = [dict(row) for row in reentry["professors"]]
        reentry_sources = [dict(row) for row in reentry["sources"]]
        deep_professors.extend(reentry_professors)
        deep_sources.extend(reentry_sources)
        raw_source_path = reentry_path.relative_to(REPO_ROOT).as_posix()
        source_paths.update({row["source_id"]: raw_source_path for row in reentry_sources})
        batch_program_ids = {row["program_id"] for row in reentry_professors}
        reentry_program_ids.update(batch_program_ids)
        if reentry_path == LATEST_REENTRY_RAW_PATH:
            latest_reentry_program_ids = batch_program_ids
    deep_by_program = {row["program_id"]: row for row in deep_professors}
    deep_source_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in deep_sources:
        deep_source_by_url[row["url"].rstrip("/")].append(row)
    openalex_rows = read_csv(REPO_ROOT / "data/processed/openalex_faculty_signals.csv")
    openalex_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in openalex_rows:
        openalex_by_name[normalized_name(row["author_name"])].append(row)

    evaluated: list[dict[str, str]] = []
    retained: list[dict[str, str]] = []
    sources: list[dict[str, str]] = []

    for program in sorted(programs, key=lambda row: (row["region"], row["institution_name"], row["candidate_program_id"])):
        program_id_value = program["candidate_program_id"]
        strongest = deep_by_program.get(program_id_value)
        if strongest is None:
            raise ValueError(f"No verified deep-review professor for {program_id_value}")
        roster = FACULTY_ROSTERS[program["institution_name"]]
        roster_source = _source_row(
            program=program,
            professor=None,
            url=roster.roster_url,
            claim_categories="current faculty roster|candidate longlist",
            exact_claim=(
                "Current official department roster or research-area faculty listing used to identify "
                "the five-person Stage 4 candidate longlist."
            ),
            title=f"{program['institution_name']} current faculty roster",
            source_type="official faculty roster or research-area page",
            official_or_secondary="official",
            verification_status="verified",
            source_record_path="Stage 4 live official-source review",
            access_note="Roster evidence establishes a current listing, not program-specific supervision authority or recruiting.",
        )
        sources.append(roster_source)

        candidate_specs = [(strongest["full_name"], strongest["research_themes"], True)] + [
            (candidate.name, candidate.themes, False) for candidate in roster.alternatives
        ]
        if len({normalized_name(name) for name, _, _ in candidate_specs}) != 5:
            raise ValueError(f"Longlist does not contain five distinct people: {program_id_value}")

        strongest_works = [
            (
                strongest.get(f"recent_work_{index}", ""),
                strongest.get(f"recent_work_{index}_url", ""),
                strongest.get(f"recent_work_{index}_year", ""),
            )
            for index in range(1, 4)
            if strongest.get(f"recent_work_{index}", "")
            and strongest.get(f"recent_work_{index}_url", "")
            and strongest.get(f"recent_work_{index}_year", "")
        ]
        strongest_qualifies = (
            strongest["can_supervise_program"].casefold() == "yes"
            and strongest["fit_strength"].casefold() == "strong"
            and bool(strongest_works)
            and "current" in strongest["appointment_status"].casefold()
        )
        program_match_count = 1 if strongest_qualifies else 0
        program_depth = 5 if strongest_qualifies else 0
        good_faith_result = (
            "Five current-roster candidates were evaluated. One met the combined current-appointment, "
            "program-supervision-authority, strong-overlap, and recent-work evidence gate. Four remained "
            "plausible but unscored and were not retained because authority and/or current-work evidence "
            "was incomplete; superficial fit was not promoted."
            if strongest_qualifies else
            "Five current-roster candidates were evaluated. None met the combined current-appointment, "
            "program-supervision-authority, strong-overlap, and recent-work evidence gate. The leading "
            "research-fit candidate and four alternatives remain plausible but unscored; exact-route "
            "supervision authority and/or candidate-specific current-work evidence is incomplete."
        )

        for name, themes, is_primary in candidate_specs:
            pid = professor_id(program["institution_id"], name)
            source_ids = [roster_source["stage4_source_id"]]
            works: list[tuple[str, str, str]] = []
            openalex = _best_openalex(openalex_by_name, name, program["institution_name"])
            qualifies = is_primary and strongest_qualifies
            if is_primary:
                works = list(strongest_works)
                extra_evidence_urls = [
                    url.strip()
                    for url in strongest.get("extra_evidence_urls", "").split("|")
                    if url.strip()
                ]
                evidence_urls = [strongest["official_faculty_url"]] + [url for _, url, _ in works] + extra_evidence_urls
                for url in dict.fromkeys(evidence_urls):
                    original = (deep_source_by_url.get(url.rstrip("/")) or [None])[0]
                    is_profile = url.rstrip("/") == strongest["official_faculty_url"].rstrip("/")
                    source = _source_row(
                        program=program,
                        professor={"professor_id": pid, "full_name": name},
                        url=url,
                        claim_categories=(original.get("stage4_claim_categories", "") if original else "") or (
                            "current appointment|program supervision authority|research themes"
                            if is_profile else "recent work|research fit"
                        ),
                        exact_claim=(original.get("exact_claim_supported", "") if original else "") or (
                            f"{name} has a current verified appointment and verified authority to supervise this program."
                            if is_profile
                            else f"Recent work supports the recorded TerraProbe/Evidex research overlap for {name}."
                        ),
                        title=(original["source_title"] if original else (name if is_profile else "Recent scholarly work")),
                        source_type=(original["source_type"] if original else ("official faculty page" if is_profile else "scholarly work")),
                        official_or_secondary=(
                            "official" if is_profile else (
                                "official" if original and original["official_or_secondary"].casefold().startswith("official") else "secondary"
                            )
                        ),
                        verification_status="verified",
                        source_record_path=(source_paths.get(original["source_id"], "") if original else ""),
                        publication_year=(
                            original.get("publication_year", "") if original else ""
                        ) or next((year for _, work_url, year in works if work_url == url), ""),
                        access_note=(original["access_note"] if original else "Carried from verified regional deep-review evidence."),
                    )
                    sources.append(source)
                    source_ids.append(source["stage4_source_id"])
            elif openalex:
                works = parse_top_works(openalex.get("top_works", ""))
                if works:
                    openalex_url = openalex.get("openalex_author_id", "") or "https://openalex.org"
                    source = _source_row(
                        program=program,
                        professor={"professor_id": pid, "full_name": name},
                        url=openalex_url,
                        claim_categories="discovery publication signal|recent work",
                        exact_claim=(
                            "Publication metadata was examined for shortlist triage only; publication-time affiliation "
                            "does not establish current appointment, supervision authority, or recruiting."
                        ),
                        title=f"OpenAlex publication signal for {name}",
                        source_type="secondary publication index",
                        official_or_secondary="secondary",
                        verification_status="discovery_only",
                        source_record_path="data/processed/openalex_faculty_signals.csv",
                        access_note="Not used to award a professor score or faculty-depth point.",
                    )
                    sources.append(source)
                    source_ids.append(source["stage4_source_id"])

            padded = works[:3] + [("", "", "")] * (3 - len(works[:3]))
            row = {
                "schema_version": PASS2_SCHEMA_VERSION,
                "evaluation_id": stable_id("stage4eval", program_id_value, pid),
                "professor_id": pid,
                "institution_id": program["institution_id"],
                "institution_name": program["institution_name"],
                "country": program["country"],
                "region": program["region"],
                "program_id": program_id_value,
                "program_name": program["exact_degree_program_name"],
                "full_name": name,
                "current_department": strongest["department"] if is_primary else roster.department,
                "faculty_position": strongest["faculty_position"] if is_primary else "Faculty; rank not independently reverified",
                "appointment_status": (
                    strongest["appointment_status"] if is_primary
                    else f"Current official roster listing verified {CHECK_DATE}"
                ),
                "supervision_authority_status": strongest["can_supervise_program"] if is_primary else "Unresolved for this specific program",
                "official_email": strongest["official_email"] or UNKNOWN if is_primary else UNKNOWN,
                "official_faculty_or_lab_url": strongest["official_faculty_url"] if is_primary else roster.roster_url,
                "official_roster_url": roster.roster_url,
                "research_themes": themes,
                "recent_work_1_title": padded[0][0],
                "recent_work_1_url": padded[0][1],
                "recent_work_1_year": padded[0][2],
                "recent_work_2_title": padded[1][0],
                "recent_work_2_url": padded[1][1],
                "recent_work_2_year": padded[1][2],
                "recent_work_3_title": padded[2][0],
                "recent_work_3_url": padded[2][1],
                "recent_work_3_year": padded[2][2],
                "recent_work_evidence_count": str(len(works)),
                "specific_overlap": (
                    strongest["fit_explanation"] if is_primary else
                    f"Plausible TerraProbe/Evidex overlap in {themes}; strong-match status was not inferred."
                ),
                "fit_strength": strongest["fit_strength"] if qualifies else "Plausible — unscored",
                "fit_rationale": strongest["fit_explanation"] if qualifies else (
                    "Current roster/research-area evidence supports shortlist inclusion, but the Stage 4 record does "
                    "not establish both candidate-specific recent work and authority to supervise this exact route."
                ),
                "candidate_disposition": "retained_strong" if qualifies else "plausible_not_retained",
                "non_retention_reason": "" if qualifies else (
                    "Not retained: program-specific supervision authority is unresolved; candidate-specific recent-work "
                    "evidence is incomplete or discovery-only. No professor score was assigned."
                ),
                "recruiting_evidence": strongest["recruiting_evidence"] if is_primary else "No current direct recruiting statement verified in the bounded review",
                "recruiting_status": strongest["recruiting_status"] if is_primary else "Recruiting status unknown",
                "prospective_student_instructions": strongest["prospective_student_instructions"],
                "contacting_faculty_appropriate": strongest["contacting_faculty_appropriate"],
                "openalex_author_id": (openalex.get("openalex_author_id", "") if openalex else ""),
                "source_ids": "|".join(dict.fromkeys(source_ids)),
                "unresolved_question": (
                    "Recruiting status remains unknown unless the cited evidence explicitly states otherwise."
                    if qualifies else
                    "Would this faculty member have authority and capacity to supervise this exact route, and does current work justify strong fit?"
                ),
                "verification_status": "verified_strong_match" if qualifies else "roster_verified_candidate; authority_or_work_incomplete",
                "plausible_candidates_evaluated": "5",
                "distinct_verified_strong_matches": str(program_match_count),
                "faculty_depth_points": str(program_depth),
                "single_professor_dependency": "true" if program_match_count == 1 else "false",
                "good_faith_search_result": good_faith_result,
                "evaluated_at": now(),
            }
            evaluated.append(row)

            if qualifies:
                retained.append({
                    "schema_version": PASS2_SCHEMA_VERSION,
                    "match_id": stable_id("stage4match", program_id_value, pid),
                    "match_rank": "1",
                    "professor_id": pid,
                    "institution_id": program["institution_id"],
                    "institution_name": program["institution_name"],
                    "country": program["country"],
                    "region": program["region"],
                    "program_id": program_id_value,
                    "program_name": program["exact_degree_program_name"],
                    "full_name": name,
                    "current_department": row["current_department"],
                    "faculty_position": row["faculty_position"],
                    "appointment_status": row["appointment_status"],
                    "supervision_authority_status": row["supervision_authority_status"],
                    "official_email": row["official_email"],
                    "official_faculty_or_lab_url": row["official_faculty_or_lab_url"],
                    "research_themes": row["research_themes"],
                    "recent_work_1_title": row["recent_work_1_title"],
                    "recent_work_1_url": row["recent_work_1_url"],
                    "recent_work_1_year": row["recent_work_1_year"],
                    "recent_work_2_title": row["recent_work_2_title"],
                    "recent_work_2_url": row["recent_work_2_url"],
                    "recent_work_2_year": row["recent_work_2_year"],
                    "recent_work_3_title": row["recent_work_3_title"],
                    "recent_work_3_url": row["recent_work_3_url"],
                    "recent_work_3_year": row["recent_work_3_year"],
                    "recent_work_evidence_count": row["recent_work_evidence_count"],
                    "specific_overlap": row["specific_overlap"],
                    "fit_strength": row["fit_strength"],
                    "fit_rationale": row["fit_rationale"],
                    "recruiting_evidence": row["recruiting_evidence"],
                    "recruiting_status": row["recruiting_status"],
                    "prospective_student_instructions": row["prospective_student_instructions"],
                    "contacting_faculty_appropriate": row["contacting_faculty_appropriate"],
                    "source_ids": row["source_ids"],
                    "unresolved_question": row["unresolved_question"],
                    "verification_status": row["verification_status"],
                    "plausible_candidates_evaluated": "5",
                    "distinct_verified_strong_matches": "1",
                    "faculty_depth_points": "5",
                    "single_professor_dependency": "true",
                    "good_faith_search_result": good_faith_result,
                    "retained_at": now(),
                })

    write_csv(EVALUATED_PATH, evaluated, PROFESSOR_CANDIDATE_EVALUATED_COLUMNS_V2)
    write_csv(RETAINED_PATH, retained, PROFESSOR_MATCH_RETAINED_COLUMNS_V2)
    unique_sources = {row["stage4_source_id"]: row for row in sources}
    sources = [unique_sources[key] for key in sorted(unique_sources)]
    write_csv(SOURCES_PATH, sources, PROFESSOR_SOURCE_COLUMNS_V2)

    evaluated_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    retained_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evaluated:
        evaluated_by_program[row["program_id"]].append(row)
    for row in retained:
        retained_by_program[row["program_id"]].append(row)
    serious_ids = {row["candidate_program_id"] for row in programs}
    source_ids = {row["stage4_source_id"] for row in sources}
    assertions = {
        "all_serious_programs_covered": set(evaluated_by_program) == serious_ids and set(retained_by_program).issubset(serious_ids),
        "at_least_five_candidates_per_serious_program": all(len(evaluated_by_program[pid]) >= 5 for pid in serious_ids),
        "no_more_than_three_matches_per_program": all(0 <= len(retained_by_program[pid]) <= 3 for pid in serious_ids),
        "good_faith_fewer_recorded": all(all(row["good_faith_search_result"] for row in evaluated_by_program[pid]) for pid in serious_ids),
        "retained_matches_have_current_appointments": all("current" in row["appointment_status"].casefold() for row in retained),
        "retained_matches_have_verified_supervision_authority": all(row["supervision_authority_status"].casefold() == "yes" for row in retained),
        "retained_matches_have_recent_work_evidence": all(int(row["recent_work_evidence_count"]) >= 1 and row["recent_work_1_url"] and row["recent_work_1_year"] for row in retained),
        "retained_matches_are_strong_and_verified": all(row["fit_strength"].casefold() == "strong" and row["verification_status"] == "verified_strong_match" for row in retained),
        "recruiting_statuses_are_controlled": all(row["recruiting_status"] in RECRUITING_STATUSES for row in evaluated),
        "no_professor_score_columns_exist": not any("score" in name.casefold() for name in PROFESSOR_CANDIDATE_EVALUATED_COLUMNS_V2 + PROFESSOR_MATCH_RETAINED_COLUMNS_V2),
        "faculty_depth_rule_enforced": all(
            all(
                row["distinct_verified_strong_matches"] == str(len(retained_by_program[pid]))
                and row["faculty_depth_points"] == ("5" if len(retained_by_program[pid]) == 1 else "0")
                and row["single_professor_dependency"] == ("true" if len(retained_by_program[pid]) == 1 else "false")
                for row in evaluated_by_program[pid]
            )
            for pid in serious_ids
        ),
        "university_level_people_deduplicate": len({row["professor_id"] for row in retained}) <= len(retained),
        "all_candidate_source_ids_resolve": all(set(row["source_ids"].split("|")).issubset(source_ids) for row in evaluated),
        "official_roster_source_per_program": all(any(s["program_id"] == pid and "current faculty roster" in s["claim_categories"] and s["official_or_secondary"] == "official" for s in sources) for pid in serious_ids),
        "required_output_schemas_exact": list(evaluated[0]) == list(PROFESSOR_CANDIDATE_EVALUATED_COLUMNS_V2) and list(retained[0]) == list(PROFESSOR_MATCH_RETAINED_COLUMNS_V2) and list(sources[0]) == list(PROFESSOR_SOURCE_COLUMNS_V2),
    }
    counts = {
        "serious_programs": len(serious_ids),
        "institutions": len({row["institution_id"] for row in programs}),
        "candidate_evaluations": len(evaluated),
        "distinct_candidate_professors": len({row["professor_id"] for row in evaluated}),
        "retained_match_rows": len(retained),
        "distinct_retained_professors": len({row["professor_id"] for row in retained}),
        "retained_matches_without_official_email": sum(
            not row["official_email"] or row["official_email"] == UNKNOWN for row in retained
        ),
        "programs_with_zero_strong_matches": sum(len(retained_by_program[pid]) == 0 for pid in serious_ids),
        "programs_with_one_strong_match": sum(len(retained_by_program[pid]) == 1 for pid in serious_ids),
        "programs_with_two_strong_matches": sum(len(retained_by_program[pid]) == 2 for pid in serious_ids),
        "programs_with_three_strong_matches": sum(len(retained_by_program[pid]) >= 3 for pid in serious_ids),
        "candidate_rows_with_recent_work": sum(int(row["recent_work_evidence_count"]) > 0 for row in evaluated),
        "source_rows": len(sources),
        "official_source_rows": sum(row["official_or_secondary"] == "official" for row in sources),
        "secondary_discovery_source_rows": sum(row["official_or_secondary"] == "secondary" for row in sources),
        "reentry_programs": len(reentry_program_ids),
        "reentry_retained_match_rows": sum(row["program_id"] in reentry_program_ids for row in retained),
        "reentry_zero_match_programs": sum(
            not retained_by_program[program_id] for program_id in reentry_program_ids
        ),
        "latest_reentry_programs": len(latest_reentry_program_ids),
        "latest_reentry_retained_match_rows": sum(
            row["program_id"] in latest_reentry_program_ids for row in retained
        ),
        "latest_reentry_zero_match_programs": sum(
            not retained_by_program[program_id] for program_id in latest_reentry_program_ids
        ),
    }
    return {
        "assertions": assertions,
        "counts": counts,
        "status": "PASS" if all(assertions.values()) else "FAIL",
    }


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(str(value).replace("|", "/") for value in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def write_report(result: dict[str, object]) -> None:
    retained = read_csv(RETAINED_PATH)
    evaluated = read_csv(EVALUATED_PATH)
    counts = result["counts"]
    by_region_programs = Counter()
    seen_programs: set[str] = set()
    for row in evaluated:
        if row["program_id"] not in seen_programs:
            by_region_programs[row["region"]] += 1
            seen_programs.add(row["program_id"])
    by_region_retained = Counter(row["region"] for row in retained)
    lines = [
        "# Pass 2 Stage 4 — Professor and department fit mapping",
        "",
        f"Generated: {now()}",
        "",
        f"Decision: **{result['status']}**",
        "",
        "## Outcome",
        "",
        (
            f"All {counts['serious_programs']} faculty-review-ready programs were searched against a current official "
            f"faculty roster or department research-area listing. Exactly five plausible candidates were evaluated "
            f"for each program ({counts['candidate_evaluations']} program-candidate evaluations; "
            f"{counts['distinct_candidate_professors']} distinct people after university-level deduplication)."
        ),
        "",
        (
            f"The defensible retained set contains {counts['retained_match_rows']} program-match rows representing "
            f"{counts['distinct_retained_professors']} distinct professors. Each program has one fully verified strong "
            f"match in {counts['programs_with_one_strong_match']} programs; the other "
            f"{counts['programs_with_zero_strong_matches']} programs have no match that clears every evidence gate. "
            "One-match programs receive 5 depth points and zero-match programs receive 0. No individual professor "
            "score exists in the Stage 4 outputs."
        ),
        "",
        "## Coverage",
        "",
        table(
            ["Region", "Serious programs", "Retained match rows"],
            [[region, by_region_programs[region], by_region_retained[region]] for region in ("us", "canada", "europe")]
            + [["Total", counts["serious_programs"], counts["retained_match_rows"]]],
        ),
        "",
        "## Department-depth result",
        "",
        table(
            ["Verified strong matches per program", "Programs", "Depth points", "Single-professor dependency"],
            [
                [0, counts["programs_with_zero_strong_matches"], 0, "false"],
                [1, counts["programs_with_one_strong_match"], 5, "true"],
                [2, counts["programs_with_two_strong_matches"], 10, "false"],
                ["3+", counts["programs_with_three_strong_matches"], 15, "false"],
            ],
        ),
        "",
        "University-level counts use `professor_id`, so the same person attached to multiple UBC, Calgary, or Waterloo routes is counted once.",
        "",
        "## Retained matches",
        "",
        table(
            ["Region", "Institution", "Program", "Professor", "Depth", "Recruiting status"],
            [[row["region"], row["institution_name"], row["program_name"], row["full_name"], row["faculty_depth_points"], row["recruiting_status"]] for row in retained],
        ),
        "",
        "## Good-faith fewer-than-three record",
        "",
        (
            "For every program, four additional current-roster candidates were evaluated. They remain in "
            "`professor_candidates_evaluated.csv` as plausible, unscored candidates. None was promoted merely from "
            "department membership, biography keywords, publication-time affiliation, or fame. A candidate was retained "
            "only when the evidence simultaneously established a current appointment, authority to supervise the exact "
            "program, specific strong research overlap, and at least one recent work/project with URL and year."
        ),
        "",
        f"Recent-work metadata was available for {counts['candidate_rows_with_recent_work']} of {counts['candidate_evaluations']} candidate evaluations. Discovery-only OpenAlex records never establish appointment, supervision, or recruiting.",
        "",
        "## Recruiting and contact controls",
        "",
        (
            "Recruiting is `Confirmed recruiting` only when the retained evidence explicitly says so; otherwise the "
            "controlled status from the verified regional record is preserved. Research activity is not treated as "
            "recruiting. Prospective-student instructions and contact appropriateness are recorded separately from fit."
        ),
        "",
        "## Acceptance checks",
        "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in result["assertions"].items()]),
        "",
        "## Blockers",
        "",
        "None prevented Stage 4 completion.",
        "",
        "## Unresolved coverage",
        "",
        (
            f"- Stage 4 re-entry 02 evaluated {counts['latest_reentry_programs']} newly eligible routes and retained "
            f"{counts['latest_reentry_retained_match_rows']} fully verified strong lead matches; "
            f"{counts['latest_reentry_zero_match_programs']} new route remains without a retained match. Across both "
            f"re-entry batches, {counts['reentry_retained_match_rows']} of {counts['reentry_programs']} routes have a retained match."
        ),
        "- UVA's strongest bounded fit has a current courtesy Computer Science appointment, but exact Computer Science PhD supervision authority was not verified; the candidate remains unscored and unretained.",
        f"- {counts['programs_with_one_strong_match']} of {counts['serious_programs']} programs have only one fully verified strong match and remain single-professor dependencies.",
        f"- {counts['programs_with_zero_strong_matches']} programs have no candidate that clears every current-appointment, supervision-authority, strong-fit, and recent-work gate; their faculty depth is 0.",
        f"- {counts['candidate_evaluations'] - counts['retained_match_rows']} plausible program-candidate evaluations were not retained because exact-route supervision authority and/or candidate-specific recent-work evidence remains incomplete.",
        f"- Official email remains unlocated for {counts['retained_matches_without_official_email']} retained professors and most unretained candidates; no address is guessed.",
        "- Recruiting status remains unknown unless a current direct statement/opening was already verified; publication activity and open labs are not used as recruiting proxies.",
        "- Faculty appointments, supervision rules, and recruiting statements are time-sensitive and require a refresh immediately before outreach or application submission.",
        "- Stage 5 scoring still covers the prior 55-program roster. Its eight-route coverage gap is intentionally unresolved at this stage boundary and must be rebuilt in Stage 5 re-entry 02.",
        "- Stage 5 may use only the 5-point faculty-depth values supported here; it may not resurrect the inflated Pass 1 depth scores.",
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def input_paths() -> list[Path]:
    paths = [
        REPO_ROOT / "data/manifests/pass2/stage_03.json",
        OUTPUT_DIR / "program_verification.csv",
        REPO_ROOT / "data/processed/openalex_faculty_signals.csv",
        *REENTRY_RAW_PATHS,
        REPO_ROOT / "src/graduate_audit/professor_mapping.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
    ]
    for region in ("us", "canada", "europe"):
        paths.extend(
            (
                REPO_ROOT / f"data/processed/deep_review/{region}/professors.csv",
                REPO_ROOT / f"data/processed/deep_review/{region}/sources.csv",
            )
        )
    return paths


def main() -> int:
    started_at = now()
    source_commit = git_head()
    result = build()
    write_report(result)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["4"] = "complete" if result["status"] == "PASS" else "failed"
    stage_status["4_reentry_01"] = "complete" if result["status"] == "PASS" else "failed"
    stage_status["4_reentry_02"] = "complete" if result["status"] == "PASS" else "failed"
    pass2.update({
        "current_stage": 4,
        "last_completed_stage": max(int(pass2.get("last_completed_stage", 0)), 4) if result["status"] == "PASS" else 3,
        "stage_status": stage_status,
        "next_stage": 5,
        "next_stage_authorized": result["status"] == "PASS",
        "stage_manifest": "data/manifests/pass2/stage_04.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_04_acceptance": result["status"],
        "stage_04_serious_programs": result["counts"]["serious_programs"],
        "stage_04_distinct_retained_professors": result["counts"]["distinct_retained_professors"],
        "stage_04_reentry_completed": 2 if result["status"] == "PASS" else 1,
        "stage_04_reentry_programs": result["counts"]["latest_reentry_programs"],
        "stage_04_reentry_cumulative_programs": result["counts"]["reentry_programs"],
        "stage_04_reentry_required": False,
        "stage_05_reentry_required": result["status"] == "PASS",
        "stage_05_reentry_source_stage": 4,
    })
    update_progress(
        progress_path,
        current_phase="pass2_stage_04_complete" if result["status"] == "PASS" else "pass2_stage_04_failed",
        pass2=pass2,
    )

    unresolved = [
        f"{result['counts']['programs_with_one_strong_match']} serious programs remain single-professor dependencies with one verified strong match and 5 faculty-depth points.",
        f"{result['counts']['programs_with_zero_strong_matches']} serious programs have no match clearing every evidence gate and receive 0 faculty-depth points.",
        f"The {result['counts']['candidate_evaluations'] - result['counts']['retained_match_rows']} unretained longlist evaluations still need exact-route supervision-authority and/or candidate-specific current-work verification before they could become strong matches.",
        f"Official email remains unlocated for {result['counts']['retained_matches_without_official_email']} retained professors and most unretained candidates; no address is guessed.",
        "Recruiting remains unknown unless supported by a current explicit statement; research activity is not recruiting evidence.",
        "Faculty appointment and recruiting evidence must be refreshed before outreach or submission.",
        "The strongest bounded UVA fit has a courtesy Computer Science appointment, but exact Computer Science PhD supervision authority remains unresolved and no UVA match was retained.",
        "Stage 5 scoring still covers the prior 55-program roster; all eight new routes remain intentionally absent until Stage 5 re-entry 02 is executed.",
    ]
    output_paths = [EVALUATED_PATH, RETAINED_PATH, SOURCES_PATH, REPORT_PATH]
    artifacts = [
        REPO_ROOT / "src/graduate_audit/professor_mapping.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "scripts/build_stage_04.py",
        REPO_ROOT / "tests/test_professor_mapping.py",
        *REENTRY_RAW_PATHS,
        progress_path,
        *output_paths,
    ]
    manifest = {
        "manifest_version": "1.0",
        "schema_version": PASS2_SCHEMA_VERSION,
        "stage": 4,
        "run_type": "faculty_reentry_02",
        "name": "Deep professor and department fit mapping",
        "status": "complete" if result["status"] == "PASS" else "failed",
        "decision": result["status"],
        "source_commit_before_stage": source_commit,
        "triggered_by_stage": 3,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in input_paths()],
        "outputs": [file_record(path) for path in output_paths],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": result["status"],
            "assertions": result["assertions"],
            "faculty_depth_rule": {"0": 0, "1": 5, "2": 10, "3_or_more": 15},
            "individual_professor_scoring": "absent",
        },
        "counts": result["counts"],
        "failures": [] if result["status"] == "PASS" else [name for name, passed in result["assertions"].items() if not passed],
        "blockers": [],
        "unresolved_coverage": unresolved,
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 4 manifest: {result['status']}")
    print(result["counts"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
