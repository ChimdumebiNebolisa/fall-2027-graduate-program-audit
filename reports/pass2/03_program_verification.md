# Stage 3 Result

Generated: 2026-09-11T13:57:00.021662+00:00

## Decision

Pass — program structure, eligibility, and funding verification re-entry 16 is complete.

## What changed

All 2,157 Stage 2 candidates now have exactly one controlled retained, conditional, monitor, or excluded status with an evidence-backed reason. The 12 re-entry 16 routes were verified against official program, admissions, funding, fee, and deadline sources. No score or admission recommendation was created.

## Coverage

| Status | All candidates | New routes |
| --- | --- | --- |
| Retained | 48 | 1 |
| Conditional | 103 | 7 |
| Monitor | 379 | 4 |
| Excluded | 1627 | 0 |
| Faculty-review ready | 151 | 8 |

### Stage 2 re-entry 16 routes

| Institution | Program | Status | Eligibility gate | Funding gate | Largest unresolved question |
| --- | --- | --- | --- | --- | --- |
| Florida Atlantic University | [Doctor of Philosophy with Major in Computer Science](https://www.fau.edu/engineering/eecs/graduate/phd/computer-science/) | conditional | resolvable_question | pass | Does FAU permit this international applicant with a U.S. computer science bachelor's but no master's to enter the direct BS-to-PhD route? |
| New Mexico Institute of Mining and Technology | [Doctor of Philosophy in Computer Science](https://www.nmt.edu/academics/compsci/graduate.php) | conditional | pass | resolvable_inquiry | Will NMT issue a renewable 0.5 FTE appointment whose stipend and tuition remission also cover fees, insurance, and summer needs? |
| Southern Illinois University-Carbondale | [Computer Science, Doctor of Philosophy](https://academics.siu.edu/computing-and-technology/computer-science/doctoral/) | conditional | resolvable_question | pass | Will SIU classify this 3.35-GPA bachelor's applicant as exceptional and admit them directly without a master's? |
| Wichita State University | [PhD in Electrical Engineering and Computer Science](https://catalog.wichita.edu/graduate/engineering/electrical-computer-engineering/phd-in-eecs/) | conditional | resolvable_question | pass | Will a CS-track faculty member commit to advise this bachelor's applicant and certify the record as exceptional? |
| Michigan Technological University | [Computer Science, PhD](https://www.mtu.edu/gradschool/programs/degrees/computer-science/) | retained | pass | pass | Will the actual assistantship offer provide renewable academic-year and summer support after fees and insurance? |
| University of Tulsa | [Computer Science, Ph.D.](https://utulsa.edu/programs/computer-science/) | conditional | resolvable_question | pass | Will Tandy confirm direct bachelor's eligibility and the applicant's exact prerequisite fit for the CS PhD? |
| Western University | [Master of Engineering Science (MESc) in Electrical and Computer Engineering](https://www.eng.uwo.ca/graduate/future-students/Graduate-Degree-Programs/electrical-computer.html) | conditional | resolvable_question | pass | Will ECE accept the applicant's computer science bachelor's as similar preparation and identify a fundable supervisor? |
| York University | [MASc in Electrical and Computer Engineering](https://futurestudents.yorku.ca/graduate/programs/electrical-engineering-and-computer-science) | conditional | resolvable_question | pass | Will York treat the applicant's CS bachelor's and senior project as equivalent to the listed engineering preparation? |
| University of Saskatchewan | [Electrical Engineering, Master of Science (M.Sc.) — Thesis](https://grad.usask.ca/programs/electrical-computer-engineering.php) | monitor | resolvable_question | resolvable_inquiry | Can a supervisor confirm both CS-to-ECE eligibility and funding that covers international tuition, fees, insurance, living costs, and summer? |
| Politecnico di Milano | [Master's Degree in Computer Science and Engineering](https://www.polimi.it/en/education/laurea-programmes/programme-detail/computer-science-and-engineering) | monitor | pass | unverified | Can the applicant win a Fall 2027 scholarship whose waiver and allowance cover total tuition and living costs? |
| Universidade do Porto | [Master in Informatics and Computing Engineering](https://fe.up.pt/estudar/meic/?lang=en) | monitor | resolvable_question | unverified | Is there an international-eligible Fall 2027 award that covers tuition and living costs from the first year? |
| University of Minho | [Master in Informatics Engineering](https://www.eng.uminho.pt/en/study/_layouts/15/uminho.portaisuoei.ui/pages/catalogocursodetail.aspx?catid=16&itemid=5482) | monitor | resolvable_question | unverified | Can the applicant complete the bachelor's early enough for a 2027 application round and obtain full English-language, degree-equivalency, and funding terms? |

Retained means an exact research route, formal applicant eligibility, and a credible officially sourced funding route are present. It does not mean admission is likely or that an eventual offer will contain adequate net funding.

Michigan Tech is retained on current official evidence. FAU, NMT, SIU, Wichita State, Tulsa, Western, and York are conditional and positioned only as `Outreach Before Decision`. Saskatchewan, Politecnico di Milano, Porto, and Minho remain monitors because eligibility and/or credible full-cost funding gates remain unresolved.

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
- FAU has conflicting official bachelor's-entry rules; SIU and Wichita publish discretionary bachelor's-entry exceptions.
- Western, York, and Saskatchewan need CS-to-ECE degree-equivalency or supervisor resolution; Porto and Minho retain admission-language or timing questions.
- The Canadian and European awards are partial, competitive, unavailable to this applicant, or unverified for living-cost coverage and are not treated as credible full funding.

## Records requiring human judgment

- 11 new routes remain conditional or monitor and must not be treated as funded recommendations.
- Stage 4 may evaluate current faculty only for the 8 new retained/conditional routes; monitor routes do not pass the faculty-review gate.
- Every conditional route needs its single eligibility or funding gate resolved before application spending; offer-level tuition, fee, insurance, renewal, and summer terms remain material.
- Michigan Tech still requires written offer details; retained is a program gate, not an adequate-net-funding conclusion.

## Files created or modified

- `data/raw/pass2/stage_03_reentry_16.json`
- `data/processed/pass2/program_verification.csv`
- `data/processed/pass2/program_sources.csv`
- `data/processed/pass2/program_exclusions.csv`
- `data/processed/pass2/stage_03_reentry_16_verification.csv`
- `data/processed/pass2/stage_03_reentry_16_sources.csv`
- `data/manifests/pass2/stage_03.json`
- `state/progress.json`

## Recommendation before the next stage

Proceed to Stage 4 only for retained and conditional rows marked faculty-review ready. Keep all monitor rows outside faculty review, and preserve every offer-, transcript-, and deadline-specific unknown until independent evidence resolves it.
