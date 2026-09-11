# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 17 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 17 | After re-entry 18 |
| --- | --- | --- |
| Funnel rows | 2169 | 2181 |
| Advance to Stage 3 | 287 | 299 |
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
| us | Arizona State University Campus Immersion | [Computer Science, PhD](https://degrees.asu.edu/masters-phd/major/ASU00/ESCOMSCPHD/computer-science-phd/) | PhD | high | official last-60-hour GPA calculation/course prerequisites/English evidence/Fall 2027 cycle/advisor capacity/written assistantship offer/tuition, fees, insurance, summer support, and net funding |
| us | Portland State University | [Doctoral Degree in Computer Science (Ph.D.)](https://web.cs.pdx.edu/phd-doctoral-degree-in-cs/) | PhD | high | Fall 2027 deadline/transcript and prerequisite mapping/English evidence/advisor capacity/guaranteed-funding offer/funding after year one/summer support, insurance, and net cost |
| us | Rensselaer Polytechnic Institute | [Ph.D. in Computer Science](https://compsci.rpi.edu/programs/phd-computer-science) | PhD | high | Fall 2027 cycle/credential and prerequisite mapping/English evidence/advisor capacity/whether an admission offer includes guaranteed support/fees, insurance, conditions, and net funding |
| us | Southern Methodist University | [Ph.D. in Computer Science](https://www.smu.edu/lyle/departments/cs/doctoral-programs) | PhD | medium | Fall 2027 cycle/credential and prerequisite review/English evidence/advisor capacity/department funding prevalence/individual fellowship or assistantship award/summer, fees, insurance, and net funding |
| us | Texas A&M University-College Station | [Doctor of Philosophy in Computer Science](https://engineering.tamu.edu/cse/academics/degrees/graduate/phd-cs.html) | PhD | high | Fall 2027 cycle/credential and prerequisite equivalency/English evidence/advisor capacity/assistantship selection/nonresident tuition treatment/stipend, summer, insurance, and net funding |
| us | Howard University | [Computer Science (Ph.D.)](https://gs.howard.edu/index.php/computer-science-phd) | PhD | high | credential and prerequisite mapping/English evidence/assistantship application requirements/department funding availability/advisor capacity/tuition, stipend, duration, summer, fees, insurance, and net funding |
| canada | Simon Fraser University | [Master of Applied Science in Engineering Science](https://www.sfu.ca/fas/study/future-graduates/programs/master-applied-science.html) | Thesis or research master's | high | Fall 2027 cycle/degree and subject equivalency/English evidence/supervisor commitment and capacity/minimum package value/international tuition, fees, insurance, living costs, and net funding |
| canada | Concordia University | [Electrical and Computer Engineering (MASc)](https://www.concordia.ca/academics/graduate/electrical-engineering-masc.html) | Thesis or research master's | high | Fall 2027 cycle/degree and course equivalency/English evidence/supervisor capacity/package amount and duration/international tuition and fees/insurance, living costs, and net funding |
| canada | Ontario Tech University | [Electrical and Computer Engineering (MASc)](https://gradstudies.ontariotechu.ca/future_students/programs/masters_programs/electrical_and_computer_engineering/index.php) | Thesis or research master's | high | CS degree equivalency to relevant engineering/Fall 2027 cycle/English evidence/supervisor commitment/international minimum package/tuition, fees, insurance, living costs, and net funding |
| europe | Lappeenranta-Lahti University of Technology | [Erasmus Mundus Joint Master's Programme Software Engineers for Green Deal (SE4GD+)](https://www.lut.fi/en/studies/tekniikka/erasmus-mundus-masters-programme-software-engineers-green-deal) | Thesis or research master's | medium | 2027 intake and application window/exact bachelor's-credit eligibility/English evidence/scholarship availability and selection/participation fee/travel, visa, insurance, living costs, and net funding/thesis allocation and supervision |
| europe | Saarland University | [Computer Science (M.Sc.)](https://www.uni-saarland.de/en/study/programmes/master/informatics.html) | Thesis or research master's | high | Fall 2027 cycle/course-credit equivalency/C1 English evidence/application ranking/scholarship eligibility and selection/semester contribution, insurance, living costs, and net funding/thesis supervisor and topic |
| europe | Chalmers University of Technology | [Software Engineering, MSc](https://www.chalmers.se/en/education/find-masters-programme/software-engineering-msc/) | Thesis or research master's | high | transcript-level prerequisite mapping/English evidence/scholarship application and selection/tuition balance/living costs, insurance, visa, travel, and net funding/research specialization and thesis supervision |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 467 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Portland State University | mechanical_signal_without_exact_doctoral_route | false_negative_corrected | us:ipeds:209807:program:phd:doctoral-degree-in-computer-science-ph-d |
| Rensselaer Polytechnic Institute | outside_bounded_positive_seed_screen | false_negative_corrected | us:ipeds:194824:program:phd:ph-d-in-computer-science |

Portland State University and Rensselaer Polytechnic Institute were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2161 | 279 | 0.251 |
| official_program_or_department_signal | 2106 | 308 | 298 | 0.968 |
| recent_paper_signal | 1649 | 907 | 76 | 0.363 |
| current_faculty_topic_signal | 6933 | 64 | 24 | 0.375 |
| lab_or_center_signal | 90 | 91 | 91 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1977 | 224 | 221 | 0.987 |
| underrepresented_route_search | 1871 | 289 | 204 | 0.990 |

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
| reentry18::bounded_reentry_has_exact_routes | PASS |
| reentry18::reentry_covers_all_regions | PASS |
| reentry18::research_masters_reentry_present | PASS |
| reentry18::doctoral_reentry_present | PASS |
| reentry18::all_candidates_advance_only_to_stage_3 | PASS |
| reentry18::all_candidates_have_exact_official_program_urls | PASS |
| reentry18::all_candidates_have_official_institution_urls | PASS |
| reentry18::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry18::all_candidate_source_ids_resolve | PASS |
| reentry18::all_sources_are_official_https | PASS |
| reentry18::program_ids_unique_after_merge | PASS |
| reentry18::all_reentry_routes_are_net_new | PASS |
| reentry18::all_reentry_candidates_present_after_merge | PASS |
| reentry18::known_seed_adjacency_retained | PASS |
| reentry18::confirmed_false_negatives_reaudited | PASS |
| reentry18::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 18 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2169 rows while the expanded funnel has 2181. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

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

- `data/raw/pass2/stage_02_reentry_18.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_18_candidates.csv`
- `data/processed/pass2/stage_02_reentry_18_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
