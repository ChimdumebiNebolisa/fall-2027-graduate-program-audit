# Pass 2 Stage 1 — Pipeline and contract repair

Date: 2026-09-10
Decision: **PASS**

## Outcome

The documented CLI now executes a staged Pass 2 pipeline instead of recording a phase name.
Discovery, screening, research-fit assessment, verification, scoring, portfolio construction,
outreach preparation, and reporting have separate inputs, outputs, and checkpoint manifests.
`run --resume` verifies checkpoints in order and starts at the first invalid stage.

Pass 1 recommendations and final outputs were not regenerated or changed in this stage. The new
schema and strict gates apply to evidence migrated into the Pass 2 pipeline.

## Root causes repaired

1. `graduate_audit.cli` previously routed every command except `validate` to one shallow
   `progress.json` update. Commands now call a concrete pipeline stage.
2. `--resume` previously had no reader, checksum validation, or stage scheduler. Each stage now
   records and validates input/output SHA-256 checksums before resume decides whether to skip it.
3. The original CSV contract had no place to trace score components, distinguish completeness
   from confidence, count distinct verified professors, record an admissions rationale, or retain
   funding evidence and conflicts. Version 2.0 adds these fields without rewriting version 1.0.
4. Funding could previously pass from `retained` status, a score of at least 18, and any non-empty
   verification text. Supervision strings beginning with `potentially` could also pass. These
   shortcuts were removed. Funding now requires an explicit verified status plus evidence, and
   supervision requires explicit verified authority, current verification, an official URL, and
   evidence IDs.

## Acceptance criteria

| Criterion | Evidence | Result |
|---|---|---|
| Documented commands perform work | CLI commands map to concrete stage runners; `portfolio` and `outreach` commands were added | PASS |
| Stages are separated | Eight ordered stage functions with explicit input/output contracts | PASS |
| Checkpoints are auditable | Every manifest records stage, status, run ID, start/completion dates, inputs, outputs, SHA-256, bytes, row counts, and failures | PASS |
| Schema covers required evidence | Additive `*_V2` contracts and dedicated score-component rows cover all eight required evidence concepts | PASS |
| Hard gates are real | Unit tests cover missing funding evidence, possible-only supervisors, distinct-professor deduplication, and the legacy validator | PASS |
| End-to-end fixture works | Two synthetic programs flow from input through report; one passes strict gates and one remains `Do Not Apply` with conflicts preserved | PASS |
| Resume uses the last valid checkpoint | Clean resume skips all stages; after score-output corruption, resume skips through verification and reruns scoring through reporting | PASS |
| No hard-coded university result | Institution names exist only in fixture CSVs and flow into outputs; pipeline source contains neither fixture institution name | PASS |

## Fixture execution

The fixture run produced:

- 2 institutions and 2 screened program records;
- 2 program-evidence records, 3 professor records, 12 score-component rows, and 8 sources;
- 2 scored programs;
- 1 core program, 0 reserve programs, and 0 monitor rows;
- 2 manual-review outreach candidates; and
- an audit report plus a structured run summary.

Initial checkpoint validation returned `PASS` for all eight stages. A clean `--resume` skipped all
eight. After appending invalid content to `scoring/program_scores.csv`, resume preserved discovery,
screening, research-fit, and verification checkpoints and reran scoring, portfolio, outreach, and
reporting. Final validation again returned `PASS` for all eight checkpoints.

## Safety and compatibility

- Legacy schema constants remain unchanged; new outputs use schema version 2.0.
- Legacy scoring refuses version 1.0 records instead of silently manufacturing new decisions from
  incomplete evidence.
- Positive score components require source IDs.
- A verified funding gate requires verified official evidence.
- One or zero distinct verified professors cannot receive more than 5 faculty-depth points.
- Outreach output is a manual-review priority list; the pipeline does not send mail or create drafts.
- Synthetic fixture institutions are test data only and are not audit findings.

## Blockers

None for Stage 1.

## Unresolved coverage

- The 56 real Pass 1 scored program rows have not been migrated to schema 2.0 or rescored. Their
  hard-coded component values remain an open Stage 5 concern.
- Existing professor-depth evidence and supervision authority have not been reverified. Stage 3
  must resolve or preserve those uncertainties before real rescoring.
- United States, Canada, and Europe recall gaps are unchanged. Stage 2 owns funnel rebuilding.
- Admissions, funding, language, and Fall 2027 cycle evidence remain for Stage 4.
- The existing 20-program portfolio and final outreach artifacts were not rebuilt; Stages 6–8 own
  those decisions and release controls.
- The fixture proves orchestration and contracts, not the completeness or correctness of real-world
  university evidence.
