# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 01 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This second bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 01 | After re-entry 02 |
| --- | --- | --- |
| Funnel rows | 1977 | 1989 |
| Advance to Stage 3 | 95 | 107 |
| Net new exact routes | 12 | 12 |
| Current-round official source records | 32 | 38 |
| Active rows missing exact program URL | documented | 264 |

The round deliberately replaced two initially considered Canadian routes already present in the funnel with York and Regina exact thesis routes. That preserved a true 12-route increment instead of overstating recall through duplicate records.

## Coverage

| Current-round region | Exact routes |
| --- | --- |
| canada | 2 |
| europe | 2 |
| us | 8 |

| Current-round degree route | Exact routes |
| --- | --- |
| PhD | 8 |
| Thesis or research master's | 4 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | Rutgers University-New Brunswick | [Computer Science PhD](https://www.cs.rutgers.edu/academics/graduate/ph-d-program/computer-science-program) | PhD | high | Fall 2027 cycle/prerequisite equivalency/admission plausibility/individual funding terms/current faculty supervision |
| us | Ohio State University-Main Campus | [Computer Science and Engineering PhD](https://cse.osu.edu/graduate/graduate/doctor-philosophy-program) | PhD | high | Fall 2027 final cycle details/competitiveness above minimum GPA/funding duration/individual award/current faculty supervision |
| us | Stony Brook University | [Computer Science PhD](https://www.fsl.cs.stonybrook.edu/SBU-CS-Grad-Admissions/) | PhD | high | Fall 2027 admissions page/prerequisite equivalency/offer-specific funding duration/summer coverage/current faculty supervision |
| us | University of California-Santa Barbara | [Computer Science PhD](https://cs.ucsb.edu/index.php/education/graduate/phd-degree) | PhD | high | Fall 2027 deadline/international transcript equivalency/funding duration and summer coverage/current faculty supervision |
| us | University of Delaware | [Computer Science PhD](https://www.udel.edu/academics/colleges/grad/prospective-students/programs/computer-science/) | PhD | high | Fall 2027 cycle/major GPA calculation/English rule after U.S. bachelor's/individual funding package/current faculty supervision |
| us | Boston University | [Computer Science PhD](https://www.bu.edu/cs/phd-program/) | PhD | high | bachelor's-entry wording/international credential equivalency/program-specific application of full-funding model/current faculty supervision |
| us | University of North Carolina at Charlotte | [Computing and Information Systems PhD - Software and Information Systems Track](https://cci.charlotte.edu/academics/software-and-information-systems/phd-sis-track) | PhD | medium | Fall 2027 application cycle/international eligibility details/assistantship guarantee and duration/current faculty supervision |
| us | Indiana University-Bloomington | [Computer Science PhD](https://luddy.iu.edu/academics/doctoral/computer-science.html) | PhD | high | 3.5 doctoral GPA rule applicability/Fall 2027 final credential evaluation/department funding norm and duration/current faculty supervision |
| canada | York University | [Computer Science MSc (Thesis Option)](https://lassonde.yorku.ca/eecs/academics/graduate/computer-science-msc/) | Thesis or research master's | high | Fall 2027 international deadline/degree equivalency/net funding after international tuition/supervisor assignment and current capacity |
| canada | University of Regina | [Computer Science MSc (Thesis-Based)](https://www.uregina.ca/academics/programs/science/master-phd-computer-science.html) | Thesis or research master's | high | Fall 2027 cycle/degree and CS-course equivalency/available supervisor/funding amount, duration, and net international cost |
| europe | University of Twente | [Computer Science MSc - Software Technology](https://www.utwente.nl/en/education/master/programmes/computer-science/specialisation/software-technology/) | Thesis or research master's | high | international degree equivalency/research-credit mapping/English test exemption/scholarship competitiveness/remaining international cost/thesis supervisor fit |
| europe | Radboud University Nijmegen | [Computing Science MSc - Software Science](https://www.ru.nl/en/education/masters/software-science) | Thesis or research master's | high | international degree equivalency/theory-credit mapping/bachelor thesis equivalency/scholarship competitiveness and amount/remaining international cost/thesis supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 275 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Rutgers University-New Brunswick | single_bounded_registry_signal_without_independent_topic_signal | false_negative_corrected | us:ipeds:186380:program:phd:computer-science-phd |
| Radboud University Nijmegen | outside_bounded_positive_seed_screen | false_negative_corrected | ror:016xsfp80:program:thesis-or-research-master-s:computing-science-msc-software-science |

Rutgers was screened out by the original one-signal rule, and Radboud was absent from the bounded positive-seed screen. Current official evidence corrects both omissions, but promotes them only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 1978 | 96 | 0.182 |
| official_program_or_department_signal | 1876 | 116 | 106 | 0.914 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6925 | 53 | 13 | 0.245 |
| lab_or_center_signal | 67 | 66 | 66 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1846 | 86 | 83 | 0.965 |
| underrepresented_route_search | 1852 | 140 | 55 | 0.979 |

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
| reentry02::bounded_reentry_has_exact_routes | PASS |
| reentry02::reentry_covers_all_regions | PASS |
| reentry02::research_masters_reentry_present | PASS |
| reentry02::doctoral_reentry_present | PASS |
| reentry02::all_candidates_advance_only_to_stage_3 | PASS |
| reentry02::all_candidates_have_exact_official_program_urls | PASS |
| reentry02::all_candidates_have_official_institution_urls | PASS |
| reentry02::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry02::all_candidate_source_ids_resolve | PASS |
| reentry02::all_sources_are_official_https | PASS |
| reentry02::program_ids_unique_after_merge | PASS |
| reentry02::all_reentry_candidates_present_after_merge | PASS |
| reentry02::known_seed_adjacency_retained | PASS |
| reentry02::confirmed_false_negatives_reaudited | PASS |
| reentry02::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 02 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 38 of 38 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 1977 rows while the expanded funnel has 1989. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Indiana's published 3.5 PhD GPA criterion is an explicit preliminary eligibility concern against the applicant's current approximately 3.35 cumulative GPA.
- Twente and Radboud scholarships are competitive and partial; neither route is currently financially viable without a verified substantial award or additional funding.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are Indiana's GPA rule, York's net international package, Regina's supervisor-dependent funding, and remaining costs after Dutch partial scholarships.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_02.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_02_candidates.csv`
- `data/processed/pass2/stage_02_reentry_02_sources.csv`
- `src/graduate_audit/candidate_reentry.py`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
