# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 02 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This third bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 02 | After re-entry 03 |
| --- | --- | --- |
| Funnel rows | 1989 | 2001 |
| Advance to Stage 3 | 107 | 119 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 31 |
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
| us | Colorado State University-Fort Collins | [Computer Science PhD](https://graduateschool.colostate.edu/programs/computer-science-phd/) | PhD | high | Fall 2027 cycle/transcript and prerequisite equivalency/admission plausibility/individual funding terms/current faculty supervision |
| us | University of Central Florida | [Computer Science PhD](https://www.ucf.edu/degree/computer-science-phd/) | PhD | high | Fall 2027 cycle/course articulation/GRE status for the target cycle/funding probability and duration/current faculty supervision |
| us | University of Illinois Chicago | [PhD in Computer Science](https://catalog.uic.edu/gcat/colleges-schools/engineering/cs/phd/) | PhD | high | 3.50 final-60-hour GPA application/Fall 2027 cycle/degree and prerequisite equivalency/individual funding terms/current faculty supervision |
| us | University of Kansas | [Doctor of Philosophy in Computer Science](https://degrees.ku.edu/graduate/doctoral/computer-science/) | PhD | high | Fall 2027 cycle/international credential and English rules/prerequisite equivalency/assistantship likelihood and duration/current faculty supervision |
| us | University of Kentucky | [Doctoral Degree in Computer Science](https://academics.uky.edu/programs/doctoral/computer-science) | PhD | high | direct bachelor's entry/Fall 2027 cycle/GPA and course equivalency/offer-specific assistantship terms/current faculty supervision |
| us | Stevens Institute of Technology | [PhD in Computer Science](https://www.stevens.edu/program/computer-science-doctoral-program) | PhD | high | bachelor's-only competitiveness/Fall 2027 cycle/international credential review/funding coverage and duration/current faculty supervision |
| us | University of New Mexico-Main Campus | [PhD in Computer Science](https://www.cs.unm.edu/programs-and-degrees/ph.d./index.html) | PhD | high | direct bachelor's entry/Fall 2027 cycle/course preparation/assistantship likelihood and duration/current faculty supervision |
| us | The University of Tennessee-Knoxville | [Computer Science PhD](https://tickle.utk.edu/academics/graduate-programs/computer-science-phd/) | PhD | high | direct bachelor's entry/Fall 2027 cycle/international and GPA requirements/assistantship availability and duration/current faculty supervision |
| canada | Dalhousie University | [Master of Computer Science](https://www.dal.ca/faculty/computerscience/graduate-programs.html) | Thesis or research master's | high | Fall 2027 cycle/international degree equivalency/technical-course GPA interpretation/supervisor alignment/individual funding amount and net cost |
| canada | University of New Brunswick | [PhD in Computer Science](https://www.unb.ca/fredericton/cs/grad/phd/index.html) | PhD | high | research-master's prerequisite and exception path/Fall 2027 cycle/confirmed supervisor/international credential equivalency/individual funding amount and duration |
| europe | University of Bonn | [Computer Science MSc](https://www.uni-bonn.de/en/studying/degree-programs/degree-programs-a-z/computer-science-msc) | Thesis or research master's | high | ECTS prerequisite mapping/prior research-thesis equivalency/C1 English proof/Fall 2027 cycle/scholarship and living-cost viability/thesis supervision fit |
| europe | Aalto University | [Computer, Communication and Information Sciences MSc - Software Engineering](https://www.aalto.fi/en/study-options/software-engineering-master-of-science-technology) | Thesis or research master's | high | 2027 academic ranking/course and degree equivalency/English proof/tuition-waiver competitiveness/living-cost funding/thesis supervision fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 287 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Illinois Chicago | single_bounded_registry_signal_without_independent_topic_signal | false_negative_corrected | us:ipeds:145600:program:phd:phd-in-computer-science |
| University of Bonn | outside_bounded_positive_seed_screen | false_negative_corrected | ror:041nas322:program:thesis-or-research-master-s:computer-science-msc |

University of Illinois Chicago, and University of Bonn were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 1990 | 108 | 0.187 |
| official_program_or_department_signal | 1896 | 128 | 118 | 0.922 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6926 | 54 | 14 | 0.259 |
| lab_or_center_signal | 70 | 69 | 69 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1848 | 89 | 86 | 0.966 |
| underrepresented_route_search | 1857 | 152 | 67 | 0.980 |

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
| reentry03::bounded_reentry_has_exact_routes | PASS |
| reentry03::reentry_covers_all_regions | PASS |
| reentry03::research_masters_reentry_present | PASS |
| reentry03::doctoral_reentry_present | PASS |
| reentry03::all_candidates_advance_only_to_stage_3 | PASS |
| reentry03::all_candidates_have_exact_official_program_urls | PASS |
| reentry03::all_candidates_have_official_institution_urls | PASS |
| reentry03::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry03::all_candidate_source_ids_resolve | PASS |
| reentry03::all_sources_are_official_https | PASS |
| reentry03::program_ids_unique_after_merge | PASS |
| reentry03::all_reentry_candidates_present_after_merge | PASS |
| reentry03::known_seed_adjacency_retained | PASS |
| reentry03::confirmed_false_negatives_reaudited | PASS |
| reentry03::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 03 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 31 of 31 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 1989 rows while the expanded funnel has 2001. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- UIC's published 3.50 final-60-hour GPA criterion is an explicit preliminary eligibility concern against the applicant's current approximately 3.35 cumulative GPA.
- UNB normally requires a research-based master's with first-class standing for PhD entry; the bachelor's-only route is therefore an explicit likely ineligibility pending Stage 3.
- Aalto's scholarship is highly competitive and tuition-only, while Bonn discovery found no program-level living-cost support; neither route is currently financially viable.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are UIC's final-60-hour GPA rule, UNB's research-master's prerequisite, and the remaining costs after Aalto or Bonn funding constraints.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_03.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_03_candidates.csv`
- `data/processed/pass2/stage_02_reentry_03_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
