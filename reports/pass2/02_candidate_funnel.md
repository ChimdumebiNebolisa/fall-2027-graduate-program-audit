# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 03 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This fourth bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 03 | After re-entry 04 |
| --- | --- | --- |
| Funnel rows | 2001 | 2013 |
| Advance to Stage 3 | 119 | 131 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 27 |
| Active rows missing exact program URL | documented | 264 |

The round was checked against the cumulative funnel by deterministic program ID. Existing institution records were retained only when the newly discovered degree route was distinct, so the increment does not overstate recall through duplicate programs.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 2 |
| europe | 2 |
| us | 8 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 9 |
| Thesis or research master's | 3 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | University of Rochester | [PhD Program in Computer Science](https://www.cs.rochester.edu/graduate/phd-program.html) | PhD | high | Fall 2027 cycle/admission plausibility/English waiver application/offer-specific funding duration and fees/current faculty supervision |
| us | University of Maryland-Baltimore County | [PhD in Computer Science](https://www.csee.umbc.edu/graduate/computer-science-m-s-ph-d/) | PhD | high | Fall 2027 cycle/prerequisite equivalency/GRE performance/assistantship probability and renewal/current faculty supervision |
| us | University of California-Riverside | [PhD in Computer Science](https://www1.cs.ucr.edu/graduate/programs/computer-science-phd) | PhD | high | Fall 2027 cycle/last-two-year GPA calculation/course equivalency/funding package probability and duration/current faculty supervision |
| us | University of Houston | [PhD in Computer Science](https://www.uh.edu/nsm/computer-science/graduate/phd/index.php) | PhD | high | Fall 2027 cycle/prerequisite mapping/admission calibration/offer-specific stipend and renewal/current faculty supervision |
| us | The University of Texas at Arlington | [Doctoral Degree in Computer Science/Computer Engineering](https://www.uta.edu/academics/schools-colleges/engineering/academics/departments/cse/phd) | PhD | high | Fall 2027 cycle/last-two-year GPA calculation/English waiver or testing/assistantship award and coverage/current faculty supervision |
| us | The University of Texas at San Antonio | [PhD in Computer Science](https://future.utsa.edu/programs/doctoral/computer-science/) | PhD | high | applicant-specific admission calibration/foreign equivalency despite expected U.S. bachelor's/assistantship renewal conditions/fee and living-cost residuals/current faculty supervision |
| us | University of Iowa | [PhD in Computer Science](https://cs.uiowa.edu/graduate/phd-computer-science) | PhD | medium | Fall 2027 cycle/formal entry requirements/English waiver or testing/initial assistantship probability and renewal/current faculty supervision |
| us | Clemson University | [Computer Science PhD](https://www.clemson.edu/cecas/departments/computing/academics/graduates/degrees/phd-cs.html) | PhD | high | Fall 2027 cycle/prerequisite equivalency/English waiver or testing/assistantship probability and net cost/current faculty supervision |
| canada | University of Northern British Columbia | [MSc in Computer Science - Thesis Option](https://www.unbc.ca/calendar/graduate/computer-science-msc-program) | Thesis or research master's | medium | Fall 2027 cycle/specific research fit/supervisor commitment/award or assistantship amount and duration/net international cost |
| canada | University of Manitoba | [PhD in Computer Science](https://umanitoba.ca/graduate-studies/admissions/programs-of-study/computer-science-phd) | PhD | high | rare direct-bachelor's exception/Fall 2027 cycle/degree and grade equivalency/confirmed supervisor/funding source, renewal, and net international cost |
| europe | University of Zurich | [MSc in Informatics - Software Systems](https://www.uzh.ch/en/studies/programs/master/software_systems.html) | Thesis or research master's | high | Fall 2027 cycle/GRE thresholds and timing/curriculum and ECTS mapping/external scholarship viability/thesis supervision fit |
| europe | TU Wien | [Master's Programme Logic and Artificial Intelligence](https://www.tuwien.at/en/studies/studies/master-programmes/informatics/logic-and-artificial-intelligence) | Thesis or research master's | high | Fall 2027 cycle/ECTS and curriculum mapping/supplementary-exam load/scholarship and living-cost viability/thesis supervision fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 299 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| The University of Texas at San Antonio | single_bounded_registry_signal_without_independent_topic_signal | false_negative_corrected | us:ipeds:229027:program:phd:phd-in-computer-science |
| University of Manitoba | outside_bounded_positive_seed_screen | false_negative_corrected | ca:dli:O19091528512:program:phd:phd-in-computer-science |

The University of Texas at San Antonio, and University of Manitoba were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2002 | 120 | 0.192 |
| official_program_or_department_signal | 1913 | 140 | 130 | 0.929 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6926 | 54 | 14 | 0.259 |
| lab_or_center_signal | 70 | 69 | 69 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1852 | 93 | 90 | 0.968 |
| underrepresented_route_search | 1863 | 164 | 79 | 0.982 |

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
| reentry04::bounded_reentry_has_exact_routes | PASS |
| reentry04::reentry_covers_all_regions | PASS |
| reentry04::research_masters_reentry_present | PASS |
| reentry04::doctoral_reentry_present | PASS |
| reentry04::all_candidates_advance_only_to_stage_3 | PASS |
| reentry04::all_candidates_have_exact_official_program_urls | PASS |
| reentry04::all_candidates_have_official_institution_urls | PASS |
| reentry04::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry04::all_candidate_source_ids_resolve | PASS |
| reentry04::all_sources_are_official_https | PASS |
| reentry04::program_ids_unique_after_merge | PASS |
| reentry04::all_reentry_candidates_present_after_merge | PASS |
| reentry04::known_seed_adjacency_retained | PASS |
| reentry04::confirmed_false_negatives_reaudited | PASS |
| reentry04::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 04 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 27 of 27 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2001 rows while the expanded funnel has 2013. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- UCR's desirable last-two-year GPA and UTA's 3.2 last-two-years expectation require an official transcript calculation rather than inference from the cumulative GPA.
- UT San Antonio and Manitoba publish unusually strong funding signals, but offer-specific coverage, renewal, fees, and net living costs still require Stage 3 verification.
- UNBC remains supervisor- and capacity-dependent, while Zurich and TU Wien have no established living-cost funding path for this applicant.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the UCR and UTA recent-coursework GPA calculations, whether the UT San Antonio and Manitoba packages clear the full net-cost gate, and whether UNBC, Zurich, or TU Wien has a viable supervision and funding path.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_04.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_04_candidates.csv`
- `data/processed/pass2/stage_02_reentry_04_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
