# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 06 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 06 | After re-entry 07 |
| --- | --- | --- |
| Funnel rows | 2037 | 2049 |
| Advance to Stage 3 | 155 | 167 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 24 |
| Active rows missing exact program URL | documented | 264 |

The round was checked against the cumulative funnel by deterministic program ID. Existing institution records were retained only when the newly discovered degree route was distinct, so the increment does not overstate recall through duplicate programs.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 4 |
| europe | 4 |
| us | 4 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 4 |
| Thesis or research master's | 8 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | Baylor University | [Ph.D. in Computer Science](https://www.ecs.baylor.edu/students-academics/degree-programs/graduate/phd-cs) | PhD | high | Fall 2027 cycle/transcript and prerequisite equivalency/English requirement/funding offer and duration/fees and net cost/current supervisor capacity |
| us | Rice University | [Ph.D. in Computer Science](https://cs.rice.edu/academics/graduate-programs/phd-program) | PhD | high | Fall 2027 cycle/preparation and degree equivalency/English requirement/support package details/fees and net cost/current supervisor capacity |
| us | Washington State University | [Doctor of Philosophy in Computer Science](https://gradschool.wsu.edu/degrees/doctor-of-philosophy-computer-science/) | PhD | high | Fall 2027 cycle/prerequisite and degree equivalency/English treatment/assistantship award and renewal/mandatory fees/current supervisor capacity |
| us | University of South Florida | [Ph.D. in Computer Science and Engineering](https://www.usf.edu/ai-cybersecurity-computing/academics/graduate/prospective-students.aspx) | PhD | medium | Fall 2027 cycle/entry standing and prerequisite mapping/international degree and English review/assistantship probability and package/net cost/current supervisor capacity |
| canada | University of Waterloo | [Master of Applied Science in Electrical and Computer Engineering](https://uwaterloo.ca/electrical-computer-engineering/master-applied-science-masc) | Thesis or research master's | high | Fall 2027 cycle/degree and course equivalency/English evidence/supervisor endorsement/future minimum package/international net cost |
| canada | Queen’s University | [Master of Applied Science in Electrical and Computer Engineering](https://www.queensu.ca/academic-calendar/graduate-studies/programs-study/electrical-computer-engineering/) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/English requirement/supervisor approval/future funding guarantee/tuition differential and net cost |
| canada | University of Alberta | [Master of Science in Electrical and Computer Engineering](https://www.ualberta.ca/en/graduate-programs/electrical-and-computer-engineering.html) | Thesis or research master's | medium | Fall 2027 cycle/related-discipline and course mapping/GPA and English requirements/supervisor availability/assistantship package and duration/international net cost |
| canada | University of Victoria | [Master of Applied Science in Electrical and Computer Engineering](https://www.uvic.ca/graduate/programs/graduate-programs/credential-pages/electrical-computer-engineering-cred/electrical-and-computer-engineering-masc.php) | Thesis or research master's | high | Fall 2027 cycle/degree and preparation equivalency/English evidence/supervisor agreement/assistantship or fellowship award/international net cost |
| europe | Graz University of Technology | [Master's Degree Programme in Software Engineering and Management](https://www.tugraz.at/en/studying-and-teaching/degree-and-certificate-programmes/masters-degree-programmes/software-engineering-and-management) | Thesis or research master's | high | Fall 2027 cycle/bachelor's equivalency and supplemental courses/English evidence/admission procedure/tuition and semester charges/scholarship and living-cost funding |
| europe | Lappeenranta-Lahti University of Technology | [Master's Programme in Software Engineering and Digital Transformation](https://www.lut.fi/en/studies/technology/masters-programmes-technology/masters-programme-software-engineering-and-digital) | Thesis or research master's | high | Fall 2027 call/degree and credit equivalency/English evidence/application documents/scholarship amount and renewal/tuition and living-cost funding |
| europe | Vrije Universiteit Amsterdam | [Computer Science MSc - Software Engineering and Green IT](https://vu.nl/en/education/master/computer-science-joint-degree-vu-uva) | Thesis or research master's | high | Fall 2027 cycle/research-university and subject equivalency/English evidence/specialization availability/institutional tuition/scholarship rank and living costs |
| europe | University of Gothenburg | [Software Engineering and Management Master's Programme](https://www.gu.se/en/study-gothenburg/software-engineering-and-management-masters-programme-n2sof) | Thesis or research master's | high | course-by-course prerequisite mapping/English equivalency/Fall 2027 application documents/scholarship nomination and award/tuition payment/living-cost funding |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 335 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Baylor University | registry_only_signals_not_promoted_to_exact_program_review | false_negative_corrected | us:ipeds:223232:program:phd:ph-d-in-computer-science |
| University of Gothenburg | outside_bounded_positive_seed_screen | false_negative_corrected | ror:01tm6cn81:program:thesis-or-research-master-s:software-engineering-and-management-master-s-programme |

Baylor University and University of Gothenburg were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2038 | 156 | 0.206 |
| official_program_or_department_signal | 1970 | 176 | 166 | 0.943 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6928 | 56 | 16 | 0.286 |
| lab_or_center_signal | 75 | 74 | 74 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1872 | 118 | 115 | 0.975 |
| underrepresented_route_search | 1870 | 185 | 100 | 0.984 |

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
| reentry07::bounded_reentry_has_exact_routes | PASS |
| reentry07::reentry_covers_all_regions | PASS |
| reentry07::research_masters_reentry_present | PASS |
| reentry07::doctoral_reentry_present | PASS |
| reentry07::all_candidates_advance_only_to_stage_3 | PASS |
| reentry07::all_candidates_have_exact_official_program_urls | PASS |
| reentry07::all_candidates_have_official_institution_urls | PASS |
| reentry07::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry07::all_candidate_source_ids_resolve | PASS |
| reentry07::all_sources_are_official_https | PASS |
| reentry07::program_ids_unique_after_merge | PASS |
| reentry07::all_reentry_candidates_present_after_merge | PASS |
| reentry07::known_seed_adjacency_retained | PASS |
| reentry07::confirmed_false_negatives_reaudited | PASS |
| reentry07::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 07 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 20 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2037 rows while the expanded funnel has 2049. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Baylor, Rice, Washington State, and South Florida require transcript-level entry review; Baylor and Rice publish strong doctoral support signals, while WSU and USF leave awards conditional.
- Waterloo, Queen's, Alberta, and Victoria require degree-equivalency, supervisor, international-package, and net-cost verification even where a minimum or assistantship mechanism is published.
- TU Graz, LUT, VU Amsterdam, and Gothenburg require curriculum and language mapping plus a viable tuition and living-cost plan; their scholarship routes are limited or competitive.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the U.S. transcript and funding conditions, whether any Canadian MASc package clears international net cost, and whether the European routes combine transcript equivalency with viable living-cost funding.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_07.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_07_candidates.csv`
- `data/processed/pass2/stage_02_reentry_07_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
