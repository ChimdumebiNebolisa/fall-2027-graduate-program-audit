# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 04 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This fifth bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 04 | After re-entry 05 |
| --- | --- | --- |
| Funnel rows | 2013 | 2025 |
| Advance to Stage 3 | 131 | 143 |
| Net new exact routes | — | 12 |
| Current-round official source records | — | 31 |
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
| us | Auburn University | [PhD in Computer Science and Software Engineering](https://www.eng.auburn.edu/program/phd-computer-science-software-engineering.html) | PhD | high | Fall 2027 cycle/prerequisite and GPA review/English requirement/assistantship probability and renewal/current faculty supervision |
| us | Mississippi State University | [PhD in Computer Science](https://www.cse.msstate.edu/grad/phd-cs/) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/English requirement/assistantship award and duration/major-professor availability |
| us | University of Arkansas | [Ph.D. in Computer Science](https://catalog.uark.edu/graduatecatalog/programsofstudy/computerscienceandcomputerengineeringcsce/) | PhD | high | Fall 2027 cycle/GRE policy/prerequisite and degree equivalency/English requirement/assistantship or fellowship award/current faculty supervision |
| us | University of Alabama at Birmingham | [Ph.D. in Computer Science](https://www.uab.edu/cas/computerscience/graduate-programs/doctoral-program) | PhD | high | Fall 2027 cycle/major GPA calculation/prerequisite mapping/English requirement/offer-specific funding and renewal/current faculty supervision |
| canada | Concordia University | [Software Engineering (MASc)](https://www.concordia.ca/academics/graduate/software-engineering-masc.html) | Thesis or research master's | high | Fall 2027 cycle/degree and GPA equivalency/English requirement/supervisor requirement and capacity/offer-specific funding and net cost |
| canada | McMaster University | [Software Engineering (MASc)](https://www.eng.mcmaster.ca/cas/degree-options/software-engineering-masc/) | Thesis or research master's | high | Fall 2027 cycle/B+ and degree equivalency/English requirement/supervisor match/20-month package amount, fees, and net cost |
| canada | University of Calgary | [MSc Thesis-based in Computer Science — Software Engineering Specialization](https://calendar.ucalgary.ca/programs/CPSCSEMSCT/admissions-cMwRI) | Thesis or research master's | high | Fall 2027 cycle/software-industry experience interpretation/last-two-years GPA/degree and English equivalency/supervisor match/funding components and net cost |
| canada | University of Regina | [Master of Applied Science in Software Systems Engineering](https://www.uregina.ca/academics/programs/engineering/masters-phd-software-systems-engineering.html) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/English requirement/supervisor availability/funding award, duration, and net cost |
| europe | University of Bamberg | [M.Sc. International Software Systems Science](https://www.uni-bamberg.de/en/ma-isosysc/) | Thesis or research master's | high | Fall 2027 cycle/German grade conversion/115-ECTS curriculum mapping/GRE or GATE applicability/English evidence/living-cost funding/thesis supervision |
| europe | Technische Universität Darmstadt | [M.Sc. Computer Science](https://www.informatik.tu-darmstadt.de/studium_fb20/im_studium/studiengaenge_liste/computer_science_msc.en.jsp) | Thesis or research master's | high | Fall 2027 cycle/60-credit competency mapping/English C1 evidence/possible entrance examination/living-cost funding/thesis supervision |
| europe | University of Potsdam | [M.Sc. Computer Science](https://www.uni-potsdam.de/en/studium/what-to-study/master/computer-science) | Thesis or research master's | high | Fall 2027 cycle/ECTS and grade mapping/English evidence/selection outcome/living-cost funding/thesis supervision |
| europe | Rheinland-Pfälzische Technische Universität Kaiserslautern-Landau | [M.Sc. Computer Science](https://rptu.de/studienangebot/22777/Computer_Science-Computer_Science-master) | Thesis or research master's | high | Fall 2027 cycle/computer-science curriculum equivalency/grade conversion/English evidence/certificate evaluation and fees/living-cost funding/thesis supervision |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 311 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| University of Alabama at Birmingham | registry_only_signals_not_promoted_to_exact_program_review | false_negative_corrected | us:ipeds:100663:program:phd:ph-d-in-computer-science |
| University of Bamberg | outside_bounded_positive_seed_screen | false_negative_corrected | ror:01c1w6d29:program:thesis-or-research-master-s:m-sc-international-software-systems-science |

University of Alabama at Birmingham, and University of Bamberg were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 2014 | 132 | 0.197 |
| official_program_or_department_signal | 1933 | 152 | 142 | 0.934 |
| recent_paper_signal | 1647 | 903 | 72 | 0.360 |
| current_faculty_topic_signal | 6927 | 55 | 15 | 0.273 |
| lab_or_center_signal | 70 | 69 | 69 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 55 | 55 | 1.000 |
| research_masters_or_scholarship_search | 1858 | 101 | 98 | 0.970 |
| underrepresented_route_search | 1867 | 173 | 88 | 0.983 |

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
| reentry05::bounded_reentry_has_exact_routes | PASS |
| reentry05::reentry_covers_all_regions | PASS |
| reentry05::research_masters_reentry_present | PASS |
| reentry05::doctoral_reentry_present | PASS |
| reentry05::all_candidates_advance_only_to_stage_3 | PASS |
| reentry05::all_candidates_have_exact_official_program_urls | PASS |
| reentry05::all_candidates_have_official_institution_urls | PASS |
| reentry05::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry05::all_candidate_source_ids_resolve | PASS |
| reentry05::all_sources_are_official_https | PASS |
| reentry05::program_ids_unique_after_merge | PASS |
| reentry05::all_reentry_candidates_present_after_merge | PASS |
| reentry05::known_seed_adjacency_retained | PASS |
| reentry05::confirmed_false_negatives_reaudited | PASS |
| reentry05::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 05 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 31 of 31 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2013 rows while the expanded funnel has 2025. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

## Material uncertainties or conflicts

- No Stage 2 blocker prevents a separate Stage 3 re-verification run.
- All 12 new routes require Stage 3 checks for the fields listed in the table; preliminary funding language is not an offer or a hard-gate pass.
- 264 other active funnel rows still lack exact official program URLs and remain catalog/manual-review coverage rather than verified candidates.
- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; EHESO/ETER and several national registries remain blocked.
- Current faculty appointment, supervision authority, and capacity remain Stage 4 work after program verification.
- UAB's typical major-GPA signal and Calgary's last-two-years GPA and industry-experience conditions require transcript and requirement-level review rather than inference from cumulative GPA.
- Auburn, Mississippi State, Arkansas, and UAB publish assistantship or fellowship mechanisms, but none establishes an applicant-specific award, complete coverage, or renewal.
- Concordia and McMaster publish positive research-master's support signals and Calgary publishes a minimum level, while Regina lists mechanisms only; all require offer and net-cost verification.
- The four German routes are research-relevant, but curriculum equivalency, language evidence, semester charges, and a viable living-cost funding path remain unresolved.
- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include these routes.
- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk but does not establish exhaustive global coverage.

## Records requiring human judgment

Stage 3 must determine whether each route is actually eligible and credibly funded. The highest-impact judgments are the UAB major-GPA calculation, Calgary's experience requirement, whether Canadian funding signals clear the full net-cost gate, and whether any German route has both transcript equivalency and a viable living-cost funding path.

## Files created or modified

- `data/raw/pass2/stage_02_reentry_05.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_05_candidates.csv`
- `data/processed/pass2/stage_02_reentry_05_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
