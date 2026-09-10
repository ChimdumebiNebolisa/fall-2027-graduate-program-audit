from __future__ import annotations

import argparse
import re
from pathlib import Path

from graduate_audit.io import read_csv, write_csv


CALENDAR_COLUMNS = (
    "existing_calendar_school", "previous_category", "survived_new_audit",
    "new_status", "change", "reason", "contradictory_calendar_instructions",
)


def _key(value: str) -> str:
    value = value.lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]", "", value)


ALIASES = {
    _key("Virginia Tech"): _key("Virginia Polytechnic Institute and State University"),
    _key("University of Nebraska-Lincoln"): _key("University of Nebraska-Lincoln"),
    _key("University of Texas Rio Grande Valley"): _key("The University of Texas Rio Grande Valley"),
    _key("University of Texas at San Antonio"): _key("The University of Texas at San Antonio"),
    _key("University of Texas at Arlington"): _key("The University of Texas at Arlington"),
}


def compare(calendar_path: Path, output_root: Path) -> list[dict[str, str]]:
    prior = read_csv(calendar_path)
    programs = read_csv(output_root / "program_screening.csv")
    portfolio_path = output_root / "portfolio.json"
    import json

    portfolio = json.loads(portfolio_path.read_text(encoding="utf-8")) if portfolio_path.exists() else {}
    portfolio_status: dict[str, str] = {}
    for category, label in (("core", "Core"), ("reserve", "Reserve"), ("monitor_for_2027_position", "Monitor")):
        for row in portfolio.get(category, []):
            portfolio_status.setdefault(_key(row.get("institution_name", "")), label)

    deep_by_name: dict[str, list[dict[str, str]]] = {}
    for row in programs:
        if row.get("verification_status", "").lower() in {"", "mechanical", "preliminary"} or not row.get("overall_score") or row.get("overall_score") == "0":
            continue
        deep_by_name.setdefault(_key(row.get("institution_name", "")), []).append(row)

    rows: list[dict[str, str]] = []
    for old in prior:
        original_key = _key(old.get("existing_calendar_school", ""))
        candidate_keys = {original_key, ALIASES.get(original_key, original_key)}
        status = next((portfolio_status[k] for k in candidate_keys if k in portfolio_status), "")
        deep = next((deep_by_name[k] for k in candidate_keys if k in deep_by_name), [])
        if status:
            best = max(deep, key=lambda row: int(float(row.get("overall_score") or 0)), default={})
            new_status = f"Survived — {status}"
            change = "Retained" if status in {"Core", "Reserve"} else "Reclassified"
            reason = best.get("biggest_risk") or best.get("unresolved_question") or "Passed hard gates at the recorded evidence date."
            survived = "Yes"
        elif deep:
            best = max(deep, key=lambda row: int(float(row.get("overall_score") or 0)))
            new_status = best.get("recommendation") or "Removed after deep review"
            change = "Downgraded or removed"
            reason = best.get("exclusion_reason") or best.get("biggest_risk") or best.get("unresolved_question") or "Did not clear the final evidence gates."
            survived = "No"
        else:
            new_status = "Not selected for deep review"
            change = "Removed from active portfolio"
            reason = "The independent universe/fit triage did not place this school above the final deep-review cutoff; this is not a claim that no relevant program exists."
            survived = "No"
        rows.append({
            "existing_calendar_school": old.get("existing_calendar_school", ""),
            "previous_category": old.get("previous_category", ""),
            "survived_new_audit": survived,
            "new_status": new_status,
            "change": change,
            "reason": reason,
            "contradictory_calendar_instructions": "Preserved as prior context; current source-backed audit controls the recommendation.",
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--calendar-summary", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = Path(args.output_dir)
    rows = compare(Path(args.calendar_summary), root)
    write_csv(root / "calendar_comparison.csv", rows, CALENDAR_COLUMNS)
    print(f"Wrote {len(rows)} Calendar comparison rows")


if __name__ == "__main__":
    main()
