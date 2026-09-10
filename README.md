# Fall 2027 Graduate Program Discovery and Fit Audit

This repository builds a source-backed institutional universe and a disciplined application portfolio for Chimdumebi Mitchell Nebolisa. It covers the United States, Canada, the 27 EU member states, the United Kingdom, Norway, Switzerland, and Iceland.

The pipeline keeps bulk downloads and private Gmail/Calendar material out of Git. Dataset releases, checksums, retrieval dates, source failures, and validation results are captured in manifests and machine-readable outputs.

## Commands

Pass 2 commands operate on an explicit input bundle and a separate work directory. The input
bundle contract is documented in `reports/pass2/01_schema_versioning.md`. For example, the
synthetic acceptance fixture can be run with the bundled or any Python 3.11+ environment:

```powershell
python -m pip install -e .

$pass2Input = "tests/fixtures/pass2_pipeline/input"
$pass2Work = "data/processed/pass2/example_pipeline_run"

python -m graduate_audit universe --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit screen --input-dir $pass2Input --work-dir $pass2Work --region all
python -m graduate_audit research-fit --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit verify --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit score --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit portfolio --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit outreach --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit report --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit validate --input-dir $pass2Input --work-dir $pass2Work
python -m graduate_audit run --input-dir $pass2Input --work-dir $pass2Work --resume
```

Each completed stage writes a checkpoint under `<work-dir>/manifests/` with input and output
checksums, file dates, row counts, failures, and a run ID. `run --resume` verifies those records
in order and restarts at the first missing or invalid checkpoint. A single-stage command refuses
to run when its immediate prerequisite checkpoint is not valid.

The legacy Pass 1 output validator remains available as
`python -m graduate_audit validate --output-dir outputs/current`. Pass 2 commands do not rewrite
the committed Pass 1 recommendations.

## Safety boundaries

- Local Git only. Do not add or push to a remote.
- Google Calendar and Gmail access is read-only and limited to graduate-school context.
- Never create Gmail drafts, send mail, or modify Calendar events.
- Never commit raw email text, calendar exports, credentials, browser state, or large database downloads.
- Search snippets are discovery aids, not final evidence.
