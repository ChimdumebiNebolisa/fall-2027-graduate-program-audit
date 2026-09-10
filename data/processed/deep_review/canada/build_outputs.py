from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from graduate_audit.schema import (
    ADMISSION_PLAUSIBILITY,
    EXCLUSION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    PROGRAM_TYPES,
    RECOMMENDATIONS,
    RECRUITING_STATUSES,
    SOURCE_COLUMNS,
)


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "data" / "processed" / "deep_review" / "canada"
EVIDENCE = ROOT / "evidence" / "deep_review" / "canada"
MANIFEST = ROOT / "data" / "manifests" / "deep_review" / "canada"
ACCESSED = "2026-09-09"


def blank(columns: tuple[str, ...], **values: object) -> dict[str, object]:
    row = {column: "" for column in columns}
    row.update(values)
    return row


def pid(institution_id: str, degree: str, name: str) -> str:
    def slug(value: str) -> str:
        return "-".join("".join(c.lower() if c.isalnum() else " " for c in value).split())
    return f"{institution_id}:program:{slug(degree)}:{slug(name)}"


def sid(url: str) -> str:
    parts = urlsplit(url.strip())
    canonical = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), parts.query, ""))
    return "src:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


institutions = {
    "waterloo": ("ca:dli:O19305471522", "University of Waterloo"),
    "ubc": ("ca:dli:O19330231062", "University of British Columbia"),
    "toronto": ("ca:dli:O19332746152", "University of Toronto"),
    "mcgill": ("ca:dli:O19359011033", "McGill University"),
    "concordia": ("ca:dli:O19359011007", "Concordia University"),
    "alberta": ("ca:dli:O19257171832", "University of Alberta"),
    "saskatchewan": ("ca:dli:O19425660421", "University of Saskatchewan"),
    "victoria": ("ca:dli:O19280533442", "University of Victoria"),
    "queens": ("ca:dli:O19376023352", "Queen's University"),
    "calgary": ("ca:dli:O18886830282", "University of Calgary"),
}


def program(key: str, degree: str, name: str, **values: object) -> dict[str, object]:
    institution_id, institution_name = institutions[key]
    defaults = dict(
        program_id=pid(institution_id, degree, name),
        institution_id=institution_id,
        institution_name=institution_name,
        country="Canada",
        program_name=name,
        degree_type=degree,
        department="Computer Science",
        language_of_instruction="English",
        current_program_status="Active on current official page",
        preliminary_fit="yes",
        screening_decision="retained",
        international_student_eligible="yes",
        admission_plausibility="Plausible to reach",
        recommendation="Outreach Before Decision",
        single_professor_dependency="yes; one faculty match verified in this bounded pass",
    )
    defaults.update(values)
    return blank(PROGRAM_COLUMNS, **defaults)


programs = [
    program(
        "waterloo", "Thesis or research master's", "MMath in Computer Science (thesis)",
        official_program_url="https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath",
        thesis_dissertation_requirement="Admission is only to the thesis option; four graduate courses plus thesis",
        research_credit_requirement="Thesis plus four one-term graduate CS courses",
        research_groups_labs="Software Engineering Research Group; Software REBELs",
        direct_from_bachelors_eligible="yes; honours bachelor in CS/engineering or equivalent",
        minimum_gpa="78% standing",
        minimum_gpa_policy="Published program minimum; cross-system conversion for a US GPA is not supplied",
        prerequisite_coursework="Honours bachelor in computer science or engineering, or equivalent",
        gre_policy="Not listed as required on the official program page",
        english_requirement_waiver="Proof if applicable; US-degree waiver not independently verified in this pass",
        fall_2027_deadline="2026-12-01",
        deadline_cycle_status="Current Fall 2027 admissions page; December 1 for September of following year",
        application_fee="150", fee_currency="CAD",
        fee_waiver_rules="No program-specific waiver found; recheck central policy",
        multiple_applications_allowed="Separate program selections are possible",
        separate_fees_required="yes; fee is per program",
        admissions_model="Hybrid department review plus supervisor match before acceptance",
        faculty_contact_expectation="Not required; advised to establish contact",
        funding_model="TA plus Graduate Research Studentship and awards",
        funding_status="Guaranteed package for full-time MMath within program time limits",
        stipend_amount="51990 total first-year international package (Fall 2026 rate)", stipend_currency="CAD",
        funding_duration_years="2", tuition_coverage="Package is designed with tuition component; verify net offer",
        mandatory_fee_coverage="Not stated as fully covered", health_insurance_coverage="Not separately verified",
        summer_funding="Funding schedule spans academic year; exact summer composition not isolated",
        funding_conditions="Full-time, satisfactory academic progress, assigned duties, within program time limits",
        supervisor_dependent_funding="partly; GRS depends on supervisor funding",
        phd_funding="Full-time PhD package published separately",
        masters_funding="Full-time MMath package published; Fall 2026 international year-one total $51,990",
        scholarships_fellowships="International Master's Award of Excellence and other awards may form package",
        admission_plausibility="Plausible to reach", recommendation="Likely Apply",
        biggest_risk="Published 78% threshold has no official US-GPA conversion and admission is selective",
        unresolved_question="Ask graduate admissions how the applicant's US transcript is converted and confirm Fall 2027 net funding",
        verification_status="Official program, funding, and fee pages checked 2026-09-09",
        notes="Primary Waterloo route; research fit is direct in empirical software engineering and DevOps.",
    ),
    program(
        "waterloo", "Direct-entry PhD", "PhD in Computer Science (direct from bachelor's exception)",
        official_program_url="https://uwaterloo.ca/computer-science/future-graduate-students/programs",
        thesis_dissertation_requirement="Doctoral research and dissertation",
        research_credit_requirement="Doctoral program requirements; direct entrants should expect about six years",
        research_groups_labs="Software Engineering Research Group; Software REBELs",
        direct_from_bachelors_eligible="yes, but only exceptional applicants",
        minimum_gpa="Not separately stated on route summary",
        minimum_gpa_policy="Exceptional direct-entry standard; normal PhD entry is after a master's",
        prerequisite_coursework="Strong CS research background",
        gre_policy="Not listed as required",
        english_requirement_waiver="Proof if applicable; US-degree waiver not independently verified",
        fall_2027_deadline="2026-12-01", deadline_cycle_status="Current page; September admission deadline mapped from recurring date",
        application_fee="150", fee_currency="CAD", separate_fees_required="yes; per program",
        admissions_model="Hybrid; supervisor required before acceptance",
        faculty_contact_expectation="Not required to apply; establishing contact advised",
        funding_model="TA plus GRS and awards",
        funding_status="Guaranteed full-time PhD package within time limits",
        stipend_amount="51090 annual international package (Fall 2026 rate)", stipend_currency="CAD",
        funding_duration_years="6 expected for bachelor's entry; guarantee wording is within time limits",
        tuition_coverage="Included in package design; verify offer net", mandatory_fee_coverage="Not separately stated",
        health_insurance_coverage="Not separately verified", summer_funding="Annual package",
        funding_conditions="Full-time, satisfactory progress, duties, and time-limit conditions",
        supervisor_dependent_funding="partly", phd_funding="Published full-time PhD package",
        masters_funding="Not applicable to this route",
        admission_plausibility="Reach", recommendation="Outreach Before Decision",
        biggest_risk="Direct entry is expressly exceptional; applicant's research helps but GPA is not obviously exceptional",
        unresolved_question="Would the department encourage PhD direct entry or the MMath route for this profile?",
        verification_status="Official route and funding pages checked 2026-09-09",
        notes="Materially different alternate; do not substitute it for the more plausible MMath without advice.",
    ),
    program(
        "ubc", "Thesis or research master's", "MSc in Computer Science (research)",
        official_program_url="https://www.cs.ubc.ca/students/grad/admissions",
        thesis_dissertation_requirement="Research MSc with about 16 months of full-time research in a two-year program",
        research_credit_requirement="Research thesis route; exact credits are in the calendar",
        research_groups_labs="Software Practices Lab; Software Engineering research group",
        direct_from_bachelors_eligible="yes; equivalent four-year bachelor's",
        minimum_gpa="Country-specific UBC minimum",
        minimum_gpa_policy="Official eligibility page directs applicants to country-specific credential rules",
        prerequisite_coursework="Substantial CS background; required undergraduate course equivalents",
        gre_policy="Not identified as required on department application page",
        english_requirement_waiver="Country/credential-specific; verify against UBC English policy",
        fall_2027_deadline="2026-12-15", deadline_cycle_status="Explicitly Fall 2027 / January 2028",
        application_fee="168.25", fee_currency="CAD",
        fee_waiver_rules="Automatic only for eligible applicants in UN least-developed-country list and limited central categories",
        multiple_applications_allowed="Possible by program/intake", separate_fees_required="yes; each program and intake",
        admissions_model="Committee/department admission with later matching",
        faculty_contact_expectation="Not necessary; department says faculty may not respond due to volume",
        funding_model="TA, RA, fellowships, and tuition awards",
        funding_status="Guaranteed at department standard minimum for two years",
        stipend_amount="42107 total package; 30467 net after listed tuition/fees in year 1 (2026-27 international)", stipend_currency="CAD",
        funding_duration_years="2", tuition_coverage="Year-one Faculty of Science tuition award plus $3,200 international tuition award; lower net in year two",
        mandatory_fee_coverage="Listed fees $1,558 reduce package net", health_insurance_coverage="Included among listed student fee components; verify plan specifics",
        summer_funding="Annual guarantee", funding_conditions="Within two-year guarantee; TA/RA/fellowship composition varies",
        supervisor_dependent_funding="no for departmental minimum; composition may include RA",
        phd_funding="Guaranteed five years at PhD minimum",
        masters_funding="Guaranteed two years; international net $30,467 year 1 and $24,728 year 2 at 2026-27 rates",
        scholarships_fellowships="Faculty of Science Tuition Award; International Tuition Award",
        admission_plausibility="Plausible to reach", recommendation="Likely Apply",
        biggest_risk="Highly competitive pool and materially lower year-two net after the one-year tuition award",
        unresolved_question="Confirm whether the 2027-28 package preserves the year-two international net level",
        verification_status="Official Fall 2027 admissions, eligibility, funding, and fee pages checked 2026-09-09",
        notes="Primary UBC route.",
    ),
    program(
        "ubc", "Integrated or structured doctorate", "PhD Track via MSc",
        official_program_url="https://www.cs.ubc.ca/students/grad/admissions/eligibility",
        thesis_dissertation_requirement="Begins under MSc funding and transfers to PhD after selection/decision",
        research_credit_requirement="MSc-stage requirements before PhD transfer; doctorate thereafter",
        research_groups_labs="Software Practices Lab; Software Engineering research group",
        direct_from_bachelors_eligible="yes, through selection of exceptional master's applicants",
        minimum_gpa="Country-specific UBC minimum; selection is exceptional",
        minimum_gpa_policy="Applicants apply to MSc; selected exceptional applicants may enter PhD Track",
        prerequisite_coursework="Four-year bachelor equivalent and sufficient CS background",
        gre_policy="Not identified as required", english_requirement_waiver="Country/credential-specific",
        fall_2027_deadline="2026-12-15", deadline_cycle_status="Explicitly Fall 2027 / January 2028",
        application_fee="168.25", fee_currency="CAD", fee_waiver_rules="Central limited waiver rules",
        admissions_model="Committee selection from MSc applicants; later PhD transfer",
        faculty_contact_expectation="Not necessary",
        funding_model="MSc guarantee before transfer; PhD guarantee after transfer",
        funding_status="Guaranteed at applicable MSc/PhD standard minimums",
        stipend_amount="Same as MSc before transfer; same as PhD after transfer", stipend_currency="CAD",
        funding_duration_years="MSc-stage then five-year PhD schedule; confirm counting in offer",
        tuition_coverage="MSc/PhD tuition awards as applicable", mandatory_fee_coverage="Fees reduce published net",
        health_insurance_coverage="Student fees include health/dental component; verify specifics", summer_funding="Annual",
        funding_conditions="Successful selection and transfer to PhD; satisfactory progress",
        supervisor_dependent_funding="no for department minimum",
        phd_funding="After transfer, same as PhD ($46,236 total international package in 2026-27)",
        masters_funding="Before transfer, same as thesis MSc",
        admission_plausibility="Reach", recommendation="Outreach Before Decision",
        biggest_risk="PhD Track is not a separately assured direct-admit route; selection is exceptional",
        unresolved_question="Whether the applicant should signal PhD Track interest and how selection occurs for Fall 2027",
        verification_status="Official Fall 2027 admissions, eligibility, funding, and fee pages checked 2026-09-09",
        notes="Materially different alternate to the normal research MSc; standard PhD entry usually expects a master's.",
    ),
    program(
        "toronto", "Direct-entry PhD", "PhD in Computer Science (PhD U)",
        official_program_url="https://web.cs.toronto.edu/graduate/faq",
        thesis_dissertation_requirement="Research-stream doctorate with dissertation",
        research_credit_requirement="Direct-entry PhD-U; departmental PhD requirements apply",
        research_groups_labs="Software Engineering group; formal methods and assurance research",
        direct_from_bachelors_eligible="yes; this is the instructed route for international applicants with an equivalent honours bachelor in a closely related field",
        minimum_gpa="SGS minimum plus department competitiveness; exact PhD-U threshold not captured on current page",
        minimum_gpa_policy="Department reviews complete record and research readiness",
        prerequisite_coursework="Honours bachelor's equivalent in closely related field",
        gre_policy="Optional; recommended for applicants educated outside Canada in department guidance",
        english_requirement_waiver="Credential-specific SGS policy; verify US-degree exemption",
        fall_2027_deadline="TBD", deadline_cycle_status="Official page says Fall 2027 applications open October 2026; deadline not yet published as of access date",
        application_fee="130", fee_currency="CAD", fee_waiver_rules="Department says no fee waiver",
        multiple_applications_allowed="One research-stream application urged", separate_fees_required="yes for separate programs",
        admissions_model="Committee-based; applicants name faculty/research interests; interviews possible",
        faculty_contact_expectation="Optional; no supervisor required before application",
        funding_model="A&S minimum support plus TA/RA and departmental fellowship",
        funding_status="Guaranteed full-time research-stream funding; enhanced package targets $39,500 take-home",
        stipend_amount="39500 take-home living allowance after tuition and incidentals (2026-27 enhanced package)", stipend_currency="CAD",
        funding_duration_years="5 for PhD-U",
        tuition_coverage="Enhanced package explicitly targets take-home after tuition/incidentals",
        mandatory_fee_coverage="Covered before stated take-home", health_insurance_coverage="Not separately itemized in reviewed source",
        summer_funding="Annual package", funding_conditions="Good standing; disclose/apply for eligible awards; package may be recomposed",
        supervisor_dependent_funding="no for department guarantee",
        phd_funding="2026-27 international A&S minimum $41,122 plus up to $7,948 departmental enhancement",
        masters_funding="International applicants are not considered for the MSc",
        scholarships_fellowships="Departmental Fellowship; entrance awards; OGS-VISA and other external awards",
        admission_plausibility="Reach", recommendation="Likely Apply",
        biggest_risk="Extremely selective direct-entry doctorate and exact Fall 2027 deadline remains unpublished",
        unresolved_question="Recheck deadline immediately after the Fall 2027 application opens in October 2026",
        verification_status="Official Fall 2027 application notice, eligibility FAQ, funding, and fee pages checked 2026-09-09",
        notes="International bachelor's applicants are explicitly directed away from MSc and to PhD-U.",
    ),
    program(
        "mcgill", "Thesis or research master's", "MSc in Computer Science (thesis)",
        official_program_url="https://www.mcgill.ca/gradapplicants/program/computer-science-msc",
        thesis_dissertation_requirement="Research-intensive thesis MSc",
        research_credit_requirement="Thesis route; departmental/calendar requirements apply",
        research_groups_labs="Software Engineering research faculty",
        direct_from_bachelors_eligible="yes; bachelor with at least a minor-equivalent background in CS",
        minimum_gpa="3.2/4.0 stated on program page", minimum_gpa_policy="Published minimum; competitive admission",
        prerequisite_coursework="At least minor-equivalent computer science background",
        gre_policy="Optional for MSc applicants educated outside Canada", english_requirement_waiver="Recognized Canadian or US degree qualifies under the official department instruction",
        fall_2027_deadline="December 15 (year not stated)", deadline_cycle_status="Current recurring Fall international deadline; Fall 2027 year must be reconfirmed",
        application_fee="143.82", fee_currency="CAD", fee_waiver_rules="No GPS fee waivers; one fee covers up to two programs in same term",
        multiple_applications_allowed="yes; up to two in same term", separate_fees_required="no for first two same-term program choices",
        admissions_model="Hybrid departmental review and supervisor matching",
        faculty_contact_expectation="Identify potential thesis supervisors; department notes professors may contact applicants after deadline",
        funding_model="Scholarships, RA and TA; supervisor/department dependent",
        funding_status="All PhD and most MSc described as funded, but no current numeric MSc minimum/guarantee located",
        stipend_amount="unknown", stipend_currency="CAD", funding_duration_years="unknown",
        tuition_coverage="not verified", mandatory_fee_coverage="not verified", health_insurance_coverage="not verified",
        summer_funding="not verified", funding_conditions="Offer-specific; likely supervisor/assistantship dependent",
        supervisor_dependent_funding="yes/unclear",
        phd_funding="Department FAQ says all PhD students funded; current amount not verified",
        masters_funding="Department FAQ says most MSc students funded; no numeric guarantee verified",
        scholarships_fellowships="McCall MacBain and central graduate awards; competitiveness/eligibility varies",
        admission_plausibility="Plausible", recommendation="Outreach Before Decision",
        biggest_risk="No current official numeric minimum or guarantee for MSc funding was found",
        unresolved_question="Will an international thesis MSc offer guarantee a net amount after tuition for the full expected duration?",
        verification_status="Official program/deadline/fee pages checked; funding precision unresolved",
        notes="Retained conditionally because research fit and bachelor eligibility are strong; do not treat as financially cleared.",
    ),
    program(
        "concordia", "Thesis or research master's", "Master of Computer Science (thesis)",
        official_program_url="https://www.concordia.ca/academics/graduate/computer-science-mcompsc.html",
        thesis_dissertation_requirement="45 credits including 29-credit research thesis",
        research_credit_requirement="29 thesis credits", research_groups_labs="Data-driven Analysis of Software (DAS) Lab; Software Engineering Research Centre",
        direct_from_bachelors_eligible="yes", minimum_gpa="High standing; university example 3.0/4.3 equivalent",
        minimum_gpa_policy="Program and international equivalency review may be stricter",
        prerequisite_coursework="Bachelor in CS, mathematics, engineering, science, or cognate area with high standing",
        gre_policy="Not identified as required", english_requirement_waiver="Credential-specific; verify",
        fall_2027_deadline="March 1 (year not stated)", deadline_cycle_status="Current recurring international Fall deadline; Fall 2027 year must be reconfirmed",
        application_fee="100", fee_currency="CAD", fee_waiver_rules="No fee waivers on current instruction page",
        multiple_applications_allowed="yes", separate_fees_required="yes; complete fee per application",
        admissions_model="Supervisor-match gate after departmental review",
        faculty_contact_expectation="Highly recommended after applying; up to three faculty may be named; no offer without match",
        funding_model="Awards, TA and RA packages offered to most thesis students",
        funding_status="Generally available to most thesis students; no guaranteed numeric minimum published",
        stipend_amount="unknown", stipend_currency="CAD", funding_duration_years="unknown",
        tuition_coverage="not verified", mandatory_fee_coverage="not verified", health_insurance_coverage="not verified",
        summer_funding="not verified", funding_conditions="Offer- and supervisor-dependent",
        supervisor_dependent_funding="yes", phd_funding="Generally available thesis funding; no numeric guarantee verified",
        masters_funding="Packages generally available to most thesis students, not stated as universal guarantee",
        scholarships_fellowships="Automatic consideration for entrance awards",
        admission_plausibility="Plausible", recommendation="Outreach Before Decision",
        biggest_risk="Supervisor match is mandatory and funding is not quantified or guaranteed publicly",
        unresolved_question="Can a potential supervisor/department confirm a two-year net funding floor for an international MCompSc?",
        verification_status="Official program, supervisor-process, and fee pages checked; funding precision unresolved",
        notes="Strong topical match; ordinary course-based MApCompSc is not a substitute for this audit.",
    ),
    program(
        "alberta", "Thesis or research master's", "MSc in Computing Science (thesis)",
        official_program_url="https://www.ualberta.ca/en/admissions/media-library/ua_viewbook_graduate-studies_2026-27_web.pdf",
        thesis_dissertation_requirement="Official 2026-27 viewbook identifies thesis MSc; detailed current department page was not reliably accessible",
        research_credit_requirement="Thesis route; exact credits need second-pass confirmation",
        research_groups_labs="Software Engineering and empirical software research",
        direct_from_bachelors_eligible="yes; historical/current official materials describe honours-equivalent bachelor and CS/math preparation",
        minimum_gpa="3.0/4.0 general graduate minimum; department-specific current page not captured",
        minimum_gpa_policy="General minimum; program may be more competitive",
        prerequisite_coursework="Strong computing science and mathematics background",
        gre_policy="not verified", english_requirement_waiver="not verified",
        fall_2027_deadline="TBD", deadline_cycle_status="No public department-specific Fall 2027 date verified in this pass",
        application_fee="135", fee_currency="CAD", fee_waiver_rules="No program-specific waiver verified",
        multiple_applications_allowed="not verified", separate_fees_required="not verified",
        admissions_model="Supervisor-linked thesis admission; exact pre-contact requirement unresolved",
        faculty_contact_expectation="General thesis guidance says connect with a supervisor; department detail unresolved",
        funding_model="RA/TA and awards; department minimum not verified",
        funding_status="unknown; no current Computing Science numeric guarantee verified",
        stipend_amount="unknown", stipend_currency="CAD", funding_duration_years="unknown",
        tuition_coverage="unknown", mandatory_fee_coverage="unknown", health_insurance_coverage="unknown",
        summer_funding="unknown", funding_conditions="unknown", supervisor_dependent_funding="likely; verify",
        phd_funding="not verified", masters_funding="not verified",
        scholarships_fellowships="Competitive University of Alberta Graduate Entrance Scholarship; not a general guarantee",
        admission_plausibility="Plausible", recommendation="Investigate Further",
        biggest_risk="Admissions deadline, funding floor, and net international support remain unresolved due incomplete department-page access",
        unresolved_question="Ask csapplygrad@ualberta.ca for Fall 2027 deadline and guaranteed MSc funding after tuition/fees",
        verification_status="Partial official verification; do not rank as financially cleared",
        notes="Bounded review retained only as an investigation route because faculty fit is strong.",
    ),
    program(
        "saskatchewan", "Thesis or research master's", "MSc in Computer Science (thesis)",
        official_program_url="https://grad.usask.ca/programs/computer-science.php",
        thesis_dissertation_requirement="Thesis-based MSc; project route also exists",
        research_credit_requirement="Thesis program; exact credits on official page/calendar",
        research_groups_labs="Software Research Lab; Software Analytics Research (SOAR)",
        direct_from_bachelors_eligible="yes; four-year honours degree or equivalent in relevant discipline",
        minimum_gpa="70% USask equivalent over last two years", minimum_gpa_policy="Published minimum",
        prerequisite_coursework="Relevant academic discipline; CS background expected",
        gre_policy="Not listed as required", english_requirement_waiver="Department-specific stricter rules; medium-of-instruction letters are not automatically accepted",
        fall_2027_deadline="December 15 (year not stated)", deadline_cycle_status="Current recurring Fall deadline; Fall 2027 year must be reconfirmed",
        application_fee="145", fee_currency="CAD", fee_waiver_rules="No waiver listed",
        multiple_applications_allowed="not verified", separate_fees_required="not verified",
        admissions_model="Departmental; supervisor approval not required to apply",
        faculty_contact_expectation="Optional/appropriate for research fit",
        funding_model="Departmental support plus tuition offset; mostservice duties often required",
        funding_status="Normally funded for full expected 20 months; automatic consideration",
        stipend_amount="Tuition plus 18000 for first 12 months; 8 months tuition plus 12000 for next 8 months", stipend_currency="CAD",
        funding_duration_years="1.67", tuition_coverage="Tuition at admission rate plus international tuition offset bursary",
        mandatory_fee_coverage="Student fees are additional and not stated as covered", health_insurance_coverage="Student fees include health/dental; not stated as covered",
        summer_funding="20-month schedule spans summer", funding_conditions="Funding may require lab-instructor/marker service; some sources require 80% entry and 75% maintenance",
        supervisor_dependent_funding="not solely; departmental system",
        phd_funding="Tuition plus $20,000/year normally for four years",
        masters_funding="Explicit 20-month schedule with international tuition offset",
        scholarships_fellowships="CGRS/NSERC top-ups where eligible",
        admission_plausibility="Plausible", recommendation="Likely Apply",
        biggest_risk="Living component is modest and some funding sources impose an 80% admission GPA condition",
        unresolved_question="Confirm which funding-source GPA condition would apply to this offer and the 2027-28 fee amount",
        verification_status="Official current program/admissions/funding/fee page checked 2026-09-09",
        notes="Strong financial precision relative to most Canadian MSc options.",
    ),
    program(
        "victoria", "Thesis or research master's", "MSc in Computer Science (thesis)",
        official_program_url="https://www.uvic.ca/ecs/computerscience/programs/msc/index.php",
        thesis_dissertation_requirement="Faculty-supervised thesis or project; thesis route selected",
        research_credit_requirement="Thesis route; exact credits in graduate calendar",
        research_groups_labs="CHISEL research group; software and its engineering strength",
        direct_from_bachelors_eligible="yes; four-year bachelor equivalent",
        minimum_gpa="B average over last two years (central minimum)", minimum_gpa_policy="Published minimum; competitive and supervisor capacity-limited",
        prerequisite_coursework="Usually CS, CE, software engineering, or mathematics with CS emphasis",
        gre_policy="Optional but highly recommended for international applicants",
        english_requirement_waiver="Official FAQ accepts qualifying designated-country study or official instruction evidence; verify US credential details",
        fall_2027_deadline="December 15 (year not stated)", deadline_cycle_status="Current September-entry deadline; Fall 2027 year not explicitly labeled",
        application_fee="183", fee_currency="CAD", fee_waiver_rules="No waiver identified; fee applies when any documents originate outside Canada",
        multiple_applications_allowed="not verified", separate_fees_required="not verified",
        admissions_model="Supervisor-led final admission after central eligibility review",
        faculty_contact_expectation="Not required; list potential supervisors; contact is permitted",
        funding_model="TA, ARA, fellowships and external awards",
        funding_status="Automatic consideration and offer normally includes funding; no universal numeric minimum/guarantee found",
        stipend_amount="unknown; UVic fellowships may be up to 20000 but are not guaranteed", stipend_currency="CAD",
        funding_duration_years="unknown", tuition_coverage="not verified", mandatory_fee_coverage="not verified",
        health_insurance_coverage="not verified", summer_funding="not verified",
        funding_conditions="Faculty availability, funding and space determine admission",
        supervisor_dependent_funding="yes", phd_funding="not quantified in reviewed sources",
        masters_funding="Normally included in offer, but no public floor verified",
        scholarships_fellowships="UVic fellowships up to $20,000; automatic consideration, competitive",
        admission_plausibility="Plausible", recommendation="Outreach Before Decision",
        biggest_risk="No numeric, duration-specific guarantee and admission depends on faculty capacity/funding",
        unresolved_question="Can the department or prospective supervisor confirm a two-year net minimum for an international thesis MSc?",
        verification_status="Official program/admissions/funding/fee pages checked; funding precision unresolved",
        notes="Good faculty/research fit but financially conditional.",
    ),
    program(
        "queens", "Thesis or research master's", "MSc in Computing (research pattern)",
        official_program_url="https://www.cs.queensu.ca/graduate/msc/patterns/research.php",
        thesis_dissertation_requirement="Research pattern with thesis; project/coursework patterns excluded from funding recommendation",
        research_credit_requirement="Four courses plus CISC 897 and thesis",
        research_groups_labs="SAIL; MCIS; software engineering research area",
        direct_from_bachelors_eligible="yes; honours bachelor",
        minimum_gpa="International applicants: minimum A standing / first class on 2027-28 admissions page",
        minimum_gpa_policy="Published international minimum; applicant's 3.35 cumulative GPA appears below without an official equivalency exception",
        prerequisite_coursework="Concentration in CS; strong CS background",
        gre_policy="Not required", english_requirement_waiver="Central policy; verify US-degree treatment",
        fall_2027_deadline="2027-01-15", deadline_cycle_status="Explicit 2027-28 academic-session funding deadline",
        application_fee="120", fee_currency="CAD", fee_waiver_rules="No waiver identified",
        multiple_applications_allowed="not verified", separate_fees_required="not verified",
        admissions_model="Committee admissibility plus supervisor selection",
        faculty_contact_expectation="Apply first, then contact a small number of faculty quoting application number",
        funding_model="GRA/TA and supervisor support",
        funding_status="Guaranteed minimum for research MSc, subject to duration and satisfactory progress",
        stipend_amount="29500 year 1 plus 9833 term 4 for international research MSc", stipend_currency="CAD",
        funding_duration_years="1.33 normally; sometimes up to 2",
        tuition_coverage="Funding intended for basic fees/living; separate net not published",
        mandatory_fee_coverage="Not itemized as covered", health_insurance_coverage="not verified", summer_funding="Term-four funding listed",
        funding_conditions="Satisfactory progress; supervisor component; normal 16-month support",
        supervisor_dependent_funding="partly; research fellowship contribution from supervisor",
        phd_funding="International minimum $25,000 year 1, renewable years 2-4 with satisfactory progress",
        masters_funding="International minimum $29,500 year 1 plus $9,833 term 4",
        scholarships_fellowships="External awards can increase package",
        admission_plausibility="Eligibility concern", recommendation="Deprioritize",
        biggest_risk="Published 2027-28 international minimum is A/first-class, apparently above current cumulative GPA",
        unresolved_question="Only reconsider if Queen's confirms the transcript meets its A-standing equivalency despite the cumulative GPA",
        single_professor_dependency="no; broad software-engineering faculty depth, but only one faculty audited here",
        screening_decision="downgraded",
        verification_status="Official 2027-28 admissions, program, funding, and fee pages checked 2026-09-09",
        notes="Financially credible but not presently an eligibility-safe application.",
    ),
    program(
        "calgary", "Direct-entry PhD", "PhD in Computer Science (without completed MSc)",
        official_program_url="https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/doctoral-thesis-based",
        thesis_dissertation_requirement="Coursework, single-authored scientific paper, candidacy exam, and dissertation",
        research_credit_requirement="Doctoral coursework and thesis; five-year expected time without completed MSc",
        research_groups_labs="Software engineering, mining software repositories, build systems and security research",
        direct_from_bachelors_eligible="yes; official route gives expected time without completed MSc",
        minimum_gpa="3.0/4.0 over last two years (central/department minimum)", minimum_gpa_policy="Published minimum; competitive selection and supervisor match",
        prerequisite_coursework="Relevant four-year bachelor and research preparation",
        gre_policy="Submit if applicable; not stated as mandatory on reviewed page", english_requirement_waiver="Credential-specific; verify",
        fall_2027_deadline="2027-01-15 early; 2027-03-01 final", deadline_cycle_status="Current recurring Fall international dates; page does not label Fall 2027 year",
        application_fee="145", fee_currency="CAD", fee_waiver_rules="No waiver listed",
        multiple_applications_allowed="not verified", separate_fees_required="not verified",
        admissions_model="Supervisor-gated hybrid; no admission unless at least one professor agrees to supervise",
        faculty_contact_expectation="List at least one; correspondence optional but encouraged",
        funding_model="GAT, supervisor support, scholarships, plus international differential-fee award",
        funding_status="Guaranteed department minimum for four years; direct-from-bachelor expected time is five years, leaving a duration gap",
        stipend_amount="24000 per year plus differential-fee award", stipend_currency="CAD", funding_duration_years="4",
        tuition_coverage="International differential-fee award helps with visa differential; base tuition coverage not fully itemized",
        mandatory_fee_coverage="not stated", health_insurance_coverage="not stated", summer_funding="Annual wording; verify payment schedule",
        funding_conditions="Supervisor support, TA mix, scholarships and satisfactory progress",
        supervisor_dependent_funding="yes in part; supervisor agreement is also an admissions gate",
        phd_funding="$24,000/year minimum guaranteed four years plus differential-fee award",
        masters_funding="$24,000/year minimum guaranteed two years plus differential-fee award",
        scholarships_fellowships="Departmental Differential Fee Award and competitive scholarships",
        admission_plausibility="Plausible to reach", recommendation="Likely Apply",
        biggest_risk="Four-year guarantee is shorter than the stated five-year expected duration for entrants without an MSc",
        unresolved_question="Will the offer cover year five for a direct-from-bachelor entrant, and what is the net amount after all tuition/fees?",
        verification_status="Official route/admissions/funding/fee pages checked 2026-09-09",
        notes="Primary Calgary route under degree preference; apply only after supervisor/fifth-year funding discussion.",
    ),
    program(
        "calgary", "Thesis or research master's", "MSc in Computer Science (thesis)",
        official_program_url="https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/masters-thesis-based",
        thesis_dissertation_requirement="Five one-semester graduate courses and thesis; public oral defence",
        research_credit_requirement="CPSC 699 plus four half-course equivalents and thesis",
        research_groups_labs="Software engineering, mining software repositories, build systems and security research",
        direct_from_bachelors_eligible="yes", minimum_gpa="3.0/4.0 over last two years",
        minimum_gpa_policy="Published minimum; competitive supervisor selection",
        prerequisite_coursework="Relevant four-year bachelor and computing background",
        gre_policy="Not stated as mandatory", english_requirement_waiver="Credential-specific; verify",
        fall_2027_deadline="2027-01-15 early; 2027-03-01 final", deadline_cycle_status="Current recurring Fall international dates; year not explicitly labeled",
        application_fee="145", fee_currency="CAD", fee_waiver_rules="No waiver listed",
        admissions_model="Supervisor-gated hybrid", faculty_contact_expectation="List at least one; correspondence optional but encouraged",
        funding_model="GAT, supervisor support, scholarships, plus international differential-fee award",
        funding_status="Guaranteed department minimum for two years",
        stipend_amount="24000 per year plus differential-fee award", stipend_currency="CAD", funding_duration_years="2",
        tuition_coverage="Differential-fee award helps with international differential; base tuition not fully itemized",
        mandatory_fee_coverage="not stated", health_insurance_coverage="not stated", summer_funding="Annual wording; verify",
        funding_conditions="Supervisor/TA/scholarship mix and satisfactory progress", supervisor_dependent_funding="yes in part",
        phd_funding="$24,000/year minimum guaranteed four years", masters_funding="$24,000/year minimum guaranteed two years",
        scholarships_fellowships="Departmental Differential Fee Award",
        admission_plausibility="Plausible", recommendation="Likely Apply",
        biggest_risk="$24,000 base minimum may be tight before non-differential tuition and fees",
        unresolved_question="Confirm net annual amount after all tuition, mandatory fees and health insurance",
        verification_status="Official route/admissions/funding/fee pages checked 2026-09-09",
        notes="Materially different, lower-risk alternate if the direct-entry PhD/fifth-year package is not viable.",
    ),
]


program_by_key = {
    "waterloo_msc": programs[0], "waterloo_phd": programs[1], "ubc_msc": programs[2],
    "ubc_track": programs[3], "toronto_phd": programs[4], "mcgill_msc": programs[5],
    "concordia_msc": programs[6], "alberta_msc": programs[7], "sask_msc": programs[8],
    "victoria_msc": programs[9], "queens_msc": programs[10], "calgary_phd": programs[11],
    "calgary_msc": programs[12],
}

# Scores follow the shared 30/15/25/15/10/5 rubric. Research fit is the
# arithmetic sum of professor fit and faculty depth; hard gates still override
# a high arithmetic total (notably Queen's published international minimum).
score_map = {
    "waterloo_msc": (28, 14, 24, 12, 9, 3),
    "waterloo_phd": (28, 14, 24, 8, 8, 3),
    "ubc_msc": (26, 14, 24, 12, 9, 3),
    "ubc_track": (26, 14, 24, 8, 8, 3),
    "toronto_phd": (28, 14, 25, 9, 10, 2),
    "mcgill_msc": (27, 12, 12, 13, 9, 4),
    "concordia_msc": (29, 13, 13, 13, 9, 4),
    "alberta_msc": (25, 11, 5, 12, 8, 3),
    "sask_msc": (27, 13, 23, 13, 9, 4),
    "victoria_msc": (28, 13, 12, 13, 9, 2),
    "queens_msc": (28, 14, 23, 5, 8, 3),
    "calgary_phd": (29, 12, 20, 12, 9, 3),
    "calgary_msc": (29, 12, 21, 13, 9, 3),
}
for key, (professor_fit, faculty_depth, funding, eligibility, degree, economics) in score_map.items():
    row = program_by_key[key]
    research_fit = professor_fit + faculty_depth
    total = research_fit + funding + eligibility + degree + economics
    row.update(
        professor_fit_score=professor_fit,
        faculty_depth_score=faculty_depth,
        research_fit_score=research_fit,
        funding_score=funding,
        eligibility_score=eligibility,
        degree_admissions_score=degree,
        application_economics_score=economics,
        overall_score=total,
    )

program_by_key["mcgill_msc"]["screening_decision"] = "deep_review_pending_numeric_funding"
program_by_key["concordia_msc"]["screening_decision"] = "deep_review_pending_numeric_funding"
program_by_key["alberta_msc"]["screening_decision"] = "downgraded_pending_funding_and_deadline"
program_by_key["victoria_msc"]["screening_decision"] = "deep_review_pending_numeric_funding"


def professor(key: str, program_key: str, name: str, **values: object) -> dict[str, object]:
    institution_id, institution_name = institutions[key]
    target = program_by_key[program_key]
    defaults = dict(
        professor_id=f"{institution_id}:faculty:" + "-".join(name.lower().replace("'", "").split()),
        institution_id=institution_id,
        institution_name=institution_name,
        program_id=target["program_id"],
        program_name=target["program_name"],
        full_name=name,
        department="Computer Science",
        appointment_status="Current department faculty; tenure/permanence not independently verified",
        can_supervise_program="Department research faculty; Fall 2027 capacity unverified",
        fit_strength="Direct",
        recruiting_evidence="No current recruitment statement found unless noted",
        recruiting_status="Recruiting status unknown",
        contacting_faculty_appropriate="yes",
        already_contacted="unknown; Gmail was not accessed in this regional pass",
        outreach_priority="First wave after administrative/funding gates",
        specific_question_goal="Whether they anticipate supervising a Fall 2027 student in the stated research direction",
        verification_status="Current official appointment plus recent work/project source checked 2026-09-09",
    )
    defaults.update(values)
    return blank(PROFESSOR_COLUMNS, **defaults)


professors = [
    professor("waterloo", "waterloo_msc", "Shane McIntosh", faculty_position="Associate Professor",
              official_faculty_url="https://uwaterloo.ca/computer-science/about/people/s4mcinto", official_email="shane.mcintosh@uwaterloo.ca",
              research_themes="empirical software engineering; release engineering; DevOps; software quality",
              fit_explanation="Direct overlap with Terraform/DevOps repair, repository mining, testing and reliable software delivery.",
              recent_work_1="Characterizing Timeout Builds in Continuous Integration", recent_work_1_url="https://rebels.cs.uwaterloo.ca/publications.html", recent_work_1_year="2024",
              recent_work_2="Developer-Applied Accelerations in Continuous Integration", recent_work_2_url="https://rebels.cs.uwaterloo.ca/papers/ase2024_yin.pdf", recent_work_2_year="2024",
              sustained_research_evidence="Official profile and lab bibliography show sustained empirical SE, CI and software-quality work.",
              prospective_student_instructions="Program says contact is not required but is advised; ask a focused supervision question.",
              recommended_outreach_angle="TerraProbe's LLM-assisted Terraform repair and reliable CI/configuration workflows."),
    professor("waterloo", "waterloo_phd", "Shane McIntosh", faculty_position="Associate Professor",
              official_faculty_url="https://uwaterloo.ca/computer-science/about/people/s4mcinto", official_email="shane.mcintosh@uwaterloo.ca",
              research_themes="empirical software engineering; release engineering; DevOps; software quality",
              fit_explanation="Same direct research match; route-specific question is whether direct-entry PhD is realistic.",
              recent_work_1="Characterizing Timeout Builds in Continuous Integration", recent_work_1_url="https://rebels.cs.uwaterloo.ca/publications.html", recent_work_1_year="2024",
              sustained_research_evidence="Sustained lab output in CI, build systems and empirical software engineering.",
              prospective_student_instructions="Contact is advised but not required.", outreach_priority="Second wave / only after route advice",
              recommended_outreach_angle="Ask about direct-entry PhD fit versus MMath for a Fall 2027 bachelor applicant."),
    professor("ubc", "ubc_msc", "Reid Holmes", faculty_position="Professor",
              official_faculty_url="https://www.cs.ubc.ca/people/reid-holmes", official_email="rtholmes@cs.ubc.ca",
              research_themes="software engineering; program analysis; developer tools; computing education",
              fit_explanation="Direct overlap with developer workflows, program analysis, software maintenance and AI-assisted development evaluation.",
              recent_work_1="Supporting Web-based API Searches in the IDE Using Signatures", recent_work_1_url="https://www.cs.ubc.ca/~rtholmes/publications.html", recent_work_1_year="2024",
              recent_work_2="Generative AI in Software Engineering Must Be Human-Centered", recent_work_2_url="https://www.cs.ubc.ca/~rtholmes/papers/jss_2024_russo.pdf", recent_work_2_year="2024",
              sustained_research_evidence="Official profile and current publication list show continued software-engineering work.",
              prospective_student_instructions="UBC says advance contact is not necessary and faculty may not respond.",
              contacting_faculty_appropriate="optional; low information value before application",
              outreach_priority="Second wave", recommended_outreach_angle="Human-centered evaluation of LLM-assisted developer workflows."),
    professor("ubc", "ubc_track", "Reid Holmes", faculty_position="Professor",
              official_faculty_url="https://www.cs.ubc.ca/people/reid-holmes", official_email="rtholmes@cs.ubc.ca",
              research_themes="software engineering; program analysis; developer tools",
              fit_explanation="Strong research match; admissions route selection remains committee-controlled.",
              recent_work_1="Generative AI in Software Engineering Must Be Human-Centered", recent_work_1_url="https://www.cs.ubc.ca/~rtholmes/papers/jss_2024_russo.pdf", recent_work_1_year="2024",
              sustained_research_evidence="Current official appointment and sustained publication record.",
              prospective_student_instructions="UBC says advance contact is unnecessary.", contacting_faculty_appropriate="optional",
              outreach_priority="Do not prioritize before application", recommended_outreach_angle="Only ask a research-direction question, not for a pre-admission commitment."),
    professor("toronto", "toronto_phd", "Marsha Chechik", faculty_position="Professor",
              official_faculty_url="https://web.cs.toronto.edu/people/faculty-directory", official_email="chechik@cs.toronto.edu",
              research_themes="software analysis; assurance; model-driven engineering; formal methods; safety",
              fit_explanation="Direct overlap with reliable AI-assisted software engineering, formal assurance, testing and trustworthy code change.",
              recent_work_1="Automated Codebase Reconciliation using Large Language Models", recent_work_1_url="https://conf.researchr.org/profile/icsr-2025/marshachechik", recent_work_1_year="2025",
              recent_work_2="A Software Engineering Perspective on Testing Large Language Models", recent_work_2_url="https://arxiv.org/abs/2406.08216", recent_work_2_year="2024",
              sustained_research_evidence="Current faculty directory plus 2024-26 work in LLM testing, assurance and software specification.",
              prospective_student_instructions="Name relevant faculty in statement; supervisor commitment is not required.",
              contacting_faculty_appropriate="optional; committee-based process", outreach_priority="Second wave",
              recommended_outreach_angle="Testing and assurance for LLM-generated repairs and evidence-grounded evaluation."),
    professor("mcgill", "mcgill_msc", "Jin L.C. Guo", faculty_position="Associate Professor",
              official_faculty_url="https://www.cs.mcgill.ca/~jguo/", official_email="jin.guo@mcgill.ca",
              research_themes="software engineering; HCI; applied ML; software documentation and stakeholder knowledge",
              fit_explanation="Strong overlap with evidence-grounded developer assistance, software documentation and evaluation of LLM support.",
              recent_work_1="Do LLMs Meet the Needs of Software Tutorial Writers?", recent_work_1_url="https://www.cs.mcgill.ca/~jguo/papers/DIS2024_LLMsForTutorialWriters.pdf", recent_work_1_year="2024",
              recent_work_2="Why People Contribute Software Documentation", recent_work_2_url="https://www.cs.mcgill.ca/~martin/papers.html", recent_work_2_year="2024",
              sustained_research_evidence="Official profile and 2024 publications show a sustained human-centered software-engineering direction.",
              prospective_student_instructions="Identify potential thesis supervisors; capacity not advertised.",
              recommended_outreach_angle="Evidex-style evidence verification for developer-facing LLM explanations and documentation."),
    professor("concordia", "concordia_msc", "Emad Shihab", faculty_position="Professor; Associate Vice-President, Research, Policy, Entrepreneurship and Impact",
              official_faculty_url="https://www.concordia.ca/ginacody/computer-science-software-eng/about/faculty-members.html", official_email="emad.shihab@concordia.ca",
              research_themes="empirical software engineering; mining repositories; software quality; maintenance; AI for software engineering",
              fit_explanation="Exceptionally direct fit to empirical evaluation of AI-generated code, maintenance, quality and repository mining.",
              recent_work_1="Evaluating the Use of LLMs for Documentation to Code Traceability", recent_work_1_url="https://das.encs.concordia.ca/members/emad-shihab", recent_work_1_year="2026",
              recent_work_2="Trustworthy AI systems collaboration with National Bank", recent_work_2_url="https://www.concordia.ca/news/stories/2025/02/20/concordia-partners-with-national-bank-of-canada-to-advance-trustworthy-artificial-intelligence-systems.html", recent_work_2_year="2025",
              sustained_research_evidence="Official faculty/lab pages show sustained software quality and empirical SE work plus a current trustworthy-AI project.",
              prospective_student_instructions="Concordia highly recommends contacting aligned faculty; supervisor match is required.",
              outreach_priority="First wave", recommended_outreach_angle="Reliable LLM-generated code/configuration changes and traceable evidence for repairs."),
    professor("alberta", "alberta_msc", "Abram Hindle", faculty_position="Professor",
              official_faculty_url="https://apps.ualberta.ca/directory/person/hindle1", official_email="hindle1@ualberta.ca",
              research_themes="empirical software engineering; mining repositories; software process; maintenance; energy",
              fit_explanation="Direct methodological fit to repository mining, maintenance and evidence-based study of software development.",
              recent_work_1="Identifying Defect-Inducing Changes in Visual Code", recent_work_1_url="https://arxiv.org/abs/2309.03411", recent_work_1_year="2023",
              recent_work_2="Patterns of Multi-Container Composition for Service Orchestration with Docker Compose", recent_work_2_url="https://arxiv.org/abs/2305.11293", recent_work_2_year="2023",
              sustained_research_evidence="Official directory describes an established empirical-SE and repository-mining program; 2023 work remains within audit recency window.",
              prospective_student_instructions="Current departmental prospective-student instructions were not fully accessible.",
              outreach_priority="First wave only after department confirms funding", recommended_outreach_angle="Empirical repair/evaluation for infrastructure-as-code and container orchestration."),
    professor("saskatchewan", "sask_msc", "Chanchal K. Roy", faculty_position="Professor",
              official_faculty_url="https://www.cs.usask.ca/people/faculty%20profiles/chanchal-roy.php", official_email="chanchal.roy@usask.ca",
              research_themes="software maintenance and evolution; clone detection; empirical software engineering; repository mining",
              fit_explanation="Direct match to program/configuration repair, code-quality analytics and empirical software evolution.",
              recent_work_1="Xmentor: rank-aware aggregation for explainable JIT defect prediction", recent_work_1_url="https://clones.usask.ca/publication/", recent_work_1_year="2026",
              recent_work_2="Take Loads Off Your Developers: Automated User Story Generation Using Large Language Model", recent_work_2_url="https://csgc.usask.ca/research-fest-2024/", recent_work_2_year="2024",
              sustained_research_evidence="Official faculty and lab pages document long-running software maintenance, analytics and repository-mining work.",
              recruiting_evidence="Current lab research page explicitly says it is looking for PhD and MSc students in software analytics topics.",
              recruiting_status="Confirmed recruiting", prospective_student_instructions="Lab page invites potential applicants to contact Prof. Roy.",
              outreach_priority="First wave", recommended_outreach_angle="LLM-assisted repair plus trustworthy software analytics for infrastructure/configuration defects."),
    professor("victoria", "victoria_msc", "Margaret-Anne Storey", faculty_position="Professor; Canada Research Chair Tier I",
              official_faculty_url="https://www.uvic.ca/ecs/computerscience/faculty-staff/faculty/storey-margaret-anne.php", official_email="mstorey@uvic.ca",
              research_themes="human and social aspects of software engineering; developer tools; empirical methods; HCI",
              fit_explanation="Strong fit for human-centered evaluation of AI coding agents, developer workflows and evidence-backed tools.",
              recent_work_1="Identifying Factors Contributing to Bad Days for Software Developers", recent_work_1_url="https://thechiselgroup.org/publications/", recent_work_1_year="2025",
              recent_work_2="Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories", recent_work_2_url="https://thechiselgroup.org/publications/", recent_work_2_year="2025",
              sustained_research_evidence="Official profile and current CHISEL bibliography show sustained human-centered software-engineering work.",
              prospective_student_instructions="No need to contact before applying; supervisor capacity/funding controls final admission.",
              outreach_priority="First wave because funding and capacity determine viability", recommended_outreach_angle="Evaluation of how developers use and trust evidence from LLM-assisted repair agents."),
    professor("queens", "queens_msc", "Ahmed E. Hassan", faculty_position="Professor; Canada Research Chair in Software Analytics",
              official_faculty_url="https://www.cs.queensu.ca/people/Ahmed/Hassan", official_email="",
              research_themes="software analytics; mining repositories; software systems; empirical software engineering",
              fit_explanation="Direct research fit, but the program's published international A-standing minimum is the controlling risk.",
              recent_work_1="Towards Semantic Versioning of Open Pre-trained Language Model Releases on Hugging Face", recent_work_1_url="https://mcis.cs.queensu.ca/publications", recent_work_1_year="2025",
              recent_work_2="A State-of-the-practice Release-readiness Checklist for Generative AI-based Software Products", recent_work_2_url="https://mcis.cs.queensu.ca/publications", recent_work_2_year="2025",
              sustained_research_evidence="Official profile/lab publication ledger shows sustained software analytics and current AI-software work.",
              prospective_student_instructions="School says apply, then contact a small number of faculty with application number.",
              outreach_priority="Do not contact unless eligibility is cleared", recommended_outreach_angle="Only after admin confirmation: release readiness and evidence-grounded evaluation for AI-generated software."),
    professor("calgary", "calgary_phd", "Mahmoud Alfadel", faculty_position="Assistant Professor",
              official_faculty_url="https://profiles.ucalgary.ca/mahmoud-alfadel", official_email="mahmoud.alfadel@ucalgary.ca",
              research_themes="software ecosystems; releases; build systems; security vulnerabilities; mining repositories",
              fit_explanation="Exceptionally direct match to TerraProbe, infrastructure/build configuration, release engineering and software security.",
              recent_work_1="BLAZE: Cross-Language and Cross-Project Bug Localization", recent_work_1_url="https://dblp.org/pid/272/9685.html", recent_work_1_year="2025",
              recent_work_2="The Cost of Downgrading Build Systems: A Case Study of Kubernetes", recent_work_2_url="https://rebels.cs.uwaterloo.ca/member/mahmoud.html", recent_work_2_year="2025",
              sustained_research_evidence="Current official profile and 2024-25 bibliography show sustained build-system, release and software-security work.",
              prospective_student_instructions="Department requires at least one professor to agree to supervise; contact is appropriate.",
              outreach_priority="First wave", recommended_outreach_angle="LLM-assisted Terraform/configuration repair and empirical validation of build/dependency changes."),
    professor("calgary", "calgary_msc", "Mahmoud Alfadel", faculty_position="Assistant Professor",
              official_faculty_url="https://profiles.ucalgary.ca/mahmoud-alfadel", official_email="mahmoud.alfadel@ucalgary.ca",
              research_themes="software ecosystems; releases; build systems; security vulnerabilities; mining repositories",
              fit_explanation="Same direct fit; MSc is the funding-duration-safe alternate route.",
              recent_work_1="BLAZE: Cross-Language and Cross-Project Bug Localization", recent_work_1_url="https://dblp.org/pid/272/9685.html", recent_work_1_year="2025",
              sustained_research_evidence="Current appointment plus sustained recent SE publication record.",
              prospective_student_instructions="Supervisor match is an admissions gate.", outreach_priority="First wave",
              recommended_outreach_angle="Ask which route best fits TerraProbe and whether two-year MSc funding is net-sufficient."),
]


source_specs = [
    ("waterloo", "waterloo_msc", "program/admissions", "MMath is a 24-month research master's; admission is thesis-only; September deadline is December 1; bachelor minimum is 78%.", "Computer Science - Master of Math", "University of Waterloo", "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath", "official program page", "Fall 2027/current"),
    ("waterloo", "waterloo_phd", "degree route", "Exceptional bachelor's applicants may be considered for direct PhD entry and should expect about six years.", "Computer Science graduate programs", "University of Waterloo", "https://uwaterloo.ca/computer-science/future-graduate-students/programs", "official department page", "current"),
    ("waterloo", "waterloo_msc", "funding", "All full-time MMath/PhD students receive packages; Fall 2026 international MMath first-year package is $51,990.", "Funding and awards", "University of Waterloo", "https://uwaterloo.ca/computer-science/current-graduate-students/funding-and-awards", "official funding page", "2026-27"),
    ("waterloo", "waterloo_msc", "application fee", "Graduate application fee is $150 CAD per program.", "How to apply", "University of Waterloo", "https://uwaterloo.ca/future-graduate-students/admissions/how-to-apply", "official admissions page", "current"),
    ("waterloo", "waterloo_msc", "faculty", "Shane McIntosh is current Associate Professor working in empirical SE, software delivery/DevOps and quality.", "Shane McIntosh", "University of Waterloo", "https://uwaterloo.ca/computer-science/about/people/s4mcinto", "official faculty profile", "current"),
    ("waterloo", "waterloo_msc", "recent work", "Lab bibliography lists multiple 2024 CI/build/software-quality papers involving Shane McIntosh.", "Software REBELs publications", "University of Waterloo", "https://rebels.cs.uwaterloo.ca/publications.html", "official lab bibliography", "2024-26"),
    ("ubc", "ubc_msc", "program/deadline", "UBC offers funded research MSc, PhD and PhD Track; deadline is December 15, 2026 for September 2027/January 2028.", "Admissions", "UBC Computer Science", "https://www.cs.ubc.ca/students/grad/admissions", "official department page", "Fall 2027"),
    ("ubc", "ubc_track", "eligibility", "MSc accepts four-year bachelor's; PhD Track selects exceptional MSc applicants without a master's.", "Eligibility", "UBC Computer Science", "https://www.cs.ubc.ca/students/grad/admissions/eligibility", "official admissions page", "current"),
    ("ubc", "ubc_msc", "funding", "2026-27 international MSc package totals $42,107 with $30,467 listed net in year one; minimum guaranteed two years.", "Stipends & Support Details 2026-2027", "UBC Computer Science", "https://www.cs.ubc.ca/grads/awards-support-current-grad-students/financial-assistantship/stipends-support-details-2026-2027", "official funding page", "2026-27"),
    ("ubc", "ubc_msc", "application model", "Advance faculty contact is not necessary; MSc students are admitted to the department.", "Online Application", "UBC Computer Science", "https://www.cs.ubc.ca/students/grad/admissions/application-components-required-documents/online-application", "official admissions page", "Fall 2027"),
    ("ubc", "ubc_msc", "application fee", "International fee is $168.25 for September 2027-August 2028; limited automatic waiver categories apply.", "Online Application and Fee", "UBC Graduate School", "https://www.grad.ubc.ca/prospective-students/application-admission/online-application-fee", "official fee page", "2027-28"),
    ("ubc", "ubc_msc", "faculty/recent work", "Reid Holmes is current Professor in software engineering/program analysis; official publications list 2024 work.", "Reid Holmes", "UBC Computer Science", "https://www.cs.ubc.ca/people/reid-holmes", "official faculty profile", "current"),
    ("toronto", "toronto_phd", "eligibility", "International honours-bachelor applicants in related fields should apply to PhD-U; they are not considered for the MSc.", "Graduate FAQ", "University of Toronto Computer Science", "https://web.cs.toronto.edu/graduate/faq", "official department FAQ", "Fall 2027"),
    ("toronto", "toronto_phd", "deadline/fee", "Fall 2027 applications open October 2026; deadline not yet stated; fee is $130 CAD.", "How to Apply", "University of Toronto Computer Science", "https://web.cs.toronto.edu/graduate/how-to-apply", "official admissions page", "Fall 2027"),
    ("toronto", "toronto_phd", "funding", "Enhanced 2026-27 package targets $39,500 take-home after tuition/incidentals; international PhD minimum is $41,122 plus up to $7,948.", "Funding, Tuition Fees and Awards", "University of Toronto Computer Science", "https://web.cs.toronto.edu/graduate/funding-tuition-awards", "official funding page", "2026-27"),
    ("toronto", "toronto_phd", "faculty", "Marsha Chechik is current Professor in software engineering/formal methods.", "Faculty Directory", "University of Toronto Computer Science", "https://web.cs.toronto.edu/people/faculty-directory", "official faculty directory", "current"),
    ("toronto", "toronto_phd", "recent work", "2025 conference profile lists Automated Codebase Reconciliation using LLMs and related SE work.", "Marsha Chechik - ICSR 2025", "ICSR / conf.researchr.org", "https://conf.researchr.org/profile/icsr-2025/marshachechik", "official conference profile", "2025"),
    ("mcgill", "mcgill_msc", "program", "MSc Computer Science thesis is research intensive and bachelor-entry; program minimum is 3.2/4.0.", "Computer Science MSc", "McGill University", "https://www.mcgill.ca/gradapplicants/program/computer-science-msc", "official program page", "current"),
    ("mcgill", "mcgill_msc", "deadline", "International thesis MSc Fall deadline is December 15; page does not label a year.", "Application Deadlines", "McGill School of Computer Science", "https://www.cs.mcgill.ca/graduate/future/deadline/", "official department page", "current recurring"),
    ("mcgill", "mcgill_msc", "funding", "Department FAQ describes all PhD and most MSc students as funded but does not provide a current MSc minimum in the reviewed text.", "Future Students FAQ", "McGill School of Computer Science", "https://www.cs.mcgill.ca/graduate/future/faq/", "official department FAQ", "current"),
    ("mcgill", "mcgill_msc", "application fee", "Latest posted 2027 fee is $143.82 CAD; one fee permits two same-term applications; no GPS waiver.", "Application support FAQ", "McGill University", "https://www.mcgill.ca/gradapplicants/how-apply/application-support", "official fee page", "Summer 2027 latest posted"),
    ("mcgill", "mcgill_msc", "faculty/recent work", "Jin Guo is current Associate Professor; official McGill pages list 2024 LLM/tutorial and software-documentation papers.", "Jin Guo", "McGill School of Computer Science", "https://www.cs.mcgill.ca/~jguo/", "official faculty page", "current"),
    ("concordia", "concordia_msc", "program/funding", "MCompSc includes a 29-credit thesis; funding packages are generally available to most thesis students; Fall international deadline is March 1.", "Computer Science MCompSc", "Concordia University", "https://www.concordia.ca/academics/graduate/computer-science-mcompsc.html", "official program page", "current recurring"),
    ("concordia", "concordia_msc", "supervisor model", "Applicants may name three faculty; contact is highly recommended and no offer issues without a supervisor match.", "Programs with additional requirements", "Concordia University", "https://www.concordia.ca/gradstudies/future-students/how-to-apply/programs-with-additional-requirements.html", "official admissions page", "current"),
    ("concordia", "concordia_msc", "application fee", "Current graduate application instruction page states $100 CAD per application and no waivers.", "Graduate application instructions", "Concordia University", "https://www.concordia.ca/gradstudies/future-students/how-to-apply/instructions.html", "official fee page", "current"),
    ("concordia", "concordia_msc", "faculty/recent work", "Emad Shihab is current Professor; lab page lists 2026 LLM documentation-code traceability work.", "Faculty members / DAS Lab", "Concordia University", "https://das.encs.concordia.ca/members/emad-shihab", "official lab profile", "current"),
    ("alberta", "alberta_msc", "program/contact", "2026-27 official viewbook identifies thesis MSc Computing Science and csapplygrad@ualberta.ca.", "Graduate Studies Viewbook 2026-2027", "University of Alberta", "https://www.ualberta.ca/en/admissions/media-library/ua_viewbook_graduate-studies_2026-27_web.pdf", "official university PDF", "2026-27"),
    ("alberta", "alberta_msc", "application fee", "Official graduate application fee is $135 CAD.", "Graduate application fee", "University of Alberta", "https://www.ualberta.ca/en/graduate-studies/resources/policies-procedures/graduate-program-manual/section-5-admissions/5-4-application-fee.html", "official policy page", "current"),
    ("alberta", "alberta_msc", "faculty", "Abram Hindle is current Professor in Computing Science focused on empirical software engineering and repository mining.", "Abram Hindle directory profile", "University of Alberta", "https://apps.ualberta.ca/directory/person/hindle1", "official directory profile", "current"),
    ("alberta", "alberta_msc", "recent work", "2023 paper studies defect-inducing changes in visual code.", "Identifying Defect-Inducing Changes in Visual Code", "arXiv", "https://arxiv.org/abs/2309.03411", "preprint record", "2023"),
    ("saskatchewan", "sask_msc", "program/admissions/funding", "MSc is bachelor-entry; Fall deadline Dec 15; fee $145 international; normal 20-month funding includes tuition plus stated living components.", "Computer Science", "University of Saskatchewan", "https://grad.usask.ca/programs/computer-science.php", "official program page", "current recurring / 2026-27 fees"),
    ("saskatchewan", "sask_msc", "faculty", "Chanchal Roy is current Professor in software engineering and maintenance/evolution.", "Chanchal Roy", "University of Saskatchewan", "https://www.cs.usask.ca/people/faculty%20profiles/chanchal-roy.php", "official faculty profile", "current"),
    ("saskatchewan", "sask_msc", "recruiting/recent work", "Current lab page explicitly seeks MSc/PhD students; bibliography lists 2026 software-analytics work.", "Research / Publications", "Chanchal Roy lab", "https://clones.usask.ca/research/", "official university-hosted lab page", "current"),
    ("victoria", "victoria_msc", "program/funding", "MSc has thesis/project routes; no supervisor needed to apply; funding consideration automatic and an offer normally includes funding.", "Computer Science MSc", "University of Victoria", "https://www.uvic.ca/ecs/computerscience/programs/msc/index.php", "official program page", "current"),
    ("victoria", "victoria_msc", "admissions", "September deadline is December 15; GRE optional but highly recommended for international applicants; supervisor capacity/funding drives admission.", "Graduate Admission FAQ", "University of Victoria", "https://www.uvic.ca/ecs/computerscience/programs/graduate-admission-faqs/index.php", "official department FAQ", "current recurring"),
    ("victoria", "victoria_msc", "application fee", "Application fee is $183 when any documents originate outside Canada.", "How to apply", "University of Victoria", "https://www.uvic.ca/graduate/admissions/how-to-apply/", "official admissions page", "current"),
    ("victoria", "victoria_msc", "faculty", "Margaret-Anne Storey is current Professor and Tier I CRC in human/social aspects of software engineering.", "Margaret-Anne Storey", "University of Victoria", "https://www.uvic.ca/ecs/computerscience/faculty-staff/faculty/storey-margaret-anne.php", "official faculty profile", "current"),
    ("victoria", "victoria_msc", "recent work", "CHISEL bibliography lists multiple 2025 human-centered software-engineering papers.", "CHISEL Publications", "CHISEL Group", "https://thechiselgroup.org/publications/", "official lab bibliography", "2025"),
    ("queens", "queens_msc", "admissions", "For 2027-28, research MSc deadline is Jan 15, 2027 and international applicants require minimum A/first-class standing.", "Graduate Applicants", "Queen's School of Computing", "https://www.cs.queensu.ca/apply/graduate.php", "official admissions page", "2027-28"),
    ("queens", "queens_msc", "degree structure", "Research MSc is thesis-based and funded; project/course patterns do not carry the same funding/PhD preparation.", "Research Master's", "Queen's School of Computing", "https://www.cs.queensu.ca/graduate/msc/patterns/research.php", "official program page", "current"),
    ("queens", "queens_msc", "funding", "International research MSc minimum is $29,500 year one plus $9,833 term four, normally 16 months.", "Finances", "Queen's School of Computing", "https://www.cs.queensu.ca/graduate/finances/index.php", "official funding page", "as of Feb 2026"),
    ("queens", "queens_msc", "application fee", "Graduate application fee is $120 CAD.", "How to Apply", "Queen's University", "https://www.queensu.ca/grad-postdoc/grad-studies/apply", "official admissions page", "current"),
    ("queens", "queens_msc", "faculty/recent work", "Ahmed Hassan is current Professor/CRC; lab ledger lists 2025 work on model releases and GenAI product readiness.", "Ahmed E. Hassan / MCIS publications", "Queen's School of Computing", "https://mcis.cs.queensu.ca/publications", "official lab bibliography", "2025"),
    ("calgary", "calgary_phd", "degree route", "PhD has a without-completed-MSc route with expected completion time of five years.", "Doctoral thesis-based", "University of Calgary Computer Science", "https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/doctoral-thesis-based", "official program page", "current"),
    ("calgary", "calgary_msc", "degree structure", "MSc is a two-year thesis program with coursework, seminar and public defence.", "Master's thesis-based", "University of Calgary Computer Science", "https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/masters-thesis-based", "official program page", "current"),
    ("calgary", "calgary_phd", "admissions/funding/fee", "International Fall early/final deadlines are Jan 15/Mar 1; fee $145; minimum $24,000 guaranteed 4 years PhD/2 MSc plus differential-fee award; supervisor agreement required.", "Admission Requirements", "University of Calgary Computer Science", "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements", "official department page", "current recurring"),
    ("calgary", "calgary_phd", "faculty", "Mahmoud Alfadel is current Assistant Professor researching build systems, releases, vulnerabilities and repository mining.", "Mahmoud Alfadel", "University of Calgary", "https://profiles.ucalgary.ca/mahmoud-alfadel", "official faculty profile", "current"),
    ("calgary", "calgary_phd", "recent work", "Bibliographic record lists 2025 bug-localization and build-system work.", "Mahmoud Alfadel bibliography", "DBLP", "https://dblp.org/pid/272/9685.html", "bibliographic index", "2025-26"),
]


sources = []
for index, (key, program_key, claim_type, claim, title, publisher, url, source_type, cycle) in enumerate(source_specs, start=1):
    institution_id, institution_name = institutions[key]
    target = program_by_key[program_key]
    sources.append(blank(
        SOURCE_COLUMNS,
        source_id=sid(url), institution_id=institution_id, institution_name=institution_name,
        program_id=target["program_id"], program_or_professor=target["program_name"],
        claim_type=claim_type, exact_claim_supported=claim, source_title=title, publisher=publisher,
        publication_date="", url=url, source_type=source_type,
        official_or_secondary="secondary" if publisher in {"arXiv", "DBLP"} else "official",
        date_accessed=ACCESSED, admissions_cycle=cycle, confidence="high" if publisher not in {"arXiv", "DBLP"} else "medium",
        verification_status="opened/current" if "2027" in cycle or cycle == "current" else "opened; cycle limits recorded",
        access_note="No search snippet used as final evidence; URL/page content reviewed.",
    ))


def exclusion(key: str, name: str, reason: str, evidence: str, url: str, confidence: str = "high") -> dict[str, object]:
    institution_id, institution_name = institutions[key]
    return blank(
        EXCLUSION_COLUMNS,
        institution_id=institution_id, institution_name=institution_name, country="Canada",
        program_id=pid(institution_id, "Unclear", name), program_name=name,
        stage_of_exclusion="deep route comparison", primary_exclusion_reason=reason,
        supporting_evidence=evidence, source_url=url, confidence=confidence,
        manual_verification="yes; official page reviewed", date_checked=ACCESSED,
    )


exclusions = [
    exclusion("toronto", "MSc in Computer Science", "Do not apply as an international applicant", "Official FAQ says international applicants are not considered for MSc and should apply to PhD-U.", "https://web.cs.toronto.edu/graduate/faq"),
    exclusion("ubc", "Standard PhD in Computer Science", "Not direct bachelor route", "Official eligibility page says standard direct PhD entry normally expects a master's; PhD Track is the bachelor-entry mechanism.", "https://www.cs.ubc.ca/students/grad/admissions/eligibility"),
    exclusion("mcgill", "PhD in Computer Science (PhD1 direct-entry exception)", "Deprioritized: published exceptional threshold conflicts with current GPA", "2026-27 catalogue says direct PhD1 may consider outstanding bachelor applicants with extensive research and minimum 3.7/4.0; use thesis MSc instead.", "https://www.mcgill.ca/students/courses/files/students.courses/graduate_course_catalogue_26-27.pdf"),
    exclusion("concordia", "PhD in Computer Science", "Standard route requires master's; bachelor holders generally enter MSc", "Current program page states master's or equivalent for PhD and bachelor holders are generally considered only for master's, with later fast-track possible.", "https://www.concordia.ca/academics/graduate/computer-science-phd.html"),
    exclusion("alberta", "PhD in Computing Science", "Direct bachelor eligibility and current funding floor not verified", "Official materials confirm the PhD exists, but this bounded pass did not verify a current direct-entry rule or numeric department guarantee; MSc remains investigation route.", "https://www.ualberta.ca/en/admissions/media-library/ua_viewbook_graduate-studies_2026-27_web.pdf", "medium"),
    exclusion("saskatchewan", "PhD in Computer Science", "Requires master's for direct application", "Current official program page lists a master's degree or equivalent as the PhD admission requirement.", "https://grad.usask.ca/programs/computer-science.php"),
    exclusion("victoria", "PhD in Computer Science", "Deprioritized direct-bachelor exception due academic threshold", "UVic central rules normally require master's; bachelor applicants may only be considered with A- equivalent in final two years; MSc is the safer route.", "https://www.uvic.ca/graduate/admissions/admission-requirements/index.php"),
    exclusion("queens", "PhD in Computing", "Requires master's", "2027-28 admissions page lists master's degree and minimum A standing for PhD.", "https://www.cs.queensu.ca/apply/graduate.php"),
    exclusion("queens", "MSc in Computing (research pattern)", "Downgraded for eligibility concern", "2027-28 official page requires international applicants to have minimum A/first-class standing; applicant cumulative GPA is approximately 3.35.", "https://www.cs.queensu.ca/apply/graduate.php"),
    exclusion("calgary", "MSc in Computer Science (thesis)", "Alternate, not excluded", "MSc remains a funded two-year alternate if the direct PhD's fifth-year funding gap or route competitiveness is unacceptable.", "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements"),
]


admin_columns = (
    "institution_id", "institution_name", "program_id", "program_name", "priority", "contact_name",
    "contact_role", "official_email", "question_to_resolve", "why_it_matters", "official_url", "date_accessed",
)
admin_specs = [
    ("waterloo", "waterloo_msc", "medium", "Computer Science Graduate Admissions", "csadmiss@uwaterloo.ca", "Confirm official US-GPA equivalency for 78% and Fall 2027 net international funding.", "Eligibility and offer net determine route choice.", "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath"),
    ("ubc", "ubc_msc", "low", "Graduate Information", "grad-info@cs.ubc.ca", "Confirm 2027-28 year-two international MSc net after the one-year tuition award.", "Year-two net drops materially under 2026-27 schedule.", "https://www.cs.ubc.ca/students/grad/admissions/application-components-required-documents/online-application"),
    ("toronto", "toronto_phd", "high", "Graduate Applications", "gradapplications.cs@utoronto.ca", "What is the Fall 2027 application deadline once the portal opens?", "The official Fall 2027 page has not yet published the date.", "https://web.cs.toronto.edu/msc-phd-info-sessions"),
    ("mcgill", "mcgill_msc", "high", "Graduate Program Coordinator", "graduate-coordinator.cs@mcgill.ca", "Does every international thesis-MSc offer include a guaranteed net amount after tuition, and for how long?", "Public wording says most, not all, MSc students are funded and gives no floor.", "https://www.cs.mcgill.ca/graduate/contact/contactinfo/"),
    ("concordia", "concordia_msc", "high", "Gina Cody Graduate Admissions", "graduate-admission@encs.concordia.ca", "What two-year net funding minimum can an international MCompSc thesis offer guarantee?", "Supervisor match is mandatory and public funding wording is non-numeric.", "https://www.concordia.ca/gradstudies/future-students/how-to-apply/programs-with-additional-requirements.html"),
    ("alberta", "alberta_msc", "high", "Computing Science Graduate Applicants", "csapplygrad@ualberta.ca", "Confirm Fall 2027 deadline, direct bachelor eligibility, supervisor process, and guaranteed MSc funding after tuition/fees.", "Several hard-gate facts remain unresolved.", "https://www.ualberta.ca/en/admissions/media-library/ua_viewbook_graduate-studies_2026-27_web.pdf"),
    ("saskatchewan", "sask_msc", "medium", "Computer Science Graduate Program", "gradprogram@cs.usask.ca", "Which funding-source GPA condition applies and will 2027-28 preserve the international tuition offset?", "The page notes some sources require 80% at admission.", "https://grad.usask.ca/programs/computer-science.php"),
    ("victoria", "victoria_msc", "high", "Computer Science Graduate Secretary", "cscgsec@uvic.ca", "Is there a guaranteed two-year net funding minimum for an international thesis MSc?", "A package is normally included but no floor/duration was found.", "https://www.uvic.ca/graduate/programs/graduate-programs/credential-pages/computer-science-msc/computer-science-msc.php"),
    ("queens", "queens_msc", "high", "School of Graduate Studies and Postdoctoral Affairs", "sgspa.reception@queensu.ca", "Does the applicant's East Texas A&M record meet Queen's published international A/first-class equivalency?", "Eligibility is the controlling gate; no application should be paid before clarification.", "https://www.queensu.ca/grad-postdoc/grad-studies/apply"),
    ("calgary", "calgary_phd", "high", "Science Student Centre", "sci.grad@ucalgary.ca", "For PhD entry without an MSc, is year five funded and what is net support after all tuition/mandatory fees?", "The program expects five years but the public guarantee is four.", "https://science.ucalgary.ca/computer-science/future-students/graduate/admission-requirements"),
]
admin_contacts = []
for key, program_key, priority, role, email, question, why, url in admin_specs:
    institution_id, institution_name = institutions[key]
    target = program_by_key[program_key]
    admin_contacts.append({
        "institution_id": institution_id, "institution_name": institution_name,
        "program_id": target["program_id"], "program_name": target["program_name"],
        "priority": priority, "contact_name": role, "contact_role": "department/program administration",
        "official_email": email, "question_to_resolve": question, "why_it_matters": why,
        "official_url": url, "date_accessed": ACCESSED,
    })


write_csv(OUT / "deep_programs.csv", PROGRAM_COLUMNS, programs)
write_csv(OUT / "professors.csv", PROFESSOR_COLUMNS, professors)
write_csv(OUT / "sources.csv", SOURCE_COLUMNS, sources)
write_csv(OUT / "admin_contacts.csv", admin_columns, admin_contacts)
write_csv(OUT / "exclusion_or_downgrade.csv", EXCLUSION_COLUMNS, exclusions)

manifest = {
    "region": "canada",
    "phase": "finalist_deep_review",
    "access_date": ACCESSED,
    "scope": {"institutions": len(institutions), "program_routes_reviewed": 20, "deep_program_rows": len(programs)},
    "route_selection": {
        "primary_routes": 10,
        "material_alternates": 3,
        "alternates": ["Waterloo direct-entry PhD", "UBC PhD Track", "Calgary MSc thesis"],
    },
    "counts": {
        "deep_programs": len(programs), "professor_program_matches": len(professors),
        "distinct_professors": len({row["professor_id"] for row in professors}),
        "source_rows": len(sources), "admin_contacts": len(admin_contacts),
        "exclusions_or_downgrades": len(exclusions),
    },
    "recommendations": {},
    "known_failures": [
        "University of Alberta current Computing Science program/funding detail pages were not reliably accessible; route remains Investigate Further.",
        "University of Toronto Fall 2027 application page is live but the deadline is not yet published.",
        "Several universities publish recurring deadline day/month without explicitly labeling the Fall 2027 cycle; those rows retain the recurring wording and require recheck.",
        "McGill, Concordia, and UVic do not publish a current universal numeric MSc funding floor in the reviewed official pages.",
    ],
    "non_actions": ["No email sent", "No Gmail accessed", "No Calendar accessed or modified", "No application submitted"],
}
for row in programs:
    manifest["recommendations"][row["recommendation"]] = manifest["recommendations"].get(row["recommendation"], 0) + 1
(MANIFEST / "coverage.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

checks = {
    "program_header_exact": tuple(programs[0]) == PROGRAM_COLUMNS,
    "professor_header_exact": tuple(professors[0]) == PROFESSOR_COLUMNS,
    "source_header_exact": tuple(sources[0]) == SOURCE_COLUMNS,
    "exclusion_header_exact": tuple(exclusions[0]) == EXCLUSION_COLUMNS,
    "program_ids_unique": len({row["program_id"] for row in programs}) == len(programs),
    "ten_institutions_covered": len({row["institution_id"] for row in programs}) == 10,
    "all_program_urls_official_http": all(str(row["official_program_url"]).startswith("https://") for row in programs),
    "all_program_types_valid": all(row["degree_type"] in PROGRAM_TYPES for row in programs),
    "all_recommendations_valid": all(row["recommendation"] in RECOMMENDATIONS for row in programs),
    "all_admission_plausibility_valid": all(row["admission_plausibility"] in ADMISSION_PLAUSIBILITY for row in programs),
    "all_score_components_present": all(all(row[column] != "" for column in (
        "professor_fit_score", "faculty_depth_score", "research_fit_score", "funding_score",
        "eligibility_score", "degree_admissions_score", "application_economics_score", "overall_score",
    )) for row in programs),
    "all_research_fit_sums_correct": all(
        int(row["research_fit_score"]) == int(row["professor_fit_score"]) + int(row["faculty_depth_score"])
        for row in programs
    ),
    "all_overall_sums_correct": all(
        int(row["overall_score"]) == int(row["research_fit_score"]) + int(row["funding_score"])
        + int(row["eligibility_score"]) + int(row["degree_admissions_score"])
        + int(row["application_economics_score"])
        for row in programs
    ),
    "component_scores_within_weights": all(
        0 <= int(row["professor_fit_score"]) <= 30
        and 0 <= int(row["faculty_depth_score"]) <= 15
        and 0 <= int(row["funding_score"]) <= 25
        and 0 <= int(row["eligibility_score"]) <= 15
        and 0 <= int(row["degree_admissions_score"]) <= 10
        and 0 <= int(row["application_economics_score"]) <= 5
        for row in programs
    ),
    "all_funding_resolved_or_flagged": all(row["funding_status"] and row["unresolved_question"] for row in programs),
    "uncertain_funding_not_retained": all(
        row["screening_decision"] != "retained"
        for row in programs
        if any(term in row["funding_status"].lower() for term in ("unknown", "no guaranteed", "generally available", "normally includes"))
    ),
    "all_eligibility_determined": all(row["direct_from_bachelors_eligible"] and row["international_student_eligible"] for row in programs),
    "every_program_has_professor_match": {row["program_id"] for row in programs} <= {row["program_id"] for row in professors},
    "all_professor_appointments_checked": all(row["appointment_status"] and row["official_faculty_url"] for row in professors),
    "all_supervision_capacity_explicit": all(row["can_supervise_program"] for row in professors),
    "all_recruiting_statuses_valid": all(row["recruiting_status"] in RECRUITING_STATUSES for row in professors),
    "confirmed_recruiting_has_evidence": all(row["recruiting_evidence"] for row in professors if row["recruiting_status"] == "Confirmed recruiting"),
    "all_deadline_cycles_labeled": all(row["deadline_cycle_status"] for row in programs),
    "all_exclusions_have_reason_and_source": all(row["primary_exclusion_reason"] and row["source_url"] for row in exclusions),
    "all_admin_questions_have_official_contact": all(row["official_email"] and row["official_url"] for row in admin_contacts),
    "no_strong_apply_with_unknown_funding": not any(row["recommendation"] == "Strong Apply" and "unknown" in row["funding_status"].lower() for row in programs),
    "only_explicit_recruiting_is_confirmed": sum(row["recruiting_status"] == "Confirmed recruiting" for row in professors) == 1,
}
validation = {
    "validated_at": ACCESSED,
    "status": "pass" if all(checks.values()) else "fail",
    "checks": checks,
    "counts": manifest["counts"],
    "failed_checks": [name for name, passed in checks.items() if not passed],
    "limitations": manifest["known_failures"],
}
(OUT / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
