# Stage 3 Result

Generated: 2026-09-11T08:40:45.517346+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 11 is complete.

## What changed

All 2,097 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 11 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 42 | 1 |
| Conditional | 78 | 8 |
| Monitor | 350 | 3 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 120 | 9 |

### Stage 2 re-entry 11 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| Binghamton University | [PhD in Computer Science](https://www.binghamton.edu/apps/academics/program/gd/computer-science) | monitor | resolvable_question | resolvable_inquiry | Will the department accept direct bachelor's entry with faculty support and issue a renewable package covering tuition, fees, insurance, stipend, and summer? |
| University of Louisiana at Lafayette | [PhD in Applied Computing and Information Sciences](https://louisiana.edu/graduateschool/majors-minors/applied-computing-and-information-sciences-phd) | conditional | pass | resolvable_inquiry | Will an actual Fall 2027 offer include the fellowship or an equivalent four-year package, and what insurance or other charges remain? |
| Montana State University | [Computer Science PhD](https://www.cs.montana.edu/phd-degree.html) | conditional | pass | resolvable_inquiry | Does the Fall 2027 offer provide guaranteed multi-year funding with tuition, fees, insurance, and summer despite the draft-page caveat? |
| Tennessee Technological University | [Computer Science PhD](https://www.tntech.edu/engineering/programs/csc/ph.d-program.php) | conditional | pass | resolvable_inquiry | Will a Fall 2027 award guarantee renewable academic-year and summer support while covering tuition, fees, and insurance? |
| University of Memphis | [PhD in Computer Science](https://www.memphis.edu/cs/programs/phd_computer_science.php) | monitor | resolvable_question | resolvable_inquiry | Can the applicant satisfy the GRE requirement and obtain a renewable offer covering stipend, tuition, fees, insurance, and summer? |
| University of Wyoming | [PhD in Computer Science](https://www.uwyo.edu/uw/degree-programs/computer-science-ms-phd.html) | conditional | pass | resolvable_inquiry | Will the applicant receive a full-time renewable assistantship, and what summer or incidental costs remain outside it? |
| Trent University | [MSc in Applied Modelling and Quantitative Methods — Thesis Stream](https://www.trentu.ca/graduatestudies/program/applied-modelling-quantitative-methods-ma-or-msc/thesis-stream) | conditional | pass | resolvable_inquiry | After international tuition, fees, insurance, and living costs, what guaranteed net amount remains for each of the two years? |
| University of Waterloo | [Master of Applied Science in Systems Design Engineering](https://uwaterloo.ca/future-graduate-students/programs/by-faculty/engineering/systems-design-engineering-master-applied-science-masc) | monitor | resolvable_question | unverified | Is the CS bachelor's formally equivalent to the required engineering preparation, and can a supervisor provide funding above the minimum to cover international tuition and living costs? |
| Concordia University | [Cybersecurity Engineering (MASc)](https://www.concordia.ca/academics/graduate/cybersecurity-engineering-masc.html) | conditional | pass | resolvable_inquiry | Will a willing advisor provide a two-year package that covers international tuition, compulsory fees, insurance, and living costs? |
| University of Pisa | [Master's Degree in Computer Science](https://www.unipi.it/en/education/courses/master-degree/computer-science-wif-lm-en/) | conditional | resolvable_question | pass | Does the transcript satisfy the 72-credit subject distribution, and can the applicant document DSU economic eligibility for 2027–28? |
| University of Florence | [MSc in Software: Science and Technology](https://www.unifi.it/en/study-us/degree-programs/second-cycle-degree/software-science-and-technology) | retained | pass | pass | Can the applicant complete the required foreign economic documentation and win the 2027–28 DSU package, including an available housing place? |
| Università di Camerino | [Master of Science in Computer Science](https://sst.unicam.it/corsi/computer-science) | conditional | resolvable_question | pass | Will academic review accept the applicant's curriculum and B2 evidence, and can current ERDIS terms be documented for a complete 2027–28 package? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Florence is retained because a current relevant research route, formal eligibility path, and credible DSU full-cost mechanism are all documented. Louisiana-Lafayette, Montana State, Tennessee Tech, Wyoming, Trent, Concordia, Pisa, and Camerino are conditional and positioned only as `Outreach Before Decision`. Binghamton, Memphis, and Waterloo remain monitors because both eligibility and/or full-cost funding gates remain unresolved.

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

- No new route publishes an explicit Fall 2027 deadline; recurring or latest-cycle dates are labeled and must be reconfirmed when the 2027–28 calls open.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- Waterloo's guaranteed minimum is below current international tuition and fees before living costs; Binghamton and Memphis also lack a resolved eligibility-and-package combination.

## Records requiring human judgment

- 11 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 9 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- The U.S. and Canadian conditionals need offer-level or net-cost funding confirmation before application spending.
- Pisa and Camerino need formal transcript or language resolution; Florence, Pisa, and Camerino also depend on annual means- and merit-tested regional scholarship calls.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_11.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_11_verification.csv`
- `data/processed/pass2/stage_03_reentry_11_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
