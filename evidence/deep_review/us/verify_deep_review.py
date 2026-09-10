from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.io import read_csv, write_json  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    EXCLUSION_COLUMNS,
    PROFESSOR_COLUMNS,
    PROGRAM_COLUMNS,
    RECRUITING_STATUSES,
    SOURCE_COLUMNS,
)


OUTPUT_DIR = REPO_ROOT / "data" / "processed" / "deep_review" / "us"
EVIDENCE_DIR = REPO_ROOT / "evidence" / "deep_review" / "us"


def headers(path: Path) -> tuple[str, ...]:
    import csv

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return tuple(next(csv.reader(handle)))


def check_url(url: str) -> dict[str, object]:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "GraduateProgramAudit/0.1 (source verification)"},
            timeout=25,
            stream=True,
            allow_redirects=True,
        )
        status = response.status_code
        result = {
            "url": url,
            "http_status": status,
            "final_url": response.url,
            "result": "reachable" if 200 <= status < 400 else "blocked" if status in {401, 403, 405, 406, 409, 429} else "unavailable",
            "error": "",
        }
        response.close()
        return result
    except requests.RequestException as exc:
        return {"url": url, "http_status": "", "final_url": "", "result": "unavailable", "error": str(exc)}


def validate(online: bool) -> tuple[dict[str, object], int]:
    programs = read_csv(OUTPUT_DIR / "deep_programs.csv")
    professors = read_csv(OUTPUT_DIR / "professors.csv")
    sources = read_csv(OUTPUT_DIR / "sources.csv")
    contacts = read_csv(OUTPUT_DIR / "admin_contacts.csv")
    exclusions = read_csv(OUTPUT_DIR / "exclusion_or_downgrade.csv")

    errors: list[str] = []
    if headers(OUTPUT_DIR / "deep_programs.csv") != PROGRAM_COLUMNS:
        errors.append("deep_programs.csv header mismatch")
    if headers(OUTPUT_DIR / "professors.csv") != PROFESSOR_COLUMNS:
        errors.append("professors.csv header mismatch")
    if headers(OUTPUT_DIR / "sources.csv") != SOURCE_COLUMNS:
        errors.append("sources.csv header mismatch")
    if headers(OUTPUT_DIR / "exclusion_or_downgrade.csv") != EXCLUSION_COLUMNS:
        errors.append("exclusion_or_downgrade.csv header mismatch")

    program_ids = {row["program_id"] for row in programs}
    professor_counts = Counter(row["program_id"] for row in professors)
    source_counts = Counter(row["program_id"] for row in sources)
    exclusion_counts = Counter(row["program_id"] for row in exclusions)
    if len(program_ids) != len(programs):
        errors.append("duplicate program identifiers")
    for row in programs:
        if professor_counts[row["program_id"]] < 1:
            errors.append(f"no professor for {row['program_id']}")
        if source_counts[row["program_id"]] < 3:
            errors.append(f"fewer than three sources for {row['program_id']}")
        professor_score = int(row["professor_fit_score"])
        depth_score = int(row["faculty_depth_score"])
        funding_score = int(row["funding_score"])
        eligibility_score = int(row["eligibility_score"])
        degree_score = int(row["degree_admissions_score"])
        economics_score = int(row["application_economics_score"])
        if not 0 <= professor_score <= 30 or not 0 <= depth_score <= 15:
            errors.append(f"research score outside bounds for {row['program_id']}")
        if not 0 <= funding_score <= 25 or not 0 <= eligibility_score <= 15:
            errors.append(f"funding/eligibility score outside bounds for {row['program_id']}")
        if not 0 <= degree_score <= 10 or not 0 <= economics_score <= 5:
            errors.append(f"degree/economics score outside bounds for {row['program_id']}")
        if int(row["research_fit_score"]) != professor_score + depth_score:
            errors.append(f"research score arithmetic mismatch for {row['program_id']}")
        if int(row["overall_score"]) != professor_score + depth_score + funding_score + eligibility_score + degree_score + economics_score:
            errors.append(f"overall score arithmetic mismatch for {row['program_id']}")
        if row["fall_2027_deadline"] and "Fall 2027" not in row["deadline_cycle_status"]:
            errors.append(f"unlabeled Fall 2027 deadline for {row['program_id']}")
        if row["screening_decision"] != "retained" and (not row["exclusion_reason"] or exclusion_counts[row["program_id"]] != 1):
            errors.append(f"non-retained program lacks reason/log for {row['program_id']}")
    for row in professors:
        if row["program_id"] not in program_ids:
            errors.append(f"orphan professor row {row['professor_id']}")
        if row["recruiting_status"] not in RECRUITING_STATUSES:
            errors.append(f"invalid recruiting status for {row['professor_id']}")
        if row["recruiting_status"] == "Confirmed recruiting" and not row["recruiting_evidence"]:
            errors.append(f"confirmed recruiting without evidence for {row['professor_id']}")

    online_rows: list[dict[str, object]] = []
    if online:
        urls = sorted({row["url"] for row in sources})
        with ThreadPoolExecutor(max_workers=12) as pool:
            futures = {pool.submit(check_url, url): url for url in urls}
            for future in as_completed(futures):
                online_rows.append(future.result())
        online_rows.sort(key=lambda row: str(row["url"]))
        write_json(EVIDENCE_DIR / "source_url_check.json", {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "method": "GET with redirects, streamed response headers, 25-second timeout",
            "interpretation": "HTTP blocking or transient unavailability does not negate a claim already reviewed in the official page; it is recorded for re-checking.",
            "counts": dict(Counter(str(row["result"]) for row in online_rows)),
            "results": online_rows,
        })

    summary = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "counts": {
            "programs": len(programs),
            "professors": len(professors),
            "sources": len(sources),
            "admin_contacts": len(contacts),
            "exclusion_or_downgrade": len(exclusions),
            "unique_source_urls_checked": len(online_rows),
            "source_url_results": dict(Counter(str(row["result"]) for row in online_rows)),
        },
    }
    print(json.dumps(summary, indent=2))
    return summary, 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    _, status = validate(args.online)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
