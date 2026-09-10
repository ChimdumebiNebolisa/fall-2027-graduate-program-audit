from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from graduate_audit.connected_context import CALENDAR_COLUMNS, compare
from graduate_audit.io import read_csv, read_json, write_csv, write_json
from graduate_audit.normalize.integrate import integrate
from graduate_audit.portfolio import score_programs, select_portfolio
from graduate_audit.reporting.outreach import prepare
from graduate_audit.reporting.reports import build_reports
from graduate_audit.schema import PROGRAM_COLUMNS_V2
from graduate_audit.validation import validate_outputs


def finalize(repo_root: Path, output_root: Path, report_root: Path) -> dict[str, object]:
    manifest = integrate(output_root)
    programs = score_programs(
        output_root / "program_screening.csv",
        output_root / "institution_universe.csv",
        output_root / "professor_evidence.csv",
    )
    portfolio = select_portfolio(programs)
    portfolio_decisions = {
        row.get("program_id", ""): label
        for label, key in (("Core", "core"), ("Reserve", "reserve"), ("Monitor", "monitor_for_2027_position"))
        for row in portfolio.get(key, [])
    }
    for row in programs:
        if row.get("program_id", "") in portfolio_decisions:
            row["final_decision"] = portfolio_decisions[row["program_id"]]
        elif row.get("screening_decision", "").lower() in {"excluded", "screened_out", "do_not_apply"}:
            row["final_decision"] = "Do Not Apply"
        elif float(row.get("overall_score") or 0) > 0:
            row["final_decision"] = "Not selected"
    write_csv(output_root / "program_screening.csv", programs, PROGRAM_COLUMNS_V2)
    write_json(output_root / "portfolio.json", portfolio)

    calendar_path = repo_root / "data/private/calendar_candidate_summary.csv"
    if calendar_path.exists():
        write_csv(output_root / "calendar_comparison.csv", compare(calendar_path, output_root), CALENDAR_COLUMNS)
    prepare(repo_root, output_root)

    validation = validate_outputs(output_root)
    write_json(output_root / "validation.json", validation)

    institutions = read_csv(output_root / "institution_universe.csv")
    programs = read_csv(output_root / "program_screening.csv")
    professors = read_csv(output_root / "professor_evidence.csv")
    sources = read_csv(output_root / "source_ledger.csv")
    exclusions = read_csv(output_root / "exclusion_log.csv")
    drafts = read_csv(output_root / "outreach_drafts.csv")
    deep_programs = [
        row for row in programs
        if row.get("verification_status", "").lower() not in {"", "mechanical", "preliminary"}
        and float(row.get("overall_score") or 0) > 0
    ]
    retained = [row for row in programs if row.get("screening_decision", "").lower() == "retained"]
    recommended_professors = [row for row in drafts if row.get("contact_type", "").lower() == "professor"]
    distinct_professors = {
        (
            row.get("institution_id", ""),
            row.get("full_name", "").strip().lower(),
            row.get("email", "").strip().lower(),
        )
        for row in professors
        if row.get("full_name", "").strip()
    }
    manifest["current_date"] = datetime.now(ZoneInfo("America/Chicago")).date().isoformat()
    source_dates = sorted(row.get("date_accessed", "") for row in sources if row.get("date_accessed", ""))
    manifest["evidence_date"] = source_dates[-1] if source_dates else manifest["current_date"]
    manifest["counts"].update({
        "institutions_indexed": len(institutions),
        "institutions_screened": len(institutions),
        "programs_screened": len(programs),
        "programs_deeply_reviewed": len(deep_programs),
        "programs_retained": len(retained),
        "programs_excluded_or_downgraded": sum(
            row.get("screening_decision", "").lower() in {"excluded", "screened_out", "downgrade", "downgraded", "do_not_apply"}
            for row in programs
        ),
        "professor_program_matches_evaluated": len(professors),
        "professors_evaluated": len(distinct_professors),
        "professors_recommended": len(recommended_professors),
        "first_wave_contacts": len(drafts),
        "sources": len(sources),
        "exclusions": len(exclusions),
        "core_applications": len(portfolio.get("core", [])),
        "reserve_applications": len(portfolio.get("reserve", [])),
        "monitor_routes": len(portfolio.get("monitor_for_2027_position", [])),
        "by_institution_status": dict(Counter(row.get("screening_status", "") for row in institutions)),
        "by_program_decision": dict(Counter(row.get("screening_decision", "") for row in programs)),
    })
    manifest["known_failures"] = [
        "Europe ROR API fallback captured 3,628 unique records of 4,462 reported filtered records (81.31%); Zenodo bulk download timed out.",
        "EHESO/ETER API returned HTTP 401 and four national-registry pages were blocked.",
        "Canada retains 50 explicitly unresolved indexed institutions; unresolved records are not treated as evidence of no program.",
    ]
    manifest["unresolved_coverage_gaps"] = [
        "European registry coverage is broad but incomplete because the ROR bulk archive and EHESO were unavailable.",
        "Mechanical screens do not exhaustively crawl every official catalogue; absence of a positive signal is not a universal no-program finding.",
        "Fall 2027 pages, funding awards, and employment vacancies not yet published remain explicitly unresolved.",
    ]
    blocked_websites: list[dict[str, str]] = []
    for blocked_path in sorted((repo_root / "data/manifests").glob("*/blocked_sources.json")):
        payload = read_json(blocked_path)
        for source in payload.get("sources", []):
            blocked_websites.append({
                "name": source.get("name") or source.get("institution") or "Official source",
                "program": source.get("program", ""),
                "url": source.get("url", ""),
                "status": source.get("status", "blocked"),
                "impact": source.get("impact") or source.get("error", ""),
            })
    manifest["blocked_websites"] = blocked_websites
    manifest["validation_results"] = validation
    manifest["scripts_executed"] = list(dict.fromkeys(manifest.get("scripts_executed", []) + [
        "graduate_audit.connected_context",
        "graduate_audit.portfolio",
        "graduate_audit.reporting.outreach",
        "graduate_audit.validation",
        "graduate_audit.reporting.reports",
        "graduate_audit.verify.apply_corrections",
        "graduate_audit.verify.final_validation",
        "scripts/build_workbook.mjs",
    ]))
    write_json(output_root / "run_manifest.json", manifest)
    build_reports(output_root, report_root)
    return {"manifest": manifest, "validation": validation, "portfolio": portfolio}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--reports-dir", required=True)
    args = parser.parse_args()
    result = finalize(Path(args.repo_root).resolve(), Path(args.output_dir).resolve(), Path(args.reports_dir).resolve())
    print({
        "validation": result["validation"]["status"],
        "core": len(result["portfolio"].get("core", [])),
        "reserve": len(result["portfolio"].get("reserve", [])),
    })


if __name__ == "__main__":
    main()
