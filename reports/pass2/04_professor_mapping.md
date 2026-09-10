# Pass 2 Stage 4 — Professor and department fit mapping

Generated: 2026-09-10T22:47:47.875271+00:00

Decision: **PASS**

## Outcome

All 63 faculty-review-ready programs were searched against a current official faculty roster or department research-area listing. Exactly five plausible candidates were evaluated for each program (315 program-candidate evaluations; 300 distinct people after university-level deduplication).

The defensible retained set contains 42 program-match rows representing 42 distinct professors. Each program has one fully verified strong match in 42 programs; the other 21 programs have no match that clears every evidence gate. One-match programs receive 5 depth points and zero-match programs receive 0. No individual professor score exists in the Stage 4 outputs.

## Coverage

| Region | Serious programs | Retained match rows |
| --- | --- | --- |
| us | 41 | 40 |
| canada | 15 | 2 |
| europe | 7 | 0 |
| Total | 63 | 42 |

## Department-depth result

| Verified strong matches per program | Programs | Depth points | Single-professor dependency |
| --- | --- | --- | --- |
| 0 | 21 | 0 | false |
| 1 | 42 | 5 | true |
| 2 | 0 | 10 | false |
| 3+ | 0 | 15 | false |

University-level counts use `professor_id`, so the same person attached to multiple UBC, Calgary, or Waterloo routes is counted once.

## Retained matches

| Region | Institution | Program | Professor | Depth | Recruiting status |
| --- | --- | --- | --- | --- | --- |
| canada | Simon Fraser University | Master of Science in Computing Science — Thesis Option | Saba Alimadadi | 5 | Confirmed recruiting |
| canada | York University | Master of Science in Computer Science — Thesis Option | Zhen Ming (Jack) Jiang | 5 | Confirmed recruiting |
| us | Boston University | PhD in Computer Science | Ankush Das | 5 | Confirmed recruiting |
| us | Brown University | Computer Science PhD | Malte Schwarzkopf | 5 | Recruiting status unknown |
| us | Carnegie Mellon University | Software Engineering PhD | Claire Le Goues | 5 | Recruiting status unknown |
| us | Case Western Reserve University | Computer Science PhD | Sumon Biswas | 5 | Recruiting status unknown |
| us | Duke University | Computer Science PhD | Danfeng Zhang | 5 | Recruiting status unknown |
| us | George Mason University | Computer Science PhD | Brittany Johnson-Matthews | 5 | Recruiting status unknown |
| us | Georgia Institute of Technology-Main Campus | Computer Science PhD | Alessandro Orso | 5 | Recruiting status unknown |
| us | Iowa State University | Computer Science PhD | Myra Cohen | 5 | Recruiting status unknown |
| us | North Carolina State University at Raleigh | Computer Science PhD | Kathryn Stolee | 5 | Recruiting status unknown |
| us | Northeastern University | Computer Science PhD | Jonathan Bell | 5 | Recruiting status unknown |
| us | Ohio State University-Main Campus | Doctor of Philosophy in Computer Science and Engineering | Zhiqiang Lin | 5 | Confirmed recruiting |
| us | Oregon State University | Computer Science PhD | Manish Motwani | 5 | Recruiting status unknown |
| us | Pennsylvania State University-Main Campus | Computer Science and Engineering PhD | Gang Tan | 5 | Recruiting status unknown |
| us | Purdue University-Main Campus | Computer Science PhD | Lin Tan | 5 | Recruiting status unknown |
| us | Rochester Institute of Technology | Computing and Information Sciences PhD | Yinxi Liu | 5 | Confirmed recruiting |
| us | Rutgers University-New Brunswick | Computer Science (Ph.D.), New Brunswick | Santosh Nagarakatte | 5 | Recruiting status unknown |
| us | Stony Brook University | PhD in Computer Science | Dongyoon Lee | 5 | Confirmed recruiting |
| us | The University of Texas at Austin | Computer Science PhD | Isil Dillig | 5 | Recruiting status unknown |
| us | The University of Texas at Dallas | Computer Science PhD | W. Eric Wong | 5 | Recruiting status unknown |
| us | University of Arizona | Computer Science PhD | Roberto Giacobazzi | 5 | Recruiting status unknown |
| us | University of California-Davis | Computer Science PhD | Cindy Rubio-González | 5 | Recruiting status unknown |
| us | University of California-Irvine | Software Engineering PhD | Joshua Garcia | 5 | Recruiting status unknown |
| us | University of California-San Diego | Computer Science and Engineering PhD | Nadia Polikarpova | 5 | Recruiting status unknown |
| us | University of California-Santa Barbara | Doctor of Philosophy in Computer Science | Tevfik Bultan | 5 | Recruiting status unknown |
| us | University of Colorado Boulder | Doctor of Philosophy in Computer Science | Sriram Sankaranarayanan | 5 | Confirmed recruiting |
| us | University of Delaware | Ph.D. in Computer Science | Stephen F. Siegel | 5 | Confirmed recruiting |
| us | University of Illinois Urbana-Champaign | Computer Science PhD | Lingming Zhang | 5 | Recruiting status unknown |
| us | University of Maryland-College Park | Computer Science PhD | David Van Horn | 5 | Recruiting status unknown |
| us | University of Massachusetts-Amherst | Computer Science PhD | Yuriy Brun | 5 | Recruiting status unknown |
| us | University of Michigan-Ann Arbor | Computer Science and Engineering PhD | Westley Weimer | 5 | Recruiting status unknown |
| us | University of Minnesota-Twin Cities | PhD in Computer Science | Kangjie Lu | 5 | Confirmed recruiting |
| us | University of Nebraska-Lincoln | Computer Science PhD | Hamid Bagheri | 5 | Recruiting status unknown |
| us | University of North Carolina at Charlotte | Ph.D. in Computing and Information Systems — Software and Information Systems Track | Jinpeng Wei | 5 | Recruiting status unknown |
| us | University of Notre Dame | Computer Science and Engineering PhD | Joanna Cecilia da Silva Santos | 5 | Recruiting status unknown |
| us | University of Utah | Computing PhD | John Regehr | 5 | Recruiting status unknown |
| us | University of Wisconsin-Madison | Computer Sciences, PhD | Aws Albarghouthi | 5 | Recruiting status unknown |
| us | Vanderbilt University | Computer Science PhD | Kevin Leach | 5 | Recruiting status unknown |
| us | Virginia Polytechnic Institute and State University | Computer Science PhD | Na Meng | 5 | Recruiting status unknown |
| us | Washington University in St Louis | Computer Science PhD | Umar Iqbal | 5 | Recruiting status unknown |
| us | William & Mary | Computer Science PhD | Denys Poshyvanyk | 5 | Recruiting status unknown |

## Good-faith fewer-than-three record

For every program, four additional current-roster candidates were evaluated. They remain in `professor_candidates_evaluated.csv` as plausible, unscored candidates. None was promoted merely from department membership, biography keywords, publication-time affiliation, or fame. A candidate was retained only when the evidence simultaneously established a current appointment, authority to supervise the exact program, specific strong research overlap, and at least one recent work/project with URL and year.

Recent-work metadata was available for 102 of 315 candidate evaluations. Discovery-only OpenAlex records never establish appointment, supervision, or recruiting.

## Recruiting and contact controls

Recruiting is `Confirmed recruiting` only when the retained evidence explicitly says so; otherwise the controlled status from the verified regional record is preserved. Research activity is not treated as recruiting. Prospective-student instructions and contact appropriateness are recorded separately from fit.

## Acceptance checks

| Assertion | Result |
| --- | --- |
| all_serious_programs_covered | PASS |
| at_least_five_candidates_per_serious_program | PASS |
| no_more_than_three_matches_per_program | PASS |
| good_faith_fewer_recorded | PASS |
| retained_matches_have_current_appointments | PASS |
| retained_matches_have_verified_supervision_authority | PASS |
| retained_matches_have_recent_work_evidence | PASS |
| retained_matches_are_strong_and_verified | PASS |
| recruiting_statuses_are_controlled | PASS |
| no_professor_score_columns_exist | PASS |
| faculty_depth_rule_enforced | PASS |
| university_level_people_deduplicate | PASS |
| all_candidate_source_ids_resolve | PASS |
| official_roster_source_per_program | PASS |
| required_output_schemas_exact | PASS |

## Blockers

None prevented Stage 4 completion.

## Unresolved coverage

- Stage 4 re-entry 02 evaluated 8 newly eligible routes and retained 8 fully verified strong lead matches; 0 new route remains without a retained match. Across both re-entry batches, 17 of 18 routes have a retained match.
- UVA's strongest bounded fit has a current courtesy Computer Science appointment, but exact Computer Science PhD supervision authority was not verified; the candidate remains unscored and unretained.
- 42 of 63 programs have only one fully verified strong match and remain single-professor dependencies.
- 21 programs have no candidate that clears every current-appointment, supervision-authority, strong-fit, and recent-work gate; their faculty depth is 0.
- 273 plausible program-candidate evaluations were not retained because exact-route supervision authority and/or candidate-specific recent-work evidence remains incomplete.
- Official email remains unlocated for 6 retained professors and most unretained candidates; no address is guessed.
- Recruiting status remains unknown unless a current direct statement/opening was already verified; publication activity and open labs are not used as recruiting proxies.
- Faculty appointments, supervision rules, and recruiting statements are time-sensitive and require a refresh immediately before outreach or application submission.
- Stage 5 scoring still covers the prior 55-program roster. Its eight-route coverage gap is intentionally unresolved at this stage boundary and must be rebuilt in Stage 5 re-entry 02.
- Stage 5 may use only the 5-point faculty-depth values supported here; it may not resurrect the inflated Pass 1 depth scores.
