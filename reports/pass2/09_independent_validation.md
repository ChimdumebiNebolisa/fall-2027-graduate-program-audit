# Stage 9 Result

## Decision

Pass

## What changed

Generated: 2026-09-11T17:32:46.329053+00:00

Completed the independent score/professor recount, core five-domain verification, recruiting-claim recheck, exclusion-sample review, portfolio economics review, and eleven-sheet workbook inspection.

## Coverage

| Validation category | Status | Coverage | Limitations |
| --- | --- | --- | --- |
| structural validation | PASS | 80 core-domain rows; 166 score recalculations; 3596 sources | Workbook validation is recorded separately after export. |
| evidence-completeness validation | PASS_WITH_DISCLOSED_GAPS | primary source recorded for 80/80 core-domain checks | 48 checks have one authoritative URL in the ledger. |
| substantive second-source verification | PARTIAL | 32/80 core-domain checks have two distinct authoritative URLs | No second distinct authoritative URL was present in the ledger for 48/80 checks; live accessibility: {'request_error': 4, 'not_checked': 16, 'reachable': 54, 'http_error': 6}. |
| portfolio-rule validation | PASS | 16 core + 6 reserve; 22 unique institutions | Fee known numerically for 13/22 active programs. |
| outreach-quality validation | PASS_WITH_REPLY_DEPENDENCIES | 12 first-wave drafts; 28 confirmed recruiting claims rechecked | Live source accessibility for recruiting claims: {'reachable': 25, 'request_error': 2, 'http_error': 1}; capacity still requires replies. |
| visual workbook validation | PASS | 11/11 sheets rendered and visually inspected; 11 sheets exported | Visual inspection checks layout/readability; substantive correctness is covered by the other validation categories. |

## Validation performed

| Assertion | Result |
| --- | --- |
| all_16_core_programs_have_five_domain_rechecks | PASS |
| no_core_claim_recheck_is_missing_a_source | PASS |
| all_confirmed_recruiting_claims_rechecked | PASS |
| recruiting_claims_preserve_exact_degree_scope | PASS |
| exclusion_sample_spans_all_regions | PASS |
| exclusion_sample_spans_major_reasons | PASS |
| all_scores_recalculate_exactly | PASS |
| all_distinct_professor_counts_recalculate_exactly | PASS |
| every_core_deadline_is_explicitly_cycle_labeled_or_caveated | PASS |
| core_programs_are_current_or_explicitly_current_in_evidence | PASS |
| core_is_within_working_range | PASS |
| active_portfolio_uses_one_program_per_university | PASS |
| active_portfolio_clears_all_hard_gates | PASS |
| stage_8_drafts_are_the_only_ready_drafts | PASS |

- Stage-specific verification: `python -m pytest tests/test_independent_validation.py -q` — 6 passed.
- Full-suite verification: `python -m pytest -q` — 186 passed.
- Workbook validation includes structural inspection, formula-error scan, and a rendered visual review of every sheet. Formula cleanliness is not used as substantive proof.

## Material uncertainties or conflicts

- Second authoritative sources are not available in the committed ledger for every material claim; this category is explicitly Partial.
- Live access failures are retained as accessibility gaps, not treated as evidence of inactivity.
- Recurring, inferred, prior-cycle, and conflicting deadlines are visibly labeled and are not asserted as confirmed Fall 2027 dates.
- Faculty capacity and offer-specific funding remain reply-dependent.

## Records requiring human judgment

- The applicant should decide which ready drafts to send and how much application-fee risk to accept.
- Unresolved and reopened exclusion-audit samples should be revisited if the desired portfolio expands beyond the 22 active options.
- Final deadline and fee checks should be repeated immediately before submission.

## Recommendation

Use the 16-program core as the working shortlist, retain the 6-program reserve as reply-dependent alternatives, and execute outreach in the documented waves. Do not treat a non-response as negative evidence.
