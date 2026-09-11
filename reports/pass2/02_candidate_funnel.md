# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 15 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 15 | After re-entry 16 |
| --- | --- | --- |
| Funnel rows | 2145 | 2157 |
| Advance to Stage 3 | 263 | 275 |
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
| us | Florida Atlantic University | [Doctor of Philosophy with Major in Computer Science](https://www.fau.edu/engineering/eecs/graduate/phd/) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/advisor capacity/assistantship selection and renewal/summer support/fees and net funding |
| us | New Mexico Institute of Mining and Technology | [Doctor of Philosophy in Computer Science](https://www.nmt.edu/academics/compsci/graduate.php) | PhD | high | Fall 2027 cycle/degree and course equivalency/English evidence/advisor capacity/assistantship value and tuition coverage/renewal and summer support/fees and insurance |
| us | Southern Illinois University-Carbondale | [Computer Science, Doctor of Philosophy](https://academics.siu.edu/computing-and-technology/computer-science/doctoral/) | PhD | medium | Fall 2027 cycle/degree and prerequisite mapping/English evidence/advisor capacity/assistantship award and renewal/summer coverage/fees and insurance |
| us | Wichita State University | [PhD in Electrical Engineering and Computer Science](https://catalog.wichita.edu/graduate/engineering/electrical-computer-engineering/phd-in-eecs/) | PhD | high | Fall 2027 cycle/exceptional bachelor's-entry threshold/degree and prerequisite equivalency/English evidence/faculty willingness and capacity/assistantship selection and renewal/fees and summer support |
| us | Michigan Technological University | [Computer Science, PhD](https://www.mtu.edu/gradschool/programs/degrees/computer-science/) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/GRE and English evidence/advisor capacity/assistantship appointment and tuition coverage/renewal and summer support/fees and insurance |
| us | University of Tulsa | [Computer Science, Ph.D.](https://utulsa.edu/programs/computer-science/) | PhD | medium | Fall 2027 cycle/degree and prerequisite mapping/English evidence/doctoral curriculum details/advisor capacity/assistantship selection and renewal/summer and fee coverage |
| canada | Western University | [Master of Engineering Science (MESc) in Electrical and Computer Engineering](https://www.eng.uwo.ca/graduate/future-students/Graduate-Degree-Programs/electrical-computer.html) | Thesis or research master's | high | Fall 2027 cycle/degree similarity and prerequisite mapping/English evidence/supervisor capacity/funding amount for 2027/renewal and summer coverage/ancillary fees and insurance |
| canada | York University | [MASc in Electrical and Computer Engineering](https://futurestudents.yorku.ca/graduate/programs/electrical-engineering-and-computer-science) | Thesis or research master's | high | Fall 2027 cycle/degree and senior-project equivalency/English evidence/supervisor assignment and capacity/offer-specific funding/tuition and ancillary fees/insurance and net support |
| canada | University of Saskatchewan | [Electrical Engineering, Master of Science (M.Sc.) — Thesis](https://grad.usask.ca/programs/electrical-computer-engineering.php) | Thesis or research master's | high | Fall 2027 cycle/degree and field equivalency/English evidence/supervisor approval and capacity/funding award and duration/international tuition offset/fees and insurance |
| europe | Politecnico di Milano | [Master's Degree in Computer Science and Engineering](https://www.polimi.it/en/education/laurea-programmes/programme-detail/computer-science-and-engineering) | Thesis or research master's | high | Fall 2027 offering and scholarship cycle/degree and subject equivalency/English evidence/thesis placement and supervision/scholarship selection/living costs/fees and insurance |
| europe | Universidade do Porto | [Master in Informatics and Computing Engineering](https://fe.up.pt/estudar/meic/?lang=en) | Thesis or research master's | high | Fall 2027 cycle/foreign degree and subject equivalency/teaching-language details/dissertation supervisor and topic/international tuition/funding selection and amount/living costs and insurance |
| europe | University of Minho | [Master in Informatics Engineering](https://www.eng.uminho.pt/en/study/_layouts/15/uminho.portaisuoei.ui/pages/catalogocursodetail.aspx?catid=16&itemid=5482) | Thesis or research master's | medium | Fall 2027 offering/foreign degree and subject equivalency/language of instruction/dissertation structure and supervision/tuition for the engineering school/merit scholarship selection/living costs and insurance |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 443 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| New Mexico Institute of Mining and Technology | mechanical_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:187967:program:phd:doctor-of-philosophy-in-computer-science |
| Politecnico di Milano | outside_bounded_positive_seed_screen | false_negative_corrected | ror:01nffqt88:program:thesis-or-research-master-s:master-s-degree-in-computer-science-and-engineering |

New Mexico Institute of Mining and Technology and Politecnico di Milano were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2137 | 255 | 0.243 |
| official_program_or_department_signal | 2082 | 284 | 274 | 0.965 |
| recent_paper_signal | 1649 | 907 | 76 | 0.363 |
| current_faculty_topic_signal | 6933 | 64 | 24 | 0.375 |
| lab_or_center_signal | 89 | 90 | 90 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1954 | 201 | 198 | 0.985 |
| underrepresented_route_search | 1871 | 265 | 180 | 0.989 |

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
| reentry16::bounded_reentry_has_exact_routes | PASS |
| reentry16::reentry_covers_all_regions | PASS |
| reentry16::research_masters_reentry_present | PASS |
| reentry16::doctoral_reentry_present | PASS |
| reentry16::all_candidates_advance_only_to_stage_3 | PASS |
| reentry16::all_candidates_have_exact_official_program_urls | PASS |
| reentry16::all_candidates_have_official_institution_urls | PASS |
| reentry16::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry16::all_candidate_source_ids_resolve | PASS |
| reentry16::all_sources_are_official_https | PASS |
| reentry16::program_ids_unique_after_merge | PASS |
| reentry16::all_reentry_routes_are_net_new | PASS |
| reentry16::all_reentry_candidates_present_after_merge | PASS |
| reentry16::known_seed_adjacency_retained | PASS |
| reentry16::confirmed_false_negatives_reaudited | PASS |
| reentry16::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 16 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 23 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2145 rows while the expanded funnel has 2157. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

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

- `data/raw/pass2/stage_02_reentry_16.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_16_candidates.csv`
- `data/processed/pass2/stage_02_reentry_16_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
