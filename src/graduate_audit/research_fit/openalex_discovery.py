from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests
import yaml

ROOT = Path(__file__).resolve().parents[3]
API_URL = "https://api.openalex.org/works"
USER_AGENT = "GraduateProgramAudit/0.1 (mailto:chimdumebinebolisa@gmail.com)"

TARGET_COUNTRY_CODES = {
    "US", "CA", "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT",
    "RO", "SK", "SI", "ES", "SE", "GB", "NO", "CH", "IS",
}


def load_queries() -> list[str]:
    config = yaml.safe_load((ROOT / "config" / "research_topics.yaml").read_text(encoding="utf-8"))
    return [query for group in config["discovery_query_clusters"].values() for query in group]


def _get_with_backoff(session: requests.Session, params: dict[str, object]) -> requests.Response:
    for attempt in range(6):
        response = session.get(API_URL, params=params, timeout=60)
        if response.status_code != 429:
            response.raise_for_status()
            return response
        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
        time.sleep(min(delay, 30))
    response.raise_for_status()
    return response


def fetch_query(session: requests.Session, query: str, per_query: int) -> tuple[list[dict], list[str]]:
    results: list[dict] = []
    urls: list[str] = []
    cursor = "*"
    while len(results) < per_query and cursor:
        params = {
            "search": query,
            "filter": f"from_publication_date:2022-01-01,to_publication_date:{date.today().isoformat()}",
            "sort": "relevance_score:desc",
            "per-page": min(100, per_query - len(results)),
            "cursor": cursor,
            "select": "id,doi,title,publication_year,publication_date,cited_by_count,authorships,primary_location,type",
        }
        response = _get_with_backoff(session, params)
        urls.append(response.url)
        payload = response.json()
        batch = payload.get("results", [])
        results.extend(batch)
        cursor = payload.get("meta", {}).get("next_cursor") if batch else None
        if len(results) < per_query and cursor:
            time.sleep(0.15)
    return results, urls


def discover(per_query: int = 200) -> dict[str, object]:
    queries = load_queries()
    raw_root = ROOT / "data" / "raw" / "openalex"
    processed_root = ROOT / "data" / "processed"
    manifest_root = ROOT / "data" / "manifests"
    raw_root.mkdir(parents=True, exist_ok=True)
    processed_root.mkdir(parents=True, exist_ok=True)
    manifest_root.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    raw_path = raw_root / "query_results.json"
    if raw_path.exists():
        all_query_results = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        all_query_results = {}
    request_urls: list[str] = []
    failures: list[dict[str, str]] = []

    for query in queries:
        if len(all_query_results.get(query, [])) >= per_query:
            continue
        try:
            works, urls = fetch_query(session, query, per_query)
            all_query_results[query] = works
            request_urls.extend(urls)
        except Exception as exc:  # preserve query-level failure and continue
            failures.append({"query": query, "error": str(exc)})

    raw_bytes = json.dumps(all_query_results, ensure_ascii=False).encode("utf-8")
    raw_path.write_bytes(raw_bytes)
    checksum = hashlib.sha256(raw_bytes).hexdigest()

    institution_stats: dict[str, dict[str, object]] = {}
    author_stats: dict[tuple[str, str], dict[str, object]] = {}
    work_rows: list[dict[str, object]] = []

    for query, works in all_query_results.items():
        for rank, work in enumerate(works, start=1):
            title = work.get("title") or ""
            citations = int(work.get("cited_by_count") or 0)
            base_weight = 1 / (1 + rank / 25) + min(math.log1p(citations) / 5, 1)
            work_id = work.get("id", "")
            seen_institutions: set[str] = set()

            for authorship in work.get("authorships") or []:
                author = authorship.get("author") or {}
                author_id = author.get("id") or ""
                author_name = author.get("display_name") or ""
                for institution in authorship.get("institutions") or []:
                    institution_id = institution.get("id") or ""
                    country_code = institution.get("country_code") or ""
                    if not institution_id or country_code not in TARGET_COUNTRY_CODES:
                        continue
                    inst_name = institution.get("display_name") or ""
                    inst_type = institution.get("type") or ""
                    ror = institution.get("ror") or ""
                    if institution_id not in seen_institutions:
                        record = institution_stats.setdefault(institution_id, {
                            "openalex_institution_id": institution_id,
                            "institution_name": inst_name,
                            "country_code": country_code,
                            "institution_type": inst_type,
                            "ror_id": ror,
                            "weighted_signal": 0.0,
                            "work_ids": set(),
                            "queries": set(),
                            "top_works": [],
                            "authors": set(),
                        })
                        record["weighted_signal"] = float(record["weighted_signal"]) + base_weight
                        record["work_ids"].add(work_id)
                        record["queries"].add(query)
                        record["top_works"].append((base_weight, title, work.get("publication_year"), work.get("doi") or work_id))
                        seen_institutions.add(institution_id)
                    record["authors"].add(author_name)

                    if author_id:
                        key = (author_id, institution_id)
                        faculty = author_stats.setdefault(key, {
                            "openalex_author_id": author_id,
                            "author_name": author_name,
                            "openalex_institution_id": institution_id,
                            "institution_name": inst_name,
                            "country_code": country_code,
                            "ror_id": ror,
                            "weighted_signal": 0.0,
                            "work_ids": set(),
                            "queries": set(),
                            "top_works": [],
                        })
                        faculty["weighted_signal"] = float(faculty["weighted_signal"]) + base_weight
                        faculty["work_ids"].add(work_id)
                        faculty["queries"].add(query)
                        faculty["top_works"].append((base_weight, title, work.get("publication_year"), work.get("doi") or work_id))

            work_rows.append({
                "query": query,
                "rank": rank,
                "work_id": work_id,
                "doi": work.get("doi") or "",
                "title": title,
                "publication_year": work.get("publication_year") or "",
                "publication_date": work.get("publication_date") or "",
                "cited_by_count": citations,
                "type": work.get("type") or "",
            })

    institution_rows = []
    for record in institution_stats.values():
        top = sorted(record["top_works"], reverse=True)[:5]
        institution_rows.append({
            "openalex_institution_id": record["openalex_institution_id"],
            "institution_name": record["institution_name"],
            "country_code": record["country_code"],
            "institution_type": record["institution_type"],
            "ror_id": record["ror_id"],
            "weighted_signal": round(float(record["weighted_signal"]), 3),
            "relevant_work_count": len(record["work_ids"]),
            "query_cluster_count": len(record["queries"]),
            "author_count": len(record["authors"]),
            "top_works": " || ".join(f"{year}: {title} [{url}]" for _, title, year, url in top),
        })

    faculty_rows = []
    for record in author_stats.values():
        top = sorted(record["top_works"], reverse=True)[:5]
        faculty_rows.append({
            "openalex_author_id": record["openalex_author_id"],
            "author_name": record["author_name"],
            "openalex_institution_id": record["openalex_institution_id"],
            "institution_name": record["institution_name"],
            "country_code": record["country_code"],
            "ror_id": record["ror_id"],
            "weighted_signal": round(float(record["weighted_signal"]), 3),
            "relevant_work_count": len(record["work_ids"]),
            "query_cluster_count": len(record["queries"]),
            "top_works": " || ".join(f"{year}: {title} [{url}]" for _, title, year, url in top),
        })

    pd.DataFrame(institution_rows).sort_values(
        ["weighted_signal", "relevant_work_count"], ascending=False
    ).head(300).to_csv(processed_root / "openalex_institution_signals.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(faculty_rows).sort_values(
        ["weighted_signal", "relevant_work_count"], ascending=False
    ).head(1000).to_csv(processed_root / "openalex_faculty_signals.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(work_rows).to_csv(processed_root / "openalex_query_works.csv", index=False, encoding="utf-8-sig")

    manifest = {
        "source": "OpenAlex Works API",
        "base_url": API_URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "query_window": {"from": "2022-01-01", "to": date.today().isoformat()},
        "queries": queries,
        "per_query_requested": per_query,
        "request_urls": request_urls,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_sha256": checksum,
        "raw_bytes": len(raw_bytes),
        "query_failures": failures,
        "counts": {
            "query_results": sum(len(v) for v in all_query_results.values()),
            "institutions_ranked": len(institution_rows),
            "author_institution_pairs": len(faculty_rows),
        },
        "limitations": [
            "Search relevance is a discovery signal, not final research-fit evidence.",
            "Authorship affiliations are publication-time metadata and require current official verification.",
        ],
    }
    manifest_path = manifest_root / "openalex_discovery.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-query", type=int, default=200)
    args = parser.parse_args()
    print(json.dumps(discover(args.per_query), indent=2))


if __name__ == "__main__":
    main()
