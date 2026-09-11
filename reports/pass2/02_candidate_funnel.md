# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 12 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 12 | After re-entry 13 |
| --- | --- | --- |
| Funnel rows | 2109 | 2121 |
| Advance to Stage 3 | 227 | 239 |
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
| us | University of Alabama in Huntsville | [Computer Science, Ph.D.](https://www.uah.edu/science/departments/computer-science/cs-graduate-programs) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/English evidence/research-plan fit/assistantship selection and duration/stipend and summer support/current supervisor capacity |
| us | The University of Texas at El Paso | [Doctor of Philosophy in Computer Science](https://catalog.utep.edu/grad/college-of-engineering/computer-science/computer-science-phd/) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GPA interpretation/English evidence/assistantship and waiver availability/fees and insurance/current lab capacity |
| us | University of Nevada-Las Vegas | [Doctor of Philosophy - Computer Science](https://www.unlv.edu/degree/phd-computer-science) | PhD | high | Fall 2027 cycle/degree and course equivalency/GPA interpretation/English evidence/assistantship selection and renewal/fees and insurance/current advisor capacity |
| us | Old Dominion University | [Computer Science (Ph.D.)](https://www.odu.edu/academics/programs/doctoral/computer-science) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/English evidence/first-year award terms/renewal and summer support/fees and insurance/current supervisor capacity |
| us | Temple University | [Computer and Information Science PhD](https://bulletin.temple.edu/graduate/scd/cst/computer-information-science-phd/) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/English evidence/track and advisor fit/assistantship offer and duration/summer support and fees/current supervisor capacity |
| us | University of Rhode Island | [Computer Science Ph.D.](https://www.uri.edu/programs/program/computer-science-ph-d/) | PhD | high | Fall 2027 cycle/degree and course mapping/GPA interpretation/English evidence/assistantship selection and duration/summer support/current advisor capacity |
| canada | Bishop's University | [M.Sc. in Computer Science - Thesis Option](https://www.ubishops.ca/academics/faculties-and-schools/faculty-of-natural-sciences-and-mathematics/computer-science/masters-degree-program/) | Thesis or research master's | high | Fall 2027 cycle/degree and course equivalency/GPA interpretation/English evidence/willing supervisor/assistantship amount and duration/international tuition and net cost |
| canada | Université du Québec à Montréal | [Maîtrise en informatique - profil avec mémoire](https://info.uqam.ca/ma%C3%AEtrise_en_informatique/) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/grade interpretation/French and English evidence/willing supervisor/scholarship eligibility and amount/international tuition and net cost |
| canada | Université de Moncton | [Maîtrise ès sciences (informatique)](https://www.umcs.umoncton.ca/fesr/programmes?programme_id=222&programme_select=222) | Thesis or research master's | medium | Fall 2027 cycle/degree and course equivalency/grade interpretation/French-language evidence/willing supervisor/assistantship or scholarship availability/international tuition and net cost |
| europe | Tampere University | [Master's Programme in AI-Native Software](https://www.tuni.fi/en/tau/masters-programmes/ai-native-software-computing-sciences-and-electrical-engineering) | Thesis or research master's | high | Fall 2027 offering and criteria/degree and course equivalency/grade selection/English evidence/scholarship selection and renewal/remaining tuition and living costs/thesis-group fit |
| europe | Paderborn University | [M.Sc. Computer Science](https://www.uni-paderborn.de/en/studyoffer/course_of_study/computer-science-master) | Thesis or research master's | high | Fall 2027 cycle/degree and subject-credit equivalency/German grade conversion/GRE or dMat exception/English evidence/semester contribution and living costs/scholarship or employment route/thesis-group fit |
| europe | Åbo Akademi University | [Master's Degree Programme in Information Technology - Computer Science](https://www.abo.fi/en/study-programme/masters-degree-programme-in-information-technology/) | Thesis or research master's | high | Fall 2027 offering and criteria/degree and course equivalency/academic selection/English evidence/2027 tuition reduction/remaining tuition and living costs/thesis-supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 407 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Alabama in Huntsville | catalog_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:100706:program:phd:computer-science-ph-d |
| Åbo Akademi University | outside_bounded_positive_seed_screen | false_negative_corrected | ror:029pk6x14:program:thesis-or-research-master-s:master-s-degree-programme-in-information-technology-computer-science |

University of Alabama in Huntsville and Åbo Akademi University were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2101 | 219 | 0.230 |
| official_program_or_department_signal | 2045 | 248 | 238 | 0.960 |
| recent_paper_signal | 1647 | 905 | 74 | 0.361 |
| current_faculty_topic_signal | 6930 | 61 | 21 | 0.344 |
| lab_or_center_signal | 84 | 85 | 85 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1929 | 176 | 173 | 0.983 |
| underrepresented_route_search | 1871 | 229 | 144 | 0.987 |

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
| reentry13::bounded_reentry_has_exact_routes | PASS |
| reentry13::reentry_covers_all_regions | PASS |
| reentry13::research_masters_reentry_present | PASS |
| reentry13::doctoral_reentry_present | PASS |
| reentry13::all_candidates_advance_only_to_stage_3 | PASS |
| reentry13::all_candidates_have_exact_official_program_urls | PASS |
| reentry13::all_candidates_have_official_institution_urls | PASS |
| reentry13::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry13::all_candidate_source_ids_resolve | PASS |
| reentry13::all_sources_are_official_https | PASS |
| reentry13::program_ids_unique_after_merge | PASS |
| reentry13::all_reentry_routes_are_net_new | PASS |
| reentry13::all_reentry_candidates_present_after_merge | PASS |
| reentry13::known_seed_adjacency_retained | PASS |
| reentry13::confirmed_false_negatives_reaudited | PASS |
| reentry13::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 13 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2109 rows while the expanded funnel has 2121. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

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

- `data/raw/pass2/stage_02_reentry_13.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_13_candidates.csv`
- `data/processed/pass2/stage_02_reentry_13_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
