from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = ROOT / "evidence" / "validation" / "cross_region_ca"
CHECK_DATE = "2026-09-09"
SEED = "cross-region-ca-v1"

US_EXCLUSIONS = ROOT / "data" / "processed" / "regions" / "us" / "exclusion_log.csv"
EUROPE_EXCLUSIONS = ROOT / "data" / "processed" / "regions" / "europe" / "exclusion_log.csv"
EUROPE_PROGRAMS = ROOT / "data" / "processed" / "deep_review" / "europe" / "deep_programs.csv"
EUROPE_PROFESSORS = ROOT / "data" / "processed" / "deep_review" / "europe" / "professors.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selection_hash(institution_id: str) -> str:
    return hashlib.sha256(f"{SEED}|{institution_id}".encode("utf-8")).hexdigest()


EXCLUSION_EVIDENCE = {
    "us:ipeds:157809": {
        "official_url": "https://www.thomasmore.edu/program/master-of-science-in-information-technology-management/",
        "finding": "The current MS in Information Technology Management is a 30-credit professional curriculum ending in MIS 690 capstone; the official curriculum does not present a thesis or dissertation research route.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion for this research-degree audit; optionally add professional IT programs to a separate coursework-only inventory.",
        "confidence": "high",
    },
    "us:ipeds:385619": {
        "official_url": "https://www.evergladesuniversity.edu/",
        "finding": "The official graduate-program list covers aviation, business, construction, hospitality, leadership, public-health administration, sustainability, and coastal/marine management; no computing research graduate degree is listed.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion; recheck only if Everglades publishes a new computing research degree after this audit date.",
        "confidence": "high",
    },
    "us:ipeds:496283": {
        "official_url": "https://www.provocollege.edu/location/eagle-gate/",
        "finding": "The official Provo College location page maps Idaho Falls offerings to the Eagle Gate College brand and healthcare/nursing career programs; no relevant graduate computing research route is shown.",
        "false_negative": "no",
        "corrective_action": "Retain the program exclusion, but normalize the IPEDS campus-to-current-brand crosswalk so this campus is not treated as an independent current computing provider.",
        "confidence": "high",
    },
    "us:ipeds:242705": {
        "official_url": "https://www.inter.edu/oferta-academica/maestrias/ | https://www.inter.edu/boletien-informativo-2026-2027-bayamon/",
        "finding": "Inter American's official master's list places Computer Science concentrations at Guayama and Barranquitas, not Bayamón; the Bayamón 2026-27 bulletin does not establish a Bayamón CS research graduate route.",
        "false_negative": "no",
        "corrective_action": "Retain this campus exclusion and preserve campus-specific program attribution; do not merge programs across the Inter American system.",
        "confidence": "high",
    },
    "us:ipeds:164270": {
        "official_url": "https://www.mcdaniel.edu/academics/graduate-professional-studies/data-analytics-ms-stem-designated-day-1-cpt",
        "finding": "McDaniel's official Data Analytics MS is a 30-36 credit online/hybrid professional program built around coursework and experiential preparation; no thesis research route is identified.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion under the research-degree rule; classify the MS separately if professional coursework programs are later inventoried.",
        "confidence": "high",
    },
    "us:ipeds:194116": {
        "official_url": "https://www.nysid.edu/master-of-fine-arts-in-interior-design",
        "finding": "NYSID's official graduate offering is in interior design and related professional design fields; even the MFA thesis is a design degree rather than a computing or software-engineering research degree.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion; no relevant computing research program was found.",
        "confidence": "high",
    },
    "us:ipeds:151801": {
        "official_url": "https://catalog.indwes.edu/programs/APS.MSCIS.AI",
        "finding": "The current MS in Computer Information Systems with AI is explicitly designed for practicing professionals and workplace application; the official plan and graduation rules do not show a research thesis or dissertation route.",
        "false_negative": "no",
        "corrective_action": "Retain the research-degree exclusion, while noting that a program-name/CIP-only screen should separately identify it as coursework-only rather than as no computing offering.",
        "confidence": "high",
    },
    "ror:04j47fz63": {
        "official_name": "Haute École de Santé Vaud",
        "official_url": "https://hesav.ch/formation/admission/",
        "finding": "HESAV's current official admissions page describes five health bachelor programs and a preparatory health year; no computer-science graduate research degree is offered by this institution page.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion; no relevant computing research program was found.",
        "confidence": "high",
    },
    "ror:039ce0m20": {
        "official_url": "https://ece.hmu.gr/en/doctoral-ph-d-studies-program/ | https://hmu.gr/en/postgraduate-studies/postgraduate-programs/",
        "finding": "HMU Electrical and Computer Engineering officially offers an original-research PhD, and HMU also lists an Informatics Engineering MSc with explicit research orientation. The PhD normally requires a relevant master's/integrated master's but permits exceptional non-master admission by reasoned department decision.",
        "false_negative": "yes",
        "corrective_action": "Add the ECE PhD to mechanical program screening and separately assess the Informatics Engineering MSc thesis/research structure; deep-review language, funding, deadline, and exceptional bachelor-entry rules before portfolio use.",
        "confidence": "high",
    },
    "ror:04bqkh239": {
        "official_url": "https://zsem.hr/en/applications/",
        "finding": "ZSEM's current official application page lists undergraduate economics/management and business mathematics/economics plus a graduate MBA; it does not list a computing research master's or doctorate.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion; do not treat short-course AI/data content or the business doctorate as a computing research program.",
        "confidence": "high",
    },
    "ror:0362ttz08": {
        "official_name": "Center for Economic Research and Graduate Education – Economics Institute",
        "official_url": "https://ei.cerge-ei.cz/study/",
        "finding": "CERGE-EI's official study page lists economics degrees, including the PhD in Economics and Master in Economic Research; no relevant computing research degree is listed.",
        "false_negative": "no",
        "corrective_action": "Retain the exclusion; economics programs with quantitative methods do not satisfy the configured computing/software research scope.",
        "confidence": "high",
    },
    "ror:053qcv951": {
        "official_url": "https://www.eadtu.eu/index.php/about/general",
        "finding": "EADTU describes itself as an institutional university network/association representing member universities, not as a degree-awarding university.",
        "false_negative": "no",
        "corrective_action": "Exclude EADTU earlier at institution-universe normalization as a non-degree-awarding association; retain its member universities as separate entities.",
        "confidence": "high",
    },
    "ror:00tf2g326": {
        "official_url": "https://www.bolton-sfc.ac.uk/downloads/prospectus/b6_prospectus_2026_online_v_small.pdf",
        "finding": "The official 2026 prospectus is for sixth-form/A-level study and does not offer graduate degrees.",
        "false_negative": "no",
        "corrective_action": "Retain the institution-universe exclusion as a secondary-school entity.",
        "confidence": "high",
    },
}


FINALIST_EVIDENCE = {
    "ror:013meh722:program:phd:phd-in-computer-science": {
        "degree_entry_url": "https://www.cst.cam.ac.uk/admissions/phd",
        "degree_entry_finding": "The Computer Science PhD page permits applicants meeting the first-class/equivalent undergraduate standard; a master's is desirable for many applicants but not a universal prerequisite.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.postgraduate.study.cam.ac.uk/funding",
        "funding_finding": "Cambridge funding is award- and competition-specific; admission does not establish a full overseas-fee-and-stipend package for this applicant.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.cst.cam.ac.uk/people/arb33",
        "faculty_appointment_finding": "The current department profile lists Alastair Beresford as Professor of Computer Security and Head of Department.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; keep funding unconfirmed and recruiting status unknown until an official award or supervisor response exists.",
    },
    "ror:02jx3x895:program:integrated-or-structured-doctorate:computer-science-mphil-phd": {
        "degree_entry_url": "https://www.ucl.ac.uk/prospective-students/graduate/research-degrees/computer-science-4-year-programme-mphil-phd",
        "degree_entry_finding": "UCL's four-year Computer Science MPhil/PhD accepts a relevant UK upper-second bachelor's/equivalent as an entry route; a master's is an alternative, not universal.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.ucl.ac.uk/prospective-students/graduate/research-degrees/computer-science-4-year-programme-mphil-phd",
        "funding_finding": "The program page separates fees from competitive scholarships and does not promise a universal full international package.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.ucl.ac.uk/engineering/computer-science/research/research-groups-and-centres/software-systems-engineering-group/people",
        "faculty_appointment_finding": "The current Software Systems Engineering group lists Prof Earl Barr among academic staff.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain Investigate Further until a full overseas-fee studentship is verified.",
    },
    "ror:041kmwe10:program:phd:phd-in-computing": {
        "degree_entry_url": "https://www.imperial.ac.uk/computing/prospective-students/phd/",
        "degree_entry_finding": "Imperial Computing says applicants are expected to have a first-class degree and distinction-level master's; applicants with only a bachelor's will not normally be considered and are directed to an MSc first.",
        "degree_entry_result": "material_discrepancy",
        "funding_url": "https://www.imperial.ac.uk/computing/prospective-students/phd/",
        "funding_finding": "The department states that it offers up to 30 fully funded studentships annually to home and overseas applicants, but selection remains competitive.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://profiles.imperial.ac.uk/c.cadar",
        "faculty_appointment_finding": "Imperial's current profile lists Cristian Cadar as Professor of Software Reliability in Computing.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "material_discrepancy",
        "corrective_action": "Change direct_from_bachelors_eligible from yes to no/not normally; downgrade or exclude this immediate route unless Imperial confirms an exceptional bachelor-only case in writing.",
    },
    "ror:05a28rw58:program:direct-entry-phd:direct-doctorate-in-computer-science": {
        "degree_entry_url": "https://inf.ethz.ch/doctorate/direct-doctorate-computer-science.html",
        "degree_entry_finding": "ETH's Direct Doctorate is explicitly for exceptionally qualified applicants entering from a bachelor's degree.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://inf.ethz.ch/doctorate/direct-doctorate-computer-science.html",
        "funding_finding": "The official route promises financial support and tuition waivers during the first two years, followed by a competitive doctoral salary intended to cover living expenses.",
        "funding_result": "material_discrepancy",
        "faculty_appointment_url": "https://inf.ethz.ch/people/person-detail.mvechev.html",
        "faculty_appointment_finding": "ETH's department directory lists Martin Vechev as Full Professor of Computer Science.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "material_discrepancy",
        "corrective_action": "Replace the vague program funding model with guaranteed conditional-on-admission support/waiver terms for the direct route; still keep applicant award and supervisor recruiting status distinct and unconfirmed.",
    },
    "ror:05a28rw58:program:phd-requiring-a-master-s:doctoral-study-programme-in-computer-science": {
        "degree_entry_url": "https://inf.ethz.ch/doctorate.html",
        "degree_entry_finding": "Regular ETH doctoral admission requires a university master's degree and a professor willing to supervise.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://inf.ethz.ch/doctorate.html",
        "funding_finding": "Most ETH doctoral candidates are employed as scientific assistants, but the regular route depends on a specific supervisor/position rather than a universal admission package.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://inf.ethz.ch/people/person-detail.mvechev.html",
        "faculty_appointment_finding": "ETH's department directory lists Martin Vechev as Full Professor of Computer Science.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain exclusion for a bachelor-only applicant and do not transfer the Direct Doctorate funding terms to this route.",
    },
    "ror:01jdpyv68:program:integrated-or-structured-doctorate:saarbr-cken-graduate-school-of-computer-science": {
        "degree_entry_url": "https://www.uni-saarland.de/en/future/computerscience.html",
        "degree_entry_finding": "Saarland's official computer-science graduate-school description allows talented bachelor's graduates to begin doctoral preparation directly.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.uni-saarland.de/en/future/computerscience.html",
        "funding_finding": "The published EUR 800 monthly direct-entry scholarship is precise but does not establish full international living-cost coverage.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://cispa.de/en/people/c01aze",
        "faculty_appointment_finding": "CISPA's current profile identifies Andreas Zeller as faculty/professor in the Saarland computer-science research ecosystem.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; keep as Investigate Further and require written full-cost funding details before application.",
    },
    "ror:05f950310:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science": {
        "degree_entry_url": "https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral",
        "degree_entry_finding": "KU Leuven requires a relevant Flemish master's/equivalent or successful predoctoral examination; a standard bachelor-only route is not established.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral",
        "funding_finding": "Doctoral admission is supervisor-initiated and financing is attached to a position or other specific source, not universally guaranteed by the study right.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://distrinet.cs.kuleuven.be/people/WouterJoosen",
        "faculty_appointment_finding": "The current DistriNet profile lists Wouter Joosen as full professor and research-group head.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain exclusion for lack of the required master's and lack of a specific funded position.",
    },
    "ror:020hwjq30:program:phd-requiring-a-master-s:doctoral-programme-in-science-computer-science": {
        "degree_entry_url": "https://www.aalto.fi/en/study-options/aalto-doctoral-programme-in-science-0",
        "degree_entry_finding": "Aalto's Doctoral Programme in Science requires a relevant master's or equivalent degree and a research-thesis background.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.aalto.fi/en/doctoral-education/funding-your-doctoral-studies",
        "funding_finding": "Aalto states that admission does not itself guarantee funding; employment contracts and grants must be secured separately.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.aalto.fi/en/people/fabian-fagerholm | https://www.aalto.fi/en/department-of-computer-science/contact-us",
        "faculty_appointment_finding": "Both official pages show Fabian Fagerholm as current Computer Science faculty, but one says Associate Professor while the department contact page says Assistant Professor.",
        "faculty_appointment_result": "uncertain",
        "overall_result": "confirmed_with_caveat",
        "corrective_action": "Keep the current-faculty match but mark academic rank as conflicting official metadata and confirm the current title with the department before outreach.",
    },
    "ror:040af2s02:program:phd-requiring-a-master-s:doctoral-programme-in-science-computer-science": {
        "degree_entry_url": "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes/doctoral-programmes/doctoral-programme-science/admissions-doctoral-studies",
        "degree_entry_finding": "The Doctoral Programme in Science requires a relevant second-cycle/master-level degree or equivalent.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes/how-apply-doctoral-programmes",
        "funding_finding": "The University states that a doctoral study right does not include funding and applicants must present a funding plan; salaried calls are separate.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.helsinki.fi/en/researchgroups/empirical-software-engineering/people",
        "faculty_appointment_finding": "The current research-group page lists Mika Mäntylä as Professor of Software Engineering.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain exclusion for the current bachelor-only profile and absent 2027 salary.",
    },
    "ror:026vcq606:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science": {
        "degree_entry_url": "https://www.kth.se/en/om/jobba-pa-kth/arbeta-och-utvecklas/befattningar-vid-kth/jobba-som-doktorand-vid-kth-1.456667",
        "degree_entry_finding": "KTH requires second-cycle eligibility, normally a second-cycle degree or 240 ECTS including at least 60 second-cycle credits, with foreign equivalency assessed for the vacancy.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.kth.se/en/om/jobba-pa-kth/arbeta-och-utvecklas/befattningar-vid-kth/jobba-som-doktorand-vid-kth-1.456667",
        "funding_finding": "KTH doctoral candidates are ordinarily employed, so salary and eligibility are tied to a posted doctoral position rather than generic program admission.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.kth.se/profile/monp?l=en",
        "faculty_appointment_finding": "KTH's current profile lists Martin Monperrus as Professor of Software Technology.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; keep credential equivalency conservative and monitor only funded vacancies with explicit eligibility.",
    },
    "ror:04qtj9h94:program:phd-requiring-a-master-s:phd-programme-dtu-compute": {
        "degree_entry_url": "https://www.compute.dtu.dk/Education/PhD-School",
        "degree_entry_finding": "DTU Compute directs candidates to advertised PhD projects; the ordinary three-year PhD employee route uses master's-level qualifications, with any integrated route requiring separate verification.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.dtu.dk/english/education/phd/intro/salary",
        "funding_finding": "DTU describes PhD candidates as salaried employees; the exact salary and term attach to the vacancy/contract rather than an open program promise.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://orbit.dtu.dk/en/persons/kurt-ekkart-kindler",
        "faculty_appointment_finding": "DTU's current research portal lists Ekkart Kindler as Associate Professor in Applied Mathematics and Computer Science.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; monitor funded vacancies and do not infer bachelor eligibility for the ordinary three-year route.",
    },
    "ror:03z77qz90:program:phd-requiring-a-master-s:phd-in-information-technology-computer-science": {
        "degree_entry_url": "https://ut.ee/en/content/phd-admissions",
        "degree_entry_finding": "University of Tartu doctoral admission requires a master's degree or an equivalent qualification giving PhD access in the awarding system.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://ut.ee/en/content/phd-admissions",
        "funding_finding": "Most admitted doctoral researchers receive junior-research-fellow employment, but some places are student-only; funding is therefore project/place-specific. The page gives a 2026 minimum full-time salary of EUR 2,100 monthly.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://ut.ee/en/employee/marlon-dumas",
        "faculty_appointment_finding": "The university employee profile lists Marlon Dumas as Professor of Information Systems.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain exclusion for the bachelor-only applicant and no specific 2027 employed place.",
    },
    "ror:036x5ad56:program:phd-requiring-a-master-s:doctoral-programme-in-computer-science-and-computer-engineering": {
        "degree_entry_url": "https://www.uni.lu/research-en/doctoral-education/dsse/computer-engineering/",
        "degree_entry_finding": "The Computer Engineering doctoral track requires a relevant master's degree or equivalent.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.uni.lu/en/jobs/doctoral-researcher-in-computer-science/",
        "funding_finding": "An official live vacancy can state a precise salary and 36-month term, but those terms are position-specific and cannot be carried forward as a Fall 2027 program guarantee.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.uni.lu/snt-en/people/lionel-briand/",
        "faculty_appointment_finding": "The current University of Luxembourg profile lists Lionel Briand as professor and head of the Software Verification and Validation group.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain exclusion for missing master's and lack of a matching Fall 2027 vacancy.",
    },
    "ror:02e2c7k09:program:phd-requiring-a-master-s:phd-vacancies-in-computer-science-software-engineering": {
        "degree_entry_url": "https://careers.tudelft.nl/",
        "degree_entry_finding": "TU Delft recruits PhD candidates through individual vacancies whose qualifications govern entry; current vacancies use master's-level preparation for the ordinary route.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://careers.tudelft.nl/job/Delft-PhD-Positie-Digitaal-Vertrouwen-2628-CD/1366274057/",
        "funding_finding": "The official vacancy provides a four-year employee contract structure and salary scale, confirming that funding is vacancy-specific rather than a generic program award.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://ocw.tudelft.nl/teachers/arie-van-deursen/",
        "faculty_appointment_finding": "TU Delft's official teaching profile identifies Arie van Deursen as Professor of Software Engineering and SERG head.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; monitor only explicit 2027 software-engineering vacancies and preserve vacancy-specific eligibility.",
    },
    "ror:02tyrky19:program:phd:phd-in-computer-science-and-statistics": {
        "degree_entry_url": "https://www.tcd.ie/media/tcd/scss/pdfs/PhD-Advertisement-Group-TRDA-Gareth.pdf",
        "degree_entry_finding": "A current official SCSS PhD call states the School's minimum entry as a 2.1 honours undergraduate degree or international equivalent; a master's is desirable for that call, not mandatory.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.tcd.ie/graduatestudies/awards/trda-pi/",
        "funding_finding": "The Research Doctorate Award is a limited competitive scheme rather than a universal package; no applicant award may be inferred from eligibility.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.scss.tcd.ie/siobhan.clarke/",
        "faculty_appointment_finding": "The current SCSS page lists Siobhán Clarke as Professor of Software Systems.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain Investigate Further until a Fall 2027 full international award is verified.",
    },
    "ror:05m7pjf47:program:phd:phd-computer-science": {
        "degree_entry_url": "https://www.ucd.ie/cs/t4media/Guide%20for%20Applicant%202026.pdf | https://hub.ucd.ie/usis/!W_HU_MENU.P_PUBLISH?AUDIENCE=&MAJR=T113&p_tag=COURSE",
        "degree_entry_finding": "UCD's 2026 official project guide includes PhD projects accepting a first/upper-second bachelor's in a technical field, and the current course portal exposes September 2027 international application routes. Bachelor entry is therefore project-specific, not universally no.",
        "degree_entry_result": "material_discrepancy",
        "funding_url": "https://www.ucd.ie/cs/t4media/Guide%20for%20Applicant%202026.pdf",
        "funding_finding": "The guide contains funded 2026 project calls, but it is not a general or transferable Fall 2027 full-funding guarantee.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.ucd.ie/cs/news/conferringofdegreesjune2025/",
        "faculty_appointment_finding": "The official School news identifies Liliana Pasquale as an associate professor and a supervisor of a newly conferred Computer Science PhD.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "material_discrepancy",
        "corrective_action": "Change direct_from_bachelors_eligible from no to project-specific/yes where a call permits it, and do not exclude solely for degree entry; retain Investigate/Do Not Apply until a matching 2027 fully funded international call is verified. Recheck the guide because direct fetch returned 404 during this audit even though UCD search indexing exposed its contents.",
    },
    "ror:052gg0110:program:phd:dphil-in-computer-science": {
        "degree_entry_url": "https://www.ox.ac.uk/admissions/graduate/courses/dphil-computer-science",
        "degree_entry_finding": "Oxford accepts a four-year first-class or strong upper-second bachelor's as one DPhil entry route; a three-year bachelor's generally needs a master's.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://www.ox.ac.uk/admissions/graduate/courses/dphil-computer-science",
        "funding_finding": "The course page describes broad competitive scholarship consideration and published overseas fees, but no individual full award is guaranteed.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.cs.ox.ac.uk/people/michael.wooldridge/",
        "faculty_appointment_finding": "Oxford Computer Science lists Michael Wooldridge as Ashall Professor of Foundations of Artificial Intelligence.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; keep funding unconfirmed and recommendation conservative.",
    },
    "ror:01nrxwf90:program:phd:phd-informatics": {
        "degree_entry_url": "https://informatics.ed.ac.uk/sites/default/files/2024-03/How%20to%20apply%20for%20a%20research%20degree%20at%20SoI.pdf",
        "degree_entry_finding": "The School's official application guide says applicants normally need a first or upper-second bachelor's degree or international equivalent; a master's is not universal.",
        "degree_entry_result": "confirmed",
        "funding_url": "https://informatics.ed.ac.uk/study-with-us/our-degrees/postgraduate-research-programmes-and-centres-doctoral-training/postgraduate-research-funding-opportunities-0",
        "funding_finding": "School studentships are competitive and limited; the cited full-fee/stipend terms do not establish a Fall 2027 applicant award.",
        "funding_result": "confirmed",
        "faculty_appointment_url": "https://www.research.ed.ac.uk/en/persons/david-aspinall/",
        "faculty_appointment_finding": "Edinburgh's research portal lists David Aspinall as Personal Chair in Software Safety and Security in Informatics.",
        "faculty_appointment_result": "confirmed",
        "overall_result": "confirmed",
        "corrective_action": "No data correction; retain Outreach Before Decision until full international funding and capacity are confirmed.",
    },
}


def build_exclusion_sample() -> list[dict[str, object]]:
    us_rows = read_csv(US_EXCLUSIONS)
    eu_rows = read_csv(EUROPE_EXCLUSIONS)
    for row in us_rows + eu_rows:
        row["selection_hash"] = selection_hash(row["institution_id"])

    selected_us = sorted(us_rows, key=lambda row: row["selection_hash"])[:7]

    selected_eu: list[dict[str, str]] = []
    seen_countries: set[str] = set()
    sorted_eu = sorted(eu_rows, key=lambda row: row["selection_hash"])
    for row in sorted_eu:
        if row["country"] not in seen_countries:
            selected_eu.append(row)
            seen_countries.add(row["country"])
        if len(selected_eu) == 6:
            break
    if len({row["primary_exclusion_reason"] for row in selected_eu}) < 2:
        minority_reason_row = next(
            row
            for row in sorted_eu
            if row["primary_exclusion_reason"] != selected_eu[0]["primary_exclusion_reason"]
        )
        selected_eu[-1] = minority_reason_row

    expected_us = [
        "us:ipeds:157809",
        "us:ipeds:385619",
        "us:ipeds:496283",
        "us:ipeds:242705",
        "us:ipeds:164270",
        "us:ipeds:194116",
        "us:ipeds:151801",
    ]
    expected_eu = [
        "ror:04j47fz63",
        "ror:039ce0m20",
        "ror:04bqkh239",
        "ror:0362ttz08",
        "ror:053qcv951",
        "ror:00tf2g326",
    ]
    assert [row["institution_id"] for row in selected_us] == expected_us
    assert [row["institution_id"] for row in selected_eu] == expected_eu

    output: list[dict[str, object]] = []
    for region, rows, method in (
        ("us", selected_us, "Seven smallest SHA-256 hashes of seed|institution_id across the full U.S. exclusion log."),
        (
            "europe",
            selected_eu,
            "SHA-256 hash order with first institution per country; final slot deterministically replaced by the first different exclusion reason to cover reason diversity.",
        ),
    ):
        for rank, row in enumerate(rows, start=1):
            evidence = EXCLUSION_EVIDENCE[row["institution_id"]]
            output.append(
                {
                    "sample_id": f"{region}-{rank:02d}",
                    "region": region,
                    "selection_seed": SEED,
                    "sample_selection": method,
                    "selection_rank": rank,
                    "selection_hash": row["selection_hash"],
                    "institution_id": row["institution_id"],
                    "institution_name": evidence.get("official_name", row["institution_name"]),
                    "country": row["country"],
                    "source_stage": row["stage_of_exclusion"],
                    "source_exclusion_reason": row["primary_exclusion_reason"],
                    "official_url": evidence["official_url"],
                    "finding": evidence["finding"],
                    "false_negative": evidence["false_negative"],
                    "corrective_action": evidence["corrective_action"],
                    "confidence": evidence["confidence"],
                    "date_checked": CHECK_DATE,
                }
            )
    return output


def build_finalist_audit() -> list[dict[str, object]]:
    programs = read_csv(EUROPE_PROGRAMS)
    professors = read_csv(EUROPE_PROFESSORS)
    professors_by_program = {row["program_id"]: row for row in professors}
    assert len(professors_by_program) == len(professors)
    assert set(FINALIST_EVIDENCE) == {row["program_id"] for row in programs}
    assert set(professors_by_program) == {row["program_id"] for row in programs}

    output: list[dict[str, object]] = []
    for row in programs:
        evidence = FINALIST_EVIDENCE[row["program_id"]]
        professor = professors_by_program[row["program_id"]]
        output.append(
            {
                "program_id": row["program_id"],
                "institution_id": row["institution_id"],
                "institution_name": row["institution_name"],
                "country": row["country"],
                "program_name": row["program_name"],
                "source_direct_from_bachelors_eligible": row["direct_from_bachelors_eligible"],
                "degree_entry_url": evidence["degree_entry_url"],
                "degree_entry_finding": evidence["degree_entry_finding"],
                "degree_entry_result": evidence["degree_entry_result"],
                "source_funding_model": row["funding_model"],
                "source_funding_status": row["funding_status"],
                "funding_url": evidence["funding_url"],
                "funding_finding": evidence["funding_finding"],
                "funding_result": evidence["funding_result"],
                "professor_id": professor["professor_id"],
                "professor_name": professor["full_name"],
                "source_faculty_position": professor["faculty_position"],
                "faculty_appointment_url": evidence["faculty_appointment_url"],
                "faculty_appointment_finding": evidence["faculty_appointment_finding"],
                "faculty_appointment_result": evidence["faculty_appointment_result"],
                "overall_result": evidence["overall_result"],
                "corrective_action": evidence["corrective_action"],
                "date_checked": CHECK_DATE,
            }
        )
    return output


def main() -> None:
    exclusion_rows = build_exclusion_sample()
    finalist_rows = build_finalist_audit()

    write_csv(OUTPUT_DIR / "exclusion_sample_audit.csv", exclusion_rows)
    write_csv(OUTPUT_DIR / "europe_finalist_second_source.csv", finalist_rows)

    exclusion_counts = Counter(row["region"] for row in exclusion_rows)
    false_negatives = [row for row in exclusion_rows if row["false_negative"] == "yes"]
    finalist_overall = Counter(row["overall_result"] for row in finalist_rows)
    finalist_category = Counter(
        result
        for row in finalist_rows
        for result in (row["degree_entry_result"], row["funding_result"], row["faculty_appointment_result"])
    )

    checks = {
        "us_sample_at_least_5": exclusion_counts["us"] >= 5,
        "europe_sample_at_least_5": exclusion_counts["europe"] >= 5,
        "europe_sample_at_least_5_countries": len({row["country"] for row in exclusion_rows if row["region"] == "europe"}) >= 5,
        "europe_sample_at_least_2_reasons": len({row["source_exclusion_reason"] for row in exclusion_rows if row["region"] == "europe"}) >= 2,
        "false_negative_enum_valid": all(row["false_negative"] in {"yes", "no"} for row in exclusion_rows),
        "exclusion_required_fields_complete": all(
            row["sample_selection"] and row["official_url"] and row["finding"] and row["corrective_action"]
            for row in exclusion_rows
        ),
        "all_europe_finalist_programs_covered_once": len(finalist_rows) == 18 and len({row["program_id"] for row in finalist_rows}) == 18,
        "all_europe_finalist_professors_covered": len({row["professor_id"] for row in finalist_rows}) == 17,
        "all_finalist_dimensions_sourced": all(
            row["degree_entry_url"]
            and row["degree_entry_finding"]
            and row["funding_url"]
            and row["funding_finding"]
            and row["faculty_appointment_url"]
            and row["faculty_appointment_finding"]
            for row in finalist_rows
        ),
        "finalist_result_enums_valid": all(
            result in {"confirmed", "material_discrepancy", "uncertain"}
            for row in finalist_rows
            for result in (row["degree_entry_result"], row["funding_result"], row["faculty_appointment_result"])
        ),
        "corrective_action_present_for_all_findings": all(row["corrective_action"] for row in finalist_rows),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"Validation checks failed: {failed}")

    validation = {
        "status": "pass_with_findings",
        "date_checked": CHECK_DATE,
        "selection_seed": SEED,
        "source_file_sha256": {
            str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
            for path in (US_EXCLUSIONS, EUROPE_EXCLUSIONS, EUROPE_PROGRAMS, EUROPE_PROFESSORS)
        },
        "counts": {
            "exclusion_samples_total": len(exclusion_rows),
            "us_exclusion_samples": exclusion_counts["us"],
            "europe_exclusion_samples": exclusion_counts["europe"],
            "europe_sample_countries": len({row["country"] for row in exclusion_rows if row["region"] == "europe"}),
            "europe_sample_reasons": len({row["source_exclusion_reason"] for row in exclusion_rows if row["region"] == "europe"}),
            "false_negatives": len(false_negatives),
            "europe_finalist_programs_checked": len(finalist_rows),
            "europe_finalist_unique_institutions": len({row["institution_id"] for row in finalist_rows}),
            "europe_finalist_unique_professors": len({row["professor_id"] for row in finalist_rows}),
            "europe_finalist_overall_results": dict(sorted(finalist_overall.items())),
            "europe_finalist_dimension_results": dict(sorted(finalist_category.items())),
        },
        "false_negative_ids": [row["institution_id"] for row in false_negatives],
        "material_finalist_findings": [
            {
                "program_id": row["program_id"],
                "institution_name": row["institution_name"],
                "corrective_action": row["corrective_action"],
            }
            for row in finalist_rows
            if row["overall_result"] == "material_discrepancy"
        ],
        "caveats": [
            "This was a bounded official-source audit, not an exhaustive re-screen of every excluded institution.",
            "No recruiting inference was made from faculty activity, publications, grants, or current students.",
            "UCD's current 2026 guide was visible through the official-domain search index but returned 404 on direct fetch; its degree-entry correction should be reconfirmed from the School or a refreshed official guide before outreach.",
            "Aalto publishes conflicting current rank labels for Fabian Fagerholm; appointment is current, exact rank needs reconciliation.",
        ],
        "checks": checks,
        "outputs": [
            "data/processed/validation/cross_region_ca/exclusion_sample_audit.csv",
            "data/processed/validation/cross_region_ca/europe_finalist_second_source.csv",
            "data/processed/validation/cross_region_ca/validation.json",
            "evidence/validation/cross_region_ca/README.md",
        ],
    }
    with (OUTPUT_DIR / "validation.json").open("w", encoding="utf-8") as handle:
        json.dump(validation, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
