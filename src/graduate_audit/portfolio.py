from __future__ import annotations

import argparse
import json
from pathlib import Path

from graduate_audit.hard_gates import evaluate_hard_gates
from graduate_audit.io import read_csv, write_csv, write_json
from graduate_audit.schema import PASS2_SCHEMA_VERSION, PROGRAM_COLUMNS_V2
from graduate_audit.scoring import calculate_score

def _number(value: object) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def score_programs(
    program_path: Path,
    institution_path: Path,
    professor_path: Path,
    source_path: Path | None = None,
) -> list[dict[str, str]]:
    programs = read_csv(program_path)
    institution_ids = {row["institution_id"] for row in read_csv(institution_path)}
    professors = read_csv(professor_path)
    sources = read_csv(source_path) if source_path and source_path.exists() else []
    if any(row.get("schema_version") != PASS2_SCHEMA_VERSION for row in programs):
        raise ValueError(
            "score_programs requires Pass 2 schema 2.0 evidence; migrate legacy rows before rescoring"
        )

    for row in programs:
        if row.get("institution_id", "") not in institution_ids:
            raise ValueError(f"program references unknown institution: {row.get('institution_id')}")
        verification = row.get("verification_status", "").strip().lower()
        screening = row.get("screening_decision", "").strip().lower()
        gates = evaluate_hard_gates(row, professors, sources)
        evidence = {
            **row,
            **gates.gates,
            "position_monitor_only": row.get("recommendation") == "Monitor for 2027 Position",
            "material_unresolved_gate": bool(row.get("unresolved_conflicts")),
            "verification_status": verification,
        }
        result = calculate_score(evidence)
        row["research_fit_score"] = str(result.research_fit_score)
        row["overall_score"] = str(result.overall_score)
        if screening == "retained" or not row.get("recommendation"):
            row["recommendation"] = result.recommendation
        row["distinct_verified_professor_count"] = str(gates.distinct_verified_professor_count)
        row["hard_gate_failures"] = "|".join(result.gate_failures)
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
        root / "source_ledger.csv",
    )
    write_csv(root / "program_screening.csv", programs, PROGRAM_COLUMNS_V2)
    portfolio = select_portfolio(programs)
    write_json(root / "portfolio.json", portfolio)
    print(json.dumps({key: len(value) for key, value in portfolio.items() if isinstance(value, list)}, indent=2))


if __name__ == "__main__":
    main()
