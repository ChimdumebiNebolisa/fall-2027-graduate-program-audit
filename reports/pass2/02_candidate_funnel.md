# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 16 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 16 | After re-entry 17 |
| --- | --- | --- |
| Funnel rows | 2157 | 2169 |
| Advance to Stage 3 | 275 | 287 |
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
| us | Drexel University | [PhD in Computer Science](https://drexel.edu/cci/academics/doctoral-programs/) | PhD | high | Fall 2027 cycle/credential and prerequisite equivalency/English evidence/advisor capacity/assistantship duration and renewal/summer support/fees, insurance, and net funding |
| us | Lehigh University | [PhD in Computer Science](https://engineering.lehigh.edu/academics/graduate/phd/phd-computer-science) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/advisor and research-group capacity/funding term and renewal/summer support/fees, insurance, and net funding |
| us | George Washington University | [PhD in Computer Science](https://graduate.engineering.gwu.edu/phd-computer-science) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English funding threshold/advisor capacity/assistantship selection and renewal/remaining tuition, summer support, and fees/insurance and net funding |
| us | University at Albany | [Doctor of Philosophy in Computer Science](https://www.albany.edu/computer-science/programs/phd-computer-science) | PhD | high | Fall 2027 cycle/credential and course equivalency/English evidence/advisor capacity/assistantship availability and award value/tuition waiver and renewal/summer support, fees, and insurance |
| us | Worcester Polytechnic Institute | [PhD in Computer Science](https://www.wpi.edu/academics/study/computer-science-phd) | PhD | high | Fall 2027 cycle/bachelor's-entry and prerequisite mapping/English evidence/advisor capacity/assistantship selection and tuition coverage/renewal and summer support/fees, insurance, and net funding |
| us | Oakland University | [Doctor of Philosophy in Computer Science and Informatics](https://www.oakland.edu/secs/doctoral-programs/) | PhD | high | Fall 2027 cycle and position availability/degree and master's equivalency/English evidence/supervisor capacity and recruiting status/stipend and tuition coverage/renewal and summer support/fees and insurance |
| canada | University of British Columbia | [Master of Applied Science in Electrical and Computer Engineering](https://ece.ubc.ca/graduate/programs/master-applied-science/) | Thesis or research master's | high | Fall 2027 application details/degree and subject equivalency/English evidence/supervisor capacity/RA or scholarship award/international tuition and fees/living costs, insurance, and net support |
| canada | University of Toronto | [Master of Applied Science in Electrical and Computer Engineering](https://www.ece.utoronto.ca/graduates/degree-programs/masc/) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/supervisor capacity/2027-28 funding amount/international tuition and ancillary fees/insurance, living costs, and net support |
| canada | McGill University | [Electrical Engineering (Thesis) (M.Sc.)](https://www.mcgill.ca/gradapplicants/program/electrical-engineering-msc) | Thesis or research master's | high | Fall 2027 deadline/degree and subject equivalency/English evidence/supervisor capacity/assistantship or award selection/international tuition and fees/living costs, insurance, and net funding |
| europe | Norwegian University of Science and Technology | [Erasmus Mundus Joint Master in Cybersecurity and Assurance (CYBERSURE)](https://www.ntnu.edu/studies/mscybsure) | Thesis or research master's | high | exact bachelor's-course eligibility/English test and document timing/scholarship selection/full versus partial award/mobility and visa costs/insurance and net funding/thesis supervisor and topic allocation |
| europe | Université Libre de Bruxelles | [Erasmus Mundus Joint Master in Cybersecurity (CYBERUS)](https://www.ulb.be/en/programme/m-secum) | Thesis or research master's | medium | Fall 2027 intake and application dates/foreign-degree and course equivalency/English evidence/Erasmus Mundus scholarship availability and selection/mobility and visa costs/insurance and net funding/dissertation supervision |
| europe | Åbo Akademi University | [Erasmus Mundus Joint Master in Engineering of Data-intensive Intelligent Software Systems (EDISS)](https://www.master-ediss.eu/) | Thesis or research master's | medium | Fall 2027 intake and scholarship call/degree and course equivalency/country-specific documents/English evidence/scholarship selection and coverage/mobility, visa, insurance, and net funding/specialization and thesis placement |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 455 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Oakland University | mechanical_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:171571:program:phd:doctor-of-philosophy-in-computer-science-and-informatics |
| Norwegian University of Science and Technology | outside_bounded_positive_seed_screen | false_negative_corrected | ror:05xg72x27:program:thesis-or-research-master-s:erasmus-mundus-joint-master-in-cybersecurity-and-assurance-cybersure |

Oakland University and Norwegian University of Science and Technology were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2149 | 267 | 0.247 |
| official_program_or_department_signal | 2094 | 296 | 286 | 0.966 |
| recent_paper_signal | 1649 | 907 | 76 | 0.363 |
| current_faculty_topic_signal | 6933 | 64 | 24 | 0.375 |
| lab_or_center_signal | 90 | 91 | 91 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1965 | 212 | 209 | 0.986 |
| underrepresented_route_search | 1871 | 277 | 192 | 0.989 |

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
| reentry17::bounded_reentry_has_exact_routes | PASS |
| reentry17::reentry_covers_all_regions | PASS |
| reentry17::research_masters_reentry_present | PASS |
| reentry17::doctoral_reentry_present | PASS |
| reentry17::all_candidates_advance_only_to_stage_3 | PASS |
| reentry17::all_candidates_have_exact_official_program_urls | PASS |
| reentry17::all_candidates_have_official_institution_urls | PASS |
| reentry17::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry17::all_candidate_source_ids_resolve | PASS |
| reentry17::all_sources_are_official_https | PASS |
| reentry17::program_ids_unique_after_merge | PASS |
| reentry17::all_reentry_routes_are_net_new | PASS |
| reentry17::all_reentry_candidates_present_after_merge | PASS |
| reentry17::known_seed_adjacency_retained | PASS |
| reentry17::confirmed_false_negatives_reaudited | PASS |
| reentry17::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 17 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2157 rows while the expanded funnel has 2169. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

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

- `data/raw/pass2/stage_02_reentry_17.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_17_candidates.csv`
- `data/processed/pass2/stage_02_reentry_17_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
