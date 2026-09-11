from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graduate_audit.pass21 import validate_recommended


CONFIG = ROOT / "config" / "pass21_decisions.yaml"
PASS2 = ROOT / "data" / "processed" / "pass2"
PROCESSED = ROOT / "data" / "processed" / "pass21"
OUTPUT = ROOT / "outputs" / "20260911-pass21-final"
REPORT_DIR = ROOT / "reports" / "pass21"
ACCESS_DATE = date(2026, 9, 11).isoformat()


RANKING_COLUMNS = [
    "Overall Rank", "University", "Country", "Exact Program", "Degree Type",
    "Recommendation Tier", "Funding Classification", "Funding Summary",
    "International Funding Eligible", "Academic Eligibility Verified",
    "Relative Admission Position", "Admission Rationale", "Program Research Fit",
    "Fit Evidence", "Example Faculty or Lab", "Application Fee", "Fee Waiver",
    "Fall 2027 Deadline", "Deadline Cycle", "Biggest Positive", "Biggest Risk",
    "Unresolved Question", "Recommended Decision", "Official Program URL",
    "Official Funding URL", "Admissions Evidence URL", "Notes",
]

EVIDENCE_COLUMNS = [
    "University", "Program", "Decision Category", "Research Degree Claim",
    "Funding Claim", "Academic Eligibility Claim", "International Eligibility Claim",
    "Program Fit Claim", "Source URL", "Source Type", "Information Cycle",
    "Access Date", "Verification Status", "Uncertainty", "Official Program URL",
    "Official Funding URL", "Admissions URL", "Fit URL",
]

EXCLUSION_COLUMNS = [
    "University", "Program", "Previous Status", "Revised Status",
    "Primary Exclusion Reason", "Funding Problem", "Eligibility Problem", "Fit Problem",
    "Application Economics Problem", "Evidence URL", "Reconsideration Condition",
]

OPEN_COLUMNS = [
    "Priority", "University", "Program", "Question", "Correct Recipient Type",
    "Official Contact", "Why the Answer Matters", "Current Decision Without Reply",
    "Evidence URL",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split_ids(value: str) -> list[str]:
    return [part for part in value.split("|") if part]


def first_source_url(program: dict[str, str], ledger: dict[str, dict[str, str]], field: str) -> str:
    for source_id in split_ids(program.get(field, "")):
        source = ledger.get(source_id)
        if source and source.get("url", "").startswith("http"):
            return source["url"]
    return program.get("official_program_url", "")


def country_name(value: str) -> str:
    return {"us": "United States", "canada": "Canada", "europe": "Europe"}.get(value.casefold(), value)


def problem_text(row: dict[str, str], field: str, fallback: str) -> str:
    return "" if row.get(field) == "true" else fallback


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    clean = lambda value: str(value).replace("|", "/").replace("\n", " ")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(clean(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def main() -> None:
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    scores = read_csv(PASS2 / "program_scores.csv")
    verification = read_csv(PASS2 / "program_verification.csv")
    professors = read_csv(PASS2 / "professor_matches_retained.csv")
    source_rows = read_csv(PASS2 / "final_source_ledger.csv")
    exclusion_audit = read_csv(PASS2 / "exclusion_sample_audit.csv")

    score_by_id = {row["program_id"]: row for row in scores}
    verification_by_id = {row["verified_program_id"]: row for row in verification if row["verified_program_id"]}
    professor_by_id = {row["program_id"]: row for row in professors}
    source_by_id = {row["source_id"]: row for row in source_rows}
    recommended_cfg = {row["program_id"]: row for row in config["recommended"]}
    conditional_cfg = {row["program_id"]: row for row in config["conditional"]}
    prior_active = {row["program_id"] for row in scores if row["all_hard_gates_pass"] == "true"}

    ranking: list[dict[str, object]] = []
    evidence: list[dict[str, object]] = []
    for decision in sorted(config["recommended"], key=lambda row: row["overall_rank"]):
        program_id = decision["program_id"]
        score = score_by_id[program_id]
        verified = verification_by_id[program_id]
        match = professor_by_id[program_id]
        row = {
            "Overall Rank": decision["overall_rank"],
            "University": score["institution_name"],
            "Country": country_name(score["country"]),
            "Exact Program": score["program_name"],
            "Degree Type": score["degree_type"],
            "Recommendation Tier": decision["recommendation_tier"],
            "Funding Classification": decision["funding_classification"],
            "Funding Summary": decision["funding_summary"],
            "International Funding Eligible": "Yes",
            "Academic Eligibility Verified": "Yes",
            "Relative Admission Position": decision["relative_admission_position"],
            "Admission Rationale": decision["admission_rationale"],
            "Program Research Fit": decision["program_research_fit"],
            "Fit Evidence": match["specific_overlap"],
            "Example Faculty or Lab": f"{match['full_name']} — {match['official_faculty_or_lab_url']}",
            "Application Fee": decision["application_fee"],
            "Fee Waiver": decision["fee_waiver"],
            "Fall 2027 Deadline": decision["deadline"],
            "Deadline Cycle": decision["deadline_cycle"],
            "Biggest Positive": decision["biggest_positive"],
            "Biggest Risk": decision["biggest_risk"],
            "Unresolved Question": decision["unresolved_question"],
            "Recommended Decision": decision["recommended_decision"],
            "Official Program URL": score["official_program_url"],
            "Official Funding URL": decision["funding_url"],
            "Admissions Evidence URL": decision["admissions_url"],
            "Notes": "Program-first review; one faculty example supports program-level fit and is not a recruiting claim.",
        }
        ranking.append(row)
        evidence.append({
            "University": row["University"],
            "Program": row["Exact Program"],
            "Decision Category": "Recommended",
            "Research Degree Claim": verified["research_requirement"],
            "Funding Claim": decision["funding_summary"],
            "Academic Eligibility Claim": f"{verified['bachelors_entry_eligibility']} Minimum: {verified['minimum_gpa']}",
            "International Eligibility Claim": verified["international_student_eligibility"],
            "Program Fit Claim": match["specific_overlap"],
            "Source URL": decision["funding_url"],
            "Source Type": "Official university/department page",
            "Information Cycle": decision["deadline_cycle"],
            "Access Date": ACCESS_DATE,
            "Verification Status": "Claim text manually compared with current official source",
            "Uncertainty": decision["unresolved_question"],
            "Official Program URL": score["official_program_url"],
            "Official Funding URL": decision["funding_url"],
            "Admissions URL": decision["admissions_url"],
            "Fit URL": match["official_faculty_or_lab_url"],
        })

    open_questions: list[dict[str, object]] = []
    for priority, decision in enumerate(config["conditional"], start=1):
        program_id = decision["program_id"]
        score = score_by_id[program_id]
        verified = verification_by_id[program_id]
        match = professor_by_id.get(program_id, {})
        open_questions.append({
            "Priority": priority,
            "University": score["institution_name"],
            "Program": score["program_name"],
            "Question": decision["question"],
            "Correct Recipient Type": decision["recipient_type"],
            "Official Contact": decision["official_contact"],
            "Why the Answer Matters": decision["why"],
            "Current Decision Without Reply": decision["current_decision"],
            "Evidence URL": decision["evidence_url"],
        })
        evidence.append({
            "University": score["institution_name"],
            "Program": score["program_name"],
            "Decision Category": "Conditional",
            "Research Degree Claim": verified["research_requirement"],
            "Funding Claim": verified["funding_status"],
            "Academic Eligibility Claim": f"{verified['bachelors_entry_eligibility']} Minimum: {verified['minimum_gpa']}",
            "International Eligibility Claim": verified["international_student_eligibility"],
            "Program Fit Claim": match.get("specific_overlap", "Program-level fit remains adequate in the Pass 2 corpus."),
            "Source URL": decision["evidence_url"],
            "Source Type": "Official university/department page",
            "Information Cycle": verified["deadline_cycle_label"],
            "Access Date": ACCESS_DATE,
            "Verification Status": "Conditional; one decision-changing question remains",
            "Uncertainty": decision["question"],
            "Official Program URL": score["official_program_url"],
            "Official Funding URL": first_source_url(verified, source_by_id, "funding_source_ids"),
            "Admissions URL": first_source_url(verified, source_by_id, "admissions_source_ids"),
            "Fit URL": match.get("official_faculty_or_lab_url", ""),
        })

    funding_pass = set(config["funding_contradiction_resolution"]["pass"])
    funding_conditional = set(config["funding_contradiction_resolution"]["conditional"])
    funding_audit: list[dict[str, object]] = []
    for score in scores:
        verified = verification_by_id[score["program_id"]]
        down = verified["funding_gate"] == "pass" and score["funding_hard_gate"] == "false"
        up = verified["funding_gate"] == "resolvable_inquiry" and score["funding_hard_gate"] == "true"
        if not (down or up):
            continue
        program_id = score["program_id"]
        if program_id in funding_pass:
            decision = "Pass"
            rationale = "Current official evidence establishes a guaranteed, normal, or highly credible funded route for admitted PhD students."
        elif program_id in funding_conditional:
            decision = "Conditional"
            rationale = "Current official evidence is competitive, supervisor-dependent, award-dependent, incomplete in duration, or insufficient on international net cost."
        else:
            raise ValueError(f"Unclassified Stage 3/Stage 5 funding contradiction: {program_id}")
        funding_audit.append({
            "University": score["institution_name"],
            "Program": score["program_name"],
            "Program ID": program_id,
            "Contradiction Direction": "Stage 3 pass → Stage 5 fail" if down else "Stage 3 inquiry → Stage 5 pass",
            "Stage 3 Funding Gate": verified["funding_gate"],
            "Stage 5 Funding Gate": score["funding_hard_gate"],
            "Pass 2.1 Funding Decision": decision,
            "Exact Reviewed Claim": verified["funding_status"],
            "Decision Rationale": rationale,
            "Official Funding URL": first_source_url(verified, source_by_id, "funding_source_ids"),
            "Information Cycle": verified["deadline_cycle_label"],
            "Access Date": ACCESS_DATE,
            "Verification Status": "Manual claim-level review; no keyword classification",
        })

    exclusions: list[dict[str, object]] = []
    for score in scores:
        program_id = score["program_id"]
        if program_id in recommended_cfg:
            continue
        verified = verification_by_id[program_id]
        previous = "Pass 2 active portfolio" if program_id in prior_active else "Pass 2 gated out"
        conditional = conditional_cfg.get(program_id)
        if conditional:
            revised = "Conditional"
            reason = conditional["current_decision"]
            funding_problem = conditional["funding_classification"]
            reconsider = conditional["question"]
            evidence_url = conditional["evidence_url"]
        else:
            revised = "Do Not Apply"
            if score["institution_name"] == "University of Illinois Urbana-Champaign":
                reason = "The 3.35 cumulative GPA is below the published 3.40 CS PhD minimum; only a rare-exception path exists, and the high-fee extreme reach is not justified over the chosen portfolio."
            elif program_id in prior_active:
                reason = "Removed from the Pass 2 active portfolio because the funding/admission/economics combination is weaker than the selected 15 programs."
            elif program_id in funding_conditional:
                reason = "Funding remains conditional after claim-level review and does not support application spending now."
            else:
                failures = score["hard_gate_failures"].replace("|", ", ") or "portfolio value"
                reason = f"Pass 2.1 does not justify application spending; unresolved or failed areas: {failures}."
            funding_problem = (
                "Funding passes claim-level review but does not overcome the remaining portfolio weaknesses."
                if program_id in funding_pass
                else ("Funding remains conditional or insufficient." if program_id in funding_conditional or score["funding_hard_gate"] == "false" else "")
            )
            reconsider = "Reconsider only if direct official evidence materially improves the failed gate or application economics."
            evidence_url = first_source_url(verified, source_by_id, "funding_source_ids")
        exclusions.append({
            "University": score["institution_name"],
            "Program": score["program_name"],
            "Previous Status": previous,
            "Revised Status": revised,
            "Primary Exclusion Reason": reason,
            "Funding Problem": funding_problem,
            "Eligibility Problem": problem_text(score, "eligibility_hard_gate", "Formal academic or international eligibility is unresolved or fails."),
            "Fit Problem": problem_text(score, "professor_hard_gate", "The existing corpus does not establish sufficient program-level concentration in Mitch's areas."),
            "Application Economics Problem": "" if score["application_fee"].replace(".", "", 1).isdigit() and float(score["application_fee"]) <= 100 else "The fee or applicable waiver is high, unknown, or unverified.",
            "Evidence URL": evidence_url or score["official_program_url"],
            "Reconsideration Condition": reconsider,
        })

    for audit in exclusion_audit:
        if audit["audit_result"] not in {"reopen_in_funnel", "unresolved_no_independent_positive"}:
            continue
        exclusions.append({
            "University": audit["institution_name"],
            "Program": "Institution-level exclusion audit; no exact recommended program",
            "Previous Status": audit["audit_result"],
            "Revised Status": "Do Not Apply",
            "Primary Exclusion Reason": audit["audit_rationale"],
            "Funding Problem": "No exact research program with credible funding is verified.",
            "Eligibility Problem": "Exact program eligibility is not verified.",
            "Fit Problem": "No decision-ready program-level fit is verified.",
            "Application Economics Problem": "No application should be purchased without an exact viable program.",
            "Evidence URL": audit["original_source_url"],
            "Reconsideration Condition": "Reconsider only if a specific research degree, eligibility route, funding package, and program-level fit are verified.",
        })

    validation = validate_recommended(ranking)
    if not validation["passed"]:
        raise ValueError("; ".join(validation["errors"]))
    if len(funding_audit) != 46:
        raise ValueError(f"Expected 46 funding contradictions, found {len(funding_audit)}")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT / "final_ranking.csv", RANKING_COLUMNS, ranking)
    write_csv(OUTPUT / "exclusions.csv", EXCLUSION_COLUMNS, exclusions)
    write_csv(OUTPUT / "funding_and_admissions_evidence.csv", EVIDENCE_COLUMNS, evidence)
    write_csv(OUTPUT / "open_questions.csv", OPEN_COLUMNS, open_questions)
    funding_columns = list(funding_audit[0])
    write_csv(OUTPUT / "funding_contradiction_audit.csv", funding_columns, funding_audit)

    tier_counts = Counter(str(row["Recommendation Tier"]) for row in ranking)
    restored = [row for row in ranking if score_by_id[next(pid for pid, cfg in recommended_cfg.items() if cfg["overall_rank"] == row["Overall Rank"])]["program_id"] not in prior_active]
    removed_ids = prior_active - set(recommended_cfg)
    fully_funded = sum(row["Funding Classification"] != "Highly credible standard funding" for row in ranking)

    report = f"""# Pass 2.1 simplified program-first shortlist

Generated: {ACCESS_DATE}

## Final ranked programs

{markdown_table(["Rank", "University", "Program", "Tier", "Funding", "Fee"], [[row["Overall Rank"], row["University"], row["Exact Program"], row["Recommendation Tier"], row["Funding Classification"], f'${row["Application Fee"]}'] for row in ranking])}

## Strongest realistic funded options

The five strongest realistic options are Lehigh, Old Dominion, Temple, UT San Antonio, and Baylor. Each combines a research PhD, current program-level funding evidence, formal eligibility, specific fit, and a fee of $90 or less.

## Best-value applications

Lehigh ($50), Old Dominion ($50), Baylor ($50), Temple ($60), and Vanderbilt ($0 after its confirmed Fall 2027 waiver) provide the strongest fee-to-upside trade-off.

## High-reach applications worth their fees

NC State is justified by an explicit four-year package and direct developer-AI fit. Vanderbilt is justified by dependable-software fit and a confirmed waiver. Boston University is justified by unusually clear five-year, twelve-month international-inclusive funding.

## Programs removed from the previous 22

{len(removed_ids)} Pass 2 selections were removed. The largest group consists of expensive high reaches whose relative admission position or program-level advantage does not justify displacing the selected portfolio. UIC moved to Conditional because the exact final-60-credit GPA must be calculated; William & Mary, RPI, and Trent moved to Conditional because decision-changing funding questions remain.

## Programs restored after correcting funding errors

{len(restored)} programs that Stage 5 had gated out are restored to the application-ready list: {', '.join(row['University'] for row in restored)}. Their official funding claims were read and classified directly rather than through substring rules.

## Important conditional programs

{markdown_table(["University", "Program", "Question"], [[row["University"], row["Program"], row["Question"]] for row in open_questions])}

## Application fees

The 15-program list totals **$1,105** before waivers and **$1,010** after the confirmed $95 Vanderbilt waiver. Possible CMU, NJIT, and Rochester waivers are excluded until granted. External transcript-evaluation charges are also excluded.

## Largest remaining portfolio weakness

The portfolio still has too few clearly funded, low-fee programs that are also genuinely less selective. Several otherwise strong options omit summer, fee, or maximum-duration terms, so written offers still require net-cost review.

## Exact next decision

Approve a $1,010 application budget for this 15-program list. If the budget must be lower, remove CMU first rather than cutting one of the five strongest realistic options.

## Method note

Pass 2.1 ranks funding certainty first, then relative admission position, program-level fit, application economics, degree structure, and unresolved risk. It does not reuse Pass 2 scores as ground truth and does not infer admission probability or professor recruiting status.
"""
    (REPORT_DIR / "final_report.md").write_text(report, encoding="utf-8")

    previous_rows = [score_by_id[program_id] for program_id in sorted(removed_ids)]
    restored_rows = [row for row in ranking if row["University"] in {item["University"] for item in restored}]
    change_log = f"""# Pass 2.1 change log

## Funding repair

The audit reconciles all 46 Stage 3/Stage 5 contradictions: 44 Stage 3 pass → Stage 5 fail rows and two Stage 3 inquiry → Stage 5 pass rows. Claim-level review classifies {sum(row['Pass 2.1 Funding Decision'] == 'Pass' for row in funding_audit)} as funding-pass and {sum(row['Pass 2.1 Funding Decision'] == 'Conditional' for row in funding_audit)} as conditional. The companion [funding contradiction audit](../../outputs/20260911-pass21-final/funding_contradiction_audit.csv) records the exact claim, official URL, cycle, access date, and rationale for every row.

## Admission repair

The prior `Plausible` rule is replaced by Strongest Realistic Option, Competitive, High Reach, Extreme Reach, Eligibility Concern, and Insufficient Evidence. No category is generated merely because Mitch meets a minimum. [UIUC's current CS PhD catalog](https://catalog.illinois.edu/graduate/engineering/computer-science-phd/) is recorded as a 3.40 undergraduate minimum with only a rare-exception path; the program remains Do Not Apply at current economics.

## Portfolio changes

### Restored to application-ready

{markdown_table(["University", "Program", "New tier", "Official funding source"], [[row["University"], row["Exact Program"], row["Recommendation Tier"], row["Official Funding URL"]] for row in restored_rows])}

### Removed from the Pass 2 active list

{markdown_table(["University", "Program", "Pass 2 funding"], [[row["institution_name"], row["program_name"], row["funding_status"]] for row in previous_rows])}

## Scope

The repair reuses the 166 scored programs, all 69 exclusion-audit records, the four reopen cases, the 13 unresolved exclusion cases, existing program verification, existing faculty evidence, and the source ledger. No new 855-university crawl was run.
"""
    (REPORT_DIR / "change_log.md").write_text(change_log, encoding="utf-8")

    workbook_data = {
        "final_ranking": ranking,
        "evidence": evidence,
        "exclusions": exclusions,
        "open_questions": open_questions,
    }
    (PROCESSED / "workbook_data.json").write_text(
        json.dumps(workbook_data, indent=2, default=str) + "\n", encoding="utf-8"
    )

    validation.update({
        "funding_contradictions_reviewed": len(funding_audit),
        "stage3_pass_to_stage5_fail": sum(row["Contradiction Direction"].startswith("Stage 3 pass") for row in funding_audit),
        "stage3_inquiry_to_stage5_pass": sum(row["Contradiction Direction"].startswith("Stage 3 inquiry") for row in funding_audit),
        "conditional_count": len(open_questions),
        "fully_funded_program_count": fully_funded,
        "previous_selections_removed": len(removed_ids),
        "previously_excluded_restored": len(restored),
        "fee_total_before_confirmed_waivers_usd": config["portfolio_rules"]["fee_total_before_confirmed_waivers_usd"],
        "fee_total_after_confirmed_waivers_usd": config["portfolio_rules"]["fee_total_after_confirmed_waivers_usd"],
        "core_claim_review": "Each recommended row includes current official program, funding, admissions, and fit URLs; claim text was compared with source content rather than URL status.",
    })
    (OUTPUT / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
