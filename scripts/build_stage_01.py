from __future__ import annotations

import hashlib
import inspect
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import graduate_audit.pipeline as pipeline_module  # noqa: E402
from graduate_audit.io import read_json, write_json  # noqa: E402
from graduate_audit.pipeline import AuditPipeline, PIPELINE_STAGES  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_record(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def stage_artifacts() -> list[Path]:
    fixed = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "src/graduate_audit/cli.py",
        REPO_ROOT / "src/graduate_audit/finalize.py",
        REPO_ROOT / "src/graduate_audit/hard_gates.py",
        REPO_ROOT / "src/graduate_audit/pipeline.py",
        REPO_ROOT / "src/graduate_audit/portfolio.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "src/graduate_audit/validation.py",
        REPO_ROOT / "tests/test_hard_gates.py",
        REPO_ROOT / "tests/test_pass2_pipeline.py",
        REPO_ROOT / "tests/test_portfolio.py",
        REPO_ROOT / "tests/test_schema.py",
        REPO_ROOT / "tests/test_validation.py",
        REPO_ROOT / "reports/pass2/01_pipeline_repair.md",
        REPO_ROOT / "reports/pass2/01_schema_versioning.md",
        REPO_ROOT / "scripts/build_stage_01.py",
        REPO_ROOT / "state/progress.json",
    ]
    fixtures = sorted((REPO_ROOT / "tests/fixtures/pass2_pipeline/input").glob("*.csv"))
    return fixed + fixtures


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def main() -> None:
    started_at = now()
    fixture_input = REPO_ROOT / "tests/fixtures/pass2_pipeline/input"
    with tempfile.TemporaryDirectory(prefix="graduate-audit-stage1-") as temporary:
        work_dir = Path(temporary) / "work"
        pipeline = AuditPipeline(fixture_input, work_dir)
        initial = pipeline.run(resume=False)
        initial_validation = pipeline.validate()
        clean_resume = pipeline.run(resume=True)
        with (work_dir / "scoring/program_scores.csv").open("a", encoding="utf-8") as handle:
            handle.write("corrupt\n")
        repair_resume = pipeline.run(resume=True)
        final_validation = pipeline.validate()
        summary = read_json(work_dir / "reports/run_summary.json")

    expected_stages = list(PIPELINE_STAGES)
    scoring_index = expected_stages.index("scoring")
    assertions = {
        "initial_run_executed_all_stages": initial["executed"] == expected_stages,
        "initial_validation_passed": initial_validation["status"] == "PASS",
        "clean_resume_skipped_all_stages": clean_resume["skipped"] == expected_stages,
        "invalid_score_resume_preserved_prior_stages": (
            repair_resume["skipped"] == expected_stages[:scoring_index]
        ),
        "invalid_score_resume_reran_downstream": (
            repair_resume["executed"] == expected_stages[scoring_index:]
        ),
        "final_validation_passed": final_validation["status"] == "PASS",
        "screening_evidence_scoring_portfolio_report_created": all(
            summary["counts"].get(key, 0) > 0
            for key in (
                "screened_programs",
                "verified_program_records",
                "scored_programs",
                "core",
            )
        ),
        "fixture_names_not_hard_coded": all(
            name not in inspect.getsource(pipeline_module)
            for name in ("Alpha Research University", "Beta Technical University")
        ),
    }
    failed = [name for name, passed in assertions.items() if not passed]
    if failed:
        raise RuntimeError(f"Stage 1 acceptance failed: {failed}")

    progress_path = REPO_ROOT / "state/progress.json"
    progress = read_json(progress_path)
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["1"] = "complete"
    pass2.update(
        {
            "current_stage": 1,
            "last_completed_stage": 1,
            "stage_status": stage_status,
            "next_stage": 2,
            "next_stage_authorized": False,
            "stage_manifest": "data/manifests/pass2/stage_01.json",
            "stage_01_acceptance": "PASS",
        }
    )
    update_progress(
        progress_path,
        current_phase="pass2_stage_01_complete",
        pass2=pass2,
    )

    payload = {
        "manifest_version": "1.0",
        "stage": 1,
        "name": "Repair the executable pipeline and contracts",
        "status": "complete",
        "decision": "PASS",
        "source_commit_before_stage": git_head(),
        "started_at": started_at,
        "completed_at": now(),
        "acceptance_assertions": assertions,
        "fixture_run": {
            "initial": initial,
            "initial_validation": initial_validation,
            "clean_resume": clean_resume,
            "invalid_checkpoint_resume": repair_resume,
            "final_validation": final_validation,
            "summary": summary,
        },
        "artifacts": [artifact_record(path) for path in stage_artifacts()],
        "blockers": [],
        "unresolved_coverage": [
            "The 56 real Pass 1 scored rows remain unmigrated and unrescored.",
            "Real professor-depth and supervision-authority evidence remains for Stage 3.",
            "Regional discovery recall gaps remain for Stage 2.",
            "Admissions, funding, language, and Fall 2027 evidence remains for Stage 4.",
            "The Pass 1 portfolio and outreach artifacts remain unchanged pending Stages 6-8.",
            "The synthetic fixture verifies orchestration and contracts, not real-world coverage.",
        ],
    }
    write_json(REPO_ROOT / "data/manifests/pass2/stage_01.json", payload)
    print(f"Stage 1 manifest: {payload['decision']}")


if __name__ == "__main__":
    main()
