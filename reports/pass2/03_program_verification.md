# Stage 3 Result

Generated: 2026-09-11T10:47:37.093694+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 13 is complete.

## What changed

All 2,121 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 13 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 44 | 2 |
| Conditional | 87 | 3 |
| Monitor | 363 | 7 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 131 | 5 |

### Stage 2 re-entry 13 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| University of Alabama in Huntsville | [Computer Science, Ph.D.](https://www.uah.edu/science/departments/computer-science/cs-graduate-programs) | conditional | pass | resolvable_inquiry | Will Computer Science issue a renewable assistantship that states stipend, tuition, mandatory fees, insurance, and summer support for the full doctorate? |
| The University of Texas at El Paso | [Doctor of Philosophy in Computer Science](https://catalog.utep.edu/grad/college-of-engineering/computer-science/computer-science-phd/) | conditional | pass | resolvable_inquiry | Will UTEP issue a renewable 20-hour appointment with adequate stipend and written coverage of tuition, fees, insurance, and summers? |
| University of Nevada-Las Vegas | [Doctor of Philosophy - Computer Science](https://www.unlv.edu/degree/phd-computer-science) | monitor | resolvable_question | resolvable_inquiry | Will UNLV approve direct-bachelor eligibility despite the cumulative GPA and pair admission with a renewable full-cost assistantship? |
| Old Dominion University | [Computer Science (Ph.D.)](https://www.odu.edu/academics/programs/doctoral/computer-science) | retained | pass | pass | What written renewal, fee, insurance, and summer terms apply after the guaranteed first-year assistantship? |
| Temple University | [Computer and Information Science PhD](https://bulletin.temple.edu/graduate/scd/cst/computer-information-science-phd/) | retained | pass | pass | Which Fall 2027 deadline controls and what written multi-year offer covers fees, insurance, and summers beyond tuition and stipend? |
| University of Rhode Island | [Computer Science Ph.D.](https://www.uri.edu/programs/program/computer-science-ph-d/) | conditional | pass | resolvable_inquiry | Will the department issue a renewable full-time assistantship, and what is the net annual cost after uncovered fees, insurance details, and summer living support? |
| Bishop's University | [M.Sc. in Computer Science — Thesis Option](https://www.ubishops.ca/academics/faculties-and-schools/faculty-of-natural-sciences-and-mathematics/computer-science/masters-degree-program/graduate-admission/) | monitor | pass | unverified | Can a supervisor commit enough renewable funding to cover international tuition, fees, insurance, living costs, and the full 20-24 month thesis period? |
| Université du Québec à Montréal | [Maîtrise en informatique — profil avec mémoire](https://info.uqam.ca/ma%C3%AEtrise_en_informatique/) | monitor | resolvable_question | unverified | Will UQAM confirm academic and French eligibility and identify a realistically attainable package covering international tuition and living costs for two years? |
| Université de Moncton | [Maîtrise ès sciences (informatique)](https://www.umcs.umoncton.ca/fesr/programmes?programme_id=222&programme_select=222) | monitor | resolvable_question | unverified | Will the program confirm French and academic eligibility and can a supervisor provide renewable support covering tuition, fees, insurance, and living costs for two years? |
| Tampere University | [Master's Programme in AI-Native Software](https://www.tuni.fi/en/tau/masters-programmes/ai-native-software-computing-sciences-and-electrical-engineering) | monitor | resolvable_question | unverified | Do the Fall 2027 academic criteria admit this transcript, and is there any external award that closes the remaining tuition and full two-year living-cost gap? |
| Paderborn University | [M.Sc. Computer Science](https://www.uni-paderborn.de/en/studyoffer/course_of_study/computer-science-master) | monitor | resolvable_question | unverified | Will the transcript satisfy every credit bucket and GRE rule, and can an external award cover the approximately EUR 1,210 monthly living-cost estimate plus fees and insurance? |
| Åbo Akademi University | [Master's Degree Programme in Information Technology — Computer Science](https://www.abo.fi/en/study-programme/masters-degree-programme-in-information-technology/) | monitor | pass | unverified | Can an external scholarship cover the remaining tuition plus mandatory fees, insurance, and two years of living costs under the Fall 2027 terms? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Old Dominion and Temple are retained on current official evidence. UAH, UTEP, and URI are conditional and positioned only as `Outreach Before Decision`. UNLV, Bishop's, UQAM, Moncton, Tampere, Paderborn, and Åbo Akademi remain monitors because eligibility and/or credible full-cost funding gates remain unresolved.

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

- Tampere and Åbo Akademi publish Fall 2027 application timing; all other routes use recurring or latest-cycle dates that are labeled and must be reconfirmed when 2027–28 calls open.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- UNLV's direct-bachelor GPA reference exceeds the applicant's cumulative GPA; UQAM, Moncton, Tampere, and Paderborn need language, grade, or transcript resolution.
- The verified Finnish scholarships are partial tuition awards without living-cost coverage and are not treated as credible full funding.

## Records requiring human judgment

- 10 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 5 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- All three conditional U.S. routes need offer-level tuition, fee, insurance, stipend, renewal, and summer confirmation before application spending.
- The two retained routes still require written offer details; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_13.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_13_verification.csv`
- `data/processed/pass2/stage_03_reentry_13_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
