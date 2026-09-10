# Independent cross-region second-source validation

Checked 2026-09-09 using official institutional pages. No source dataset was edited.

Coverage:

- All eight retained Canadian routes: four checks each for funding wording, bachelor's/international eligibility, current faculty appointment, and deadline-cycle labeling.
- Five Canadian universe exclusions selected deterministically by SHA-256 of institution ID.
- Five retained U.S. finalists selected deterministically by SHA-256 of program ID; the sample spans five distinct funding wordings.

`second_source_checks.csv` is the full audit trail. `corrections_needed.csv` is the actionable subset. Results distinguish confirmation, partial corroboration, non-confirmation, and correction-required findings. Different official pages were used where a program-level second page existed; when only one current program-level page carried the precise amount, the second official page corroborates policy/structure and that limitation is stated.

Material corrections are not applied here because this task is independently read-only with respect to the source datasets.
