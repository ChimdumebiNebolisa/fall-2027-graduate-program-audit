# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 08 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 08 | After re-entry 09 |
| --- | --- | --- |
| Funnel rows | 2061 | 2073 |
| Advance to Stage 3 | 179 | 191 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 25 |
| Active rows missing exact program URL | documented | 264 |

The round was checked against the cumulative funnel by deterministic program ID. Existing institution records were retained only when the newly discovered degree route was distinct, so the increment does not overstate recall through duplicate programs.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 1 |
| europe | 4 |
| us | 7 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 7 |
| Thesis or research master's | 5 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | Emory University | [PhD in Computer Science and Informatics](https://computerscience.emory.edu/graduate-phd/index.html) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/support duration and renewal/fees and benefits/current supervisor capacity |
| us | Northwestern University | [PhD in Computer Science](https://www.mccormick.northwestern.edu/computer-science/academics/graduate/phd/) | PhD | high | Fall 2027 cycle/academic preparation and English evidence/five-year guarantee conditions/summer and fee coverage/advisor matching/current supervisor capacity |
| us | University of Pittsburgh-Pittsburgh Campus | [PhD in Computer Science](https://intranet.cs.pitt.edu/grad/) | PhD | medium | Fall 2027 cycle/degree preparation and English evidence/first-two-year support terms/later advisor funding/fees and insurance/current supervisor capacity |
| us | Brandeis University | [Computer Science PhD](https://www.brandeis.edu/computer-science/_pdfs/computer-science-phd-handbook.pdf) | PhD | medium | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/program-specific five-year package/advisor consent and continuation/fees and net cost |
| us | Michigan State University | [Computer Science PhD](https://engineering.msu.edu/academics/majors-degrees/computer-science-phd) | PhD | high | Fall 2027 cycle/background-course mapping/English waiver or evidence/assistantship selection/tuition, fees, and insurance/current supervisor capacity |
| us | Syracuse University | [Doctor of Philosophy in Computer/Information Science and Engineering](https://ecs.syracuse.edu/academics/electrical-engineering-and-computer-science/programs/computer-information-science-engineering-doctoral-program) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/fellowship or assistantship selection/tuition and fee coverage/current supervisor capacity |
| us | Johns Hopkins University | [PhD in Computer Science](https://www.cs.jhu.edu/academic-programs/graduate-studies/phd-program/) | PhD | high | Fall 2027 cycle/degree preparation and English evidence/support duration/good-standing and advisor conditions/fees and insurance/current supervisor capacity |
| canada | St. Francis Xavier University | [Master of Science in Computer Science](https://www.stfx.ca/programs-courses/programs/master-science-computer-science) | Thesis or research master's | high | Fall 2027 cycle/degree and course equivalency/English evidence/willing supervisor/international funding package/fees and living-cost shortfall |
| europe | KTH Royal Institute of Technology | [MSc Computer Science](https://www.kth.se/en/studies/master/computer-science) | Thesis or research master's | high | transcript-to-ECTS prerequisite mapping/English evidence/2027 selection/scholarship rank and award/tuition liability/living-cost funding |
| europe | University of Helsinki | [Master's Programme in Computer Science](https://www.helsinki.fi/en/degree-programmes/computer-science-masters-programme) | Thesis or research master's | high | 2027 application call/degree and subject equivalency/English evidence/tuition-waiver selection/remaining tuition/living-cost funding |
| europe | University of Copenhagen | [MSc in Computer Science](https://www.ku.dk/studies/masters/computer-science) | Thesis or research master's | high | 2027 application cycle/degree and course equivalency/English evidence/admission selection/government scholarship award and value/remaining tuition and living costs |
| europe | University of Tartu | [Master's in Computer Science](https://ut.ee/en/curriculum/computer-science) | Thesis or research master's | high | Fall 2027 cycle/degree and computing-background equivalency/English evidence/tuition reduction or scholarship/DIGILINK selection/remaining tuition and living costs |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 359 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| St. Francis Xavier University | outside_bounded_positive_seed_screen | false_negative_corrected | ca:dli:O19391556899:program:thesis-or-research-master-s:master-of-science-in-computer-science |
| KTH Royal Institute of Technology | doctoral_route_recorded_research_masters_route_missed | false_negative_corrected | ror:026vcq606:program:thesis-or-research-master-s:msc-computer-science |

St. Francis Xavier University and KTH Royal Institute of Technology were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2062 | 180 | 0.215 |
| official_program_or_department_signal | 1997 | 200 | 190 | 0.950 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6928 | 59 | 19 | 0.322 |
| lab_or_center_signal | 78 | 77 | 77 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1890 | 137 | 134 | 0.978 |
| underrepresented_route_search | 1871 | 200 | 115 | 0.985 |

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
| reentry09::bounded_reentry_has_exact_routes | PASS |
| reentry09::reentry_covers_all_regions | PASS |
| reentry09::research_masters_reentry_present | PASS |
| reentry09::doctoral_reentry_present | PASS |
| reentry09::all_candidates_advance_only_to_stage_3 | PASS |
| reentry09::all_candidates_have_exact_official_program_urls | PASS |
| reentry09::all_candidates_have_official_institution_urls | PASS |
| reentry09::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry09::all_candidate_source_ids_resolve | PASS |
| reentry09::all_sources_are_official_https | PASS |
| reentry09::program_ids_unique_after_merge | PASS |
| reentry09::all_reentry_routes_are_net_new | PASS |
| reentry09::all_reentry_candidates_present_after_merge | PASS |
| reentry09::known_seed_adjacency_retained | PASS |
| reentry09::confirmed_false_negatives_reaudited | PASS |
| reentry09::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 09 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 19 of 25 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2061 rows while the expanded funnel has 2073. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Emory, Northwestern, Pitt, Brandeis, Michigan State, Syracuse, and Johns Hopkins require transcript-level entry and offer-level support review; their signals range from departmental support statements to competitive or advisor-dependent mechanisms.
- St. Francis Xavier requires degree-equivalency, willing-supervisor, international-package, and net-cost verification even though most accepted MSc students are described as receiving support.
- KTH, Helsinki, Copenhagen, and Tartu require course and language mapping plus a viable tuition and living-cost plan; their scholarships or reductions are partial, limited, or highly competitive.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the U.S. transcript and funding conditions, whether the St. Francis Xavier MSc package clears international net cost, and whether the European routes combine transcript equivalency with viable living-cost funding.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_09.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_09_candidates.csv`
- `data/processed/pass2/stage_02_reentry_09_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
