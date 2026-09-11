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


def _validate_round(round_number: int):
    definitions = json.loads(
        (REPO_ROOT / f"data/raw/pass2/stage_03_reentry_{round_number:02d}.json").read_text(
            encoding="utf-8"
        )
    )["programs"]
    verification = read_csv(OUTPUT_DIR / "program_verification.csv")
    sources = read_csv(OUTPUT_DIR / "program_sources.csv")
    exclusions = read_csv(OUTPUT_DIR / "program_exclusions.csv")
    return validate_program_reentry(definitions, verification, sources, exclusions)


def test_stage3_reentry_01_artifacts_survive_cumulative_rebuild():
    result = _validate_round(1)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 8
    assert result["counts"]["reentry_conditional"] == 2
    assert result["counts"]["reentry_monitor"] == 2


def test_stage3_reentry_02_artifacts_pass_incremental_gate():
    result = _validate_round(2)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 3
    assert result["counts"]["reentry_conditional"] == 5
    assert result["counts"]["reentry_monitor"] == 4


def test_stage3_reentry_03_artifacts_pass_incremental_gate():
    result = _validate_round(3)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 1
    assert result["counts"]["reentry_conditional"] == 7
    assert result["counts"]["reentry_monitor"] == 4


def test_stage3_reentry_04_artifacts_pass_incremental_gate():
    result = _validate_round(4)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 2
    assert result["counts"]["reentry_conditional"] == 7
    assert result["counts"]["reentry_monitor"] == 3


def test_stage3_reentry_05_artifacts_pass_incremental_gate():
    result = _validate_round(5)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 1
    assert result["counts"]["reentry_conditional"] == 2
    assert result["counts"]["reentry_monitor"] == 9


def test_stage3_reentry_06_artifacts_pass_incremental_gate():
    result = _validate_round(6)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 0
    assert result["counts"]["reentry_conditional"] == 6
    assert result["counts"]["reentry_monitor"] == 6


def test_stage3_reentry_07_artifacts_pass_incremental_gate():
    result = _validate_round(7)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 3
    assert result["counts"]["reentry_conditional"] == 4
    assert result["counts"]["reentry_monitor"] == 5


def test_stage3_reentry_08_artifacts_pass_incremental_gate():
    result = _validate_round(8)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 2
    assert result["counts"]["reentry_conditional"] == 2
    assert result["counts"]["reentry_monitor"] == 8


def test_stage3_reentry_09_artifacts_pass_incremental_gate():
    result = _validate_round(9)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 3
    assert result["counts"]["reentry_conditional"] == 3
    assert result["counts"]["reentry_monitor"] == 6


def test_stage3_reentry_10_artifacts_pass_incremental_gate():
    result = _validate_round(10)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 0
    assert result["counts"]["reentry_conditional"] == 5
    assert result["counts"]["reentry_monitor"] == 7


def test_stage3_reentry_11_artifacts_pass_incremental_gate():
    result = _validate_round(11)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 1
    assert result["counts"]["reentry_conditional"] == 8
    assert result["counts"]["reentry_monitor"] == 3


def test_stage3_reentry_12_artifacts_pass_incremental_gate():
    result = _validate_round(12)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 0
    assert result["counts"]["reentry_conditional"] == 6
    assert result["counts"]["reentry_monitor"] == 6


def test_stage3_reentry_13_artifacts_pass_incremental_gate():
    result = _validate_round(13)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 2
    assert result["counts"]["reentry_conditional"] == 3
    assert result["counts"]["reentry_monitor"] == 7


def test_stage3_reentry_14_artifacts_pass_incremental_gate():
    result = _validate_round(14)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 2
    assert result["counts"]["reentry_conditional"] == 3
    assert result["counts"]["reentry_monitor"] == 7


def test_stage3_reentry_15_artifacts_pass_incremental_gate():
    result = _validate_round(15)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 1
    assert result["counts"]["reentry_conditional"] == 6
    assert result["counts"]["reentry_monitor"] == 5


def test_stage3_reentry_16_artifacts_pass_incremental_gate():
    result = _validate_round(16)

    assert result["validation_status"] == "PASS"
    assert all(result["assertions"].values())
    assert result["counts"]["reentry_retained"] == 1
    assert result["counts"]["reentry_conditional"] == 7
    assert result["counts"]["reentry_monitor"] == 4
