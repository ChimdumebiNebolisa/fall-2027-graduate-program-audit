# Fall 2027 Graduate Program Discovery and Fit Audit

This repository builds a source-backed institutional universe and a disciplined application portfolio for Chimdumebi Mitchell Nebolisa. It covers the United States, Canada, the 27 EU member states, the United Kingdom, Norway, Switzerland, and Iceland.

The pipeline keeps bulk downloads and private Gmail/Calendar material out of Git. Dataset releases, checksums, retrieval dates, source failures, and validation results are captured in manifests and machine-readable outputs.

## Commands

Run with the bundled or any Python 3.11+ environment:

```powershell
python -m graduate_audit universe
python -m graduate_audit screen --region us
python -m graduate_audit research-fit
python -m graduate_audit verify
python -m graduate_audit score
python -m graduate_audit validate
python -m graduate_audit report
python -m graduate_audit run --resume
```

During this audit, phase-specific scripts and generated outputs are registered in `run_manifest.json`. Raw datasets are downloaded to the ignored `data/raw/` directory; normalized and final CSV outputs are tracked.

## Safety boundaries

- Local Git only. Do not add or push to a remote.
- Google Calendar and Gmail access is read-only and limited to graduate-school context.
- Never create Gmail drafts, send mail, or modify Calendar events.
- Never commit raw email text, calendar exports, credentials, browser state, or large database downloads.
- Search snippets are discovery aids, not final evidence.

