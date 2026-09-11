from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import yaml

from graduate_audit.schema import PASS2_SCHEMA_VERSION

GENERATING_PROCESS = "graduate_audit.evidence_scoring:v1"
COMPONENT_ORDER = (
    "professor_alignment",
    "department_program_depth",
    "funding_net_viability",
    "eligibility_credential_alignment",
    "degree_admissions_alignment",
    "application_economics",
)
OUTPUT_SCORE_FIELDS = {
    "professor_alignment": "professor_alignment_score",
    "department_program_depth": "department_program_depth_score",
    "funding_net_viability": "funding_net_viability_score",
    "eligibility_credential_alignment": "eligibility_credential_alignment_score",
    "degree_admissions_alignment": "degree_admissions_alignment_score",
    "application_economics": "application_economics_score",
}
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}
VERIFIED_OFFICIAL_SOURCE_STATUSES = {
    "verified",
    "official page checked",
    "opened/current",
    "opened; cycle limits recorded",
    "opened official page",
    "accessible or indexed official page",
    "official current guide checked",
}


@dataclass(frozen=True)
class ComponentResult:
    component: str
    score: int
    maximum: int
    anchor: str
    evidence_ids: tuple[str, ...]
    completeness: str
    confidence: str
    uncertainty: str
    verification_status: str


@dataclass(frozen=True)
class GateResult:
    funding: bool
    professor: bool
    eligibility: bool
    degree_structure: bool
    coursework_exception: bool

    @property
    def failures(self) -> tuple[str, ...]:
        values = {
            "funding": self.funding,
            "professor": self.professor,
            "eligibility": self.eligibility,
            "degree_structure": self.degree_structure,
            "coursework_exception": self.coursework_exception,
        }
        return tuple(name for name, passed in values.items() if not passed)

    @property
    def all_pass(self) -> bool:
        return not self.failures


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def split_ids(value: object) -> tuple[str, ...]:
    return tuple(dict.fromkeys(part.strip() for part in str(value or "").split("|") if part.strip()))


def load_rubric(path: str | Path) -> dict[str, object]:
    rubric = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if rubric.get("schema_version") != PASS2_SCHEMA_VERSION:
        raise ValueError("Stage 5 scoring rubric must use schema version 2.0")
    components = rubric.get("components", {})
    if tuple(components) != COMPONENT_ORDER:
        raise ValueError("Stage 5 rubric components are missing or out of canonical order")
    if sum(int(components[name]["weight"]) for name in COMPONENT_ORDER) != 100:
        raise ValueError("Stage 5 rubric weights must sum to 100")
    for name in COMPONENT_ORDER:
        weight = int(components[name]["weight"])
        anchors = components[name].get("anchors", [])
        scores = {int(anchor["score"]) for anchor in anchors}
        if not anchors or max(scores) != weight or min(scores) != 0:
            raise ValueError(f"{name} anchors must span 0..{weight}")
    return rubric


def anchor_description(rubric: Mapping[str, object], component: str, anchor_key: str) -> str:
    anchors = rubric["components"][component]["anchors"]  # type: ignore[index]
    for anchor in anchors:
        if anchor["key"] == anchor_key:
            return str(anchor["criterion"])
    raise KeyError(f"Unknown anchor {component}/{anchor_key}")


def _official_verified_funding_sources(
    program: Mapping[str, object], sources_by_id: Mapping[str, Mapping[str, object]]
) -> tuple[Mapping[str, object], ...]:
    valid = []
    program_id = str(program.get("candidate_program_id") or program.get("program_id") or "")
    reference_value = program.get("funding_source_ids") or program.get("funding_gate_evidence")
    for source_id in split_ids(reference_value):
        source = sources_by_id.get(source_id)
        if not source:
            continue
        categories = {
            part.strip().casefold()
            for part in str(source.get("claim_categories") or source.get("claim_type") or "").split("|")
        }
        source_program_id = str(source.get("candidate_program_id") or source.get("program_id") or "")
        verification_status = str(source.get("verification_status", "")).strip().casefold()
        source_verified = (
            verification_status in VERIFIED_OFFICIAL_SOURCE_STATUSES
            or verification_status.startswith("official indexed page content checked")
        )
        if (
            "funding" in categories
            and str(source.get("official_or_secondary", "")).casefold() == "official"
            and source_verified
            and source_program_id == program_id
        ):
            valid.append(source)
    return tuple(valid)


def funding_hard_gate_from_evidence(
    program: Mapping[str, object], sources_by_id: Mapping[str, Mapping[str, object]]
) -> bool:
    """Evaluate funding without reading labels, recommendations, or score fields."""
    sources = _official_verified_funding_sources(program, sources_by_id)
    if not sources:
        return False
    weak_markers = (
        "most doctoral", "most phds", "most phd", "typically", "selected",
        "may be offered", "may offer", "possible unfunded", "no funding guarantee",
        "lack of funding guarantee", "generally available", "competitive and cycle-specific",
        "does not provide a current", "availability is competitive", "non-guaranteed",
        "non guaranteed", "many ", "not all admits", "not promise it to all", "usually",
        "later funding patterns", "later funding is not", "later support expected",
        "not a guarantee", "distinction between", "nearly all", "majority",
        "not every", "not universal", "without a universal guarantee", "one-to-five-year",
    )
    credible_markers = (
        "guaranteed", "funding guarantee", "five-year package",
        "five years of full", "full tuition/health doctoral funding", "all full-time",
        "all phd students", "all cs phd admits", "all admitted phd students",
        "100% of admitted", "minimum is", "minimum guaranteed", "minimum funding",
        "take-home after tuition", "fully funded", "full support", "support commitment",
        "multi-year assistantship funding", "phd students receive support",
    )
    return any(
        not any(marker in claim for marker in weak_markers)
        and any(marker in claim for marker in credible_markers)
        for source in sources
        if (claim := str(source.get("exact_claim_supported", "")).casefold())
    )


def coursework_exception_gate_from_evidence(
    program: Mapping[str, object], sources_by_id: Mapping[str, Mapping[str, object]]
) -> bool:
    degree_type = str(program.get("degree_type", "")).casefold()
    research_requirement = str(program.get("research_requirement", "")).casefold()
    coursework_only = "coursework" in degree_type or "professional" in degree_type
    if not coursework_only:
        return True
    sources = _official_verified_funding_sources(program, sources_by_id)
    claims = " ".join(str(source.get("exact_claim_supported", "")) for source in sources).casefold()
    exceptional_scholarship = "full scholarship" in claims or "fully funded scholarship" in claims
    substantial_research = any(token in research_requirement for token in ("thesis", "dissertation", "substantial research"))
    return exceptional_scholarship and substantial_research


def professor_hard_gate(retained: Iterable[Mapping[str, object]]) -> bool:
    return any(
        str(row.get("verification_status", "")) == "verified_strong_match"
        and str(row.get("supervision_authority_status", "")).casefold() == "yes"
        and int(str(row.get("recent_work_evidence_count", "0") or "0")) >= 1
        and bool(str(row.get("recent_work_1_url", "")).strip())
        and bool(str(row.get("recent_work_1_year", "")).strip())
        for row in retained
    )


def _depth_score(count: int) -> tuple[int, str]:
    if count >= 3:
        return 15, "three_or_more_distinct"
    if count == 2:
        return 10, "two_distinct"
    if count == 1:
        return 5, "one_distinct"
    return 0, "none"


def _professor_score(count: int) -> tuple[int, str]:
    if count >= 3:
        return 30, "three_or_more_verified_strong"
    if count == 2:
        return 25, "two_verified_strong"
    if count == 1:
        return 20, "one_verified_strong"
    return 0, "no_verified_strong"


def _coverage_is_resolved(value: object) -> bool:
    text = str(value or "").casefold()
    unresolved = (
        "not verified", "not stated", "not itemized", "not fully", "not confirmed", "not guaranteed",
        "remaining", "partial", "may ", "verify", "confirm", "check offer", "separate net",
        "reduce", "excluded", "dependent",
    )
    return bool(text.strip()) and not any(marker in text for marker in unresolved)


def _funding_score(
    program: Mapping[str, object], sources_by_id: Mapping[str, Mapping[str, object]], gate: bool
) -> tuple[int, str, str, str, str]:
    valid_sources = _official_verified_funding_sources(program, sources_by_id)
    refs = tuple(str(source["stage3_source_id"]) for source in valid_sources)
    if gate:
        fields = (
            "funding_duration", "tuition_coverage", "mandatory_fee_coverage",
            "health_insurance_coverage", "summer_coverage",
        )
        complete = all(_coverage_is_resolved(program.get(field)) for field in fields)
        if complete:
            return 25, "verified_comprehensive_support", "complete", "high", ""
        unresolved = "One or more duration, tuition, fee, health, summer, or net-cost terms remain unresolved."
        return 20, "verified_support_with_cost_gaps", "partial", "medium", unresolved
    if refs:
        return (
            10,
            "documented_but_not_gate_credible",
            "partial",
            "low",
            "Official funding evidence exists but does not prove a credible program-wide package or full scholarship.",
        )
    return 0, "no_verified_material_support", "missing", "low", "No verified official material funding source is recorded."


def _credential_question(program: Mapping[str, object]) -> bool:
    text = " ".join(
        str(program.get(field, ""))
        for field in (
            "largest_unresolved_question", "minimum_gpa_application",
            "bachelors_entry_eligibility", "prerequisite_coursework",
        )
    ).casefold()
    markers = ("gpa", "transcript", "equival", "a-standing", "credential", "unclear", "exceptional")
    return any(marker in text for marker in markers)


def _eligibility_score(program: Mapping[str, object], refs: tuple[str, ...]) -> tuple[int, str, str, str, str]:
    gate = str(program.get("eligibility_gate", "")).casefold()
    if not refs:
        return 0, "ineligible_or_unverified", "missing", "low", "No official eligibility source is recorded."
    if gate == "pass":
        if _credential_question(program):
            return 10, "verified_with_material_question", "partial", "medium", str(program.get("largest_unresolved_question", ""))
        return 15, "verified_alignment", "complete", "high", ""
    if gate == "resolvable_question":
        return 5, "resolvable_eligibility_question", "partial", "low", str(program.get("largest_unresolved_question", ""))
    return 0, "ineligible_or_unverified", "missing", "low", str(program.get("largest_unresolved_question", ""))


def _degree_score(program: Mapping[str, object], refs: tuple[str, ...], coursework_gate: bool) -> tuple[int, str, str, str, str]:
    if not refs or str(program.get("degree_structure_gate", "")).casefold() != "pass" or not coursework_gate:
        return 0, "incompatible_or_coursework_only", "missing", "low", "Research degree structure is incompatible or not verified."
    text = " ".join(
        str(program.get(field, ""))
        for field in ("bachelors_entry_eligibility", "admissions_model", "largest_unresolved_question")
    ).casefold()
    material_question = any(token in text for token in ("unclear", "exceptional", "supervisor-gated", "supervisor required", "supervisor agreement required"))
    if material_question:
        return 5, "compatible_but_supervisor_or_entry_question", "partial", "medium", str(program.get("largest_unresolved_question", ""))
    return 10, "verified_compatible_route", "complete", "high", ""


def _application_fee_number(value: object) -> float | None:
    text = str(value or "")
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def _economics_score(program: Mapping[str, object], refs: tuple[str, ...]) -> tuple[int, str, str, str, str]:
    if not refs:
        return 0, "high_or_unverified_cost", "missing", "low", "No official fee/waiver evidence is recorded."
    fee = _application_fee_number(program.get("application_fee"))
    waiver = str(program.get("fee_waiver_rules", "")).casefold()
    if fee == 0 or "application is free" in waiver or "fee is waived" in waiver or "automatic" in waiver:
        return 5, "no_fee_or_verified_waiver", "complete", "high", ""
    if (fee is not None and fee <= 100) or any(token in waiver for token in ("may ask", "may be requested", "limited waiver", "waiver path")):
        return 3, "moderate_fee_or_possible_waiver", "partial", "medium", "Applicable waiver or final Fall 2027 cost is not guaranteed."
    return 0, "high_or_unverified_cost", "partial" if fee is not None else "missing", "low", "Fee is high or the applicable Fall 2027 amount/waiver remains unverified."


def calibrate_admission(
    program: Mapping[str, object], official_sources: Iterable[Mapping[str, object]], eligibility_gate: bool
) -> tuple[str, str]:
    if not eligibility_gate:
        return "Eligibility concern", str(program.get("largest_unresolved_question", "")) or "Formal eligibility remains unresolved."
    strategic_text = " ".join(str(source.get("exact_claim_supported", "")) for source in official_sources).casefold()
    strategic_markers = ("admit rate", "acceptance rate", "cohort profile", "applications received", "selectivity")
    if not any(marker in strategic_text for marker in strategic_markers):
        return (
            "Insufficient evidence",
            "Published minimums and formal eligibility do not calibrate admission chances; no official cohort/selectivity evidence is recorded.",
        )
    return (
        "Insufficient evidence",
        "Official strategic evidence is present but does not support a calibrated category from the current structured record.",
    )


def score_program(
    program: Mapping[str, object],
    evaluated_candidates: list[Mapping[str, object]],
    retained_matches: list[Mapping[str, object]],
    sources_by_id: Mapping[str, Mapping[str, object]],
    profile: Mapping[str, object],
    rubric: Mapping[str, object],
    calculated_at: str,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    distinct_matches = {
        str(row.get("professor_id", ""))
        for row in retained_matches
        if str(row.get("verification_status", "")) == "verified_strong_match"
        and str(row.get("supervision_authority_status", "")).casefold() == "yes"
        and int(str(row.get("recent_work_evidence_count", "0") or "0")) >= 1
    }
    match_count = len(distinct_matches)
    professor_refs = tuple(dict.fromkeys(
        ref for row in (retained_matches or evaluated_candidates) for ref in split_ids(row.get("source_ids"))
    ))
    program_refs = split_ids(program.get("program_source_ids"))
    admissions_refs = split_ids(program.get("admissions_source_ids"))
    eligibility_refs = tuple(dict.fromkeys(program_refs + admissions_refs))
    economics_refs = tuple(dict.fromkeys(admissions_refs + program_refs))
    funding_refs = tuple(
        str(source["stage3_source_id"])
        for source in _official_verified_funding_sources(program, sources_by_id)
    )

    funding_gate = funding_hard_gate_from_evidence(program, sources_by_id)
    coursework_gate = coursework_exception_gate_from_evidence(program, sources_by_id)
    professor_gate = professor_hard_gate(retained_matches)
    eligibility_gate = str(program.get("eligibility_gate", "")).casefold() == "pass"
    degree_gate = str(program.get("degree_structure_gate", "")).casefold() == "pass"
    gates = GateResult(funding_gate, professor_gate, eligibility_gate, degree_gate, coursework_gate)

    professor_value, professor_anchor = _professor_score(match_count)
    depth_value, depth_anchor = _depth_score(match_count)
    funding_value, funding_anchor, funding_complete, funding_confidence, funding_uncertainty = _funding_score(program, sources_by_id, funding_gate)
    eligibility_value, eligibility_anchor, eligibility_complete, eligibility_confidence, eligibility_uncertainty = _eligibility_score(program, eligibility_refs)
    degree_value, degree_anchor, degree_complete, degree_confidence, degree_uncertainty = _degree_score(program, eligibility_refs, coursework_gate)
    economics_value, economics_anchor, economics_complete, economics_confidence, economics_uncertainty = _economics_score(program, economics_refs)

    professor_uncertainty = "" if match_count else "No candidate clears every Stage 4 professor evidence gate."
    components = [
        ComponentResult("professor_alignment", professor_value, 30, professor_anchor, professor_refs, "complete" if match_count else "partial", "high" if match_count else "low", professor_uncertainty, "verified_calculation" if match_count else "partial_evidence_calculation"),
        ComponentResult("department_program_depth", depth_value, 15, depth_anchor, professor_refs, "complete", "high", "Single-professor dependency." if match_count == 1 else ("No verified department depth." if match_count == 0 else ""), "verified_calculation"),
        ComponentResult("funding_net_viability", funding_value, 25, funding_anchor, funding_refs, funding_complete, funding_confidence, funding_uncertainty, "verified_calculation" if funding_gate else "partial_evidence_calculation"),
        ComponentResult("eligibility_credential_alignment", eligibility_value, 15, eligibility_anchor, eligibility_refs, eligibility_complete, eligibility_confidence, eligibility_uncertainty, "verified_calculation" if eligibility_value > 0 else "partial_evidence_calculation"),
        ComponentResult("degree_admissions_alignment", degree_value, 10, degree_anchor, eligibility_refs, degree_complete, degree_confidence, degree_uncertainty, "verified_calculation" if degree_value > 0 else "partial_evidence_calculation"),
        ComponentResult("application_economics", economics_value, 5, economics_anchor, economics_refs, economics_complete, economics_confidence, economics_uncertainty, "verified_calculation" if economics_value > 0 else "partial_evidence_calculation"),
    ]
    evidence_rows: list[dict[str, str]] = []
    for component in components:
        if component.score > 0 and not component.evidence_ids:
            raise ValueError(f"Positive score lacks evidence: {program['candidate_program_id']} / {component.component}")
        evidence_rows.append({
            "schema_version": PASS2_SCHEMA_VERSION,
            "score_evidence_id": stable_id("scoreev", str(program["candidate_program_id"]), component.component),
            "program_id": str(program["candidate_program_id"]),
            "institution_id": str(program["institution_id"]),
            "institution_name": str(program["institution_name"]),
            "component": component.component,
            "component_score": str(component.score),
            "max_score": str(component.maximum),
            "rubric_anchor": component.anchor,
            "rubric_anchor_description": anchor_description(rubric, component.component, component.anchor),
            "supporting_evidence_ids": "|".join(component.evidence_ids),
            "evidence_completeness": component.completeness,
            "score_confidence": component.confidence,
            "uncertainty_or_conflict": component.uncertainty,
            "reviewer_or_generating_process": GENERATING_PROCESS,
            "verification_status": component.verification_status,
            "calculated_at": calculated_at,
        })

    official_program_sources = [sources_by_id[ref] for ref in eligibility_refs if ref in sources_by_id]
    plausibility, plausibility_rationale = calibrate_admission(program, official_program_sources, eligibility_gate)
    overall = sum(component.score for component in components)
    lowest_confidence = min((component.confidence for component in components), key=CONFIDENCE_ORDER.get)
    incomplete = [component.component for component in components if component.completeness != "complete"]
    score_evidence_ids = tuple(row["score_evidence_id"] for row in evidence_rows)
    component_pattern = "|".join(f"{component.component}:{component.score}/{component.maximum}" for component in components)
    row = {
        "schema_version": PASS2_SCHEMA_VERSION,
        "evidence_rank": "",
        "score_band": "80-100" if overall >= 80 else ("65-79" if overall >= 65 else ("50-64" if overall >= 50 else "0-49")),
        "program_id": str(program["candidate_program_id"]),
        "institution_id": str(program["institution_id"]),
        "institution_name": str(program["institution_name"]),
        "country": str(program["country"]),
        "region": str(program["region"]),
        "program_name": str(program["exact_degree_program_name"]),
        "degree_type": str(program["degree_type"]),
        "official_program_url": str(program["official_program_url"]),
        "stage3_verification_status": str(program["verification_status"]),
        "professor_alignment_score": str(professor_value),
        "department_program_depth_score": str(depth_value),
        "funding_net_viability_score": str(funding_value),
        "eligibility_credential_alignment_score": str(eligibility_value),
        "degree_admissions_alignment_score": str(degree_value),
        "application_economics_score": str(economics_value),
        "overall_score": str(overall),
        "component_score_pattern": component_pattern,
        "funding_hard_gate": str(funding_gate).lower(),
        "professor_hard_gate": str(professor_gate).lower(),
        "eligibility_hard_gate": str(eligibility_gate).lower(),
        "degree_structure_hard_gate": str(degree_gate).lower(),
        "coursework_exception_gate": str(coursework_gate).lower(),
        "all_hard_gates_pass": str(gates.all_pass).lower(),
        "hard_gate_failures": "|".join(gates.failures),
        "distinct_verified_strong_matches": str(match_count),
        "faculty_depth_points": str(depth_value),
        "single_professor_dependency": str(match_count == 1).lower(),
        "funding_status": str(program["funding_status"]),
        "application_fee": str(program["application_fee"]),
        "fee_currency": str(program["fee_currency"]),
        "admission_plausibility": plausibility,
        "admission_plausibility_rationale": plausibility_rationale,
        "published_minimum_gpa": str(program["minimum_gpa"]),
        "applicant_cumulative_gpa": str(profile["cumulative_gpa"]),
        "applicant_recent_two_year_gpa": str(profile["recent_two_year_gpa"]),
        "admission_probability": "",
        "evidence_completeness": "complete" if not incomplete else "partial",
        "score_confidence": lowest_confidence,
        "unresolved_conflicts": " | ".join(dict.fromkeys(filter(None, [str(program.get("largest_unresolved_question", ""))] + [component.uncertainty for component in components]))),
        "ranking_status": "eligible_for_evidence_ranking" if gates.all_pass else "gated_out; diagnostic score only",
        "score_evidence_ids": "|".join(score_evidence_ids),
        "generated_by": GENERATING_PROCESS,
        "scored_at": calculated_at,
    }
    return row, evidence_rows
