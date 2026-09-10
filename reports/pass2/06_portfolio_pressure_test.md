# Pass 2 Stage 6 — Portfolio construction and pressure test

Generated: 2026-09-10T20:24:04.440908+00:00

Decision: **PASS — RETURN_TO_CANDIDATE_DISCOVERY**

## Outcome

All 45 scored programs across 42 universities received a preliminary disposition and all ten pressure-test answers (450 answers total). The evidence supports 0 core, 0 reserve, 7 monitor, and 38 do-not-apply programs.

The core is intentionally empty. Every hard-gate survivor still has `Insufficient evidence` for strategic admission calibration and a single-professor dependency. Stage 6 therefore returns to candidate discovery instead of padding a 12–16 application target or relabeling a program as Plausible.

## Preliminary active portfolio

| List | Institution | Program | Score | Plausibility | Verified strong professors |
| --- | --- | --- | --- | --- | --- |
| monitor | Washington University in St Louis | Computer Science PhD | 75 | Insufficient evidence | 1 |
| monitor | University of Massachusetts-Amherst | Computer Science PhD | 73 | Insufficient evidence | 1 |
| monitor | Virginia Polytechnic Institute and State University | Computer Science PhD | 73 | Insufficient evidence | 1 |
| monitor | Carnegie Mellon University | Software Engineering PhD | 70 | Insufficient evidence | 1 |
| monitor | Northeastern University | Computer Science PhD | 70 | Insufficient evidence | 1 |
| monitor | University of Illinois Urbana-Champaign | Computer Science PhD | 68 | Insufficient evidence | 1 |
| monitor | University of Michigan-Ann Arbor | Computer Science and Engineering PhD | 68 | Insufficient evidence | 1 |

## Active portfolio composition

| Dimension | Category | Count |
| --- | --- | --- |
| degree type | PhD | 7 |
| region | us | 7 |
| funding type | verified support with material cost gaps | 7 |
| plausibility category | Insufficient evidence | 7 |

## Do-not-apply list

| Institution | Program | Failed hard gates | Diagnostic score |
| --- | --- | --- | --- |
| Iowa State University | Computer Science PhD | funding | 65 |
| University of Notre Dame | Computer Science and Engineering PhD | funding | 65 |
| Case Western Reserve University | Computer Science PhD | funding | 63 |
| North Carolina State University at Raleigh | Computer Science PhD | funding | 63 |
| Pennsylvania State University-Main Campus | Computer Science and Engineering PhD | funding | 63 |
| Purdue University-Main Campus | Computer Science PhD | funding | 63 |
| The University of Texas at Austin | Computer Science PhD | funding | 63 |
| University of Maryland-College Park | Computer Science PhD | funding | 63 |
| William & Mary | Computer Science PhD | funding | 63 |
| University of California-Davis | Computer Science PhD | funding | 60 |
| Vanderbilt University | Computer Science PhD | funding | 60 |
| Rochester Institute of Technology | Computing and Information Sciences PhD | funding | 58 |
| The University of Texas at Dallas | Computer Science PhD | funding | 58 |
| University of California-Irvine | Software Engineering PhD | funding | 55 |
| George Mason University | Computer Science PhD | funding | 53 |
| Oregon State University | Computer Science PhD | funding | 53 |
| Georgia Institute of Technology-Main Campus | Computer Science PhD | funding | 45 |
| University of Nebraska-Lincoln | Computer Science PhD | funding, eligibility | 43 |
| ETH Zurich | Direct Doctorate in Computer Science | funding, professor | 25 |
| Trinity College Dublin | PhD in Computer Science and Statistics | funding, professor | 25 |
| University of British Columbia | MSc in Computer Science (research) | funding, professor | 25 |
| Concordia University | Master of Computer Science (thesis) | funding, professor | 23 |
| McGill University | MSc in Computer Science (thesis) | funding, professor | 20 |
| Queen’s University | MSc in Computing (research pattern) | funding, professor | 20 |
| Saarland University | Saarbrücken Graduate School of Computer Science | funding, professor | 20 |
| University College London | Computer Science MPhil/PhD | funding, professor | 20 |
| University of Alberta | MSc in Computing Science (thesis) | funding, professor | 20 |
| University of Calgary | MSc in Computer Science (thesis) | funding, professor | 20 |
| University of Cambridge | PhD in Computer Science | funding, professor | 20 |
| University of Edinburgh | PhD Informatics | funding, professor | 20 |
| University of Oxford | DPhil in Computer Science | funding, professor | 20 |
| University of Saskatchewan | MSc in Computer Science (thesis) | funding, professor | 20 |
| University of Toronto | PhD in Computer Science (PhD U) | funding, professor | 20 |
| University of Victoria | MSc in Computer Science (thesis) | funding, professor | 20 |
| University of Waterloo | MMath in Computer Science (thesis) | funding, professor | 20 |
| University of British Columbia | PhD Track via MSc | funding, professor | 18 |
| University of Waterloo | PhD in Computer Science (direct from bachelor's exception) | funding, professor | 15 |
| University of Calgary | PhD in Computer Science (without completed MSc) | funding, professor, eligibility | 10 |

## Pressure-test coverage

| Question | Prompt | Assessments across 45 programs |
| --- | --- | --- |
| 1 | Is there at least one genuinely relevant research program? | pass: 45 |
| 2 | Are there current, verified professor matches? | fail: 20, pass: 25 |
| 3 | Is the department deeper than a single professor, or is that dependency worth the risk? | fail: 20, risk: 25 |
| 4 | Is funding credible for this applicant and degree type? | fail: 38, pass: 7 |
| 5 | Is the applicant formally eligible? | fail: 2, pass: 43 |
| 6 | What evidence supports the strategic plausibility category? | fail: 2, unresolved: 43 |
| 7 | Would the applicant prefer this opportunity over another already retained? | fail: 38, unresolved: 7 |
| 8 | Is the application fee and effort justified? | fail: 38, unresolved: 7 |
| 9 | Could one professor or administrator reply materially change the decision? | yes: 45 |
| 10 | What new evidence would cause the recommendation to change? | actionable: 45 |

The complete answer text and resolving Stage 5 score-evidence IDs are stored with every program in `data/processed/pass2/portfolio.json`.

## Acceptance checks

| Assertion | Result |
| --- | --- |
| all_scored_programs_receive_one_disposition | PASS |
| every_university_has_exactly_one_primary_program | PASS |
| primary_program_selection_uses_evidence_not_prestige | PASS |
| every_program_answers_all_ten_pressure_questions | PASS |
| pressure_test_evidence_ids_resolve | PASS |
| every_active_selection_passes_all_hard_gates | PASS |
| every_hard_gate_survivor_is_preserved | PASS |
| failed_gate_programs_are_do_not_apply | PASS |
| one_active_program_per_university_unless_second_rule_verified | PASS |
| active_second_programs_are_independently_compelling_and_simultaneous_verified | PASS |
| core_is_quality_limited_not_quota_filled | PASS |
| lottery_cap_enforced | PASS |
| lottery_plus_reach_share_within_one_third | PASS |
| plausibility_labels_are_unchanged | PASS |
| insufficient_calibration_returns_to_discovery_instead_of_padding | PASS |
| all_required_preliminary_lists_exist | PASS |
| composition_reports_all_required_dimensions | PASS |
| active_composition_reconciles | PASS |
| all_disposition_composition_reconciles | PASS |

## Blockers

None prevented Stage 6 completion. The lack of an evidence-supported core is the policy result required by the plan, not a reason to pad the list.

## Unresolved coverage

- All 7 monitor programs have only one verified strong professor and need either a verified second match or persuasive availability confirmation.
- All 7 monitor programs lack evidence adequate for a strategic Competitive/Plausible/Reach calibration.
- 38 programs fail at least one hard gate and remain do-not-apply until direct official evidence resolves every failure.
- Applicant preference among the 7 monitor opportunities is not directly verified.
- Offer-specific funding, fee, health-insurance, summer, and duration gaps remain where recorded in Stage 5 evidence.
- Candidate discovery must find additional hard-gate-clearing, strategically calibrated options before a quality-first core can be recommended.
