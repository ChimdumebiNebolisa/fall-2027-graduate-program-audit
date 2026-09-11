# Stage 3 Result

Generated: 2026-09-11T15:07:33.156513+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 17 is complete.

## What changed

All 2,169 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 17 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 52 | 4 |
| Conditional | 108 | 5 |
| Monitor | 381 | 2 |
| Excluded | 1628 | 1 |
| Faculty-review ready | 160 | 9 |

### Stage 2 re-entry 17 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| Drexel University | [PhD in Computer Science](https://drexel.edu/cci/academics/doctoral-programs/phd-computer-science/) | retained | pass | pass | What stipend, fee, insurance, summer, and renewal terms will appear in the Fall 2027 assistantship offer? |
| Lehigh University | [PhD in Computer Science](https://engineering.lehigh.edu/academics/graduate/phd/phd-computer-science) | retained | pass | pass | What duration, summer, insurance, and mandatory-fee terms will Lehigh include in the actual funding offer? |
| George Washington University | [PhD in Computer Science](https://graduate.engineering.gwu.edu/phd-computer-science) | conditional | pass | resolvable_inquiry | Will a CS faculty member select the applicant for a renewable package covering all tuition, living costs, fees, insurance, and summers? |
| University at Albany | [Doctor of Philosophy in Computer Science](https://www.albany.edu/computer-science/programs/phd-computer-science) | conditional | pass | resolvable_inquiry | Does the Fall 2027 CS assistantship cover full tuition, fees, insurance, summer support, and multiple years at a livable stipend? |
| Worcester Polytechnic Institute | [PhD in Computer Science](https://www.wpi.edu/academics/study/computer-science-phd) | conditional | pass | resolvable_inquiry | Will WPI issue a multi-year full package covering tuition, fees, health insurance, and summers in addition to stipend? |
| Oakland University | [Doctor of Philosophy in Computer Science and Informatics](https://graduatecatalog.oakland.edu/programs/RiD4RoYOIfoKUJ6fRCKU/requirements-QhMWt) | monitor | resolvable_question | unverified | Will Oakland approve direct bachelor's entry for this record and pair it with a renewable full-cost Fall 2027 assistantship? |
| University of British Columbia | [Master of Applied Science in Electrical and Computer Engineering](https://www.grad.ubc.ca/prospective-students/graduate-degree-programs/master-of-applied-science-electrical-computer-engineering) | conditional | resolvable_question | pass | Will ECE treat the applicant's CS curriculum as sufficiently overlapping with ECE and issue a two-year net-positive funding package? |
| University of Toronto | [Master of Applied Science in Electrical and Computer Engineering](https://www.ece.utoronto.ca/graduates/degree-programs/masc/) | retained | pass | pass | What exact 2027-28 net funding, ancillary-fee, insurance, and summer payment terms apply to an international MASc offer? |
| McGill University | [Electrical Engineering (Thesis) (M.Sc.)](https://www.mcgill.ca/gradapplicants/program/electrical-engineering-msc) | conditional | pass | resolvable_inquiry | What guaranteed net funding, tuition, fees, insurance, summer coverage, and renewal terms will an international ECE MSc offer contain? |
| Norwegian University of Science and Technology | [Erasmus Mundus Joint Master in Cybersecurity and Assurance (CYBERSURE)](https://www.cybersure-master.eu/admission) | excluded | fail | pass | None for the gate: the applicant cannot supply a completed bachelor's by the published non-EU deadline. |
| Université Libre de Bruxelles | [Erasmus Mundus Joint Master in Cybersecurity (CYBERUS)](https://www.ulb.be/en/programme/m-secum) | monitor | pass | unverified | Will CYBERUS run a Fall 2027 intake with scholarships after the current funding period ends? |
| Åbo Akademi University | [Erasmus Mundus Joint Master in Engineering of Data-intensive Intelligent Software Systems (EDISS)](https://www.master-ediss.eu/) | retained | pass | pass | What exact Fall 2027 application window, number of awards, and local fee obligations will EDISS publish? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Drexel, Lehigh, Toronto ECE, and EDISS are retained on current official evidence. GW, UAlbany, WPI, UBC ECE, and McGill ECE are conditional and positioned only as `Outreach Before Decision`. Oakland and CYBERUS remain monitors. CYBERSURE is excluded because its published non-EU degree-document deadline precedes the applicant's graduation.

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
| excluded_rows_fail_eligibility_and_do_not_proceed | PASS |
| exclusions_match_status | PASS |
| no_score_or_recommendation_fields | PASS |

- Current-round official URL retrieval: 42 of 42 returned HTTP 200.
- Stage-specific tests: 24 passed.
- Full suite boundary: 143 passed and 3 expected downstream coverage failures in Stages 4 and 5.

## Material uncertainties or conflicts

- Drexel, Lehigh, GW, UAlbany, Oakland, McGill, CYBERUS, and EDISS still rely partly or wholly on recurring or latest-cycle dates that must be reconfirmed for Fall 2027.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- Oakland's direct bachelor's entry is discretionary; UBC still needs a CS-to-ECE course-overlap determination.
- GW, UAlbany, WPI, and McGill publish competitive support routes rather than universal full-cost packages.
- CYBERUS has no published Fall 2027 call; EDISS has renewed funding through 2031 but has not published the Fall 2027 application window or award count.

## Records requiring human judgment

- 8 new routes are conditional, monitor, or excluded and must not be treated as unconditional funded recommendations.
- Stage 4 may evaluate current faculty only for the 9 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- Every conditional route needs its single eligibility or funding gate resolved before application spending; offer-level tuition, fee, insurance, renewal, and summer terms remain material.
- Every retained route still requires offer-level net-cost review; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_17.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_17_verification.csv`
- `data/processed/pass2/stage_03_reentry_17_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
