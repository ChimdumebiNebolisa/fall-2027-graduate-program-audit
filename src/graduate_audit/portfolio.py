from __future__ import annotations

import argparse
import json
from pathlib import Path

from graduate_audit.io import read_csv, write_csv, write_json
from graduate_audit.schema import PROGRAM_COLUMNS
from graduate_audit.scoring import calculate_score

YES = {"yes", "true", "verified", "eligible", "1"}
CREDIBLE_FUNDING = {
    "verified", "guaranteed", "normally funded", "normally_funded_not_guaranteed",
    "guaranteed_all_admitted", "position salary", "position_salary", "full scholarship",
}
COMPATIBLE_DEGREES = {
    "PhD", "Direct-entry PhD", "Integrated or structured doctorate",
    "Thesis or research master's", "Project-based master's with substantial research",
}


def _yes(value: object) -> bool:
    normalized = str(value or "").strip().lower()
    return normalized in YES or normalized.startswith(("yes;", "yes —", "yes -", "verified;"))


def _credible_funding(value: object) -> bool:
    normalized = str(value or "").strip().lower()
    return normalized in CREDIBLE_FUNDING or any(
        token in normalized
        for token in ("normally funded", "guaranteed", "full tuition and stipend", "position salary")
    )


def _number(value: object) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _recognized_active(institution: dict[str, str]) -> bool:
    recognition = institution.get("recognition_status", "").lower()
    source_database = institution.get("source_database", "").lower()
    active = institution.get("active_status", "").lower()
    registry_evidence = any(
        token in recognition or token in source_database
        for token in ("recognized", "accredited", "official", "ipeds", "cicic", "ircc")
    )
    return registry_evidence and any(token in active for token in ("active", "current", "yes"))


def score_programs(program_path: Path, institution_path: Path, professor_path: Path) -> list[dict[str, str]]:
    programs = read_csv(program_path)
    institutions = {row["institution_id"]: row for row in read_csv(institution_path)}
    professors = read_csv(professor_path)
    supervisor_programs = {
        row.get("program_id", "")
        for row in professors
        if _yes(row.get("can_supervise_program"))
        and any(
            token in row.get("verification_status", "").lower()
            for token in ("verified", "complete", "official")
        )
    }

    for row in programs:
        institution = institutions.get(row.get("institution_id", ""), {})
        degree = row.get("degree_type", "")
        funding = row.get("funding_status", "").strip().lower()
        verification = row.get("verification_status", "").strip().lower()
        screening = row.get("screening_decision", "").strip().lower()
        evidence = {
            **row,
            "recognized_active_institution": _recognized_active(institution),
            "relevant_research_program": _number(row.get("research_fit_score")) > 0 and screening not in {"excluded", "screened_out"},
            "bachelor_entry_or_research_masters_route": _yes(row.get("direct_from_bachelors_eligible")),
            "verified_professor_match": row.get("program_id", "") in supervisor_programs,
            "credible_funding_or_full_scholarship": _credible_funding(funding),
            "compatible_degree_structure": degree in COMPATIBLE_DEGREES,
            "position_monitor_only": row.get("recommendation") == "Monitor for 2027 Position",
            "material_unresolved_gate": row.get("recommendation") == "Outreach Before Decision",
            "verification_status": verification,
        }
        result = calculate_score(evidence)
        row["research_fit_score"] = str(result.research_fit_score)
        row["overall_score"] = str(result.overall_score)
        if not row.get("recommendation") or row["recommendation"] in {"Strong Apply", "Likely Apply", "Deprioritize", "Do Not Apply"}:
            row["recommendation"] = result.recommendation
        if result.gate_failures:
            failure_text = ", ".join(result.gate_failures)
            row["notes"] = "; ".join(part for part in [row.get("notes", ""), f"Hard-gate failures: {failure_text}"] if part)
    return programs


def select_portfolio(programs: list[dict[str, str]], core_max: int = 20, reserve_max: int = 10) -> dict[str, object]:
    ranked = sorted(
        programs,
        key=lambda row: (_number(row.get("overall_score")), _number(row.get("research_fit_score")), _number(row.get("funding_score"))),
        reverse=True,
    )
    core: list[dict[str, str]] = []
    reserve: list[dict[str, str]] = []
    monitors: list[dict[str, str]] = []
    used_institutions: set[str] = set()
    reach_count = 0

    for row in ranked:
        recommendation = row.get("recommendation", "")
        summary = {
            "institution_id": row.get("institution_id", ""),
            "institution_name": row.get("institution_name", ""),
            "program_id": row.get("program_id", ""),
            "program_name": row.get("program_name", ""),
            "degree_type": row.get("degree_type", ""),
            "overall_score": _number(row.get("overall_score")),
            "research_fit_score": _number(row.get("research_fit_score")),
            "funding_score": _number(row.get("funding_score")),
            "admission_plausibility": row.get("admission_plausibility", ""),
            "recommendation": recommendation,
            "biggest_risk": row.get("biggest_risk", ""),
            "unresolved_question": row.get("unresolved_question", ""),
        }
        if recommendation == "Monitor for 2027 Position":
            monitors.append(summary)
            continue
        if recommendation not in {"Strong Apply", "Likely Apply", "Outreach Before Decision"}:
            continue
        institution_id = row.get("institution_id", "")
        is_reach = row.get("admission_plausibility") == "Reach"
        core_eligible = recommendation in {"Strong Apply", "Likely Apply"}
        if core_eligible and institution_id not in used_institutions and len(core) < core_max and (not is_reach or reach_count < 5):
            core.append(summary)
            used_institutions.add(institution_id)
            reach_count += int(is_reach)
        elif len(reserve) < reserve_max:
            reserve.append(summary)

    return {
        "core": core,
        "reserve": reserve,
        "monitor_for_2027_position": monitors,
        "rules": {
            "core_target": "18-20, never padded",
            "maximum_reach_in_core": 5,
            "normally_one_program_per_institution": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = Path(args.output_dir)
    programs = score_programs(
        root / "program_screening.csv",
        root / "institution_universe.csv",
        root / "professor_evidence.csv",
    )
    write_csv(root / "program_screening.csv", programs, PROGRAM_COLUMNS)
    portfolio = select_portfolio(programs)
    write_json(root / "portfolio.json", portfolio)
    print(json.dumps({key: len(value) for key, value in portfolio.items() if isinstance(value, list)}, indent=2))


if __name__ == "__main__":
    main()

