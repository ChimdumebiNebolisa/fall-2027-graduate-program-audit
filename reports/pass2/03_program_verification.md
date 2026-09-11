# Stage 3 Result

Generated: 2026-09-11T16:01:11.828633+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 18 is complete.

## What changed

All 2,181 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 18 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 54 | 2 |
| Conditional | 112 | 4 |
| Monitor | 387 | 6 |
| Excluded | 1628 | 0 |
| Faculty-review ready | 166 | 6 |

### Stage 2 re-entry 18 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| Arizona State University Campus Immersion | [Computer Science, PhD](https://degrees.asu.edu/masters-phd/major/ASU00/ESCOMSCPHD/computer-science-phd/) | monitor | resolvable_question | unverified | Does the official transcript satisfy the 3.50 last-60-hour route, and would admission include a complete written multi-year funding offer? |
| Portland State University | [Doctoral Degree in Computer Science (Ph.D.)](https://web.cs.pdx.edu/phd-doctoral-degree-in-cs/) | conditional | pass | resolvable_inquiry | Will a Fall 2027 admission offer include renewable support after the first year and adequate insurance and summer coverage? |
| Rensselaer Polytechnic Institute | [Ph.D. in Computer Science](https://compsci.rpi.edu/programs/phd-computer-science) | retained | pass | pass | Will the individual Fall 2027 admission offer confirm the department's duration guarantee and specify fees, insurance, and renewal conditions? |
| Southern Methodist University | [Ph.D. in Computer Science](https://www.smu.edu/lyle/departments/cs/doctoral-programs) | conditional | pass | resolvable_inquiry | Does the Computer Science PhD normally fund international admits with a renewable full package, and what is the Fall 2027 deadline? |
| Texas A&M University-College Station | [Doctor of Philosophy in Computer Science](https://engineering.tamu.edu/cse/academics/degrees/graduate/phd-cs.html) | conditional | pass | resolvable_inquiry | Would a Fall 2027 offer include an assistantship covering nonresident tuition plus an adequate stipend and twelve-month support? |
| Howard University | [Computer Science (Ph.D.)](https://gs.howard.edu/index.php/computer-science-phd) | conditional | pass | resolvable_inquiry | How many Computer Science Fall 2027 admits receive renewable tuition, stipend, insurance, and summer support? |
| Simon Fraser University | [Master of Applied Science in Engineering Science](https://www.sfu.ca/fas/study/future-graduates/programs/master-applied-science.html) | retained | pass | pass | What minimum net amount and tuition offset will a willing supervisor commit for the full two-year international MASc? |
| Concordia University | [Electrical and Computer Engineering (MASc)](https://www.concordia.ca/academics/graduate/electrical-engineering-masc.html) | monitor | resolvable_question | resolvable_inquiry | Will ECE accept the applicant's CS degree as equivalent and issue a two-year package adequate after international tuition and fees? |
| Ontario Tech University | [Electrical and Computer Engineering (MASc)](https://gradstudies.ontariotechu.ca/future_students/programs/masters_programs/electrical_and_computer_engineering/index.php) | monitor | resolvable_question | resolvable_inquiry | Will the program accept a CS bachelor's as equivalent engineering preparation and guarantee a sufficient two-year international package? |
| Lappeenranta-Lahti University of Technology | [Erasmus Mundus Joint Master's Programme Software Engineers for Green Deal (SE4GD+)](https://www.lut.fi/en/studies/tekniikka/erasmus-mundus-masters-programme-software-engineers-green-deal) | monitor | resolvable_question | unverified | Will SE4GD+ open a funded Fall 2027 cohort with a full Erasmus Mundus scholarship available to this applicant? |
| Saarland University | [Computer Science (M.Sc.)](https://www.uni-saarland.de/en/study/programmes/master/informatics.html) | monitor | resolvable_question | unverified | Will the applicant satisfy the exact C1 and subject-credit review and secure enough living-cost funding for the full degree? |
| Chalmers University of Technology | [Software Engineering, MSc](https://www.chalmers.se/en/education/find-masters-programme/software-engineering-msc/) | monitor | resolvable_question | unverified | Does the transcript satisfy every prerequisite bucket, and can a scholarship cover enough tuition and living cost to make the route viable? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

RPI and Simon Fraser Engineering Science are retained on current official evidence. Portland State, SMU, Texas A&M, and Howard are conditional and positioned only as `Outreach Before Decision`. ASU, Concordia ECE, Ontario Tech ECE, LUT SE4GD+, Saarland, and Chalmers remain monitors. No current-round route was excluded.

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

- Current-round official URL retrieval: 24 of 24 returned HTTP 200.
- Stage-specific tests: 25 passed.
- Full suite boundary: 149 passed and 3 expected downstream coverage failures in Stages 4 and 5.

## Material uncertainties or conflicts

- ASU, Portland State, RPI, SMU, Texas A&M, Howard, Simon Fraser, Concordia, Ontario Tech, LUT, and Saarland still rely partly or wholly on recurring or latest-cycle dates that must be reconfirmed for Fall 2027.
- Simultaneous-application and separate-fee rules remain unverified wherever the official source did not publish an exact rule.
- Offer-specific stipend, mandatory-fee, health-insurance, and summer coverage remain explicit unknowns wherever official pages did not publish them.
- ASU's last-60-credit GPA rule needs a transcript calculation; Concordia and Ontario Tech still need formal degree-equivalency review.
- Portland State, SMU, Texas A&M, Howard, Concordia, and Ontario Tech publish competitive support routes rather than universal full-cost packages.
- LUT SE4GD+ has no published Fall 2027 call or award terms; Saarland and Chalmers do not publish guaranteed living support.

## Records requiring human judgment

- 10 new routes are conditional, monitor, or excluded and must not be treated as unconditional funded recommendations.
- Stage 4 may evaluate current faculty only for the 6 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- Every conditional route needs its single eligibility or funding gate resolved before application spending; offer-level tuition, fee, insurance, renewal, and summer terms remain material.
- Every retained route still requires offer-level net-cost review; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_18.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_18_verification.csv`
- `data/processed/pass2/stage_03_reentry_18_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
