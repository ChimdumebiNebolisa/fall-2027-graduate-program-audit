# Stage 3 Result

Generated: 2026-09-11T12:54:07.166360+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 15 is complete.

## What changed

All 2,145 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 15 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 47 | 1 |
| Conditional | 96 | 6 |
| Monitor | 375 | 5 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 143 | 7 |

### Stage 2 re-entry 15 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| University of New Hampshire-Main Campus | [Computer Science, Ph.D.](https://www.unh.edu/program/doctor-philosophy/computer-science) | conditional | pass | resolvable_inquiry | Will UNH offer this applicant renewable year-round support covering tuition, mandatory fees, insurance, stipend, and summer? |
| University of Missouri-Columbia | [PhD in Computer Science](https://catalog.missouri.edu/collegeofengineering/computerscience/) | conditional | pass | resolvable_inquiry | Will Mizzou issue an international-eligible assistantship with renewable tuition, fee, insurance, stipend, and summer coverage? |
| University of Wisconsin-Milwaukee | [Computer Science PhD](https://uwm.edu/engineering/academics/computer-science-phd/) | conditional | pass | resolvable_inquiry | Will UWM award and renew an assistantship that covers full tuition, fees, insurance, stipend, and summer for this applicant? |
| Illinois Institute of Technology | [Computer Science (Ph.D.)](https://www.iit.edu/academics/programs/computer-science-phd) | conditional | pass | resolvable_inquiry | Will the advertised faculty funding slot remain open for Fall 2027 with renewable stipend, tuition, fees, insurance, and summer coverage? |
| New Jersey Institute of Technology | [Ph.D. Computer Science](https://www.njit.edu/academics/degree/phd-computer-science) | retained | pass | pass | What exact duration, stipend, tuition, mandatory-fee, health-insurance, and summer terms would NJIT put in this applicant's offer? |
| University of Connecticut | [Computer Science and Engineering (PhD)](https://catalog.uconn.edu/graduate/degree-programs/computer-science-engineering-phd/) | conditional | pass | resolvable_inquiry | Can a verified-fit UConn advisor or the School confirm a renewable international package covering tuition, fees, insurance, stipend, and summer? |
| École de technologie supérieure | [Maîtrise en génie logiciel — profil avec mémoire (M.Sc.A.)](https://www.etsmtl.ca/programmes-formations/maitrise-genie-logiciel) | monitor | resolvable_question | unverified | Can an eligible software-engineering supervisor accept the applicant and provide a package that covers base tuition, fees, insurance, and living costs beyond the limited exemption? |
| Université du Québec à Rimouski | [Maîtrise en informatique — profil recherche avec mémoire](https://www.uqar.ca/programmes-domaines-detudes/maitrise-en-informatique/) | monitor | resolvable_question | unverified | Can UQAR confirm French/English completion rules, supervisor entry requirements, and a funding package sufficient for international tuition and living costs? |
| Saint Mary’s University | [MSc in Applied Science — Computing Science research field](https://www.smu.ca/faculty-of-science/master-in-applied-science-future-students.html) | conditional | resolvable_question | pass | Will a Computing Science supervisor accept the applicant and confirm a two-year international package whose post-tuition value is adequate? |
| Mälardalen University | [Master's Programme in Software Engineering](https://www.mdu.se/en/malardalen-university/education/international/programme/masters-programme-in-software-engineering) | monitor | resolvable_question | unverified | Does the applicant meet the exact mathematics and computing-credit gate, and how would living costs be funded even if the full-tuition scholarship is won? |
| Linnaeus University | [Software Technology, Master Programme — 120 credits](https://www.lnu.se/en/programme/software-technology-master-programme-nada2/vaxjo-international-autumn/) | monitor | pass | unverified | What credible source will cover the remaining tuition and two years of living costs if the applicant receives at most the general 75% scholarship? |
| University of Coimbra | [Master in Informatics Engineering](https://www.uc.pt/en/fctuc/dei/education/masters/master-in-informatics-engineering/) | monitor | resolvable_question | unverified | Will Coimbra recognize the applicant's degree and permit full English completion, and what source will cover remaining tuition and living costs? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

NJIT is retained on current official evidence. UNH, Missouri, UWM, Illinois Tech, UConn, and Saint Mary’s are conditional and positioned only as `Outreach Before Decision`. ÉTS, UQAR, Mälardalen, Linnaeus, and Coimbra remain monitors because eligibility and/or credible full-cost funding gates remain unresolved.

## Validation performed

| Assertion | Result |
| --- | --- |
| all_12_reentry_programs_present | PASS |
| one_status_per_stage2_candidate | PASS |
| controlled_statuses_only | PASS |
| all_material_fields_explicit | PASS |
| reentry_program_and_admissions_sources_present | PASS |
| all_reentry_source_ids_resolve | PASS |
| all_reentry_sources_official | PASS |
| material_funding_claims_have_official_sources | PASS |
| retained_rows_pass_route_eligibility_and_funding | PASS |
| conditional_rows_have_exactly_one_resolvable_gate | PASS |
| conditional_rows_are_outreach_only | PASS |
| monitor_rows_do_not_proceed | PASS |
| exclusions_match_status | PASS |
| no_score_or_recommendation_fields | PASS |

## Material uncertainties or conflicts

- None of the latest routes publishes a confirmed Fall 2027 cycle; recurring or latest-cycle dates are labeled and must be reconfirmed when 2027–28 calls open.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- ÉTS, UQAR, Saint Mary’s, Mälardalen, and Coimbra need language, degree-equivalency, prerequisite, or supervisor resolution.
- The Canadian and European awards are partial, competitive, unavailable to this applicant, or unverified for living-cost coverage and are not treated as credible full funding.

## Records requiring human judgment

- 11 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 7 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- All five conditional U.S. routes and Saint Mary’s need offer-level tuition, fee, insurance, stipend, renewal, and summer confirmation before application spending.
- NJIT still requires written offer details; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_15.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_15_verification.csv`
- `data/processed/pass2/stage_03_reentry_15_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
