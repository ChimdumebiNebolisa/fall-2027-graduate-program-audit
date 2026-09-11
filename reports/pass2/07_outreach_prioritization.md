# Stage 7 Result

## Decision

Pass

## What changed

Generated: 2026-09-11T16:35:57.663938+00:00

Verified contact-history status for 28 recommended contacts across 22 active programs, then scored every contact across all seven configured dimensions. The result is a 12-contact first wave and a ranked 11-contact second wave.

No email was sent, no Gmail draft was created, and no Calendar item was modified. The connected-account status file is ignored by Git and contains no message body, subject, snippet, message ID, or thread ID.

## Coverage

### First wave

| Rank | Type | Institution | Contact | Score | Decision a reply could change |
| --- | --- | --- | --- | --- | --- |
| 1 | professor | Trent University | Omar Alam | 100 | Retain or deprioritize MSc in Applied Modelling and Quantitative Methods — Thesis Stream by confirming whether Omar Alam expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 2 | professor | University of Minnesota-Twin Cities | Kangjie Lu | 100 | Retain or deprioritize PhD in Computer Science by confirming whether Kangjie Lu expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 3 | professor | University of Toronto | David Lie | 100 | Retain or deprioritize Master of Applied Science in Electrical and Computer Engineering by confirming whether David Lie expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 4 | professor | University of Utah | John Regehr | 100 | Retain or deprioritize Computing PhD by confirming whether John Regehr expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 5 | professor | University of Waterloo | Patrick Lam | 100 | Retain or deprioritize Master of Applied Science in Electrical and Computer Engineering by confirming whether Patrick Lam expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 6 | professor | York University | Zhen Ming (Jack) Jiang | 100 | Retain or deprioritize Master of Science in Computer Science — Thesis Option by confirming whether Zhen Ming (Jack) Jiang expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 7 | professor | Brown University | Malte Schwarzkopf | 93 | Retain or deprioritize Computer Science PhD by confirming whether Malte Schwarzkopf expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 8 | professor | University of Colorado Boulder | Sriram Sankaranarayanan | 93 | Retain or deprioritize Doctor of Philosophy in Computer Science by confirming whether Sriram Sankaranarayanan expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 9 | professor | Duke University | Danfeng Zhang | 86 | Retain or deprioritize Computer Science PhD by confirming whether Danfeng Zhang expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 10 | professor | Johns Hopkins University | Yinzhi Cao | 86 | Retain or deprioritize Doctor of Philosophy in Computer Science by confirming whether Yinzhi Cao expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 11 | professor | Lehigh University | Lichao Sun | 86 | Retain or deprioritize PhD in Computer Science by confirming whether Lichao Sun expects to supervise a funded Fall 2027 student in the verified overlap area. |
| 12 | professor | New Jersey Institute of Technology | Martin Kellogg | 86 | Retain or deprioritize Ph.D. Computer Science by confirming whether Martin Kellogg expects to supervise a funded Fall 2027 student in the verified overlap area. |

### Second wave

| Rank | Type | Institution | Contact | Score | Information gap |
| --- | --- | --- | --- | --- | --- |
| 13 | professor | Northeastern University | Jonathan Bell | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 14 | professor | Northwestern University | Robby Findler | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 15 | professor | Old Dominion University | Shuai Hao | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 16 | professor | University of Illinois Chicago | Mark Grechanik | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 17 | professor | University of Massachusetts-Amherst | Yuriy Brun | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 18 | professor | Virginia Polytechnic Institute and State University | Na Meng | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 19 | professor | Washington University in St Louis | Umar Iqbal | 86 | Recruiting status remains unknown unless the cited evidence explicitly states otherwise. |
| 20 | department | Northeastern University | Khoury PhD Admissions | 82 | Confirm Fall 2027 deadline, fee, and summer-support mechanics when the cycle page updates |
| 21 | department | University of Massachusetts-Amherst | CICS Graduate Admissions | 75 | Confirm the Fall 2027 offer's summer and insurance/fee details |
| 22 | department | Virginia Polytechnic Institute and State University | CS Graduate Program | 75 | What summer-support expectation applies after year one? |
| 23 | department | University of Michigan-Ann Arbor | CSE Graduate Admissions | 70 | How will the committee weigh the >3.5 recent-two-year record against the 3.35 cumulative GPA? |

### Blocked or unknown contact history

| Institution | Type | Contact | History | Reason |
| --- | --- | --- | --- | --- |
| University of Arizona | professor | Roberto Giacobazzi | unknown | Official address not verified |
| Carnegie Mellon University | professor | Claire Le Goues | unknown | Official address not verified |
| University of Michigan-Ann Arbor | professor | Westley Weimer | unknown | Official address not verified |
| Washington University in St Louis | department | CSE Graduate Office | unknown | Official address not verified |
| Carnegie Mellon University | department | SCS Graduate Admissions | unknown | Official address not verified |

## Validation performed

| Assertion | Result |
| --- | --- |
| every_active_program_has_recommended_professor_disposition | PASS |
| every_recommended_contact_has_history_status | PASS |
| contact_history_values_are_tristate | PASS |
| unknown_history_is_preserved | PASS |
| first_wave_size_is_evidence_bounded | PASS |
| every_first_wave_reply_can_change_a_specific_decision | PASS |
| first_wave_has_verified_contact_and_no_prior_contact | PASS |
| prior_contact_never_receives_fresh_introduction | PASS |
| missing_official_contacts_are_blocked | PASS |
| all_priority_dimensions_are_scored | PASS |
| no_duplicate_official_contact | PASS |
| second_wave_is_ranked | PASS |
| only_active_programs_are_prioritized | PASS |
| private_history_has_no_raw_message_material | PASS |
| private_history_is_git_ignored | PASS |

- Stage-specific verification: `python -m pytest tests/test_outreach_prioritization.py -q` — 10 passed.
- Full-suite verification: `python -m pytest -q` — 170 passed.

## Material uncertainties or conflicts

- 5 contacts remain `unknown`, not `no contact`, because no verified official address was available for an exact-address search.
- All 22 active programs remain single-professor dependencies; a negative or absent reply would not by itself prove no faculty depth exists.
- Offer-specific funding, summer support, fees, and Fall 2027 cycle details remain unresolved where the official program evidence says they are not yet published.
- Contact history reflects the connected Gmail account searched on 2026-09-11; messages in another account or under an unverified address are outside coverage.

## Records requiring human judgment

- The applicant must approve which contacts, if any, proceed to drafting in Stage 8; Stage 7 ranks decision value but does not authorize contact.
- Personal preference among active programs remains unverified and can change wave ordering.
- Before outreach, recheck each first-wave recipient address and whether the stated Fall 2027 question is still unresolved.

## Recommendation

Proceed to Stage 8 to draft, but not send, concise messages for the first wave. Preserve the ranked second wave and resolve missing official addresses before considering those blocked contacts.
