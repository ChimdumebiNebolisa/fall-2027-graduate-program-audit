# Stage 3 Result

Generated: 2026-09-11T11:51:14.496167+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 14 is complete.

## What changed

All 2,133 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 14 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 46 | 2 |
| Conditional | 90 | 3 |
| Monitor | 370 | 7 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 136 | 5 |

### Stage 2 re-entry 14 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| University of Nebraska at Omaha | [Computing & Information Science, Ph.D.](https://www.unomaha.edu/college-of-information-science-and-technology/academics/computing_and_information_science_phd.php) | conditional | pass | resolvable_inquiry | Will UNO issue a renewable assistantship whose stipend plus tuition, fees, insurance, and summer terms produce adequate net funding? |
| University of Colorado Colorado Springs | [Cybersecurity, PhD](https://www.uccs.edu/academics/programs/security-phd) | conditional | pass | resolvable_inquiry | Will an aligned faculty member commit renewable grant funding with adequate stipend and written tuition, fee, insurance, and summer coverage? |
| University of Massachusetts-Lowell | [Doctor of Philosophy (Ph.D.) in Computer Science](https://www.uml.edu/sciences/computer-science/programs/doctorate.aspx) | conditional | pass | resolvable_inquiry | Will an adviser or department commit a renewable package covering adequate stipend, tuition, fees, insurance, and summers? |
| University of Louisville | [Doctor of Philosophy in Computer Science and Engineering](https://catalog.louisville.edu/graduate/programs-study/doctor-philosophy-computer-science-engineering/) | retained | pass | pass | Will the eventual written offer include this fellowship and clarify mandatory fees, summer timing, and renewal through completion? |
| Wayne State University | [Computer Science (Ph.D.)](https://bulletins.wayne.edu/graduate/college-engineering/computer-science/computer-science-phd/index.html) | monitor | pass | unverified | Does Computer Science offer incoming international PhD students a renewable package covering stipend, tuition, fees, insurance, and summers? |
| Clarkson University | [PhD in Computer Science](https://www.clarkson.edu/academics/majors-minors/computer-science-phd) | retained | pass | pass | Will Clarkson's written offer extend adequate stipend and tuition coverage through the full doctorate and specify fees, insurance, and summers? |
| Université du Québec en Outaouais | [Maîtrise en informatique (profil mémoire)](https://uqo.ca/programmes/3097) | monitor | resolvable_question | resolvable_inquiry | Will UQO confirm degree/GPA and French eligibility and provide a package covering tuition, fees, insurance, and living costs? |
| Université du Québec à Chicoutimi | [Maîtrise en informatique - profil recherche (mémoire)](https://programmes.uqac.ca/3017) | monitor | resolvable_question | resolvable_inquiry | Will UQAC confirm equivalency/French eligibility and assemble funding beyond the tuition differential to cover total costs? |
| Université du Québec à Trois-Rivières | [Maîtrise en mathématiques et informatique appliquées (avec mémoire)](https://oraprdnt.uqtr.uquebec.ca/portail/triw082.afficher?owa_cd_pgm=3799&owa_version=1) | monitor | resolvable_question | resolvable_inquiry | Will UQTR confirm GPA/French eligibility and a supervisor-backed package adequate for tuition, fees, insurance, and living costs? |
| Vrije Universiteit Brussel | [Master of Science in Applied Sciences and Engineering: Computer Science - Software Systems](https://www.vub.be/en/studying-vub/all-study-programmes-vub/bachelors-and-masters-programmes-vub/master-applied-sciences-and-engineering-computer-science/program/master/master-software-systems) | monitor | resolvable_question | unverified | Will faculty screening confirm equivalency and can the applicant secure funding for tuition, fees, insurance, and Brussels living costs? |
| University of Southern Denmark | [Software Engineering - MSc in Engineering](https://www.sdu.dk/en/uddannelse/kandidat/softwareengineering) | monitor | resolvable_question | unverified | Does the transcript meet every ECTS prerequisite, and is any full-cost scholarship available for this Odense program? |
| University of Klagenfurt | [Master's Degree Programme Informatics](https://www.aau.at/en/studien/master-informatics/) | monitor | resolvable_question | unverified | Will equivalency be approved, and can the applicant identify funding beyond an apparently ineligible partial scholarship to cover total costs? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Louisville and Clarkson are retained on current official evidence. UNO, UCCS, and UMass Lowell are conditional and positioned only as `Outreach Before Decision`. Wayne State, UQO, UQAC, UQTR, VUB, SDU, and Klagenfurt remain monitors because eligibility and/or credible full-cost funding gates remain unresolved.

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

- UNO publishes Fall 2027 timing; other routes use recurring or latest-cycle dates that are labeled and must be reconfirmed when 2027–28 calls open.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- UQO, UQAC, UQTR, VUB, SDU, and Klagenfurt need language, grade, degree-equivalency, GRE, or transcript resolution.
- The Canadian and European awards are partial, competitive, unavailable to this applicant, or unverified for living-cost coverage and are not treated as credible full funding.

## Records requiring human judgment

- 10 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 5 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- All three conditional U.S. routes need offer-level tuition, fee, insurance, stipend, renewal, and summer confirmation before application spending.
- The two retained routes still require written offer details; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_14.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_14_verification.csv`
- `data/processed/pass2/stage_03_reentry_14_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
