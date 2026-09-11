# Stage 3 Result

Generated: 2026-09-11T05:59:47.646449+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 09 is complete.

## What changed

All 2,073 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 09 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 41 | 3 |
| Conditional | 65 | 3 |
| Monitor | 340 | 6 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 106 | 6 |

### Stage 2 re-entry 09 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| Emory University | [Doctor of Philosophy in Computer Science and Informatics](https://computerscience.emory.edu/graduate-phd/index.html) | retained | pass | pass | What are the Fall 2027 stipend, insurance, mandatory-fee, summer-support, and English-test terms in the actual offer? |
| Northwestern University | [Doctor of Philosophy in Computer Science](https://www.mccormick.northwestern.edu/computer-science/academics/graduate/phd/) | retained | pass | pass | What stipend, summer, health-insurance, and mandatory-fee terms will accompany the five-year Fall 2027 guarantee? |
| University of Pittsburgh-Pittsburgh Campus | [Doctor of Philosophy in Computer Science](https://intranet.cs.pitt.edu/grad/) | conditional | pass | resolvable_inquiry | Will a Fall 2027 CS PhD admission offer guarantee full tuition, adequate stipend, insurance, fees, and summer support for a stated duration? |
| Brandeis University | [Doctor of Philosophy in Computer Science](https://www.brandeis.edu/gsas/programs/computer_science.html) | conditional | pass | resolvable_inquiry | Does every admitted Fall 2027 CS PhD student receive the five-year tuition, stipend, and health package, including summer and fees? |
| Michigan State University | [Doctor of Philosophy in Computer Science](https://engineering.msu.edu/academics/majors-degrees/computer-science-phd) | monitor | resolvable_question | unverified | Does the transcript meet every prerequisite, and will a Fall 2027 offer include renewable full tuition, stipend, insurance, fees, and summer funding? |
| Syracuse University | [Doctor of Philosophy in Computer/Information Science and Engineering](https://ecs.syracuse.edu/academics/electrical-engineering-and-computer-science/programs/computer-information-science-engineering-doctoral-program) | monitor | pass | unverified | Will a Fall 2027 offer include renewable full tuition, adequate stipend, insurance, fees, and separate summer support? |
| Johns Hopkins University | [Doctor of Philosophy in Computer Science](https://www.cs.jhu.edu/academic-programs/graduate-studies/phd-program/) | retained | pass | pass | What maximum duration, fee, summer, and Fall 2027 stipend terms govern the good-standing funding guarantee? |
| St. Francis Xavier University | [Master of Science in Computer Science](https://www.stfx.ca/programs-courses/programs/master-science-computer-science) | conditional | resolvable_question | pass | Will a willing supervisor support the application, and will the specific package cover tuition plus adequate living, fees, insurance, and summer costs for two years? |
| KTH Royal Institute of Technology | [Master of Science in Computer Science](https://www.kth.se/en/studies/master/computer-science) | monitor | resolvable_question | unverified | Does the transcript satisfy every ECTS prerequisite, and can the applicant secure a scholarship that covers both tuition and the full two-year living cost? |
| University of Helsinki | [Master's Programme in Computer Science](https://www.helsinki.fi/en/degree-programmes/computer-science-masters-programme) | monitor | resolvable_question | unverified | Will admissions accept the relevant-study mapping, and can the applicant secure full tuition plus independent living, health, fee, and summer funding? |
| University of Copenhagen | [Master of Science in Computer Science](https://www.ku.dk/studies/masters/computer-science) | monitor | resolvable_question | unverified | Does the transcript satisfy each ECTS category, and will any scholarship cover the full tuition and living cost for the two-year degree? |
| University of Tartu | [Master of Science in Engineering (Computer Science)](https://ut.ee/en/curriculum/computer-science) | monitor | pass | unverified | Can the applicant secure a renewable combination that covers EUR 14,400 tuition plus living, health, fees, and summer costs for two years? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Emory, Northwestern, and Johns Hopkins are retained. Conditional rows are positioned only as `Outreach Before Decision`: Pittsburgh and Brandeis require offer-specific funding confirmation, while StFX requires a willing supervisor. Michigan State, Syracuse, KTH, Helsinki, Copenhagen, and Tartu remain monitors because formal eligibility and/or a credible full-cost funding route is unresolved.

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

- Fall 2027 dates are explicit for Syracuse, KTH, and Helsinki; other dates are recurring or latest-cycle evidence and remain labeled for reconfirmation.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- KTH, Helsinki, Copenhagen, and Tartu publish competitive or partial awards that do not establish full tuition and living-cost support.

## Records requiring human judgment

- 9 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 6 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- Pittsburgh and Brandeis need offer-level funding confirmation; StFX needs documented supervisor willingness and package sufficiency.
- Michigan State and the four European monitors need transcript or full-cost funding resolution as recorded in their largest unresolved question.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_09.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_09_verification.csv`
- `data/processed/pass2/stage_03_reentry_09_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
