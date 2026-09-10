"""Build the conservative Europe deep-review deliverables.

The records are deliberately explicit about cycle and funding uncertainty.  A faculty
match is never encoded as evidence of an advertised position or guaranteed funding.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "data" / "processed" / "deep_review" / "europe"
EVIDENCE = ROOT / "evidence" / "deep_review" / "europe"
MANIFEST = ROOT / "data" / "manifests" / "deep_review" / "europe"
CHECKED = "2026-09-09"
sys.path.insert(0, str(ROOT / "src"))
from graduate_audit.schema import (  # noqa: E402
    EXCLUSION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
    professor_id as make_professor_id,
    source_id as make_source_id,
)


ID_MAP = {
    "eu-cambridge-phd-cs": "ror:013meh722:program:phd:phd-in-computer-science",
    "eu-ucl-cs-mphil-phd": "ror:02jx3x895:program:integrated-or-structured-doctorate:computer-science-mphil-phd",
    "eu-imperial-phd-computing": "ror:041kmwe10:program:phd:phd-in-computing",
    "eu-eth-direct-doctorate-cs": "ror:05a28rw58:program:direct-entry-phd:direct-doctorate-in-computer-science",
    "eu-eth-doctorate-cs": "ror:05a28rw58:program:phd-requiring-a-master-s:doctoral-study-programme-in-computer-science",
    "eu-saarland-phd-cs": "ror:01jdpyv68:program:integrated-or-structured-doctorate:saarbr-cken-graduate-school-of-computer-science",
    "eu-kuleuven-phd-cs": "ror:05f950310:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science",
    "eu-aalto-dpcs-cs": "ror:020hwjq30:program:phd-requiring-a-master-s:doctoral-programme-in-science-computer-science",
    "eu-helsinki-dpcs": "ror:040af2s02:program:phd-requiring-a-master-s:doctoral-programme-in-science-computer-science",
    "eu-kth-phd-cs": "ror:026vcq606:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science",
    "eu-dtu-phd-compute": "ror:04qtj9h94:program:phd-requiring-a-master-s:phd-programme-dtu-compute",
    "eu-tartu-phd-it-cs": "ror:03z77qz90:program:phd-requiring-a-master-s:phd-in-information-technology-computer-science",
    "eu-luxembourg-phd-ce": "ror:036x5ad56:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science-and-computer-engineering",
    "eu-tudelft-phd-cs": "ror:02e2c7k09:program:phd-requiring-a-master-s:phd-vacancies-in-computer-science-software-engineering",
    "eu-tcd-phd-cs": "ror:02tyrky19:program:phd:phd-in-computer-science-and-statistics",
    "eu-ucd-phd-cs": "ror:05m7pjf47:program:phd:phd-computer-science",
    "eu-oxford-dphil-cs": "ror:052gg0110:program:phd:dphil-in-computer-science",
    "eu-edinburgh-phd-informatics": "ror:01nrxwf90:program:phd:phd-informatics",
}


def p(
    pid, iid, institution, country, name, route, eligible, entry, admissions,
    deadline, deadline_label, tuition, funding, funding_status, scores,
    recommendation, risk, question, url, english="English-medium program; formal test/waiver rules apply",
    english_url="", international="Yes, subject to credential equivalency", degree="Individual supervised research culminating in a thesis/defence",
):
    pid = ID_MAP[pid]
    if institution == "University of Tartu":
        iid = "ror:03z77qz90"
    labels = ["professor_alignment_score", "department_depth_score", "funding_score", "eligibility_score", "degree_admissions_score", "application_economics_score"]
    row = {
        "program_id": pid, "institution_id": iid, "institution_name": institution,
        "country": country, "program_name": name, "route_classification": route,
        "fall_2027_eligible": eligible, "degree_structure": degree,
        "entry_credential": entry, "english_status": english,
        "english_evidence_url": english_url or url, "international_eligibility": international,
        "admissions_model": admissions, "supervisor_contact_policy": "Check program instructions; faculty fit is not an open-position claim",
        "current_or_latest_deadline": deadline, "deadline_cycle_label": deadline_label,
        "fall_2027_deadline_status": "official" if "2027" in deadline and "not" not in deadline.lower() else "not yet published / latest-cycle only",
        "application_fee": "Not verified for Fall 2027 unless stated in tuition field",
        "current_international_tuition": tuition, "funding_model": funding,
        "funding_precision": "International-rate award coverage recorded only where the official source states it",
        "fall_2027_funding_status": funding_status, "faculty_match_count": "1",
        "recommendation": recommendation,
        "hard_gate_status": "hold—no Fall 2027 full-funding award/position verified" if eligible == "Yes" else "fail—entry credential or international route unresolved/incompatible",
        "retained_for_application": "No", "biggest_risk": risk, "unresolved_question": question,
        "program_url": url, "checked_date": CHECKED,
    }
    row.update(dict(zip(labels, scores)))
    row["overall_score"] = sum(scores)
    return row


programs = [
    p("eu-cambridge-phd-cs", "ror:013meh722", "University of Cambridge", "United Kingdom", "PhD in Computer Science", "immediate bachelor's-entry route", "Yes", "First-class honours/equivalent; a master's is increasingly desirable but not a formal universal prerequisite", "Central postgraduate application plus proposed research area and supervisor fit", "14 Oct 2026 or 8 Dec 2026 for main funding routes; 13 May 2027 final externally funded deadline", "official 2027/28 cycle", "2027/28 fee and maintenance liability must be checked; no award assumed", "Competitive Cambridge/Gates/departmental studentships; full international coverage is award-specific", "Not confirmed for applicant", (22, 15, 13, 10, 9, 2), "Outreach Before Decision", "Very high selectivity and no verified award", "Which 2027 studentship covers full overseas fees plus stipend?", "https://www.cst.cam.ac.uk/admissions/phd", english="Program and application materials are in English; proof rules depend on applicant history", english_url="https://www.postgraduate.study.cam.ac.uk/international/competence-english"),
    p("eu-ucl-cs-mphil-phd", "ror:02jx3x895", "University College London", "United Kingdom", "Computer Science MPhil/PhD", "immediate bachelor's-entry route", "Yes", "Relevant bachelor's at UK upper-second equivalent or stronger; exact Nigerian/US credential assessment is individual", "Research-degree application; identifying/contacting a potential supervisor is advised", "12 Feb 2027 and 16 Apr 2027 for October 2027 entry", "official 2027/28 cycle", "2027/28 UK and international fees shown as to be confirmed", "Department, doctoral-training and external awards; no universal international package", "Not confirmed for applicant", (27, 15, 8, 11, 9, 2), "Investigate Further", "Published 2027 tuition and a full award are both absent", "Is there an overseas-fee-covering studentship tied to software engineering/LLM reliability?", "https://www.ucl.ac.uk/study/prospective-students/graduate/courses/computer-science-mphilphd", english_url="https://www.ucl.ac.uk/prospective-students/graduate/english-language-requirements"),
    p("eu-imperial-phd-computing", "ror:041kmwe10", "Imperial College London", "United Kingdom", "PhD in Computing", "immediate bachelor's-entry route", "Yes", "Strong relevant first degree; project/supervisor-specific expectations apply", "Departmental PhD application and research-group/supervisor fit", "Fall 2027 deadline not yet verified", "latest available page; 2027 deadline not published in captured evidence", "International fee not verified for 2027/28", "Department states up to 30 fully funded PhD studentships annually for home and overseas candidates; selection is competitive", "Program-level availability stated, applicant award not confirmed", (29, 15, 21, 11, 9, 2), "Outreach Before Decision", "Funding is competitive rather than guaranteed", "Which 2027 studentship/research group would nominate this applicant?", "https://www.imperial.ac.uk/computing/prospective-students/phd/", english_url="https://www.imperial.ac.uk/study/apply/postgraduate-taught/english-language-requirements/"),
    p("eu-eth-direct-doctorate-cs", "ror:05a28rw58", "ETH Zurich", "Switzerland", "Direct Doctorate in Computer Science", "immediate bachelor's-entry route", "Yes", "Outstanding relevant bachelor's; highly selective direct-doctorate pathway", "Departmental direct-doctorate selection combining master's-level coursework and doctoral research", "Fall 2027 deadline not yet published", "latest official route page", "No tuition figure relied on in this review", "Doctoral candidates are commonly employed; direct-doctorate financial terms must be confirmed in the offer", "No Fall 2027 offer confirmed", (29, 15, 22, 10, 10, 4), "Outreach Before Decision", "Exceptional-entry threshold and no individual offer", "Will the direct-doctorate admission include an employment contract covering the whole route?", "https://inf.ethz.ch/doctorate/direct-doctorate-computer-science.html", english="Computer Science doctoral work can be completed in English; thesis-language rules permit English", english_url="https://ethz.ch/students/en/doctorate/transferable-skills/languages.html"),
    p("eu-eth-doctorate-cs", "ror:05a28rw58", "ETH Zurich", "Switzerland", "Doctoral Study Programme in Computer Science", "master's-required future route", "No", "Relevant university master's degree required", "Professor-backed doctoral admission, normally with an employment relationship", "Position/supervisor dependent; no Fall 2027 universal deadline", "rolling/position-specific", "No tuition figure relied on", "Most doctoral candidates are employed as scientific assistants; a specific position is required", "No Fall 2027 position and applicant lacks required master's", (29, 15, 22, 0, 6, 4), "Do Not Apply", "Master's requirement is not met for Fall 2027", "Revisit after a qualifying research master's", "https://inf.ethz.ch/doctorate.html", english_url="https://ethz.ch/students/en/doctorate/transferable-skills/languages.html"),
    p("eu-saarland-phd-cs", "ror:01jdpyv68", "Saarland University", "Germany", "Saarbrücken Graduate School of Computer Science", "immediate bachelor's-entry route", "Yes", "Exceptional bachelor's graduates may enter the preparatory/doctoral route directly", "Graduate-school application with research-area matching", "Fall 2027 deadline not yet published", "latest official program description", "No tuition figure relied on", "Official page mentions an EUR 800/month scholarship for direct-entry students; this is not treated as sufficient full support without additional coverage", "Insufficiently precise for full international cost coverage", (28, 15, 8, 11, 10, 5), "Investigate Further", "EUR 800/month alone is not a credible full-cost package", "What additional stipend, insurance, and fee coverage is guaranteed for 2027?", "https://www.uni-saarland.de/en/future/computerscience.html", english="Computer Science graduate programs are advertised in English", english_url="https://www.uni-saarland.de/en/future/computerscience.html"),
    p("eu-kuleuven-phd-cs", "ror:05f950310", "KU Leuven", "Belgium", "Doctoral Programme in Computer Science", "master's-required future route", "No", "Relevant master's or equivalent required", "Promoter initiates doctoral application; funding may be vacancy-, project-, or externally based", "No universal deadline; vacancy/supervisor dependent", "rolling/position-specific", "Doctoral fee/funding package not verified for Fall 2027", "No universal stipend; retain only a fully funded vacancy or written award", "No position; applicant lacks master's", (25, 14, 12, 0, 5, 4), "Do Not Apply", "Master's required and no funded vacancy identified", "Revisit funded vacancies after master's completion", "https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral", english="Official doctoral instructions require mastery of English", english_url="https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral"),
    p("eu-aalto-dpcs-cs", "ror:020hwjq30", "Aalto University", "Finland", "Aalto Doctoral Programme in Science — Computer Science", "master's-required future route", "No", "Applicable master's degree required", "Study-right application; full-time applicants must document at least six months of secured funding", "2027 dates not posted; latest page used monthly 2026 processing dates", "latest 2026 cycle", "No tuition fees for doctoral study", "Salary/grant is not guaranteed by admission; funding must be separately secured", "No Fall 2027 funding and applicant lacks master's", (25, 14, 10, 0, 6, 5), "Do Not Apply", "Admission does not fund the degree and master's is required", "Revisit salaried doctoral vacancies after master's", "https://www.aalto.fi/en/study-options/aalto-doctoral-programme-in-science", english="English is an official study language for the programme; proof rules apply", english_url="https://www.aalto.fi/en/doctoral-education/how-to-apply-for-doctoral-studies"),
    p("eu-helsinki-dpcs", "ror:040af2s02", "University of Helsinki", "Finland", "Doctoral Programme in Science — Computer Science", "master's-required future route", "No", "Relevant master's/equivalent required", "Doctoral study-right application with supervising arrangements; employment is separate", "2027 dates not posted; latest 2026 admissions rounds only", "latest 2026 cycle", "No doctoral tuition fees", "Study right does not include funding; salaried doctoral researcher calls are separate", "No Fall 2027 salary and applicant lacks master's", (24, 14, 8, 0, 6, 5), "Do Not Apply", "Master's required and study right is unfunded", "Revisit salaried calls after master's", "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes", english="All doctoral programmes can be completed in English", english_url="https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes"),
    p("eu-kth-phd-cs", "ror:026vcq606", "KTH Royal Institute of Technology", "Sweden", "Doctoral Programme in Computer Science", "position-only monitor", "No", "Second-cycle/master's qualification normally required", "Apply to an advertised doctoral position; admitted candidates are normally employees", "Vacancy-specific; no Fall 2027 position verified", "position-specific", "Not treated as tuition-funded student admission", "Most doctoral students receive salary through employment", "No Fall 2027 vacancy and applicant lacks second-cycle qualification", (28, 15, 22, 0, 6, 5), "Do Not Apply", "No qualifying master's and no 2027 vacancy", "Monitor only after satisfying second-cycle eligibility", "https://www.kth.se/en/studies/phd", english="Vacancies state English requirements; KTH doctoral guidance uses English", english_url="https://www.kth.se/en/studies/phd"),
    p("eu-dtu-phd-compute", "ror:04qtj9h94", "Technical University of Denmark", "Denmark", "PhD Programme — DTU Compute", "position-only monitor", "No", "Relevant master's/equivalent normally required", "Apply to an advertised salaried PhD vacancy", "Vacancy-specific; no Fall 2027 position verified", "position-specific", "No self-funded route retained", "Employment terms are vacancy-specific; no current 2027 vacancy was found", "No Fall 2027 vacancy and applicant lacks master's", (19, 13, 20, 0, 6, 5), "Do Not Apply", "Master's required and match is only moderate", "Monitor 2028+ vacancies in software systems/AI engineering", "https://www.dtu.dk/english/education/phd/intro", english="English requirement is vacancy/admissions specific", english_url="https://www.dtu.dk/english/education/phd/intro"),
    p("eu-tartu-phd-it-cs", "ror:03z77q656", "University of Tartu", "Estonia", "PhD in Information Technology — Computer Science", "master's-required future route", "No", "Relevant master's/equivalent required", "Doctoral admissions route with project/supervisor alignment", "Fall 2027 dates not published; current curriculum evidence is 2026/27", "latest 2026/27 cycle", "No international fee amount relied on", "Funding/employment must be verified for the specific doctoral place", "No 2027 award and applicant lacks master's", (17, 12, 10, 0, 6, 5), "Do Not Apply", "Master's required and no specific fully funded place", "Revisit funded doctoral calls after master's", "https://ut.ee/en/curriculum/computer-science", english="Official curriculum/admissions page provides English-language route and proficiency rules", english_url="https://ut.ee/en/curriculum/computer-science"),
    p("eu-luxembourg-phd-ce", "ror:036x5ad56", "University of Luxembourg", "Luxembourg", "Doctoral Programme in Computer Science and Computer Engineering", "master's-required future route", "No", "Relevant master's degree required", "Supervisor/project-based doctoral admission; vacancies carry separate employment terms", "Admissions possible throughout year; specific vacancy deadlines apply", "rolling/latest official page", "EUR 400 per semester on program page", "A live 2026 vacancy listed EUR 43,445 gross/year for 36 months, but it is not a Fall 2027 offer and requires a master's", "Precise current example only; not transferable to Fall 2027", (29, 14, 21, 0, 6, 4), "Do Not Apply", "Master's required; current funded vacancy is not a 2027 route", "Monitor future SnT/SVV vacancies after master's", "https://www.uni.lu/research-en/doctoral-education/dsse/computer-engineering/", english="English is the stated working language", english_url="https://www.uni.lu/research-en/doctoral-education/dsse/computer-engineering/"),
    p("eu-tudelft-phd-cs", "ror:02e2c7k09", "Delft University of Technology", "Netherlands", "PhD vacancies in Computer Science / Software Engineering", "position-only monitor", "No", "Vacancy-specific; Dutch PhD appointments normally expect a relevant master's", "Employment-vacancy application rather than cohort admission", "Vacancy-specific; no Fall 2027 vacancy verified", "position-specific", "No self-funded route retained", "Salaried employee appointment; salary and eligibility must be taken from each vacancy", "No Fall 2027 vacancy; master's-level eligibility expected", (29, 15, 23, 0, 7, 5), "Do Not Apply", "No Fall 2027 vacancy and master's expected", "Monitor 2028+ AI4SE/SERG vacancies after master's", "https://careers.tudelft.nl/", english="English requirements are vacancy-specific", english_url="https://careers.tudelft.nl/"),
    p("eu-tcd-phd-cs", "ror:02tyrky19", "Trinity College Dublin", "Ireland", "PhD in Computer Science and Statistics", "immediate bachelor's-entry route", "Yes", "Strong relevant honours bachelor's may be considered; supervisor/school approval required", "Research proposal and supervisor-supported school application", "30 Sep 2026 for September 2026; 31 Mar 2027 for March 2027", "latest published cycles, not Fall 2027", "2026/27 PhD non-EU fee not captured; MSc research non-EU page showed EUR 16,960 and must not be substituted", "Funding comes from competitive national/EU/industry/supervisor sources; no universal package", "No Fall 2027 full award verified", (19, 13, 9, 10, 8, 2), "Investigate Further", "Fall 2027 deadline, fee and full funding are unverified", "Will the school confirm a full non-EU stipend/fee award before application?", "https://www.tcd.ie/courses/postgraduate/postgraduate-research/engineering-mathematics-and-science/school-of-computer-science-and-statistics/", english="Program is delivered/supervised in English; formal proof rules apply", english_url="https://www.tcd.ie/study/international/how-to-apply/english-language-requirements/"),
    p("eu-ucd-phd-cs", "ror:05m7pjf47", "University College Dublin", "Ireland", "PhD Computer Science", "immediate bachelor's-entry route", "No", "Relevant honours bachelor's route appears structurally available, subject to supervisor and school", "Supervisor/project-backed research-degree application", "September 2027 application opens 1 Oct 2026", "official 2027 intake metadata", "EUR 15,440 per year non-EU full-time on the official course page", "No full international award verified", "No funding; official page also marks international non-EU suitability 'No'", (26, 14, 0, 0, 7, 1), "Do Not Apply", "Official course metadata says international non-EU suitability 'No'", "Is the non-EU 'No' field authoritative or a catalogue error, and is full funding available?", "https://hub.ucd.ie/usis/!W_HU_MENU.P_PUBLISH?AUDIENCE=&MAJR=T113&p_tag=COURSE", english="English-language institution; formal admissions proof rules apply", english_url="https://www.ucd.ie/global/study-at-ucd/english-language-requirements/", international="Unresolved: official course page marks international non-EU suitability 'No'"),
    p("eu-oxford-dphil-cs", "ror:052gg0110", "University of Oxford", "United Kingdom", "DPhil in Computer Science", "immediate bachelor's-entry route", "Yes", "Four-year relevant bachelor's with first/strong 2:1 equivalency, or three-year bachelor's plus master's", "Central graduate application with research statement and supervisor-area fit", "2027/28 application deadline not yet captured; page was partly 2026/27 when checked", "latest official page, mixed-cycle warning", "2027/28 international fee/award coverage not fully verified", "Clarendon/departmental and project awards are competitive; no award assumed", "No Fall 2027 award confirmed", (20, 15, 14, 9, 9, 2), "Investigate Further", "Extreme selectivity and unconfirmed full international funding", "Which official 2027 deadline guarantees consideration for overseas-fee-plus-stipend funding?", "https://www.ox.ac.uk/admissions/graduate/courses/dphil-computer-science", english_url="https://www.ox.ac.uk/admissions/graduate/international-applicants/english-language-requirements"),
    p("eu-edinburgh-phd-informatics", "ror:01nrxwf90", "University of Edinburgh", "United Kingdom", "PhD Informatics", "immediate bachelor's-entry route", "Yes", "Normally a UK 2:1 honours bachelor's or equivalent; supervisor/project expectations vary", "Research-degree application after identifying an appropriate supervisor", "Fall 2027 deadline not yet published", "latest 2026/27 funding and fee evidence", "2026/27 international Informatics research fee GBP 34,800/year", "School awards are competitive; historic/current IGS material referenced home/overseas tuition plus UKRI-rate stipend, but no 2027 award is confirmed", "No Fall 2027 award confirmed", (22, 15, 15, 11, 9, 2), "Outreach Before Decision", "Very high unfunded cost if scholarship fails", "Will a 2027 award cover GBP 34,800+ overseas fees and full stipend?", "https://informatics.ed.ac.uk/study-with-us/our-degrees/postgraduate-research-and-cdts/research-degrees", english_url="https://www.ed.ac.uk/studying/international/english/postgraduate"),
]


degree_types = {
    ID_MAP["eu-cambridge-phd-cs"]: "PhD",
    ID_MAP["eu-ucl-cs-mphil-phd"]: "Integrated or structured doctorate",
    ID_MAP["eu-imperial-phd-computing"]: "PhD",
    ID_MAP["eu-eth-direct-doctorate-cs"]: "Direct-entry PhD",
    ID_MAP["eu-saarland-phd-cs"]: "Integrated or structured doctorate",
    ID_MAP["eu-tcd-phd-cs"]: "PhD",
    ID_MAP["eu-ucd-phd-cs"]: "PhD",
    ID_MAP["eu-oxford-dphil-cs"]: "PhD",
    ID_MAP["eu-edinburgh-phd-informatics"]: "PhD",
}
position_monitors = {
    ID_MAP["eu-kth-phd-cs"], ID_MAP["eu-dtu-phd-compute"], ID_MAP["eu-tudelft-phd-cs"],
}
ucd_id = ID_MAP["eu-ucd-phd-cs"]


def standard_program(row):
    route = row["route_classification"]
    is_monitor = row["program_id"] in position_monitors
    is_excluded = (route == "master's-required future route") or row["program_id"] == ucd_id
    decision = "excluded" if is_excluded else "deep_review"
    recommendation = "Monitor for 2027 Position" if is_monitor else row["recommendation"]
    if is_monitor:
        plausibility = "Eligibility concern"
    elif is_excluded:
        plausibility = "Clearly ineligible" if row["program_id"] != ucd_id else "Insufficient evidence"
    elif row["program_id"] in {ID_MAP["eu-cambridge-phd-cs"], ID_MAP["eu-imperial-phd-computing"], ID_MAP["eu-eth-direct-doctorate-cs"], ID_MAP["eu-oxford-dphil-cs"]}:
        plausibility = "Reach"
    else:
        plausibility = "Plausible to reach"
    stipend_amount = ""
    stipend_currency = ""
    funding_duration = ""
    if row["program_id"] == ID_MAP["eu-saarland-phd-cs"]:
        stipend_amount, stipend_currency = "800/month (direct-entry page; not treated as full funding)", "EUR"
    elif row["program_id"] == ID_MAP["eu-luxembourg-phd-ce"]:
        stipend_amount, stipend_currency, funding_duration = "43445 gross/year (current vacancy example only)", "EUR", "3"
    elif row["program_id"] == ID_MAP["eu-edinburgh-phd-informatics"]:
        stipend_amount, stipend_currency, funding_duration = "20780/year (2025/26 UKRI-rate example only)", "GBP", "3.5"
    return {
        "program_id": row["program_id"], "institution_id": row["institution_id"],
        "institution_name": row["institution_name"], "country": row["country"],
        "program_name": row["program_name"],
        "degree_type": degree_types.get(row["program_id"], "PhD requiring a master's"),
        "department": "Computer Science / Computing / Informatics",
        "official_program_url": row["program_url"],
        "thesis_dissertation_requirement": row["degree_structure"],
        "research_credit_requirement": "Program-specific; not reduced to coursework-only study",
        "research_groups_labs": "See linked faculty row; one verified match does not establish department-wide capacity",
        "direct_from_bachelors_eligible": "yes" if route == "immediate bachelor's-entry route" and row["program_id"] != ucd_id else ("unclear; vacancy/credential-equivalency specific" if is_monitor else "no"),
        "international_student_eligible": "unresolved; official catalogue says non-EU No" if row["program_id"] == ucd_id else "yes; credential and visa conditions apply",
        "language_of_instruction": row["english_status"],
        "current_program_status": "Active/current official route checked 2026-09-09",
        "preliminary_fit": "yes",
        "screening_decision": decision,
        "exclusion_reason": row["biggest_risk"] if decision == "excluded" else "",
        "minimum_gpa": "Not numerically stated on the program evidence used",
        "minimum_gpa_policy": row["entry_credential"],
        "prerequisite_coursework": "Relevant computer science background; program/vacancy-specific details apply",
        "gre_policy": "Not verified as required; recheck the Fall 2027 application",
        "english_requirement_waiver": "Applicant-specific; verify from official English source " + row["english_evidence_url"],
        "fall_2027_deadline": row["current_or_latest_deadline"],
        "deadline_cycle_status": row["deadline_cycle_label"],
        "application_fee": row["application_fee"], "fee_currency": "",
        "fee_waiver_rules": "Not verified for Fall 2027",
        "multiple_applications_allowed": "Not verified", "separate_fees_required": "Not verified",
        "admissions_model": row["admissions_model"],
        "faculty_contact_expectation": row["supervisor_contact_policy"],
        "funding_model": row["funding_model"], "funding_status": row["fall_2027_funding_status"],
        "stipend_amount": stipend_amount, "stipend_currency": stipend_currency,
        "funding_duration_years": funding_duration,
        "tuition_coverage": "Not confirmed for applicant; international rate must be explicit in an offer",
        "mandatory_fee_coverage": "Not confirmed", "health_insurance_coverage": "Not confirmed",
        "summer_funding": "Not confirmed", "funding_conditions": row["funding_precision"],
        "supervisor_dependent_funding": "yes or position/award-specific",
        "phd_funding": row["funding_model"], "masters_funding": "Not applicable to this reviewed route",
        "scholarships_fellowships": "Only official competitive schemes/positions; no applicant award assumed",
        "professor_fit_score": row["professor_alignment_score"],
        "faculty_depth_score": row["department_depth_score"],
        "research_fit_score": row["professor_alignment_score"],
        "funding_score": row["funding_score"], "eligibility_score": row["eligibility_score"],
        "degree_admissions_score": row["degree_admissions_score"],
        "application_economics_score": row["application_economics_score"],
        "overall_score": row["overall_score"], "admission_plausibility": plausibility,
        "recommendation": recommendation, "biggest_risk": row["biggest_risk"],
        "unresolved_question": row["unresolved_question"], "single_professor_dependency": "yes; bounded pass retained one current match",
        "verification_status": "Official pages checked; cycle/funding limitations explicit",
        "notes": f"Route classification: {route}. No faculty match is an open-position claim. Not retained for application without verified full funding.",
    }


program_rows = [standard_program(row) for row in programs]


professors = [
    ("eu-cambridge-phd-cs", "Alastair Beresford", "Professor of Computer Security", "University of Cambridge", "https://www.cst.cam.ac.uk/people/arb33", "arb33@cam.ac.uk", "security and privacy of large distributed systems", "Strong systems-security adjacency to reliable infrastructure tooling; LLM program repair is not his stated core area", "Strong", "Current department profile verifies active appointment/research; no 2024–26 paper selected", "", "https://www.cst.cam.ac.uk/people/arb33", "profile_verified_recent_paper_not_selected"),
    ("eu-ucl-cs-mphil-phd", "Earl Barr", "Professor of Software Engineering", "University College London", "https://www.ucl.ac.uk/engineering/computer-science/research/research-groups-and-centres/software-systems-engineering-group/people", "", "software engineering, program repair, language models for code", "Direct fit to Terraform repair, LLM-code evaluation and empirical software engineering", "Very strong", "Automatic Semantic Augmentation of Language Model Prompts (for Code Summarization)", "2024", "https://discovery.ucl.ac.uk/view/people/EBARR53.date.html", "profile_and_recent_work_verified"),
    ("eu-imperial-phd-computing", "Cristian Cadar", "Professor of Software Reliability", "Imperial College London", "https://profiles.imperial.ac.uk/c.cadar", "c.cadar@imperial.ac.uk", "software reliability, testing, symbolic execution, fuzzing", "Excellent reliability/testing fit; applicant's LLM repair work offers a complementary angle", "Very strong", "Effective Fuzzing within CI/CD Pipelines", "2024", "https://srg.doc.ic.ac.uk/files/papers/pazzer-fuzzing-24.pdf", "profile_and_recent_work_verified"),
    ("eu-eth-direct-doctorate-cs", "Martin Vechev", "Professor of Computer Science", "ETH Zurich", "https://www.sri.inf.ethz.ch/people/martin", "", "secure and reliable intelligent systems, programming languages, AI for code", "Near-direct fit to reliable LLM-generated code and repair evaluation", "Very strong", "Instruction Tuning for Secure Code Generation", "2024", "https://www.sri.inf.ethz.ch/publications/jhe2024safecoder", "profile_and_recent_work_verified"),
    ("eu-eth-doctorate-cs", "Martin Vechev", "Professor of Computer Science", "ETH Zurich", "https://www.sri.inf.ethz.ch/people/martin", "", "secure and reliable intelligent systems, programming languages, AI for code", "Near-direct research fit, but the regular doctorate requires a master's", "Very strong", "Instruction Tuning for Secure Code Generation", "2024", "https://www.sri.inf.ethz.ch/publications/jhe2024safecoder", "profile_and_recent_work_verified"),
    ("eu-saarland-phd-cs", "Andreas Zeller", "Faculty / Professor", "Saarland University / CISPA", "https://cispa.de/en/people/c01aze", "", "automated debugging, testing, software security", "Direct intellectual fit to automated repair and evidence-backed debugging", "Very strong", "Current CISPA faculty evidence; recent paper not independently selected", "", "https://cispa.de/en/people/c01aze", "profile_verified_recent_paper_not_selected"),
    ("eu-kuleuven-phd-cs", "Wouter Joosen", "Full Professor; head of DistriNet", "KU Leuven", "https://distrinet.cs.kuleuven.be/people/WouterJoosen", "", "distributed software, security, continuous risk assessment", "Strong secure-software and systems fit; less direct on LLM repair", "Strong", "Run-time Threat Models for Systematic and Continuous Risk Assessment", "2024", "https://distrinet.cs.kuleuven.be/research/publications/2024", "profile_and_recent_work_verified"),
    ("eu-aalto-dpcs-cs", "Fabian Fagerholm", "Associate Professor", "Aalto University", "https://www.aalto.fi/en/department-of-computer-science/faculty-0", "", "empirical software engineering, developer experience, software practice", "Good empirical-SE/evaluation fit; weaker direct program-repair match", "Moderate", "Measuring End-user Developers' Episodic Experience of a Low-code Development Platform", "2024", "https://research.aalto.fi/en/persons/fabian-fagerholm/", "profile_and_recent_work_verified"),
    ("eu-helsinki-dpcs", "Mika Mäntylä", "Professor of Software Engineering", "University of Helsinki", "https://www.helsinki.fi/en/researchgroups/empirical-software-engineering/people", "", "software testing, maintenance, operations, NLP/ML for software engineering", "Strong empirical and ML-for-SE fit", "Strong", "Speed and Performance of Parserless and Unsupervised Anomaly Detection Methods on Software Logs", "2024", "https://researchportal.helsinki.fi/en/publications/speed-and-performance-of-parserless-and-unsupervised-anomaly-dete/", "profile_and_recent_work_verified"),
    ("eu-kth-phd-cs", "Martin Monperrus", "Professor of Software Technology", "KTH Royal Institute of Technology", "https://www.kth.se/profile/monp?l=en", "", "automated program repair, AI for code, software hardening", "Direct fit to LLM-based repair and reliable developer tooling", "Very strong", "KTH official 2024 profile describes automatic program repair and AI for code", "2024", "https://www.kth.se/forskning/sarskilda-forskningssatsningar/forskningsprogram-kaw/wasp/nyheter/kth-professorn-martin-monperrus-far-prestigefyllt-pris-for-nytt-satt-att-anvanda-maskininlarning-1.1321457", "profile_and_recent_official_evidence_verified"),
    ("eu-dtu-phd-compute", "Ekkart Kindler", "Associate Professor", "Technical University of Denmark", "https://orbit.dtu.dk/en/persons/ekkart-kindler/", "", "model-based software engineering, formal methods, process modelling", "Moderate fit to reliable software generation; weak direct LLM-repair evidence", "Moderate", "Bringing Machine Learning Models Beyond the Experimental Stage with Explainable AI", "2025", "https://orbit.dtu.dk/en/persons/ekkart-kindler/", "profile_and_recent_work_verified"),
    ("eu-tartu-phd-it-cs", "Marlon Dumas", "Professor of Information Systems", "University of Tartu", "https://ut.ee/en/employee/marlon-dumas", "", "business process management, process mining, service-oriented computing", "Some evaluation/workflow overlap but weak direct fit to program repair", "Weak", "Current university profile used; recent official paper not independently verified", "", "https://ut.ee/en/employee/marlon-dumas", "profile_verified_recent_paper_not_selected"),
    ("eu-luxembourg-phd-ce", "Lionel Briand", "Professor / head of SVV research group", "University of Luxembourg", "https://www.uni.lu/snt-en/people/lionel-briand/", "", "software verification and validation, testing, trustworthy AI-enabled systems", "Excellent match to evidence-backed evaluation, repair and trustworthy software", "Very strong", "Systematic Evaluation of Deep Learning Models for Log-based Failure Prediction", "2024", "https://orbilu.uni.lu/profile?uid=50001049", "profile_and_recent_work_verified"),
    ("eu-tudelft-phd-cs", "Arie van Deursen", "Professor of Software Engineering", "Delft University of Technology", "https://research.tudelft.nl/en/persons/a-van-deursen/", "", "AI for software engineering, testing, architecture, empirical SE", "Excellent AI4SE and program-analysis fit", "Very strong", "Context-Aware Automated Sprint Plan Generation for Agile Software Development", "2024", "https://se.ewi.tudelft.nl/ai4fintech/tracks/01_software_analytics.html", "profile_and_recent_work_verified"),
    ("eu-tcd-phd-cs", "Siobhán Clarke", "Professor of Software Systems", "Trinity College Dublin", "https://www.tcd.ie/research/profiles/index.php?profile=sclarke&prpublications=true", "siobhan.clarke@tcd.ie", "dynamic software systems, services, edge/IoT, ML-enabled systems", "Good software-systems fit; less direct on repair or code LLMs", "Moderate", "Dynamic Service Placement in Edge Computing: A Comparative Evaluation of Nature-Inspired Algorithms", "2024", "https://www.tcd.ie/research/profiles/index.php?profile=sclarke&prpublications=true", "profile_and_recent_work_verified"),
    ("eu-ucd-phd-cs", "Liliana Pasquale", "Associate Professor", "University College Dublin", "https://www.ucd.ie/cs/t4media/Guide%20for%20Applicants_EoI.for.MSCA-PF.2025.v02.pdf", "liliana.pasquale@ucd.ie", "secure software engineering, AI for secure development, security logs", "Excellent match to LLM coding assistants and evidence/assurance for secure software", "Very strong", "Current supervised PhD topic: Large Language Models as Coding Assistants for Secure Software Development", "2026", "https://ucdcs-research.ucd.ie/node/1190/", "profile_and_current_supervision_verified"),
    ("eu-oxford-dphil-cs", "Michael Wooldridge", "Ashall Professor of Foundations of Artificial Intelligence", "University of Oxford", "https://www.cs.ox.ac.uk/people/michael.wooldridge/", "mjw@cs.ox.ac.uk", "multi-agent systems, AI foundations, reasoning", "Good agent-evaluation adjacency, but weak direct software-repair evidence", "Moderate", "Official 2024 appointment as AI research theme head/Ashall Professor", "2024", "https://www.cs.ox.ac.uk/news/2391-full.html", "profile_and_recent_official_evidence_verified"),
    ("eu-edinburgh-phd-informatics", "David Aspinall", "Professor of Software Safety and Security", "University of Edinburgh", "https://www.research.ed.ac.uk/en/persons/david-aspinall/", "", "software safety, security, formal verification, robust ML security", "Strong reliability/verification fit; less direct on program repair", "Strong", "Formally Verifying Robustness and Generalisation of Network Intrusion Detection Models", "2025", "https://www.research.ed.ac.uk/en/persons/david-aspinall/", "profile_and_recent_work_verified"),
]


prof_fields = ["program_id", "full_name", "title", "institution_name", "current_appointment_url", "official_email", "research_themes", "fit_explanation", "fit_strength", "recent_work_title", "recent_work_year", "recent_work_url", "verification_status"]
prof_rows = []
for row in professors:
    data = dict(zip(prof_fields[:13], row))
    data["program_id"] = ID_MAP[data["program_id"]]
    data.update({
        "recruiting_status": "Recruiting status unknown",
        "recruiting_evidence": "No Fall 2027 opening verified",
        "contact_appropriate": "Yes, only for research-fit/funding clarification; not as an assumed vacancy",
        "verification_status": row[-1], "checked_date": CHECKED,
    })
    prof_rows.append(data)

program_by_id = {row["program_id"]: row for row in program_rows}
professor_rows = []
for row in prof_rows:
    program = program_by_id[row["program_id"]]
    professor_rows.append({
        "professor_id": make_professor_id(program["institution_id"], row["full_name"]),
        "institution_id": program["institution_id"], "institution_name": program["institution_name"],
        "program_id": row["program_id"], "program_name": program["program_name"],
        "full_name": row["full_name"], "department": program["department"],
        "faculty_position": row["title"], "appointment_status": "Current official institutional profile checked",
        "can_supervise_program": "Potentially; role fit verified but Fall 2027 capacity not verified",
        "official_faculty_url": row["current_appointment_url"], "official_email": row["official_email"],
        "research_themes": row["research_themes"], "fit_explanation": row["fit_explanation"],
        "fit_strength": row["fit_strength"], "recent_work_1": row["recent_work_title"],
        "recent_work_1_url": row["recent_work_url"], "recent_work_1_year": row["recent_work_year"],
        "recent_work_2": "", "recent_work_2_url": "", "recent_work_2_year": "",
        "recent_work_3": "", "recent_work_3_url": "", "recent_work_3_year": "",
        "sustained_research_evidence": "Current official profile plus the recent-work evidence shown; partial rows are explicitly labelled",
        "recruiting_evidence": "No Fall 2027 opening verified; not inferred from fit, publications, grants, or current students",
        "recruiting_status": "Recruiting status unknown",
        "prospective_student_instructions": "Use program instructions; ask a focused fit/funding question only where contact is appropriate",
        "contacting_faculty_appropriate": "yes, for fit/capacity clarification; not as an assumed vacancy",
        "already_contacted": "unknown; no email-system access in this regional pass",
        "last_contact_date": "", "previous_outcome": "", "outreach_priority": "After administrative eligibility and funding gates",
        "outreach_score": "", "recommended_outreach_angle": "Connect TerraProbe/Evidex to the verified research themes without inventing contributions",
        "specific_question_goal": "Whether Fall 2027 supervision and full international funding could exist for this research direction",
        "openalex_author_id": "", "orcid": "", "verification_status": row["verification_status"],
        "notes": "Faculty match is not evidence of an open or funded position.",
    })


source_rows = []
sid = 0
for row in programs:
    for claim_type, url, note in [
        ("program_admissions", row["program_url"], "Official program/admissions page; cycle label preserved in deep_programs.csv"),
        ("english", row["english_evidence_url"], "Official English-language or admissions evidence; waivers/test thresholds remain applicant-specific"),
    ]:
        sid += 1
        source_rows.append({"source_id": f"EU-S{sid:03d}", "program_id": row["program_id"], "entity": row["institution_name"], "claim_type": claim_type, "source_url": url, "official_source": "Yes", "access_status": "accessible or indexed official page", "cycle_scope": row["deadline_cycle_label"], "evidence_note": note, "checked_date": CHECKED})
for row in prof_rows:
    for claim_type, url, note in [
        ("faculty_appointment", row["current_appointment_url"], "Official institutional profile/group page used to verify current role and research themes"),
        ("recent_work", row["recent_work_url"], "Official repository/profile/paper evidence; absence of a selected recent paper is explicitly marked"),
    ]:
        sid += 1
        source_rows.append({"source_id": f"EU-S{sid:03d}", "program_id": row["program_id"], "entity": row["full_name"], "claim_type": claim_type, "source_url": url, "official_source": "Yes", "access_status": "accessible or indexed official page", "cycle_scope": "current at 2026-09-09", "evidence_note": note, "checked_date": CHECKED})

supplemental_sources = [
    ("eu-eth-direct-doctorate-cs", "funding", "https://ethz.ch/en/doctorate.html", "Official ETH overview states that most doctoral candidates are employed as scientific assistants; an individual contract is still required."),
    ("eu-eth-doctorate-cs", "funding", "https://ethz.ch/en/doctorate.html", "Official ETH overview states that most doctoral candidates are employed as scientific assistants; an individual contract is still required."),
    ("eu-luxembourg-phd-ce", "funding_current_example", "https://www.uni.lu/en/jobs/doctoral-researcher-in-computer-science/", "Official live vacancy supplied a precise current salary example; it is not represented as a Fall 2027 opening."),
    ("eu-tudelft-phd-cs", "vacancy_model", "https://careers.tudelft.nl/", "Official careers portal establishes the employment-vacancy application model; no Fall 2027 vacancy was present."),
    ("eu-tcd-phd-cs", "fees", "https://www.tcd.ie/courses/postgraduate/fees/", "Official 2026/27 fee source; the MSc research amount is explicitly not substituted for the PhD fee."),
    ("eu-ucd-phd-cs", "program_fees_international", "https://hub.ucd.ie/usis/!W_HU_MENU.P_PUBLISH?AUDIENCE=&MAJR=T113&p_tag=COURSE", "Official course record supplies the non-EU fee and the contradictory non-EU suitability field."),
    ("eu-edinburgh-phd-informatics", "funding", "https://informatics.ed.ac.uk/study-with-us/our-degrees/postgraduate-research-and-cdts/postgraduate-research-funding-opportunities-0", "Official school funding page; award availability is competitive and cycle-specific."),
    ("eu-edinburgh-phd-informatics", "fees", "https://registryservices.ed.ac.uk/tuition-fees/find/postgraduate-research/2026-2027/research-degrees", "Official 2026/27 fee schedule; not projected to 2027/28."),
]
for pid, claim_type, url, note in supplemental_sources:
    pid = ID_MAP[pid]
    sid += 1
    source_rows.append({"source_id": f"EU-S{sid:03d}", "program_id": pid, "entity": next(r["institution_name"] for r in programs if r["program_id"] == pid), "claim_type": claim_type, "source_url": url, "official_source": "Yes", "access_status": "accessible or indexed official page", "cycle_scope": "current/latest-cycle, not projected", "evidence_note": note, "checked_date": CHECKED})

standard_source_rows = []
for row in source_rows:
    program = program_by_id[row["program_id"]]
    standard_source_rows.append({
        "source_id": make_source_id(row["source_url"]),
        "institution_id": program["institution_id"], "institution_name": program["institution_name"],
        "program_id": row["program_id"], "program_or_professor": row["entity"],
        "claim_type": row["claim_type"], "exact_claim_supported": row["evidence_note"],
        "source_title": row["entity"] + " — official evidence", "publisher": program["institution_name"],
        "publication_date": "", "url": row["source_url"],
        "source_type": "official program/profile/repository page", "official_or_secondary": "official",
        "date_accessed": CHECKED, "admissions_cycle": row["cycle_scope"], "confidence": "high" if "accessible" in row["access_status"] else "medium",
        "verification_status": row["access_status"], "access_note": "Search snippets were discovery only; final claim points to the official destination. Recheck cycle-specific facts when 2027 material opens.",
    })


contacts_by_program = {
    "eu-cambridge-phd-cs": ("Postgraduate admissions", "", "https://www.cst.cam.ac.uk/admissions/phd"),
    "eu-ucl-cs-mphil-phd": ("Computer Science research admissions", "", "https://www.ucl.ac.uk/study/prospective-students/graduate/courses/computer-science-mphilphd"),
    "eu-imperial-phd-computing": ("Department of Computing PhD admissions", "", "https://www.imperial.ac.uk/computing/prospective-students/phd/"),
    "eu-eth-direct-doctorate-cs": ("D-INFK doctoral administration", "", "https://inf.ethz.ch/doctorate.html"),
    "eu-eth-doctorate-cs": ("D-INFK doctoral administration", "", "https://inf.ethz.ch/doctorate.html"),
    "eu-saarland-phd-cs": ("Saarland Graduate School admissions", "", "https://www.uni-saarland.de/en/future/computerscience.html"),
    "eu-kuleuven-phd-cs": ("Doctoral admissions", "", "https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral"),
    "eu-aalto-dpcs-cs": ("Doctoral Programme in Science services", "", "https://www.aalto.fi/en/study-options/aalto-doctoral-programme-in-science"),
    "eu-helsinki-dpcs": ("Doctoral admissions", "", "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes"),
    "eu-kth-phd-cs": ("KTH doctoral recruitment", "", "https://www.kth.se/en/studies/phd"),
    "eu-dtu-phd-compute": ("DTU Compute", "compute@compute.dtu.dk", "https://www.compute.dtu.dk/Sections/SofSys"),
    "eu-tartu-phd-it-cs": ("Doctoral admissions", "", "https://ut.ee/en/curriculum/computer-science"),
    "eu-luxembourg-phd-ce": ("Doctoral School in Science and Engineering", "", "https://www.uni.lu/research-en/doctoral-education/dsse/computer-engineering/"),
    "eu-tudelft-phd-cs": ("TU Delft recruitment", "", "https://careers.tudelft.nl/"),
    "eu-tcd-phd-cs": ("Research admissions", "research.admissions@tcd.ie", "https://www.tcd.ie/courses/postgraduate/postgraduate-research/engineering-mathematics-and-science/school-of-computer-science-and-statistics/"),
    "eu-ucd-phd-cs": ("School of Computer Science", "computerscience@ucd.ie", "https://www.ucd.ie/cs/study/researchdegrees/"),
    "eu-oxford-dphil-cs": ("Graduate admissions", "", "https://www.ox.ac.uk/admissions/graduate/courses/dphil-computer-science"),
    "eu-edinburgh-phd-informatics": ("Informatics postgraduate research admissions", "phd-admissions@inf.ed.ac.uk", "https://informatics.ed.ac.uk/study-with-us/our-degrees/postgraduate-research-and-cdts/research-degrees"),
}
contacts_by_program = {ID_MAP[key]: value for key, value in contacts_by_program.items()}
admin_rows = []
for row in programs:
    office, email, url = contacts_by_program[row["program_id"]]
    admin_rows.append({"program_id": row["program_id"], "institution_name": row["institution_name"], "office": office, "email": email, "official_contact_url": url, "recommended_question": row["unresolved_question"], "checked_date": CHECKED})


downgrades = []
for row in programs:
    standard = program_by_id[row["program_id"]]
    action = "deep exclusion" if standard["screening_decision"] == "excluded" else "deep review downgrade/hold"
    downgrades.append({
        "institution_id": row["institution_id"], "institution_name": row["institution_name"],
        "country": row["country"], "program_id": row["program_id"], "program_name": row["program_name"],
        "stage_of_exclusion": action, "primary_exclusion_reason": row["biggest_risk"],
        "supporting_evidence": f"{row['funding_status'] if 'funding_status' in row else row['fall_2027_funding_status']}; reversible question: {row['unresolved_question']}",
        "source_url": row["program_url"], "confidence": "high" if standard["screening_decision"] == "excluded" else "medium",
        "manual_verification": "yes; official page reviewed and cycle uncertainty preserved", "date_checked": CHECKED,
    })


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


write_csv(OUT / "deep_programs.csv", program_rows, PROGRAM_COLUMNS)
write_csv(OUT / "professors.csv", professor_rows, PROFESSOR_COLUMNS)
write_csv(OUT / "sources.csv", standard_source_rows, SOURCE_COLUMNS)
write_csv(OUT / "admin_contacts.csv", admin_rows, list(admin_rows[0]))
write_csv(OUT / "exclusion_or_downgrade.csv", downgrades, EXCLUSION_COLUMNS)


allowed_routes = {"immediate bachelor's-entry route", "master's-required future route", "research master's", "position-only monitor"}
errors = []
if len(programs) != 18:
    errors.append("expected 18 programs (12 original + 6 added)")
if len({r["program_id"] for r in programs}) != len(programs):
    errors.append("duplicate program_id")
if any(r["route_classification"] not in allowed_routes for r in programs):
    errors.append("invalid route classification")
if any(not r["recommendation"] for r in programs):
    errors.append("blank recommendation")
if any(r["retained_for_application"] == "Yes" and r["fall_2027_funding_status"] != "Confirmed for applicant" for r in programs):
    errors.append("unfunded route retained")
if any(r["recruiting_status"] != "Recruiting status unknown" for r in professor_rows):
    errors.append("faculty recruiting inference present")
if {r["program_id"] for r in programs} != {r["program_id"] for r in professor_rows}:
    errors.append("program/professor coverage mismatch")
if {r["program_id"] for r in programs} != {r["program_id"] for r in admin_rows}:
    errors.append("program/admin coverage mismatch")
if any(r["recommendation"] != "Monitor for 2027 Position" for r in program_rows if r["program_id"] in position_monitors):
    errors.append("position-only route incorrectly rejected instead of monitored")
if tuple(program_rows[0]) != PROGRAM_COLUMNS:
    errors.append("program output does not match PROGRAM_COLUMNS")
if tuple(professor_rows[0]) != PROFESSOR_COLUMNS:
    errors.append("professor output does not match PROFESSOR_COLUMNS")
if tuple(standard_source_rows[0]) != SOURCE_COLUMNS:
    errors.append("source output does not match SOURCE_COLUMNS")
if tuple(downgrades[0]) != EXCLUSION_COLUMNS:
    errors.append("exclusion output does not match EXCLUSION_COLUMNS")

validation = {
    "generated_at": CHECKED,
    "status": "pass" if not errors else "fail",
    "counts": {
        "deep_programs": len(program_rows), "professors": len(professor_rows),
        "sources": len(standard_source_rows), "admin_contacts": len(admin_rows),
        "exclusions_or_downgrades": len(downgrades),
        "immediate_bachelors_entry": sum(r["route_classification"] == "immediate bachelor's-entry route" for r in programs),
        "masters_required_future": sum(r["route_classification"] == "master's-required future route" for r in programs),
        "research_masters": sum(r["route_classification"] == "research master's" for r in programs),
        "position_only_monitor": sum(r["route_classification"] == "position-only monitor" for r in programs),
        "fall_2027_eligible_yes": sum(r["fall_2027_eligible"] == "Yes" for r in programs),
        "screening_deep_review": sum(r["screening_decision"] == "deep_review" for r in program_rows),
        "screening_retained": sum(r["screening_decision"] == "retained" for r in program_rows),
        "screening_excluded": sum(r["screening_decision"] == "excluded" for r in program_rows),
        "monitor_for_2027_position": sum(r["recommendation"] == "Monitor for 2027 Position" for r in program_rows),
    },
    "checks": {
        "all_program_ids_unique": len({r["program_id"] for r in programs}) == len(programs),
        "all_routes_enum_valid": all(r["route_classification"] in allowed_routes for r in programs),
        "program_columns_exact": tuple(program_rows[0]) == PROGRAM_COLUMNS,
        "professor_columns_exact": tuple(professor_rows[0]) == PROFESSOR_COLUMNS,
        "source_columns_exact": tuple(standard_source_rows[0]) == SOURCE_COLUMNS,
        "exclusion_columns_exact": tuple(downgrades[0]) == EXCLUSION_COLUMNS,
        "original_12_program_ids_reused": set(ID_MAP.values()) - {ID_MAP[k] for k in ["eu-luxembourg-phd-ce", "eu-tudelft-phd-cs", "eu-tcd-phd-cs", "eu-ucd-phd-cs", "eu-oxford-dphil-cs", "eu-edinburgh-phd-informatics"]} <= {r["program_id"] for r in program_rows},
        "every_program_has_professor_row": {r["program_id"] for r in programs} == {r["program_id"] for r in professor_rows},
        "every_program_has_admin_contact_route": {r["program_id"] for r in programs} == {r["program_id"] for r in admin_rows},
        "no_faculty_match_encoded_as_recruiting": all(r["recruiting_status"] == "Recruiting status unknown" for r in professor_rows),
        "no_unfunded_route_retained": not any(r["screening_decision"] == "retained" and "confirmed" not in r["funding_status"].lower() for r in program_rows),
        "position_only_routes_are_monitors": all(r["recommendation"] == "Monitor for 2027 Position" for r in program_rows if r["program_id"] in position_monitors),
        "scores_sum_to_components": all(r["overall_score"] == sum(int(r[k]) for k in ["professor_alignment_score", "department_depth_score", "funding_score", "eligibility_score", "degree_admissions_score", "application_economics_score"]) for r in programs),
    },
    "warnings": [
        "No route is retained for application because no applicant-specific Fall 2027 full-funding award or salaried position is verified.",
        "Fall 2027 deadlines or fees not yet published are labelled latest-cycle/not-yet-published; current examples are not projected forward.",
        "Oxford official course page was discoverable/indexed but intermittently returned access restrictions; claims are conservative and must be rechecked when the 2027/28 application opens.",
        "UCD official course metadata marks international non-EU suitability 'No'; this conflicts with the presence of a non-EU fee and requires written clarification.",
        "Only one faculty match per program was retained. Three rows lack an independently selected 2024–26 paper and are marked partial rather than silently inferred.",
    ],
    "errors": errors,
}
(OUT / "validation.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


readme = """# Europe deep review (checked 2026-09-09)\n\nThis pass covers the 12 mechanically screened Europe programs plus six requested seed checks: University of Luxembourg, TU Delft, Trinity College Dublin, University College Dublin, University of Oxford, and University of Edinburgh. It is intentionally conservative.\n\n- A faculty match means only topical alignment and a current institutional affiliation. Every faculty row says that recruiting is unknown unless a later, specific vacancy proves otherwise.\n- No program is retained for application because an applicant-specific Fall 2027 full international funding package or salaried position has not yet been verified. "Outreach Before Decision" and "Investigate Further" are research actions, not apply recommendations.\n- Deadlines, fees, and stipends carry their actual cycle label. 2026/27 facts are not projected into 2027/28.\n- Master's-required and position-only European routes fail the Fall 2027 eligibility gate for a May 2027 bachelor's graduate unless the official program explicitly has a direct-entry pathway.\n- English was verified from official program/admissions pages. Test-score and waiver eligibility still require applicant-specific assessment.\n- The UCD catalogue contradiction and intermittent Oxford page access are preserved as unresolved issues.\n\nScores use the shared 30/15/25/15/10/5 dimensions, but recommendations are hard-gate overrides: high topical fit cannot compensate for missing eligibility or funding.\n"""
EVIDENCE.mkdir(parents=True, exist_ok=True)
(EVIDENCE / "README.md").write_text(readme, encoding="utf-8")
(EVIDENCE / "source_notes.json").write_text(json.dumps({
    "checked_date": CHECKED,
    "official_source_policy": "Official university, department, careers, or institutional repository pages only for retained claims.",
    "search_snippets_policy": "Used for discovery/access diagnosis only; CSV claims point to the official destination URL.",
    "blocked_or_partial": [
        {"institution": "University of Oxford", "issue": "official course page intermittently access-restricted; recheck at 2027/28 opening"},
        {"institution": "University College Dublin", "issue": "official course metadata contains internally conflicting non-EU signals"},
        {"scope": "Fall 2027", "issue": "many continental vacancy-based systems have not posted positions this far ahead"},
    ],
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

artifact_paths = [
    OUT / "deep_programs.csv", OUT / "professors.csv", OUT / "sources.csv",
    OUT / "admin_contacts.csv", OUT / "exclusion_or_downgrade.csv",
    OUT / "validation.json", EVIDENCE / "README.md", EVIDENCE / "source_notes.json",
]
(MANIFEST / "manifest.json").write_text(json.dumps({
    "generated_at": CHECKED,
    "scope": "12 Europe screening candidates plus 6 requested institutional seed checks",
    "artifacts": [
        {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
        for path in artifact_paths
    ],
    "generator": "data/manifests/deep_review/europe/build_outputs.py",
}, indent=2) + "\n", encoding="utf-8")

if errors:
    raise SystemExit("validation failed: " + "; ".join(errors))
print(json.dumps(validation["counts"], indent=2))
