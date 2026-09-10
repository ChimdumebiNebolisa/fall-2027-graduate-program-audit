import json
from pathlib import Path

from graduate_audit.io import read_csv
from graduate_audit.program_reentry import _controlled_status, validate_program_reentry


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"


def test_controlled_reentry_status_uses_only_route_gates():
    assert _controlled_status("pass", "pass") == "retained"
    assert _controlled_status("pass", "resolvable_inquiry") == "conditional"
    assert _controlled_status("resolvable_question", "pass") == "conditional"
    assert _controlled_status("resolvable_question", "resolvable_inquiry") == "monitor"
    assert _controlled_status("pass", "unverified") == "monitor"


def test_stage3_reentry_artifacts_pass_incremental_gate():
    definitions = json.loads(
        (REPO_ROOT / "data/raw/pass2/stage_03_reentry_01.json").read_text(encoding="utf-8")
    )["programs"]
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    sources = read_csv(OUTPUT_DIR / "program_sources.csv")
    exclusions = read_csv(OUTPUT_DIR / "program_exclusions.csv")
    result = validate_program_reentry(definitions, verification, sources, exclusions)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 8
    assert result["counts"]["reentry_conditional"] == 2
    assert result["counts"]["reentry_monitor"] == 2
