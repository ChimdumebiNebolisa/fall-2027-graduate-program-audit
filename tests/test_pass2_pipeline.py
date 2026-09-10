import inspect
import json
from pathlib import Path

import graduate_audit.pipeline as pipeline_module
from graduate_audit.cli import main
from graduate_audit.io import read_csv
from graduate_audit.pipeline import AuditPipeline, PIPELINE_STAGES


FIXTURE_INPUT = Path(__file__).parent / "fixtures" / "pass2_pipeline" / "input"


def test_fixture_end_to_end_creates_all_stage_outputs(tmp_path):
    work_dir = tmp_path / "audit"
    result = AuditPipeline(FIXTURE_INPUT, work_dir).run(resume=False)

    assert result["executed"] == list(PIPELINE_STAGES)
    assert (work_dir / "screening" / "programs.csv").exists()
    assert (work_dir / "evidence" / "program_evidence.csv").exists()
    assert (work_dir / "scoring" / "program_scores.csv").exists()
    assert (work_dir / "portfolio" / "portfolio.json").exists()
    assert (work_dir / "reports" / "audit_report.md").exists()

    scores = {row["program_id"]: row for row in read_csv(work_dir / "scoring" / "program_scores.csv")}
    assert scores["fixture:alpha:program:phd:computer-science"]["institution_name"] == (
        "Alpha Research University"
    )
    assert scores["fixture:alpha:program:phd:computer-science"]["recommendation"] == "Strong Apply"
    assert scores["fixture:beta:program:phd:information-science"]["recommendation"] == "Do Not Apply"

    portfolio = json.loads((work_dir / "portfolio" / "portfolio.json").read_text(encoding="utf-8"))
    assert [row["program_id"] for row in portfolio["core"]] == [
        "fixture:alpha:program:phd:computer-science"
    ]

    for stage in PIPELINE_STAGES:
        checkpoint = json.loads(
            (work_dir / "manifests" / f"{stage}.json").read_text(encoding="utf-8")
        )
        assert checkpoint["status"] == "complete"
        assert checkpoint["started_at"]
        assert checkpoint["completed_at"]
        assert "parameters" in checkpoint
        assert checkpoint["inputs"]
        assert checkpoint["outputs"]
        assert checkpoint["failures"] == []
        assert all(item["sha256"] and "row_count" in item for item in checkpoint["outputs"])

    implementation = inspect.getsource(pipeline_module)
    assert "Alpha Research University" not in implementation
    assert "Beta Technical University" not in implementation


def test_resume_starts_at_first_invalid_checkpoint(tmp_path):
    work_dir = tmp_path / "audit"
    pipeline = AuditPipeline(FIXTURE_INPUT, work_dir)
    pipeline.run(resume=False)
    before = {
        stage: json.loads(
            (work_dir / "manifests" / f"{stage}.json").read_text(encoding="utf-8")
        )["run_id"]
        for stage in PIPELINE_STAGES
    }
    with (work_dir / "scoring" / "program_scores.csv").open("a", encoding="utf-8") as handle:
        handle.write("corrupt\n")

    result = pipeline.run(resume=True)

    scoring_index = list(PIPELINE_STAGES).index("scoring")
    assert result["skipped"] == list(PIPELINE_STAGES[:scoring_index])
    assert result["executed"] == list(PIPELINE_STAGES[scoring_index:])
    after = {
        stage: json.loads(
            (work_dir / "manifests" / f"{stage}.json").read_text(encoding="utf-8")
        )["run_id"]
        for stage in PIPELINE_STAGES
    }
    assert after["verification"] == before["verification"]
    assert after["scoring"] != before["scoring"]


def test_cli_run_executes_fixture_pipeline(tmp_path):
    work_dir = tmp_path / "audit"
    progress_path = tmp_path / "progress.json"

    exit_code = main(
        [
            "run",
            "--input-dir",
            str(FIXTURE_INPUT),
            "--work-dir",
            str(work_dir),
            "--progress-path",
            str(progress_path),
        ]
    )

    assert exit_code == 0
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    assert progress["pipeline"]["last_valid_checkpoint"] == "reporting"
    assert (work_dir / "reports" / "audit_report.md").exists()


def test_each_documented_cli_stage_executes_in_order(tmp_path):
    work_dir = tmp_path / "audit"
    progress_path = tmp_path / "progress.json"
    shared = [
        "--input-dir",
        str(FIXTURE_INPUT),
        "--work-dir",
        str(work_dir),
        "--progress-path",
        str(progress_path),
    ]

    for command in (
        "universe",
        "screen",
        "research-fit",
        "verify",
        "score",
        "portfolio",
        "outreach",
        "report",
        "validate",
    ):
        assert main([command, *shared]) == 0

    assert AuditPipeline(FIXTURE_INPUT, work_dir).validate()["status"] == "PASS"
