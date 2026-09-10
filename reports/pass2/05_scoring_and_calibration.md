# Pass 2 Stage 5 — Evidence-based scoring and admission calibration

Generated: 2026-09-10T23:47:25.585438+00:00

Decision: **PASS**

## Outcome

All 71 serious Stage 4 programs were recalculated from six recorded evidence components (426 component rows). Only 16 programs clear the direct funding, verified-professor, eligibility, degree-structure, and coursework-exception gates. Gated-out rows retain diagnostic component totals but receive no evidence rank.

## Hard-gate result

| Gate | Programs passing | Programs failing |
| --- | --- | --- |
| Direct verified funding | 25 | 46 |
| Verified strong professor | 50 | 21 |
| Formal eligibility | 67 | 4 |
| All hard gates | 16 | 55 |

The funding gate is recomputed from exact-program source IDs whose source rows are official, verified, and explicitly funding-related. It never reads the Stage 3 retained/conditional label, a recommendation, total score, or funding score.

## Evidence-ranked hard-gate survivors

| Dense rank | Institution | Program | Score | Pattern | Admission calibration |
| --- | --- | --- | --- | --- | --- |
| 1 | Washington University in St Louis | Computer Science PhD | 75 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:15/15/degree_admissions_alignment:10/10/application_economics:5/5 | Insufficient evidence |
| 2 | University of Arizona | Computer Science PhD | 73 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:25/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 2 | University of Colorado Boulder | Doctor of Philosophy in Computer Science | 73 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:25/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 2 | University of Massachusetts-Amherst | Computer Science PhD | 73 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:15/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 2 | University of Minnesota-Twin Cities | PhD in Computer Science | 73 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:25/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 2 | Virginia Polytechnic Institute and State University | Computer Science PhD | 73 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:15/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 3 | Carnegie Mellon University | Software Engineering PhD | 70 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:5/5 | Insufficient evidence |
| 3 | Duke University | Computer Science PhD | 70 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:25/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:0/5 | Insufficient evidence |
| 3 | Northeastern University | Computer Science PhD | 70 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:15/15/degree_admissions_alignment:10/10/application_economics:0/5 | Insufficient evidence |
| 3 | University of Kentucky | Doctoral Degree in Computer Science | 70 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:15/15/degree_admissions_alignment:10/10/application_economics:0/5 | Insufficient evidence |
| 4 | University of Illinois Chicago | PhD in Computer Science | 68 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 4 | University of Illinois Urbana-Champaign | Computer Science PhD | 68 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 4 | University of Michigan-Ann Arbor | Computer Science and Engineering PhD | 68 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 4 | University of Utah | Computing PhD | 68 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:3/5 | Insufficient evidence |
| 5 | Brown University | Computer Science PhD | 65 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:0/5 | Insufficient evidence |
| 5 | York University | Master of Science in Computer Science — Thesis Option | 65 | professor_alignment:20/30/department_program_depth:5/15/funding_net_viability:20/25/eligibility_credential_alignment:10/15/degree_admissions_alignment:10/10/application_economics:0/5 | Insufficient evidence |

Tied totals share the same dense rank. Prestige and institution identity are not scoring inputs or tie-breakers.

## Admission calibration

67 rows are `Insufficient evidence`; 4 carry an `Eligibility concern`. The source ledger contains formal requirements but no official cohort/selectivity evidence adequate for a strategic Plausible/Reach category. Published GPA minimums remain in a separate field and never create plausibility. No admission percentage is emitted.

## Acceptance checks

| Assertion | Result |
| --- | --- |
| entire_serious_program_pool_recalculated | PASS |
| latest_reentry_03_fully_recalculated | PASS |
| exactly_six_components_per_program | PASS |
| program_rows_reference_exact_component_evidence | PASS |
| component_evidence_has_required_audit_metadata | PASS |
| component_scores_use_rubric_anchors | PASS |
| rubric_avoids_unexplained_one_point_bands | PASS |
| overall_scores_are_component_sums | PASS |
| positive_components_have_resolving_evidence | PASS |
| funding_gate_is_recomputed_from_direct_sources | PASS |
| funding_gate_ignores_labels_recommendations_and_scores | PASS |
| one_professor_depth_cap_enforced | PASS |
| duplicate_professors_do_not_inflate_depth | PASS |
| missing_or_unverifiable_evidence_reduces_confidence | PASS |
| minimum_gpa_alone_never_creates_plausible | PASS |
| no_admission_percentages_emitted | PASS |
| coursework_only_without_exceptional_funding_fails | PASS |
| only_hard_gate_survivors_receive_ranks | PASS |
| tied_totals_share_dense_rank | PASS |
| required_output_schemas_exact | PASS |
| no_institution_specific_score_constants | PASS |

## Blockers

None prevented Stage 5 completion.

## Unresolved coverage

- Stage 5 re-entry 03 recalculated 8 newly eligible routes. All 8 pass the professor gate. The direct funding gate passes for 2, and 2 clear every hard gate.
- 46 programs lack direct source evidence strong enough for the funding hard gate.
- 21 programs lack a fully verified strong professor with exact-route supervision authority.
- 21 programs have zero verified faculty-depth points; 50 have only one verified strong match and remain capped at 5 points.
- 67 programs lack official cohort/selectivity evidence for strategic admission calibration.
- Offer-specific net funding, fees, health insurance, summers, and duration remain incomplete where identified in the component evidence.
- The existing Stage 6 portfolio still covers the prior score pool; Stage 6 must be rebuilt against these 71 scores.
- Stage 6 must pressure-test only hard-gate survivors for a core portfolio; diagnostic totals cannot override a failed gate.
