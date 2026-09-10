from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PORTFOLIO = ROOT / "outputs" / "20260909-fall2027-audit" / "portfolio.json"
OUT = ROOT / "data" / "processed" / "validation" / "finalists_us"
CHECKED_DATE = "2026-09-09"


PROGRAM_CHECKS = [
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:211440",
        "institution_name": "Carnegie Mellon University",
        "program_id": "us:ipeds:211440:program:phd:software-engineering-phd",
        "program_name": "Software Engineering PhD",
        "primary_claim": "The Software Engineering PhD is an active SCS doctorate. SCS separately states that all PhD students receive full financial support while in good academic standing; adviser matching is by mutual research interest. The offer must still specify exact 2027 health and fee components.",
        "primary_url": "https://se-phd.isri.cmu.edu/",
        "second_url": "https://www.cs.cmu.edu/education/phd/",
        "result": "confirmed",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:179867",
        "institution_name": "Washington University in St Louis",
        "program_id": "us:ipeds:179867:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The current CSE PhD route remains active and McKelvey separately says all full-time PhD students receive tuition and health-fee remission plus monthly living support; most offers are guaranteed with progress. The December 1 deadline is not yet Fall-2027-labeled.",
        "primary_url": "https://admin.aprc.wustl.edu/academics/graduate-admissions/index.html",
        "second_url": "https://engineering.washu.edu/academics/graduate-admissions/tuition-financial-assistance/funding_your_grad_degree.html",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:221999",
        "institution_name": "Vanderbilt University",
        "program_id": "us:ipeds:221999:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The direct-from-bachelor CS PhD and doctoral assistance are confirmed. The Fall 2027 engineering page calls December 15, 2026 the recommended submission date and January 8, 2027 the final deadline, so storing December 15 as the deadline is materially ambiguous.",
        "primary_url": "https://computing.vanderbilt.edu/csphd/",
        "second_url": "https://engineering.vanderbilt.edu/graduate-admissions/",
        "result": "conflict",
        "correction_needed": "Use 2027-01-08 as the final Fall 2027 deadline, or add a distinct recommended-deadline field for 2026-12-15.",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:170976",
        "institution_name": "University of Michigan-Ann Arbor",
        "program_id": "us:ipeds:170976:program:phd:computer-science-and-engineering-phd",
        "program_name": "Computer Science and Engineering PhD",
        "primary_claim": "The CSE PhD accepts bachelor-level entrants and international students. A separate current College of Engineering PhD page independently confirms that engineering PhD applicants may enter with a bachelor's and that admitted PhD students are fully funded; the CSE-specific five-year package page was not directly retrievable during this validation pass.",
        "primary_url": "https://cse.engin.umich.edu/academics/graduate/admissions/",
        "second_url": "https://www.engin.umich.edu/majors-programs/graduate-professional/phd/",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:166629",
        "institution_name": "University of Massachusetts-Amherst",
        "program_id": "us:ipeds:166629:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The CS PhD route and bachelor-level application are current. The separate policy page limits the five-year guarantee to students whose most recent admission letter contains it and conditions support on adequate progress and available funds; the cycle-specific deadline remains unpublished.",
        "primary_url": "https://www.cics.umass.edu/academics/phd-computer-science/how-apply-phd-program",
        "second_url": "https://www.cics.umass.edu/academics/academic-policies/graduate-programs-policies/msphd-degree-requirements/other-msphd-program-information",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:233921",
        "institution_name": "Virginia Polytechnic Institute and State University",
        "program_id": "us:ipeds:233921:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The bachelor-entry PhD and international route are current. The funding page says that beginning with the Fall 2026 admission cycle, 100% of admitted PhD students receive a conditional five-year offer excluding summers; some fees remain the student's responsibility.",
        "primary_url": "https://website.cs.vt.edu/academic/graduate/future-grads/doctorate.html",
        "second_url": "https://students.cs.vt.edu/Graduate/Funding.html",
        "result": "qualified",
        "correction_needed": "Revise the portfolio risk wording: the funding policy is effective beginning Fall 2026, not stated as limited only to the Fall 2026 cohort.",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:167358",
        "institution_name": "Northeastern University",
        "program_id": "us:ipeds:167358:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "Khoury's current application page permits entry after a four-year undergraduate degree and states a five-year support package. The independent 2026-27 catalog confirms an active research PhD with 48 credits beyond the BS/BA and faculty-advised dissertation supervision; the Fall 2027 deadline is still unlabeled.",
        "primary_url": "https://www.khoury.northeastern.edu/apply/phd-apply/",
        "second_url": "https://catalog.northeastern.edu/graduate/computer-information-science/computer-science/computer-science-phd/",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "ca:dli:O19305471522",
        "institution_name": "University of Waterloo",
        "program_id": "ca:dli:O19305471522:program:thesis-or-research-master-s:mmath-in-computer-science-thesis",
        "program_name": "MMath in Computer Science (thesis)",
        "primary_claim": "The thesis MMath accepts a relevant honours bachelor's and international applicants. Cheriton's separate funding page confirms packages for all full-time MMath students within time limits and publishes an international package, but the December 1 rule is recurring rather than explicitly Fall-2027-labeled.",
        "primary_url": "https://uwaterloo.ca/future-graduate-students/programs/by-faculty/math/computer-science-master-math-mmath",
        "second_url": "https://uwaterloo.ca/computer-science/current-graduate-students/funding-and-awards",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:231624",
        "institution_name": "William & Mary",
        "program_id": "us:ipeds:231624:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The department admissions page confirms an active PhD, international application requirements, and stipend plus full tuition for admitted full-time PhD/MS-PhD students. The 2026-27 catalog independently confirms the PhD and bachelor-level preparation, but not duration, summer, health, or Fall 2027 cycle terms.",
        "primary_url": "https://cdsp.wm.edu/admissions/graduate/computer-science/",
        "second_url": "https://catalog.wm.edu/graduate/school-computing-data-sciences-physics/departments/csci/",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:152080",
        "institution_name": "University of Notre Dame",
        "program_id": "us:ipeds:152080:program:phd:computer-science-and-engineering-phd",
        "program_name": "Computer Science and Engineering PhD",
        "primary_claim": "The program expressly accepts BS holders and international applicants and says PhD students are generally supported with 12-month stipends, tuition, and health coverage. The Graduate School reports 94% receive multi-year stipend support, so 'generally' must not be converted into a universal guarantee; December 15 remains recurring, not Fall-2027-labeled.",
        "primary_url": "https://engineering.nd.edu/departments-programs/graduate-programs/phd-in-computer-science-and-engineering/",
        "second_url": "https://graduateschool.nd.edu/funding/",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:153603",
        "institution_name": "Iowa State University",
        "program_id": "us:ipeds:153603:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The PhD accepts bachelor-level and international applicants and has a Fall 2027 deadline. The separate FAQ confirms two years of typical TA support, with later RA support typically tied to a major professor rather than guaranteed; the portfolio already reflects that limitation.",
        "primary_url": "https://www.cs.iastate.edu/graduate-studies/phd-application-requirements",
        "second_url": "https://www.cs.iastate.edu/graduate-studies/faq-prospective-graduate-students",
        "result": "confirmed",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:228778",
        "institution_name": "The University of Texas at Austin",
        "program_id": "us:ipeds:228778:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The research PhD is available directly after a bachelor's and to international applicants. The cost-and-aid page independently says most, not all, PhD students receive five years of stipend, health, and tuition support, contingent on performance and available funds; the Fall 2027 deadline remains unlabeled.",
        "primary_url": "https://www.cs.utexas.edu/graduate/degrees-and-programs",
        "second_url": "https://www.cs.utexas.edu/graduate/cost-and-aid",
        "result": "confirmed",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "ca:dli:O19425660421",
        "institution_name": "University of Saskatchewan",
        "program_id": "ca:dli:O19425660421:program:thesis-or-research-master-s:msc-in-computer-science-thesis",
        "program_name": "MSc in Computer Science (thesis)",
        "primary_claim": "The thesis MSc accepts four-year bachelor's holders and international applicants and is normally funded for 20 months. The department application page confirms these terms but still labels its displayed December 15 deadline for Fall 2026, not Fall 2027.",
        "primary_url": "https://grad.usask.ca/programs/computer-science.php",
        "second_url": "https://www.cs.usask.ca/students/graduate/graduate-programs/applications-for-admission.php",
        "result": "conflict",
        "correction_needed": "Treat the Fall 2027 deadline as TBD until an official page labels the new cycle; do not carry the Fall 2026 date forward as a current-cycle deadline.",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "ca:dli:O19332746152",
        "institution_name": "University of Toronto",
        "program_id": "ca:dli:O19332746152:program:direct-entry-phd:phd-in-computer-science-phd-u",
        "program_name": "PhD in Computer Science (PhD U)",
        "primary_claim": "The FAQ directs international applicants with an honours-bachelor equivalent to PhD-U. The funding page independently guarantees 60 months for PhD-U subject to satisfactory progress and covers tuition plus a living package; the Fall 2027 deadline is correctly left TBD.",
        "primary_url": "https://web.cs.toronto.edu/graduate/faq",
        "second_url": "https://web.cs.toronto.edu/graduate/funding-tuition-awards",
        "result": "confirmed",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "ca:dli:O19330231062",
        "institution_name": "University of British Columbia",
        "program_id": "ca:dli:O19330231062:program:thesis-or-research-master-s:msc-in-computer-science-research",
        "program_name": "MSc in Computer Science (research)",
        "primary_claim": "The research MSc accepts qualified bachelor's and international applicants. The 2026-27 support page independently guarantees the standard minimum for two years and shows the lower year-two international net; the departmental December 15 date still conflicts with central intake configuration.",
        "primary_url": "https://www.cs.ubc.ca/students/grad/admissions",
        "second_url": "https://www.cs.ubc.ca/grads/awards-support-current-grad-students/financial-assistantship/stipends-support-details-2026-2027",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:195003",
        "institution_name": "Rochester Institute of Technology",
        "program_id": "us:ipeds:195003:program:phd:computing-and-information-sciences-phd",
        "program_name": "Computing and Information Sciences PhD",
        "primary_claim": "The active bachelor-entry, international-eligible doctorate is confirmed, and the department reports full-time students as fully supported while the degree page says support is typical. The degree page expressly says GRE required, contradicting the deep-review GRE field; Fall 2027 admissions/funded-studentship details are not yet open.",
        "primary_url": "https://www.rit.edu/study/computing-and-information-sciences-phd",
        "second_url": "https://www.rit.edu/computing/phd-computing-and-information-sciences",
        "result": "conflict",
        "correction_needed": "Change GRE policy to Required. Preserve funding as qualified until offer duration, health, fees, and summer are explicit; keep the Fall 2027 deadline TBD.",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "ca:dli:O18886830282",
        "institution_name": "University of Calgary",
        "program_id": "ca:dli:O18886830282:program:thesis-or-research-master-s:msc-in-computer-science-thesis",
        "program_name": "MSc in Computer Science (thesis)",
        "primary_claim": "The thesis MSc accepts a four-year degree and international applicants, requires a supervisor for admission, and has a two-year department funding minimum. The central program listing confirms the MSc, requirements, and recurring January 15/March 1 deadlines, but does not label them for Fall 2027.",
        "primary_url": "https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs/masters-thesis-based",
        "second_url": "https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs/computer-science-msc-thesis",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "current_core",
        "institution_id": "us:ipeds:110653",
        "institution_name": "University of California-Irvine",
        "program_id": "us:ipeds:110653:program:phd:software-engineering-phd",
        "program_name": "Software Engineering PhD",
        "primary_claim": "The Software Engineering PhD and bachelor/international eligibility are current. The ICS FAQ gives a recurring December 15 deadline and only says ICS strives to fund all PhD admits; it does not label December 15 for Fall 2027 or make an unconditional funding guarantee.",
        "primary_url": "https://informatics.ics.uci.edu/phd-software-engineering/",
        "second_url": "https://ics.uci.edu/admissions-information-and-computer-science/graduate-admissions/graduate-research-admissions-faq/",
        "result": "conflict",
        "correction_needed": "Clear or qualify 2026-12-15 as a recurring, not cycle-labeled, deadline until an official Fall 2027 page appears; retain aspirational funding language.",
    },
    {
        "portfolio_tier": "corrected_to_reserve",
        "institution_id": "us:ipeds:163286",
        "institution_name": "University of Maryland-College Park",
        "program_id": "us:ipeds:163286:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The active PhD permits direct application without a master's and is open to international applicants, with a Fall 2027 deadline. The admissions FAQ says PhD students are funded through TA/RA arrangements but explicitly says the admission offer carries no funding guarantee; reserve treatment is appropriate.",
        "primary_url": "https://www.cs.umd.edu/grad/apply",
        "second_url": "https://www.cs.umd.edu/grad/admissions-faq",
        "result": "qualified",
        "correction_needed": "",
    },
]


EXCLUSION_CHECKS = [
    {
        "portfolio_tier": "deep_review_exclusion_sample",
        "institution_id": "us:ipeds:145637",
        "institution_name": "University of Illinois Urbana-Champaign",
        "program_id": "us:ipeds:145637:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The exclusion called 3.40 a published minimum above the applicant's 3.35 cumulative GPA. The current Siebel comparison table labels 3.40 as recommended, while the Graduate College minimum is 3.0 over the last two undergraduate years; the hard-screen exclusion is unsupported.",
        "primary_url": "https://catalog.illinois.edu/graduate/engineering/computer-science-phd/",
        "second_url": "https://siebelschool.illinois.edu/admissions/graduate/degree-program-options",
        "result": "conflict",
        "correction_needed": "Remove hard-GPA exclusion and reconsider as a reach/reserve candidate using the applicant's recent-two-year GPA; do not describe 3.40 as a minimum.",
    },
    {
        "portfolio_tier": "deep_review_exclusion_sample",
        "institution_id": "us:ipeds:232186",
        "institution_name": "George Mason University",
        "program_id": "us:ipeds:232186:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The program is active but no current department-wide multi-year funding guarantee was found. A current official faculty-hosted recruiting page advertises stipend, tuition, and health coverage for a specific security lab and gives recurring dates, which supports targeted outreach but not a program-wide guarantee.",
        "primary_url": "https://cs.gmu.edu/academics/graduate-programs",
        "second_url": "https://people.cs.gmu.edu/~qzeng2/recruiting_students.html",
        "result": "qualified",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "deep_review_exclusion_sample",
        "institution_id": "us:ipeds:199193",
        "institution_name": "North Carolina State University at Raleigh",
        "program_id": "us:ipeds:199193:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The downgrade said no multi-year department-wide guarantee was verified and emphasized advisor-dependent RA funding. The current financial-aid page now promises a comprehensive four-year package to every fall PhD admit who requests aid, including tuition, individual health insurance, and stipend, though fees and summers remain outside the package.",
        "primary_url": "https://csc.ncsu.edu/academics/graduate/phd/",
        "second_url": "https://csc.ncsu.edu/academics/graduate/financial-aid-and-cost/",
        "result": "conflict",
        "correction_needed": "Re-score funding and reconsider for reserve/core comparison; retain explicit risks for student fees, summer support, year five, and transition to advisor-funded RA.",
    },
    {
        "portfolio_tier": "deep_review_exclusion_sample",
        "institution_id": "us:ipeds:243780",
        "institution_name": "Purdue University-Main Campus",
        "program_id": "us:ipeds:243780:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The downgrade rests on possible admission without support. Purdue's separate financial-support page independently says admitted applicants are considered automatically but admission without support is possible, so the hard funding concern remains valid.",
        "primary_url": "https://www.cs.purdue.edu/graduate/admission/steps.html",
        "second_url": "https://www.cs.purdue.edu/graduate/financial_support/finding-support.html",
        "result": "confirmed",
        "correction_needed": "",
    },
    {
        "portfolio_tier": "deep_review_exclusion_sample",
        "institution_id": "us:ipeds:228787",
        "institution_name": "The University of Texas at Dallas",
        "program_id": "us:ipeds:228787:program:phd:computer-science-phd",
        "program_name": "Computer Science PhD",
        "primary_claim": "The PhD accepts related bachelor's entrants but publishes a 3.5 GPA expectation for the last 60 hours. The FAQ says most full-time PhD students are funded subject to performance, eligibility, and available funds, with advisor responsibility after matching; both applicant GPA calculation and guarantee remain unresolved.",
        "primary_url": "https://catalog.utdallas.edu/2026/graduate/programs/ecs/computer-science",
        "second_url": "https://cs.utdallas.edu/education/graduate-studies/phd-faqs/",
        "result": "confirmed",
        "correction_needed": "",
    },
]


FACULTY_CHECKS = {
    "us:ipeds:211440:program:phd:software-engineering-phd": (
        "Claire Le Goues",
        "https://s3d.cmu.edu/people/core-faculty/legoues-claire.html",
        "confirmed",
        "Current core-faculty appointment supports supervision eligibility; no Fall 2027 recruiting claim was found.",
    ),
    "us:ipeds:179867:program:phd:computer-science-phd": (
        "Umar Iqbal",
        "https://engineering.washu.edu/faculty/Umar-Iqbal.html",
        "confirmed",
        "Current CSE assistant-professor appointment and 2026 research are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:221999:program:phd:computer-science-phd": (
        "Kevin Leach",
        "https://computing.vanderbilt.edu/bio/kevin-leach/",
        "confirmed",
        "Current CS assistant-professor appointment and software-security research are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:170976:program:phd:computer-science-and-engineering-phd": (
        "Westley Weimer",
        "https://eecs.engin.umich.edu/people/weimer-westley/",
        "qualified",
        "Current CSE professor listing and recent program-repair work were indexed, but the profile returned HTTP 403 to direct retrieval; recruiting remains unknown.",
    ),
    "us:ipeds:166629:program:phd:computer-science-phd": (
        "Yuriy Brun",
        "https://www.cics.umass.edu/about/directory/yuriy-brun",
        "confirmed",
        "Current CICS professor appointment and recent software-engineering work are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:233921:program:phd:computer-science-phd": (
        "Na Meng",
        "https://website.cs.vt.edu/people/faculty/na-ming.html",
        "confirmed",
        "Current CS associate-professor appointment and software-engineering/programming-languages areas are verified; recruiting remains unknown.",
    ),
    "us:ipeds:167358:program:phd:computer-science-phd": (
        "Jonathan Bell",
        "https://www.khoury.northeastern.edu/people/jonathan-bell/",
        "confirmed",
        "Current Khoury associate-professor appointment supports supervision eligibility; no Fall 2027 recruiting claim was found.",
    ),
    "ca:dli:O19305471522:program:thesis-or-research-master-s:mmath-in-computer-science-thesis": (
        "Shane McIntosh",
        "https://uwaterloo.ca/computer-science/about/people/s4mcinto",
        "qualified",
        "Current Cheriton associate-professor appointment and software-engineering work are verified; Fall 2027 supervision capacity is unknown.",
    ),
    "us:ipeds:231624:program:phd:computer-science-phd": (
        "Denys Poshyvanyk",
        "https://www.cs.wm.edu/~dposhyvanyk/index.html",
        "confirmed",
        "Current department-chair/professor role and software-engineering work are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:152080:program:phd:computer-science-and-engineering-phd": (
        "Joanna Cecilia da Silva Santos",
        "https://cse.nd.edu/faculty/joanna-cecilia-da-silva-santos/",
        "confirmed",
        "Current CSE assistant-professor appointment and active secure-software research are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:153603:program:phd:computer-science-phd": (
        "Myra Cohen",
        "https://www.cs.iastate.edu/people/myra-cohen",
        "confirmed",
        "Current professor/chair appointment and configurable-software testing work are verified; recruiting status remains unknown.",
    ),
    "us:ipeds:228778:program:phd:computer-science-phd": (
        "Isil Dillig",
        "https://www.cs.utexas.edu/people/faculty-researchers/isil-dillig",
        "confirmed",
        "Current professor/department-chair appointment and formal software-verification work are verified; recruiting remains unknown.",
    ),
    "ca:dli:O19425660421:program:thesis-or-research-master-s:msc-in-computer-science-thesis": (
        "Chanchal K. Roy",
        "https://www.cs.usask.ca/people/faculty%20profiles/chanchal-roy.php",
        "qualified",
        "Current professor appointment and a general lab call for MSc/PhD students are verified; Fall 2027 capacity and offer terms remain unconfirmed.",
    ),
    "ca:dli:O19332746152:program:direct-entry-phd:phd-in-computer-science-phd-u": (
        "Marsha Chechik",
        "https://web.cs.toronto.edu/people/faculty-directory",
        "qualified",
        "Current faculty-directory presence and recent reconciliation work are verified; individual Fall 2027 supervision capacity is unknown.",
    ),
    "ca:dli:O19330231062:program:thesis-or-research-master-s:msc-in-computer-science-research": (
        "Reid Holmes",
        "https://www.cs.ubc.ca/people/reid-holmes",
        "qualified",
        "Current CS professor appointment and recent software-engineering work are verified; Fall 2027 supervision capacity is unknown.",
    ),
    "us:ipeds:195003:program:phd:computing-and-information-sciences-phd": (
        "Yinxi Liu",
        "https://www.rit.edu/computing/directory/yxlics-yinxi-liu",
        "confirmed",
        "Current assistant-professor appointment and an official PhD research opening are verified; the opening's Fall 2027 start must still be reconfirmed.",
    ),
    "ca:dli:O18886830282:program:thesis-or-research-master-s:msc-in-computer-science-thesis": (
        "Mahmoud Alfadel",
        "https://profiles.ucalgary.ca/mahmoud-alfadel",
        "qualified",
        "Current assistant-professor profile and software-engineering work are verified; Fall 2027 supervision capacity is unknown.",
    ),
    "us:ipeds:110653:program:phd:software-engineering-phd": (
        "Joshua Garcia",
        "https://jgarcia.ics.uci.edu/",
        "confirmed",
        "Current Informatics associate-professor appointment and software-testing/vulnerability work are verified; recruiting remains unknown.",
    ),
    "us:ipeds:163286:program:phd:computer-science-phd": (
        "David Van Horn",
        "https://www.cs.umd.edu/people/dvanhorn",
        "confirmed",
        "Current CS/UMIACS associate-professor appointment and programming-languages/software-engineering fit are verified; recruiting remains unknown.",
    ),
}


FIELDS = [
    "portfolio_tier",
    "institution_id",
    "institution_name",
    "program_id",
    "program_name",
    "faculty_name",
    "faculty_url",
    "faculty_result",
    "faculty_note",
    "primary_claim",
    "primary_url",
    "second_url",
    "result",
    "correction_needed",
    "checked_date",
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            faculty = FACULTY_CHECKS.get(row["program_id"])
            faculty_fields = {
                "faculty_name": faculty[0] if faculty else "",
                "faculty_url": faculty[1] if faculty else "",
                "faculty_result": faculty[2] if faculty else "",
                "faculty_note": faculty[3] if faculty else "",
            }
            writer.writerow({**row, **faculty_fields, "checked_date": CHECKED_DATE})


def main() -> None:
    portfolio_bytes = PORTFOLIO.read_bytes()
    portfolio = json.loads(portfolio_bytes)
    core_ids = {row["program_id"] for row in portfolio["core"]}
    expected_core_ids = {
        row["program_id"] for row in PROGRAM_CHECKS if row["portfolio_tier"] == "current_core"
    }
    assert len(portfolio["core"]) == 18, "Current portfolio core count changed; re-audit scope."
    assert core_ids == expected_core_ids, "Current core membership differs from validation rows."
    maryland = next(
        row for row in PROGRAM_CHECKS if row["portfolio_tier"] == "corrected_to_reserve"
    )
    assert any(row["program_id"] == maryland["program_id"] for row in portfolio["reserve"])
    assert len(PROGRAM_CHECKS) == 19
    assert set(FACULTY_CHECKS) == {row["program_id"] for row in PROGRAM_CHECKS}
    assert len(EXCLUSION_CHECKS) == 5

    write_csv(OUT / "program_checks.csv", PROGRAM_CHECKS)
    write_csv(OUT / "exclusion_sample_checks.csv", EXCLUSION_CHECKS)

    program_counts = Counter(row["result"] for row in PROGRAM_CHECKS)
    exclusion_counts = Counter(row["result"] for row in EXCLUSION_CHECKS)
    corrections = [
        {
            "institution_name": row["institution_name"],
            "program_id": row["program_id"],
            "portfolio_tier": row["portfolio_tier"],
            "result": row["result"],
            "correction": row["correction_needed"],
        }
        for row in PROGRAM_CHECKS + EXCLUSION_CHECKS
        if row["correction_needed"]
    ]
    payload = {
        "checked_date": CHECKED_DATE,
        "portfolio_path": str(PORTFOLIO.relative_to(ROOT)).replace("\\", "/"),
        "portfolio_sha256": hashlib.sha256(portfolio_bytes).hexdigest(),
        "scope": {
            "current_core_programs": 18,
            "corrected_former_core_programs": 1,
            "total_program_rows": 19,
            "sampled_us_exclusions": 5,
        },
        "program_results": dict(sorted(program_counts.items())),
        "exclusion_sample_results": dict(sorted(exclusion_counts.items())),
        "pending_correction_count": len(corrections),
        "pending_corrections": corrections,
        "resolved_correction_count": 1,
        "resolved_corrections": [
            {
                "institution_name": "University of Maryland-College Park",
                "program_id": "us:ipeds:163286:program:phd:computer-science-phd",
                "resolution": "Current portfolio already moved Maryland from core to reserve and reduced funding strength after the official FAQ was found to disclaim an admission-offer funding guarantee.",
            }
        ],
        "method": "Claims were checked against a distinct current official university, school, department, catalog, funding, or official faculty-hosted page. Search snippets were used only to locate pages; result classifications use the opened official pages. Recruiting was not inferred from an active lab or publications.",
        "limitations": [
            "A qualified result means the route remains plausible but at least one hard-gate term is conditional, recurring rather than cycle-labeled, offer-specific, or not independently quantified.",
            "Northeastern's dedicated funding subpage returned HTTP 403 to the audit client; the independent 2026-27 official catalog was used to confirm the active bachelor-entry PhD and supervision structure, while the funding wording remains sourced to the official application page.",
            "Michigan CSE's FAQ and faculty profile returned HTTP 403 to direct retrieval. A distinct current College of Engineering PhD page confirmed bachelor entry and full funding; the faculty check is therefore qualified rather than treated as fresh recruiting evidence.",
            "No row interprets a current faculty appointment as evidence that the faculty member is recruiting for Fall 2027.",
        ],
    }
    (OUT / "validation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
