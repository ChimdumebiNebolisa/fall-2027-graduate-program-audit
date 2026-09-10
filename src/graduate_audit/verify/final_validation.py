from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from graduate_audit.io import read_csv, write_json


EXPECTED_SHEETS = {
    "coverage_dashboard.png",
    "schools_and_programs.png",
    "professor_matches.png",
    "department_and_admin_outreach.png",
    "school_summary.png",
    "this_weekend_outreach_queue.png",
    "outreach_drafts.png",
    "screening_and_exclusions.png",
    "calendar_comparison.png",
    "sources.png",
    "methodology.png",
}


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def validate(repo_root: Path, output_root: Path, require_workbook: bool) -> dict[str, object]:
    errors: list[str] = []
    checks: dict[str, object] = {}
    base = _read_json(output_root / "validation.json")
    if base.get("status") != "PASS":
        errors.append("base CSV validation did not pass")

    portfolio = _read_json(output_root / "portfolio.json")
    core_ids = {row.get("program_id", "") for row in portfolio.get("core", [])}
    verified_ids: set[str] = set()
    validation_root = repo_root / "data/processed/validation"
    for relative in (
        "finalists_us/program_checks.csv",
        "finalists_us/exclusion_sample_checks.csv",
        "cross_region_ca/europe_finalist_second_source.csv",
        "cross_region_eu/second_source_checks.csv",
    ):
        path = validation_root / relative
        if path.exists():
            verified_ids.update(row.get("program_id", "") for row in read_csv(path) if row.get("program_id"))
    missing_finalists = sorted(core_ids - verified_ids)
    if missing_finalists:
        errors.append(f"core finalists missing independent verification: {missing_finalists}")
    checks["core_finalists_second_source_checked"] = len(core_ids) - len(missing_finalists)

    sampled_regions: set[str] = set()
    for relative in (
        "finalists_us/exclusion_sample_checks.csv",
        "cross_region_ca/exclusion_sample_audit.csv",
        "cross_region_eu/second_source_checks.csv",
    ):
        path = validation_root / relative
        if not path.exists():
            continue
        for row in read_csv(path):
            if "exclusion" not in (row.get("portfolio_tier", "") + row.get("record_type", "") + row.get("claim_type", "")).lower() and not row.get("sample_id"):
                continue
            region = (row.get("region") or row.get("country") or "").lower()
            if "united states" in region or region == "us":
                sampled_regions.add("us")
            elif "canada" in region:
                sampled_regions.add("canada")
            elif region:
                sampled_regions.add("europe")
    missing_regions = {"us", "canada", "europe"} - sampled_regions
    if missing_regions:
        errors.append(f"missing independent exclusion sample for regions: {sorted(missing_regions)}")
    checks["exclusion_sample_regions"] = sorted(sampled_regions)

    programs = {row.get("program_id", ""): row for row in read_csv(output_root / "program_screening.csv")}
    expected_corrections = {
        "Vanderbilt final deadline": "2027-01-08" in programs.get("us:ipeds:221999:program:phd:computer-science-phd", {}).get("fall_2027_deadline", ""),
        "Virginia Tech standing policy": "Beginning with the Fall 2026" in programs.get("us:ipeds:233921:program:phd:computer-science-phd", {}).get("funding_status", ""),
        "Saskatchewan cycle label": programs.get("ca:dli:O19425660421:program:thesis-or-research-master-s:msc-in-computer-science-thesis", {}).get("fall_2027_deadline") == "Not yet published",
        "RIT GRE": programs.get("us:ipeds:195003:program:phd:computing-and-information-sciences-phd", {}).get("gre_policy", "").startswith("Required"),
        "UCI recurring deadline": "recurring" in programs.get("us:ipeds:110653:program:phd:software-engineering-phd", {}).get("fall_2027_deadline", "").lower(),
        "UIUC restored": programs.get("us:ipeds:145637:program:phd:computer-science-phd", {}).get("final_decision") == "Core",
        "NC State restored": programs.get("us:ipeds:199193:program:phd:computer-science-phd", {}).get("final_decision") == "Core",
        "Maryland reserve": programs.get("us:ipeds:163286:program:phd:computer-science-phd", {}).get("final_decision") == "Reserve",
        "Imperial immediate route excluded": programs.get("ror:041kmwe10:program:phd:phd-in-computing", {}).get("final_decision") == "Do Not Apply",
        "HMU false negative restored": programs.get("ror:039ce0m20:program:phd-requiring-a-master-s:electrical-and-computer-engineering-phd", {}).get("screening_decision") == "preliminary_fit",
    }
    unapplied = [name for name, passed in expected_corrections.items() if not passed]
    if unapplied:
        errors.append(f"independent-review corrections not applied: {unapplied}")
    checks["independent_review_corrections"] = expected_corrections

    drafts = read_csv(output_root / "outreach_drafts.csv")
    if len(drafts) != 15:
        errors.append(f"expected 15 first-wave drafts, found {len(drafts)}")
    if any(row.get("send_status", "").lower() not in {"", "not sent"} for row in drafts):
        errors.append("an outreach draft has a non-local send status")
    checks["first_wave_contacts"] = len(drafts)

    if require_workbook:
        workbook = output_root / "graduate_program_audit.xlsx"
        if not workbook.exists() or workbook.stat().st_size == 0:
            errors.append("workbook is missing or empty")
        renders = {path.name for path in (output_root / "renders").glob("*.png")}
        missing_renders = sorted(EXPECTED_SHEETS - renders)
        if missing_renders:
            errors.append(f"missing workbook renders: {missing_renders}")
        scan_path = output_root / "workbook_formula_error_scan.ndjson"
        scan_text = scan_path.read_text(encoding="utf-8") if scan_path.exists() else ""
        formula_errors = re.findall(r"#(?:REF!|DIV/0!|VALUE!|NAME\?|N/A)", scan_text)
        if formula_errors:
            errors.append(f"workbook formula-error scan found: {sorted(set(formula_errors))}")
        checks["workbook_bytes"] = workbook.stat().st_size if workbook.exists() else 0
        checks["workbook_renders"] = len(renders)
        checks["formula_error_matches"] = len(formula_errors)

    result = {"status": "PASS" if not errors else "FAIL", "errors": errors, "checks": checks}
    write_json(output_root / "final_validation.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--require-workbook", action="store_true")
    args = parser.parse_args()
    result = validate(Path(args.repo_root).resolve(), Path(args.output_dir).resolve(), args.require_workbook)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
