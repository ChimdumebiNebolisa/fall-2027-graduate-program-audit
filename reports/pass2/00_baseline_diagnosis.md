# Stage 0 Result

## Decision
Pass

## What changed

The repository was frozen at commit `d2e770b2d5dafe25537481f7b83663471e7060fc` and diagnosed without changing any program recommendation, score, portfolio membership, outreach ranking, report, or workbook. A complete machine-readable inventory, an issue register, and a Stage 0 manifest were added. The Pass 2 progress state now records Stage 0 as complete and keeps Stage 1 unauthorized pending user approval.

## Coverage

- Baseline tracked files inventoried: 169.
- Workbook sheets inventoried: 11.
- Total artifact inventory records: 180.
- Current final output/report files checked for traceability: 52.
- Final artifacts with tracked producers: 41.
- Explicitly non-reproducible final artifacts: 11 QA render snapshots.
- Dataset records: 78; scripts: 34; reports: 4; source ledgers: 12; validation artifacts: 33.
- The full per-artifact inventory, classification, checksum, row count where applicable, and producer mapping is stored in `data/manifests/pass2/stage_00.json` under `artifact_inventory`.

## Validation performed

- Compared the working tree with `d2e770b2d5dafe25537481f7b83663471e7060fc` before Stage 0 writes; the baseline was clean.
- Computed SHA-256 checksums from a Git archive of the frozen commit, including every file under the current output and report directories.
- Imported the workbook with the approved spreadsheet runtime and independently parsed its worksheet metadata; both methods found the same 11 sheets.
- Checked every current final output for a tracked producer. Eleven `renders/qa` PNGs have no tracked producer and are explicitly marked non-reproducible; no final output remains unmapped.
- Checked Git tracking/ignore rules and scanned tracked content for raw Gmail/Calendar export markers. Only `data/private/README.md` is tracked under `data/private`; raw connected-account source paths are ignored.
- Joined scored program rows to professor rows to test faculty depth. All 56 of 56 scored programs exceed the one-professor depth cap while having one distinct professor row.
- Confirmed that the Stage 0 output generator did not modify recommendation-bearing Pass 1 outputs.

## Material uncertainties or conflicts

- The prior validation status is not reliable as a substantive pass because critical funding, supervision, faculty-depth, and score-provenance gates are defective.
- European discovery is short by 834 records relative to the ROR filtered total and several registry sources were blocked.
- Canada retains 50 unresolved indexed institutions and nine blocked or insufficient program pages.
- The 11 QA render snapshots cannot be recreated by a tracked command; they are preserved only as unverified baseline evidence.
- Sanitized Calendar comparison and contact-status fields are tracked, but no raw messages or Calendar event bodies were found. Stage 7 must keep any connected-account detail private.

## Records requiring human judgment

No program-level judgments were changed in Stage 0. Later stages must decide how to resolve official-source conflicts, funding ambiguity, supervision authority, and whether each current recommendation survives evidence-backed reconstruction.

## Files created or modified

- `reports/pass2/00_baseline_diagnosis.md`
- `data/processed/pass2/baseline_issue_register.csv`
- `data/manifests/pass2/stage_00.json`
- `state/progress.json`
- `scripts/build_stage_00.py`

## Recommendation before the next stage

Begin Stage 1 only after explicit user approval. Stage 1 may repair the executable pipeline, schemas, checkpoint manifests, and tests. It may not rescore programs, change recommendations, or treat the Pass 1 validation result as proof that later gates passed.

## Baseline identity

- Commit: `d2e770b2d5dafe25537481f7b83663471e7060fc`
- Commit timestamp: `2026-09-10T00:24:01-05:00`
- Execution plan SHA-256: `4e1bf6ff8639bf4088fd89a1268e4d3a8e4319554edfc98d8403945deb3f1ed8`
- Recommendation-bearing outputs changed in this stage: no

## Artifact inventory summary

| Classification | Artifacts |
| --- | --- |
| repairable | 51 |
| reusable | 71 |
| superseded | 44 |
| unverified | 14 |

| Artifact type | Artifacts |
| --- | --- |
| contract/configuration | 5 |
| dataset | 78 |
| documentation | 13 |
| manifest | 16 |
| project file | 34 |
| report | 4 |
| script | 34 |
| source ledger | 12 |
| validation | 33 |
| workbook | 1 |
| workbook sheet | 11 |

Each baseline artifact has exactly one disposition: reusable, repairable, superseded, or unverified. `Reusable` means it may seed a later stage; it does not waive freshness or official-source verification.

## Workbook sheet inventory

| Index | Workbook sheet | Used range | Classification | Producer |
| --- | --- | --- | --- | --- |
| 0 | COVERAGE DASHBOARD | A1:H18 | superseded | scripts/build_workbook.mjs |
| 1 | SCHOOLS & PROGRAMS | A1:AP60 | superseded | scripts/build_workbook.mjs |
| 2 | PROFESSOR MATCHES | A1:AE60 | superseded | scripts/build_workbook.mjs |
| 3 | DEPARTMENT AND ADMIN OUTREACH | A1:O39 | superseded | scripts/build_workbook.mjs |
| 4 | SCHOOL SUMMARY | A1:S56 | superseded | scripts/build_workbook.mjs |
| 5 | THIS WEEKEND OUTREACH QUEUE | A1:N19 | superseded | scripts/build_workbook.mjs |
| 6 | OUTREACH DRAFTS | A1:H19 | superseded | scripts/build_workbook.mjs |
| 7 | SCREENING AND EXCLUSIONS | A1:K54 | superseded | scripts/build_workbook.mjs |
| 8 | CALENDAR COMPARISON | A1:G59 | superseded | scripts/build_workbook.mjs |
| 9 | SOURCES | A1:Q794 | superseded | scripts/build_workbook.mjs |
| 10 | METHODOLOGY | A1:B16 | superseded | scripts/build_workbook.mjs |

## Baseline issues

| ID | Severity | Category | Affected | Stage owner | Summary |
| --- | --- | --- | --- | --- | --- |
| P2-0001 | critical | pipeline | 7 | Stage 1 | Seven documented CLI commands only record a phase name and perform no audit work. |
| P2-0002 | critical | resume | 1 | Stage 1 | run --resume ignores checkpoints and merely registers the run phase. |
| P2-0003 | critical | schema | 2 | Stage 1 | The shared schema lacks the required Pass 2 evidence, confidence, depth, funding-gate, regional-model, rationale, and conflict fields. |
| P2-0004 | critical | scoring | 56 | Stage 5 | Institution/program score components are hard-coded rather than calculated from claim-level evidence. |
| P2-0005 | critical | faculty depth | 56 | Stage 4 + Stage 5 | Every scored program receives more than five faculty-depth points despite only one distinct professor row. |
| P2-0006 | critical | funding gate | 1880 | Stage 1 + Stage 3 + Stage 5 | The funding hard gate can pass from a retained label, funding score, and any verification text. |
| P2-0007 | high | supervision authority | 31 | Stage 1 + Stage 4 | Unverified or merely potential supervision authority is treated as a verified professor match. |
| P2-0008 | high | admission calibration | 23 | Stage 1 + Stage 5 | Current admission-plausibility labels include values outside the controlled Pass 2 categories. |
| P2-0009 | high | candidate discovery | 2 | Stage 2 | Global OpenAlex outputs are truncated to 300 institutions and 1,000 faculty without regional/topic recall or exclusion-sample saturation checks. |
| P2-0010 | high | contact history | 3 | Stage 7 | First-wave administrative contacts have blank contact history instead of an explicit unknown state, and the pipeline can default missing history to No. |
| P2-0011 | high | outreach scoring | 15 | Stage 7 | Outreach priority is inferred from program rank/fit fallbacks and a hard-coded admin score rather than configured component scores. |
| P2-0012 | high | generated final text | 15 | Stage 8 | Fifteen templated emails are published in final outputs without Draft Ready evidence or per-draft manual review records. |
| P2-0013 | high | validation | 3 | Stage 1 + Stage 9 | Validation files report one undifferentiated PASS while hard-gate, evidence-completeness, score provenance, and outreach-quality defects remain. |
| P2-0014 | medium | traceability | 11 | Stage 1 + Stage 9 | Eleven QA render snapshots have no tracked generating command. |
| P2-0015 | high | coverage | 834 | Stage 2 | European discovery exposes 3,628 of 4,462 reported ROR records (81.31%) and retains blocked registry sources. |
| P2-0016 | high | coverage | 59 | Stage 2 + Stage 3 | Canada retains 50 unresolved indexed institutions and nine blocked or insufficient official program pages. |
| P2-0017 | medium | portfolio | 20 | Stage 6 | Portfolio construction encodes a 20-core target and fixed reach allowance without the Stage 6 ten-question pressure test. |

The issue register contains the affected records, evidence, proposed repair, acceptance impact, status, and stage owner for each item.

## Privacy audit

- Tracked files under `data/private`: `data/private/README.md` only.
- Ignored connected-source paths verified: `data/private/gmail_contact_history.csv` and `data/private/calendar_candidate_summary.csv`.
- Raw Gmail/Calendar export or event markers found in tracked content: none.
- Tracked connected-context outputs: sanitized school comparison and broad contact-status/outcome fields only.
- Result: pass for the Stage 0 raw-private-content check.

## Current final output traceability and checksums

| Final output | SHA-256 | Traceability | Producer or disposition |
| --- | --- | --- | --- |
| outputs/20260909-fall2027-audit/admin_contacts.csv | c54241a096733e36b4cddeea9312e31c8a5022d1b32c5f9b7a675590433b1346 | tracked producer | src/graduate_audit/reporting/outreach.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/calendar_comparison.csv | 666e25b70cc1cc2feae2cb32f45a403e2261c23ead95adb06775040d63f3ec31 | tracked producer | src/graduate_audit/connected_context.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/exclusion_log.csv | 6eb06407dffc4cda9847ea87650d74eff979fa1a9b0d860df3786213553134f6 | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py |
| outputs/20260909-fall2027-audit/final_validation.json | 99a9f5a306445249551f04527bc4235f9827ba5500ee7fd75c614408e631de8f | tracked producer | src/graduate_audit/verify/final_validation.py |
| outputs/20260909-fall2027-audit/graduate_program_audit.xlsx | 90509c3c4b12528286d8015e5f8618175aebda68d707b95987a4f1211dd2a89d | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/institution_universe.csv | 683e8cc3dee95b5347c6dc7b7bb45256377a3175b11013db646aeb6eb131b0a2 | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py |
| outputs/20260909-fall2027-audit/outreach_drafts.csv | 833db3f4ea18759089a1cdad331205b7d95400405b06f7987b471a5de7776e08 | tracked producer | src/graduate_audit/reporting/outreach.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/portfolio.json | fd1bbb0e6e802f824992fcf2f0eae83844720434a77f04757fc31074657b3500 | tracked producer | src/graduate_audit/portfolio.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/professor_evidence.csv | a02f68de4e15bd436aaca16826ba0b0e43a0ec629e1530cde67b3620bbbc2dc6 | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/reporting/outreach.py; src/graduate_audit/verify/apply_corrections.py |
| outputs/20260909-fall2027-audit/program_screening.csv | 43bb75f33e5cb3b6176880eec833698922070bcff40c462f497fa7a137644896 | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/portfolio.py; src/graduate_audit/verify/apply_corrections.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/render_html/calendar_comparison.html | 79e8b5897e9d67eae8b3c85a01032ad787bad7b96f6c2049c896f8e08fc25fd6 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/coverage_dashboard.html | 1432ef24d92ac93a6c440de4d9d63d30380d3d4aa58a7fdbc99253a453149aa1 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/department_and_admin_outreach.html | ea58440acd43ff8a94b29efff2e727f112e33a8bad7922b34dde7d9b07c00e1f | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/methodology.html | 0609c3af10752588e4e8d7bdadfcb0b4b63e1da2940366d147b4bc17484ec968 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/outreach_drafts.html | 78ccd41ff3a8fbb23b2a425f27d5d317241a6d0ac9aa407ba3876baf00ce5443 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/professor_matches.html | f9a8ace4d365b9a14234a01b74e595aaf33eb0c05b6c189fcca8a77d7ddc60cb | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/school_summary.html | b4297f748a4db8b8e5dc8888bcb3d388606fdfb8c044cb84fc6188b294ec9c8a | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/schools_and_programs.html | 1ba96613b85d5fa1105d5f064cda5b0aaa7207007274fd1d9b0980d109be80ee | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/screening_and_exclusions.html | dcbcfe1d1502616484cf59177259bd6345effadcd9b86c3e915a6f764a69f500 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/sources.html | 466efd6ac8058c03c73b814f305f8c4f73412636f3d111740ce33b20c00639e2 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/render_html/this_weekend_outreach_queue.html | dfaff5f55d150f8245e85ed4fdc11890419de6a3fe7f47ef9465161fe7375c44 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/calendar_comparison.png | 8d7cbaff89428e22cf05e344a3bcdcdd22d37456ed3411d9ccd05e08136d8617 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/coverage_dashboard.png | 63a117a592763108c95bfc0b375fc424bcf62fb0ef1cd467a966b9114e54550a | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/department_and_admin_outreach.png | a5fa4f4c51553011d5858a06fdb55fa0b5a520c7bf6e5301848f336309882bd4 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/methodology.png | cca7b3fc021e29a950e8c9bd75928bb4faf2191bf18aed84171118677b3ab5e2 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/outreach_drafts.png | d0d3e7c151ebcfda45233badec41902352f33b24f8fec6a2955eb763019e39db | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/professor_matches.png | 055fca46fdca153669ff7b004a7410e4df9064e15584a0fe4bf534b50875907e | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/qa/calendar_comparison.png | 97e3e5d871595ac1e76bec0cc6b268aafd2eae169fd78a3e192a691bbfc4826c | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/coverage_dashboard.png | 1db861759d8b1d0e91f746b39dbadfb85812331a126795242592536da2d3f9e8 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/department_and_admin_outreach.png | b209739f8d05e355c6830b5554f39e009be0b1950d8461435c20fcb2907e2949 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/methodology.png | 9da8a8173f72b123cbf6905bf09a85556ac8f92554bcdab6eb24d48960c60822 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/outreach_drafts.png | 13f5eec6ae9ca79ac75a6b3003dd5de36a47ab244354b1e2fae7211f01d8abe0 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/professor_matches.png | 80218a8dfe8c03eca041c397afe4a255268c1d01540dceec8bfd49e6512c9c6c | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/school_summary.png | 1cd8c3b72373dd2665581572846863606d9d0ad7b90d1e58300e71019b7ee172 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/schools_and_programs.png | fc9031d72c1a75ed263d328d0a7cbe8838f3583ccdacbe2407c6fdcb803e9a4f | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/screening_and_exclusions.png | 6fd893e409835ed402244d9b1bdc1a46404d7edd6d6cdd2cc1ccd63a6708a16c | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/sources.png | 8c92bfa2817d319f87b2767d4d2d18a0ea4e206ee4b5c16319bf5f5a50204c7c | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/qa/this_weekend_outreach_queue.png | 5efbebbc5041a6c2f653966213f0c03461b22705271614b3f11296a05e04e5d4 | explicitly non-reproducible | No tracked command writes renders/qa; preserved visual-review snapshot |
| outputs/20260909-fall2027-audit/renders/school_summary.png | 75486803db12c59c1f70064defcec6f7670743bc391059123e7cb5fe03a17f93 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/schools_and_programs.png | 3a2f91731a289ee146fe591698a476ec7397ae192dc8ee3b8305935fdfdd095b | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/screening_and_exclusions.png | a576beb7206b7dacdef9d9a0d3a4d88794ab9ef5043c7d26b90b205d96a50726 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/sources.png | b44a2cdc579434c0dd48e98f4c14ee4e6125d8508a8f8dbd86792777a3ea1d31 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/renders/this_weekend_outreach_queue.png | 5c89c404c9fad972d27e2a2d9599b96eea2dd11c7aca16bcd40d45e971715e95 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/run_manifest.json | 2dc65a011d66f530e2939714525f198ec704e8ebe71c68ad37172b59abd80cb9 | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/finalize.py; src/graduate_audit/verify/final_validation.py |
| outputs/20260909-fall2027-audit/source_ledger.csv | e024f529b335948ab10b1db50d815161e1a8756f812fa9c6a8086c48d0fedeac | tracked producer | src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py |
| outputs/20260909-fall2027-audit/validation.json | b4b1d1eb2e7d2cd7c5663bb255b9de69d9f037b418e7711b56ddf9c5de95cc30 | tracked producer | src/graduate_audit/validation.py; src/graduate_audit/finalize.py |
| outputs/20260909-fall2027-audit/workbook_formula_error_scan.ndjson | acc0111e19cf44d2753fc9ecd164bf1b27fbd65597463a25cf48bd1c65e90146 | tracked producer | scripts/build_workbook.mjs |
| outputs/20260909-fall2027-audit/workbook_inspection.ndjson | 62d50cf0baf02e19446fec469c884602dee44986c5461634750dcc029e8ab6e0 | tracked producer | scripts/build_workbook.mjs |
| reports/20260909-fall2027-audit/coverage_report.md | 5c00af8f7200e24e5ca6659577b95a96b0c486c14751eece3536610df08c3ad6 | tracked producer | src/graduate_audit/reporting/reports.py |
| reports/20260909-fall2027-audit/final_shortlist.md | c715604de28deb7844bbc8ac54ed9a63f67749d847098c53a968cb06f1121406 | tracked producer | src/graduate_audit/reporting/reports.py |
| reports/20260909-fall2027-audit/methodology.md | 7c716119edacc1556672a2e052dbd4cf125df89c0c160c04da99025d3e67e20a | tracked producer | src/graduate_audit/reporting/reports.py |
| reports/20260909-fall2027-audit/strategic_findings.md | ac838ba017628b7ce5aa0b54c5216fb96ad06cdcbee8234212aa858c3310f65d | tracked producer | src/graduate_audit/reporting/reports.py |

## Completion-gate assessment

Stage 0 passes because the baseline commit and output checksums are frozen, every required artifact and workbook sheet is inventoried and classified, raw private Gmail/Calendar content is not tracked, the required defect classes are registered, and every current final output is either linked to a tracked producer or explicitly labeled non-reproducible. This pass diagnoses the baseline; it does not endorse the existing recommendations.
