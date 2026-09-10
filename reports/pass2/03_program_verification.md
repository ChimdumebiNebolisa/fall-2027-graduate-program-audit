# Pass 2 Stage 3 — Program structure, eligibility, and funding verification

Generated: 2026-09-10T21:05:18.303739+00:00

Decision: **PASS — verification re-entry 01 complete**

## Outcome

All 1,977 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 Stage 2 re-entry routes were re-verified from official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 26 | 8 |
| Conditional | 29 | 2 |
| Monitor | 295 | 2 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 55 | 10 |

## Stage 2 re-entry routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| University of Wisconsin-Madison | [Computer Sciences, PhD](https://guide.wisc.edu/graduate/computer-sciences/computer-sciences-phd/) | conditional | pass | resolvable_inquiry | Will an admission offer include the published four-year funding guarantee for this applicant? |
| University of Minnesota-Twin Cities | [PhD in Computer Science](https://cse.umn.edu/cs/phd-admissions) | retained | pass | pass | What are the offer-specific stipend, summer, remaining health-insurance, and mandatory-fee amounts? |
| University of Colorado Boulder | [Doctor of Philosophy in Computer Science](https://www.colorado.edu/cs/academics/graduate-programs/doctor-philosophy) | retained | pass | pass | What summer support and current 2027-2028 stipend will the individual offer provide? |
| University of Arizona | [Computer Science PhD](https://cs.arizona.edu/graduate/prospective-students) | retained | pass | pass | What duration, stipend, mandatory-fee, and summer terms will the admission offer specify? |
| University at Buffalo | [PhD in Computer Science and Engineering](https://engineering.buffalo.edu/computer-science-engineering/graduate/degrees-and-programs/phd-in-computer-science-and-engineering.html) | monitor | resolvable_question | resolvable_inquiry | Will the committee admit this bachelor's applicant directly and issue a fully funded multi-year offer? |
| University of Utah | [Computing PhD](https://www.cs.utah.edu/graduate/academic-programs/ms-and-phd-programs/) | retained | pass | pass | What is the correct Fall 2027 deadline, and will the offer specify full first-year appointment and differential-fee coverage? |
| University of California-San Diego | [Computer Science and Engineering PhD](https://cse.ucsd.edu/graduate/doctoral-programs-computer-science-and-engineering) | retained | pass | pass | What multi-year and summer support will the offer and prospective advisor commit beyond year one? |
| Duke University | [Computer Science PhD](https://cs.duke.edu/graduate/phd) | retained | pass | pass | What are the 2027-2028 stipend, summer-support, and offer-specific conditions? |
| Brown University | [Computer Science PhD](https://cs.brown.edu/degrees/doctoral/) | retained | pass | pass | What are the exact guaranteed duration, 2027-2028 stipend, summer, and mandatory-fee terms? |
| University of Virginia-Main Campus | [Ph.D. in Computer Science](https://engineering.virginia.edu/department/computer-science/academics/graduate-programs/phd-computer-science) | retained | pass | pass | Will the individual offer guarantee support beyond the first year and specify summer coverage? |
| Simon Fraser University | [Master of Science in Computing Science — Thesis Option](https://www.sfu.ca/fas/study/future-graduates/programs/master-science-thesis.html) | conditional | resolvable_question | pass | Will SFU deem the applicant's 3.35/4.0 GPA equivalent to its 3.00/4.33 threshold, and what is net support after tuition and fees? |
| Chalmers University of Technology | [Computer Science, MSc](https://www.chalmers.se/en/education/find-masters-programme/computer-science-msc/) | monitor | resolvable_question | unverified | Does the transcript satisfy every credit prerequisite, and is there a scholarship covering tuition plus adequate living costs? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Conditional rows are positioned only as `Outreach Before Decision`. Wisconsin needs a funding-incidence answer because its four-year guarantee applies to many, not all, admits. SFU needs an official interpretation of the applicant's 4.0-scale GPA against its 4.33-scale minimum. Buffalo and Chalmers remain monitors because each has more than one material gate unresolved.

## Acceptance checks

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

## Blockers

None prevented Stage 3 completion.

## Unresolved coverage

- Fall 2027 is explicitly published for Colorado, UC San Diego, Duke, UVA, SFU (deadline TBD), and Chalmers; other rows use the latest current deadline page with the cycle limitation labeled.
- University of Virginia's official pages remained blocked to automated HTTP retrieval, although their current indexed official-page content was available; Stage 4 should browser-check them again before using the row.
- Application-fee amounts remain unverified for Wisconsin and Brown; simultaneous-application rules remain unknown for most routes.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever the official page did not publish them.
- Chalmers has no verified adequate funding route for this fee-paying Nigerian applicant; Buffalo has both direct-entry and funding-incidence uncertainty.
- 4 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 10 new retained/conditional routes; the two monitor routes do not pass the faculty-review gate.
- The full test suite therefore has two expected Stage 4 coverage failures: roster configuration and five-professor evaluation coverage for the 10 new faculty-review-ready routes. Stage 3-specific tests pass.
