# Europe regional discovery output

This directory covers the 27 EU member states, United Kingdom, Norway,
Switzerland, and Iceland. Run the regional phase with:

```powershell
$env:PYTHONPATH = "src"
python -m graduate_audit.ingest.europe
```

For a complete ROR-derived universe, download the frozen
`v2.10-2026-07-20-ror-data.zip` release and pass it with `--bulk-zip`. The
generated API-fallback snapshot is broad but not complete: ROR explicitly warns
that paging filter-only queries can produce duplicates and omissions. The exact
counts and coverage ratio are recorded in `coverage.json`.

`program_screening.csv` is a bounded positive-signal screen of official pages.
It is not an exhaustive catalog crawl. `program_screened_out` therefore records
a completed workflow disposition for this regional pass, not proof that an
institution has no relevant program. Every such row is retained in
`exclusion_log.csv` with low confidence and mandatory manual verification.

No program is finally retained in this phase. Supervisor authority, research
fit, Fall 2027 recruitment, international eligibility, and funding must be
verified later. EHESO/ETER identifiers are blank because its HEI API required
authorization at the freeze date; the failure and its impact are recorded under
`data/manifests/europe/`.
