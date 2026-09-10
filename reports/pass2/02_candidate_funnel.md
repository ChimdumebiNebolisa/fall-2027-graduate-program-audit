# Pass 2 Stage 2 — High-recall candidate funnel

Date: 2026-09-10
Decision: **PASS with documented non-saturation**

## Outcome

Stage 2 rebuilt the discovery funnel from independent registry, official-program, department/research, recent-paper, current-faculty cross-match, lab/center, Calendar, first-audit, research-master/scholarship, and underrepresented-route paths. It does not score or recommend universities.

The OpenAlex exporter now retains all 1,647 observed target-country institutions and all 6,923 author–institution pairs instead of a global top-300/top-1,000 slice. Downstream discovery filtered 815 non-educational institution records before candidate contribution.

## Funnel counts

| Measure | Count |
| --- | --- |
| Funnel rows | 1965 |
| Distinct institutions | 815 |
| Advance to Stage 3 | 83 |
| Catalog verification required | 253 |
| Manual secondary review | 11 |
| Screened out with reason | 1618 |
| Official program URL present | 93 |
| Active rows missing official program URL | 264 |

The 1,618 screened-out rows remain in the funnel with explicit reasons. Single-source mechanical signals do not advance unless another independent path supports catalog review; duplicate mechanical rows at one institution are consolidated.

## Regional and route coverage

| Region | Status | Rows |
| --- | --- | --- |
| canada | advance_to_stage_3 | 37 |
| canada | catalog_verification_required | 3 |
| canada | screened_out | 3 |
| europe | advance_to_stage_3 | 19 |
| europe | catalog_verification_required | 79 |
| us | advance_to_stage_3 | 27 |
| us | catalog_verification_required | 171 |
| us | manual_secondary_review | 11 |
| us | screened_out | 1615 |

| Region | Priority route bucket | Active rows |
| --- | --- | --- |
| canada | doctoral_bachelors_entry | 4 |
| canada | research_masters | 32 |
| canada | structured_or_masters_required_doctorate | 1 |
| canada | unresolved_or_exceptional_route | 3 |
| europe | doctoral_bachelors_entry | 6 |
| europe | research_masters | 1 |
| europe | structured_or_masters_required_doctorate | 12 |
| europe | unresolved_or_exceptional_route | 79 |
| us | doctoral_bachelors_entry | 27 |
| us | unresolved_or_exceptional_route | 182 |

All three regions are represented. The active funnel includes bachelor's-entry doctoral routes, thesis/research master's routes, and structured or master's-required doctoral routes. Exact eligibility and funding remain Stage 3 questions.

## Regional research-topic coverage

| Region | Research-topic cluster | Active rows |
| --- | --- | --- |
| canada | ai_for_se | 28 |
| canada | repair_analysis | 23 |
| canada | systems_security | 34 |
| canada | trustworthy_ai | 26 |
| europe | ai_for_se | 62 |
| europe | repair_analysis | 66 |
| europe | systems_security | 71 |
| europe | trustworthy_ai | 58 |
| us | ai_for_se | 142 |
| us | repair_analysis | 100 |
| us | systems_security | 140 |
| us | trustworthy_ai | 121 |

No regional or topic quota determined inclusion. Topic counts are coverage diagnostics, not university scores.

## Discovery contribution and yield

| Discovery path | Examined | Contributed | Introduced | Stage 3 | Review | Screened out | Active yield |
| --- | --- | --- | --- | --- | --- | --- | --- |
| recognized_institution_record | 5833 | 1965 | 1839 | 83 | 264 | 1618 | 0.1766 |
| official_program_or_department_signal | 1839 | 93 | 0 | 83 | 0 | 10 | 0.8925 |
| recent_paper_signal | 1647 | 903 | 83 | 72 | 253 | 578 | 0.3599 |
| current_faculty_topic_signal | 6923 | 51 | 0 | 11 | 0 | 40 | 0.2157 |
| lab_or_center_signal | 56 | 55 | 0 | 55 | 0 | 0 | 1.0000 |
| calendar_prior_list | 55 | 204 | 3 | 21 | 34 | 149 | 0.2696 |
| first_audit_program | 56 | 55 | 40 | 55 | 0 | 0 | 1.0000 |
| research_masters_or_scholarship_search | 1839 | 80 | 0 | 77 | 0 | 3 | 0.9625 |
| underrepresented_route_search | 1839 | 119 | 0 | 34 | 82 | 3 | 0.9748 |

Active yield is the share of contributed rows that remains active after cross-path and deduplication checks. This makes noisy sources visible: registry and program-code paths provide breadth, while official-program and first-audit paths provide most immediately verifiable routes.

## Known-seed recovery

### TerraProbe-adjacent

| Institution | Program | Route | Evidence confidence |
| --- | --- | --- | --- |
| Carnegie Mellon University | Software Engineering PhD | Doctoral route accepting bachelor's entrants | high |
| Case Western Reserve University | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| George Mason University | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| Georgia Institute of Technology-Main Campus | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| Iowa State University | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| North Carolina State University at Raleigh | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| Northeastern University | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| Oregon State University | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |

### Evidex-adjacent

| Institution | Program | Route | Evidence confidence |
| --- | --- | --- | --- |
| Pennsylvania State University-Main Campus | Computer Science and Engineering PhD | Doctoral route accepting bachelor's entrants | high |
| Rochester Institute of Technology | Computing and Information Sciences PhD | Doctoral route accepting bachelor's entrants | high |
| The University of Texas at Austin | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| The University of Texas at Austin | Ph.D. in Computer Science | Doctoral route; bachelor's entry requires Stage 3 verification | medium |
| University of Illinois Urbana-Champaign | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| University of Maryland-College Park | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| University of Massachusetts-Amherst | Computer Science PhD | Doctoral route accepting bachelor's entrants | high |
| University of Notre Dame | Computer Science and Engineering PhD | Doctoral route accepting bachelor's entrants | high |

Both seed categories have exact official-program rows advancing to Stage 3. Seed adjacency is a discovery check, not a professor/recruiting claim.

## Calendar recovery

The bounded prior report contained 55 Calendar candidates. Canonical registry and alias matching recovered 53; 2 remain unmatched or outside scope.

Unmatched entries: Gwangju Institute of Science and Technology, University of Limerick. Gwangju Institute of Science and Technology is outside the configured geography. University of Limerick is in scope but absent from the incomplete European registry snapshot; it remains an explicit coverage gap rather than a negative finding.

## Contamination and affiliation normalization

| Check | Count |
| --- | --- |
| OpenAlex institution rows | 1647 |
| Non-educational institutions filtered | 815 |
| Educational institutions matched to registry | 666 |
| Educational institutions unmatched | 166 |
| Institution-name corrections | 30 |
| Author–institution rows | 6923 |
| Current official-faculty cross-matches | 11 |
| Publication-time-only affiliations | 3686 |
| Faculty affiliations unmatched | 712 |
| Faculty affiliation-name corrections | 166 |

OpenAlex author affiliations are publication-time metadata. Only 11 rows cross-match a current official-faculty record from the first audit; all other author affiliations are excluded from the `current_faculty_topic_signal` path pending Stage 4.

## Exclusion-sample audit

| Audit result | Rows |
| --- | --- |
| confirmed_screened_out | 16 |
| reopen_in_funnel | 4 |
| unresolved_no_independent_positive | 13 |

The 33-row deterministic sample covers the United States, Canada, and Europe and all five normalized major exclusion strata. Every sample row records its original reason, source, independent signals, audit result, rationale, and false-negative risk.

4 sampled exclusions had independent signals and were reopened in the funnel. 13 bounded mechanical exclusions had no independent positive signal but cannot be confirmed without exhaustive catalog inspection. 16 specialty/school-entity exclusions were confirmed by their original official-scope evidence and absence of a cross-signal.

## Saturation decision

**Saturation was not reached.** The sample exposed 4 false-negative-risk cases, and 13 mechanical exclusions remain unresolved. The funnel therefore reopens independent cross-signal cases and preserves catalog-review candidates instead of claiming exhaustive negative coverage. This is acceptable for Stage 2 only because the limitation is explicit and no university is scored or recommended.

## Blockers

None prevented Stage 2 completion.

## Unresolved coverage

- The European registry snapshot remains incomplete: 3,628 unique records were captured from 4,462 reported filtered records, and University of Limerick is not present.
- EHESO/ETER and several national-registry sources remain blocked from the first audit.
- 264 active candidates still require an exact official program URL/catalog determination.
- 166 educational OpenAlex institutions could not be normalized to the frozen regional registry and therefore did not contribute candidates.
- 3,686 faculty affiliations are publication-time only and 712 are unmatched; Stage 4 must verify current appointments and supervision authority.
- Stage 2 does not verify program status, admission eligibility, funding, language, or Fall 2027 details; those belong to Stage 3.
