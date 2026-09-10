from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import write_csv, write_json  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    ADMISSION_PLAUSIBILITY,
    EXCLUSION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    RECOMMENDATIONS,
    RECRUITING_STATUSES,
    SOURCE_COLUMNS,
    professor_id,
    program_id,
    source_id,
)


ACCESSED = "2026-09-09"
OUTPUT_DIR = REPO_ROOT / "data" / "processed" / "deep_review" / "us"
MANIFEST_DIR = REPO_ROOT / "data" / "manifests" / "deep_review" / "us"

ADMIN_COLUMNS = (
    "institution_id", "institution_name", "program_id", "program_name",
    "contact_type", "contact_name", "contact_role", "official_email",
    "official_url", "contact_guidance", "question_to_resolve",
    "verification_status", "date_accessed",
)


def p(
    institution_id: str,
    institution_name: str,
    program_name: str,
    department: str,
    url: str,
    *,
    labs: str,
    direct: str,
    international: str,
    gpa: str,
    gpa_policy: str,
    prerequisites: str,
    gre: str,
    english: str,
    deadline: str,
    deadline_status: str,
    fee: str,
    waiver: str,
    multiple: str,
    separate: str,
    admissions: str,
    contact: str,
    funding_model: str,
    funding_status: str,
    duration: str,
    tuition: str,
    mandatory_fees: str,
    health: str,
    summer: str,
    conditions: str,
    supervisor_dependent: str,
    fellowships: str,
    fit: str,
    decision: str,
    exclusion: str,
    plausibility: str,
    recommendation: str,
    risk: str,
    unresolved: str,
    notes: str,
) -> dict[str, str]:
    pid = program_id(institution_id, "PhD", program_name)
    return {
        "program_id": pid,
        "institution_id": institution_id,
        "institution_name": institution_name,
        "country": "United States",
        "program_name": program_name,
        "degree_type": "PhD",
        "department": department,
        "official_program_url": url,
        "thesis_dissertation_requirement": "Yes — original dissertation and defense required",
        "research_credit_requirement": "Sustained doctoral research/dissertation enrollment required; exact credits follow program rules",
        "research_groups_labs": labs,
        "direct_from_bachelors_eligible": direct,
        "international_student_eligible": international,
        "language_of_instruction": "English",
        "current_program_status": f"Active program verified on official site {ACCESSED}",
        "preliminary_fit": fit,
        "screening_decision": decision,
        "exclusion_reason": exclusion,
        "minimum_gpa": gpa,
        "minimum_gpa_policy": gpa_policy,
        "prerequisite_coursework": prerequisites,
        "gre_policy": gre,
        "english_requirement_waiver": english,
        "fall_2027_deadline": deadline,
        "deadline_cycle_status": deadline_status,
        "application_fee": fee,
        "fee_currency": "USD",
        "fee_waiver_rules": waiver,
        "multiple_applications_allowed": multiple,
        "separate_fees_required": separate,
        "admissions_model": admissions,
        "faculty_contact_expectation": contact,
        "funding_model": funding_model,
        "funding_status": funding_status,
        "stipend_amount": "Not stated in reviewed official source",
        "stipend_currency": "USD",
        "funding_duration_years": duration,
        "tuition_coverage": tuition,
        "mandatory_fee_coverage": mandatory_fees,
        "health_insurance_coverage": health,
        "summer_funding": summer,
        "funding_conditions": conditions,
        "supervisor_dependent_funding": supervisor_dependent,
        "phd_funding": funding_status,
        "masters_funding": "Not reviewed; this audit is limited to the PhD route",
        "scholarships_fellowships": fellowships,
        "professor_fit_score": "",
        "faculty_depth_score": "",
        "research_fit_score": "",
        "funding_score": "",
        "eligibility_score": "",
        "degree_admissions_score": "",
        "application_economics_score": "",
        "overall_score": "",
        "admission_plausibility": plausibility,
        "recommendation": recommendation,
        "biggest_risk": risk,
        "unresolved_question": unresolved,
        "single_professor_dependency": "Yes — one strongest current match was verified; broader faculty-depth review remains necessary",
        "verification_status": "Verified against current official program/admissions/funding pages; unresolved items are explicit",
        "notes": notes,
    }


PROGRAMS = [
    p(
        "us:ipeds:211440", "Carnegie Mellon University", "Software Engineering PhD",
        "Software and Societal Systems Department", "https://se-phd.isri.cmu.edu/",
        labs="Software Engineering Institute ecosystem; program-analysis, software assurance, and AI-for-SE groups",
        direct="Yes — SCS accepts applicants holding a bachelor's degree or equivalent",
        international="Yes — international applicants are explicitly covered by SCS graduate admissions",
        gpa="No hard program minimum located", gpa_policy="Holistic SCS review; no minimum published on reviewed program page",
        prerequisites="Strong computer science/software engineering preparation and research potential",
        gre="Not required for SCS PhD applications", english="SCS English-proficiency rules apply; waiver is fact-specific",
        deadline="2026-12-09", deadline_status="Fall 2027 final deadline, explicitly labeled; early deadline 2026-11-18 at 3 p.m. ET",
        fee="0", waiver="Software Engineering PhD program page states the application fee is waived",
        multiple="Yes, subject to SCS application rules", separate="Program-specific application rules apply",
        admissions="Committee-based program admission", contact="Faculty contact is optional; admission is not controlled by a single professor",
        funding_model="Departmental RA/TA support", funding_status="Credible full-support commitment: tuition and living support for admitted SE PhD students in good standing",
        duration="Normal doctoral duration; exact guarantee term not stated on reviewed SE page", tuition="Full tuition covered",
        mandatory_fees="Not itemized on reviewed source", health="Included in SCS doctoral support package; plan details not itemized",
        summer="Living support described, but summer mechanics not itemized", conditions="Continued satisfactory progress and good standing",
        supervisor_dependent="No — program describes support for admitted PhD students", fellowships="University and external fellowships may supplement RA/TA support",
        fit="Exceptional match for automated repair, testing, software reliability, and AI-assisted development",
        decision="retained", exclusion="", plausibility="Reach", recommendation="Likely Apply",
        risk="Extremely selective admission", unresolved="Confirm exact 2027 stipend and health/fee components in an offer",
        notes="Current Fall 2027 SCS deadline was verified; recruiting remains unknown for the named faculty match.",
    ),
    p(
        "us:ipeds:145637", "University of Illinois Urbana-Champaign", "Computer Science PhD",
        "Siebel School of Computing and Data Science", "https://catalog.illinois.edu/graduate/engineering/computer-science-phd/",
        labs="Programming Languages, Formal Methods, and Software Engineering research area",
        direct="Yes — admission from a bachelor's degree is permitted",
        international="Yes — international application and English requirements are published",
        gpa="3.40/4.00", gpa_policy="Published minimum undergraduate GPA for consideration; exceptions are rare",
        prerequisites="Strong computing preparation; program evaluates breadth and research readiness",
        gre="Not required", english="Official English test or qualifying waiver under Graduate College rules",
        deadline="", deadline_status="Latest official CS page lists December 15, but the reviewed source did not label the Fall 2027 cycle",
        fee="90", waiver="International applicants generally cannot receive the Graduate College fee waiver",
        multiple="Graduate College rules apply", separate="Separate application/fee requirements apply where multiple programs are permitted",
        admissions="Committee-based admission", contact="Faculty contact is optional and does not replace the application",
        funding_model="Five-year qualifying assistantship/fellowship model", funding_status="Catalog describes five years of eligible appointments with stipend and tuition waiver",
        duration="5", tuition="Full tuition waiver with qualifying appointment", mandatory_fees="Partial fee waiver; remaining fees may be owed",
        health="Not confirmed in reviewed CS catalog source", summer="Not guaranteed in reviewed source",
        conditions="Good standing and qualifying appointment", supervisor_dependent="Partly — appointment source can change",
        fellowships="Competitive university and external fellowships",
        fit="Excellent faculty fit, but the published GPA threshold conflicts with the applicant's verified 3.35 cumulative GPA",
        decision="excluded", exclusion="Published 3.40 undergraduate GPA minimum exceeds the verified 3.35 cumulative GPA; rare-exception route is too uncertain for a fee-bearing application",
        plausibility="Clearly ineligible", recommendation="Do Not Apply", risk="Hard published GPA screen",
        unresolved="Whether the school would authorize a rare GPA exception based on recent-two-year performance",
        notes="This is a conservative portfolio exclusion, not a claim that an exception is impossible.",
    ),
    p(
        "us:ipeds:139755", "Georgia Institute of Technology-Main Campus", "Computer Science PhD",
        "College of Computing", "https://www.cc.gatech.edu/degree-programs/phd-computer-science",
        labs="Software Engineering, program analysis, reliability, and cybersecurity research",
        direct="Yes — bachelor's degree or equivalent accepted", international="Yes — international requirements are stated in the current application portal",
        gpa="3.0/4.0", gpa_policy="Current program portal minimum", prerequisites="Bachelor's preparation appropriate to computer science research",
        gre="Not required in current portal", english="TOEFL/IELTS requirement and institutional waiver rules apply",
        deadline="2026-12-15", deadline_status="Fall 2027 deadline explicitly labeled in current Georgia Tech program portal",
        fee="105 international / 95 domestic", waiver="Institute waiver rules are limited; no program-wide international waiver verified",
        multiple="Institute graduate application rules apply", separate="Separate fees ordinarily apply",
        admissions="Committee-based admission", contact="Program contact available; faculty outreach optional",
        funding_model="RA/TA and fellowship opportunities", funding_status="Funding opportunities are linked, but no CS-wide multi-year guarantee was located",
        duration="Not guaranteed", tuition="May be covered by qualifying assistantship", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Offer- and appointment-specific",
        supervisor_dependent="Often yes for RA support", fellowships="Institute and external fellowships",
        fit="Strong software testing and program-analysis fit", decision="downgrade",
        exclusion="Funding package is not verified as guaranteed for every admitted CS PhD student",
        plausibility="Reach", recommendation="Outreach Before Decision", risk="Potential admission without a sufficiently explicit support package",
        unresolved="Will a Fall 2027 CS PhD offer guarantee tuition, stipend, insurance, and duration?",
        notes="Deadline is current and exact; funding assessment is intentionally conservative.",
    ),
    p(
        "us:ipeds:228778", "The University of Texas at Austin", "Computer Science PhD",
        "Department of Computer Science", "https://www.cs.utexas.edu/graduate/degrees-and-programs",
        labs="Programming Languages, Verification, Software Engineering, and Systems groups",
        direct="Yes — bachelor's degree or comparable foreign degree accepted", international="Yes — Graduate School publishes international requirements",
        gpa="3.0/4.0", gpa_policy="Minimum on upper-division work; holistic review beyond the minimum",
        prerequisites="Strong CS background; deficiencies may require preparatory work", gre="Not required by current CS admissions page",
        english="International English requirement; waiver depends on official Graduate School criteria",
        deadline="", deadline_status="Current CS page lists December 15 but did not explicitly label Fall 2027 in the reviewed text",
        fee="90 international / 65 domestic", waiver="International application fee waivers are not available under the reviewed Graduate School policy",
        multiple="Graduate School policy applies", separate="Separate program fees apply where multiple submissions are allowed",
        admissions="Committee-based admission", contact="Faculty contact optional; csadmis@cs.utexas.edu handles admissions questions",
        funding_model="Fellowship, GRA, and TA support", funding_status="Most CS PhD students receive support for the first five years; not stated as an unconditional guarantee for every admit",
        duration="5 for most students", tuition="Qualifying appointments cover tuition", mandatory_fees="Qualifying appointments cover specified fees",
        health="Qualifying appointments include insurance", summer="Varies by fellowship or research appointment",
        conditions="Academic progress and appointment availability", supervisor_dependent="Partly, especially for GRA support",
        fellowships="Departmental, university, and external fellowships",
        fit="Exceptional program-analysis, verification, synthesis, and secure-software fit", decision="retained", exclusion="",
        plausibility="Reach", recommendation="Likely Apply", risk="High selectivity and support wording is 'most,' not every admit",
        unresolved="Confirm that any offer contains a five-year minimum-support commitment",
        notes="Retained because the published five-year norm is credible, with offer-letter verification required.",
    ),
    p(
        "us:ipeds:110653", "University of California-Irvine", "Software Engineering PhD",
        "Department of Informatics", "https://informatics.ics.uci.edu/phd-software-engineering/",
        labs="Software Design and Collaboration Laboratory; program analysis, security, and testing groups",
        direct="Yes — UCI permits PhD entry after a bachelor's degree", international="Yes — international graduate applicants are explicitly supported",
        gpa="3.0/4.0", gpa_policy="Minimum graduate admission GPA; program uses holistic review",
        prerequisites="Undergraduate preparation in computing and research readiness", gre="Not required by current ICS research-program FAQ",
        english="TOEFL/IELTS unless an official UCI waiver applies",
        deadline="2026-12-15", deadline_status="Fall 2027 application opens 2026-10-01; current ICS deadline is December 15 (combined official-source chain)",
        fee="155 international / 135 domestic", waiver="International applicants are not eligible for the standard UCI fee waiver",
        multiple="Yes", separate="Yes — each program application requires its own fee",
        admissions="Committee-based with faculty-fit review", contact="Direct faculty contact is encouraged by the program",
        funding_model="TA, GSR, and fellowship support", funding_status="ICS states it strives to award all admitted PhD students full funding; this is not an unconditional guarantee",
        duration="Not guaranteed on reviewed page", tuition="Normally included in full-funding awards", mandatory_fees="Not itemized",
        health="Not itemized", summer="Not guaranteed", conditions="Award and appointment terms; academic progress",
        supervisor_dependent="Partly for GSR support", fellowships="UCI and external fellowships",
        fit="Very strong dedicated software-engineering route with automated analysis, security, and testing match",
        decision="retained", exclusion="", plausibility="Plausible to reach", recommendation="Likely Apply",
        risk="High fee and aspirational rather than guaranteed funding language", unresolved="Will the admission offer guarantee multi-year tuition, stipend, health, and summer support?",
        notes="Fall 2027 cycle opening and standing ICS December 15 deadline are both official; ask the program to confirm if the posted date changes.",
    ),
    p(
        "us:ipeds:233921", "Virginia Polytechnic Institute and State University", "Computer Science PhD",
        "Department of Computer Science", "https://website.cs.vt.edu/academic/graduate/future-grads/doctorate.html",
        labs="Software engineering, automated program analysis, testing, security, and trustworthy AI groups",
        direct="Yes — the program describes a five-year path from the bachelor's degree", international="Yes — international English and application rules are published",
        gpa="3.0/4.0", gpa_policy="Published minimum; holistic competitive review",
        prerequisites="Strong background in computer science or related discipline", gre="Not required",
        english="TOEFL 90 or IELTS 6.5 unless an official waiver applies",
        deadline="2026-12-01", deadline_status="Fall 2027 full-consideration deadline explicitly labeled",
        fee="75", waiver="Graduate School waiver categories apply; no broad international waiver verified",
        multiple="Graduate School rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission", contact="Faculty contact optional before admission",
        funding_model="Five-year departmental multi-year offer", funding_status="Department states 100% of admitted PhD students beginning Fall 2026 receive a five-year offer, excluding summers",
        duration="5", tuition="Included in qualifying assistantship/support offer", mandatory_fees="Check offer; not fully itemized on reviewed page",
        health="Check offer; not fully itemized on reviewed page", summer="Explicitly excluded from the five-year academic-year commitment",
        conditions="Satisfactory progress and offer terms", supervisor_dependent="No for academic-year baseline; summer/research supplements may depend on advisor",
        fellowships="Competitive fellowships and supplemental awards",
        fit="Excellent fit for LLM-assisted software engineering, testing, build/configuration repair, and security",
        decision="retained", exclusion="", plausibility="Plausible to reach", recommendation="Strong Apply",
        risk="Summer funding is outside the published guarantee", unresolved="What summer-support expectation applies after year one?",
        notes="One of the clearest current Fall 2027 deadlines and funding commitments in this audit.",
    ),
    p(
        "us:ipeds:232186", "George Mason University", "Computer Science PhD",
        "Department of Computer Science", "https://cs.gmu.edu/academics/graduate-programs",
        labs="Software engineering, human-centered software engineering, program repair, and security faculty",
        direct="Yes — current graduate requirements permit a relevant bachelor's route", international="Yes — international deadlines and requirements are published",
        gpa="3.0/4.0 expected", gpa_policy="Program and Graduate School review; exact hard-screen behavior not verified",
        prerequisites="Substantial computer science preparation", gre="Current requirement not conclusively verified",
        english="International English requirement; official waiver rules apply",
        deadline="", deadline_status="Latest program table is Fall 2026: funding 2025-12-01, standard 2026-03-15, international-space 2026-06-01; Fall 2027 not posted",
        fee="75", waiver="Limited Graduate School waivers; availability is not guaranteed",
        multiple="Graduate Admissions rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission", contact="Faculty outreach is optional and may clarify funding/lab fit",
        funding_model="TA/RA and fellowship opportunities", funding_status="No current department-wide multi-year guarantee located",
        duration="Not guaranteed", tuition="May accompany assistantship; not guaranteed", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Offer- and appointment-specific",
        supervisor_dependent="Often yes for RA support", fellowships="Competitive awards available",
        fit="Strong human-centered program-repair and software-engineering faculty match", decision="downgrade",
        exclusion="Fall 2027 deadline and a credible full-support commitment were not verified",
        plausibility="Plausible", recommendation="Investigate Further", risk="Funding and cycle uncertainty",
        unresolved="Will Fall 2027 admission include guaranteed tuition, stipend, health, and duration?",
        notes="Do not treat the Fall 2026 dates as Fall 2027 dates.",
    ),
    p(
        "us:ipeds:199193", "North Carolina State University at Raleigh", "Computer Science PhD",
        "Department of Computer Science", "https://csc.ncsu.edu/academics/graduate/phd/",
        labs="Software Engineering, Analytics, and automated testing/program-analysis groups",
        direct="Yes — 72-credit route beyond a bachelor's degree", international="Yes — international applicants are eligible for fall admission",
        gpa="3.0/4.0 typical Graduate School baseline", gpa_policy="B average expected; holistic departmental review",
        prerequisites="Core computer science and mathematics preparation", gre="Current program policy not conclusively verified",
        english="TOEFL/IELTS unless Graduate School waiver applies",
        deadline="", deadline_status="Current CS page lists December 15 for fall PhD admission, but the reviewed page did not label Fall 2027",
        fee="95 international / 85 domestic", waiver="Graduate School waiver criteria apply",
        multiple="Graduate School rules apply", separate="Separate fees apply where multiple applications are permitted",
        admissions="Hybrid committee/advisor model", contact="Faculty contact is appropriate because RA support is advisor-determined",
        funding_model="RA, TA, and fellowship support", funding_status="No department-wide guarantee located; RA funding is explicitly advisor-determined",
        duration="Not guaranteed", tuition="May accompany qualifying appointment", mandatory_fees="Not verified",
        health="Not verified", summer="Advisor/project dependent", conditions="Assistantship availability and satisfactory progress",
        supervisor_dependent="Yes, explicitly for RA funding", fellowships="Department, Graduate School, and external fellowships",
        fit="Strong automated testing, program analysis, and developer/AI interaction fit", decision="downgrade",
        exclusion="Support is materially advisor-dependent and no multi-year funding guarantee was verified",
        plausibility="Plausible to reach", recommendation="Outreach Before Decision", risk="Advisor-dependent funding",
        unresolved="Would the named faculty member have funded Fall 2027 openings and can the department guarantee baseline support?",
        notes="Current faculty fit is strong; funding is the controlling downgrade.",
    ),
    p(
        "us:ipeds:214777", "Pennsylvania State University-Main Campus", "Computer Science and Engineering PhD",
        "Department of Computer Science and Engineering", "https://www.eecs.psu.edu/students/graduate/Graduate-Degree-Programs-CSE.aspx",
        labs="Programming languages, formal methods, software security, and verification",
        direct="Yes — a recognized bachelor's degree can satisfy Graduate School entry requirements", international="Yes — country-specific international requirements are published",
        gpa="No hard CSE minimum verified", gpa_policy="Competitive holistic review",
        prerequisites="Strong background in computer science or computer engineering", gre="Current CSE GRE policy not conclusively verified",
        english="English test/waiver follows Graduate School country and degree rules",
        deadline="", deadline_status="Current EECS page lists December 20 for fall, but the reviewed page did not label Fall 2027",
        fee="85 international / 65 domestic", waiver="Applicants may ask about limited waivers",
        multiple="One active Graduate School application at a time", separate="A new fee applies to a new application unless waived",
        admissions="Committee-based admission", contact="Faculty outreach optional; program office handles admissions",
        funding_model="Competitive TA/RA appointments", funding_status="Appointments can include stipend, tuition, and 80% health premium; renewal and summer support are not guaranteed",
        duration="Appointment-by-appointment", tuition="Covered with qualifying assistantship", mandatory_fees="Not fully covered/verified",
        health="80% premium with qualifying appointment", summer="Not guaranteed; tuition assistance may be possible",
        conditions="Appointment availability and academic performance", supervisor_dependent="Often yes for RA support",
        fellowships="Competitive fellowships and awards",
        fit="Strong formal methods, program analysis, and software-security match", decision="downgrade",
        exclusion="No multi-year funding guarantee; summer and renewal are explicitly uncertain",
        plausibility="Plausible to reach", recommendation="Deprioritize", risk="Annual funding renewal and uncovered health/fees",
        unresolved="Can CSE provide a written multi-year minimum-support commitment for Fall 2027?",
        notes="Funding page was treated literally; appointment benefits are not a universal admission guarantee.",
    ),
    p(
        "us:ipeds:209542", "Oregon State University", "Computer Science PhD",
        "School of Electrical Engineering and Computer Science", "https://engineering.oregonstate.edu/academics/programs/computer-science/graduate",
        labs="Software engineering, program analysis, automated repair, and dependable systems",
        direct="Yes — bachelor's degree route is explicitly available", international="Yes — international applicants are eligible",
        gpa="3.0/4.0 Graduate School baseline", gpa_policy="Program uses holistic competitive review",
        prerequisites="Substantial computer science preparation", gre="Not required",
        english="TOEFL/IELTS/Duolingo unless official waiver applies",
        deadline="2026-12-10", deadline_status="Fall 2027 deadline explicitly labeled",
        fee="85", waiver="Program says it does not grant application-fee waivers; international waiver unavailable",
        multiple="Graduate School rules apply", separate="Separate fees generally apply",
        admissions="Hybrid committee/faculty-fit model", contact="Faculty outreach is appropriate for fit and funding clarification",
        funding_model="Assistantship and fellowship opportunities", funding_status="No CS-wide full-funding guarantee located",
        duration="Not guaranteed", tuition="May accompany qualifying appointment", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Offer- and appointment-specific",
        supervisor_dependent="Often yes for RA support", fellowships="University and external fellowships",
        fit="Excellent automated repair, specifications, analysis, and testing match", decision="downgrade",
        exclusion="Exact Fall 2027 route is active, but full multi-year funding is not verified",
        plausibility="Plausible", recommendation="Outreach Before Decision", risk="Potentially unfunded or partially funded offer",
        unresolved="Is every admitted CS PhD guaranteed tuition, stipend, health, and a minimum duration?",
        notes="Do not transfer the Robotics PhD funding guarantee to this separate CS program.",
    ),
    p(
        "us:ipeds:166629", "University of Massachusetts-Amherst", "Computer Science PhD",
        "Manning College of Information and Computer Sciences", "https://www.cics.umass.edu/academics/phd-computer-science/how-apply-phd-program",
        labs="Software Engineering and Program Analysis; PL; trustworthy AI and security groups",
        direct="Yes — applicants with strong undergraduate CS preparation are eligible", international="Yes — international requirements are stated",
        gpa="No hard program minimum stated", gpa_policy="Holistic review of academic and research record",
        prerequisites="Solid undergraduate computer science preparation", gre="Not required",
        english="English test or qualifying Graduate School waiver",
        deadline="", deadline_status="Current CICS page lists December 15, but the reviewed page did not explicitly label Fall 2027",
        fee="90", waiver="Graduate School/program waiver rules apply; no broad international waiver verified",
        multiple="Graduate School rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission", contact="Faculty contact optional before admission",
        funding_model="TA/RA/fellowship guarantee for students whose admission letter includes it", funding_status="CICS policy guarantees support for the first five years for covered doctoral students, subject to adequate progress and availability of funds",
        duration="5", tuition="Covered under qualifying support", mandatory_fees="Not fully itemized",
        health="Not fully itemized in reviewed policy", summer="Entering offer describes first 12 months; later summer mechanism should be confirmed",
        conditions="Adequate progress, availability of funds, and terms of the admission letter", supervisor_dependent="No for stated baseline guarantee; RA assignment may vary",
        fellowships="Competitive internal and external fellowships",
        fit="Outstanding automated repair, program analysis, testing, and LLM-evaluation fit", decision="retained", exclusion="",
        plausibility="Plausible to reach", recommendation="Strong Apply", risk="Funding guarantee applies through offer-letter terms and includes conditions",
        unresolved="Confirm the Fall 2027 offer's summer and insurance/fee details",
        notes="The five-year policy is credible but not unconditional; the admission letter controls.",
    ),
    p(
        "us:ipeds:163286", "University of Maryland-College Park", "Computer Science PhD",
        "Department of Computer Science", "https://www.cs.umd.edu/grad/apply",
        labs="Programming Languages, Software Engineering, Systems, and Security groups",
        direct="Yes — a master's degree is not required", international="Yes — international requirements are published for the current cycle",
        gpa="3.0/4.0 Graduate School baseline", gpa_policy="Competitive department review; minimum does not ensure admission",
        prerequisites="Strong computer science preparation", gre="Not required for the current cycle",
        english="TOEFL/IELTS/PTE unless official Graduate School waiver applies",
        deadline="2026-12-04", deadline_status="Fall 2027 deadline explicitly labeled in the 2026–27 admissions cycle",
        fee="75", waiver="Graduate School waiver categories are limited",
        multiple="Graduate School rules apply", separate="Separate fee generally required",
        admissions="Committee plus faculty-availability review", contact="Faculty outreach optional and appropriate for research fit",
        funding_model="TA/RA support", funding_status="Department states PhD students are funded subject to satisfactory progress; exact offer guarantee terms should be checked",
        duration="Normal doctoral period; exact guaranteed years not stated on reviewed page", tuition="Covered under qualifying support",
        mandatory_fees="Not fully itemized", health="Not fully itemized", summer="Not clearly guaranteed",
        conditions="Satisfactory progress and appointment terms", supervisor_dependent="Partly; faculty availability influences admission and RA assignment",
        fellowships="Departmental, university, and external fellowships",
        fit="Excellent program-analysis, semantics, verification, and software-security fit", decision="retained", exclusion="",
        plausibility="Reach", recommendation="Likely Apply", risk="Very selective and funding duration/summer details are not explicit",
        unresolved="Does the Fall 2027 offer guarantee summer support and how many years?",
        notes="Current Fall 2027 cycle was explicitly verified.",
    ),
    p(
        "us:ipeds:170976", "University of Michigan-Ann Arbor", "Computer Science and Engineering PhD",
        "Computer Science and Engineering", "https://cse.engin.umich.edu/academics/graduate/admissions/",
        labs="Software Systems Laboratory; programming languages; software engineering; security",
        direct="Yes — bachelor's degree by matriculation; master's degree not required", international="Yes — international applicants are explicitly covered",
        gpa="No hard minimum; successful applicants typically 3.5+", gpa_policy="3.5 is described as typical, not an eligibility cutoff",
        prerequisites="Strong computing, mathematics, and research preparation", gre="Not accepted/required under current CSE policy",
        english="English test unless Rackham waiver applies",
        deadline="2026-12-15", deadline_status="Fall 2027 application cycle and deadline explicitly labeled; 11:59 p.m. ET",
        fee="90 international / 75 domestic", waiver="Rackham fee waivers are primarily limited to qualifying domestic applicants/programs",
        multiple="Rackham rules apply", separate="Separate applications/fees generally apply",
        admissions="Committee-based admission", contact="Faculty contact encouraged for research questions but not required",
        funding_model="Departmental fellowship/RA/TA guarantee", funding_status="CSE guarantees full support for admitted PhD students for five years from bachelor's entry, subject to progress and program conditions",
        duration="5 from bachelor's; 4 from relevant master's", tuition="Full tuition coverage", mandatory_fees="Covered as specified by CSE support",
        health="Health insurance included", summer="Included in year-round support expectation; confirm offer mechanics",
        conditions="Satisfactory academic progress, advisor/research engagement, and CSE rules", supervisor_dependent="No for baseline department guarantee; advisor fit still matters",
        fellowships="Internal and external fellowship opportunities",
        fit="Outstanding automated program repair, software testing, analysis, and AI-for-SE fit", decision="retained", exclusion="",
        plausibility="Reach", recommendation="Strong Apply", risk="Extremely competitive; typical GPA is above applicant cumulative GPA",
        unresolved="How will the committee weigh the >3.5 recent-two-year record against the 3.35 cumulative GPA?",
        notes="The typical-GPA statement is not treated as a hard cutoff.",
    ),
    p(
        "us:ipeds:231624", "William & Mary", "Computer Science PhD",
        "Department of Computer Science", "https://cdsp.wm.edu/admissions/graduate/computer-science/",
        labs="SEMEL; software engineering, evolution, analytics, testing, and AI-for-SE",
        direct="Yes — master's degree is not required for the PhD", international="Yes — international deadlines and visa considerations are stated",
        gpa="No hard program minimum verified", gpa_policy="Holistic admissions review",
        prerequisites="Computer science or closely related preparation", gre="Not required under current page",
        english="A U.S. bachelor's may support a waiver, subject to official Graduate Admissions determination",
        deadline="", deadline_status="Current page lists February 15 funding priority, March 15 international/visa, June 1 other; Fall 2027 not explicitly labeled",
        fee="50", waiver="Program/Graduate School waiver rules apply",
        multiple="Graduate School rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission", contact="No advisor is required before application and named-faculty preferences receive no admissions priority",
        funding_model="Departmental assistantship", funding_status="All admitted full-time PhD and MS/PhD students receive a stipend and full tuition waiver",
        duration="Not stated on reviewed page", tuition="Full tuition waiver", mandatory_fees="Other fees may remain",
        health="Not stated", summer="Not stated", conditions="Full-time enrollment and appointment/program conditions",
        supervisor_dependent="No for published baseline", fellowships="Competitive fellowships may supplement support",
        fit="Outstanding SE evolution, testing, repository mining, and AI-for-SE fit", decision="retained", exclusion="",
        plausibility="Plausible", recommendation="Strong Apply", risk="Funding duration, fees, health, and summer are not itemized",
        unresolved="How many years of support are guaranteed and are summer and health insurance included?",
        notes="Excellent fit/value; explicitly no need to secure an advisor before applying.",
    ),
    p(
        "us:ipeds:110644", "University of California-Davis", "Computer Science PhD",
        "Graduate Group in Computer Science", "https://grad.ucdavis.edu/programs/gcsi",
        labs="Software engineering, program analysis, testing, programming languages, and security",
        direct="Yes — relevant bachelor's degree preparation can qualify", international="Yes — international application requirements are published",
        gpa="3.0/4.0", gpa_policy="Published minimum; holistic graduate-group review",
        prerequisites="Computing and mathematics preparation appropriate to selected research area", gre="Not required under current program policy",
        english="English test unless UC Davis waiver applies",
        deadline="2026-12-15", deadline_status="Fall 2027 general and fellowship deadline explicitly labeled",
        fee="155 international / 135 domestic", waiver="Standard waivers target specified domestic preparation programs; no broad international waiver",
        multiple="Yes", separate="Yes — each application carries a separate fee",
        admissions="Graduate-group committee with faculty-fit component", contact="Prospective faculty contact is appropriate",
        funding_model="TA/RA and fellowship support", funding_status="Official international page says programs may offer first-year support but later funding is not assured",
        duration="Not guaranteed", tuition="May accompany appointment", mandatory_fees="Not guaranteed",
        health="Not guaranteed", summer="Not guaranteed", conditions="Offer, appointment, and advisor funding",
        supervisor_dependent="Yes for substantial RA support", fellowships="Competitive UC Davis and external fellowships",
        fit="Excellent program-analysis, automated bug finding, software defects, and testing match", decision="downgrade",
        exclusion="No credible multi-year funding guarantee; official guidance warns later funding may be uncertain",
        plausibility="Plausible to reach", recommendation="Outreach Before Decision", risk="High fee plus multi-year funding uncertainty",
        unresolved="Can the graduate group guarantee five years of tuition, stipend, health, and summer support in writing?",
        notes="Current Fall 2027 deadline verified; funding is the controlling concern.",
    ),
    p(
        "us:ipeds:243780", "Purdue University-Main Campus", "Computer Science PhD",
        "Department of Computer Science", "https://www.cs.purdue.edu/graduate/admission/steps.html",
        labs="Software Engineering, programming languages, reliability, and AI-for-SE",
        direct="Yes — bachelor's degree route accepted", international="Yes — international Graduate School requirements apply",
        gpa="No hard CS minimum verified", gpa_policy="Holistic competitive review",
        prerequisites="Strong CS and mathematics background", gre="Not required under current CS policy",
        english="TOEFL/IELTS/Duolingo or official waiver",
        deadline="2026-12-01", deadline_status="Fall 2027 deadline explicitly labeled",
        fee="75 international / 60 domestic", waiver="Graduate School waiver categories apply; no universal international waiver",
        multiple="Graduate School rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission", contact="Admissions questions must go to csgradinfo@purdue.edu; faculty contact is optional",
        funding_model="Fellowship, TA, and RA consideration", funding_status="Applicants are automatically considered, but the program explicitly allows admission without funding",
        duration="Not guaranteed", tuition="Covered only with qualifying award/appointment", mandatory_fees="Not verified",
        health="Not verified", summer="Not guaranteed", conditions="Award and appointment availability",
        supervisor_dependent="Often yes for RA support", fellowships="Automatic consideration for fellowships and assistantships",
        fit="Strong dependable software, AI-SE synergy, testing, and program-analysis fit", decision="downgrade",
        exclusion="The program explicitly permits admission without funding",
        plausibility="Plausible to reach", recommendation="Outreach Before Decision", risk="Unfunded admission is possible",
        unresolved="Would a Fall 2027 offer include a multi-year support commitment?",
        notes="Exact Fall 2027 deadline is current; do not equate automatic funding consideration with funding.",
    ),
    p(
        "us:ipeds:167358", "Northeastern University", "Computer Science PhD",
        "Khoury College of Computer Sciences", "https://www.khoury.northeastern.edu/apply/phd-apply/",
        labs="Programming Research Laboratory; software engineering, program analysis, and security groups",
        direct="Yes — four-year undergraduate degree accepted", international="Yes — international English requirements are published",
        gpa="No hard program minimum verified", gpa_policy="Holistic research-focused review",
        prerequisites="Strong computer science preparation", gre="Test optional; CS PhD page says scores are highly encouraged",
        english="English test unless Northeastern waiver criteria apply",
        deadline="", deadline_status="Current Khoury page lists December 15, but the reviewed page did not label Fall 2027",
        fee="Not stated on reviewed official PhD page", waiver="Current official program material advertises fee-waiver codes for qualifying information-session attendees",
        multiple="Graduate admissions rules apply", separate="Not conclusively verified",
        admissions="Committee-based admission", contact="Faculty outreach optional; attend PhD information sessions for program guidance",
        funding_model="College five-year assistantship/fellowship package", funding_status="Khoury states all admitted CS and Cybersecurity PhD students receive a five-year package",
        duration="5", tuition="Full tuition for stated courseload", mandatory_fees="Not fully itemized",
        health="Individual health insurance included", summer="Not fully itemized on reviewed page",
        conditions="Satisfactory progress and package terms", supervisor_dependent="No for published baseline",
        fellowships="Internal and external fellowship opportunities",
        fit="Excellent program analysis, testing, software supply chain, and programming-languages fit", decision="retained", exclusion="",
        plausibility="Plausible to reach", recommendation="Likely Apply", risk="Application fee and Fall 2027 cycle date were not yet explicit",
        unresolved="Confirm Fall 2027 deadline, fee, and summer-support mechanics when the cycle page updates",
        notes="Funding page was on an official Khoury domain path; exact offer letter still controls.",
    ),
    p(
        "us:ipeds:153603", "Iowa State University", "Computer Science PhD",
        "Department of Computer Science", "https://www.cs.iastate.edu/graduate-studies/phd-application-requirements",
        labs="Laboratory for Software Design; configurable systems, testing, SE, and program analysis",
        direct="Yes — direct admission from a bachelor's degree is stated in the FAQ", international="Yes — international applicants are explicitly covered",
        gpa="3.0/4.0 typical Graduate College baseline", gpa_policy="Holistic departmental review",
        prerequisites="Computer science or related background and research preparation", gre="Not required under current program requirements",
        english="English test or official Iowa State waiver",
        deadline="2026-12-15", deadline_status="Fall 2027 application deadline explicitly labeled; supporting documents due 2027-01-10",
        fee="0", waiver="Graduate application is free",
        multiple="Graduate College rules apply", separate="No application fee",
        admissions="Hybrid committee/faculty-fit model", contact="Application asks for three faculty of interest; targeted outreach is appropriate",
        funding_model="Initial TA package followed by TA/RA support", funding_status="Selected admitted PhD students receive two academic years of TA support with full tuition and health; years 3–5 and summers are usually RA but advisor-dependent",
        duration="2 guaranteed academic years for selected funded admits; later support not guaranteed", tuition="100% during stated TA support",
        mandatory_fees="Not fully itemized", health="Included during stated TA support", summer="Usually RA but not guaranteed",
        conditions="Selection for funded offer, progress, teaching performance, and advisor grants", supervisor_dependent="Yes after the initial TA period",
        fellowships="University and external fellowships",
        fit="Outstanding configurable-software, software testing, search-based SE, and reliability fit", decision="retained", exclusion="",
        plausibility="Plausible", recommendation="Strong Apply", risk="Support after two academic years is advisor-dependent",
        unresolved="Can the department describe a fallback if RA support is unavailable in years 3–5 or summer?",
        notes="Exceptional application economics and exact Fall 2027 cycle; later-year funding should be asked directly.",
    ),
    p(
        "us:ipeds:181464", "University of Nebraska-Lincoln", "Computer Science PhD",
        "School of Computing", "https://graduate.unl.edu/academics/programs/COMP-PHD/",
        labs="Software engineering, formal methods, automated repair, testing, and security",
        direct="Likely yes — no master's prerequisite is stated; direct-bachelor wording was not explicit on reviewed program page",
        international="Yes — international English/document requirements are published",
        gpa="No hard program minimum verified", gpa_policy="Holistic Graduate Studies/program review",
        prerequisites="Relevant computing preparation", gre="Not required",
        english="English test or official Graduate Studies waiver",
        deadline="", deadline_status="Current page lists December 1 for fall financial consideration and March 1 otherwise; Fall 2027 not explicitly labeled",
        fee="50", waiver="Program-specific waiver availability not guaranteed",
        multiple="Yes under Graduate Studies rules", separate="Yes — separate $50 fee for each application",
        admissions="Hybrid committee/faculty-fit model", contact="Statement should identify potential advisors; outreach is appropriate",
        funding_model="Assistantship and fellowship consideration", funding_status="A financial-consideration deadline is published, but no department-wide funding guarantee was located",
        duration="Not guaranteed", tuition="May accompany qualifying assistantship", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Offer, appointment, and advisor availability",
        supervisor_dependent="Often yes for RA support", fellowships="Competitive assistantships and fellowships",
        fit="Strong LLM-assisted program repair, formal methods, security, and testing fit", decision="downgrade",
        exclusion="Direct-from-bachelor wording and multi-year full funding remain insufficiently verified",
        plausibility="Plausible", recommendation="Outreach Before Decision", risk="Eligibility wording and funding uncertainty",
        unresolved="Can a bachelor's-only applicant be admitted directly, and what support is guaranteed?",
        notes="Deadline is deliberately left blank because the official page did not identify Fall 2027.",
    ),
    p(
        "us:ipeds:228787", "The University of Texas at Dallas", "Computer Science PhD",
        "Department of Computer Science", "https://catalog.utdallas.edu/2026/graduate/programs/ecs/computer-science",
        labs="Software Engineering and programming-languages/testing/security research",
        direct="Yes — BS entry is permitted with specified preparation", international="Yes — international graduate applicants are eligible",
        gpa="3.5/4.0 in last 60 semester hours for BS-entry route", gpa_policy="Published last-60-hours requirement; cumulative GPA is not the stated measure",
        prerequisites="Calculus, linear algebra, and CS preparation specified in the catalog", gre="Optional for the latest explicitly referenced cycle; Fall 2027 policy not confirmed",
        english="English test/waiver follows UTD Graduate Admissions rules",
        deadline="", deadline_status="2026–27 catalog lists December 15 for fall, but the reviewed text did not explicitly label Fall 2027",
        fee="75", waiver="Graduate Admissions waiver rules apply; no broad waiver verified",
        multiple="Graduate Admissions rules apply", separate="Separate fees generally apply",
        admissions="Committee-based admission with later advisor selection", contact="Program office contact recommended; faculty outreach optional",
        funding_model="TA/RA opportunities", funding_status="FAQ says most TA decisions are associated with fall review, but no funding guarantee was located",
        duration="Not guaranteed", tuition="May accompany qualifying appointment", mandatory_fees="Not verified",
        health="Not verified", summer="Not guaranteed", conditions="Appointment availability and academic progress",
        supervisor_dependent="Often yes for RA support", fellowships="Competitive fellowships and assistantships",
        fit="Strong automated testing, program repair, reliability, and software-analysis fit", decision="downgrade",
        exclusion="The exact last-60-hour GPA calculation and a multi-year support commitment are unresolved",
        plausibility="Eligibility concern", recommendation="Investigate Further", risk="Applicant may or may not meet the last-60-hour 3.5 rule; funding is unguaranteed",
        unresolved="Obtain an official last-60-hour GPA calculation and written funding terms",
        notes="The applicant's >3.5 recent-two-year GPA is promising but is not substituted for UTD's official last-60 calculation.",
    ),
    p(
        "us:ipeds:221999", "Vanderbilt University", "Computer Science PhD",
        "Department of Computer Science, College of Connected Computing", "https://computing.vanderbilt.edu/csphd/",
        labs="Institute for Software Integrated Systems; software engineering, trustworthy computing, and systems security",
        direct="Yes — undergraduate transcripts and bachelor's/equivalent pathway are supported", international="Yes — international English and waiver processes are published",
        gpa="No hard program minimum stated", gpa_policy="Holistic committee review",
        prerequisites="Strong computer science/engineering preparation and research potential", gre="Not required for Spring/Fall 2027",
        english="English waiver reviewed after submission; official decision appears in applicant portal",
        deadline="2026-12-15", deadline_status="Fall 2027 recommended deadline explicitly labeled; final deadline 2027-01-08; fee-waiver priority 2026-12-01",
        fee="95", waiver="Automatic Fall 2027 waiver eligibility for applicants enrolled in or graduated from a U.S. school if complete by 2026-12-01",
        multiple="Graduate School rules apply", separate="Separate fees generally apply unless waived",
        admissions="Committee-based admission", contact="Faculty outreach optional; named graduate recruitment and program contacts provided",
        funding_model="TA/RA plus fellowship supplements", funding_status="CS PhD students receive stipend, full tuition waiver, and health insurance; continuation depends on academic/research progress",
        duration="Normal PhD duration; supplement fellowships may last 3–5 years", tuition="Full tuition waiver", mandatory_fees="School page says student activity fees are covered",
        health="Paid health insurance", summer="Twelve-month detail not explicit on reviewed CS page",
        conditions="Satisfactory academic and research progress", supervisor_dependent="No for stated baseline; RA source can depend on advisor",
        fellowships="Provost, University Graduate, Dean's, and external fellowships",
        fit="Exceptional dependable-software, software security, human factors, and trustworthy-systems fit",
        decision="retained", exclusion="", plausibility="Plausible to reach", recommendation="Strong Apply",
        risk="Competitive admission and exact summer/duration terms should be read in offer",
        unresolved="Confirm duration and summer-support language in the Fall 2027 offer",
        notes="Applicant's current enrollment at a U.S. institution appears to match the stated fee-waiver criterion if completed by the priority date; portal makes the final determination.",
    ),
    p(
        "us:ipeds:152080", "University of Notre Dame", "Computer Science and Engineering PhD",
        "Department of Computer Science and Engineering", "https://engineering.nd.edu/departments-programs/graduate-programs/phd-in-computer-science-and-engineering/",
        labs="Security and Software Engineering Research Lab; software engineering, program analysis, assurance, and systems",
        direct="Yes — open to applicants with either BS or MS; MS explicitly not required", international="Yes — international Graduate School requirements apply",
        gpa="No hard program minimum stated", gpa_policy="Holistic program review",
        prerequisites="Bachelor's degree in computer science or related field", gre="Not required",
        english="English test/waiver follows Notre Dame Graduate School rules",
        deadline="", deadline_status="Current program page states December 15 for the following fall; Fall 2027 is not explicitly labeled",
        fee="75", waiver="Need, hardship, fellowship, military, automatic, and departmental waiver paths are published",
        multiple="Graduate School rules apply", separate="The $75 fee applies to each application unless waived",
        admissions="Committee-based admission", contact="Program provides DGS/program email; targeted faculty outreach is appropriate",
        funding_model="RA/TA/fellowship support", funding_status="Program states PhD students are generally supported with 12-month stipends, full tuition scholarships, and 100% health premium",
        duration="Typical program 3–5 years; exact guarantee term not stated", tuition="Full tuition scholarship", mandatory_fees="Not itemized",
        health="100% premium paid", summer="12-month stipend indicates summer inclusion", conditions="Appointment/program terms and satisfactory progress",
        supervisor_dependent="Partly for RA support", fellowships="Fellowships may increase the regular stipend",
        fit="Exceptional LLM security testing, program analysis, verification, and secure-software fit",
        decision="retained", exclusion="", plausibility="Plausible", recommendation="Strong Apply",
        risk="Funding language says 'generally supported' rather than an unconditional admission guarantee",
        unresolved="Confirm guaranteed duration in the admission offer and whether the December 15 date is unchanged for Fall 2027",
        notes="The direct-from-BS rule is explicit and the application fee has multiple waiver paths.",
    ),
    p(
        "us:ipeds:179867", "Washington University in St Louis", "Computer Science PhD",
        "Department of Computer Science and Engineering", "https://admin.aprc.wustl.edu/academics/graduate-admissions/index.html",
        labs="Security, privacy, AI-agent systems, embedded/software systems, and programming languages",
        direct="Yes — McKelvey doctoral admission accepts bachelor's-prepared applicants", international="Yes — international graduate admission is supported",
        gpa="No hard CSE minimum verified", gpa_policy="Holistic departmental review",
        prerequisites="Strong computing preparation and research fit", gre="Current CSE requirement not conclusively verified",
        english="English test or official WashU waiver",
        deadline="", deadline_status="Current McKelvey page lists December 1 for fall PhD applications, but the reviewed page did not explicitly label Fall 2027",
        fee="Not stated on reviewed official admissions page", waiver="Official Fall 2027 CSE information-session registration says attendees indicating graduate interest receive an automatic waiver",
        multiple="Graduate admissions rules apply", separate="Not conclusively verified",
        admissions="Committee-based departmental admission", contact="Faculty outreach is appropriate; CSE graduate office is the administrative channel",
        funding_model="School doctoral support", funding_status="McKelvey states its PhD students are fully funded with full tuition and health insurance",
        duration="Not stated on reviewed page", tuition="Full tuition support", mandatory_fees="Not itemized",
        health="Included", summer="Not itemized", conditions="Satisfactory progress and program/appointment terms",
        supervisor_dependent="No for published school baseline; research assignment still matters", fellowships="Competitive university and external fellowships",
        fit="Exceptional current AI-agent reliability, privacy/security, LLM-platform evaluation, and trustworthy-systems fit",
        decision="retained", exclusion="", plausibility="Plausible to reach", recommendation="Strong Apply",
        risk="Exact fee, support duration, and cycle-labeled Fall 2027 deadline were not all present on one official page",
        unresolved="Confirm deadline/fee and multi-year/summer terms with CSE Graduate Admissions",
        notes="The September 2026 Fall 2027 CSE information session is current and offers a fee-waiver path.",
    ),
    p(
        "us:ipeds:201645", "Case Western Reserve University", "Computer Science PhD",
        "Department of Computer and Data Sciences", "https://case.edu/programs/computer-science-phd",
        labs="Software engineering, program analysis/testing, responsible AI engineering, safety and fairness",
        direct="Yes — bachelor's required and master's only preferred; direct-undergraduate route takes about five years", international="Yes — international English options are listed",
        gpa="No hard program minimum stated", gpa_policy="Holistic review; computing degree preferred but not required",
        prerequisites="Bachelor's in computing preferred; relevant preparation evaluated", gre="Required on the current program page",
        english="TOEFL/IELTS or posted degree from an English-speaking school",
        deadline="2027-01-05", deadline_status="Fall 2027 priority deadline explicitly labeled; final deadline 2027-08-01",
        fee="50", waiver="Severe-hardship waivers may be requested from the program but are not guaranteed",
        multiple="Graduate Studies rules apply", separate="Separate fee generally applies",
        admissions="Committee-based admission", contact="Department and Graduate Studies contacts provided; faculty outreach appropriate",
        funding_model="Selective RA/TA/fellowship support", funding_status="Official program says selected incoming students are supported; no universal guarantee located",
        duration="Not guaranteed", tuition="May accompany selected assistantship/fellowship", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Selection and appointment terms",
        supervisor_dependent="Often yes for RA support", fellowships="Competitive State of Ohio and alumni fellowships",
        fit="Excellent responsible-AI engineering, fairness/safety, software testing, program analysis, and reliability fit",
        decision="downgrade", exclusion="Funding is explicitly selective rather than guaranteed for all admitted PhD students",
        plausibility="Plausible", recommendation="Outreach Before Decision", risk="Could be admitted without full support",
        unresolved="Would the program issue a full multi-year funding offer, and is GRE still required for Fall 2027?",
        notes="Current Fall 2027 deadline and $50 fee are explicit; funding remains the hard-gate concern.",
    ),
    p(
        "us:ipeds:195003", "Rochester Institute of Technology", "Computing and Information Sciences PhD",
        "Golisano College of Computing and Information Sciences", "https://www.rit.edu/study/computing-and-information-sciences-phd",
        labs="Better Software @ RIT; cybersecurity; software engineering; trustworthy AI and agent security",
        direct="Yes — bachelor's or U.S. equivalent accepted; RIT explicitly says a master's is not required", international="Yes — program is STEM-OPT eligible and publishes full-time visa requirements",
        gpa="3.0/4.0 typical", gpa_policy="Typical rather than automatic cutoff; holistic committee review",
        prerequisites="Relevant undergraduate preparation and research statement", gre="Not required unless current program page specifies otherwise",
        english="English test or official RIT waiver",
        deadline="", deadline_status="2026–27 curriculum lists December 31 priority and rolling thereafter; page does not explicitly label Fall 2027",
        fee="65", waiver="Current RIT students/alumni and specified groups receive waivers; others may ask Graduate Admissions",
        multiple="Graduate Admissions rules apply", separate="Separate fees generally apply",
        admissions="Interdisciplinary PhD admissions committee", contact="Direct outreach is appropriate for the officially advertised research openings",
        funding_model="Graduate assistantship", funding_status="Program states PhD students typically receive full tuition plus RA stipend or TA salary; not worded as universal guarantee",
        duration="Not guaranteed", tuition="Typically full tuition", mandatory_fees="Not verified",
        health="Not verified", summer="Not verified", conditions="Assistantship and satisfactory progress",
        supervisor_dependent="Often yes for RA support", fellowships="Graduate assistantships and competitive awards",
        fit="Exceptional current openings in AI/agent security, program analysis/testing, software engineering, and verifiable LLM research",
        decision="retained", exclusion="", plausibility="Plausible", recommendation="Strong Apply",
        risk="Baseline funding uses 'typically' and cycle deadline is not explicitly labeled Fall 2027",
        unresolved="Confirm guaranteed package duration, health, summer, and whether the advertised openings are for Fall 2027",
        notes="Official research-opportunities page explicitly lists current PhD openings; this is the only confirmed-recruiting evidence in the dataset.",
    ),
]


# professor alignment / department depth / funding / eligibility / degree model /
# application economics.  The maxima are the committed 30/15/25/15/10/5 rubric.
# These scores are evidence summaries, not admission-probability estimates.
SCORES = {
    "Carnegie Mellon University": (30, 13, 25, 14, 10, 5),
    "University of Illinois Urbana-Champaign": (29, 13, 24, 5, 10, 2),
    "Georgia Institute of Technology-Main Campus": (28, 12, 12, 14, 10, 1),
    "The University of Texas at Austin": (30, 13, 21, 14, 10, 1),
    "University of California-Irvine": (29, 12, 19, 14, 10, 0),
    "Virginia Polytechnic Institute and State University": (29, 12, 23, 14, 10, 3),
    "George Mason University": (26, 9, 8, 14, 10, 2),
    "North Carolina State University at Raleigh": (28, 11, 10, 14, 10, 1),
    "Pennsylvania State University-Main Campus": (27, 10, 11, 14, 10, 2),
    "Oregon State University": (29, 10, 9, 14, 10, 1),
    "University of Massachusetts-Amherst": (30, 12, 23, 14, 10, 2),
    "University of Maryland-College Park": (29, 12, 22, 14, 10, 2),
    "University of Michigan-Ann Arbor": (30, 13, 25, 12, 10, 1),
    "William & Mary": (30, 11, 22, 14, 10, 3),
    "University of California-Davis": (29, 11, 9, 14, 10, 0),
    "Purdue University-Main Campus": (27, 12, 8, 14, 10, 2),
    "Northeastern University": (28, 12, 24, 14, 10, 3),
    "Iowa State University": (30, 11, 20, 14, 10, 5),
    "University of Nebraska-Lincoln": (29, 9, 8, 10, 10, 2),
    "The University of Texas at Dallas": (27, 10, 8, 9, 10, 2),
    "Vanderbilt University": (29, 12, 24, 14, 10, 5),
    "University of Notre Dame": (30, 11, 22, 14, 10, 3),
    "Washington University in St Louis": (30, 12, 24, 14, 10, 5),
    "Case Western Reserve University": (29, 11, 8, 14, 10, 3),
    "Rochester Institute of Technology": (30, 13, 18, 14, 10, 2),
}

for _program in PROGRAMS:
    _professor, _depth, _funding, _eligibility, _degree, _economics = SCORES[_program["institution_name"]]
    _program["professor_fit_score"] = str(_professor)
    _program["faculty_depth_score"] = str(_depth)
    _program["research_fit_score"] = str(_professor + _depth)
    _program["funding_score"] = str(_funding)
    _program["eligibility_score"] = str(_eligibility)
    _program["degree_admissions_score"] = str(_degree)
    _program["application_economics_score"] = str(_economics)
    _program["overall_score"] = str(_professor + _depth + _funding + _eligibility + _degree + _economics)

# UIUC's official catalog says exceptions to 3.40 are rare, not impossible.
next(row for row in PROGRAMS if row["institution_name"] == "University of Illinois Urbana-Champaign")["admission_plausibility"] = "Eligibility concern"


def prof(
    institution_id: str,
    institution_name: str,
    program_name: str,
    full_name: str,
    department: str,
    position: str,
    url: str,
    email: str,
    themes: str,
    explanation: str,
    work: str,
    work_url: str,
    work_year: str,
    *,
    recruiting_status: str = "Recruiting status unknown",
    recruiting_evidence: str = "No current direct Fall 2027 recruiting statement located",
    instructions: str = "Use a concise, evidence-specific inquiry only if the program permits faculty outreach",
    contact_ok: str = "Yes — for research-fit questions, not as a substitute for the formal application",
    priority: str = "High",
    angle: str,
    question: str,
    notes: str = "Publication or project activity is research-fit evidence only and is not treated as recruiting evidence.",
) -> dict[str, str]:
    pid = program_id(institution_id, "PhD", program_name)
    return {
        "professor_id": professor_id(institution_id, full_name),
        "institution_id": institution_id,
        "institution_name": institution_name,
        "program_id": pid,
        "program_name": program_name,
        "full_name": full_name,
        "department": department,
        "faculty_position": position,
        "appointment_status": f"Current tenure-line faculty appointment verified on official page {ACCESSED}",
        "can_supervise_program": "Yes",
        "official_faculty_url": url,
        "official_email": email,
        "research_themes": themes,
        "fit_explanation": explanation,
        "fit_strength": "Strong",
        "recent_work_1": work,
        "recent_work_1_url": work_url,
        "recent_work_1_year": work_year,
        "recent_work_2": "",
        "recent_work_2_url": "",
        "recent_work_2_year": "",
        "recent_work_3": "",
        "recent_work_3_url": "",
        "recent_work_3_year": "",
        "sustained_research_evidence": f"Current faculty profile plus {work_year} paper/project evidence",
        "recruiting_evidence": recruiting_evidence,
        "recruiting_status": recruiting_status,
        "prospective_student_instructions": instructions,
        "contacting_faculty_appropriate": contact_ok,
        "already_contacted": "No evidence in this workspace",
        "last_contact_date": "",
        "previous_outcome": "",
        "outreach_priority": priority,
        "outreach_score": "",
        "recommended_outreach_angle": angle,
        "specific_question_goal": question,
        "openalex_author_id": "",
        "orcid": "",
        "verification_status": "Current appointment and recent work verified; recruiting status treated separately",
        "notes": notes,
    }


PROFESSORS = [
    prof("us:ipeds:211440", "Carnegie Mellon University", "Software Engineering PhD", "Claire Le Goues", "Software and Societal Systems Department", "Professor", "https://s3d.cmu.edu/people/core-faculty/legoues-claire.html", "", "Automated program repair; software testing; program analysis; assurance", "Direct fit with TerraProbe's repair/evaluation work and reliable AI-assisted software development.", "Human and AI Roles in Software Engineering", "https://s3d.cmu.edu/news/2026/0728-humans-in-se.html", "2026", angle="Connect TerraProbe's Terraform repair evidence to evaluation of AI-assisted repair and human oversight.", question="Which evaluation failures in LLM-based repair are highest priority for a new PhD student?"),
    prof("us:ipeds:145637", "University of Illinois Urbana-Champaign", "Computer Science PhD", "Lingming Zhang", "Siebel School of Computing and Data Science", "Associate Professor", "https://siebelschool.illinois.edu/about/people/all-faculty/lingming", "lingming@illinois.edu", "Software engineering; testing; program repair; code LLMs and agents", "Technically excellent match, but the program is excluded on its published GPA threshold.", "Demystifying LLM-Based Software Engineering Agents", "https://lingming.cs.illinois.edu/publications/fse2025.pdf", "2025", priority="Do not contact unless GPA exception is authorized", angle="Only inquire after program confirms GPA eligibility.", question="Does the rare-exception policy permit review with a 3.35 cumulative and >3.5 recent-two-year GPA?"),
    prof("us:ipeds:139755", "Georgia Institute of Technology-Main Campus", "Computer Science PhD", "Alessandro Orso", "School of Computer Science", "Professor and Associate School Chair", "https://people.research.gatech.edu/alessandro-orso", "alessandro.orso@cc.gatech.edu", "Software testing; program analysis; reliability; security", "Strong alignment with automated repair validation, IaC analysis, and reliable software systems.", "Generating REST API Specifications through Static Analysis", "https://sites.cc.gatech.edu/home/orso/orso.pdf", "2024", angle="Relate Terraform/configuration repair to static analysis and executable specification validation.", question="Are there funded Fall 2027 projects applying program analysis to configuration or AI-generated code?"),
    prof("us:ipeds:228778", "The University of Texas at Austin", "Computer Science PhD", "Isil Dillig", "Department of Computer Science", "Professor and Department Chair", "https://www.cs.utexas.edu/people/faculty-researchers/isil-dillig", "isil@cs.utexas.edu", "Program analysis; verification; synthesis; security", "Exceptional methods match for automated repair, evidence-backed verification, and trustworthy code generation.", "VeriSoftBench: Evaluating LLMs for Formal Software Verification", "https://www.cs.utexas.edu/~isil/publications.html", "2026", angle="Frame TerraProbe and Evidex as repair plus verification/evidence-grounding experience.", question="Which verification tasks would best expose false confidence in LLM-generated repairs?"),
    prof("us:ipeds:110653", "University of California-Irvine", "Software Engineering PhD", "Joshua Garcia", "Department of Informatics", "Associate Professor", "https://jgarcia.ics.uci.edu/", "", "Static/dynamic/AI-based analysis; software security; testing; vulnerability management", "Strong match to automated infrastructure repair and secure, explainable validation pipelines.", "Open-Source Software Vulnerability Management in Practice", "https://jgarcia.ics.uci.edu/?page_id=7", "2025", angle="Connect IaC repair and evidence verification to vulnerability-management workflows.", question="Does the group anticipate funded Fall 2027 work on AI-assisted analysis or secure configuration repair?"),
    prof("us:ipeds:233921", "Virginia Polytechnic Institute and State University", "Computer Science PhD", "Na Meng", "Department of Computer Science", "Associate Professor", "https://website.cs.vt.edu/people/faculty/na-ming.html", "nm8247@cs.vt.edu", "Software engineering; program transformation; LLMs; testing; security", "Near-direct fit to build/configuration repair, LLM-assisted maintenance, and rigorous evaluation.", "How Effectively Do LLMs Help with Build Conflict Resolution?", "https://people.cs.vt.edu/nm8247/publications.html", "2026", angle="Lead with TerraProbe and ask about build/configuration conflict evaluation.", question="What failure modes matter most in current LLM-assisted build and configuration repair research?"),
    prof("us:ipeds:232186", "George Mason University", "Computer Science PhD", "Brittany Johnson-Matthews", "Department of Computer Science", "Assistant Professor", "https://people.cs.gmu.edu/~johnsonb/", "johnsonb@gmu.edu", "Human-centered software engineering; program repair; developer tools", "Strong human/practical evaluation complement to the applicant's repair-system experience.", "Exploring Experiences with Automated Program Repair in Practice", "https://doi.org/10.1145/3597503.3639182", "2024", angle="Discuss practitioner trust and evidence requirements for automated Terraform repair.", question="Would a Fall 2027 project on developer trust in LLM-based configuration repair have funded support?"),
    prof("us:ipeds:199193", "North Carolina State University at Raleigh", "Computer Science PhD", "Kathryn Stolee", "Department of Computer Science", "Associate Professor", "https://csc.ncsu.edu/people/ktstolee/", "", "Software engineering; program analysis; testing; developer interaction with AI", "Strong fit for evaluating how developers use and validate AI-generated repairs.", "How Do Developers Interact with AI?", "https://csc.ncsu.edu/people/ktstolee/", "2026", angle="Connect TerraProbe's repair workflow to developer-AI interaction and validation.", question="Are funded Fall 2027 RA openings expected, and is baseline support available independent of a specific grant?"),
    prof("us:ipeds:214777", "Pennsylvania State University-Main Campus", "Computer Science and Engineering PhD", "Gang Tan", "Department of Computer Science and Engineering", "Distinguished Professor", "https://www.eecs.psu.edu/departments/directory-detail-g.aspx?q=gxt29", "gxt29@psu.edu", "Software security; programming languages; formal methods; program analysis", "Strong match for secure and formally grounded repair/evaluation.", "Comprehensive Memory Safety Validation", "https://www.eecs.psu.edu/departments/directory-detail-g.aspx?q=gxt29", "2024", angle="Tie evidence-grounded claims to proof-oriented software security and validation.", question="Can the department offer multi-year support independent of annual RA renewal?"),
    prof("us:ipeds:209542", "Oregon State University", "Computer Science PhD", "Manish Motwani", "School of Electrical Engineering and Computer Science", "Assistant Professor", "https://engineering.oregonstate.edu/people/manish-motwani", "manish.motwani@oregonstate.edu", "Software testing; program repair; program analysis; automated specifications", "Direct fit with repair, testing, and infrastructure specification recovery.", "Generating REST API Specifications through Static Analysis", "https://doi.org/10.1145/3597503.3639137", "2024", angle="Relate Terraform repair to specification inference and validation.", question="Are funded Fall 2027 projects available, and does the CS program guarantee baseline support?"),
    prof("us:ipeds:166629", "University of Massachusetts-Amherst", "Computer Science PhD", "Yuriy Brun", "Manning College of Information and Computer Sciences", "Professor", "https://www.cics.umass.edu/about/directory/yuriy-brun", "brun@cs.umass.edu", "Software engineering; automated repair; testing; reliable AI-assisted development", "Exceptional match to Terraform repair and evidence-centered evaluation.", "LLM-Assisted Formal Verification", "https://people.cs.umass.edu/~brun/", "2025", angle="Connect TerraProbe repair evidence and Evidex grounding to reliable AI-for-SE.", question="Which reliability benchmarks would be most valuable for infrastructure-code repair agents?"),
    prof("us:ipeds:163286", "University of Maryland-College Park", "Computer Science PhD", "David Van Horn", "Department of Computer Science", "Associate Professor", "https://www.cs.umd.edu/~dvanhorn/", "", "Programming languages; program analysis; verification; security", "Strong theoretical foundation for sound repair and verification of generated code.", "Webs", "https://www.cs.umd.edu/~dvanhorn/", "2025", angle="Frame repair correctness as a semantics and verification problem.", question="Are there Fall 2027 opportunities applying PL methods to trustworthy AI-generated software?"),
    prof("us:ipeds:170976", "University of Michigan-Ann Arbor", "Computer Science and Engineering PhD", "Westley Weimer", "Computer Science and Engineering", "Professor", "https://eecs.engin.umich.edu/people/weimer-westley/", "", "Automated program repair; software engineering; program analysis; software quality", "Canonical fit for the applicant's automated Terraform repair background.", "Automated Program Repair: Emerging Trends and Future Directions", "https://doi.org/10.1145/3704997", "2025", angle="Lead with TerraProbe's accepted full paper and the evaluation design behind its repair claims.", question="What new evaluation problems in LLM-era automated repair are most important for incoming PhD work?"),
    prof("us:ipeds:231624", "William & Mary", "Computer Science PhD", "Denys Poshyvanyk", "Department of Computer Science", "Chancellor Professor and Department Chair", "https://www.cs.wm.edu/~dposhyvanyk/index.html", "dposhyvanyk@wm.edu", "Software evolution; repository mining; testing; AI-for-SE; security", "Exceptional fit for empirical evaluation of AI-generated repairs and code provenance.", "Hallucination Detection in LLM-Generated Code", "https://www.cs.wm.edu/~dposhyvanyk/publications.html", "2026", instructions="Program says advisor contact is not required and confers no admissions priority; contact only with a substantive research question", angle="Connect Evidex grounding and TerraProbe to hallucination/provenance validation in generated code.", question="Which empirical signals best distinguish plausible from trustworthy LLM-generated code changes?"),
    prof("us:ipeds:110644", "University of California-Davis", "Computer Science PhD", "Cindy Rubio-González", "Department of Computer Science", "Professor", "https://cs.ucdavis.edu/directory/cindy-rubio-gonzalez", "crubio@ucdavis.edu", "Program analysis; automated bug finding; optimization; software defects", "Direct methods fit for automated configuration analysis and repair validation.", "CI-Bench: Evaluating LLM Tools on Continuous-Integration Failures", "https://web.cs.ucdavis.edu/~rubio/", "2026", angle="Relate Terraform failures to CI defect benchmarks and program-analysis validation.", question="Could a Fall 2027 project on IaC/CI repair carry a multi-year funding commitment?"),
    prof("us:ipeds:243780", "Purdue University-Main Campus", "Computer Science PhD", "Lin Tan", "Department of Computer Science", "Professor", "https://www.cs.purdue.edu/people/faculty/lintan.html", "lintan@purdue.edu", "Software dependability; AI-SE synergy; software text analytics; testing", "Strong fit for reliable AI-assisted maintenance and evidence-based code quality.", "Recent AI/SE and software dependability publications", "https://www.cs.purdue.edu/homes/lintan/text.html", "2025", angle="Discuss rigorous evidence for repair correctness and reliability in AI-assisted workflows.", question="Is funded Fall 2027 RA support expected, given that admission without funding is possible?"),
    prof("us:ipeds:167358", "Northeastern University", "Computer Science PhD", "Jonathan Bell", "Khoury College of Computer Sciences", "Associate Professor", "https://www.khoury.northeastern.edu/people/jonathan-bell/", "j.bell@northeastern.edu", "Software engineering; program analysis; testing; dependency management", "Strong fit for build/configuration reliability and automated test/analysis infrastructure.", "Dependency management and software supply-chain analysis", "https://doi.org/10.1109/ICSE48619.2023.00124", "2023", angle="Connect Terraform dependency/configuration repair to supply-chain and testing research.", question="What build/configuration reliability problems are current priorities for the group?"),
    prof("us:ipeds:153603", "Iowa State University", "Computer Science PhD", "Myra Cohen", "Department of Computer Science", "Professor and Lanh & Oanh Nguyen Chair", "https://www.cs.iastate.edu/people/myra-cohen", "mcohen@iastate.edu", "Configurable software; software testing; search-based software engineering", "Exceptional fit for Terraform/configuration repair and combinatorial evaluation.", "Configurable-software failure and testing research", "https://doi.org/10.1145/3646548.3672597", "2024", angle="Lead with Terraform configuration repair and testing methodology.", question="Which configurable-systems benchmarks would make a strong Fall 2027 PhD project, and how secure is years 3–5 funding?"),
    prof("us:ipeds:181464", "University of Nebraska-Lincoln", "Computer Science PhD", "Hamid Bagheri", "School of Computing", "Associate Professor", "https://cse.unl.edu/~hbagheri/", "hbagheri@unl.edu", "Software engineering; automated repair; formal methods; security; LLMs", "Direct match to LLM-assisted repair and rigorous software validation.", "LLM Agent Issue-to-Commit and Alloy-Model Repair Projects", "https://cse.unl.edu/~hbagheri/publications.html", "2026", angle="Connect TerraProbe to LLM repair agents and Evidex to grounded validation.", question="Can the program confirm direct BS entry and a full multi-year funding package for Fall 2027?"),
    prof("us:ipeds:228787", "The University of Texas at Dallas", "Computer Science PhD", "W. Eric Wong", "Department of Computer Science", "Professor", "https://cs.utdallas.edu/people/faculty/", "ewong@utdallas.edu", "Software testing; debugging; reliability; safety; program repair", "Strong repair/testing match, subject to the program's last-60-hour GPA rule and funding uncertainty.", "Search-Based Automated Program Repair: A Survey", "https://doi.org/10.1109/QRS-C63300.2024.00063", "2024", angle="Discuss Terraform repair search spaces and evidence-backed patch validation.", question="Would the department pre-assess last-60-hour GPA eligibility and expected Fall 2027 funding?"),
    prof("us:ipeds:221999", "Vanderbilt University", "Computer Science PhD", "Kevin Leach", "Department of Computer Science", "Assistant Professor", "https://computing.vanderbilt.edu/bio/kevin-leach/", "kevin.leach@vanderbilt.edu", "Software engineering; cybersecurity; dependable systems; human factors", "Excellent fit for secure, dependable software and evidence-rich evaluation of developer tooling.", "Who's Pushing the Code? An Exploration of GitHub Impersonation", "https://www.vanderbilt.edu/valiant/author/waddelma/page/29/", "2025", angle="Connect repair-agent trust and evidence provenance to secure developer workflows.", question="What Fall 2027 projects at the software-engineering/security intersection would benefit from repair and claim-verification experience?"),
    prof("us:ipeds:152080", "University of Notre Dame", "Computer Science and Engineering PhD", "Joanna Cecilia da Silva Santos", "Department of Computer Science and Engineering", "Assistant Professor", "https://cse.nd.edu/faculty/joanna-cecilia-da-silva-santos/", "jdasilv2@nd.edu", "Software engineering; software security; program analysis; source-code manipulation", "Exceptional direct fit for LLM-generated security tests, software verification, and secure repair.", "Leveraging LLMs to Generate Security Tests for Mobile Apps", "https://cse.nd.edu/news/santos-wins-google-research-award/", "2024", angle="Lead with TerraProbe and ask about adapting LLM repair/testing to security-sensitive configurations.", question="Does S2E anticipate a funded Fall 2027 opening focused on LLM security testing or program analysis?"),
    prof("us:ipeds:179867", "Washington University in St Louis", "Computer Science PhD", "Umar Iqbal", "Department of Computer Science and Engineering", "Assistant Professor", "https://engineering.washu.edu/faculty/Umar-Iqbal.html", "umar.iqbal@wustl.edu", "AI-agent security and reliability; web privacy/security; LLM-platform evaluation", "Exceptional overlap with agent security, evidence-grounded claims, and trustworthy evaluation.", "AI Agents Prompt Redesign of Web for Security, Privacy, Reliability", "https://engineering.washu.edu/news/2026/AI-agents-prompt-redesign-of-web-for-security-privacy-reliability.html", "2026", angle="Connect Evidex to claim fidelity and TerraProbe to safe agent actions over infrastructure.", question="Which agent reliability or permission failures are the strongest fit for an incoming Fall 2027 student?"),
    prof("us:ipeds:201645", "Case Western Reserve University", "Computer Science PhD", "Sumon Biswas", "Department of Computer and Data Sciences", "Assistant Professor", "https://engineering.case.edu/about/school-directory/sumon-biswas", "sumon@case.edu", "Responsible AI engineering; software engineering; verification; fairness and safety; reasoning LLMs", "Exceptional fit for evidence-grounded verification and trustworthy AI-enabled software systems.", "FairSense: Long-Term Fairness Analysis of ML-Enabled Systems", "https://engineering.case.edu/about/school-directory/sumon-biswas", "2025", angle="Frame Evidex as evidence-grounded AI evaluation and TerraProbe as trustworthy software automation.", question="Would a Fall 2027 offer for responsible-AI engineering include guaranteed multi-year support?"),
    prof("us:ipeds:195003", "Rochester Institute of Technology", "Computing and Information Sciences PhD", "Yinxi Liu", "Department of Cybersecurity", "Assistant Professor", "https://www.rit.edu/computing/directory/yxlics-yinxi-liu", "yxlics@rit.edu", "Software/web security; AI and agent security; program analysis; testing; security measurement", "Near-direct match to agent security, program analysis/testing, and infrastructure configuration security.", "Current PhD Research Opening: AI/Agent Security and Program Analysis/Testing", "https://www.rit.edu/cybersecurity/phd-research-opportunities", "2026", recruiting_status="Confirmed recruiting", recruiting_evidence="Official RIT PhD Research Opportunities page lists Yinxi Liu with one available PhD position in software/web security, AI/agent security, program analysis, testing, and security measurement", instructions="Apply to the Computing and Information Sciences PhD and send a concise fit inquiry referencing the current official opening", angle="Lead with TerraProbe's infrastructure repair/security and Evidex's evaluation/grounding work.", question="Is the advertised PhD opening intended for Fall 2027, and what funding duration/benefits are guaranteed?", notes="Confirmed recruiting is limited to the current official opening; the start cycle and final availability must be reconfirmed."),
]


SOURCE_SPECS: dict[str, list[tuple[str, str, str, str, str, str, str]]] = {
    "Carnegie Mellon University": [
        ("https://se-phd.isri.cmu.edu/", "Program status, application process, fee waiver, and research scope", "Software Engineering PhD", "Official program page", "Fall 2027/current", "High", ""),
        ("https://admissions.scs.cmu.edu/portal/apply_gr", "Fall 2027 early and final deadlines", "SCS Graduate Application", "Official admissions portal", "Fall 2027", "High", ""),
        ("https://se-phd.s3d.cmu.edu/Prospective%20Students/index.html", "Guaranteed tuition and living support for admitted SE PhD students", "Prospective Students", "Official funding/program page", "Current", "High", ""),
        ("https://s3d.cmu.edu/people/core-faculty/legoues-claire.html", "Current appointment and repair/testing research", "Claire Le Goues", "Official faculty page", "N/A", "High", ""),
        ("https://s3d.cmu.edu/news/2026/0728-humans-in-se.html", "Current AI/software-engineering project evidence", "Humans in Software Engineering", "Official university news", "N/A", "High", ""),
    ],
    "University of Illinois Urbana-Champaign": [
        ("https://catalog.illinois.edu/graduate/engineering/computer-science-phd/", "Active PhD, direct bachelor's entry, 3.40 minimum, and five-year funding model", "Computer Science PhD Catalog", "Official catalog", "Current", "High", ""),
        ("https://grad.illinois.edu/admissions/application-instructions/completing-your-graduate-application", "$90 fee and waiver policy", "Completing Your Graduate Application", "Official admissions page", "Current", "High", ""),
        ("https://siebelschool.illinois.edu/about/people/all-faculty/lingming", "Current appointment, email, and research themes", "Lingming Zhang", "Official faculty page", "N/A", "High", ""),
        ("https://lingming.cs.illinois.edu/publications/fse2025.pdf", "2025 LLM-based software-engineering agents paper", "Demystifying LLM-Based Software Engineering Agents", "University-hosted scholarly paper", "N/A", "High", ""),
    ],
    "Georgia Institute of Technology-Main Campus": [
        ("https://gradapp.gatech.edu/portal/program-info?cmd=view-program&program=169bcfc7-d134-ed0b-40e7-12bc93147f9a", "Fall 2027 deadline, bachelor/equivalent, 3.0 GPA, international rules, and program contact", "Computer Science PhD Program Information", "Official admissions portal", "Fall 2027", "High", ""),
        ("https://www.cc.gatech.edu/degree-programs/phd-computer-science", "Active CS PhD program and research scope", "PhD in Computer Science", "Official program page", "Current", "High", ""),
        ("https://math.gatech.edu/node/75", "$95 domestic/$105 international institute application fee", "Graduate Application Information", "Official university page", "Current", "Medium", "Fee page is hosted by another Georgia Tech department but states institute-wide fee."),
        ("https://people.research.gatech.edu/alessandro-orso", "Current appointment, email, and testing/program-analysis research", "Alessandro Orso", "Official faculty page", "N/A", "High", ""),
        ("https://sites.cc.gatech.edu/home/orso/orso.pdf", "2024 recent publication evidence", "Alessandro Orso CV", "Official university-hosted CV", "N/A", "High", ""),
    ],
    "The University of Texas at Austin": [
        ("https://www.cs.utexas.edu/graduate/apply", "Bachelor/comparable degree, 3.0 upper-division GPA, current December 15 deadline, and admissions contact", "Graduate Admissions", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://www.cs.utexas.edu/graduate/cost-and-aid", "Most PhDs receive first-five-year support and assistantship benefits", "Graduate Cost and Aid", "Official funding page", "Current", "High", ""),
        ("https://graduate.utexas.edu/admissions/apply", "$65 domestic/$90 international fee and international waiver limitation", "Apply for Graduate Admission", "Official admissions page", "Current", "High", ""),
        ("https://www.cs.utexas.edu/people/faculty-researchers/isil-dillig", "Current appointment and research themes", "Isil Dillig", "Official faculty page", "N/A", "High", ""),
        ("https://www.cs.utexas.edu/~isil/publications.html", "2026 formal-verification benchmark publication", "Isil Dillig Publications", "Official faculty publication page", "N/A", "High", ""),
    ],
    "University of California-Irvine": [
        ("https://informatics.ics.uci.edu/phd-software-engineering/", "Active Software Engineering PhD and faculty-contact guidance", "Software Engineering PhD", "Official program page", "Current", "High", ""),
        ("https://ics.uci.edu/admissions-information-and-computer-science/graduate-admissions/graduate-research-admissions-faq/", "December 15 deadline, GPA, GRE, international, multiple applications, and funding language", "Graduate Research Admissions FAQ", "Official admissions page", "Current", "High", ""),
        ("https://apply.grad.uci.edu/apply/?sr=e7677a64-54d2-41ab-b4c5-71f0e1dd6034", "Fall 2027 application opens October 1, 2026", "UCI Graduate Application", "Official application portal", "Fall 2027", "High", ""),
        ("https://grad.uci.edu/admissions/application-fee-fee-waivers/", "$135 domestic/$155 international fee and waiver rules", "Application Fee and Fee Waivers", "Official admissions page", "Current", "High", ""),
        ("https://jgarcia.ics.uci.edu/?page_id=7", "Current research and 2025 recent publication evidence", "Joshua Garcia Publications", "Official faculty site", "N/A", "High", ""),
    ],
    "Virginia Polytechnic Institute and State University": [
        ("https://website.cs.vt.edu/academic/graduate/future-grads/doctorate.html", "Active PhD, direct bachelor's route, GPA, English, and dissertation", "Doctorate", "Official program page", "Current", "High", ""),
        ("https://website.cs.vt.edu/academic/graduate/future-grads/ApplicationDeadlines.html", "Fall 2027 December 1 deadline", "Application Deadlines", "Official admissions page", "Fall 2027", "High", ""),
        ("https://students.cs.vt.edu/Graduate/Funding.html", "Five-year offer to 100% of admitted PhDs beginning Fall 2026, excluding summers", "Graduate Funding", "Official funding page", "Current", "High", ""),
        ("https://graduateschool.vt.edu/admissions/tuition-and-costs/Application_Fees.html", "$75 application fee", "Application Fees", "Official admissions page", "Current", "High", ""),
        ("https://people.cs.vt.edu/nm8247/publications.html", "Current 2025–26 LLM, testing, build-conflict, and security work", "Na Meng Publications", "Official faculty publication page", "N/A", "High", ""),
    ],
    "George Mason University": [
        ("https://cs.gmu.edu/academics/graduate-programs", "Active CS PhD", "Graduate Programs", "Official program page", "Current", "High", ""),
        ("https://itsapps.gmu.edu/graduate-deadlines-and-requirements/Programs/Details/a3L1I0000002hg6UAA", "Latest published Fall 2026 deadlines; Fall 2027 unavailable", "Program Deadlines and Requirements", "Official admissions page", "Fall 2026", "High", ""),
        ("https://graduate.gmu.edu/studying-here/prospective-students", "$75 application fee and limited waivers", "Prospective Students", "Official admissions page", "Current", "High", ""),
        ("https://people.cs.gmu.edu/~johnsonb/", "Current faculty research profile", "Brittany Johnson-Matthews", "Official faculty site", "N/A", "High", ""),
        ("https://doi.org/10.1145/3597503.3639182", "2024 automated program repair in practice paper", "Exploring Experiences with Automated Program Repair in Practice", "Scholarly publisher", "N/A", "High", ""),
    ],
    "North Carolina State University at Raleigh": [
        ("https://csc.ncsu.edu/academics/graduate/phd/", "Active PhD, 72-hour bachelor route, dissertation, and advisor-determined RA funding", "Computer Science PhD", "Official program page", "Current", "High", ""),
        ("https://csc.ncsu.edu/academics/graduate/application-deadlines/", "Current December 15 fall PhD deadline and fall-only foreign admission", "Application Deadlines", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://catalog.ncsu.edu/graduate/engineering/computer-science/computer-science.pdf", "Bachelor's eligibility, B-average expectation, and English requirements", "Computer Science Graduate Catalog", "Official catalog", "Current", "High", ""),
        ("https://grad.ncsu.edu/programs/where-do-i-start/", "$85 domestic/$95 international application fee", "Where Do I Start?", "Official admissions page", "Current", "High", ""),
        ("https://csc.ncsu.edu/people/ktstolee/", "Current appointment and 2026 developer/AI work", "Kathryn Stolee", "Official faculty page", "N/A", "High", ""),
    ],
    "Pennsylvania State University-Main Campus": [
        ("https://www.eecs.psu.edu/students/graduate/Graduate-Degree-Programs-CSE.aspx", "Active CSE PhD", "Graduate Degree Programs — CSE", "Official program page", "Current", "High", ""),
        ("https://www.eecs.psu.edu/students/graduate/EECS-graduate-deadlines.aspx", "Current December 20 fall deadline without Fall 2027 label", "EECS Graduate Deadlines", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://gradschool.psu.edu/admissions/prepare-to-apply?country=NGA", "International degree eligibility, $65/$85 fee, and one-application rule", "Prepare to Apply — Nigeria", "Official admissions page", "Current", "High", ""),
        ("https://www.eecs.psu.edu/Students/graduate/EECS-students-graduate-funding-opportunities.aspx", "Competitive TA/RA benefits and non-guaranteed renewal/summer", "Graduate Funding Opportunities", "Official funding page", "Current", "High", ""),
        ("https://www.eecs.psu.edu/departments/directory-detail-g.aspx?q=gxt29", "Current appointment, email, themes, and 2024 work", "Gang Tan", "Official faculty page", "N/A", "High", ""),
    ],
    "Oregon State University": [
        ("https://engineering.oregonstate.edu/academics/programs/computer-science/graduate", "Active PhD, direct bachelor, exact Fall 2027 deadline, and no program fee waiver", "Computer Science Graduate Program", "Official program page", "Fall 2027", "High", ""),
        ("https://gradadmissions.oregonstate.edu/preparing-graduate-school", "$85 fee and international waiver limitation", "Preparing for Graduate School", "Official admissions page", "Current", "High", ""),
        ("https://engineering.oregonstate.edu/people/manish-motwani", "Current appointment, email, and research themes", "Manish Motwani", "Official faculty page", "N/A", "High", ""),
        ("https://doi.org/10.1145/3597503.3639137", "2024 static-analysis/specification paper", "Generating REST API Specifications through Static Analysis", "Scholarly publisher", "N/A", "High", ""),
    ],
    "University of Massachusetts-Amherst": [
        ("https://www.cics.umass.edu/academics/phd-computer-science/how-apply-phd-program", "Active PhD, current deadline, fee, bachelor background, and international requirements", "How to Apply to the PhD Program", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://www.cics.umass.edu/academics/academic-policies/graduate-programs-policies/msphd-degree-requirements/other-msphd-program-information", "Five-year conditional doctoral funding guarantee", "Other MS/PhD Program Information", "Official funding/policy page", "Current", "High", ""),
        ("https://www.cics.umass.edu/about/directory/yuriy-brun", "Current appointment and research areas", "Yuriy Brun", "Official faculty page", "N/A", "High", ""),
        ("https://people.cs.umass.edu/~brun/", "2025 recent work and sustained repair/testing research", "Yuriy Brun", "Official faculty site", "N/A", "High", ""),
    ],
    "University of Maryland-College Park": [
        ("https://www.cs.umd.edu/grad/apply", "Fall 2027 deadline, fee, GRE, and international requirements", "Graduate Application", "Official admissions page", "Fall 2027", "High", ""),
        ("https://www.cs.umd.edu/grad/admissions-faq", "Direct bachelor's eligibility, committee/faculty model, and funding description", "Admissions FAQ", "Official admissions page", "Current", "High", ""),
        ("https://academiccatalog.umd.edu/graduate/programs/computer-science-cmsc/", "Active PhD and broad full-time doctoral support", "Computer Science Graduate Catalog", "Official catalog", "Current", "High", ""),
        ("https://www.cs.umd.edu/~dvanhorn/", "Current appointment, research themes, and 2024–25 work", "David Van Horn", "Official faculty site", "N/A", "High", ""),
    ],
    "University of Michigan-Ann Arbor": [
        ("https://cse.engin.umich.edu/academics/graduate/admissions/", "Fall 2027 deadline, direct bachelor's eligibility, international rules, typical GPA, and funding guarantee", "Graduate Admissions", "Official admissions page", "Fall 2027", "High", ""),
        ("https://cse.engin.umich.edu/academics/graduate/admissions/funding/", "Full tuition, stipend, health, and duration", "PhD Funding", "Official funding page", "Current", "High", ""),
        ("https://rackham.umich.edu/admissions/applying/application-fee-and-payment/", "$75 domestic/$90 international fee and waiver rules", "Application Fee and Payment", "Official admissions page", "Current", "High", ""),
        ("https://eecs.engin.umich.edu/people/weimer-westley/", "Current appointment and research themes", "Westley Weimer", "Official faculty page", "N/A", "High", ""),
        ("https://doi.org/10.1145/3704997", "2025 automated program repair work", "Automated Program Repair: Emerging Trends", "Scholarly publisher", "N/A", "High", ""),
    ],
    "William & Mary": [
        ("https://cdsp.wm.edu/admissions/graduate/computer-science/", "Active PhD, direct bachelor, current deadlines, no-advisor rule, and funding", "Computer Science Graduate Admissions", "Official admissions/program page", "Current; cycle not labeled", "High", ""),
        ("https://catalog.wm.edu/graduate/school-computing-data-sciences-physics/admission/", "$50 application fee", "Graduate Admission", "Official catalog", "Current", "High", ""),
        ("https://www.cs.wm.edu/~dposhyvanyk/index.html", "Current appointment, email, and research themes", "Denys Poshyvanyk", "Official faculty site", "N/A", "High", ""),
        ("https://www.cs.wm.edu/~dposhyvanyk/publications.html", "2025–26 AI-for-SE and code-hallucination work", "Denys Poshyvanyk Publications", "Official faculty publication page", "N/A", "High", ""),
    ],
    "University of California-Davis": [
        ("https://grad.ucdavis.edu/programs/gcsi", "Active CS PhD and Fall 2027 deadline", "Computer Science Graduate Program", "Official program page", "Fall 2027", "High", ""),
        ("https://cs.ucdavis.edu/graduate/prospective-students/how-apply", "3.0 GPA, English/international rules, and deadline", "How to Apply", "Official admissions page", "Current", "High", ""),
        ("https://grad.ucdavis.edu/admissions-process-overview", "$135/$155 fee, separate applications, and waiver policy", "Admissions Process Overview", "Official admissions page", "Current", "High", ""),
        ("https://grad.ucdavis.edu/international-applicants", "First-year support may be offered but later funding may be uncertain", "International Applicants", "Official admissions/funding page", "Current", "High", ""),
        ("https://web.cs.ucdavis.edu/~rubio/", "Current appointment context and 2026 CI/defect work", "Cindy Rubio-González", "Official faculty site", "N/A", "High", ""),
    ],
    "Purdue University-Main Campus": [
        ("https://www.cs.purdue.edu/graduate/admission/steps.html", "Fall 2027 deadline, admission model, funding consideration, possible unfunded admission, and contact", "Graduate Admission Steps", "Official admissions page", "Fall 2027", "High", ""),
        ("https://engineering.purdue.edu/IE/academics/graduate/future/future-grad-requirements", "$60 domestic/$75 international Graduate School fee", "Graduate Application Requirements", "Official university page", "Current", "Medium", "Institution-wide fee is stated on another Purdue department page."),
        ("https://www.cs.purdue.edu/people/faculty/lintan.html", "Current appointment, email, and research themes", "Lin Tan", "Official faculty page", "N/A", "High", ""),
        ("https://www.cs.purdue.edu/homes/lintan/text.html", "Recent software-dependability/AI-SE work", "Lin Tan Research", "Official faculty site", "N/A", "High", ""),
    ],
    "Northeastern University": [
        ("https://www.khoury.northeastern.edu/apply/phd-apply/", "Active PhD, direct bachelor's route, English, GRE, current deadline, and admission model", "Apply to the PhD Program", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://devsite.khoury.northeastern.edu/apply/phd-apply/financial-support-for-phd-students/", "Five-year package, tuition, health insurance, and assistantship", "Financial Support for PhD Students", "Official college funding page", "Current", "Medium", "Official Khoury domain uses a devsite path; confirm at offer stage."),
        ("https://www.khoury.northeastern.edu/phd-programs/khoury-phd-open-house/", "Current PhD funding/health context and fee-waiver event path", "Khoury PhD Open House", "Official college page", "Current", "High", ""),
        ("https://www.khoury.northeastern.edu/people/jonathan-bell/", "Current appointment, email, and research themes", "Jonathan Bell", "Official faculty page", "N/A", "High", ""),
        ("https://doi.org/10.1109/ICSE48619.2023.00124", "Recent dependency-management software-engineering work", "ICSE 2023 Paper", "Scholarly publisher", "N/A", "High", ""),
    ],
    "Iowa State University": [
        ("https://www.cs.iastate.edu/graduate-studies/phd-application-requirements", "Fall 2027 deadlines, free application, international rules, faculty list, and initial funding package", "PhD Application Requirements", "Official admissions page", "Fall 2027", "High", ""),
        ("https://www.cs.iastate.edu/graduate-studies/faq-prospective-graduate-students", "Direct bachelor's eligibility and later funding norm", "Prospective Graduate Student FAQ", "Official admissions/funding page", "Current", "High", ""),
        ("https://www.cs.iastate.edu/people/myra-cohen", "Current appointment, email, and configurable-software/testing research", "Myra Cohen", "Official faculty page", "N/A", "High", ""),
        ("https://doi.org/10.1145/3646548.3672597", "2024 configurable-software testing work", "Recent Configurable Software Research", "Scholarly publisher", "N/A", "Medium", "DOI used as recent-work evidence; faculty page establishes current appointment."),
    ],
    "University of Nebraska-Lincoln": [
        ("https://graduate.unl.edu/academics/programs/COMP-PHD/", "Active PhD, fee, current deadlines, English, GRE, advisor-interest prompt, and contacts", "Computer Science PhD", "Official admissions/program page", "Current; cycle not labeled", "High", ""),
        ("https://graduate.unl.edu/application-requirements-additional-details/", "Separate $50 fees for multiple applications", "Application Requirements — Additional Details", "Official admissions page", "Current", "High", ""),
        ("https://cse.unl.edu/~hbagheri/", "Current appointment and research themes", "Hamid Bagheri", "Official faculty site", "N/A", "High", ""),
        ("https://cse.unl.edu/~hbagheri/publications.html", "2025–26 LLM/program-repair work", "Hamid Bagheri Publications", "Official faculty publication page", "N/A", "High", ""),
    ],
    "The University of Texas at Dallas": [
        ("https://catalog.utdallas.edu/2026/graduate/programs/ecs/computer-science", "Active PhD, BS-entry requirements, last-60 GPA, dissertation, and current deadline", "Computer Science Graduate Catalog", "Official catalog", "2026–27; date not explicitly Fall 2027", "High", ""),
        ("https://academics.utdallas.edu/fact-sheets/ecs/phd-computer-science/", "Program contacts and current admissions summary", "Computer Science PhD Fact Sheet", "Official program page", "Current", "High", ""),
        ("https://graduate-admissions.utdallas.edu/apply-to-ut-dallas/deadlines-and-fees/", "$75 application fee", "Deadlines and Fees", "Official admissions page", "Current", "High", ""),
        ("https://cs.utdallas.edu/admissions/admissions-faq/", "TA timing, no master's prerequisite for BS CS, and lack of funding guarantee", "Admissions FAQ", "Official admissions page", "Current with some stale wording", "Medium", "GRE language conflicts with newer catalog; discrepancy preserved."),
        ("https://doi.org/10.1109/QRS-C63300.2024.00063", "2024 automated program repair survey", "Search-Based Automated Program Repair: A Survey", "Scholarly publisher", "N/A", "High", ""),
    ],
    "Vanderbilt University": [
        ("https://computing.vanderbilt.edu/csphd/", "Fall 2027 deadlines, $95 fee, waiver rule, funding, contacts, and active PhD", "Computer Science PhD Program", "Official program page", "Fall 2027", "High", ""),
        ("https://engineering.vanderbilt.edu/graduate-admissions/", "Fall 2027 final deadlines, GRE, full doctoral assistance, insurance, and fees", "Graduate Programs in Engineering", "Official admissions/funding page", "Fall 2027", "High", ""),
        ("https://computing.vanderbilt.edu/bio/kevin-leach/", "Current appointment and dependable-software/security research", "Kevin Leach", "Official faculty page", "N/A", "High", ""),
        ("https://www.vanderbilt.edu/valiant/author/waddelma/page/29/", "2025 GitHub impersonation/software-security work", "Who's Pushing the Code?", "Official university research page", "N/A", "High", ""),
    ],
    "University of Notre Dame": [
        ("https://engineering.nd.edu/departments-programs/graduate-programs/phd-in-computer-science-and-engineering/", "Active PhD, direct BS route, deadline, research areas, funding, and contact", "PhD in Computer Science and Engineering", "Official program page", "Current; cycle not labeled", "High", ""),
        ("https://graduateschool.nd.edu/admissions/application-requirements/application-fee-and-waiver/", "$75 per application and waiver paths", "Application Fee and Waiver", "Official admissions page", "Current", "High", ""),
        ("https://cse.nd.edu/faculty/joanna-cecilia-da-silva-santos/", "Current appointment, email, and research areas", "Joanna Cecilia da Silva Santos", "Official faculty page", "N/A", "High", ""),
        ("https://cse.nd.edu/news/santos-wins-google-research-award/", "2024 LLM-generated security-testing project", "Santos Wins Google Research Award", "Official university news", "N/A", "High", ""),
    ],
    "Washington University in St Louis": [
        ("https://admin.aprc.wustl.edu/academics/graduate-admissions/deadlines.html", "Current December 1 fall PhD deadline", "Application Deadlines", "Official admissions page", "Current; cycle not labeled", "High", ""),
        ("https://admin.aprc.wustl.edu/academics/graduate-admissions/index.html", "Active CS PhD and full tuition/health doctoral funding", "Graduate Admissions", "Official admissions/funding page", "Current", "High", ""),
        ("https://gradadmit.wustl.edu/register/?id=a12c466a-dd5c-4938-9b45-b852d6de86b4", "Fall 2027 CSE information session and automatic fee waiver for indicated graduate interest", "CSE PhD Virtual Information Session", "Official admissions event page", "Fall 2027", "High", ""),
        ("https://engineering.washu.edu/faculty/Umar-Iqbal.html", "Current appointment, email, and agent/security research", "Umar Iqbal", "Official faculty page", "N/A", "High", ""),
        ("https://engineering.washu.edu/news/2026/AI-agents-prompt-redesign-of-web-for-security-privacy-reliability.html", "2026 agent security/reliability project", "AI Agents Prompt Redesign of Web", "Official university news", "N/A", "High", ""),
    ],
    "Case Western Reserve University": [
        ("https://case.edu/programs/computer-science-phd", "Active PhD, direct bachelor's route, fee, GRE, English, and international eligibility", "Computer Science PhD", "Official program page", "Current", "High", ""),
        ("https://case.edu/gradstudies/prospective-students/admissions-information/application-deadlines", "Fall 2027 priority and final deadlines", "Application Deadlines", "Official admissions page", "Fall 2027", "High", ""),
        ("https://case.edu/engineering/computer-and-data-sciences/academics/computing-science/doctor-philosophy-0", "Direct-undergraduate duration and selective funding language", "PhD in Computer Science", "Official program page", "Current", "High", ""),
        ("https://engineering.case.edu/about/school-directory/sumon-biswas", "Current appointment, email, themes, and 2025 work", "Sumon Biswas", "Official faculty page", "N/A", "High", ""),
    ],
    "Rochester Institute of Technology": [
        ("https://www.rit.edu/study/computing-and-information-sciences-phd", "Active interdisciplinary PhD, bachelor's entry, international eligibility, priority deadline, and typical funding", "Computing and Information Sciences PhD", "Official program page", "2026–27; Fall 2027 not explicit", "High", ""),
        ("https://www.rit.edu/admissions/graduate/applying-doctoral-program", "Direct bachelor's route, typical GPA, and $65 fee", "Applying for a Doctoral Program", "Official admissions page", "Current", "High", ""),
        ("https://www.rit.edu/computing/directory/yxlics-yinxi-liu", "Current appointment and email", "Yinxi Liu", "Official faculty page", "N/A", "High", ""),
        ("https://www.rit.edu/cybersecurity/phd-research-opportunities", "Current explicit PhD opening in agent security and program analysis/testing", "PhD Research Opportunities", "Official research-opportunities page", "Current", "High", "Start cycle not explicit; confirm Fall 2027."),
    ],
}


CONTACTS = {
    "Carnegie Mellon University": ("Graduate Admissions", "SCS Graduate Admissions", "Admissions office", "", "https://www.cs.cmu.edu/education/graduate-admissions"),
    "University of Illinois Urbana-Champaign": ("Graduate Admissions", "Siebel Graduate Admissions", "Program admissions", "grad-admissions@siebelschool.illinois.edu", "https://siebelschool.illinois.edu/academics/graduate/admissions"),
    "Georgia Institute of Technology-Main Campus": ("Graduate Program", "Theresa Nash", "Academic program contact", "ic-academics@cc.gatech.edu", "https://gradapp.gatech.edu/portal/program-info?cmd=view-program&program=169bcfc7-d134-ed0b-40e7-12bc93147f9a"),
    "The University of Texas at Austin": ("Graduate Admissions", "CS Graduate Admissions", "Program admissions", "csadmis@cs.utexas.edu", "https://www.cs.utexas.edu/graduate/apply"),
    "University of California-Irvine": ("Graduate Program", "ICS Graduate Counselors", "Program advising", "gcounsel@ics.uci.edu", "https://ics.uci.edu/admissions-information-and-computer-science/graduate-admissions/"),
    "Virginia Polytechnic Institute and State University": ("Graduate Program", "CS Graduate Program", "Program admissions", "gradinfo@cs.vt.edu", "https://website.cs.vt.edu/academic/graduate/future-grads.html"),
    "George Mason University": ("Graduate Program", "CS Graduate Program", "Program admissions", "", "https://cs.gmu.edu/academics/graduate-programs"),
    "North Carolina State University at Raleigh": ("Graduate Program", "CSC Graduate Program", "Program admissions", "csc-gradoffice@ncsu.edu", "https://csc.ncsu.edu/academics/graduate/"),
    "Pennsylvania State University-Main Campus": ("Graduate Program", "EECS Graduate Office", "Program admissions", "", "https://www.eecs.psu.edu/students/graduate/"),
    "Oregon State University": ("Graduate Program", "EECS Graduate Information", "Program admissions", "eecs.gradinfo@oregonstate.edu", "https://engineering.oregonstate.edu/academics/programs/computer-science/graduate"),
    "University of Massachusetts-Amherst": ("Graduate Program", "CICS Graduate Admissions", "Program admissions", "grad-info@cs.umass.edu", "https://www.cics.umass.edu/academics/phd-computer-science/how-apply-phd-program"),
    "University of Maryland-College Park": ("Graduate Admissions", "CS Graduate Application Support", "Application support", "gradappsupport@umd.edu", "https://www.cs.umd.edu/grad/apply"),
    "University of Michigan-Ann Arbor": ("Graduate Program", "CSE Graduate Admissions", "Program admissions", "csegradstaff@umich.edu", "https://cse.engin.umich.edu/academics/graduate/admissions/"),
    "William & Mary": ("Graduate Program", "CS Graduate Program", "Program admissions", "gradinfo@cs.wm.edu", "https://cdsp.wm.edu/admissions/graduate/computer-science/"),
    "University of California-Davis": ("Graduate Program", "Computer Science Graduate Group", "Program admissions", "csgradadmit@ucdavis.edu", "https://cs.ucdavis.edu/graduate/prospective-students/how-apply"),
    "Purdue University-Main Campus": ("Graduate Program", "CS Graduate Information", "Required admissions contact", "csgradinfo@purdue.edu", "https://www.cs.purdue.edu/graduate/admission/steps.html"),
    "Northeastern University": ("Graduate Program", "Khoury PhD Admissions", "Program admissions", "khoury-phd@northeastern.edu", "https://www.khoury.northeastern.edu/apply/phd-apply/"),
    "Iowa State University": ("Graduate Program", "CS Graduate Admissions", "Program admissions", "csadmissions@iastate.edu", "https://www.cs.iastate.edu/graduate-studies/phd-application-requirements"),
    "University of Nebraska-Lincoln": ("Graduate Program", "Tori Kimminau", "Graduate program coordinator", "tori.kimminau@unl.edu", "https://graduate.unl.edu/academics/programs/COMP-PHD/"),
    "The University of Texas at Dallas": ("Graduate Program", "Shyam Karrah", "Prospective student contact", "skarrah@utdallas.edu", "https://academics.utdallas.edu/fact-sheets/ecs/phd-computer-science/"),
    "Vanderbilt University": ("Graduate Program", "Melissa Harrell", "PhD Graduate Program Coordinator", "CS.PhD.Admin@Vanderbilt.edu", "https://computing.vanderbilt.edu/csphd/"),
    "University of Notre Dame": ("Graduate Program", "Taeho Jung", "Director of Graduate Studies", "cse-grad-info@nd.edu", "https://engineering.nd.edu/departments-programs/graduate-programs/phd-in-computer-science-and-engineering/"),
    "Washington University in St Louis": ("Graduate Program", "CSE Graduate Office", "Program admissions", "", "https://admin.aprc.wustl.edu/academics/graduate-admissions/index.html"),
    "Case Western Reserve University": ("Graduate Program", "Computer and Data Sciences Student Affairs", "Program contact", "cdsecsestudentaffairs@case.edu", "https://case.edu/engineering/computer-and-data-sciences/academics/computing-science/doctor-philosophy-0"),
    "Rochester Institute of Technology": ("Graduate Admissions", "RIT Graduate Admissions", "Admissions office", "gradinfo@rit.edu", "https://www.rit.edu/admissions/graduate/applying-doctoral-program"),
}


def make_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    by_name = {row["institution_name"]: row for row in PROGRAMS}
    for institution_name, specs in SOURCE_SPECS.items():
        program = by_name[institution_name]
        for index, (url, claim, title, kind, cycle, confidence, note) in enumerate(specs, start=1):
            rows.append({
                "source_id": f"{source_id(url)}:{index}",
                "institution_id": program["institution_id"],
                "institution_name": institution_name,
                "program_id": program["program_id"],
                "program_or_professor": program["program_name"],
                "claim_type": "Program/admissions/funding/faculty evidence",
                "exact_claim_supported": claim,
                "source_title": title,
                "publisher": institution_name if "Scholarly publisher" not in kind else "DOI-linked scholarly publisher",
                "publication_date": "",
                "url": url,
                "source_type": kind,
                "official_or_secondary": "Official" if "Scholarly publisher" not in kind else "Primary scholarly source",
                "date_accessed": ACCESSED,
                "admissions_cycle": cycle,
                "confidence": confidence,
                "verification_status": "Verified",
                "access_note": note,
            })
    return rows


def make_contacts() -> list[dict[str, str]]:
    rows = []
    for program in PROGRAMS:
        contact_type, name, role, email, url = CONTACTS[program["institution_name"]]
        rows.append({
            "institution_id": program["institution_id"],
            "institution_name": program["institution_name"],
            "program_id": program["program_id"],
            "program_name": program["program_name"],
            "contact_type": contact_type,
            "contact_name": name,
            "contact_role": role,
            "official_email": email,
            "official_url": url,
            "contact_guidance": program["faculty_contact_expectation"],
            "question_to_resolve": program["unresolved_question"],
            "verification_status": "Official program/contact page checked; blank email means no address was confidently extracted",
            "date_accessed": ACCESSED,
        })
    return rows


def make_exclusions() -> list[dict[str, str]]:
    first_source = {name: specs[0][0] for name, specs in SOURCE_SPECS.items()}
    return [{
        "institution_id": row["institution_id"],
        "institution_name": row["institution_name"],
        "country": row["country"],
        "program_id": row["program_id"],
        "program_name": row["program_name"],
        "stage_of_exclusion": "deep_review_exclusion" if row["screening_decision"] == "excluded" else "deep_review_downgrade",
        "primary_exclusion_reason": row["exclusion_reason"],
        "supporting_evidence": f"{row['funding_status']} Biggest risk: {row['biggest_risk']}",
        "source_url": first_source[row["institution_name"]],
        "confidence": "High" if row["screening_decision"] == "excluded" else "Medium",
        "manual_verification": "Yes — official program/admissions/funding pages checked",
        "date_checked": ACCESSED,
    } for row in PROGRAMS if row["screening_decision"] != "retained"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(sources: list[dict[str, str]], contacts: list[dict[str, str]], exclusions: list[dict[str, str]]) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    if len(PROGRAMS) != 25:
        errors.append(f"expected 25 reviewed programs, found {len(PROGRAMS)}")
    if len({r['institution_id'] for r in PROGRAMS}) != len(PROGRAMS):
        errors.append("duplicate institution_id in programs")
    if len({r['program_id'] for r in PROGRAMS}) != len(PROGRAMS):
        errors.append("duplicate program_id in programs")
    if len(PROFESSORS) < len(PROGRAMS):
        errors.append("fewer than one professor row per reviewed program")
    professors_by_program = Counter(r["program_id"] for r in PROFESSORS)
    sources_by_program = Counter(r["program_id"] for r in sources)
    exclusions_by_program = Counter(r["program_id"] for r in exclusions)
    score_maxima = {
        "professor_fit_score": 30,
        "faculty_depth_score": 15,
        "funding_score": 25,
        "eligibility_score": 15,
        "degree_admissions_score": 10,
        "application_economics_score": 5,
    }
    for row in PROGRAMS:
        missing = [c for c in ("official_program_url", "direct_from_bachelors_eligible", "international_student_eligible", "funding_status", "application_fee", "deadline_cycle_status", "admission_plausibility", "recommendation", "verification_status") if not row[c]]
        if missing:
            errors.append(f"{row['institution_name']}: missing required determinations {missing}")
        if row["admission_plausibility"] not in ADMISSION_PLAUSIBILITY:
            errors.append(f"{row['institution_name']}: invalid admission plausibility")
        if row["recommendation"] not in RECOMMENDATIONS:
            errors.append(f"{row['institution_name']}: invalid recommendation")
        if row["fall_2027_deadline"] and "Fall 2027" not in row["deadline_cycle_status"]:
            errors.append(f"{row['institution_name']}: date present without Fall 2027 cycle label")
        if row["screening_decision"] != "retained":
            if not row["exclusion_reason"]:
                errors.append(f"{row['institution_name']}: non-retained row lacks reason")
            if exclusions_by_program[row["program_id"]] != 1:
                errors.append(f"{row['institution_name']}: non-retained row lacks one downgrade/exclusion record")
        elif row["exclusion_reason"]:
            errors.append(f"{row['institution_name']}: retained row has exclusion reason")
        if professors_by_program[row["program_id"]] < 1:
            errors.append(f"{row['institution_name']}: no professor evidence")
        if sources_by_program[row["program_id"]] < 3:
            errors.append(f"{row['institution_name']}: fewer than three source records")
        components: dict[str, int] = {}
        for field, maximum in score_maxima.items():
            try:
                value = int(row[field])
            except (TypeError, ValueError):
                errors.append(f"{row['institution_name']}: {field} is not an integer")
                continue
            if not 0 <= value <= maximum:
                errors.append(f"{row['institution_name']}: {field}={value} outside 0..{maximum}")
            components[field] = value
        if len(components) == len(score_maxima):
            expected_research = components["professor_fit_score"] + components["faculty_depth_score"]
            expected_overall = sum(components.values())
            if int(row["research_fit_score"]) != expected_research:
                errors.append(f"{row['institution_name']}: research_fit_score arithmetic mismatch")
            if int(row["overall_score"]) != expected_overall:
                errors.append(f"{row['institution_name']}: overall_score arithmetic mismatch")
    for row in PROFESSORS:
        if row["recruiting_status"] not in RECRUITING_STATUSES:
            errors.append(f"{row['full_name']}: invalid recruiting status")
        if row["recruiting_status"] == "Confirmed recruiting" and not row["recruiting_evidence"]:
            errors.append(f"{row['full_name']}: confirmed recruiting without evidence")
        if not all(row[c] for c in ("official_faculty_url", "appointment_status", "recent_work_1", "recent_work_1_url", "recent_work_1_year")):
            errors.append(f"{row['full_name']}: incomplete appointment/recent-work evidence")
        if row["can_supervise_program"].lower() not in {"yes", "true", "verified"}:
            warnings.append(f"{row['full_name']}: supervision not verified")
    if len(contacts) != len(PROGRAMS):
        errors.append("admin contact coverage is not one row per program")
    for row in contacts:
        if not row["official_url"]:
            errors.append(f"{row['institution_name']}: contact row has no official URL")
        if not row["official_email"]:
            warnings.append(f"{row['institution_name']}: administrative email not confidently verified; use official contact page")
    if tuple(PROGRAMS[0].keys()) != PROGRAM_COLUMNS:
        errors.append("program row key order/header differs from PROGRAM_COLUMNS")
    if tuple(PROFESSORS[0].keys()) != PROFESSOR_COLUMNS:
        errors.append("professor row key order/header differs from PROFESSOR_COLUMNS")
    if tuple(sources[0].keys()) != SOURCE_COLUMNS:
        errors.append("source row key order/header differs from SOURCE_COLUMNS")
    if tuple(exclusions[0].keys()) != EXCLUSION_COLUMNS:
        errors.append("exclusion row key order/header differs from EXCLUSION_COLUMNS")
    return {
        "status": "PASS" if not errors else "FAIL",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "data_access_date": ACCESSED,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "programs": len(PROGRAMS),
            "professors": len(PROFESSORS),
            "sources": len(sources),
            "admin_contacts": len(contacts),
            "exclusion_or_downgrade": len(exclusions),
            "retained": sum(r["screening_decision"] == "retained" for r in PROGRAMS),
            "downgraded": sum(r["screening_decision"] == "downgrade" for r in PROGRAMS),
            "excluded": sum(r["screening_decision"] == "excluded" for r in PROGRAMS),
            "cycle_labeled_fall_2027_deadlines": sum(bool(r["fall_2027_deadline"]) for r in PROGRAMS),
            "recruiting_confirmed": sum(r["recruiting_status"] == "Confirmed recruiting" for r in PROFESSORS),
            "recruiting_unknown": sum(r["recruiting_status"] == "Recruiting status unknown" for r in PROFESSORS),
        },
        "checks": {
            "exact_shared_headers": not any("header differs" in e for e in errors),
            "one_program_per_reviewed_institution": len(PROGRAMS) == len({r["institution_id"] for r in PROGRAMS}),
            "professor_coverage": all(professors_by_program[r["program_id"]] >= 1 for r in PROGRAMS),
            "source_coverage": all(sources_by_program[r["program_id"]] >= 3 for r in PROGRAMS),
            "non_retained_reason_and_log": all(r["exclusion_reason"] and exclusions_by_program[r["program_id"]] == 1 for r in PROGRAMS if r["screening_decision"] != "retained"),
            "deadline_cycle_guard": all(not r["fall_2027_deadline"] or "Fall 2027" in r["deadline_cycle_status"] for r in PROGRAMS),
            "recruiting_evidence_guard": all(r["recruiting_status"] != "Confirmed recruiting" or r["recruiting_evidence"] for r in PROFESSORS),
            "score_bounds_and_arithmetic": not any("_score" in e for e in errors),
        },
        "known_limitations": [
            "Faculty depth is intentionally limited to one strongest verified current match per program; single-professor dependency is flagged in every program row.",
            "Blank fall_2027_deadline values are deliberate where the current official page gave a recurring/latest deadline without an explicit Fall 2027 cycle label.",
            "Funding language is transcribed conservatively; assistantship availability and 'typically/most/generally' are not treated as universal guarantees.",
            "No recruiting inference was made from publications, grants, current students, or lab activity. Only RIT has a direct current opening statement, whose start cycle remains to be reconfirmed.",
            "The five lower-priority second-tranche suggestions (Lehigh, UTSA, Colorado School of Mines, University of Houston, Michigan Tech) were deferred rather than represented as reviewed.",
            "No email, calendar, or external-system mutations were performed.",
        ],
    }


def main() -> int:
    sources = make_sources()
    contacts = make_contacts()
    exclusions = make_exclusions()
    validation = validate(sources, contacts, exclusions)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT_DIR / "deep_programs.csv", PROGRAMS, PROGRAM_COLUMNS)
    write_csv(OUTPUT_DIR / "professors.csv", PROFESSORS, PROFESSOR_COLUMNS)
    write_csv(OUTPUT_DIR / "sources.csv", sources, SOURCE_COLUMNS)
    write_csv(OUTPUT_DIR / "admin_contacts.csv", contacts, ADMIN_COLUMNS)
    write_csv(OUTPUT_DIR / "exclusion_or_downgrade.csv", exclusions, EXCLUSION_COLUMNS)
    write_json(OUTPUT_DIR / "validation.json", validation)
    files = [
        OUTPUT_DIR / "deep_programs.csv",
        OUTPUT_DIR / "professors.csv",
        OUTPUT_DIR / "sources.csv",
        OUTPUT_DIR / "admin_contacts.csv",
        OUTPUT_DIR / "exclusion_or_downgrade.csv",
        OUTPUT_DIR / "validation.json",
    ]
    manifest = {
        "region": "us",
        "phase": "finalist_deep_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_access_date": ACCESSED,
        "status": validation["status"],
        "scope": {
            "initial_institutions_reviewed": 20,
            "priority_second_tranche_reviewed": ["Vanderbilt University", "University of Notre Dame", "Washington University in St Louis", "Case Western Reserve University", "Rochester Institute of Technology"],
            "deferred_second_tranche": ["Lehigh University", "University of Texas at San Antonio", "Colorado School of Mines", "University of Houston", "Michigan Technological University"],
        },
        "counts": validation["counts"],
        "files": [{"path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"), "sha256": sha256(path), "bytes": path.stat().st_size} for path in files],
        "source_policy": "Official institution pages for program/admissions/funding/faculty claims; scholarly publisher or university-hosted paper for recent work. Search snippets were discovery only.",
    }
    write_json(MANIFEST_DIR / "run_manifest.json", manifest)
    print(json.dumps({"validation": validation, "manifest": str(MANIFEST_DIR / "run_manifest.json")}, indent=2))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
