from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

WEIGHTS = {
    "professor_fit_score": 30,
    "faculty_depth_score": 15,
    "funding_score": 25,
    "eligibility_score": 15,
    "degree_admissions_score": 10,
    "application_economics_score": 5,
}

TRUE_VALUES = {True, 1, "1", "true", "yes", "y", "verified", "eligible", "credible"}


def _truthy(value: object) -> bool:
    return value if isinstance(value, bool) else str(value).strip().lower() in TRUE_VALUES


@dataclass(frozen=True)
class ScoreResult:
    research_fit_score: int
    overall_score: int
    recommendation: str
    gate_failures: tuple[str, ...]


def calculate_score(row: Mapping[str, object]) -> ScoreResult:
    components: dict[str, int] = {}
    for field, maximum in WEIGHTS.items():
        try:
            value = int(float(row.get(field, 0) or 0))
        except (TypeError, ValueError):
            value = 0
        if not 0 <= value <= maximum:
            raise ValueError(f"{field} must be between 0 and {maximum}; received {value}")
        components[field] = value

    gate_map = {
        "recognized_active_institution": row.get("recognized_active_institution"),
        "relevant_research_program": row.get("relevant_research_program"),
        "international_student_eligible": row.get("international_student_eligible"),
        "bachelor_entry_or_research_masters_route": row.get("bachelor_entry_or_research_masters_route"),
        "verified_professor_match": row.get("verified_professor_match"),
        "credible_funding_or_full_scholarship": row.get("credible_funding_or_full_scholarship"),
        "compatible_degree_structure": row.get("compatible_degree_structure"),
    }
    gate_failures = tuple(name for name, value in gate_map.items() if not _truthy(value))
    research_fit = components["professor_fit_score"] + components["faculty_depth_score"]
    overall = sum(components.values())

    if gate_failures or overall < 65:
        recommendation = "Do Not Apply"
    elif str(row.get("position_monitor_only", "")).lower() in {"true", "yes", "1"}:
        recommendation = "Monitor for 2027 Position"
    elif str(row.get("material_unresolved_gate", "")).lower() in {"true", "yes", "1"}:
        recommendation = "Outreach Before Decision"
    elif str(row.get("verification_status", "")).lower() in {"blocked", "contradictory", "incomplete"}:
        recommendation = "Investigate Further"
    elif overall >= 85 and _truthy(row.get("credible_funding_or_full_scholarship")):
        recommendation = "Strong Apply"
    elif overall >= 75:
        recommendation = "Likely Apply"
    else:
        recommendation = "Deprioritize"

    return ScoreResult(research_fit, overall, recommendation, gate_failures)
