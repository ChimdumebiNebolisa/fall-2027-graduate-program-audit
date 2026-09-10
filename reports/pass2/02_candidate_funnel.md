# Pass 2 Stage 2 — High-recall candidate funnel

Date: 2026-09-10
Decision: **PASS — discovery re-entry 01 complete**

## Outcome

Stage 6 returned the workflow to discovery because the verified portfolio had no hard-gate survivor with a strategically usable plausibility calibration. This bounded re-entry adds exact official research routes only. It does not score, rank, or verify programs, funding, or faculty.

| Measure | Initial Stage 2 | After re-entry |
| --- | --- | --- |
| Funnel rows | 1965 | 1977 |
| Advance to Stage 3 | 83 | 95 |
| Catalog verification required | 253 | 253 |
| Manual secondary review | 11 | 11 |
| Screened out | 1618 | 1618 |
| Active rows missing exact program URL | documented | 264 |
| Curated re-entry source records | 0 | 32 |

## Exact routes added

| Region | Institution | Exact route | Degree | Confidence | Still unresolved |
| --- | --- | --- | --- | --- | --- |
| us | University of Wisconsin-Madison | [Computer Sciences PhD](https://guide.wisc.edu/graduate/computer-sciences/computer-sciences-phd/) | PhD | high | Fall 2027 cycle/international credential equivalency/individual funding guarantee/current faculty supervision |
| us | University of Minnesota-Twin Cities | [Computer Science PhD](https://cse.umn.edu/cs/phd-admissions) | PhD | high | Fall 2027 cycle/international transcript equivalency/current faculty supervision/offer-specific net funding |
| us | University of Colorado Boulder | [Computer Science PhD](https://www.colorado.edu/cs/academics/graduate-programs/doctor-philosophy) | PhD | high | Fall 2027 cycle/international credential equivalency/summer funding/current faculty supervision |
| us | University of Arizona | [Computer Science PhD](https://cs.arizona.edu/graduate/prospective-students) | PhD | high | bachelor's-entry eligibility/Fall 2027 cycle/international credential equivalency/current faculty supervision |
| us | University at Buffalo | [Computer Science and Engineering PhD](https://engineering.buffalo.edu/computer-science-engineering/graduate/degrees-and-programs/phd-in-computer-science-and-engineering.html) | PhD | high | committee approval for bachelor's entry/Fall 2027 cycle/funding incidence/current faculty supervision |
| us | University of Utah | [Computing PhD](https://www.cs.utah.edu/graduate/academic-programs/ms-and-phd-programs/) | PhD | medium | bachelor's-entry eligibility/Fall 2027 cycle/international requirements/funding/current faculty supervision |
| us | University of California-San Diego | [Computer Science and Engineering PhD](https://cse.ucsd.edu/graduate/doctoral-programs-computer-science-and-engineering) | PhD | high | Fall 2027 cycle/international credential equivalency/multi-year funding continuity/current faculty supervision |
| us | Duke University | [Computer Science PhD](https://cs.duke.edu/graduate/phd) | PhD | high | bachelor's-entry eligibility/Fall 2027 cycle/international requirements/current faculty supervision/offer-specific funding |
| us | Brown University | [Computer Science PhD](https://cs.brown.edu/degrees/doctoral/) | PhD | high | bachelor's-entry eligibility/Fall 2027 cycle/international requirements/funding duration/current faculty supervision |
| us | University of Virginia-Main Campus | [Computer Science PhD](https://engineering.virginia.edu/department/computer-science/academics/graduate-programs/phd-computer-science) | PhD | high | bachelor's-entry eligibility/Fall 2027 cycle/international requirements/funding continuity/current faculty supervision |
| canada | Simon Fraser University | [Computing Science Master of Science (Thesis)](https://www.sfu.ca/fas/study/future-graduates/programs/master-science-thesis.html) | Thesis or research master's | high | Fall 2027 cycle/international degree equivalency/supervisor match/offer-specific net funding/current faculty supervision |
| europe | Chalmers University of Technology | [Computer Science MSc](https://www.chalmers.se/en/education/find-masters-programme/computer-science-msc/) | Thesis or research master's | high | degree-specific eligibility/tuition status/scholarship funding/living-cost adequacy/current faculty supervision |

The 12 routes include 10 U.S. PhDs and two thesis/research master's routes (one Canadian and one European). Every route has at least two official source records and an explicit preliminary eligibility, funding, and research-fit signal.

## Coverage after re-entry

| Region | Funnel rows |
| --- | --- |
| canada | 44 |
| europe | 99 |
| us | 1834 |

| Priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 47 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 264 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

## False-negative audit

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Simon Fraser University | official_inventory_no_research_computing_route | false_negative_corrected | ca:dli:O18781994282:program:thesis-or-research-master-s:computing-science-master-of-science-thesis |
| Chalmers University of Technology | outside_bounded_positive_seed_screen | false_negative_corrected | ror:040wg7k59:program:thesis-or-research-master-s:computer-science-msc |

Simon Fraser was missing from the candidate funnel despite being present in the Canadian institution universe. Chalmers remained an unresolved catalog placeholder. Both are now explicitly recorded as corrected false negatives and promoted only to Stage 3 verification.

## Discovery-source yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 1966 | 84 | 0.177 |
| official_program_or_department_signal | 1858 | 104 | 94 | 0.904 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6923 | 51 | 11 | 0.216 |
| lab_or_center_signal | 59 | 58 | 58 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1842 | 82 | 79 | 0.963 |
| underrepresented_route_search | 1846 | 128 | 43 | 0.977 |

## Acceptance checks

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
| reentry::bounded_reentry_has_exact_routes | PASS |
| reentry::reentry_covers_all_regions | PASS |
| reentry::research_masters_reentry_present | PASS |
| reentry::doctoral_reentry_present | PASS |
| reentry::all_candidates_advance_only_to_stage_3 | PASS |
| reentry::all_candidates_have_exact_official_program_urls | PASS |
| reentry::all_candidates_have_official_institution_urls | PASS |
| reentry::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry::all_candidate_source_ids_resolve | PASS |
| reentry::all_sources_are_official_https | PASS |
| reentry::program_ids_unique_after_merge | PASS |
| reentry::all_reentry_candidates_present_after_merge | PASS |
| reentry::known_seed_adjacency_retained | PASS |
| reentry::confirmed_false_negatives_reaudited | PASS |
| reentry::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every incremental re-entry assertion passes. Discovery remains explicitly non-saturated; the re-entry is a bounded response to Stage 6, not an exhaustive claim.

## Blockers and unresolved coverage

- No Stage 2 blocker prevents progression to Stage 3 re-verification.
- The 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Fresh URL QA returned HTTP 200 for 30 of 32 official source records. Both remaining records are University of Virginia pages that returned an automated-access HTTP 403; their claims require fresh browser verification in Stage 3.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- Existing Stage 3–6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- The full-suite cross-stage test `test_every_stage2_candidate_has_exactly_one_controlled_status` is expected to fail until Stage 3 re-entry: verification has 1,965 rows while the expanded funnel has 1,977. Stage 2's targeted tests and acceptance assertions pass.
