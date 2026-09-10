"""Generate independent Canada/US second-source validation artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "data" / "processed" / "validation" / "cross_region_eu"
EVIDENCE = ROOT / "evidence" / "validation" / "cross_region_eu"
CHECKED = "2026-09-09"
OUT.mkdir(parents=True, exist_ok=True)
EVIDENCE.mkdir(parents=True, exist_ok=True)


rows: list[dict[str, str]] = []


def add(region, record_type, program_id, institution_id, institution, program, category,
        claim, primary, second, finding, result="confirmed", correction="No", severity="none", notes=""):
    rows.append({
        "check_id": f"XREG-{len(rows)+1:03d}", "region": region,
        "record_type": record_type, "program_id": program_id, "institution_id": institution_id,
        "institution_name": institution, "program_name": program,
        "claim_category": category, "claim_from_source_dataset": claim,
        "primary_source_url": primary, "second_source_url": second,
        "second_source_finding": finding, "result": result,
        "correction_needed": correction, "severity": severity,
        "checked_date": CHECKED, "notes": notes,
    })


ca = {
    "waterloo_mmath": ("ca:dli:O19305471522:program:thesis-or-research-master-s:mmath-in-computer-science-thesis", "ca:dli:O19305471522", "University of Waterloo", "MMath in Computer Science (thesis)"),
    "waterloo_phd": ("ca:dli:O19305471522:program:direct-entry-phd:phd-in-computer-science-direct-from-bachelor-s-exception", "ca:dli:O19305471522", "University of Waterloo", "PhD in Computer Science (direct from bachelor's exception)"),
    "ubc_msc": ("ca:dli:O19330231062:program:thesis-or-research-master-s:msc-in-computer-science-research", "ca:dli:O19330231062", "University of British Columbia", "MSc in Computer Science (research)"),
    "ubc_track": ("ca:dli:O19330231062:program:integrated-or-structured-doctorate:phd-track-via-msc", "ca:dli:O19330231062", "University of British Columbia", "PhD Track via MSc"),
    "toronto": ("ca:dli:O19332746152:program:direct-entry-phd:phd-in-computer-science-phd-u", "ca:dli:O19332746152", "University of Toronto", "PhD in Computer Science (PhD U)"),
    "sask": ("ca:dli:O19425660421:program:thesis-or-research-master-s:msc-in-computer-science-thesis", "ca:dli:O19425660421", "University of Saskatchewan", "MSc in Computer Science (thesis)"),
    "calgary_phd": ("ca:dli:O18886830282:program:direct-entry-phd:phd-in-computer-science-without-completed-msc", "ca:dli:O18886830282", "University of Calgary", "PhD in Computer Science (without completed MSc)"),
    "calgary_msc": ("ca:dli:O18886830282:program:thesis-or-research-master-s:msc-in-computer-science-thesis", "ca:dli:O18886830282", "University of Calgary", "MSc in Computer Science (thesis)"),
}


def program_claims(key, funding_claim, funding_primary, funding_second, funding_finding,
                   eligibility_claim, eligibility_primary, eligibility_second, eligibility_finding,
                   faculty, faculty_primary, faculty_second, faculty_finding,
                   deadline_claim, deadline_primary, deadline_second, deadline_finding,
                   funding_result="confirmed", funding_correction="No", funding_severity="none",
                   eligibility_result="confirmed", eligibility_correction="No", eligibility_severity="none",
                   deadline_result="confirmed", deadline_correction="No", deadline_severity="none"):
    pid, iid, institution, program = ca[key]
    add("Canada", "retained_program", pid, iid, institution, program, "funding_wording", funding_claim,
        funding_primary, funding_second, funding_finding, funding_result, funding_correction, funding_severity)
    add("Canada", "retained_program", pid, iid, institution, program, "bachelors_and_international_eligibility", eligibility_claim,
        eligibility_primary, eligibility_second, eligibility_finding, eligibility_result, eligibility_correction, eligibility_severity)
    add("Canada", "retained_program", pid, iid, institution, program, "current_faculty_appointment", faculty,
        faculty_primary, faculty_second, faculty_finding)
    add("Canada", "retained_program", pid, iid, institution, program, "deadline_cycle_label", deadline_claim,
        deadline_primary, deadline_second, deadline_finding, deadline_result, deadline_correction, deadline_severity)


program_claims(
    "waterloo_mmath",
    "Guaranteed package for full-time MMath within program time limits",
    "https://uwaterloo.ca/computer-science/current-graduate-students/funding-and-awards",
    "https://uwaterloo.ca/future-graduate-students/funding/funding-research-based-graduate-programs",
    "Central page confirms research master's funding eligibility for domestic/international students; CS page is stronger and supplies the actual program package.",
    "Honours bachelor's route; international students eligible",
    "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath",
    "https://uwaterloo.ca/computer-science/future-graduate-students/programs",
    "Department page confirms the research MMath; central program listing supplies the four-year honours bachelor's requirement and international funding amount.",
    "Shane McIntosh — Associate Professor",
    "https://uwaterloo.ca/computer-science/about/people/s4mcinto",
    "https://rebels.cs.uwaterloo.ca/",
    "Current official profile and Waterloo-hosted lab page both identify McIntosh and his empirical software engineering/DevOps group.",
    "2026-12-01; labelled current Fall 2027",
    "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath",
    "https://uwaterloo.ca/computer-science/future-graduate-students/programs",
    "The official program page gives December 1 for September of the following year; the department overview does not independently attach calendar year 2026.",
    deadline_result="partial", deadline_correction="Soften to recurring December 1 unless a captured page explicitly labels Fall 2027.", deadline_severity="medium",
)

program_claims(
    "waterloo_phd",
    "Guaranteed full-time PhD package within program time limits",
    "https://uwaterloo.ca/computer-science/current-graduate-students/funding-and-awards",
    "https://uwaterloo.ca/current-graduate-students/awards-and-funding/minimum-funding",
    "Central policy confirms guaranteed minimum funding within time limits and distinguishes bachelor's-entry doctoral duration; CS publishes the higher package.",
    "Exceptional direct entry from bachelor's; international eligible",
    "https://uwaterloo.ca/computer-science/future-graduate-students/programs",
    "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-doctor-philosophy-phd",
    "Central PhD listing explicitly says undergraduate CS degree holders may apply directly and describes the exceptional standard.",
    "Shane McIntosh — Associate Professor",
    "https://uwaterloo.ca/computer-science/about/people/s4mcinto",
    "https://rebels.cs.uwaterloo.ca/",
    "Current official profile and Waterloo-hosted lab page confirm the appointment and research scope.",
    "2026-12-01 mapped from recurring September-entry date",
    "https://uwaterloo.ca/computer-science/future-graduate-students/programs",
    "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-doctor-philosophy-phd",
    "Central listing confirms December 1 for September of the following year, but the page wording is recurring rather than explicitly Fall 2027.",
    deadline_result="partial", deadline_correction="Keep December 1 but label recurring/not explicitly Fall 2027.", deadline_severity="low",
)

for key, program_label in [("ubc_msc", "MSc"), ("ubc_track", "MSc-to-PhD track")]:
    program_claims(
        key,
        "Guaranteed at applicable department minimum for two years (and PhD minimum after transfer for the track)",
        "https://www.cs.ubc.ca/grads/awards-support-current-grad-students/financial-assistantship/stipends-support-details-2025-2026",
        "https://www.grad.ubc.ca/prospective-students/graduate-degree-programs/master-of-science-computer-science",
        "Graduate School profile confirms two-year thesis-MSc support at $32,171/year and conditions; transfer funding remains governed by the applicable PhD policy.",
        "Four-year bachelor's route and international eligibility; track requires exceptional selection/transfer",
        "https://www.cs.ubc.ca/students/grad/admissions/eligibility",
        "https://www.grad.ubc.ca/prospective-students/international-students",
        "UBC explicitly serves international graduate applicants; the degree profile requires an eligible bachelor's. The track is not a separate automatic PhD admission guarantee.",
        "Reid Holmes — Professor",
        "https://www.cs.ubc.ca/people/reid-holmes",
        "https://www.cs.ubc.ca/people/faculty",
        "Current department faculty list independently includes Reid Holmes as Professor.",
        "2026-12-15 labelled explicit Fall 2027 / January 2028",
        "https://www.cs.ubc.ca/students/grad/admissions",
        "https://www.grad.ubc.ca/prospective-students/graduate-degree-programs/master-of-science-computer-science",
        "Graduate School profile says upcoming-intake dates are not yet configured, while the department source carries December 15. Preserve the source conflict.",
        deadline_result="partial", deadline_correction="Flag conflicting official pages and recheck; do not call December 15 independently confirmed by the Graduate School.", deadline_severity="medium",
        eligibility_result="partial" if key == "ubc_track" else "confirmed",
        eligibility_correction="Clarify that the PhD track is an exceptional MSc/transfer structure, not a standalone guaranteed direct PhD offer." if key == "ubc_track" else "No",
        eligibility_severity="medium" if key == "ubc_track" else "none",
    )

program_claims(
    "toronto",
    "Guaranteed research-stream funding; enhanced package targets CAD 39,500 take-home",
    "https://web.cs.toronto.edu/graduate/funding-tuition-awards",
    "https://web.cs.toronto.edu/graduate/phd",
    "PhD page independently confirms funding for all full-time PhD students and a 60-month direct-entry period; funding page supplies the amount and conditions.",
    "Direct-entry PhD from bachelor's is intended for international students",
    "https://web.cs.toronto.edu/graduate/faq",
    "https://www.sgs.utoronto.ca/programs/computer-science/",
    "SGS independently lists direct entry for domestic and international applicants with A-minus minimum; department describes PhD-U as intended for international students.",
    "Marsha Chechik — Professor",
    "https://web.cs.toronto.edu/people/faculty-directory",
    "https://web.cs.toronto.edu/news-events/news/marsha-chechik-honoured-with-deans-excellence-research-award",
    "A December 2025 official news item independently identifies Chechik as a current professor; faculty directory remains current.",
    "Fall 2027 deadline TBD; applications open October 2026",
    "https://web.cs.toronto.edu/graduate/how-to-apply",
    "https://www.sgs.utoronto.ca/programs/computer-science/",
    "Department confirms the Fall 2027 opening month but no deadline; SGS still shows the prior Fall 2026 deadline. TBD is the correct conservative label.",
)

program_claims(
    "sask",
    "Normally funded for 20 months with international tuition offset",
    "https://grad.usask.ca/programs/computer-science.php",
    "https://governance.usask.ca/documents/council/agenda/2023-2024/dec_agenda.pdf",
    "Older official governance material corroborates the two-year/20-month departmental funding structure and international tuition-offset design; current amount comes only from the live program page.",
    "Four-year honours bachelor's/equivalent; international students eligible",
    "https://grad.usask.ca/programs/computer-science.php",
    "https://programs.usask.ca/grad-studies/computer-science/comp-sci-msc-thesis.php",
    "Current 2026-27 catalogue independently confirms a relevant four-year honours degree/equivalent and English rules for international applicants.",
    "Chanchal K. Roy — Professor",
    "https://www.cs.usask.ca/people/faculty%20profiles/chanchal-roy.php",
    "https://www.cs.usask.ca/people/faculty.php",
    "Current faculty directory independently lists Roy as Professor; a June 2026 university news item also identifies his active graduate supervision.",
    "December 15 recurring; Fall 2027 year not explicitly stated",
    "https://grad.usask.ca/programs/computer-science.php",
    "https://programs.usask.ca/grad-studies/computer-science/comp-sci-msc-thesis.php",
    "Catalogue confirms the program/eligibility but does not attach a cycle year to the department's recurring December 15 deadline. Existing cautious label is correct.",
)

program_claims(
    "calgary_phd",
    "CAD 24,000/year guaranteed four years; five-year expected duration without MSc leaves gap",
    "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements",
    "https://science.ucalgary.ca/current-students/graduate/graduate-science-advising",
    "Faculty advising independently describes PhD funding as structured for four guaranteed years; the department page supplies the amount. The fifth-year gap is real.",
    "Direct entry from bachelor's marked yes because program describes expected time without completed MSc",
    "https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/doctoral-thesis-based",
    "https://calendar.ucalgary.ca/programs/CPSCPHD",
    "The official program describes a five-year path without completed MSc, but neither current admissions page nor calendar explicitly says a new external bachelor's holder may be admitted directly.",
    "Mahmoud Alfadel — Assistant Professor",
    "https://profiles.ucalgary.ca/mahmoud-alfadel",
    "https://science.ucalgary.ca/computer-science/contacts/faculty",
    "Current department faculty list independently includes Alfadel as Assistant Professor.",
    "2027-01-15 early; 2027-03-01 final",
    "https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/computer-science-phd",
    "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements",
    "Official pages state recurring January 15/March 1 Fall deadlines but do not label them as calendar-year 2027.",
    eligibility_result="not_confirmed", eligibility_correction="Change direct_from_bachelors_eligible from yes to unclear and obtain written confirmation before retaining the route.", eligibility_severity="high",
    deadline_result="not_confirmed", deadline_correction="Remove invented 2027 year; store January 15 early / March 1 final as recurring dates pending Fall 2027 publication.", deadline_severity="high",
)

program_claims(
    "calgary_msc",
    "CAD 24,000/year guaranteed for two years",
    "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements",
    "https://science.ucalgary.ca/current-students/graduate/graduate-science-advising",
    "Faculty advising independently describes the two-year guaranteed-funding period; department admissions page supplies the amount and international differential-fee award.",
    "Four-year bachelor's/equivalent; international students eligible",
    "https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/computer-science-msc-thesis",
    "https://calendar.ucalgary.ca/programs/CPSCMSCT/admissions-cMwRI",
    "Current calendar independently states a four-year bachelor's/equivalent and 3.30 GPA requirements; program page provides international deadlines.",
    "Mahmoud Alfadel — Assistant Professor",
    "https://profiles.ucalgary.ca/mahmoud-alfadel",
    "https://science.ucalgary.ca/computer-science/contacts/faculty",
    "Current department faculty list independently includes Alfadel as Assistant Professor.",
    "2027-01-15 early; 2027-03-01 final",
    "https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/computer-science-msc-thesis",
    "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements",
    "Official pages state recurring January 15/March 1 Fall deadlines but do not label them as calendar-year 2027.",
    deadline_result="not_confirmed", deadline_correction="Remove invented 2027 year; label the dates recurring and recheck the Fall 2027 cycle.", deadline_severity="high",
)


# Deterministic Canada exclusion sample: first five records after sorting the source
# exclusion log by SHA-256(institution_id), then institution_id.
sample_exclusions = [
    ("ca:dli:O19359010910", "Conservatoire de musique de Rimouski", "Official scope is music; no computing research graduate degree", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/prepare/designated-learning-institutions-list.html", "https://www.conservatoire.gouv.qc.ca/fr/conservatoires/rimouski/", "Institutional page describes music performance training from primary through second-cycle university only.", "confirmed", "No", "none"),
    ("ca:dli:O19332928222", "OCAD University", "Official scope is art/design; no computing research graduate degree", "http://nscad.ca/en/home/default.aspx", "https://gradadmissions.ocadu.ca/graduate-programs", "OCAD's official list contains seven art/design/media master's programs including Digital Futures, but no CS/SE research graduate degree. The exclusion is supportable, while the stored primary URL is for a different institution (NSCAD).", "confirmed_with_source_defect", "Replace the NSCAD URL with OCAD's official graduate-program list and note the Digital Futures boundary decision.", "high"),
    ("ca:dli:O122051172047", "College of Emmanuel and St Chad", "Official scope is theology; no computing research graduate degree", "https://www.cicic.ca/873/College_of_Emmanuel_and_St._Chad.canada?id=3614", "https://migration.emmanuelstchad.ca/programs/", "Official college inventory lists theology/ministry degrees only (MDiv, BTh, MTS, LTh, DMin).", "confirmed", "No", "none"),
    ("ca:dli:O19395677925", "Université de Hearst", "No computing research graduate degree in official inventory", "http://www.uhearst.ca/english", "https://uhearst.ca/programmes/nos-programmes-detudes/", "Current official inventory lists business, interdisciplinary social sciences, psychology, and a graduate psychotherapy diploma; no computing research degree.", "confirmed", "Replace obsolete English landing page with the current official program inventory.", "medium"),
    ("ca:dli:O19359010924", "Conservatoire de musique de Trois-Rivières", "Official scope is music; no computing research graduate degree", "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/prepare/designated-learning-institutions-list.html", "https://www.conservatoire.gouv.qc.ca/fr/conservatoires/trois-rivieres/", "Institutional page describes music-performance education through second-cycle university; no computing graduate program.", "confirmed", "No", "none"),
]
for iid, institution, claim, primary, second, finding, result, correction, severity in sample_exclusions:
    add("Canada", "universe_exclusion_sample", "", iid, institution, "", "exclusion_scope", claim,
        primary, second, finding, result, correction, severity,
        "Deterministic SHA-256 sample; negative screen checked against the institution's own program inventory.")


us_checks = [
    ("us:ipeds:195003:program:phd:computing-and-information-sciences-phd", "us:ipeds:195003", "Rochester Institute of Technology", "Computing and Information Sciences PhD", "Typically full tuition plus RA stipend/TA salary; not a universal-guarantee wording", "https://www.rit.edu/study/computing-and-information-sciences-phd", "https://www.rit.edu/computing/phd-computing-and-information-sciences", "A separate department page says 100% of full-time students are fully supported; central doctoral admissions still uses 'typically'. Existing wording is conservative.", "confirmed", "No", "none"),
    ("us:ipeds:233921:program:phd:computer-science-phd", "us:ipeds:233921", "Virginia Polytechnic Institute and State University", "Computer Science PhD", "100% of Fall 2026 admitted PhD students receive five-year offer, excluding summers", "https://website.cs.vt.edu/academic/graduate/future-grads/doctorate.html", "https://graduateschool.vt.edu/funding/assistantships.html", "Graduate School confirms stipend, proportional in-state tuition, conditional out-of-state waiver and health subsidy; comprehensive/CFE fees and summer tuition are not covered by the standard assistantship.", "partial", "Add explicit mandatory-fee/CFE liability and preserve that the 100% statement is a department/Fall-2026 cohort claim.", "medium"),
    ("us:ipeds:110653:program:phd:software-engineering-phd", "us:ipeds:110653", "University of California-Irvine", "Software Engineering PhD", "ICS strives to award all admitted PhD students full funding; not unconditional", "https://informatics.ics.uci.edu/phd-software-engineering/", "https://grad.uci.edu/helparticles/funding-your-graduate-education/", "Graduate Division says most PhD students are supported through mixed sources and funding is coordinated departmentally. It does not convert 'strives' into a guarantee.", "confirmed", "No", "none"),
    ("us:ipeds:163286:program:phd:computer-science-phd", "us:ipeds:163286", "University of Maryland-College Park", "Computer Science PhD", "PhD students funded subject to satisfactory progress; exact guarantee terms should be checked", "https://www.cs.umd.edu/node/25572", "https://www.cs.umd.edu/grad/admissions-faq", "The official admissions FAQ explicitly says all PhD students are funded through TA/RA subject to progress but that no funding guarantee is provided as part of the admission offer.", "correction_required", "Revise funding_status to say explicitly 'no guarantee in the admission offer'; do not pass a guaranteed-funding hard gate before reviewing the individual offer.", "high"),
    ("us:ipeds:228778:program:phd:computer-science-phd", "us:ipeds:228778", "The University of Texas at Austin", "Computer Science PhD", "Most PhD students receive first-five-year support; no universal guarantee", "https://www.cs.utexas.edu/graduate/cost-and-aid", "https://www.cs.utexas.edu/~gracs/pages/gracs-primer.html", "Official department page says 'most' and conditions support on performance/fund availability; department-hosted student guide says terms are specified in admission letters and some GRAs are secured after year one.", "confirmed", "No", "none"),
]
for pid, iid, institution, program, claim, primary, second, finding, result, correction, severity in us_checks:
    add("United States", "retained_program_funding_sample", pid, iid, institution, program,
        "funding_wording", claim, primary, second, finding, result, correction, severity,
        "Selected deterministically by SHA-256(program_id): first five retained US rows; wordings span typically/100%/strives/funded-subject-to-progress/most.")


fields = list(rows[0])
with (OUT / "second_source_checks.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

corrections = [row for row in rows if row["correction_needed"] != "No"]
with (OUT / "corrections_needed.csv").open("w", newline="", encoding="utf-8-sig") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(corrections)

counts = {
    "checks_total": len(rows),
    "canada_retained_routes": len(ca),
    "canada_retained_claim_checks": sum(r["region"] == "Canada" and r["record_type"] == "retained_program" for r in rows),
    "canada_exclusions_sampled": sum(r["record_type"] == "universe_exclusion_sample" for r in rows),
    "us_retained_funding_sampled": sum(r["record_type"] == "retained_program_funding_sample" for r in rows),
    "corrections_or_clarifications": len(corrections),
    "high_severity_corrections": sum(r["severity"] == "high" and r["correction_needed"] != "No" for r in rows),
}
errors = []
if counts["canada_retained_routes"] != 8 or counts["canada_retained_claim_checks"] != 32:
    errors.append("Canadian retained-route coverage incomplete")
if counts["canada_exclusions_sampled"] < 5:
    errors.append("Canadian exclusion sample below five")
if counts["us_retained_funding_sampled"] < 5:
    errors.append("US retained funding sample below five")
if any(not r["primary_source_url"] or not r["second_source_url"] for r in rows):
    errors.append("missing primary or second source URL")
if len({r["check_id"] for r in rows}) != len(rows):
    errors.append("duplicate check_id")

validation = {
    "generated_at": CHECKED,
    "status": "pass" if not errors else "fail",
    "counts": counts,
    "sampling": {
        "canada_exclusions": "Sort source exclusion_log.csv by SHA-256(institution_id), then institution_id; take first five.",
        "us_retained": "Filter screening_decision=retained; sort by SHA-256(program_id); take first five. These five also span materially different funding wordings.",
    },
    "checks": {
        "all_eight_canadian_retained_routes_covered": counts["canada_retained_routes"] == 8 and counts["canada_retained_claim_checks"] == 32,
        "four_claim_categories_each_canadian_route": all(sum(r["program_id"] == pid and r["record_type"] == "retained_program" for r in rows) == 4 for pid, *_ in ca.values()),
        "at_least_five_canadian_exclusions": counts["canada_exclusions_sampled"] >= 5,
        "at_least_five_us_retained_finalists": counts["us_retained_funding_sampled"] >= 5,
        "all_checks_have_primary_and_second_source": all(r["primary_source_url"] and r["second_source_url"] for r in rows),
        "source_datasets_unchanged_by_this_script": True,
    },
    "material_findings": [
        "Calgary PhD direct-from-bachelor eligibility is not explicit enough to record as yes.",
        "Calgary MSc and PhD recurring deadlines were incorrectly assigned calendar-year 2027.",
        "UMD's official FAQ says funding is not guaranteed in the admission offer.",
        "OCAD's stored exclusion source URL points to NSCAD, a different institution.",
        "UBC department and Graduate School pages disagree on whether the upcoming intake deadline is configured.",
    ],
    "errors": errors,
}
(OUT / "validation.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

readme = """# Independent cross-region second-source validation\n\nChecked 2026-09-09 using official institutional pages. No source dataset was edited.\n\nCoverage:\n\n- All eight retained Canadian routes: four checks each for funding wording, bachelor's/international eligibility, current faculty appointment, and deadline-cycle labeling.\n- Five Canadian universe exclusions selected deterministically by SHA-256 of institution ID.\n- Five retained U.S. finalists selected deterministically by SHA-256 of program ID; the sample spans five distinct funding wordings.\n\n`second_source_checks.csv` is the full audit trail. `corrections_needed.csv` is the actionable subset. Results distinguish confirmation, partial corroboration, non-confirmation, and correction-required findings. Different official pages were used where a program-level second page existed; when only one current program-level page carried the precise amount, the second official page corroborates policy/structure and that limitation is stated.\n\nMaterial corrections are not applied here because this task is independently read-only with respect to the source datasets.\n"""
(EVIDENCE / "README.md").write_text(readme, encoding="utf-8")
(EVIDENCE / "method.json").write_text(json.dumps({
    "checked_date": CHECKED,
    "official_only": True,
    "search_snippets": "Discovery only; output records the official destination URLs.",
    "canada_exclusion_sample_ids": [item[0] for item in sample_exclusions],
    "us_sample_program_ids": [item[0] for item in us_checks],
    "sha256_second_source_checks": hashlib.sha256((OUT / "second_source_checks.csv").read_bytes()).hexdigest(),
}, indent=2) + "\n", encoding="utf-8")

if errors:
    raise SystemExit("validation failed: " + "; ".join(errors))
print(json.dumps(counts, indent=2))
