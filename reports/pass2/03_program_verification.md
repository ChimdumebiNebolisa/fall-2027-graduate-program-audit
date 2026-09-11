# Stage 3 Result

Generated: 2026-09-11T09:45:12.086178+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 12 is complete.

## What changed

All 2,109 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 12 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 42 | 0 |
| Conditional | 84 | 6 |
| Monitor | 356 | 6 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 126 | 6 |

### Stage 2 re-entry 12 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| New Mexico State University-Main Campus | [Computer Science (Ph.D.)](https://nmsu.edu/degree-programs/graduate/doctoral/computer-science.html) | monitor | resolvable_question | resolvable_inquiry | Will the department waive or reinterpret the 3.5 GPA gate and issue a renewable assistantship covering tuition, fees, insurance, stipend, and summer? |
| University of Idaho | [Computer Science, Ph.D.](https://www.uidaho.edu/academics/degree-finder/computer-sci-phd) | conditional | pass | resolvable_inquiry | Will the program issue a renewable faculty or departmental package that covers tuition, fees, insurance, stipend, and summer for an international PhD student? |
| Kansas State University | [Doctor of Philosophy in Computer Science](https://www.cs.ksu.edu/academics/graduate/phd/) | conditional | pass | resolvable_inquiry | Which appointment will be offered, for how many years, and what tuition, fees, insurance, stipend, and summer costs will it cover? |
| Oklahoma State University-Main Campus | [Doctor of Philosophy in Computer Science](https://cas.okstate.edu/computer_science/graduate/phd_cs) | conditional | pass | resolvable_inquiry | Will OSU issue and renew an assistantship that covers full tuition, mandatory fees, insurance, stipend, and summer for this applicant? |
| West Virginia University | [Computer Science, Ph.D.](https://catalog.wvu.edu/graduate/collegeofengineeringandmineralresources/thelanedepartmentofcomputerscienceandelectricalengineering/cs/phd/) | conditional | pass | resolvable_inquiry | Will WVU provide a renewable GTA or GRA and what net tuition, college charges, fees, insurance, stipend, and summer costs remain? |
| Louisiana State University and Agricultural & Mechanical College | [Ph.D. in Computer Science and Engineering](https://www.lsu.edu/eng/cse/programs/graduate_program/graduate_phd.php) | conditional | pass | resolvable_inquiry | Will LSU issue a renewable five-year package and exactly which tuition, fees, insurance, stipend, and summer costs will it cover? |
| University of Lethbridge | [Master of Science in Computer Science](https://www.ulethbridge.ca/future-student/graduate-studies/master-science/computer-science) | monitor | resolvable_question | resolvable_inquiry | Can the applicant document the required upper-level preparation, secure a supervisor, and obtain a two-year package that covers international tuition and living costs? |
| Brock University | [Computer Science MSc — Thesis Stream](https://brocku.ca/programs/graduate/msc-cosc/) | conditional | pass | resolvable_inquiry | What current six-term net package will Brock provide after international tuition, fees, taxes, insurance, and living costs? |
| Lakehead University | [Master of Science in Computer Science — Thesis Route](https://www.lakeheadu.ca/programs/graduate/programs/masters/computer-science) | monitor | pass | unverified | Is any renewable funding package available that covers international tuition, fees, insurance, living costs, and summer for the thesis route? |
| Blekinge Institute of Technology | [Master's Programme in Software Engineering, 120 credits](https://www.bth.se/english/education/programmes/masters-programme-in-software-engineering-120-credits) | monitor | resolvable_question | unverified | Can the transcript meet every ECTS prerequisite, and is there any external full-cost award beyond BTH's partial tuition scholarship? |
| Karlstad University | [Master in Computer Science](https://www.kau.se/en/cs/education/programmes-and-courses/programmes/master-computer-science) | monitor | resolvable_question | unverified | Will the transcript satisfy every ECTS prerequisite, and is any funding available for the remaining tuition and all living costs? |
| Linköping University | [Computer Science, Master's Programme, 120 credits](https://liu.se/en/education/program/6mics) | monitor | pass | unverified | Can the applicant win support despite the latest scholarship benchmark, and is any source available for the remaining tuition and living costs? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Idaho, Kansas State, Oklahoma State, West Virginia, LSU, and Brock are conditional and positioned only as `Outreach Before Decision`. NMSU, Lethbridge, Lakehead, BTH, Karlstad, and Linköping remain monitors because eligibility and/or credible full-cost funding gates remain unresolved. No re-entry 12 route meets the retained gate on current evidence.

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

- Karlstad and Linköping publish Autumn 2027 program timing; all other routes use recurring or latest-cycle dates that are labeled and must be reconfirmed when their 2027–28 calls open.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- NMSU's published 3.5 minimum exceeds the applicant's 3.35 GPA; Lethbridge and the two prerequisite-heavy Swedish routes need formal transcript mapping.
- The verified Swedish scholarships are partial tuition awards without living-cost coverage and are not treated as credible full funding.

## Records requiring human judgment

- 12 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 6 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- The U.S. and Canadian conditionals need offer-level or net-cost funding confirmation before application spending.
- All six conditional routes need offer-level tuition, fee, insurance, stipend, renewal, and summer confirmation before application spending.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_12.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_12_verification.csv`
- `data/processed/pass2/stage_03_reentry_12_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
