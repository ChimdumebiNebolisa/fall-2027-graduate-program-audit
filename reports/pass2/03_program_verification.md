# Stage 3 Result

Generated: 2026-09-11T07:22:07.854742+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 10 is complete.

## What changed

All 2,085 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 10 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 41 | 0 |
| Conditional | 70 | 5 |
| Monitor | 347 | 7 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 111 | 5 |

### Stage 2 re-entry 10 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| University of Oregon | [Doctor of Philosophy in Computer Science](https://scds.uoregon.edu/cs/graduate-programs/cs-phd) | conditional | pass | resolvable_inquiry | Will a Fall 2027 offer guarantee a funded appointment for the full expected duration and cover summer, insurance, tuition, and mandatory fees? |
| University of Georgia | [Doctor of Philosophy in Computer Science](https://www.cs.uga.edu/doctor-philosophy-computer-science) | conditional | pass | resolvable_inquiry | Will the applicant receive a renewable TA/RA package that covers the full doctoral period, including fees, insurance, and summer? |
| Georgia State University | [Doctor of Philosophy in Computer Science](https://graduate.gsu.edu/program/computer-science-phd/) | conditional | pass | resolvable_inquiry | Would a Fall 2027 offer include renewable support with tuition, fees, insurance, and summer coverage rather than only competitive consideration? |
| University of South Carolina-Columbia | [Doctor of Philosophy in Computer Science](https://cse.sc.edu/graduate/phd) | conditional | pass | resolvable_inquiry | Will an actual offer guarantee renewable support and fully specify residual tuition, fees, insurance, and summer funding? |
| University of Nevada-Reno | [Doctor of Philosophy in Computer Science and Engineering](https://www.unr.edu/cse/graduate-program) | conditional | pass | resolvable_inquiry | Will the department issue a renewable assistantship covering stipend, insurance, and sufficient tuition while leaving a manageable mandatory-fee balance? |
| University of Prince Edward Island | [Master of Science in Mathematical and Computational Sciences](https://www.upei.ca/programs/master-science-mathematical-and-computational-sciences) | monitor | resolvable_question | unverified | Can the applicant secure a qualified supervisor and a documented package covering the international program fee and living costs? |
| University of Winnipeg | [Master of Science in Applied Computer Science and Society — Thesis-Based](https://www.uwinnipeg.ca/programs/msc-acs.html) | monitor | resolvable_question | unverified | Will an eligible supervisor take the applicant and provide or identify funding sufficient for tuition, fees, insurance, and living costs? |
| Queen’s University | [Doctor of Philosophy in Computing](https://www.cs.queensu.ca/graduate/phd/) | monitor | fail_current_profile | pass | Is there any official direct-entry exception available to a Fall 2027 applicant without the required master's degree? |
| Uppsala University | [Master's Programme in Computer Science](https://www.uu.se/en/study/programme/masters-programme-computer-science) | monitor | resolvable_question | unverified | Does the transcript meet both exact credit thresholds, and can the applicant independently fund living costs even if a tuition scholarship is won? |
| Lund University | [Master's Programme in Machine Learning, Systems and Control](https://www.lunduniversity.lu.se/study/machine-learning-systems-and-control-masters-programme-TAMSR) | monitor | resolvable_question | unverified | Does the transcript include the required control and mathematics credits, and can the applicant fund living costs and any tuition not covered by a competitive award? |
| University of Luxembourg | [Master in Information and Computer Sciences](https://www.uni.lu/fstm-en/study-programs/master-in-information-and-computer-sciences/) | monitor | resolvable_question | unverified | Will the transcript and English evidence pass individual review, and is there any funding source covering both years of tuition and living costs? |
| Technical University of Denmark | [Master of Science in Engineering in Computer Science and Engineering](https://www.dtu.dk/english/education/graduate/msc-programmes/computer-science-and-engineering) | monitor | resolvable_question | unverified | Does the transcript satisfy every 75-ECTS subject allocation, and can the applicant fund living costs even if one of the very limited tuition waivers is awarded? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

No re-entry 10 route is retained. Oregon, Georgia, Georgia State, South Carolina, and Nevada-Reno are conditional and positioned only as `Outreach Before Decision` because an offer-level assistantship package remains unresolved. UPEI, Winnipeg, Queen's, Uppsala, Lund, Luxembourg, and DTU remain monitors because formal eligibility and/or a credible full-cost funding route is unresolved.

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

- Fall 2027 deadline or cycle evidence is explicit for Oregon, Georgia, Queen's, and Lund; Lund's exact closing day and other recurring or latest-cycle dates remain labeled for reconfirmation.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- Uppsala, Lund, Luxembourg, and DTU publish competitive or partial awards that do not establish full tuition and living-cost support.

## Records requiring human judgment

- 12 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 5 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- The five U.S. conditionals need offer-level funding confirmation; UPEI and Winnipeg need documented supervisor willingness and package sufficiency.
- Queen's currently requires an MSc, while all four European monitors need transcript or full-cost funding resolution as recorded in their largest unresolved question.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_10.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_10_verification.csv`
- `data/processed/pass2/stage_03_reentry_10_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
