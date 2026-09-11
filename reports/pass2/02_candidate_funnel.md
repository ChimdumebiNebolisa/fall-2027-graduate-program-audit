# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 07 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 07 | After re-entry 08 |
| --- | --- | --- |
| Funnel rows | 2049 | 2061 |
| Advance to Stage 3 | 167 | 179 |
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
| PhD | 7 |
| Thesis or research master's | 5 |

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | University of Cincinnati-Main Campus | [Ph.D. in Computer Science and Engineering](https://www.ceas.uc.edu/academics/departments/electrical-computer-engineering/degrees-programs/computer-science-engineering-phd.html) | PhD | high | Fall 2027 cycle/foreign-degree and prerequisite equivalency/English requirement/assistantship duration and renewal/fees and net cost/current supervisor capacity |
| us | Virginia Commonwealth University | [Doctor of Philosophy in Computer Science](https://bulletin.vcu.edu/graduate/school-engineering/computer-science/computer-science-phd/) | PhD | high | Fall 2027 cycle/transcript and prerequisite mapping/English evidence/faculty-advisor alignment/assistantship award and renewal/health insurance and net cost |
| us | Missouri University of Science and Technology | [Doctor of Philosophy in Computer Science](https://cs.mst.edu/graduate-degrees/phd/) | PhD | high | Fall 2027 cycle/direct-entry standing/GRE and English requirements/advisor interest/unrestricted funding package/fees and net cost |
| us | University of North Texas | [Ph.D. in Computer Science and Engineering](https://www.unt.edu/academics/programs/computer-science-and-engineering-phd.html) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English evidence/assistantship competitiveness/tuition and fees/current supervisor capacity |
| canada | Memorial University of Newfoundland | [PhD in Computer Science](https://www.mun.ca/computerscience/graduate-students/graduate-programs/phd/) | PhD | high | Fall 2027 cycle/master's equivalency/English evidence/secured supervisor financing/funding duration and composition/international tuition and net cost |
| canada | University of Guelph | [PhD in Computer Science](https://www.uoguelph.ca/programs/phd-computer-science) | PhD | high | live Computer Science title versus Computational Sciences calendar title/Fall 2027 cycle/thesis-master's or exceptional-entry qualification/advisor alignment/English evidence/funding duration and international net cost |
| canada | Toronto Metropolitan University | [PhD in Computer Science](https://www.torontomu.ca/graduate/programs/computer-science/) | PhD | high | Fall 2027 cycle/research-master's equivalency/English evidence/international base funding/tuition and net cost/current supervisor capacity |
| canada | École Polytechnique de Montréal | [Research Master's in Computer Engineering - Software Engineering Option](https://www.polymtl.ca/gigl/en/programs-offered/graduate-studies) | Thesis or research master's | high | Fall 2027 cycle/degree and language equivalency/French-learning condition/supervisor acceptance/project-specific funding/international tuition and net cost |
| europe | University of Oulu | [Master's in Software Engineering and Information Systems](https://www.oulu.fi/en/apply/masters-software-engineering-and-information-systems) | Thesis or research master's | high | January 2027 application terms/transcript and subject equivalency/English evidence/second-year waiver conditions/thesis scholarship availability/tuition and living-cost sufficiency |
| europe | University of Stuttgart | [Computer Science M.Sc.](https://www.uni-stuttgart.de/en/study/study-programs/Computer-Science-M.Sc-00007./) | Thesis or research master's | medium | Fall 2027 cycle/subject and credit equivalency/English evidence/profile availability/competitive scholarship eligibility/semester contribution and living costs |
| europe | University of Antwerp | [Master of Computer Science: Software Engineering](https://www.uantwerpen.be/en/study/programmes/all-programmes/master-software-engineering/programme-info/) | Thesis or research master's | high | 2027 intake/degree and prerequisite equivalency/English evidence/tuition-fee reduction selection/external scholarship eligibility/living-cost funding |
| europe | University of Groningen | [MSc Computing Science - Software Engineering and Distributed Systems](https://www.rug.nl/masters/computing-science/?lang=en) | Thesis or research master's | high | Fall 2027 cycle/international degree and subject equivalency/English evidence/SEDS track enrollment/scholarship nomination/institutional tuition and living costs |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 347 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Cincinnati-Main Campus | registry_only_signals_not_promoted_to_exact_program_review | false_negative_corrected | us:ipeds:201885:program:phd:ph-d-in-computer-science-and-engineering |
| University of Antwerp | outside_bounded_positive_seed_screen | false_negative_corrected | ror:008x57b05:program:thesis-or-research-master-s:master-of-computer-science-software-engineering |

University of Cincinnati-Main Campus and University of Antwerp were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2050 | 168 | 0.211 |
| official_program_or_department_signal | 1984 | 188 | 178 | 0.947 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6928 | 56 | 16 | 0.286 |
| lab_or_center_signal | 76 | 75 | 75 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1881 | 128 | 125 | 0.977 |
| underrepresented_route_search | 1870 | 194 | 109 | 0.985 |

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
| reentry08::bounded_reentry_has_exact_routes | PASS |
| reentry08::reentry_covers_all_regions | PASS |
| reentry08::research_masters_reentry_present | PASS |
| reentry08::doctoral_reentry_present | PASS |
| reentry08::all_candidates_advance_only_to_stage_3 | PASS |
| reentry08::all_candidates_have_exact_official_program_urls | PASS |
| reentry08::all_candidates_have_official_institution_urls | PASS |
| reentry08::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry08::all_candidate_source_ids_resolve | PASS |
| reentry08::all_sources_are_official_https | PASS |
| reentry08::program_ids_unique_after_merge | PASS |
| reentry08::all_reentry_candidates_present_after_merge | PASS |
| reentry08::known_seed_adjacency_retained | PASS |
| reentry08::confirmed_false_negatives_reaudited | PASS |
| reentry08::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 08 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2049 rows while the expanded funnel has 2061. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Cincinnati, VCU, Missouri S&T, and UNT require transcript-level entry review; their doctoral support signals range from a published first-year package to competitive, advisor-dependent assistantships.
- Memorial, Guelph, Toronto Metropolitan, and Polytechnique Montréal require degree-equivalency, supervisor, international-package, and net-cost verification even where a funding mechanism is published.
- Oulu, Stuttgart, Antwerp, and Groningen require curriculum and language mapping plus a viable tuition and living-cost plan; waivers and scholarships are partial, restricted, or highly competitive.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the U.S. transcript and funding conditions, whether any Canadian MASc package clears international net cost, and whether the European routes combine transcript equivalency with viable living-cost funding.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_08.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_08_candidates.csv`
- `data/processed/pass2/stage_02_reentry_08_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
