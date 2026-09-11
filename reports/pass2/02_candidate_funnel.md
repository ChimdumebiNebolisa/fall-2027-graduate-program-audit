# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 11 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 11 | After re-entry 12 |
| --- | --- | --- |
| Funnel rows | 2097 | 2109 |
| Advance to Stage 3 | 215 | 227 |
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
| us | New Mexico State University-Main Campus | [Computer Science (Ph.D.)](https://nmsu.edu/degree-programs/graduate/doctoral/computer-science.html) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GPA interpretation/English evidence/assistantship selection and duration/fees and insurance/current supervisor capacity |
| us | University of Idaho | [Computer Science Ph.D.](https://www.uidaho.edu/academics/degree-finder/computer-sci-phd) | PhD | high | Fall 2027 cycle/degree and course mapping/GPA threshold/English evidence/funding appointment and renewal/fees and insurance/current advisor capacity |
| us | Kansas State University | [Doctor of Philosophy in Computer Science](https://www.cs.ksu.edu/academics/graduate/phd/) | PhD | high | Fall 2027 cycle/bachelor's and master's credit mapping/English evidence/advisor acceptance/assistantship availability and duration/tuition and fee treatment/current lab capacity |
| us | Oklahoma State University-Main Campus | [Doctor of Philosophy in Computer Science](https://cas.okstate.edu/computer_science/graduate/phd_cs) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GPA and English evidence/assistantship offer and renewal/tuition, fees, insurance, and summer support/current advisor capacity |
| us | West Virginia University | [Ph.D. in Computer Science and Information Science](https://lcsee.statler.wvu.edu/graduate) | PhD | high | Fall 2027 cycle/degree and GPA mapping/English and spoken-English evidence/advisor and concentration fit/GTA or GRA offer and renewal/college tuition, fees, insurance, and summer support |
| us | Louisiana State University and Agricultural & Mechanical College | [Ph.D. in Computer Science and Engineering](https://www.lsu.edu/eng/cse/programs/graduate_program/graduate_phd.php) | PhD | high | Fall 2027 cycle/degree and course mapping/GPA and English evidence/advisor capacity/assistantship offer and annual renewal/tuition, fees, insurance, and summer coverage |
| canada | University of Lethbridge | [MSc in Computer Science (Thesis)](https://www.ulethbridge.ca/future-student/graduate-studies/master-science/computer-science) | Thesis or research master's | high | Fall 2027 cycle/four-year degree equivalency/upper-level course and GPA mapping/English evidence/secured supervisor/funding amount and duration/international tuition and net cost |
| canada | Brock University | [Computer Science MSc — Thesis Stream](https://brocku.ca/programs/graduate/msc-cosc/) | Thesis or research master's | high | Fall 2027 cycle/four-year degree and course mapping/high-B interpretation/English evidence/potential supervisor/current funding amount and guarantee/international tuition, tax, and net cost |
| canada | Lakehead University | [Master of Science in Computer Science — Thesis Route](https://www.lakeheadu.ca/programs/graduate/programs/masters/computer-science) | Thesis or research master's | high | Fall 2027 cycle/honours-degree equivalency/B standing and prerequisite mapping/English evidence/potential supervisor/assistantship or award amount and duration/international tuition and net cost |
| europe | Blekinge Institute of Technology | [Master's Programme in Software Engineering, 120 credits](https://www.bth.se/english/education/programmes/masters-programme-in-software-engineering-120-credits) | Thesis or research master's | high | Fall 2027 cycle/degree and ECTS subject mapping/mathematics and software-engineering prerequisites/English evidence/scholarship selection and percentage/remaining tuition and living costs/thesis-group fit |
| europe | Karlstad University | [Master in Computer Science](https://www.kau.se/en/cs/education/programmes-and-courses/programmes/master-computer-science) | Thesis or research master's | high | Fall 2027 cycle/degree and 90-ECTS mapping/named prerequisite equivalencies/English evidence/scholarship competitiveness and renewal/remaining tuition and living costs/thesis-supervisor fit |
| europe | Linköping University | [Computer Science, Master's Programme, 120 credits](https://liu.se/en/education/program/6mics) | Thesis or research master's | high | Fall 2027 cycle/bachelor's and computing-course equivalency/English evidence/selection competitiveness/scholarship academic threshold and award/remaining tuition and living costs/thesis-supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 395 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Idaho | catalog_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:142285:program:phd:computer-science-ph-d |
| Blekinge Institute of Technology | outside_bounded_positive_seed_screen | false_negative_corrected | ror:0093a8w51:program:thesis-or-research-master-s:master-s-programme-in-software-engineering-120-credits |

University of Idaho and Blekinge Institute of Technology were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2089 | 207 | 0.225 |
| official_program_or_department_signal | 2033 | 236 | 226 | 0.958 |
| recent_paper_signal | 1647 | 905 | 74 | 0.361 |
| current_faculty_topic_signal | 6930 | 61 | 21 | 0.344 |
| lab_or_center_signal | 82 | 82 | 82 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1919 | 166 | 163 | 0.982 |
| underrepresented_route_search | 1871 | 218 | 133 | 0.986 |

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
| reentry12::bounded_reentry_has_exact_routes | PASS |
| reentry12::reentry_covers_all_regions | PASS |
| reentry12::research_masters_reentry_present | PASS |
| reentry12::doctoral_reentry_present | PASS |
| reentry12::all_candidates_advance_only_to_stage_3 | PASS |
| reentry12::all_candidates_have_exact_official_program_urls | PASS |
| reentry12::all_candidates_have_official_institution_urls | PASS |
| reentry12::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry12::all_candidate_source_ids_resolve | PASS |
| reentry12::all_sources_are_official_https | PASS |
| reentry12::program_ids_unique_after_merge | PASS |
| reentry12::all_reentry_routes_are_net_new | PASS |
| reentry12::all_reentry_candidates_present_after_merge | PASS |
| reentry12::known_seed_adjacency_retained | PASS |
| reentry12::confirmed_false_negatives_reaudited | PASS |
| reentry12::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 12 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 18 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2097 rows while the expanded funnel has 2109. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- The six current U.S. doctoral routes require transcript-level entry, current-advisor capacity, and offer-level assistantship review; every recorded support mechanism remains preliminary.
- The three current Canadian thesis routes require degree and course equivalency, willing-supervisor, current international-package, and net-cost verification.
- The three current Swedish routes require ECTS and English mapping plus a viable tuition and living-cost plan; every recorded institutional scholarship is selective and partial.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the six U.S. transcript and assistantship conditions, whether the three Canadian thesis routes clear supervisor and international net-cost gates, and whether the three Swedish routes combine qualification equivalency with a viable scholarship and living-cost plan.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_12.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_12_candidates.csv`
- `data/processed/pass2/stage_02_reentry_12_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
