# Stage 2 Result

## Decision

Pass

## What changed

Stage 6 re-entry 13 returned the workflow to discovery because the evidence-calibrated portfolio still had zero justified core applications. This bounded non-saturation pass adds 12 genuinely new exact research routes supported by current official program, research, and preliminary funding evidence. It does not score, rank, retain, or claim verified funding or faculty capacity.

| Measure | After re-entry 13 | After re-entry 14 |
| --- | --- | --- |
| Funnel rows | 2121 | 2133 |
| Advance to Stage 3 | 239 | 251 |
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
| us | University of Nebraska at Omaha | [Computing & Information Science, Ph.D.](https://www.unomaha.edu/college-of-information-science-and-technology/academics/computing_and_information_science_phd.php) | PhD | high | Fall 2027 cycle/degree and course equivalency/GRE and English evidence/assistantship selection and renewal/summer support/fees and insurance/current advisor capacity |
| us | University of Colorado Colorado Springs | [Cybersecurity, PhD](https://www.uccs.edu/academics/programs/security-phd) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GRE exception/English evidence/operational-security requirement/assistantship availability and duration/fees and insurance/current supervisor capacity |
| us | University of Massachusetts-Lowell | [Doctor of Philosophy (Ph.D.) in Computer Science](https://www.uml.edu/sciences/computer-science/programs/doctorate.aspx) | PhD | high | Fall 2027 cycle/degree and course equivalency/GRE and English evidence/advisor match/assistantship offer and duration/summer support/fees and insurance |
| us | University of Louisville | [Doctor of Philosophy in Computer Science and Engineering](https://catalog.louisville.edu/graduate/programs-study/doctor-philosophy-computer-science-engineering/) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GRE and English evidence/research-area and advisor fit/fellowship selection and renewal/summer coverage/fees and net support |
| us | Wayne State University | [Computer Science (Ph.D.)](https://bulletins.wayne.edu/graduate/college-engineering/computer-science/computer-science-phd/index.html) | PhD | high | Fall 2027 cycle/degree and prerequisite mapping/GRE and English evidence/advisor selection/assistantship availability and coverage/fees and insurance/current faculty capacity |
| us | Clarkson University | [PhD in Computer Science](https://www.clarkson.edu/academics/majors-minors/computer-science-phd) | PhD | high | Fall 2027 cycle/degree and prerequisite equivalency/GRE waiver/English evidence/advisor alignment/assistantship selection and duration/summer coverage/fees and insurance |
| canada | Université du Québec en Outaouais | [Maîtrise en informatique (profil mémoire)](https://uqo.ca/programmes/3097) | Thesis or research master's | high | Fall 2027 offering/international degree and course equivalency/French evidence/supervisor agreement/scholarship eligibility and amount/international tuition/living costs and net package |
| canada | Université du Québec à Chicoutimi | [Maîtrise en informatique - profil recherche (mémoire)](https://programmes.uqac.ca/3017) | Thesis or research master's | high | Fall 2027 cycle/degree and prerequisite equivalency/French evidence/topic and supervisor fit/tuition-exemption selection/remaining tuition and fees/living costs |
| canada | Université du Québec à Trois-Rivières | [Maîtrise en mathématiques et informatique appliquées (avec mémoire)](https://oraprdnt.uqtr.uquebec.ca/portail/triw082.afficher?owa_cd_pgm=3799&owa_version=1) | Thesis or research master's | high | Fall 2027 cycle/degree and GPA equivalency/computing and mathematics preparation/French evidence/supervisor and topic fit/assistantship or scholarship award/international tuition and living costs |
| europe | Vrije Universiteit Brussel | [Master of Science in Applied Sciences and Engineering: Computer Science - Software Systems](https://www.vub.be/en/studying-vub/all-study-programmes-vub/bachelors-and-masters-programmes-vub/master-applied-sciences-and-engineering-computer-science/program/master/master-software-systems) | Thesis or research master's | high | Fall 2027 offering and criteria/degree and subject-credit equivalency/English evidence/scholarship eligibility and selection/non-EEA tuition/living costs/research-training and thesis-group fit |
| europe | University of Southern Denmark | [Software Engineering - MSc in Engineering](https://www.sdu.dk/en/uddannelse/kandidat/softwareengineering) | Thesis or research master's | high | Fall 2027 offering and criteria/degree and course equivalency/English evidence/master's thesis and research-group fit/tuition changes/alternative scholarships/living costs and complete funding plan |
| europe | University of Klagenfurt | [Master's Degree Programme Informatics](https://www.aau.at/en/studien/master-informatics/) | Thesis or research master's | high | Fall 2027 offering and criteria/degree and course equivalency/additional examinations/B2 English evidence/scholarship eligibility and selection/future tuition and living costs/project and thesis-supervisor fit |

| Cumulative priority route bucket | Active rows |
| --- | --- |
| doctoral_bachelors_entry | 48 |
| research_masters | 35 |
| structured_or_masters_required_doctorate | 13 |
| unresolved_or_exceptional_route | 419 |

All three regions and the required doctoral and research-master route families remain represented. Inclusion was driven by exact fit and official-route evidence, not a global top-N or prestige cutoff.

### Current false-negative corrections

| Institution | Original stratum | Audit result | Correction |
| --- | --- | --- | --- |
| Université du Québec à Trois-Rivières | catalog_signal_without_exact_research_masters_route | false_negative_corrected | ca:dli:O19359011172:program:thesis-or-research-master-s:ma-trise-en-math-matiques-et-informatique-appliqu-es-avec-m-moire |
| Vrije Universiteit Brussel | outside_bounded_positive_seed_screen | false_negative_corrected | ror:006e5kg04:program:thesis-or-research-master-s:master-of-science-in-applied-sciences-and-engineering-computer-science-software-systems |

Université du Québec à Trois-Rivières and Vrije Universiteit Brussel were missed by the original bounded screen. Current official evidence corrects those omissions, but promotes the routes only to Stage 3 verification.

### Discovery-source contribution and yield

| Path | Examined | Contributed | Advanced | Active yield |
| --- | --- | --- | --- | --- |
| recognized_institution_record | 5834 | 2113 | 231 | 0.234 |
| official_program_or_department_signal | 2057 | 260 | 250 | 0.962 |
| recent_paper_signal | 1649 | 907 | 76 | 0.363 |
| current_faculty_topic_signal | 6930 | 61 | 21 | 0.344 |
| lab_or_center_signal | 87 | 88 | 88 | 1.000 |
| calendar_prior_list | 55 | 204 | 21 | 0.270 |
| first_audit_program | 56 | 57 | 57 | 1.000 |
| research_masters_or_scholarship_search | 1936 | 183 | 180 | 0.984 |
| underrepresented_route_search | 1871 | 241 | 156 | 0.988 |

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
| reentry14::bounded_reentry_has_exact_routes | PASS |
| reentry14::reentry_covers_all_regions | PASS |
| reentry14::research_masters_reentry_present | PASS |
| reentry14::doctoral_reentry_present | PASS |
| reentry14::all_candidates_advance_only_to_stage_3 | PASS |
| reentry14::all_candidates_have_exact_official_program_urls | PASS |
| reentry14::all_candidates_have_official_institution_urls | PASS |
| reentry14::all_candidates_have_fit_and_preliminary_route_fields | PASS |
| reentry14::all_candidate_source_ids_resolve | PASS |
| reentry14::all_sources_are_official_https | PASS |
| reentry14::program_ids_unique_after_merge | PASS |
| reentry14::all_reentry_routes_are_net_new | PASS |
| reentry14::all_reentry_candidates_present_after_merge | PASS |
| reentry14::known_seed_adjacency_retained | PASS |
| reentry14::confirmed_false_negatives_reaudited | PASS |
| reentry14::no_scoring_fields_introduced | PASS |

The original Stage 2 acceptance contract still passes, and every re-entry 14 assertion passes. The 12 exact program IDs are unique, all resolve to canonical institution records, all current-round source records use official HTTPS URLs, and no scoring field was introduced.

Automated source retrieval returned HTTP 200 for 24 of 24 current-round official records. Non-200 or connection exceptions are preserved in the manifest and do not erase browser-reviewed evidence.

The cross-stage control is expected to fail until the next separate Stage 3 re-entry: program verification has 2121 rows while the expanded funnel has 2133. This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.

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

- `data/raw/pass2/stage_02_reentry_14.json`
- `data/processed/pass2/candidate_program_funnel.csv`
- `data/processed/pass2/discovery_source_yield.csv`
- `data/processed/pass2/exclusion_sample_audit.csv`
- `data/processed/pass2/stage_02_reentry_14_candidates.csv`
- `data/processed/pass2/stage_02_reentry_14_sources.csv`
- `scripts/build_stage_02_reentry.py`
- `tests/test_candidate_reentry.py`
- `state/progress.json`
- `data/manifests/pass2/stage_02.json`

## Recommendation before the next stage

Begin one separate Stage 3 re-entry run for these 12 exact routes. Do not treat any preliminary funding signal, research-area match, or discovery confidence as a retention decision or funding hard-gate pass.
