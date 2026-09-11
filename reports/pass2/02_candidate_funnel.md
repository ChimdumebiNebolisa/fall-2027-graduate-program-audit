# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 10 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 10 | After re-entry 11 |
| --- | --- | --- |
| Funnel rows | 2085 | 2097 |
| Advance to Stage 3 | 203 | 215 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 24 |
| Active rows missing exact program URL | documented | 264 |

The round was checked against the cumulative funnel by deterministic program ID. Existing institution records were retained only when the newly discovered degree route was distinct, so the increment does not overstate recall through duplicate programs.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 3 |
| europe | 3 |
| us | 6 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 6 |
| Thesis or research master's | 6 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | Binghamton University | [PhD in Computer Science](https://www.binghamton.edu/apps/academics/program/gd/computer-science) | PhD | high | Fall 2027 cycle/direct-entry and degree-preparation rule/transcript and prerequisite mapping/English evidence/assistantship award and duration/fees and insurance/current supervisor capacity |
| us | University of Louisiana at Lafayette | [PhD in Applied Computing and Information Sciences](https://louisiana.edu/graduateschool/majors-minors/applied-computing-and-information-sciences-phd) | PhD | high | Fall 2027 cycle/bachelor's preparation and transcript mapping/English evidence/fellowship or assistantship selection/support duration and summer coverage/remaining fees and insurance/current supervisor capacity |
| us | Montana State University | [Computer Science PhD](https://www.cs.montana.edu/phd-degree.html) | PhD | high | Fall 2027 cycle/3.30 recent-coursework GPA calculation/related-degree and prerequisite mapping/English evidence/assistantship offer and renewal/fees, insurance, and summer coverage/current supervisor capacity |
| us | Tennessee Technological University | [Computer Science PhD](https://www.tntech.edu/engineering/programs/csc/ph.d-program.php) | PhD | high | Fall 2027 cycle/BS-to-PhD course and GPA mapping/English evidence/assistantship selection and renewal/summer funding/remaining fees and insurance/current supervisor capacity |
| us | University of Memphis | [PhD in Computer Science](https://www.memphis.edu/cs/programs/phd_computer_science.php) | PhD | high | Fall 2027 cycle/four-year degree and prerequisite mapping/GPA interpretation/English evidence/assistantship offer and duration/tuition, fees, insurance, and summer support/current supervisor capacity |
| us | University of Wyoming | [PhD in Computer Science](https://www.uwyo.edu/uw/degree-programs/computer-science-ms-phd.html) | PhD | high | Fall 2027 cycle/conflicting direct-entry language/degree and course mapping/English evidence/assistantship appointment and duration/fees, insurance, and summer support/current supervisor capacity |
| canada | Trent University | [MSc in Applied Modelling and Quantitative Methods — Thesis Stream](https://www.trentu.ca/graduatestudies/program/applied-modelling-quantitative-methods-ma-or-msc/thesis-stream) | Thesis or research master's | high | Fall 2027 cycle/honours-degree equivalency/B+ and course mapping/English evidence/willing supervisor/funding eligibility and duration/international tuition and net cost |
| canada | University of Waterloo | [MASc in Systems Design Engineering](https://uwaterloo.ca/future-graduate-students/programs/by-faculty/engineering/systems-design-engineering-master-applied-science-masc) | Thesis or research master's | high | Fall 2027 cycle/engineering-degree equivalency/mathematics and GPA mapping/English evidence/confirmed supervisor/funding composition and deductions/international tuition and net cost |
| canada | Concordia University | [Cybersecurity Engineering (MASc)](https://www.concordia.ca/academics/graduate/cybersecurity-engineering-masc.html) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite mapping/GPA interpretation/English evidence/willing research advisor/funding amount and duration/international tuition and net cost |
| europe | University of Pisa | [Master's Degree in Computer Science](https://www.unipi.it/en/education/courses/master-degree/computer-science-wif-lm-en/) | Thesis or research master's | high | Fall 2027 cycle/foreign-degree and 72-credit mapping/B2 English evidence/pre-enrolment and visa documents/DSU income-document eligibility/scholarship selection and renewal/residual living costs |
| europe | University of Florence | [MSc in Software: Science and Technology](https://www.unifi.it/en/study-us/degree-programs/second-cycle-degree/software-science-and-technology) | Thesis or research master's | high | Fall 2027 cycle/foreign-degree and curriculum mapping/English evidence/non-EU application and visa process/DSU or university scholarship eligibility/award benefits and renewal/residual tuition and living costs |
| europe | Università di Camerino | [Master of Science in Computer Science](https://sst.unicam.it/corsi/computer-science) | Thesis or research master's | high | Fall 2027 cycle/bachelor's and course equivalency/B2 English evidence/CIMEA and visa documentation/UNICAM or ERDIS selection/award renewal/residual tuition and living costs/current thesis-supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 383 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Louisiana at Lafayette | catalog_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:160658:program:phd:phd-in-applied-computing-and-information-sciences |
| University of Florence | outside_bounded_positive_seed_screen | false_negative_corrected | ror:04jr1s763:program:thesis-or-research-master-s:msc-in-software-science-and-technology |

University of Louisiana at Lafayette and University of Florence were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2077 | 195 | 0.221 |
| official_program_or_department_signal | 2021 | 224 | 214 | 0.955 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6929 | 60 | 20 | 0.333 |
| lab_or_center_signal | 79 | 79 | 79 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1912 | 159 | 156 | 0.981 |
| underrepresented_route_search | 1871 | 211 | 126 | 0.986 |

## Validation performed

| Assertion | Result |
| --- | --- |
| baseline::all_regions_represented | PASS |
| baseline::priority_degree_routes_represented | PASS |
| baseline::terraprobe_adjacent_seed_recovered | PASS |
| baseline::evidex_adjacent_seed_recovered | PASS |
| baseline::exclusion_sample_all_regions | PASS |
| baseline::exclusion_sample_all_major_strata | PASS |
| baseline::exclusion_sample_complete | PASS |
| baseline::required_candidate_fields_complete | PASS |
| baseline::missing_program_urls_explicitly_flagged | PASS |
| baseline::screened_out_rows_have_reasons | PASS |
| baseline::all_discovery_paths_reported | PASS |
| baseline::non_educational_contamination_reported | PASS |
| baseline::affiliation_corrections_reported | PASS |
| baseline::no_global_top_n_cutoff | PASS |
| baseline::no_university_scoring_fields | PASS |
| baseline::false_negative_saturation_or_limitation_documented | PASS |
| reentry11::bounded_reentry_has_exact_routes | PASS |
| reentry11::reentry_covers_all_regions | PASS |
| reentry11::research_masters_reentry_present | PASS |
| reentry11::doctoral_reentry_present | PASS |
| reentry11::all_candidates_advance_only_to_stage_3 | PASS |
| reentry11::all_candidates_have_exact_official_program_urls | PASS |
| reentry11::all_candidates_have_official_institution_urls | PASS |
| reentry11::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry11::all_candidate_source_ids_resolve | PASS |
| reentry11::all_sources_are_official_https | PASS |
| reentry11::program_ids_unique_after_merge | PASS |
| reentry11::all_reentry_routes_are_net_new | PASS |
| reentry11::all_reentry_candidates_present_after_merge | PASS |
| reentry11::known_seed_adjacency_retained | PASS |
| reentry11::confirmed_false_negatives_reaudited | PASS |
| reentry11::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 11 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2085 rows while the expanded funnel has 2097. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Binghamton, Louisiana-Lafayette, Montana State, Tennessee Tech, Memphis, and Wyoming require transcript-level entry and offer-level assistantship review; Wyoming's direct-entry language is internally inconsistent and every recorded support mechanism remains preliminary.
- Trent, Waterloo, and Concordia require degree-equivalency, willing-supervisor, international-package, and net-cost verification; published funding prevalence or minimums are not applicant-specific awards.
- Pisa, Florence, and Camerino require course, qualification, language, and visa-document mapping plus a viable tuition and living-cost plan; DSU, ERDIS, and university awards are selective or annual.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the six U.S. transcript and assistantship conditions, whether the Trent, Waterloo, and Concordia research-master routes clear supervisor and international net-cost gates, how Wyoming's conflicting direct-entry language resolves, and whether the three Italian routes combine qualification equivalency with viable scholarship and living-cost coverage.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_11.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_11_candidates.csv`
- `data/processed/pass2/stage_02_reentry_11_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
