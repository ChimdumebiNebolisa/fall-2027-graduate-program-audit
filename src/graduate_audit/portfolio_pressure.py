from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Mapping

from graduate_audit.evidence_scoring import COMPONENT_ORDER, split_ids
from graduate_audit.schema import PASS2_SCHEMA_VERSION

GENERATING_PROCESS = "graduate_audit.portfolio_pressure:v1"
CORE_MIN = 12
CORE_MAX = 16
CORE_PLAUSIBILITY = {"Competitive", "Plausible"}
STRETCH_PLAUSIBILITY = {"Reach", "Lottery", "Plausible to reach"}
ACTIVE_STATUSES = {"core", "reserve", "monitor"}

PRESSURE_QUESTIONS = (
    (1, "Is there at least one genuinely relevant research program?"),
    (2, "Are there current, verified professor matches?"),
    (3, "Is the department deeper than a single professor, or is that dependency worth the risk?"),
    (4, "Is funding credible for this applicant and degree type?"),
    (5, "Is the applicant formally eligible?"),
    (6, "What evidence supports the strategic plausibility category?"),
    (7, "Would the applicant prefer this opportunity over another already retained?"),
    (8, "Is the application fee and effort justified?"),
    (9, "Could one professor or administrator reply materially change the decision?"),
    (10, "What new evidence would cause the recommendation to change?"),
)


def _truthy(value: object) -> bool:
    return str(value or "").strip().casefold() in {"1", "true", "yes", "pass", "verified"}


def _score(row: Mapping[str, object]) -> int:
    try:
        return int(float(str(row.get("overall_score", "0") or "0")))
    except ValueError:
        return 0


def _all_hard_gates_pass(row: Mapping[str, object]) -> bool:
    return _truthy(row.get("all_hard_gates_pass"))


def _simultaneous_rules_verified(verification: Mapping[str, object]) -> bool:
    text = str(verification.get("simultaneous_application_rules", "")).strip().casefold()
    if not text or any(marker in text for marker in ("not verified", "unverified", "unknown", "unclear")):
        return False
    return any(
        marker in text
        for marker in (
            "separate program selections are possible",
            "simultaneous applications are allowed",
            "multiple applications are allowed",
            "may apply to multiple",
            "possible by program",
        )
    )


def _independently_compelling(row: Mapping[str, object], primary: Mapping[str, object]) -> bool:
    return (
        _all_hard_gates_pass(row)
        and _score(row) >= max(65, _score(primary) - 5)
        and int(str(row.get("professor_alignment_score", "0") or "0")) >= 20
        and int(str(row.get("funding_net_viability_score", "0") or "0")) >= 20
    )


def _funding_type(row: Mapping[str, object]) -> str:
    value = int(str(row.get("funding_net_viability_score", "0") or "0"))
    if value == 25:
        return "verified comprehensive support"
    if value == 20:
        return "verified support with material cost gaps"
    if value == 10:
        return "official evidence below hard-gate standard"
    return "no verified material support"


def assign_portfolio_statuses(
    scores: Iterable[Mapping[str, object]],
    verifications_by_program: Mapping[str, Mapping[str, object]],
    *,
    core_max: int = CORE_MAX,
) -> tuple[dict[str, dict[str, object]], dict[str, object]]:
    """Assign evidence-policy dispositions without inventing plausibility labels."""
    rows = [dict(row) for row in scores]
    by_institution: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_institution[str(row.get("institution_id", ""))].append(row)

    decisions: dict[str, dict[str, object]] = {}
    active_candidates: list[dict[str, object]] = []
    for institution_rows in by_institution.values():
        ranked = sorted(
            institution_rows,
            key=lambda row: (
                not _all_hard_gates_pass(row),
                -_score(row),
                str(row.get("program_id", "")),
            ),
        )
        primary = ranked[0]
        primary_id = str(primary["program_id"])
        for index, row in enumerate(ranked):
            program_id = str(row["program_id"])
            if not _all_hard_gates_pass(row):
                failures = split_ids(row.get("hard_gate_failures"))
                decisions[program_id] = {
                    "portfolio_status": "do_not_apply",
                    "is_primary_program": index == 0,
                    "second_program_rule_verified": False,
                    "selection_rationale": "Failed hard gates: " + ", ".join(failures) + ".",
                }
                continue
            if index == 0:
                active_candidates.append(row)
                decisions[program_id] = {
                    "portfolio_status": "pending",
                    "is_primary_program": True,
                    "second_program_rule_verified": False,
                    "selection_rationale": "Primary hard-gate-clearing program at this university.",
                }
                continue
            verification = verifications_by_program.get(program_id, {})
            second_verified = _simultaneous_rules_verified(verification)
            compelling = _independently_compelling(row, primary)
            if compelling and second_verified:
                active_candidates.append(row)
                decisions[program_id] = {
                    "portfolio_status": "pending",
                    "is_primary_program": False,
                    "second_program_rule_verified": True,
                    "selection_rationale": (
                        f"Independently compelling second program relative to {primary_id}; simultaneous-application rules are verified."
                    ),
                }
            else:
                decisions[program_id] = {
                    "portfolio_status": "not_retained_alternate",
                    "is_primary_program": False,
                    "second_program_rule_verified": second_verified,
                    "selection_rationale": (
                        "A second program is not retained because independent strength and verified simultaneous-application rules are not both established."
                    ),
                }

    stable: list[dict[str, object]] = []
    stretch: list[dict[str, object]] = []
    monitor: list[dict[str, object]] = []
    for row in active_candidates:
        plausibility = str(row.get("admission_plausibility", ""))
        if plausibility in CORE_PLAUSIBILITY:
            stable.append(row)
        elif plausibility in STRETCH_PLAUSIBILITY:
            stretch.append(row)
        else:
            monitor.append(row)

    ordering = lambda row: (-_score(row), str(row.get("program_id", "")))
    stable.sort(key=ordering)
    stretch.sort(key=ordering)
    monitor.sort(key=ordering)

    core = stable[:core_max]
    reserve = stable[core_max:]
    stretch_capacity = min(max(0, core_max - len(core)), len(core) // 2)
    stretch_in_core: list[dict[str, object]] = []
    lottery_count = 0
    for row in stretch:
        is_lottery = str(row.get("admission_plausibility", "")) == "Lottery"
        if len(stretch_in_core) < stretch_capacity and (not is_lottery or lottery_count < 1):
            stretch_in_core.append(row)
            lottery_count += int(is_lottery)
        else:
            reserve.append(row)
    core.extend(stretch_in_core)

    for row in core:
        decisions[str(row["program_id"])].update({
            "portfolio_status": "core",
            "selection_rationale": "Evidence-supported core selection within the 12–16 quality-first range.",
        })
    for row in reserve:
        decisions[str(row["program_id"])].update({
            "portfolio_status": "reserve",
            "selection_rationale": "Hard gates and strategic calibration pass, but core capacity or stretch limits place this program in reserve.",
        })
    for row in monitor:
        decisions[str(row["program_id"])].update({
            "portfolio_status": "monitor",
            "selection_rationale": (
                "All hard gates pass, but strategic admission evidence is insufficient; monitor until the uncertainty is resolved."
            ),
        })

    credible_core_candidates = len(stable) + len(stretch)
    return_to_discovery = len(core) < CORE_MIN
    policy_result = {
        "credible_core_candidates": credible_core_candidates,
        "core_count": len(core),
        "return_to_candidate_discovery": return_to_discovery,
        "return_reason": (
            f"Only {credible_core_candidates} hard-gate-clearing programs have an evidence-supported Competitive, Plausible, Reach, or Lottery calibration; fewer than {CORE_MIN} core applications are justified."
            if return_to_discovery
            else "The evidence supports a quality-first core within the working range."
        ),
    }
    return decisions, policy_result


def _component_evidence_ids(
    evidence_by_component: Mapping[str, Mapping[str, object]], *components: str
) -> list[str]:
    return [
        str(evidence_by_component[component]["score_evidence_id"])
        for component in components
        if component in evidence_by_component
    ]


def _pressure_test_answers(
    row: Mapping[str, object],
    decision: Mapping[str, object],
    evidence_by_component: Mapping[str, Mapping[str, object]],
) -> list[dict[str, object]]:
    status = str(decision["portfolio_status"])
    all_ids = _component_evidence_ids(evidence_by_component, *COMPONENT_ORDER)
    hard_pass = _all_hard_gates_pass(row)
    professor_pass = _truthy(row.get("professor_hard_gate"))
    funding_pass = _truthy(row.get("funding_hard_gate"))
    eligibility_pass = _truthy(row.get("eligibility_hard_gate"))
    degree_pass = _truthy(row.get("degree_structure_hard_gate"))
    depth = int(str(row.get("distinct_verified_strong_matches", "0") or "0"))
    plausibility = str(row.get("admission_plausibility", ""))
    plausibility_rationale = str(row.get("admission_plausibility_rationale", ""))
    failures = split_ids(row.get("hard_gate_failures"))

    if depth >= 2:
        depth_assessment = "pass"
        depth_answer = f"Yes—{depth} distinct verified strong matches provide department depth."
    elif depth == 1:
        depth_assessment = "risk"
        depth_answer = "No—only one verified strong professor is recorded. The dependency is not worth application commitment until current availability or a second match is verified."
    else:
        depth_assessment = "fail"
        depth_answer = "No—no verified strong professor depth is recorded."

    if status in {"core", "reserve"}:
        preference_answer = "Provisionally yes relative to lower-ranked retained options; the applicant's personal preference has not been directly verified."
        preference_assessment = "risk"
    elif status == "monitor":
        preference_answer = "Unresolved—the opportunity cannot displace an application-ready option until strategic plausibility and single-professor risk are resolved."
        preference_assessment = "unresolved"
    else:
        preference_answer = "No—a program that fails a hard gate should not displace a hard-gate-clearing option."
        preference_assessment = "fail"

    economics = int(str(row.get("application_economics_score", "0") or "0"))
    if status in {"core", "reserve"} and economics > 0:
        economics_answer = "Provisionally yes—the evidence supports applying, subject to the recorded fee or waiver caveat."
        economics_assessment = "pass" if economics == 5 else "risk"
    elif status == "monitor":
        economics_answer = "Not yet—do not incur the fee or effort until strategic admission evidence and the recorded program risks are resolved."
        economics_assessment = "unresolved"
    else:
        economics_answer = "No—the application fee and effort are not justified while a hard gate fails."
        economics_assessment = "fail"

    reply_targets = []
    if depth <= 1:
        reply_targets.append("a verified-fit professor confirming supervision availability or an additional current supervisor")
    if not funding_pass:
        reply_targets.append("a program administrator supplying direct program-wide funding terms")
    if not eligibility_pass:
        reply_targets.append("admissions confirming formal eligibility")
    if plausibility == "Insufficient evidence":
        reply_targets.append("the program supplying official cohort/selectivity or applicant-profile context")
    reply_answer = (
        "Yes—" + "; ".join(reply_targets) + " could materially change the disposition."
        if reply_targets
        else "No single reply is currently identified as sufficient to change the disposition."
    )

    if hard_pass:
        change_trigger = (
            "Verified strategic admission evidence, plus either a second verified strong professor or persuasive confirmation that the single-professor dependency is acceptable; offer-specific funding and fee gaps must also be resolved where recorded."
        )
    else:
        change_trigger = "Direct official evidence must resolve every failed hard gate (" + ", ".join(failures) + ") before reconsideration."

    specs = (
        (
            "pass" if degree_pass else "fail",
            "Yes—the exact research route and compatible degree structure are verified." if degree_pass else "No—the relevant research route or compatible degree structure is not verified.",
            ("degree_admissions_alignment",),
        ),
        (
            "pass" if professor_pass else "fail",
            "Yes—at least one current professor clears the appointment, supervision-authority, fit, and recent-work gates." if professor_pass else "No—no current professor clears every verification gate.",
            ("professor_alignment",),
        ),
        (depth_assessment, depth_answer, ("department_program_depth", "professor_alignment")),
        (
            "pass" if funding_pass else "fail",
            "Yes—direct official verified evidence clears the funding hard gate, with any net-cost gaps recorded separately." if funding_pass else "No—direct official evidence does not establish a credible package for this program and degree type.",
            ("funding_net_viability",),
        ),
        (
            "pass" if eligibility_pass else "fail",
            "Yes—formal eligibility clears the verified gate." if eligibility_pass else "No—formal eligibility is unresolved or fails the verified gate.",
            ("eligibility_credential_alignment",),
        ),
        (
            "unresolved" if plausibility == "Insufficient evidence" else ("fail" if plausibility in {"Eligibility concern", "Clearly ineligible"} else "pass"),
            f"Category: {plausibility}. {plausibility_rationale}",
            ("eligibility_credential_alignment", "degree_admissions_alignment"),
        ),
        (preference_assessment, preference_answer, COMPONENT_ORDER),
        (economics_assessment, economics_answer, ("application_economics", "funding_net_viability")),
        ("yes" if reply_targets else "no", reply_answer, COMPONENT_ORDER),
        ("actionable", change_trigger, COMPONENT_ORDER),
    )
    return [
        {
            "question_number": number,
            "question": question,
            "assessment": assessment,
            "answer": answer,
            "evidence_ids": _component_evidence_ids(evidence_by_component, *components) or all_ids,
        }
        for (number, question), (assessment, answer, components) in zip(PRESSURE_QUESTIONS, specs)
    ]


def _entry(
    row: Mapping[str, object],
    verification: Mapping[str, object],
    decision: Mapping[str, object],
    evidence_by_component: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    return {
        "institution_id": str(row.get("institution_id", "")),
        "institution_name": str(row.get("institution_name", "")),
        "program_id": str(row.get("program_id", "")),
        "program_name": str(row.get("program_name", "")),
        "degree_type": str(row.get("degree_type", "")),
        "region": str(row.get("region", "")),
        "official_program_url": str(row.get("official_program_url", "")),
        "portfolio_status": str(decision["portfolio_status"]),
        "is_primary_program": bool(decision["is_primary_program"]),
        "second_program_rule_verified": bool(decision["second_program_rule_verified"]),
        "overall_score": _score(row),
        "evidence_rank": str(row.get("evidence_rank", "")),
        "funding_type": _funding_type(row),
        "admission_plausibility": str(row.get("admission_plausibility", "")),
        "all_hard_gates_pass": _all_hard_gates_pass(row),
        "hard_gate_failures": list(split_ids(row.get("hard_gate_failures"))),
        "distinct_verified_strong_matches": int(str(row.get("distinct_verified_strong_matches", "0") or "0")),
        "application_fee": str(row.get("application_fee", "")),
        "fee_currency": str(row.get("fee_currency", "")),
        "simultaneous_application_rules": str(verification.get("simultaneous_application_rules", "")),
        "selection_rationale": str(decision["selection_rationale"]),
        "unresolved_conflicts": str(row.get("unresolved_conflicts", "")),
        "score_evidence_ids": list(split_ids(row.get("score_evidence_ids"))),
        "pressure_test_answers": _pressure_test_answers(row, decision, evidence_by_component),
    }


def _composition(entries: Iterable[Mapping[str, object]]) -> dict[str, object]:
    rows = list(entries)
    dimensions = {
        "by_degree_type": Counter(str(row["degree_type"]) for row in rows),
        "by_region": Counter(str(row["region"]) for row in rows),
        "by_funding_type": Counter(str(row["funding_type"]) for row in rows),
        "by_plausibility_category": Counter(str(row["admission_plausibility"]) for row in rows),
    }
    return {
        "total": len(rows),
        **{name: dict(sorted(values.items())) for name, values in dimensions.items()},
    }


def build_pressure_tested_portfolio(
    scores: Iterable[Mapping[str, object]],
    verifications: Iterable[Mapping[str, object]],
    score_evidence: Iterable[Mapping[str, object]],
    *,
    generated_at: str,
) -> dict[str, object]:
    score_rows = [dict(row) for row in scores]
    verification_by_program = {
        str(row.get("candidate_program_id", "")): row for row in verifications
    }
    evidence_by_program: dict[str, dict[str, Mapping[str, object]]] = defaultdict(dict)
    for row in score_evidence:
        evidence_by_program[str(row.get("program_id", ""))][str(row.get("component", ""))] = row

    decisions, policy_result = assign_portfolio_statuses(score_rows, verification_by_program)
    buckets: dict[str, list[dict[str, object]]] = {
        "core": [],
        "reserve": [],
        "monitor": [],
        "do_not_apply": [],
        "not_retained_alternates": [],
    }
    for row in score_rows:
        program_id = str(row["program_id"])
        decision = decisions[program_id]
        status = str(decision["portfolio_status"])
        bucket = "not_retained_alternates" if status == "not_retained_alternate" else status
        buckets[bucket].append(
            _entry(
                row,
                verification_by_program.get(program_id, {}),
                decision,
                evidence_by_program.get(program_id, {}),
            )
        )
    for rows in buckets.values():
        rows.sort(key=lambda row: (-int(row["overall_score"]), str(row["institution_name"]), str(row["program_id"])))

    active = buckets["core"] + buckets["reserve"] + buckets["monitor"]
    all_entries = [row for rows in buckets.values() for row in rows]
    return {
        "schema_version": PASS2_SCHEMA_VERSION,
        "portfolio_version": "pass2-stage6-v1",
        "generated_at": generated_at,
        "generated_by": GENERATING_PROCESS,
        "decision": "RETURN_TO_CANDIDATE_DISCOVERY" if policy_result["return_to_candidate_discovery"] else "PORTFOLIO_READY",
        "policy": {
            "core_working_range": {"minimum": CORE_MIN, "maximum": CORE_MAX, "quality_overrides_count": True},
            "normally_one_primary_program_per_university": True,
            "second_program_requires_independent_strength_and_verified_simultaneous_rules": True,
            "maximum_lottery_in_core": 1,
            "maximum_combined_lottery_and_reach_share": "one-third",
            "plausibility_labels_are_never_adjusted_for_balance": True,
        },
        "discovery_return": policy_result,
        "composition": {
            "active_portfolio": _composition(active),
            "all_program_dispositions": _composition(all_entries),
        },
        **buckets,
    }
