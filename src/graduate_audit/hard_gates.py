from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from graduate_audit.evidence_scoring import funding_hard_gate_from_evidence

TRUE_VALUES = {True, 1, "1", "true", "yes", "verified", "eligible"}
VERIFIED_SUPERVISION_VALUES = {"true", "yes", "verified"}


def _truthy(value: object) -> bool:
    return value if isinstance(value, bool) else str(value or "").strip().lower() in TRUE_VALUES


def _verified_professor_key(row: Mapping[str, object]) -> str | None:
    can_supervise = str(row.get("can_supervise_program", "")).strip().lower()
    verification = str(row.get("verification_status", "")).strip().lower()
    if can_supervise not in VERIFIED_SUPERVISION_VALUES or verification != "verified":
        return None
    if not str(row.get("official_faculty_url", "")).strip():
        return None
    if not str(row.get("evidence_ids", "")).strip():
        return None
    return str(
        row.get("professor_id")
        or row.get("official_faculty_url")
        or row.get("full_name")
        or ""
    ).strip().lower() or None


@dataclass(frozen=True)
class HardGateResult:
    gates: dict[str, bool]
    failures: tuple[str, ...]
    distinct_verified_professor_count: int


def evaluate_hard_gates(
    program: Mapping[str, object],
    professors: Iterable[Mapping[str, object]],
    sources: Iterable[Mapping[str, object]] = (),
) -> HardGateResult:
    program_id = str(program.get("program_id", ""))
    professor_keys = {
        key
        for row in professors
        if str(row.get("program_id", "")) == program_id
        if (key := _verified_professor_key(row)) is not None
    }
    source_by_id = {
        str(row.get("stage3_source_id") or row.get("source_id") or ""): row
        for row in sources
        if str(row.get("stage3_source_id") or row.get("source_id") or "")
    }
    gates = {
        "recognized_active_institution": _truthy(program.get("recognized_active_institution")),
        "relevant_research_program": _truthy(program.get("relevant_research_program")),
        "international_student_eligible": _truthy(program.get("international_student_eligible")),
        "bachelor_entry_or_research_masters_route": _truthy(
            program.get("bachelor_entry_or_research_masters_route")
        ),
        "verified_professor_match": bool(professor_keys),
        "credible_funding_or_full_scholarship": funding_hard_gate_from_evidence(program, source_by_id),
        "compatible_degree_structure": _truthy(program.get("compatible_degree_structure")),
    }
    failures = tuple(name for name, passed in gates.items() if not passed)
    return HardGateResult(gates, failures, len(professor_keys))
