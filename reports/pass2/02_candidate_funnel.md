# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 14 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 14 | After re-entry 15 |
| --- | --- | --- |
| Funnel rows | 2133 | 2145 |
| Advance to Stage 3 | 251 | 263 |
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
| us | University of New Hampshire-Main Campus | [Computer Science, Ph.D.](https://www.unh.edu/program/doctor-philosophy/computer-science) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/advisor capacity/funding award and duration/summer support/fees and insurance |
| us | University of Missouri-Columbia | [PhD in Computer Science](https://engineering.missouri.edu/departments/eecs/eecs-degrees/) | PhD | high | Fall 2027 cycle/degree and course equivalency/English evidence/advisor capacity/assistantship selection and coverage/summer support/fees and insurance |
| us | University of Wisconsin-Milwaukee | [Computer Science PhD](https://uwm.edu/engineering/academics/computer-science-phd/) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/English evidence/major-professor availability/assistantship selection and renewal/summer support/fees and insurance |
| us | Illinois Institute of Technology | [Computer Science (Ph.D.)](https://www.iit.edu/academics/programs/computer-science-phd) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/GRE and English evidence/faculty opening persistence/funding duration and renewal/summer coverage/fees and insurance |
| us | New Jersey Institute of Technology | [Ph.D. Computer Science](https://www.njit.edu/academics/degree/phd-computer-science) | PhD | high | Fall 2027 cycle/degree recognition and prerequisites/English evidence/advisor capacity/assistantship award and renewal/summer coverage/fees and insurance |
| us | University of Connecticut | [Computer Science and Engineering (PhD)](https://catalog.uconn.edu/graduate/degree-programs/computer-science-engineering-phd/) | PhD | medium | Fall 2027 cycle/degree and course equivalency/English evidence/research-area depth/advisor capacity/assistantship award and duration/fees and insurance |
| canada | École de technologie supérieure | [Maîtrise en génie logiciel (profil avec mémoire)](https://www.etsmtl.ca/programmes-formations/maitrise-genie-logiciel) | Thesis or research master's | high | Fall 2027 cycle/degree equivalency/English-based admission and French course/supervisor commitment/tuition exemption selection/stipend and net cost/fees and insurance |
| canada | Université du Québec à Rimouski | [Maîtrise en informatique (profil recherche avec mémoire)](https://www.uqar.ca/programmes-domaines-detudes/maitrise-en-informatique/) | Thesis or research master's | medium | Fall 2027 cycle/degree and course equivalency/language evidence/supervisor requirement and capacity/research-topic depth/scholarship and exemption selection/net cost and insurance |
| canada | Saint Mary’s University | [MSc in Applied Science — Computing Science research field](https://www.smu.ca/faculty-of-science/master-in-applied-science-future-students.html) | Thesis or research master's | medium | Fall 2027 cycle/degree and course equivalency/English evidence/Computing Science supervisor capacity/stipend composition and guarantee/tuition and fees/insurance and net cost |
| europe | Mälardalen University | [Master's Programme in Software Engineering](https://www.mdu.se/en/malardalen-university/education/international/programme/masters-programme-in-software-engineering) | Thesis or research master's | high | Fall 2027 cycle/computer science and mathematics credit mapping/English evidence/thesis-supervision fit/scholarship selection/living costs/fees and insurance |
| europe | Linnaeus University | [Software Technology, Master Programme — 120 credits](https://www.lnu.se/en/programme/software-technology-master-programme-nada2/vaxjo-international-autumn/) | Thesis or research master's | medium | Fall 2027 cycle/degree and subject-credit equivalency/English evidence/thesis topic and supervision/scholarship selection/remaining tuition and living costs/fees and insurance |
| europe | University of Coimbra | [Master in Informatics Engineering](https://www.uc.pt/en/fctuc/dei/education/masters/master-in-informatics-engineering/) | Thesis or research master's | high | Fall 2027 cycle/foreign degree recognition and subject mapping/English delivery/dissertation versus internship path/research supervisor/scholarship selection/remaining tuition and living costs |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 431 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Université du Québec à Rimouski | catalog_signal_without_exact_research_masters_route | false_negative_corrected | ca:dli:O19359011159:program:thesis-or-research-master-s:ma-trise-en-informatique-profil-recherche-avec-m-moire |
| Mälardalen University | outside_bounded_positive_seed_screen | false_negative_corrected | ror:033vfbz75:program:thesis-or-research-master-s:master-s-programme-in-software-engineering |

Université du Québec à Rimouski and Mälardalen University were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2125 | 243 | 0.239 |
| official_program_or_department_signal | 2069 | 272 | 262 | 0.963 |
| recent_paper_signal | 1649 | 907 | 76 | 0.363 |
| current_faculty_topic_signal | 6932 | 63 | 23 | 0.365 |
| lab_or_center_signal | 89 | 90 | 90 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1944 | 191 | 188 | 0.984 |
| underrepresented_route_search | 1871 | 253 | 168 | 0.988 |

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
| reentry15::bounded_reentry_has_exact_routes | PASS |
| reentry15::reentry_covers_all_regions | PASS |
| reentry15::research_masters_reentry_present | PASS |
| reentry15::doctoral_reentry_present | PASS |
| reentry15::all_candidates_advance_only_to_stage_3 | PASS |
| reentry15::all_candidates_have_exact_official_program_urls | PASS |
| reentry15::all_candidates_have_official_institution_urls | PASS |
| reentry15::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry15::all_candidate_source_ids_resolve | PASS |
| reentry15::all_sources_are_official_https | PASS |
| reentry15::program_ids_unique_after_merge | PASS |
| reentry15::all_reentry_routes_are_net_new | PASS |
| reentry15::all_reentry_candidates_present_after_merge | PASS |
| reentry15::known_seed_adjacency_retained | PASS |
| reentry15::confirmed_false_negatives_reaudited | PASS |
| reentry15::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 15 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 19 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2133 rows while the expanded funnel has 2145. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- The six current U.S. doctoral routes require transcript-level entry, current-advisor capacity, and offer-level assistantship review; every recorded support mechanism remains preliminary.
- The three current Canadian thesis routes require degree and course equivalency, willing-supervisor, current international-package, and net-cost verification.
- The three current European routes require subject-credit and English mapping plus a viable tuition and living-cost plan; every recorded institutional discount or funding route remains incomplete.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the six U.S. transcript and assistantship conditions, whether the three Canadian thesis routes clear supervisor and international net-cost gates, and whether the three European routes combine qualification equivalency with a viable tuition and living-cost plan.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_15.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_15_candidates.csv`
- `data/processed/pass2/stage_02_reentry_15_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
