from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from graduate_audit.io import read_csv, write_csv, write_json
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
)

ROOT = Path(__file__).resolve().parents[3]
REGIONS = ("us", "canada", "europe")
DEEP_REVIEW_ROOT = ROOT / "data" / "processed" / "deep_review"


def _find_region_file(region: str, kind: str) -> Path | None:
    region_root = ROOT / "data" / "processed" / "regions" / region
    candidates = sorted(region_root.glob(f"*{kind}*.csv"))
    return candidates[0] if candidates else None


def _merge_rows(kind: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for region in REGIONS:
        path = _find_region_file(region, kind)
        if path:
            for row in read_csv(path):
                row.setdefault("region", region)
                rows.append(row)
    return rows


def _read_deep_review(filename: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not DEEP_REVIEW_ROOT.exists():
        return rows
    for path in sorted(DEEP_REVIEW_ROOT.glob(f"*/{filename}")):
        rows.extend(read_csv(path))
    return rows


def _replace_with_deep_review(
    base_rows: list[dict[str, str]],
    deep_rows: list[dict[str, str]],
    key: str,
) -> list[dict[str, str]]:
    """Use a verified deep-review row when it shares a stable key with a seed row."""
    if not deep_rows:
        return base_rows
    deep_keys = {row.get(key, "").strip() for row in deep_rows if row.get(key, "").strip()}
    deep_program_names = {
        (row.get("institution_id", "").strip(), row.get("program_name", "").strip().casefold())
        for row in deep_rows
        if row.get("institution_id", "").strip() and row.get("program_name", "").strip()
    }
    return [
        row for row in base_rows
        if row.get(key, "").strip() not in deep_keys
        and (row.get("institution_id", "").strip(), row.get("program_name", "").strip().casefold()) not in deep_program_names
    ] + deep_rows


def _dedupe(rows: list[dict[str, str]], key: str) -> tuple[list[dict[str, str]], list[str]]:
    chosen: dict[str, dict[str, str]] = {}
    duplicate_keys: list[str] = []
    for row in rows:
        row_key = row.get(key, "").strip()
        if not row_key:
            continue
        if row_key not in chosen:
            chosen[row_key] = row
            continue
        duplicate_keys.append(row_key)
        existing = chosen[row_key]
        for field, value in row.items():
            if value and not existing.get(field):
                existing[field] = value
    return list(chosen.values()), sorted(set(duplicate_keys))


def integrate(output_dir: str | Path) -> dict[str, object]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    institutions_raw = _merge_rows("institution")
    programs_raw = _replace_with_deep_review(
        _merge_rows("program"), _read_deep_review("deep_programs.csv"), "program_id"
    )
    exclusions_raw = _merge_rows("exclusion") + _read_deep_review("exclusion_or_downgrade.csv")
    sources_raw = _merge_rows("source") + _read_deep_review("sources.csv")
    professors_raw = _merge_rows("professor") + _read_deep_review("professors.csv")

    institutions, duplicate_institutions = _dedupe(institutions_raw, "institution_id")
    programs, duplicate_programs = _dedupe(programs_raw, "program_id")
    professors, duplicate_professors = _dedupe(professors_raw, "professor_id")

    program_decisions: dict[str, set[str]] = {}
    for row in programs:
        program_decisions.setdefault(row.get("institution_id", ""), set()).add(
            row.get("screening_decision", "").strip().lower()
        )
    for row in institutions:
        decisions = program_decisions.get(row.get("institution_id", ""), set())
        if "retained" in decisions:
            row["screening_status"] = "retained"
            row["exclusion_reason"] = ""
        elif decisions & {"deep_review", "advance_to_deep_review"}:
            row["screening_status"] = "deep_review"
        elif decisions and decisions <= {"excluded", "screened_out", "do_not_apply", "deprioritize"}:
            row["screening_status"] = "program_screened_out"
            if not row.get("exclusion_reason"):
                row["exclusion_reason"] = "All identified candidate programs failed a program-level hard gate or fit screen."

    write_csv(destination / "institution_universe.csv", institutions, INSTITUTION_COLUMNS)
    write_csv(destination / "program_screening.csv", programs, PROGRAM_COLUMNS)
    write_csv(destination / "exclusion_log.csv", exclusions_raw, EXCLUSION_COLUMNS)
    write_csv(destination / "professor_evidence.csv", professors, PROFESSOR_COLUMNS)
    write_csv(destination / "source_ledger.csv", sources_raw, SOURCE_COLUMNS)

    statuses = Counter(row.get("screening_status", "") for row in institutions)
    program_decisions = Counter(row.get("screening_decision", "") for row in programs)
    countries = Counter(row.get("country", "") for row in institutions)
    region_counts = Counter(row.get("region", "") for row in institutions)
    manifest_files = []
    for manifest_path in sorted((ROOT / "data" / "manifests").rglob("*.json")):
        try:
            manifest_files.append({
                "path": str(manifest_path.relative_to(ROOT)),
                "payload": json.loads(manifest_path.read_text(encoding="utf-8")),
            })
        except (OSError, json.JSONDecodeError) as exc:
            manifest_files.append({"path": str(manifest_path.relative_to(ROOT)), "error": str(exc)})

    manifest = {
        "run_id": destination.name,
        "current_date": datetime.now().astimezone().date().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "region_definitions": {
            "us": "50 states, District of Columbia, and IPEDS other US jurisdictions",
            "canada": "all provinces and territories",
            "europe": "EU-27 plus United Kingdom, Norway, Switzerland, and Iceland",
        },
        "counts": {
            "institutions_indexed": len(institutions),
            "programs_considered": len(programs),
            "exclusions": len(exclusions_raw),
            "professors_evaluated": len(professors),
            "sources": len(sources_raw),
            "by_region": dict(region_counts),
            "by_country": dict(countries),
            "by_institution_status": dict(statuses),
            "by_program_decision": dict(program_decisions),
        },
        "deduplication": {
            "duplicate_institution_ids_resolved": duplicate_institutions,
            "duplicate_program_ids_resolved": duplicate_programs,
            "duplicate_professor_ids_resolved": duplicate_professors,
        },
        "dataset_manifests": manifest_files,
        "scripts_executed": [
            "graduate_audit.research_fit.openalex_discovery",
            "graduate_audit.normalize.integrate",
        ],
        "known_failures": [],
        "blocked_websites": [],
        "unresolved_coverage_gaps": [],
        "validation_results": {},
    }
    write_json(destination / "run_manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(integrate(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
