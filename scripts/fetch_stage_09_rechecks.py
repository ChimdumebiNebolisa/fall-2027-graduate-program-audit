from __future__ import annotations

import csv
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
PASS2 = REPO_ROOT / "data/processed/pass2"
OUTPUT = REPO_ROOT / "data/raw/pass2/stage_09_live_rechecks.json"
USER_AGENT = "GraduateProgramAudit/2.0 (+independent evidence recheck)"


def read_csv(name: str) -> list[dict[str, str]]:
    with (PASS2 / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def urls_to_check() -> list[str]:
    portfolio = json.loads((PASS2 / "portfolio.json").read_text(encoding="utf-8"))
    core_ids = {row["program_id"] for row in portfolio["core"]}
    urls: set[str] = {row["official_program_url"] for row in portfolio["core"] if row["official_program_url"].startswith("http")}
    for source in read_csv("program_sources.csv"):
        if source["candidate_program_id"] in core_ids and source["official_or_secondary"].lower() == "official" and source["url"].startswith("http"):
            urls.add(source["url"])

    source_by_id = {row["stage4_source_id"]: row for row in read_csv("professor_sources.csv")}
    for professor in read_csv("professor_matches_retained.csv"):
        if professor["recruiting_status"] != "Confirmed recruiting":
            continue
        candidates = []
        for source_id in professor["source_ids"].split("|"):
            source = source_by_id.get(source_id)
            if source and any(term in source["claim_categories"].lower() for term in ("recruit", "prospective", "position", "hiring")):
                candidates.append(source["url"])
        url = candidates[0] if candidates else professor["official_faculty_or_lab_url"]
        if url.startswith("http"):
            urls.add(url)
    return sorted(urls)


def fetch(url: str) -> dict[str, object]:
    checked_at = datetime.now(timezone.utc).isoformat()
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8"},
            timeout=20,
            allow_redirects=True,
        )
        content_type = response.headers.get("content-type", "")
        return {
            "url": url,
            "status": "reachable" if response.status_code < 400 else "http_error",
            "http_status": response.status_code,
            "final_url": response.url,
            "content_type": content_type,
            "content_bytes": len(response.content),
            "checked_at": checked_at,
            "error": "" if response.status_code < 400 else f"HTTP {response.status_code}",
        }
    except requests.RequestException as exc:
        return {
            "url": url,
            "status": "request_error",
            "http_status": "",
            "final_url": "",
            "content_type": "",
            "content_bytes": 0,
            "checked_at": checked_at,
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> int:
    urls = urls_to_check()
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_url = {executor.submit(fetch, url): url for url in urls}
        for future in as_completed(future_to_url):
            results.append(future.result())
    results.sort(key=lambda row: str(row["url"]))
    payload = {
        "schema_version": "2.0",
        "purpose": "Live URL accessibility recheck only; substantive claims remain tied to the committed source ledger.",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "url_count": len(results),
        "reachable_count": sum(row["status"] == "reachable" for row in results),
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} URLs: {payload['reachable_count']} reachable")
    failures = [row for row in results if row["status"] != "reachable"]
    for row in failures:
        print(f"{row['status']}: {row['url']} ({row['error']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
