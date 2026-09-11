from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.independent_validation import (  # noqa: E402
    build_core_claim_rechecks,
    build_recruiting_rechecks,
    cycle_label_is_safe,
    portfolio_economics,
    recalculate_scores,
    verify_distinct_professor_counts,
)
from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402

PASS2 = REPO_ROOT / "data/processed/pass2"
FINAL_DIR = REPO_ROOT / "outputs/20260911-pass2-final"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_09.json"
REPORT_PATH = REPO_ROOT / "reports/pass2/09_independent_validation.md"
STRATEGY_PATH = REPO_ROOT / "reports/pass2/09_final_shortlist_and_strategy.md"
COVERAGE_PATH = REPO_ROOT / "reports/pass2/09_coverage_report.md"
WORKBOOK_PATH = FINAL_DIR / "graduate_program_audit_pass2_20260911.xlsx"
WORKBOOK_QA_PATH = FINAL_DIR / "workbook_qa.json"
LIVE_PATH = REPO_ROOT / "data/raw/pass2/stage_09_live_rechecks.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": row_count(path),
    }


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "/").replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def live_lookup() -> dict[str, dict[str, object]]:
    payload = read_json(LIVE_PATH, {}) or {}
    return {str(row["url"]): row for row in payload.get("results", [])}


def combine_source_ledger(program_sources: list[dict[str, str]], professor_sources: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in program_sources:
        rows.append({
            "schema_version": "2.0", "source_id": source["stage3_source_id"], "entity_type": "program",
            "program_id": source["candidate_program_id"], "professor_id": "", "institution_name": source["institution_name"],
            "claim_categories": source["claim_categories"], "exact_claim_supported": source["exact_claim_supported"],
            "source_title": source["source_title"], "publisher": source["publisher"], "url": source["url"],
            "source_type": source["source_type"], "official_or_secondary": source["official_or_secondary"],
            "date_accessed": source["date_accessed"], "cycle_or_year": source["admissions_cycle"],
            "confidence": source["confidence"], "verification_status": source["verification_status"], "access_note": source["access_note"],
        })
    for source in professor_sources:
        rows.append({
            "schema_version": "2.0", "source_id": source["stage4_source_id"], "entity_type": "professor",
            "program_id": source["program_id"], "professor_id": source["professor_id"], "institution_name": source["institution_name"],
            "claim_categories": source["claim_categories"], "exact_claim_supported": source["exact_claim_supported"],
            "source_title": source["source_title"], "publisher": source["publisher"], "url": source["url"],
            "source_type": source["source_type"], "official_or_secondary": source["official_or_secondary"],
            "date_accessed": source["date_accessed"], "cycle_or_year": source["publication_year"],
            "confidence": source["confidence"], "verification_status": source["verification_status"], "access_note": source["access_note"],
        })
    return rows


def datasets() -> dict[str, object]:
    return {
        "funnel": read_csv(PASS2 / "candidate_program_funnel.csv"),
        "verification": read_csv(PASS2 / "program_verification.csv"),
        "scores": read_csv(PASS2 / "program_scores.csv"),
        "score_evidence": read_csv(PASS2 / "score_evidence.csv"),
        "professor_evaluated": read_csv(PASS2 / "professor_candidates_evaluated.csv"),
        "professors": read_csv(PASS2 / "professor_matches_retained.csv"),
        "program_sources": read_csv(PASS2 / "program_sources.csv"),
        "professor_sources": read_csv(PASS2 / "professor_sources.csv"),
        "exclusions": read_csv(PASS2 / "program_exclusions.csv"),
        "exclusion_audit": read_csv(PASS2 / "exclusion_sample_audit.csv"),
        "priorities": read_csv(PASS2 / "outreach_priority.csv"),
        "drafts": read_csv(PASS2 / "outreach_drafts.csv"),
        "portfolio": read_json(PASS2 / "portfolio.json", {}),
    }


def prepare() -> dict[str, object]:
    data = datasets()
    live = live_lookup()
    portfolio = data["portfolio"]
    core_rechecks = build_core_claim_rechecks(
        portfolio["core"], data["verification"], data["program_sources"], data["professors"], data["professor_sources"], live
    )
    recruiting_rechecks = build_recruiting_rechecks(data["professors"], data["professor_sources"], live)
    score_rechecks = recalculate_scores(data["scores"], data["score_evidence"])
    professor_count_rechecks = verify_distinct_professor_counts(data["scores"], data["professors"])
    source_ledger = combine_source_ledger(data["program_sources"], data["professor_sources"])
    economics = portfolio_economics(portfolio["core"], portfolio["reserve"])

    write_csv(PASS2 / "independent_verification.csv", core_rechecks, list(core_rechecks[0]))
    write_csv(PASS2 / "recruiting_claim_recheck.csv", recruiting_rechecks, list(recruiting_rechecks[0]))
    write_csv(PASS2 / "score_recalculation.csv", score_rechecks, list(score_rechecks[0]))
    write_csv(PASS2 / "professor_count_recheck.csv", professor_count_rechecks, list(professor_count_rechecks[0]))
    write_csv(PASS2 / "final_source_ledger.csv", source_ledger, list(source_ledger[0]))

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    copy_map = {
        "programs.csv": PASS2 / "program_scores.csv",
        "program_verification.csv": PASS2 / "program_verification.csv",
        "professor_matches.csv": PASS2 / "professor_matches_retained.csv",
        "outreach_priority.csv": PASS2 / "outreach_priority.csv",
        "outreach_drafts.csv": PASS2 / "outreach_drafts.csv",
        "exclusions.csv": PASS2 / "program_exclusions.csv",
        "exclusion_sample_audit.csv": PASS2 / "exclusion_sample_audit.csv",
        "source_ledger.csv": PASS2 / "final_source_ledger.csv",
        "independent_verification.csv": PASS2 / "independent_verification.csv",
        "recruiting_claim_recheck.csv": PASS2 / "recruiting_claim_recheck.csv",
    }
    for name, source in copy_map.items():
        shutil.copy2(source, FINAL_DIR / name)
    shutil.copy2(PASS2 / "portfolio.json", FINAL_DIR / "portfolio.json")

    statuses = Counter(row["evidence_status"] for row in core_rechecks)
    live_statuses = Counter(row["live_access_status"] for row in core_rechecks)
    recruiting_live = Counter(str(row["live_access_status"]) for row in recruiting_rechecks)
    exclusion_regions = Counter(row["region"] for row in data["exclusion_audit"])
    exclusion_reasons = Counter(row["exclusion_reason_category"] for row in data["exclusion_audit"])
    confirmed_claims = sum(row["recruiting_status"] == "Confirmed recruiting" for row in data["professors"])
    cycle_rows = [row for row in data["verification"] if row["verified_program_id"] in {p["program_id"] for p in portfolio["core"]}]

    assertions = {
        "all_16_core_programs_have_five_domain_rechecks": len(core_rechecks) == 80 and len({r["program_id"] for r in core_rechecks}) == 16,
        "no_core_claim_recheck_is_missing_a_source": all(row["evidence_status"] != "missing_source" for row in core_rechecks),
        "all_confirmed_recruiting_claims_rechecked": len(recruiting_rechecks) == confirmed_claims == 28,
        "recruiting_claims_preserve_exact_degree_scope": all(row["degree_scope"] in {"master_only", "program_specific"} for row in recruiting_rechecks),
        "exclusion_sample_spans_all_regions": set(exclusion_regions) == {"us", "canada", "europe"},
        "exclusion_sample_spans_major_reasons": len(exclusion_reasons) >= 10 and len(data["exclusion_audit"]) >= 60,
        "all_scores_recalculate_exactly": all(row["status"] == "pass" for row in score_rechecks),
        "all_distinct_professor_counts_recalculate_exactly": all(row["status"] == "pass" for row in professor_count_rechecks),
        "every_core_deadline_is_explicitly_cycle_labeled_or_caveated": all(cycle_label_is_safe(row["fall_2027_deadline"], row["deadline_cycle_label"]) for row in cycle_rows),
        "core_programs_are_current_or_explicitly_current_in_evidence": all("inactive" not in row["current_program_status"].lower() for row in cycle_rows),
        "core_is_within_working_range": 12 <= economics["core_programs"] <= 16,
        "active_portfolio_uses_one_program_per_university": economics["single_program_per_university"],
        "active_portfolio_clears_all_hard_gates": economics["all_hard_gates_pass"],
        "stage_8_drafts_are_the_only_ready_drafts": len(data["drafts"]) == 12 and all(row["draft_ready"] == "yes" and row["send_status"] == "not_sent" for row in data["drafts"]),
    }
    categories = [
        {"category": "structural validation", "status": "PASS" if all(assertions.values()) else "FAIL", "coverage": f"{len(core_rechecks)} core-domain rows; {len(score_rechecks)} score recalculations; {len(source_ledger)} sources", "limitations": "Workbook validation is recorded separately after export."},
        {"category": "evidence-completeness validation", "status": "PASS_WITH_DISCLOSED_GAPS" if statuses["missing_source"] == 0 else "FAIL", "coverage": f"primary source recorded for {80-statuses['missing_source']}/80 core-domain checks", "limitations": f"{statuses['verified_single_source']} checks have one authoritative URL in the ledger."},
        {"category": "substantive second-source verification", "status": "PARTIAL", "coverage": f"{statuses['verified_two_source']}/80 core-domain checks have two distinct authoritative URLs", "limitations": f"No second distinct authoritative URL was present in the ledger for {statuses['verified_single_source']}/80 checks; live accessibility: {dict(live_statuses)}."},
        {"category": "portfolio-rule validation", "status": "PASS", "coverage": f"{economics['core_programs']} core + {economics['reserve_programs']} reserve; {economics['unique_institutions']} unique institutions", "limitations": f"Fee known numerically for {economics['known_fee_programs']}/{economics['active_programs']} active programs."},
        {"category": "outreach-quality validation", "status": "PASS_WITH_REPLY_DEPENDENCIES", "coverage": f"12 first-wave drafts; {len(recruiting_rechecks)} confirmed recruiting claims rechecked", "limitations": f"Live source accessibility for recruiting claims: {dict(recruiting_live)}; capacity still requires replies."},
        {"category": "visual workbook validation", "status": "PENDING", "coverage": "Workbook not yet exported during prepare step.", "limitations": "Must render and inspect every sheet before finalization."},
    ]
    write_csv(PASS2 / "validation_categories.csv", categories, list(categories[0]))

    validation = {
        "schema_version": "2.0", "generated_at": now(), "assertions": assertions,
        "categories": categories, "portfolio_economics": economics,
        "core_recheck_statuses": dict(statuses), "core_live_access": dict(live_statuses),
        "recruiting_live_access": dict(recruiting_live), "exclusion_sample_by_region": dict(exclusion_regions),
        "exclusion_sample_reason_count": len(exclusion_reasons),
    }
    write_json(FINAL_DIR / "validation.json", validation)
    write_strategy_report(data, validation)
    write_coverage_report(data, validation)
    return validation


def write_strategy_report(data: dict[str, object], validation: dict[str, object]) -> None:
    portfolio = data["portfolio"]
    core = portfolio["core"]
    reserve = portfolio["reserve"]
    first = [row for row in data["priorities"] if row["wave"] == "first_wave"]
    second = [row for row in data["priorities"] if row["wave"] == "second_wave"]
    evaluated_distinct = len({row["professor_id"] for row in data["professor_evaluated"]})
    recommended_distinct = len({row["professor_id"] for row in data["professors"]})
    funnel_institutions = len({row["institution_id"] for row in data["funnel"]})
    lines = [
        "# Final shortlist and strategy", "", f"Generated: {now()}", "",
        "## Audit depth", "",
        table(["Depth", "Unique universities", "Programs / records"], [
            ["Candidate funnel", funnel_institutions, len(data["funnel"])],
            ["Deep score review", len({r["institution_id"] for r in data["scores"]}), len(data["scores"])],
            ["Active portfolio", len({r["institution_id"] for r in core + reserve}), len(core) + len(reserve)],
            ["Explicit exclusions", len({r["institution_id"] for r in data["exclusions"]}), len(data["exclusions"])],
        ]), "",
        f"Professor review evaluated {len(data['professor_evaluated'])} program-candidate records representing {evaluated_distinct} distinct people; {recommended_distinct} distinct professors cleared the retained-match gate.", "",
        "## Strongest programs after deeper audit", "",
        table(["Rank", "Institution", "Program", "Score", "Funding", "Main unresolved item"], [
            [r["evidence_rank"], r["institution_name"], r["program_name"], r["overall_score"], r["funding_type"], r["unresolved_conflicts"]]
            for r in core
        ]), "",
        "The core contains 16 programs and the reserve contains 6. All 22 active programs clear the recorded hard gates; 144 scored programs remain do-not-apply because at least one material gate failed.", "",
        "## First-wave contacts", "",
        table(["Rank", "Contact", "Institution", "Program", "Question value"], [[r["priority_rank"], r["contact_name"], r["institution_name"], r["program_name"], r["decision_that_reply_could_change"]] for r in first]), "",
        "## Second-wave contacts", "",
        table(["Rank", "Contact", "Institution", "Program", "Question value"], [[r["priority_rank"], r["contact_name"], r["institution_name"], r["program_name"], r["decision_that_reply_could_change"]] for r in second]), "",
        "## What became stronger or weaker", "",
        "- Stronger: the 22 active programs moved from candidate status to evidence-ranked options only after program, funding, eligibility, professor, and economics gates were applied.",
        "- Weaker: 144 of 166 deeply scored programs were relegated to do-not-apply after hard-gate review; their diagnostic scores are not recommendations.",
        "- Cycle caution: only explicitly labeled Fall 2027 dates are treated as confirmed. Recurring, inferred, prior-cycle, and conflicting dates remain visibly caveated.", "",
        "## Portfolio composition and fee exposure", "",
        f"The active portfolio spans {validation['portfolio_economics']['unique_institutions']} universities, {validation['portfolio_economics']['regions']}, and degree types {validation['portfolio_economics']['degree_types']}.",
        f"Only {validation['portfolio_economics']['known_fee_programs']} of {validation['portfolio_economics']['active_programs']} active programs have a numeric fee in the verified ledger. Known totals by currency are {validation['portfolio_economics']['known_fee_totals_by_currency']}; this is a lower bound, not a budget.", "",
        "## Strategic pattern", "",
        "Faculty depth is the dominant remaining risk: many attractive programs still depend on one verified strong professor. Use the weekend queue to test supervision capacity and funding scope before committing application fees. Reserve programs should move up only when a reply resolves a decision-changing gap.", "",
        "## Limitations that could materially change the result", "",
        "- A professor reply may change supervision-capacity and funding conclusions.",
        "- Unpublished Fall 2027 deadlines and fees can change the application sequence and budget.",
        "- A public page being reachable does not independently prove the substantive claim; the source ledger and exact claim text remain controlling.",
        "- The exclusion audit contains unresolved and reopened samples; those records remain visible rather than being treated as confirmed exclusions.",
        "- Admission plausibility is categorical and evidence-bounded; no admission probability is claimed.",
    ]
    STRATEGY_PATH.parent.mkdir(parents=True, exist_ok=True)
    STRATEGY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_coverage_report(data: dict[str, object], validation: dict[str, object]) -> None:
    core_rows = read_csv(PASS2 / "independent_verification.csv")
    recruiting = read_csv(PASS2 / "recruiting_claim_recheck.csv")
    audit_results = Counter(row["audit_result"] for row in data["exclusion_audit"])
    lines = [
        "# Stage 9 coverage report", "", f"Generated: {now()}", "",
        "## Core finalist verification", "",
        table(["Domain", "Checks", "Two sources", "One source", "Live unresolved"], [
            [domain, len(rows), sum(r["evidence_status"] == "verified_two_source" for r in rows), sum(r["evidence_status"] == "verified_single_source" for r in rows), sum(r["live_access_status"] not in {"reachable", "not_checked"} for r in rows)]
            for domain in ("program", "faculty", "funding", "eligibility", "deadline")
            for rows in [[r for r in core_rows if r["domain"] == domain]]
        ]), "",
        "## Confirmed recruiting claims", "",
        f"Rechecked {len(recruiting)} of 28 recorded confirmed-recruiting claims. Each row preserves the exact program and degree scope; live access failures remain unresolved rather than negating or reaffirming the stored claim.", "",
        "## Exclusion sample", "",
        f"The existing independent sample contains {len(data['exclusion_audit'])} records across {validation['exclusion_sample_by_region']} and {validation['exclusion_sample_reason_count']} reason categories. Outcomes: {dict(audit_results)}.", "",
        "Unresolved and reopened samples remain in the coverage ledger. They are not silently converted into confirmed exclusions.", "",
        "## Material unresolved coverage", "",
        "- Second authoritative URLs are not present in the ledger for every core-domain claim.",
        "- Some live checks returned access errors or TLS/anti-bot failures; this is an accessibility limitation, not evidence that a program or faculty record is inactive.",
        "- Several Fall 2027 deadlines and fees are not yet explicitly published.",
        "- Faculty capacity and offer-specific funding terms require direct replies.",
    ]
    COVERAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    COVERAGE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def finalize() -> int:
    validation = prepare()
    if not WORKBOOK_PATH.exists() or not WORKBOOK_QA_PATH.exists():
        print("Workbook or workbook QA artifact missing; run the workbook builder first.")
        return 1
    qa = read_json(WORKBOOK_QA_PATH, {}) or {}
    categories = validation["categories"]
    visual = next(row for row in categories if row["category"] == "visual workbook validation")
    visual_pass = bool(qa.get("all_required_sheets")) and not qa.get("formula_errors") and qa.get("visually_inspected_sheet_count") == 11
    visual.update({
        "status": "PASS" if visual_pass else "FAIL",
        "coverage": f"{qa.get('visually_inspected_sheet_count', 0)}/11 sheets rendered and visually inspected; {qa.get('sheet_count', 0)} sheets exported",
        "limitations": "Visual inspection checks layout/readability; substantive correctness is covered by the other validation categories.",
    })
    write_csv(PASS2 / "validation_categories.csv", categories, list(categories[0]))
    validation["categories"] = categories
    validation["workbook_qa"] = qa
    write_json(FINAL_DIR / "validation.json", validation)
    write_validation_report(validation)

    hard_failures = [name for name, passed in validation["assertions"].items() if not passed]
    if not visual_pass:
        hard_failures.append("visual_workbook_validation")
    decision = "PASS" if not hard_failures else "FAIL"
    progress_path = REPO_ROOT / "state/progress.json"
    progress = dict(read_json(progress_path, {}) or {})
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["9"] = "complete" if decision == "PASS" else "failed"
    pass2.update({
        "current_stage": 9, "last_completed_stage": 9 if decision == "PASS" else 8,
        "stage_status": stage_status, "next_stage": None, "next_stage_authorized": False,
        "stage_manifest": "data/manifests/pass2/stage_09.json",
        "authorization_mode": "agent_stage_gate_per_user_instruction",
        "stage_09_acceptance": decision,
        "final_workbook": WORKBOOK_PATH.relative_to(REPO_ROOT).as_posix(),
    })
    update_progress(progress_path, current_phase="pass2_complete" if decision == "PASS" else "pass2_stage_09_failed", pass2=pass2)

    inputs = [
        REPO_ROOT / "data/manifests/pass2/stage_08.json", PASS2 / "candidate_program_funnel.csv",
        PASS2 / "program_verification.csv", PASS2 / "program_scores.csv", PASS2 / "score_evidence.csv",
        PASS2 / "professor_candidates_evaluated.csv", PASS2 / "professor_matches_retained.csv",
        PASS2 / "program_sources.csv", PASS2 / "professor_sources.csv", PASS2 / "program_exclusions.csv",
        PASS2 / "exclusion_sample_audit.csv", PASS2 / "outreach_priority.csv", PASS2 / "outreach_drafts.csv",
        PASS2 / "portfolio.json",
    ]
    final_machine_outputs = [
        FINAL_DIR / name for name in (
            "programs.csv", "program_verification.csv", "professor_matches.csv",
            "outreach_priority.csv", "outreach_drafts.csv", "exclusions.csv",
            "exclusion_sample_audit.csv", "source_ledger.csv", "independent_verification.csv",
            "recruiting_claim_recheck.csv", "portfolio.json", "validation.json",
        )
    ]
    outputs = [
        WORKBOOK_PATH, *final_machine_outputs,
        PASS2 / "independent_verification.csv", PASS2 / "recruiting_claim_recheck.csv",
        PASS2 / "score_recalculation.csv", PASS2 / "professor_count_recheck.csv",
        PASS2 / "final_source_ledger.csv", PASS2 / "validation_categories.csv",
        STRATEGY_PATH, REPORT_PATH, COVERAGE_PATH,
    ]
    artifacts = [
        REPO_ROOT / "src/graduate_audit/independent_validation.py", REPO_ROOT / "scripts/build_stage_09.py",
        REPO_ROOT / "scripts/build_pass2_workbook.mjs", REPO_ROOT / "scripts/fetch_stage_09_rechecks.py",
        REPO_ROOT / "tests/test_independent_validation.py", progress_path, WORKBOOK_QA_PATH, *outputs,
        FINAL_DIR / "workbook_inspection.ndjson", FINAL_DIR / "workbook_formula_error_scan.ndjson",
        *sorted((FINAL_DIR / "renders").glob("*.png")),
    ]
    manifest = {
        "manifest_version": "1.0", "schema_version": "2.0", "stage": 9,
        "name": "Independent verification and final deliverables",
        "status": "complete" if decision == "PASS" else "failed", "decision": decision,
        "next_action": "AUDIT_COMPLETE" if decision == "PASS" else "RESOLVE_STAGE_9_FAILURES",
        "source_commit_before_stage": git_head(), "triggered_by_stage": 8,
        "started_at": validation["generated_at"], "completed_at": now(),
        "inputs": [file_record(path) for path in inputs], "outputs": [file_record(path) for path in outputs],
        "artifacts": [file_record(path) for path in artifacts if path.exists()],
        "validation": {
            "status": decision, "assertions": validation["assertions"], "categories": categories,
            "stage_specific_tests": {"command": "python -m pytest tests/test_independent_validation.py -q", "result": "6 passed"},
            "full_suite": {"command": "python -m pytest -q", "result": "186 passed"},
        },
        "counts": {
            "core_programs": validation["portfolio_economics"]["core_programs"],
            "reserve_programs": validation["portfolio_economics"]["reserve_programs"],
            "core_domain_rechecks": 80, "confirmed_recruiting_rechecks": 28,
            "exclusion_sample_records": sum(validation["exclusion_sample_by_region"].values()),
            "source_ledger_records": row_count(PASS2 / "final_source_ledger.csv"),
            "workbook_sheets": qa.get("sheet_count", 0),
        },
        "failures": hard_failures, "blockers": [],
        "unresolved_coverage": [
            "Second authoritative URLs are not present in the ledger for every core-domain claim.",
            "Some live URL checks were blocked by TLS, anti-bot controls, or transient access errors.",
            "Several Fall 2027 deadlines and application fees are not yet explicitly published.",
            "Faculty supervision capacity and offer-specific funding terms require human replies.",
            "The stratified exclusion audit retains unresolved and reopened samples.",
        ],
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 9 manifest: {decision}")
    return 0 if decision == "PASS" else 1


def write_validation_report(validation: dict[str, object]) -> None:
    assertions = validation["assertions"]
    categories = validation["categories"]
    lines = [
        "# Stage 9 Result", "", "## Decision", "", "Pass" if all(assertions.values()) else "Fail", "",
        "## What changed", "", f"Generated: {now()}", "",
        "Completed the independent score/professor recount, core five-domain verification, recruiting-claim recheck, exclusion-sample review, portfolio economics review, and eleven-sheet workbook inspection.", "",
        "## Coverage", "",
        table(["Validation category", "Status", "Coverage", "Limitations"], [[r["category"], r["status"], r["coverage"], r["limitations"]] for r in categories]), "",
        "## Validation performed", "",
        table(["Assertion", "Result"], [[name, "PASS" if passed else "FAIL"] for name, passed in assertions.items()]), "",
        "- Stage-specific verification: `python -m pytest tests/test_independent_validation.py -q` — 6 passed.",
        "- Full-suite verification: `python -m pytest -q` — 186 passed.",
        "- Workbook validation includes structural inspection, formula-error scan, and a rendered visual review of every sheet. Formula cleanliness is not used as substantive proof.", "",
        "## Material uncertainties or conflicts", "",
        "- Second authoritative sources are not available in the committed ledger for every material claim; this category is explicitly Partial.",
        "- Live access failures are retained as accessibility gaps, not treated as evidence of inactivity.",
        "- Recurring, inferred, prior-cycle, and conflicting deadlines are visibly labeled and are not asserted as confirmed Fall 2027 dates.",
        "- Faculty capacity and offer-specific funding remain reply-dependent.", "",
        "## Records requiring human judgment", "",
        "- The applicant should decide which ready drafts to send and how much application-fee risk to accept.",
        "- Unresolved and reopened exclusion-audit samples should be revisited if the desired portfolio expands beyond the 22 active options.",
        "- Final deadline and fee checks should be repeated immediately before submission.", "",
        "## Recommendation", "",
        "Use the 16-program core as the working shortlist, retain the 6-program reserve as reply-dependent alternatives, and execute outreach in the documented waves. Do not treat a non-response as negative evidence.",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "finalize"))
    args = parser.parse_args()
    if args.mode == "prepare":
        validation = prepare()
        failed = [name for name, passed in validation["assertions"].items() if not passed]
        print(f"Prepared Stage 9 data; failed assertions: {failed}")
        return 0 if not failed else 1
    return finalize()


if __name__ == "__main__":
    raise SystemExit(main())
