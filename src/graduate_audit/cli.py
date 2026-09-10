from __future__ import annotations

import argparse
import json
from pathlib import Path

from .progress import update_progress
from .validation import validate_outputs

ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graduate-audit")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("universe")
    screen = sub.add_parser("screen")
    screen.add_argument("--region", choices=("us", "canada", "europe", "all"), default="all")
    sub.add_parser("research-fit")
    sub.add_parser("verify")
    sub.add_parser("score")
    validate = sub.add_parser("validate")
    validate.add_argument("--output-dir", default=str(ROOT / "outputs" / "current"))
    sub.add_parser("report")
    run = sub.add_parser("run")
    run.add_argument("--resume", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        result = validate_outputs(args.output_dir)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 1

    progress_path = ROOT / "state" / "progress.json"
    update_progress(progress_path, current_phase=args.command)
    print(f"Registered phase: {args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

