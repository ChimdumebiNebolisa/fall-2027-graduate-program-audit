from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import AuditPipeline, PipelineError
from .progress import update_progress
from .validation import validate_outputs

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = ROOT / "data" / "pipeline_input"
DEFAULT_WORK_DIR = ROOT / "data" / "processed" / "pipeline"
DEFAULT_PROGRESS_PATH = ROOT / "state" / "progress.json"

COMMAND_STAGES = {
    "universe": "discovery",
    "screen": "screening",
    "research-fit": "research_fit",
    "verify": "verification",
    "score": "scoring",
    "portfolio": "portfolio",
    "outreach": "outreach",
    "report": "reporting",
}


def _add_pipeline_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR))
    parser.add_argument("--work-dir", default=str(DEFAULT_WORK_DIR))
    parser.add_argument("--progress-path", default=str(DEFAULT_PROGRESS_PATH))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graduate-audit")
    sub = parser.add_subparsers(dest="command", required=True)
    universe = sub.add_parser("universe")
    _add_pipeline_paths(universe)
    screen = sub.add_parser("screen")
    _add_pipeline_paths(screen)
    screen.add_argument("--region", choices=("us", "canada", "europe", "all"), default="all")
    for command in ("research-fit", "verify", "score", "portfolio", "outreach", "report"):
        stage_parser = sub.add_parser(command)
        _add_pipeline_paths(stage_parser)
    validate = sub.add_parser("validate")
    _add_pipeline_paths(validate)
    validate.add_argument(
        "--output-dir",
        help="validate a legacy Pass 1 output directory instead of Pass 2 checkpoints",
    )
    run = sub.add_parser("run")
    _add_pipeline_paths(run)
    run.add_argument("--resume", action="store_true")
    run.add_argument("--region", choices=("us", "canada", "europe", "all"), default="all")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate" and args.output_dir:
            result = validate_outputs(args.output_dir)
        else:
            region = getattr(args, "region", "all")
            pipeline = AuditPipeline(args.input_dir, args.work_dir, region=region)
            if args.command == "validate":
                result = pipeline.validate()
            elif args.command == "run":
                result = pipeline.run(resume=args.resume)
            else:
                result = pipeline.run_stage(COMMAND_STAGES[args.command])
        update_progress(
            args.progress_path,
            current_phase=f"pipeline_{args.command}",
            pipeline={
                "status": result["status"],
                "last_valid_checkpoint": result.get("last_valid_checkpoint"),
                "executed": result.get("executed", []),
                "skipped": result.get("skipped", []),
            },
        )
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in {"complete", "PASS"} else 1
    except (OSError, PipelineError, ValueError) as error:
        update_progress(
            args.progress_path,
            current_phase=f"pipeline_{args.command}_failed",
            pipeline={"status": "failed", "error": str(error)},
        )
        print(json.dumps({"status": "FAIL", "error": str(error)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
