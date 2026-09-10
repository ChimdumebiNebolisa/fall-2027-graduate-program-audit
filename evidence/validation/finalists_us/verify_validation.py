from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "processed" / "validation" / "finalists_us"
ALLOWED = {"confirmed", "qualified", "conflict"}
REQUIRED = {
    "portfolio_tier",
    "institution_id",
    "institution_name",
    "program_id",
    "program_name",
    "faculty_name",
    "faculty_url",
    "faculty_result",
    "faculty_note",
    "primary_claim",
    "primary_url",
    "second_url",
    "result",
    "correction_needed",
    "checked_date",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        assert set(reader.fieldnames or []) == REQUIRED
        return list(reader)


def check_urls(rows: list[dict[str, str]]) -> None:
    for row in rows:
        for field in ("primary_url", "second_url"):
            parsed = urlparse(row[field])
            assert parsed.scheme == "https" and parsed.netloc, (row["program_id"], field)
        assert row["primary_url"] != row["second_url"], row["program_id"]


def main() -> None:
    programs = read_csv("program_checks.csv")
    exclusions = read_csv("exclusion_sample_checks.csv")
    summary = json.loads((OUT / "validation.json").read_text(encoding="utf-8"))

    assert len(programs) == 19
    assert Counter(row["portfolio_tier"] for row in programs) == {
        "current_core": 18,
        "corrected_to_reserve": 1,
    }
    assert len(exclusions) == 5
    assert len({row["program_id"] for row in programs}) == 19
    assert len({row["program_id"] for row in exclusions}) == 5
    assert not ({row["program_id"] for row in programs} & {row["program_id"] for row in exclusions})

    for row in programs + exclusions:
        assert row["result"] in ALLOWED
        assert row["checked_date"] == "2026-09-09"
        assert row["primary_claim"].strip()
        if row["result"] == "conflict":
            assert row["correction_needed"].strip()
    for row in programs:
        assert row["faculty_name"].strip()
        assert row["faculty_result"] in {"confirmed", "qualified"}
        parsed = urlparse(row["faculty_url"])
        assert parsed.scheme == "https" and parsed.netloc
        assert row["faculty_note"].strip()
    check_urls(programs + exclusions)

    assert summary["scope"]["current_core_programs"] == 18
    assert summary["scope"]["corrected_former_core_programs"] == 1
    assert summary["scope"]["total_program_rows"] == 19
    assert summary["scope"]["sampled_us_exclusions"] == 5
    assert summary["program_results"] == dict(sorted(Counter(row["result"] for row in programs).items()))
    assert summary["exclusion_sample_results"] == dict(
        sorted(Counter(row["result"] for row in exclusions).items())
    )
    correction_count = sum(bool(row["correction_needed"].strip()) for row in programs + exclusions)
    assert summary["pending_correction_count"] == correction_count == len(
        summary["pending_corrections"]
    )
    assert summary["resolved_correction_count"] == len(summary["resolved_corrections"]) == 1
    assert len(summary["portfolio_sha256"]) == 64
    print(
        json.dumps(
            {
                "program_rows": len(programs),
                "program_results": dict(Counter(row["result"] for row in programs)),
                "exclusion_rows": len(exclusions),
                "exclusion_results": dict(Counter(row["result"] for row in exclusions)),
                "corrections": correction_count,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
