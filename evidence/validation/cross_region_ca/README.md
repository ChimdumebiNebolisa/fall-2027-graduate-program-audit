# Cross-region exclusion and Europe-finalist validation

Checked 2026-09-09 using current official institutional sources. Search results were used only to discover official pages; findings in the CSVs cite the official pages themselves. No source regional or deep-review files were changed.

## Deterministic exclusion sample

The fixed seed is `cross-region-ca-v1` and the ordering key is SHA-256 of `seed|institution_id`.

- United States: the seven smallest hashes across the full U.S. exclusion log.
- Europe: institutions were scanned in hash order and the first institution from each new country was selected. The sixth slot was deterministically replaced by the first row with a different exclusion reason because the initial six all had the same bounded-screen disposition.

This produced 7 U.S. cases and 6 European cases across 6 European countries and 2 source exclusion reasons. The sample is reproducible but bounded; it is not evidence that all other exclusions are correct.

One sampled false negative was found: Hellenic Mediterranean University has an official Electrical and Computer Engineering PhD and a research-oriented Informatics Engineering MSc. The PhD should be added to mechanical screening; its exceptional bachelor-entry rule, English, deadline, and funding still require deep review.

The EADTU row was not a false negative, but the audit found a universe-quality issue: EADTU is an association/network, not a degree-awarding provider, and should be removed earlier during institution normalization.

## European finalist second-source audit

All 18 current deep-review program rows and their 18 linked faculty rows (17 unique professors because Martin Vechev is linked to both ETH routes) were checked for degree entry, funding classification, and current appointment.

Material corrections:

1. Imperial Computing says bachelor-only applicants will not normally be considered; the current `yes` bachelor-entry value should be changed to `no/not normally` and the immediate route downgraded or excluded absent written exception.
2. ETH's Direct Doctorate explicitly includes financial support and tuition waivers for its first two years and a doctoral salary thereafter. Program funding is conditional on admission but substantially more definite than the current vague/unconfirmed classification.
3. UCD published 2026 Computer Science PhD project calls accepting a strong technical bachelor's, so bachelor entry is project-specific rather than universally `no`. Funding remains call-specific and no matching Fall 2027 award was verified.

One appointment caveat remains: two current Aalto pages disagree on whether Fabian Fagerholm is an associate or assistant professor. Both establish a current Computer Science appointment, but exact rank should be confirmed before outreach.

No professor was classified as recruiting. Current appointment and research fit do not prove Fall 2027 capacity or funding.

## Outputs

- `data/processed/validation/cross_region_ca/exclusion_sample_audit.csv`
- `data/processed/validation/cross_region_ca/europe_finalist_second_source.csv`
- `data/processed/validation/cross_region_ca/validation.json`

`build_validation.py` regenerates the structured outputs and asserts sample composition, source-field completeness, enums, and full finalist coverage.
