# United States IPEDS coverage

Access date: 2026-09-09

This regional output uses the frozen official NCES IPEDS `HD2024`, `IC2024`,
`C2024_A`, `C2023_A`, and `C2022_A` complete-data archives. Checksums and selected ZIP
members are recorded in `data/manifests/us/ipeds_release_manifest.json`.

## Coverage

- 2,107 active, degree-granting institutions with master's or doctoral
  authority. The filter uses `CYACTIVE=1`, `DEGGRANT=1`, and either a master's
  or doctoral highest offering (`HLOFFER=7/9`) or a post-master's highest
  offering (`HLOFFER=8`) paired with a positive IC master's/doctoral indicator.
- All 50 states and the District of Columbia are represented.
- 53 institutions in IPEDS other jurisdictions are explicitly marked: 51 in
  Puerto Rico, one in Guam, and one in the U.S. Virgin Islands.
- 679 institutions have at least one configured graduate first-major CIP
  completion signal across academic years 2021-22 through 2023-24.
- 598 have a primary signal; 81 have only a secondary review-only signal.
- 1,428 institutions have no configured signal and receive an explicit
  mechanical-screen exclusion row.
- 1,786 unique institution/CIP signal rows were produced, plus nine official
  program-page spot checks. The spot checks are not finalist reviews.

## Screening rule

Completions rows are retained only when `MAJORNUM=1`, normalized `AWLEVEL` is
7, 17, 18, or 19, the CIP code is configured in `research_topics.yaml`, and
`CTOTALT>0`. Leading zeros are normalized because the 2022 file encodes some
award levels as `07` while later files use `7`.

IPEDS CIP data is a discovery signal only. It does not establish that a
current program exists, that it matches the applicant's research, that direct
entry or international admission is allowed, that funding is available, or
that any professor can supervise or is recruiting. New and non-completing
programs may be missed. Accreditation is not independently verified here.

## Files

- `institution_universe.csv`: full U.S./IPEDS-jurisdiction universe with a
  schema-valid status on every row.
- `program_screening.csv`: mechanical institution/CIP candidates and nine
  bounded official-page spot checks.
- `exclusion_log.csv`: one reason and source for every no-signal institution.
- `source_ledger.csv`: institution-authority, CIP-signal, and official-page
  claim records.
- `data/manifests/us/coverage.json`: exact counts, state/jurisdiction coverage,
  limitations, blocked sources, and validation result.
- `evidence/programs/us/official_program_verification.csv`: the nine opened
  official program pages, separated from the mechanical CIP evidence.
