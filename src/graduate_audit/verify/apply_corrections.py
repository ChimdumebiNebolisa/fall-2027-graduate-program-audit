from __future__ import annotations

import argparse
from pathlib import Path

from graduate_audit.io import read_csv, write_csv
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
    program_id,
    source_id,
)


PROGRAM_CORRECTIONS: dict[str, dict[str, str]] = {
    "ca:dli:O19305471522:program:thesis-or-research-master-s:mmath-in-computer-science-thesis": {
        "fall_2027_deadline": "December 1 (recurring annual rule)",
        "deadline_cycle_status": "Official page gives December 1 for September of the following year; not explicitly labeled Fall 2027; recheck when the cycle opens.",
    },
    "ca:dli:O19305471522:program:direct-entry-phd:phd-in-computer-science-direct-from-bachelor-s-exception": {
        "fall_2027_deadline": "December 1 (recurring annual rule)",
        "deadline_cycle_status": "Official page gives December 1 for September of the following year; not explicitly labeled Fall 2027.",
    },
    "ca:dli:O19330231062:program:thesis-or-research-master-s:msc-in-computer-science-research": {
        "fall_2027_deadline": "December 15 (department page; official-source conflict)",
        "deadline_cycle_status": "Department page gives December 15, while the Graduate School says the upcoming intake is not yet configured; recheck and preserve the conflict.",
    },
    "ca:dli:O19330231062:program:integrated-or-structured-doctorate:phd-track-via-msc": {
        "fall_2027_deadline": "December 15 (department page; official-source conflict)",
        "deadline_cycle_status": "Department page gives December 15, while the Graduate School says the upcoming intake is not yet configured; recheck.",
        "notes": "Exceptional MSc/transfer structure, not a standalone guaranteed direct-PhD admission route.",
    },
    "ca:dli:O18886830282:program:direct-entry-phd:phd-in-computer-science-without-completed-msc": {
        "direct_from_bachelors_eligible": "Unclear — a five-year path without a completed MSc is described, but external direct admission from a bachelor's was not explicitly verified.",
        "fall_2027_deadline": "January 15 early / March 1 final (recurring annual rule)",
        "deadline_cycle_status": "Official pages state recurring Fall deadlines but do not label calendar year 2027.",
        "screening_decision": "downgraded",
        "recommendation": "Outreach Before Decision",
        "eligibility_score": "5",
        "biggest_risk": "Direct entry from an external bachelor's is not explicitly confirmed; four-year funding is also shorter than the stated five-year path.",
        "unresolved_question": "Will Calgary admit an external bachelor's holder directly, cover year five, and state the net amount after tuition and fees?",
    },
    "ca:dli:O18886830282:program:thesis-or-research-master-s:msc-in-computer-science-thesis": {
        "fall_2027_deadline": "January 15 early / March 1 final (recurring annual rule)",
        "deadline_cycle_status": "Official pages state recurring Fall deadlines but do not label calendar year 2027; recheck when the cycle opens.",
    },
    "us:ipeds:163286:program:phd:computer-science-phd": {
        "screening_decision": "downgrade",
        "funding_status": "All PhD students are funded through TA/RA subject to progress, but the official FAQ explicitly says no funding guarantee is provided in the admission offer.",
        "funding_score": "10",
        "recommendation": "Outreach Before Decision",
        "biggest_risk": "The admission offer does not guarantee funding even though current PhD students are generally funded.",
        "unresolved_question": "Would a Fall 2027 offer include a written multi-year tuition, stipend, health, fee, and summer commitment?",
    },
    "us:ipeds:233921:program:phd:computer-science-phd": {
        "funding_status": "Beginning with the Fall 2026 admission cycle, 100% of admitted PhD students receive a conditional five-year offer, excluding summers; some fees remain the student's responsibility.",
        "mandatory_fee_coverage": "Standard assistantship may leave comprehensive/CFE and other mandatory-fee liability.",
        "summer_funding": "Excluded from the published five-year offer statement; must be arranged separately.",
        "biggest_risk": "The policy is effective from Fall 2026 but excludes summers and leaves some mandatory fees to the student.",
    },
    "us:ipeds:221999:program:phd:computer-science-phd": {
        "fall_2027_deadline": "2027-01-08 final; 2026-12-15 recommended",
        "deadline_cycle_status": "Official Fall 2027 engineering admissions page; December 1, 2026 is the fee-waiver priority date.",
    },
    "ca:dli:O19425660421:program:thesis-or-research-master-s:msc-in-computer-science-thesis": {
        "fall_2027_deadline": "Not yet published",
        "deadline_cycle_status": "The official department page still labels December 15 for Fall 2026; no Fall 2027 date is inferred.",
    },
    "us:ipeds:195003:program:phd:computing-and-information-sciences-phd": {
        "gre_policy": "Required on the current official degree page; reconfirm when the Fall 2027 cycle opens.",
        "fall_2027_deadline": "Not yet published",
        "deadline_cycle_status": "The 2026–27 curriculum lists December 31 priority and rolling review thereafter; it is not labeled Fall 2027.",
    },
    "us:ipeds:110653:program:phd:software-engineering-phd": {
        "fall_2027_deadline": "December 15 (recurring rule; Fall 2027 not yet cycle-labeled)",
        "deadline_cycle_status": "Official ICS FAQ states a recurring December 15 deadline; no source independently labels it for Fall 2027.",
    },
    "us:ipeds:145637:program:phd:computer-science-phd": {
        "minimum_gpa": "3.0/4.0 over the last two undergraduate years; 3.40 is recommended by the program",
        "minimum_gpa_policy": "The Graduate College minimum is 3.0 over the last two undergraduate years; 3.40 is a program recommendation, not a hard minimum.",
        "screening_decision": "retained",
        "exclusion_reason": "",
        "eligibility_score": "11",
        "admission_plausibility": "Reach",
        "recommendation": "Likely Apply",
        "biggest_risk": "The program recommends a 3.40 cumulative GPA; the applicant's recent-two-year performance clears the formal 3.0 minimum, but the cumulative GPA is below that recommendation.",
        "unresolved_question": "How will the committee weigh the stronger recent-two-year record against the 3.35 cumulative GPA and 3.40 recommendation?",
        "notes": "Independent exclusion sampling corrected the earlier false hard-GPA exclusion; faculty fit and funding remain strong, with offer-specific terms to confirm.",
    },
    "us:ipeds:199193:program:phd:computer-science-phd": {
        "funding_model": "Four-year comprehensive package for each fall PhD admit who requests aid; later support transitions toward adviser-funded RA work.",
        "funding_status": "Current official policy promises tuition, individual health insurance, and stipend for four years to every fall PhD admit requesting aid; fees, summers, year five, and adviser transition remain unresolved.",
        "phd_funding": "Four-year tuition, individual health insurance, and stipend package for fall PhD admits requesting aid; conditions and later adviser funding apply.",
        "funding_score": "21",
        "screening_decision": "retained",
        "exclusion_reason": "",
        "recommendation": "Likely Apply",
        "biggest_risk": "The package excludes student fees and does not settle summer funding, year five, or the transition to adviser-funded RA support.",
        "unresolved_question": "What are the summer, student-fee, year-five, and adviser-transition terms in a Fall 2027 offer?",
        "notes": "Independent exclusion sampling found a newer department-wide four-year package; the program was rescored and restored to the application portfolio.",
    },
    "ror:041kmwe10:program:phd:phd-in-computing": {
        "direct_from_bachelors_eligible": "No — applicants with only a bachelor's are not normally considered; the department expects a distinction-level master's.",
        "screening_decision": "excluded",
        "eligibility_score": "0",
        "recommendation": "Do Not Apply",
        "exclusion_reason": "Bachelor-only applicants are not normally considered; a master's is expected for the immediate route.",
        "biggest_risk": "Imperial says bachelor-only applicants are not normally considered for this route.",
        "unresolved_question": "Would Imperial confirm an exceptional bachelor-only route in writing, or should an MSc come first?",
    },
    "ror:05a28rw58:program:direct-entry-phd:direct-doctorate-in-computer-science": {
        "funding_model": "Conditional on Direct Doctorate admission: financial support and tuition waivers for the first two years, followed by a competitive doctoral salary intended to cover living expenses.",
        "funding_status": "Program-level support is stated for admitted Direct Doctorate students; no individual Fall 2027 offer or supervisor capacity is confirmed.",
        "tuition_coverage": "Tuition waiver stated for the first two years; later doctoral terms follow the salaried phase and must be confirmed in the offer.",
        "biggest_risk": "Exceptional-entry threshold and no confirmed Fall 2027 supervisor capacity or individual offer.",
        "unresolved_question": "Will a Fall 2027 admission include the stated two-year support/waiver and subsequent salaried doctoral appointment?",
    },
    "ror:05m7pjf47:program:phd:phd-computer-science": {
        "direct_from_bachelors_eligible": "Project-specific — some official project calls accept a first/upper-second bachelor's; this is not a universal route.",
        "minimum_gpa_policy": "Project-specific calls may accept a strong relevant bachelor's; confirm against the exact 2027 project.",
        "exclusion_reason": "No matching Fall 2027 fully funded international project is verified; current catalogue metadata also requires clarification for non-EU applicants.",
        "biggest_risk": "Bachelor entry is project-specific, the indexed project guide became unavailable, and no matching fully funded international 2027 call is verified.",
        "unresolved_question": "Which current 2027 project, if any, accepts a bachelor's-only non-EU applicant with full funding?",
    },
}


def _recalculate(row: dict[str, str]) -> None:
    fields = (
        "professor_fit_score", "faculty_depth_score", "funding_score",
        "eligibility_score", "degree_admissions_score", "application_economics_score",
    )
    if all(str(row.get(field, "")).strip() for field in fields):
        row["research_fit_score"] = str(int(row["professor_fit_score"]) + int(row["faculty_depth_score"]))
        row["overall_score"] = str(sum(int(row[field]) for field in fields))


def apply_program_corrections(repo_root: Path) -> int:
    changed = 0
    for region in ("canada", "us", "europe"):
        path = repo_root / "data/processed/deep_review" / region / "deep_programs.csv"
        rows = read_csv(path)
        for row in rows:
            correction = PROGRAM_CORRECTIONS.get(row.get("program_id", ""))
            if correction:
                row.update(correction)
                _recalculate(row)
                changed += 1
        write_csv(path, rows, PROGRAM_COLUMNS)
    return changed


def apply_faculty_corrections(repo_root: Path) -> int:
    changed = 0
    for region in ("europe", "us"):
        path = repo_root / "data/processed/deep_review" / region / "professors.csv"
        rows = read_csv(path)
        for row in rows:
            if row.get("professor_id") == "ror:020hwjq30:faculty:fabian-fagerholm":
                row["faculty_position"] = "Current Computer Science faculty; official pages conflict between Associate Professor and Assistant Professor"
                row["appointment_status"] = "Current appointment confirmed; rank unresolved across official pages"
                row["notes"] = "Current faculty status is confirmed, but official Aalto pages conflict on academic rank; verify title before outreach."
                changed += 1
            elif row.get("professor_id") == "us:ipeds:145637:faculty:lingming-zhang":
                row["fit_explanation"] = "Excellent direct fit in automated program repair, software testing, and LLM-based software-engineering agents."
                row["outreach_priority"] = "Second wave"
                row["recommended_outreach_angle"] = "Connect TerraProbe's LLM-based Terraform repair setting to current work on LLM software-engineering agents and program repair."
                row["specific_question_goal"] = "Whether this research direction and Fall 2027 supervision capacity align, without presuming recruitment."
                row["notes"] = "Current appointment and recent work verified; recruiting status remains unknown. Earlier GPA hard exclusion was corrected after independent validation."
                changed += 1
        write_csv(path, rows, PROFESSOR_COLUMNS)
    return changed


def apply_hmu_false_negative(repo_root: Path) -> dict[str, int]:
    region_root = repo_root / "data/processed/regions/europe"
    institution_path = region_root / "institution_universe.csv"
    institutions = read_csv(institution_path)
    institution_changes = 0
    for row in institutions:
        if row.get("institution_id") == "ror:039ce0m20":
            row["relevant_graduate_field_signal"] = "Official ECE PhD and research-oriented Informatics Engineering MSc found in independent exclusion audit."
            row["screening_status"] = "preliminary_fit"
            row["exclusion_reason"] = ""
            row["manual_verification"] = "Required — program existence confirmed; eligibility, language, funding, and deadline need deep review."
            row["notes"] = "False negative corrected after deterministic independent exclusion sampling on 2026-09-09."
            institution_changes += 1
    write_csv(institution_path, institutions, INSTITUTION_COLUMNS)

    program_path = region_root / "program_screening.csv"
    programs = read_csv(program_path)
    existing_ids = {row.get("program_id") for row in programs}
    additions = [
        {
            "institution_id": "ror:039ce0m20",
            "institution_name": "Hellenic Mediterranean University",
            "country": "Greece",
            "program_name": "Electrical and Computer Engineering PhD",
            "degree_type": "PhD requiring a master's",
            "department": "Electrical and Computer Engineering",
            "official_program_url": "https://ece.hmu.gr/en/doctoral-ph-d-studies-program/",
            "thesis_dissertation_requirement": "Original doctoral research and dissertation stated on the official program page.",
            "direct_from_bachelors_eligible": "No ordinarily; exceptional non-master admission may be possible by reasoned department decision.",
            "international_student_eligible": "Unresolved in this mechanical correction; verify before any portfolio use.",
            "language_of_instruction": "Unresolved; verify program and dissertation language requirements.",
            "current_program_status": "Current official program page located 2026-09-09.",
            "preliminary_fit": "Relevant computing research route; topic-level fit not yet deeply reviewed.",
            "screening_decision": "preliminary_fit",
            "fall_2027_deadline": "Not yet verified",
            "deadline_cycle_status": "No Fall 2027 date inferred.",
            "funding_status": "Not yet verified",
            "recommendation": "Investigate Further",
            "biggest_risk": "Ordinary entry appears to require a master's and funding/language are unresolved.",
            "unresolved_question": "Is an exceptional bachelor-entry applicant eligible with full funding and English supervision?",
            "verification_status": "Independent exclusion recheck; deep review required",
            "notes": "Added after a deterministic exclusion sample found a false negative; not a finalist without full deep review.",
        },
        {
            "institution_id": "ror:039ce0m20",
            "institution_name": "Hellenic Mediterranean University",
            "country": "Greece",
            "program_name": "Informatics Engineering MSc",
            "degree_type": "Thesis or research master's",
            "department": "Informatics Engineering",
            "official_program_url": "https://hmu.gr/en/postgraduate-studies/postgraduate-programs/",
            "research_credit_requirement": "Official university listing describes a research orientation; thesis structure requires deep review.",
            "direct_from_bachelors_eligible": "Potentially, subject to credential review; not yet verified.",
            "international_student_eligible": "Unresolved in this mechanical correction; verify before any portfolio use.",
            "language_of_instruction": "Unresolved; verify English availability.",
            "current_program_status": "Current official program listing located 2026-09-09.",
            "preliminary_fit": "Relevant research-oriented computing master's signal; topic-level fit not yet deeply reviewed.",
            "screening_decision": "preliminary_fit",
            "fall_2027_deadline": "Not yet verified",
            "deadline_cycle_status": "No Fall 2027 date inferred.",
            "funding_status": "Not yet verified",
            "recommendation": "Investigate Further",
            "biggest_risk": "Research structure, language, international eligibility, and full funding are unresolved.",
            "unresolved_question": "Does the route offer a substantial thesis, English supervision, international admission, and full funding?",
            "verification_status": "Independent exclusion recheck; deep review required",
            "notes": "Added after a deterministic exclusion sample found a false negative; not a finalist without full deep review.",
        },
    ]
    program_additions = 0
    for row in additions:
        row["program_id"] = program_id(row["institution_id"], row["degree_type"], row["program_name"])
        if row["program_id"] not in existing_ids:
            programs.append(row)
            program_additions += 1
    write_csv(program_path, programs, PROGRAM_COLUMNS)

    exclusion_path = region_root / "exclusion_log.csv"
    exclusions = read_csv(exclusion_path)
    kept = [row for row in exclusions if row.get("institution_id") != "ror:039ce0m20"]
    write_csv(exclusion_path, kept, EXCLUSION_COLUMNS)
    return {
        "institutions_corrected": institution_changes,
        "programs_added": program_additions,
        "exclusions_removed": len(exclusions) - len(kept),
    }


def apply_exclusion_corrections(repo_root: Path) -> int:
    changed = 0
    canada_path = repo_root / "data/processed/regions/canada/exclusion_log.csv"
    rows = read_csv(canada_path)
    for row in rows:
        if row.get("institution_id") == "ca:dli:O19332928222":
            row["source_url"] = "https://gradadmissions.ocadu.ca/graduate-programs"
            row["supporting_evidence"] = "Official OCAD graduate inventory includes art/design/media programs such as Digital Futures but no CS/SE research graduate degree."
            changed += 1
        elif row.get("institution_id") == "ca:dli:O19395677925":
            row["source_url"] = "https://uhearst.ca/programmes/nos-programmes-detudes/"
            row["supporting_evidence"] = "Current official inventory lists no computing research graduate degree."
            changed += 1
    write_csv(canada_path, rows, EXCLUSION_COLUMNS)

    us_path = repo_root / "data/processed/deep_review/us/exclusion_or_downgrade.csv"
    us_rows = read_csv(us_path)
    restored = {
        "us:ipeds:145637:program:phd:computer-science-phd",
        "us:ipeds:199193:program:phd:computer-science-phd",
    }
    kept = [row for row in us_rows if row.get("program_id") not in restored]
    changed += len(us_rows) - len(kept)
    write_csv(us_path, kept, EXCLUSION_COLUMNS)
    return changed


def build_second_source_ledger(repo_root: Path) -> int:
    rows: list[dict[str, str]] = []
    for path in sorted((repo_root / "data/processed/validation").glob("*/second_source_checks.csv")):
        for check in read_csv(path):
            url = check.get("second_source_url") or check.get("source_url") or ""
            if not url:
                continue
            rows.append({
                "source_id": source_id(url + "#" + (check.get("check_id") or check.get("claim_category") or "check")),
                "institution_id": check.get("institution_id", ""),
                "institution_name": check.get("institution_name", ""),
                "program_id": check.get("program_id", ""),
                "program_or_professor": check.get("program_name") or check.get("professor_name") or "Independent exclusion sample",
                "claim_type": "independent second-source: " + (check.get("claim_category") or check.get("claim_type") or "verification"),
                "exact_claim_supported": check.get("second_source_finding") or check.get("finding") or check.get("result") or "Independent source check recorded.",
                "source_title": "Independent second-source verification",
                "publisher": check.get("institution_name", ""),
                "publication_date": "",
                "url": url,
                "source_type": "official verification page",
                "official_or_secondary": "official",
                "date_accessed": check.get("checked_date") or check.get("date_checked") or "2026-09-09",
                "admissions_cycle": "As labeled in the checked source; no date rolled forward",
                "confidence": check.get("result") or check.get("confidence") or "independently checked",
                "verification_status": "second-source checked",
                "access_note": "; ".join(filter(None, [check.get("correction_needed", ""), check.get("notes", "")])),
            })
    ca_root = repo_root / "data/processed/validation/cross_region_ca"
    for path in (ca_root / "europe_finalist_second_source.csv", ca_root / "exclusion_sample_audit.csv"):
        if not path.exists():
            continue
        for check in read_csv(path):
            raw_url = (
                check.get("funding_url") or check.get("faculty_appointment_url")
                or check.get("degree_entry_url") or check.get("official_url") or ""
            )
            url = raw_url.split(" | ")[0]
            if not url:
                continue
            finding = (
                check.get("funding_finding") or check.get("faculty_appointment_finding")
                or check.get("degree_entry_finding") or check.get("finding")
                or "Independent verification recorded."
            )
            claim_type = "finalist hard-gate verification" if check.get("program_id") else "independent exclusion sample"
            rows.append({
                "source_id": source_id(url + "#validation-" + (check.get("program_id") or check.get("sample_id") or "check")),
                "institution_id": check.get("institution_id", ""),
                "institution_name": check.get("institution_name", ""),
                "program_id": check.get("program_id", ""),
                "program_or_professor": check.get("program_name") or check.get("professor_name") or "Independent exclusion sample",
                "claim_type": "independent second-source: " + claim_type,
                "exact_claim_supported": finding,
                "source_title": "Independent official-source verification",
                "publisher": check.get("institution_name", ""),
                "publication_date": "",
                "url": url,
                "source_type": "official verification page",
                "official_or_secondary": "official",
                "date_accessed": check.get("date_checked") or "2026-09-09",
                "admissions_cycle": "As labeled in source; no date rolled forward",
                "confidence": check.get("overall_result") or check.get("confidence") or "independently checked",
                "verification_status": "second-source checked",
                "access_note": check.get("corrective_action", ""),
            })
    us_root = repo_root / "data/processed/validation/finalists_us"
    for path in (us_root / "program_checks.csv", us_root / "exclusion_sample_checks.csv"):
        if not path.exists():
            continue
        for check in read_csv(path):
            url = check.get("second_url") or check.get("faculty_url") or check.get("primary_url") or ""
            if not url:
                continue
            rows.append({
                "source_id": source_id(url + "#validation-" + (check.get("program_id") or check.get("institution_id") or "check")),
                "institution_id": check.get("institution_id", ""),
                "institution_name": check.get("institution_name", ""),
                "program_id": check.get("program_id", ""),
                "program_or_professor": check.get("faculty_name") or check.get("program_name") or "Independent exclusion sample",
                "claim_type": "independent second-source: U.S. finalist or exclusion verification",
                "exact_claim_supported": check.get("primary_claim") or check.get("faculty_note") or "Independent verification recorded.",
                "source_title": "Independent official-source verification",
                "publisher": check.get("institution_name", ""),
                "publication_date": "",
                "url": url,
                "source_type": "official verification page",
                "official_or_secondary": "official",
                "date_accessed": check.get("checked_date") or "2026-09-09",
                "admissions_cycle": "As labeled in source; no date rolled forward",
                "confidence": check.get("result") or check.get("faculty_result") or "independently checked",
                "verification_status": "second-source checked",
                "access_note": check.get("correction_needed", ""),
            })
    destination = repo_root / "data/processed/validation/second_source_ledger/sources.csv"
    write_csv(destination, rows, SOURCE_COLUMNS)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    print({
        "program_rows_corrected": apply_program_corrections(root),
        "faculty_rows_corrected": apply_faculty_corrections(root),
        "hmu_false_negative": apply_hmu_false_negative(root),
        "exclusions_corrected": apply_exclusion_corrections(root),
        "second_source_ledger_rows": build_second_source_ledger(root),
    })


if __name__ == "__main__":
    main()
