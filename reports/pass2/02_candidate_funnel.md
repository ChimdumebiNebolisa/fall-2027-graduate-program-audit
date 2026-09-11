# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 05 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This sixth bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 05 | After re-entry 06 |
| --- | --- | --- |
| Funnel rows | 2025 | 2037 |
| Advance to Stage 3 | 143 | 155 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 36 |
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
| us | North Dakota State University-Main Campus | [Ph.D. in Software and Security Engineering](https://www.ndsu.edu/programs/graduate/software-and-security-engineering) | PhD | high | Fall 2027 cycle/transcript and prerequisite equivalency/English requirement/assistantship award and renewal/differential tuition and fees/current faculty supervision |
| us | Boise State University | [Computing PhD — Computer Science or Cybersecurity Emphasis](https://www.boisestate.edu/computing/academics/doctoral-program/) | PhD | high | Fall 2027 deadline and emphasis availability/prerequisite mapping/English requirement/first-year assistantship competition/post-year-one funding/current advisor fit |
| us | The University of Alabama | [Ph.D. in Computer Science](https://eng.ua.edu/majors/computer-science-ph-d/) | PhD | high | direct bachelor's entry/Fall 2027 cycle/GPA and prerequisite mapping/English treatment/assistantship package and duration/current supervisor capacity |
| us | Florida International University | [Doctor of Philosophy in Computer Science](https://www.cis.fiu.edu/degree/doctor-of-philosophy-in-computer-science/) | PhD | high | Fall 2027 cycle/upper-division GPA calculation/mathematics prerequisites/English requirement/first-year award probability/advisor-funded continuation |
| canada | Ontario Tech University | [Software Engineering (MASc)](https://gradstudies.ontariotechu.ca/future_students/programs/masters_programs/software_engineering/index.php) | Thesis or research master's | high | Fall 2027 cycle/degree equivalency/supervisor commitment/English treatment/minimum package amount and duration/international tuition differential |
| canada | Carleton University | [Electrical and Computer Engineering (MASc) — Software Engineering Concentration](https://graduate.carleton.ca/program/electrical-and-computer-engineering-masters-programs/) | Thesis or research master's | high | Fall 2027 cycle/concentration availability/degree equivalency and GPA/English treatment/supervisor requirement/international funding package |
| canada | University of Ottawa | [Master of Applied Science in Electrical and Computer Engineering](https://www.uottawa.ca/faculty-engineering/graduate-studies/programs/electrical-computer-engineering) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/English treatment/supervisor and thesis placement/funding amount and duration/international net cost |
| canada | University of Windsor | [Electrical Engineering (MASc)](https://www.uwindsor.ca/graduate-studies/320/electrical-engineering) | Thesis or research master's | medium | computer-science degree equivalency/Fall 2027 cycle/advisor match/English treatment/competitive scholarship and assistantship package/international tuition and living cost |
| europe | Saarland University | [M.Sc. Cybersecurity](https://www.uni-saarland.de/en/study/programmes/master/cybersecurity.html) | Thesis or research master's | high | Fall 2027 cycle/curriculum equivalency/grade conversion/C1 English proof/semester contribution/living-cost funding |
| europe | University of Passau | [M.Sc. Computer Science](https://www.uni-passau.de/en/msc-computer-science) | Thesis or research master's | high | Fall 2027 cycle/110-ECTS subject mapping/German grade conversion or cohort rank/English evidence/semester contribution/living-cost funding |
| europe | Technische Universität Berlin | [Computer Science (Informatik), M.Sc.](https://www.tu.berlin/en/studying/study-programs/all-programs-offered/study-course/computer-science-informatik-m-sc/) | Thesis or research master's | high | Fall 2027 cycle/detailed credit-category mapping/B2 English evidence/application document review/semester charges/living-cost funding |
| europe | University of Trento | [Master's Degree in Computer Science](https://corsi.unitn.it/en/computer-science-master) | Thesis or research master's | high | 2027-2028 admissions call/degree and course equivalency/English evidence/merit ranking/scholarship availability and renewal/net living cost |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 323 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| North Dakota State University-Main Campus | registry_only_signals_not_promoted_to_exact_program_review | false_negative_corrected | us:ipeds:200332:program:phd:ph-d-in-software-and-security-engineering |
| University of Trento | outside_bounded_positive_seed_screen | false_negative_corrected | ror:05trd4x28:program:thesis-or-research-master-s:master-s-degree-in-computer-science |

North Dakota State University-Main Campus, and University of Trento were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2026 | 144 | 0.201 |
| official_program_or_department_signal | 1955 | 164 | 154 | 0.939 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6927 | 55 | 15 | 0.273 |
| lab_or_center_signal | 73 | 72 | 72 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1866 | 109 | 106 | 0.972 |
| underrepresented_route_search | 1870 | 179 | 94 | 0.983 |

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
| reentry06::bounded_reentry_has_exact_routes | PASS |
| reentry06::reentry_covers_all_regions | PASS |
| reentry06::research_masters_reentry_present | PASS |
| reentry06::doctoral_reentry_present | PASS |
| reentry06::all_candidates_advance_only_to_stage_3 | PASS |
| reentry06::all_candidates_have_exact_official_program_urls | PASS |
| reentry06::all_candidates_have_official_institution_urls | PASS |
| reentry06::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry06::all_candidate_source_ids_resolve | PASS |
| reentry06::all_sources_are_official_https | PASS |
| reentry06::program_ids_unique_after_merge | PASS |
| reentry06::all_reentry_candidates_present_after_merge | PASS |
| reentry06::known_seed_adjacency_retained | PASS |
| reentry06::confirmed_false_negatives_reaudited | PASS |
| reentry06::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 06 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 36 of 36 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2025 rows while the expanded funnel has 2037. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- NDSU's program GPA and computing preparation, Boise's emphasis prerequisites, Alabama's exact bachelor's-entry treatment, and FIU's upper-division GPA and mathematics rules require transcript-level review.
- NDSU, Boise, Alabama, and FIU publish assistantship mechanisms, but awards are competitive; Boise and FIU also leave post-first-year funding dependent on an advisor.
- Ontario Tech, Carleton, uOttawa, and Windsor publish research-master's support mechanisms, but international eligibility, supervisor commitments, package duration, and net cost remain unresolved.
- Saarland, Passau, and TU Berlin avoid regular tuition but leave curriculum, language, semester-charge, and living-cost funding questions; Trento's tuition waiver and stipend are limited and merit-ranked.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are NDSU's GPA and preparation gate, Boise and FIU's continuation funding, whether any Canadian MASc package clears international net cost, and whether the European routes combine transcript equivalency with viable living-cost funding.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_06.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_06_candidates.csv`
- `data/processed/pass2/stage_02_reentry_06_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
