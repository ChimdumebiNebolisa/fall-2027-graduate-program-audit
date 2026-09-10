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


def select_portfolio(
    programs: list[dict[str, str]],
    core_max: int = 16,
    reserve_max: int | None = None,
) -> dict[str, object]:
    ranked = sorted(
        programs,
        key=lambda row: (_number(row.get("overall_score")), _number(row.get("research_fit_score")), _number(row.get("funding_score"))),
        reverse=True,
    )
    core: list[dict[str, str]] = []
    reserve: list[dict[str, str]] = []
    monitors: list[dict[str, str]] = []
    do_not_apply: list[dict[str, str]] = []
    alternates: list[dict[str, str]] = []
    used_institutions: set[str] = set()
    pending_stretch_institutions: set[str] = set()
    stretch_candidates: list[dict[str, str]] = []

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
        explicit_gate = row.get("all_hard_gates_pass", "").strip().lower()
        hard_gate_pass = explicit_gate == "true" if explicit_gate else not row.get("hard_gate_failures", "").strip()
        if not hard_gate_pass or recommendation == "Do Not Apply":
            do_not_apply.append(summary)
            continue
        if recommendation == "Monitor for 2027 Position" or row.get("admission_plausibility") in {
            "Insufficient evidence", "Eligibility concern", "Clearly ineligible"
        }:
            if row.get("institution_id", "") in used_institutions:
                alternates.append(summary)
                continue
            monitors.append(summary)
            used_institutions.add(row.get("institution_id", ""))
            continue
        if recommendation not in {"Strong Apply", "Likely Apply", "Outreach Before Decision"}:
            continue
        institution_id = row.get("institution_id", "")
        if institution_id in used_institutions or institution_id in pending_stretch_institutions:
            alternates.append(summary)
            continue
        is_stretch = row.get("admission_plausibility") in {"Reach", "Lottery", "Plausible to reach"}
        core_eligible = recommendation in {"Strong Apply", "Likely Apply"}
        if core_eligible and is_stretch:
            stretch_candidates.append(summary)
            pending_stretch_institutions.add(institution_id)
            continue
        if core_eligible and len(core) < core_max:
            core.append(summary)
            used_institutions.add(institution_id)
        elif reserve_max is None or len(reserve) < reserve_max:
            reserve.append(summary)
            used_institutions.add(institution_id)

    stretch_capacity = min(max(0, core_max - len(core)), len(core) // 2)
    lottery_count = 0
    for summary in stretch_candidates:
        is_lottery = summary["admission_plausibility"] == "Lottery"
        if len([row for row in core if row["admission_plausibility"] in {"Reach", "Lottery", "Plausible to reach"}]) < stretch_capacity and (not is_lottery or lottery_count < 1):
            core.append(summary)
            lottery_count += int(is_lottery)
        elif reserve_max is None or len(reserve) < reserve_max:
            reserve.append(summary)
        used_institutions.add(summary["institution_id"])

    return {
        "core": core,
        "reserve": reserve,
        "monitor_for_2027_position": monitors,
        "do_not_apply": do_not_apply,
        "not_retained_alternates": alternates,
        "rules": {
            "core_working_range": "12-16, never padded",
            "maximum_lottery_in_core": 1,
            "maximum_lottery_plus_reach_share": "one-third",
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
