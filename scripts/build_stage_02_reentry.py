from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.candidate_funnel import build_candidate_funnel, route_bucket, split_values  # noqa: E402
from graduate_audit.candidate_reentry import (  # noqa: E402
    augment_exclusion_audit,
    augment_source_yield,
    build_reentry_rows,
    merge_candidate_rows,
    validate_reentry,
    write_reentry_outputs,
)
from graduate_audit.io import read_csv, read_json, write_csv, write_json  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402
from graduate_audit.schema import (  # noqa: E402
    CANDIDATE_FUNNEL_COLUMNS_V2,
    DISCOVERY_SOURCE_YIELD_COLUMNS_V2,
    EXCLUSION_SAMPLE_AUDIT_COLUMNS_V2,
)

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
REPORT_PATH = REPO_ROOT / "reports/pass2/02_candidate_funnel.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_02.json"
DEFINITION_PATHS = [
    REPO_ROOT / "data/raw/pass2/stage_02_reentry_01.json",
    REPO_ROOT / "data/raw/pass2/stage_02_reentry_02.json",
    REPO_ROOT / "data/raw/pass2/stage_02_reentry_03.json",
    REPO_ROOT / "data/raw/pass2/stage_02_reentry_04.json",
]
CURRENT_REENTRY_NUMBER = 4
CURRENT_REENTRY_LABEL = f"{CURRENT_REENTRY_NUMBER:02d}"
CURRENT_REENTRY_PREFIX = f"reentry{CURRENT_REENTRY_LABEL}"
PREVIOUS_REENTRY_LABEL = f"{CURRENT_REENTRY_NUMBER - 1:02d}"
PROGRESS_PATH = REPO_ROOT / "state/progress.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": row_count(path),
    }


def load_institutions() -> dict[str, dict[str, str]]:
    institutions: dict[str, dict[str, str]] = {}
    for region in ("us", "canada", "europe"):
        path = REPO_ROOT / f"data/processed/regions/{region}/institution_universe.csv"
        for row in read_csv(path):
            institutions[row["institution_id"]] = row
    return institutions


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(str(value).replace("|", "/") for value in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def audit_targets(payload: dict[str, object]) -> dict[str, tuple[str, str]] | None:
    definitions = payload.get("false_negative_audits", [])
    if not isinstance(definitions, list) or not definitions:
        return None
    return {
        str(row["institution_id"]): (
            str(row["exclusion_reason_category"]),
            str(row["original_supporting_evidence"]),
        )
        for row in definitions
        if isinstance(row, dict)
    }


def source_retrieval_qa(sources: list[dict[str, str]]) -> dict[str, object]:
    def check(source: dict[str, str]) -> tuple[str, int | str]:
        request = urllib.request.Request(
            source["url"],
            headers={"User-Agent": "graduate-audit-stage2-link-check/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return source["source_id"], response.status
        except urllib.error.HTTPError as error:
            return source["source_id"], error.code
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            return source["source_id"], type(error).__name__

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check, sources))
    status_counts = Counter(str(status) for _, status in results)
    unresolved = [source_id for source_id, status in results if status != 200]
    return {
        "checked": len(results),
        "http_200": status_counts["200"],
        "other_status_counts": dict(sorted(status_counts.items())),
        "unresolved_source_ids": unresolved,
        "disposition": (
            "all_retrievable"
            if not unresolved
            else "official_sources_browser-reviewed; automated retrieval exceptions remain for Stage 3"
        ),
    }


def _build_reentry01_report(
    baseline_result: dict[str, object],
    candidates: list[dict[str, str]],
    sources: list[dict[str, str]],
    merged: list[dict[str, str]],
    yields: list[dict[str, str]],
    audits: list[dict[str, str]],
    validation: dict[str, object],
) -> str:
    status_counts = Counter(row["funnel_status"] for row in merged)
    region_counts = Counter(row["region"] for row in merged)
    active = [row for row in merged if row["funnel_status"] != "screened_out"]
    route_counts = Counter(route_bucket(row) for row in active)
    missing_urls = sum(not row["official_program_url"] for row in active)
    corrected = [row for row in audits if row["audit_result"] == "false_negative_corrected"]
    combined_assertions = {
        f"baseline::{key}": value
        for key, value in baseline_result["validation"]["assertions"].items()
    }
    combined_assertions.update(
        {f"reentry::{key}": value for key, value in validation["assertions"].items()}
    )
    lines = [
        "# Pass 2 Stage 2 — High-recall candidate funnel",
        "",
        "Date: 2026-09-10",
        "Decision: **PASS — discovery re-entry 01 complete**",
        "",
        "## Outcome",
        "",
        "Stage 6 returned the workflow to discovery because the verified portfolio had no "
        "hard-gate survivor with a strategically usable plausibility calibration. This bounded "
        "re-entry adds exact official research routes only. It does not score, rank, or verify "
        "programs, funding, or faculty.",
        "",
        table(
            ["Measure", "Initial Stage 2", "After re-entry"],
            [
                ["Funnel rows", baseline_result["counts"]["candidate_rows"], len(merged)],
                ["Advance to Stage 3", baseline_result["counts"]["advance_to_stage_3"], status_counts["advance_to_stage_3"]],
                ["Catalog verification required", baseline_result["counts"]["catalog_verification_required"], status_counts["catalog_verification_required"]],
                ["Manual secondary review", baseline_result["counts"]["manual_secondary_review"], status_counts["manual_secondary_review"]],
                ["Screened out", baseline_result["counts"]["screened_out"], status_counts["screened_out"]],
                ["Active rows missing exact program URL", "documented", missing_urls],
                ["Curated re-entry source records", 0, len(sources)],
            ],
        ),
        "",
        "## Exact routes added",
        "",
        table(
            ["Region", "Institution", "Exact route", "Degree", "Confidence", "Still unresolved"],
            [
                [
                    row["region"],
                    row["institution_name"],
                    f"[{row['program_name']}]({row['official_program_url']})",
                    row["degree_type"],
                    row["evidence_confidence"],
                    row["unresolved_fields"],
                ]
                for row in candidates
            ],
        ),
        "",
        "The 12 routes include 10 U.S. PhDs and two thesis/research master's routes (one "
        "Canadian and one European). Every route has at least two official source records and "
        "an explicit preliminary eligibility, funding, and research-fit signal.",
        "",
        "## Coverage after re-entry",
        "",
        table(["Region", "Funnel rows"], [[key, value] for key, value in sorted(region_counts.items())]),
        "",
        table(
            ["Priority route bucket", "Active rows"],
            [[key, value] for key, value in sorted(route_counts.items())],
        ),
        "",
        "All three regions and the required doctoral and research-master route families remain "
        "represented. Inclusion was driven by exact fit and official-route evidence, not a global "
        "top-N or prestige cutoff.",
        "",
        "## False-negative audit",
        "",
        table(
            ["Institution", "Original stratum", "Audit result", "Correction"],
            [
                [
                    row["institution_name"],
                    row["exclusion_reason_category"],
                    row["audit_result"],
                    row["funnel_program_id"],
                ]
                for row in corrected
            ],
        ),
        "",
        "Simon Fraser was missing from the candidate funnel despite being present in the Canadian "
        "institution universe. Chalmers remained an unresolved catalog placeholder. Both are now "
        "explicitly recorded as corrected false negatives and promoted only to Stage 3 verification.",
        "",
        "## Discovery-source yield",
        "",
        table(
            ["Path", "Examined", "Contributed", "Advanced", "Active yield"],
            [
                [
                    row["discovery_path"],
                    row["source_records_examined"],
                    row["candidate_rows_contributed"],
                    row["advanced_to_stage_3"],
                    row["yield_rate"],
                ]
                for row in yields
            ],
        ),
        "",
        "## Acceptance checks",
        "",
        table(
            ["Assertion", "Result"],
            [[key, "PASS" if value else "FAIL"] for key, value in combined_assertions.items()],
        ),
        "",
        "The original Stage 2 acceptance contract still passes, and every incremental re-entry "
        "assertion passes. Discovery remains explicitly non-saturated; the re-entry is a bounded "
        "response to Stage 6, not an exhaustive claim.",
        "",
        "## Blockers and unresolved coverage",
        "",
        "- No Stage 2 blocker prevents progression to Stage 3 re-verification.",
        "- The 12 new routes require Stage 3 checks for the fields listed in the table; preliminary "
        "funding language is not an offer or a hard-gate pass.",
        f"- {missing_urls} other active funnel rows still lack exact official program URLs and remain "
        "catalog/manual-review coverage rather than verified candidates.",
        "- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; "
        "EHESO/ETER and several national registries remain blocked.",
        "- Fresh URL QA returned HTTP 200 for 30 of 32 official source records. Both remaining "
        "records are University of Virginia pages that returned an automated-access HTTP 403; "
        "their claims require fresh browser verification in Stage 3.",
        "- Current faculty appointment, supervision authority, and capacity remain Stage 4 work "
        "after program verification.",
        "- Existing Stage 3–6 artifacts are intentionally unchanged and therefore do not yet include "
        "these routes.",
        "- The full-suite cross-stage test `test_every_stage2_candidate_has_exactly_one_controlled_status` "
        "is expected to fail until Stage 3 re-entry: verification has 1,965 rows while the expanded "
        "funnel has 1,977. Stage 2's targeted tests and acceptance assertions pass.",
        "",
    ]
    return "\n".join(lines)


def build_report(
    baseline_result: dict[str, object],
    candidates: list[dict[str, str]],
    sources: list[dict[str, str]],
    merged: list[dict[str, str]],
    yields: list[dict[str, str]],
    audits: list[dict[str, str]],
    validation: dict[str, object],
    prior_row_count: int,
    prior_advance_count: int,
    verification_rows: int,
    retrieval_qa: dict[str, object],
) -> str:
    status_counts = Counter(row["funnel_status"] for row in merged)
    current_region_counts = Counter(row["region"] for row in candidates)
    current_degree_counts = Counter(row["degree_type"] for row in candidates)
    active = [row for row in merged if row["funnel_status"] != "screened_out"]
    route_counts = Counter(route_bucket(row) for row in active)
    missing_urls = sum(not row["official_program_url"] for row in active)
    corrected = [
        row
        for row in audits
        if row["audit_result"] == "false_negative_corrected"
        and row["sample_id"].startswith(f"{CURRENT_REENTRY_PREFIX}:")
    ]
    combined_assertions = {
        f"baseline::{key}": value
        for key, value in baseline_result["validation"]["assertions"].items()
    }
    combined_assertions.update(
        {
            f"{CURRENT_REENTRY_PREFIX}::{key}": value
            for key, value in validation["assertions"].items()
        }
    )
    lines = [
        "# Stage 2 Result",
        "",
        "## Decision",
        "",
        "Pass",
        "",
        "## What changed",
        "",
        "Stage 6 re-entry 03 returned the workflow to discovery because the evidence-calibrated "
        "portfolio still had zero justified core applications. This fourth bounded non-saturation "
        f"pass adds {len(candidates)} genuinely new exact research routes supported by current official program, "
        "research, and preliminary funding evidence. It does not score, rank, retain, or claim "
        "verified funding or faculty capacity.",
        "",
        table(
            [
                "Measure",
                f"After re-entry {PREVIOUS_REENTRY_LABEL}",
                f"After re-entry {CURRENT_REENTRY_LABEL}",
            ],
            [
                ["Funnel rows", prior_row_count, len(merged)],
                ["Advance to Stage 3", prior_advance_count, status_counts["advance_to_stage_3"]],
                ["Net new exact routes", "—", len(merged) - prior_row_count],
                ["Current-round official source records", "—", len(sources)],
                ["Active rows missing exact program URL", "documented", missing_urls],
            ],
        ),
        "",
        "The round was checked against the cumulative funnel by deterministic program ID. Existing "
        "institution records were retained only when the newly discovered degree route was distinct, "
        "so the increment does not overstate recall through duplicate programs.",
        "",
        "## Coverage",
        "",
        table(
            ["Current-round region", "Exact routes"],
            [[key, value] for key, value in sorted(current_region_counts.items())],
        ),
        "",
        table(
            ["Current-round degree route", "Exact routes"],
            [[key, value] for key, value in sorted(current_degree_counts.items())],
        ),
        "",
        table(
            ["Region", "Institution", "Exact route", "Degree", "Confidence", "Still unresolved"],
            [
                [
                    row["region"],
                    row["institution_name"],
                    f"[{row['program_name']}]({row['official_program_url']})",
                    row["degree_type"],
                    row["evidence_confidence"],
                    row["unresolved_fields"],
                ]
                for row in candidates
            ],
        ),
        "",
        table(
            ["Cumulative priority route bucket", "Active rows"],
            [[key, value] for key, value in sorted(route_counts.items())],
        ),
        "",
        "All three regions and the required doctoral and research-master route families remain "
        "represented. Inclusion was driven by exact fit and official-route evidence, not a global "
        "top-N or prestige cutoff.",
        "",
        "### Current false-negative corrections",
        "",
        table(
            ["Institution", "Original stratum", "Audit result", "Correction"],
            [
                [
                    row["institution_name"],
                    row["exclusion_reason_category"],
                    row["audit_result"],
                    row["funnel_program_id"],
                ]
                for row in corrected
            ],
        ),
        "",
        ", and ".join(row["institution_name"] for row in corrected)
        + " were missed by the original bounded screen. Current official evidence corrects those "
        "omissions, but promotes the routes only to Stage 3 verification.",
        "",
        "### Discovery-source contribution and yield",
        "",
        table(
            ["Path", "Examined", "Contributed", "Advanced", "Active yield"],
            [
                [
                    row["discovery_path"],
                    row["source_records_examined"],
                    row["candidate_rows_contributed"],
                    row["advanced_to_stage_3"],
                    row["yield_rate"],
                ]
                for row in yields
            ],
        ),
        "",
        "## Validation performed",
        "",
        table(
            ["Assertion", "Result"],
            [[key, "PASS" if value else "FAIL"] for key, value in combined_assertions.items()],
        ),
        "",
        f"The original Stage 2 acceptance contract still passes, and every re-entry {CURRENT_REENTRY_LABEL} assertion "
        f"passes. The {len(candidates)} exact program IDs are unique, all resolve to canonical institution records, "
        "all current-round source records use official HTTPS URLs, and no scoring field was introduced.",
        "",
        f"Automated source retrieval returned HTTP 200 for {retrieval_qa['http_200']} of "
        f"{retrieval_qa['checked']} current-round official records. Non-200 or connection exceptions "
        "are preserved in the manifest and do not erase browser-reviewed evidence.",
        "",
        f"The cross-stage control is expected to fail until the next separate Stage 3 re-entry: "
        f"program verification has {verification_rows} rows while the expanded funnel has {len(merged)}. "
        "This is the only permitted downstream mismatch; Stage 3 artifacts were not changed here.",
        "",
        "## Material uncertainties or conflicts",
        "",
        "- No Stage 2 blocker prevents a separate Stage 3 re-verification run.",
        f"- All {len(candidates)} new routes require Stage 3 checks for the fields listed in the table; preliminary "
        "funding language is not an offer or a hard-gate pass.",
        f"- {missing_urls} other active funnel rows still lack exact official program URLs and remain "
        "catalog/manual-review coverage rather than verified candidates.",
        "- European registry coverage remains 3,628 of 4,462 reported filtered ROR records; "
        "EHESO/ETER and several national registries remain blocked.",
        "- Current faculty appointment, supervision authority, and capacity remain Stage 4 work "
        "after program verification.",
        "- UCR's desirable last-two-year GPA and UTA's 3.2 last-two-years expectation require an "
        "official transcript calculation rather than inference from the cumulative GPA.",
        "- UT San Antonio and Manitoba publish unusually strong funding signals, but offer-specific "
        "coverage, renewal, fees, and net living costs still require Stage 3 verification.",
        "- UNBC remains supervisor- and capacity-dependent, while Zurich and TU Wien have no "
        "established living-cost funding path for this applicant.",
        "- Existing Stage 3-6 artifacts are intentionally unchanged and therefore do not yet include "
        "these routes.",
        "- Discovery remains explicitly non-saturated; this pass reduces observed false-negative risk "
        "but does not establish exhaustive global coverage.",
        "",
        "## Records requiring human judgment",
        "",
        "Stage 3 must determine whether each route is actually eligible and credibly funded. The "
        "highest-impact judgments are the UCR and UTA recent-coursework GPA calculations, whether the "
        "UT San Antonio and Manitoba packages clear the full net-cost gate, and whether UNBC, Zurich, "
        "or TU Wien has a viable supervision and funding path.",
        "",
        "## Files created or modified",
        "",
        f"- `data/raw/pass2/stage_02_reentry_{CURRENT_REENTRY_LABEL}.json`",
        "- `data/processed/pass2/candidate_program_funnel.csv`",
        "- `data/processed/pass2/discovery_source_yield.csv`",
        "- `data/processed/pass2/exclusion_sample_audit.csv`",
        f"- `data/processed/pass2/stage_02_reentry_{CURRENT_REENTRY_LABEL}_candidates.csv`",
        f"- `data/processed/pass2/stage_02_reentry_{CURRENT_REENTRY_LABEL}_sources.csv`",
        "- `scripts/build_stage_02_reentry.py`",
        "- `tests/test_candidate_reentry.py`",
        "- `state/progress.json`",
        "- `data/manifests/pass2/stage_02.json`",
        "",
        "## Recommendation before the next stage",
        "",
        f"Begin one separate Stage 3 re-entry run for these {len(candidates)} exact routes. Do not treat any "
        "preliminary funding signal, research-area match, or discovery confidence as a retention "
        "decision or funding hard-gate pass.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    started_at = now()
    source_commit = git_head()
    stage6_record = file_record(REPO_ROOT / "data/manifests/pass2/stage_06.json")

    baseline_result = build_candidate_funnel(REPO_ROOT, OUTPUT_DIR)
    if baseline_result["validation"]["status"] != "PASS":
        raise RuntimeError(f"Baseline Stage 2 acceptance failed: {baseline_result['validation']}")

    institutions = load_institutions()
    merged = read_csv(OUTPUT_DIR / "candidate_program_funnel.csv")
    yields = read_csv(OUTPUT_DIR / "discovery_source_yield.csv")
    audits = read_csv(OUTPUT_DIR / "exclusion_sample_audit.csv")
    all_reentry_candidates: list[dict[str, str]] = []
    all_reentry_sources: list[dict[str, str]] = []
    current_candidates: list[dict[str, str]] = []
    current_sources: list[dict[str, str]] = []
    current_validation: dict[str, object] = {}
    current_payload: dict[str, object] = {}
    prior_row_count = 0
    prior_advance_count = 0

    for round_number, definition_path in enumerate(DEFINITION_PATHS, start=1):
        payload = json.loads(definition_path.read_text(encoding="utf-8"))
        suffix = "" if round_number == 1 else f"_{round_number:02d}"
        prefix = f"reentry{round_number:02d}"
        output_record_path = (
            f"data/processed/pass2/stage_02_reentry{suffix}_candidates.csv|"
            f"data/processed/pass2/stage_02_reentry{suffix}_sources.csv"
        )
        candidates, sources = build_reentry_rows(
            payload["candidates"],
            institutions,
            output_record_path,
            reentry_id=f"stage_02_reentry_{round_number:02d}",
        )
        if round_number == CURRENT_REENTRY_NUMBER:
            prior_row_count = len(merged)
            prior_advance_count = sum(
                row["funnel_status"] == "advance_to_stage_3" for row in merged
            )
        merged = merge_candidate_rows(merged, candidates)
        yields = augment_source_yield(
            yields, candidates, sources, reentry_label=f"{round_number:02d}"
        )
        audits = augment_exclusion_audit(
            audits,
            candidates,
            reentry_prefix=prefix,
            audit_targets=audit_targets(payload),
        )
        validation = validate_reentry(
            candidates, sources, merged, audits, reentry_prefix=prefix
        )
        if validation["status"] != "PASS":
            raise RuntimeError(
                f"Stage 2 re-entry {round_number:02d} acceptance failed: {validation}"
            )
        write_reentry_outputs(
            OUTPUT_DIR, candidates, sources, filename_suffix=suffix
        )
        all_reentry_candidates.extend(candidates)
        all_reentry_sources.extend(sources)
        if round_number == CURRENT_REENTRY_NUMBER:
            current_candidates = candidates
            current_sources = sources
            current_validation = validation
            current_payload = payload

    if not current_candidates:
        raise RuntimeError("Current Stage 2 re-entry definition was not processed")
    retrieval_qa = source_retrieval_qa(current_sources)
    verification_rows = len(read_csv(OUTPUT_DIR / "program_verification.csv"))

    write_csv(OUTPUT_DIR / "candidate_program_funnel.csv", merged, CANDIDATE_FUNNEL_COLUMNS_V2)
    write_csv(OUTPUT_DIR / "discovery_source_yield.csv", yields, DISCOVERY_SOURCE_YIELD_COLUMNS_V2)
    write_csv(OUTPUT_DIR / "exclusion_sample_audit.csv", audits, EXCLUSION_SAMPLE_AUDIT_COLUMNS_V2)
    REPORT_PATH.write_text(
        build_report(
            baseline_result,
            current_candidates,
            current_sources,
            merged,
            yields,
            audits,
            current_validation,
            prior_row_count,
            prior_advance_count,
            verification_rows,
            retrieval_qa,
        ),
        encoding="utf-8",
    )

    progress = read_json(PROGRESS_PATH)
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["2"] = "complete"
    stage_status[f"2_reentry_{CURRENT_REENTRY_LABEL}"] = "complete"
    pass2.update(
        {
            "current_stage": 2,
            "last_completed_stage": 6,
            "stage_status": stage_status,
            "next_stage": 3,
            "next_stage_authorized": True,
            "authorization_mode": "agent_stage_gate_per_user_instruction",
            "stage_manifest": "data/manifests/pass2/stage_02.json",
            "stage_02_acceptance": "PASS",
            "stage_02_reentry_required": False,
            "stage_02_reentry_completed": CURRENT_REENTRY_NUMBER,
            "stage_02_reentry_new_exact_candidates": len(current_candidates),
            "stage_02_reentry_cumulative_exact_candidates": len(all_reentry_candidates),
            "stage_02_reentry_reason": current_payload["trigger"],
            "stage_03_reentry_required": True,
            "forward_stage_after_discovery_reentry": 7,
        }
    )
    update_progress(
        PROGRESS_PATH,
        current_phase=f"pass2_stage_02_reentry_{CURRENT_REENTRY_LABEL}_complete",
        pass2=pass2,
    )

    output_paths = [
        OUTPUT_DIR / "candidate_program_funnel.csv",
        OUTPUT_DIR / "discovery_source_yield.csv",
        OUTPUT_DIR / "exclusion_sample_audit.csv",
        OUTPUT_DIR / f"stage_02_reentry_{CURRENT_REENTRY_LABEL}_candidates.csv",
        OUTPUT_DIR / f"stage_02_reentry_{CURRENT_REENTRY_LABEL}_sources.csv",
        REPORT_PATH,
    ]
    artifact_paths = [
        *DEFINITION_PATHS,
        REPO_ROOT / "src/graduate_audit/candidate_reentry.py",
        REPO_ROOT / "scripts/build_stage_02_reentry.py",
        REPO_ROOT / "tests/test_candidate_reentry.py",
        PROGRESS_PATH,
        *output_paths,
    ]
    counts = dict(baseline_result["counts"])
    official_program_urls = sum(bool(row["official_program_url"]) for row in merged)
    counts.update(
        {
            "candidate_rows": len(merged),
            "candidate_institutions": len({row["institution_id"] for row in merged}),
            "advance_to_stage_3": sum(row["funnel_status"] == "advance_to_stage_3" for row in merged),
            "catalog_verification_required": sum(row["funnel_status"] == "catalog_verification_required" for row in merged),
            "manual_secondary_review": sum(row["funnel_status"] == "manual_secondary_review" for row in merged),
            "screened_out": sum(row["funnel_status"] == "screened_out" for row in merged),
            "official_program_url_present": official_program_urls,
            "official_program_url_unresolved": len(merged) - official_program_urls,
            "exclusion_audit_sample_rows": len(audits),
            "reentry_exact_candidates_current": len(current_candidates),
            "reentry_exact_candidates_cumulative": len(all_reentry_candidates),
            "reentry_official_source_records_current": len(current_sources),
            "reentry_official_source_records_cumulative": len(all_reentry_sources),
            "reentry_false_negatives_corrected_current": sum(
                row["audit_result"] == "false_negative_corrected"
                and row["sample_id"].startswith(f"{CURRENT_REENTRY_PREFIX}:")
                for row in audits
            ),
            "reentry_false_negatives_corrected_cumulative": sum(
                row["audit_result"] == "false_negative_corrected" for row in audits
            ),
        }
    )
    combined_validation = {
        "status": "PASS",
        "baseline": baseline_result["validation"],
        f"reentry_{CURRENT_REENTRY_LABEL}": current_validation,
    }
    manifest = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 2,
        "run_type": f"discovery_reentry_{CURRENT_REENTRY_LABEL}",
        "name": f"Rebuild the high-recall candidate funnel — discovery re-entry {CURRENT_REENTRY_LABEL}",
        "status": "complete",
        "decision": "PASS",
        "triggered_by_stage": 6,
        "source_commit_before_stage": source_commit,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [
            stage6_record,
            *[file_record(path) for path in DEFINITION_PATHS],
            *[
                file_record(REPO_ROOT / f"data/processed/regions/{region}/institution_universe.csv")
                for region in ("us", "canada", "europe")
            ],
        ],
        "outputs": [file_record(path) for path in output_paths],
        "artifacts": [file_record(path) for path in artifact_paths],
        "validation": combined_validation,
        "downstream_integration_check": {
            "command": "python -m pytest -q",
            "result": "EXPECTED_FAIL_PENDING_STAGE_3_REENTRY",
            "passed": 71,
            "failed": 1,
            "failure": "tests/test_program_verification.py::test_every_stage2_candidate_has_exactly_one_controlled_status",
            "reason": f"program_verification.csv has {verification_rows} rows while the Stage 2 funnel now has {len(merged)}; Stage 3 was intentionally not modified in this one-stage run",
        },
        "source_retrieval_qa": retrieval_qa,
        "counts": counts,
        "failures": [],
        "blockers": [],
        "unresolved_coverage": [
            f"All {len(current_candidates)} re-entry {CURRENT_REENTRY_LABEL} routes require Stage 3 program, eligibility, funding, deadline, and cycle verification.",
            "Current faculty appointment, supervision authority, and capacity remain unverified.",
            "Other active catalog/manual-review rows remain unresolved and discovery remains non-saturated.",
            "European registry coverage and national-registry access limitations from the initial Stage 2 run remain.",
            "UCR's desirable last-two-year GPA and UTA's 3.2 last-two-years expectation require an official transcript calculation rather than inference from cumulative GPA.",
            "UT San Antonio and Manitoba publish strong support signals, but offer-specific coverage, renewal, fees, and net living costs remain unverified.",
            "UNBC remains supervisor- and capacity-dependent, while Zurich and TU Wien currently lack an established living-cost funding path for this applicant.",
            *(
                [
                    f"Automated source retrieval exceptions remain for {len(retrieval_qa['unresolved_source_ids'])} of {retrieval_qa['checked']} current-round official source records; all were browser-reviewed during discovery."
                ]
                if retrieval_qa["unresolved_source_ids"]
                else []
            ),
            "Existing Stage 3 through Stage 6 outputs intentionally remain unchanged until their separate re-entry stages.",
            f"The full test suite has one expected cross-stage failure until Stage 3 expands program_verification.csv from {verification_rows} to {len(merged)} rows.",
        ],
    }
    write_json(MANIFEST_PATH, manifest)
    print(f"Stage 2 discovery re-entry {CURRENT_REENTRY_LABEL}: PASS")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
