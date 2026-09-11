# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 09 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 09 | After re-entry 10 |
| --- | --- | --- |
| Funnel rows | 2073 | 2085 |
| Advance to Stage 3 | 191 | 203 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 24 |
| Active rows missing exact program URL | documented | 264 |

The round was checked against the cumulative funnel by deterministic program ID. Existing institution records were retained only when the newly discovered degree route was distinct, so the increment does not overstate recall through duplicate programs.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 3 |
| europe | 4 |
| us | 5 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 6 |
| Thesis or research master's | 6 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | University of Oregon | [PhD in Computer Science](https://scds.uoregon.edu/cs/graduate-programs/cs-phd) | PhD | high | Fall 2027 cycle/transcript and prerequisite mapping/English evidence/assistantship award and duration/fees and insurance/current supervisor capacity |
| us | University of Georgia | [Doctor of Philosophy in Computer Science](https://www.cs.uga.edu/doctor-philosophy-computer-science) | PhD | high | Fall 2027 cycle/transcript preparation/English evidence/assistantship selection/tuition, fees, and insurance/current supervisor capacity |
| us | Georgia State University | [Computer Science PhD](https://graduate.gsu.edu/program/computer-science-phd/) | PhD | high | Fall 2027 cycle/foundation-course assessment/English evidence/assistantship selection and renewal/fee and insurance coverage/current supervisor capacity |
| us | University of South Carolina-Columbia | [Doctor of Philosophy in Computer Science](https://cse.sc.edu/graduate/phd) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/English evidence/assistantship award and renewal/net tuition and fees/current supervisor capacity |
| us | University of Nevada-Reno | [Ph.D. in Computer Science and Engineering](https://www.unr.edu/cse/graduate-program) | PhD | high | Fall 2027 cycle/direct-entry transcript standard/English evidence/assistantship sponsorship and renewal/remaining fees/current supervisor capacity |
| canada | University of Prince Edward Island | [Master of Science in Mathematical and Computational Sciences](https://www.upei.ca/programs/master-science-mathematical-and-computational-sciences) | Thesis or research master's | high | Fall 2027 cycle/four-year degree equivalency/course and English requirements/willing supervisor/funding package and international tuition/net cost |
| canada | University of Winnipeg | [MSc in Applied Computer Science and Society — Thesis-Based](https://acs.uwinnipeg.ca/graduate_thesis_based) | Thesis or research master's | high | Fall 2027 cycle/four-year degree equivalency/course and English requirements/willing supervisor/scholarship selection/international tuition and net cost |
| canada | Queen’s University | [PhD in Computing](https://www.cs.queensu.ca/graduate/phd/) | PhD | high | direct-entry eligibility without MSc/Fall 2027 cycle/English evidence/supervisor alignment/funding renewal and net cost/current supervisor capacity |
| europe | Uppsala University | [Master's Programme in Computer Science](https://www.uu.se/en/study/programme/masters-programme-computer-science) | Thesis or research master's | high | Fall 2027 cycle/90-credit CS and 30-credit mathematics mapping/English evidence/tuition liability/scholarship selection/living-cost plan |
| europe | Lund University | [Master's Programme in Machine Learning, Systems and Control](https://www.lunduniversity.lu.se/lubas/i-uoh-lu-TAMSR) | Thesis or research master's | high | Fall 2027 cycle/prerequisite course mapping/English evidence/tuition liability/scholarship selection/living-cost plan |
| europe | University of Luxembourg | [Master in Information and Computer Sciences](https://www.uni.lu/fstm-en/study-programs/master-in-information-and-computer-sciences/) | Thesis or research master's | high | Fall 2027 cycle/bachelor and course equivalency/English evidence/scholarship selection/tuition and living costs/research-supervisor fit |
| europe | Technical University of Denmark | [MSc Eng in Computer Science and Engineering](https://www.dtu.dk/english/education/graduate/msc-programmes/computer-science-and-engineering) | Thesis or research master's | high | Fall 2027 cycle/75-ECTS prerequisite mapping/English evidence/tuition-waiver selection/living-cost plan/thesis-supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 371 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Prince Edward Island | outside_bounded_positive_seed_screen | false_negative_corrected | ca:dli:O19220071452:program:thesis-or-research-master-s:master-of-science-in-mathematical-and-computational-sciences |
| University of Luxembourg | doctoral_route_recorded_research_masters_route_missed | false_negative_corrected | ror:036x5ad56:program:thesis-or-research-master-s:master-in-information-and-computer-sciences |

University of Prince Edward Island and University of Luxembourg were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2068 | 186 | 0.218 |
| official_program_or_department_signal | 2009 | 212 | 202 | 0.953 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6928 | 59 | 19 | 0.322 |
| lab_or_center_signal | 78 | 77 | 77 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1902 | 149 | 146 | 0.980 |
| underrepresented_route_search | 1871 | 206 | 121 | 0.985 |

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
| reentry10::bounded_reentry_has_exact_routes | PASS |
| reentry10::reentry_covers_all_regions | PASS |
| reentry10::research_masters_reentry_present | PASS |
| reentry10::doctoral_reentry_present | PASS |
| reentry10::all_candidates_advance_only_to_stage_3 | PASS |
| reentry10::all_candidates_have_exact_official_program_urls | PASS |
| reentry10::all_candidates_have_official_institution_urls | PASS |
| reentry10::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry10::all_candidate_source_ids_resolve | PASS |
| reentry10::all_sources_are_official_https | PASS |
| reentry10::program_ids_unique_after_merge | PASS |
| reentry10::all_reentry_routes_are_net_new | PASS |
| reentry10::all_reentry_candidates_present_after_merge | PASS |
| reentry10::known_seed_adjacency_retained | PASS |
| reentry10::confirmed_false_negatives_reaudited | PASS |
| reentry10::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 10 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 21 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2073 rows while the expanded funnel has 2085. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Oregon, Georgia, Georgia State, South Carolina, and Nevada-Reno require transcript-level entry and offer-level assistantship review; the recorded mechanisms are competitive, limited, or appointment-dependent.
- UPEI and Winnipeg require degree-equivalency, willing-supervisor, international-package, and net-cost verification; Queen's normally requires an MSc, making direct PhD eligibility unresolved.
- Uppsala, Lund, Luxembourg, and DTU require course and language mapping plus a viable tuition and living-cost plan; their scholarships or waivers are limited or highly competitive.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the U.S. transcript and assistantship conditions, whether the UPEI and Winnipeg MSc routes clear supervisor and international net-cost gates, whether Queen's permits the applicant's direct doctoral entry, and whether the European routes combine transcript equivalency with viable living-cost funding.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_10.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_10_candidates.csv`
- `data/processed/pass2/stage_02_reentry_10_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
