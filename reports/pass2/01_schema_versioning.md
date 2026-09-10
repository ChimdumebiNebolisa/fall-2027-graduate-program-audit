# Pass 2 schema versioning and migration notes

## Boundary

Pass 2 introduces schema version `2.0`. The original `INSTITUTION_COLUMNS`, `PROGRAM_COLUMNS`,
`PROFESSOR_COLUMNS`, and `SOURCE_COLUMNS` constants remain the Pass 1 contract. Existing Pass 1
CSV files are not rewritten or silently promoted. New pipeline outputs use the additive `*_V2`
contracts in `src/graduate_audit/schema.py` and carry `schema_version=2.0`.

This is an additive migration, not a rescoring migration. A later stage must verify and migrate
real program evidence before any Pass 1 recommendation is replaced.

## Added evidence fields

The Pass 2 program contract adds:

- `score_component_evidence`: serialized component-to-anchor-and-source mapping;
- `evidence_completeness`: `complete`, `partial`, or an explicitly unresolved state;
- `score_confidence`: `high`, `medium`, or `low`;
- `distinct_verified_professor_count`: deduplicated count of current, officially sourced,
  verified supervisors;
- `admission_plausibility_rationale`: evidence-backed reason for the controlled category;
- `funding_gate_status` and `funding_gate_evidence`: explicit funding determination and source IDs;
- `regional_admissions_model`: the regional/program admissions structure;
- `unresolved_conflicts`: contradictions and unknowns preserved as data; and
- `hard_gate_failures`: pipe-delimited failed-gate identifiers.

The dedicated score-component contract records the program, component, numeric score, maximum,
rubric anchor, evidence IDs, evidence completeness, score confidence, and unresolved conflicts.
Professor evidence adds source IDs and unresolved conflicts. Institution records add the regional
admissions model and unresolved conflicts.

## Pipeline input bundle

An input directory must contain six CSV files:

1. `institutions.csv` — recognized-institution candidates and regional model;
2. `program_candidates.csv` — discovered program routes and exact research-fit signals;
3. `program_evidence.csv` — verified gate facts, completeness, confidence, rationale, and conflicts;
4. `professor_evidence.csv` — current appointment, supervision authority, official URL, and source IDs;
5. `score_components.csv` — six evidence-backed component rows per program; and
6. `source_ledger.csv` — the sources referenced by funding, professor, and component evidence.

Positive component scores require source IDs. A verified funding gate requires a verified official
source. A verified supervisor must have explicit supervision status, current verification, an
official faculty URL, and evidence IDs. Terms such as `potentially` do not pass the supervision
gate, and retained status or a high funding score cannot manufacture a funding pass.

## Migration procedure for real records

1. Copy a source record into an isolated Pass 2 input bundle; do not edit `outputs/current`.
2. Add the new evidence fields and source-ledger rows, preserving unknowns and conflicts.
3. Run discovery through verification and inspect the checkpoint failures.
4. Add six sourced component rows only after the evidence packet is complete enough to score.
5. Run scoring, portfolio, outreach, reporting, and checkpoint validation.
6. Compare Pass 2 decisions with Pass 1 before any later-stage publication or replacement.

Synthetic fixtures under `tests/fixtures/pass2_pipeline/` demonstrate the contract only; they are
not university findings and must never be merged into the real audit dataset.
