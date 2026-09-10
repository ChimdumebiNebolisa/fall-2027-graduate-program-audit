from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from graduate_audit.candidate_funnel import (  # noqa: E402
    DISCOVERY_PATHS,
    REGIONS,
    build_candidate_funnel,
    route_bucket,
    split_values,
)
from graduate_audit.io import read_csv, read_json, write_json  # noqa: E402
from graduate_audit.progress import update_progress  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "data/processed/pass2"
REPORT_PATH = REPO_ROOT / "reports/pass2/02_candidate_funnel.md"
MANIFEST_PATH = REPO_ROOT / "data/manifests/pass2/stage_02.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return sum(1 for _ in csv.DictReader(handle))
    return None


def file_record(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": row_count(path),
    }


def source_paths() -> list[Path]:
    paths = [
        REPO_ROOT / "config/applicant_profile.yaml",
        REPO_ROOT / "config/geographic_scope.yaml",
        REPO_ROOT / "config/research_topics.yaml",
        REPO_ROOT / "data/manifests/openalex_discovery.json",
        REPO_ROOT / "data/processed/openalex_institution_signals.csv",
        REPO_ROOT / "data/processed/openalex_faculty_signals.csv",
        REPO_ROOT / "reports/20260909-fall2027-audit/final_shortlist.md",
        REPO_ROOT / "src/graduate_audit/candidate_funnel.py",
        REPO_ROOT / "src/graduate_audit/research_fit/openalex_discovery.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
    ]
    for region in REGIONS:
        paths.extend(
            [
                REPO_ROOT / f"data/processed/regions/{region}/institution_universe.csv",
                REPO_ROOT / f"data/processed/regions/{region}/program_screening.csv",
                REPO_ROOT / f"data/processed/regions/{region}/exclusion_log.csv",
                REPO_ROOT / f"data/processed/deep_review/{region}/deep_programs.csv",
                REPO_ROOT / f"data/processed/deep_review/{region}/professors.csv",
            ]
        )
    return paths


def output_paths() -> list[Path]:
    return [
        OUTPUT_DIR / "candidate_program_funnel.csv",
        OUTPUT_DIR / "discovery_source_yield.csv",
        OUTPUT_DIR / "exclusion_sample_audit.csv",
        REPORT_PATH,
    ]


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


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


def write_report(result: dict[str, object]) -> None:
    candidates = read_csv(OUTPUT_DIR / "candidate_program_funnel.csv")
    yield_rows = read_csv(OUTPUT_DIR / "discovery_source_yield.csv")
    audit_rows = read_csv(OUTPUT_DIR / "exclusion_sample_audit.csv")
    active = [row for row in candidates if row["funnel_status"] != "screened_out"]
    counts = result["counts"]
    by_region_status = Counter((row["region"], row["funnel_status"]) for row in candidates)
    by_region_route = Counter((row["region"], route_bucket(row)) for row in active)
    by_region_topic = Counter()
    for row in active:
        for cluster in split_values(row["research_topic_clusters"]):
            by_region_topic[(row["region"], cluster)] += 1
    seed_examples: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in active:
        if row["funnel_status"] != "advance_to_stage_3":
            continue
        for seed in split_values(row["seed_adjacency"]):
            seed_examples[seed].append(row)
    audit_results = Counter(row["audit_result"] for row in audit_rows)
    active_missing_urls = sum(not row["official_program_url"] for row in active)

    report = [
        "# Pass 2 Stage 2 — High-recall candidate funnel",
        "",
        "Date: 2026-09-10",
        "Decision: **PASS with documented non-saturation**",
        "",
        "## Outcome",
        "",
        "Stage 2 rebuilt the discovery funnel from independent registry, official-program, "
        "department/research, recent-paper, current-faculty cross-match, lab/center, Calendar, "
        "first-audit, research-master/scholarship, and underrepresented-route paths. It does not "
        "score or recommend universities.",
        "",
        f"The OpenAlex exporter now retains all {counts['openalex_institution_rows']:,} observed "
        f"target-country institutions and all {counts['openalex_faculty_affiliation_rows']:,} "
        "author–institution pairs instead of a global top-300/top-1,000 slice. Downstream discovery "
        f"filtered {counts['openalex_non_educational_filtered']:,} non-educational institution "
        "records before candidate contribution.",
        "",
        "## Funnel counts",
        "",
        table(
            ["Measure", "Count"],
            [
                ["Funnel rows", counts["candidate_rows"]],
                ["Distinct institutions", counts["candidate_institutions"]],
                ["Advance to Stage 3", counts["advance_to_stage_3"]],
                ["Catalog verification required", counts["catalog_verification_required"]],
                ["Manual secondary review", counts["manual_secondary_review"]],
                ["Screened out with reason", counts["screened_out"]],
                ["Official program URL present", counts["official_program_url_present"]],
                ["Active rows missing official program URL", active_missing_urls],
            ],
        ),
        "",
        f"The {counts['screened_out']:,} screened-out rows remain in the funnel with explicit "
        "reasons. Single-source "
        "mechanical signals do not advance unless another independent path supports catalog review; "
        "duplicate mechanical rows at one institution are consolidated.",
        "",
        "## Regional and route coverage",
        "",
        table(
            ["Region", "Status", "Rows"],
            [
                [region, status, count]
                for (region, status), count in sorted(by_region_status.items())
            ],
        ),
        "",
        table(
            ["Region", "Priority route bucket", "Active rows"],
            [
                [region, route, count]
                for (region, route), count in sorted(by_region_route.items())
            ],
        ),
        "",
        "All three regions are represented. The active funnel includes bachelor's-entry doctoral "
        "routes, thesis/research master's routes, and structured or master's-required doctoral "
        "routes. Exact eligibility and funding remain Stage 3 questions.",
        "",
        "## Regional research-topic coverage",
        "",
        table(
            ["Region", "Research-topic cluster", "Active rows"],
            [
                [region, cluster, count]
                for (region, cluster), count in sorted(by_region_topic.items())
            ],
        ),
        "",
        "No regional or topic quota determined inclusion. Topic counts are coverage diagnostics, "
        "not university scores.",
        "",
        "## Discovery contribution and yield",
        "",
        table(
            [
                "Discovery path",
                "Examined",
                "Contributed",
                "Introduced",
                "Stage 3",
                "Review",
                "Screened out",
                "Active yield",
            ],
            [
                [
                    row["discovery_path"],
                    row["source_records_examined"],
                    row["candidate_rows_contributed"],
                    row["candidate_rows_introduced"],
                    row["advanced_to_stage_3"],
                    row["catalog_or_manual_review"],
                    row["screened_out"],
                    row["yield_rate"],
                ]
                for row in yield_rows
            ],
        ),
        "",
        "Active yield is the share of contributed rows that remains active after cross-path and "
        "deduplication checks. This makes noisy sources visible: registry and program-code paths "
        "provide breadth, while official-program and first-audit paths provide most immediately "
        "verifiable routes.",
        "",
        "## Known-seed recovery",
        "",
    ]
    for seed in ("TerraProbe-adjacent", "Evidex-adjacent"):
        examples = seed_examples.get(seed, [])[:8]
        report.extend(
            [
                f"### {seed}",
                "",
                table(
                    ["Institution", "Program", "Route", "Evidence confidence"],
                    [
                        [
                            row["institution_name"],
                            row["program_name"],
                            row["relevant_degree_route"],
                            row["evidence_confidence"],
                        ]
                        for row in examples
                    ],
                ),
                "",
            ]
        )
    report.extend(
        [
            "Both seed categories have exact official-program rows advancing to Stage 3. Seed "
            "adjacency is a discovery check, not a professor/recruiting claim.",
            "",
            "## Calendar recovery",
            "",
            f"The bounded prior report contained {counts['calendar_rows']} Calendar candidates. "
            f"Canonical registry and alias matching recovered {counts['calendar_in_scope_matched']}; "
            f"{counts['calendar_unmatched_or_out_of_scope']} remain unmatched or outside scope.",
            "",
            "Unmatched entries: "
            + ", ".join(result["unmatched_calendar_candidates"])
            + ". Gwangju Institute of Science and Technology is outside the configured geography. "
            "University of Limerick is in scope but absent from the incomplete European registry "
            "snapshot; it remains an explicit coverage gap rather than a negative finding.",
            "",
            "## Contamination and affiliation normalization",
            "",
            table(
                ["Check", "Count"],
                [
                    ["OpenAlex institution rows", counts["openalex_institution_rows"]],
                    ["Non-educational institutions filtered", counts["openalex_non_educational_filtered"]],
                    ["Educational institutions matched to registry", counts["openalex_matched_educational_institutions"]],
                    ["Educational institutions unmatched", counts["openalex_unmatched_educational_institutions"]],
                    ["Institution-name corrections", counts["openalex_institution_name_corrections"]],
                    ["Author–institution rows", counts["openalex_faculty_affiliation_rows"]],
                    ["Current official-faculty cross-matches", counts["openalex_faculty_current_official_matches"]],
                    ["Publication-time-only affiliations", counts["openalex_faculty_publication_time_only"]],
                    ["Faculty affiliations unmatched", counts["openalex_faculty_unmatched_affiliations"]],
                    ["Faculty affiliation-name corrections", counts["openalex_faculty_affiliation_name_corrections"]],
                ],
            ),
            "",
            "OpenAlex author affiliations are publication-time metadata. Only "
            f"{counts['openalex_faculty_current_official_matches']:,} rows cross-match a current "
            "official-faculty record from the first audit; all other author affiliations are "
            "excluded from the `current_faculty_topic_signal` path pending Stage 4.",
            "",
            "## Exclusion-sample audit",
            "",
            table(
                ["Audit result", "Rows"],
                [[result_name, count] for result_name, count in sorted(audit_results.items())],
            ),
            "",
            f"The {counts['exclusion_audit_sample_rows']}-row deterministic sample covers the United "
            "States, Canada, and Europe and all "
            "five normalized major exclusion strata. Every sample row records its original reason, "
            "source, independent signals, audit result, rationale, and false-negative risk.",
            "",
            f"{counts['exclusion_audit_reopened']} sampled exclusions had independent signals and "
            "were reopened in the funnel. "
            f"{counts['exclusion_audit_unresolved']} bounded mechanical exclusions had no independent "
            "positive signal but cannot be confirmed without exhaustive catalog inspection. "
            f"{counts['exclusion_audit_confirmed']} specialty/school-entity "
            "exclusions were confirmed by their original official-scope evidence and absence of a "
            "cross-signal.",
            "",
            "## Saturation decision",
            "",
            "**Saturation was not reached.** The sample exposed "
            f"{counts['exclusion_audit_reopened']} false-negative-risk cases, and "
            f"{counts['exclusion_audit_unresolved']} mechanical exclusions remain unresolved. The "
            "funnel therefore reopens independent "
            "cross-signal cases and preserves catalog-review candidates instead of claiming exhaustive "
            "negative coverage. This is acceptable for Stage 2 only because the limitation is explicit "
            "and no university is scored or recommended.",
            "",
            "## Blockers",
            "",
            "None prevented Stage 2 completion.",
            "",
            "## Unresolved coverage",
            "",
            "- The European registry snapshot remains incomplete: 3,628 unique records were captured "
            "from 4,462 reported filtered records, and University of Limerick is not present.",
            "- EHESO/ETER and several national-registry sources remain blocked from the first audit.",
            f"- {active_missing_urls} active candidates still require an exact official program "
            "URL/catalog determination.",
            f"- {counts['openalex_unmatched_educational_institutions']} educational OpenAlex "
            "institutions could not be normalized to the frozen regional "
            "registry and therefore did not contribute candidates.",
            f"- {counts['openalex_faculty_publication_time_only']:,} faculty affiliations are "
            f"publication-time only and {counts['openalex_faculty_unmatched_affiliations']:,} are "
            "unmatched; Stage 4 "
            "must verify current appointments and supervision authority.",
            "- Stage 2 does not verify program status, admission eligibility, funding, language, or "
            "Fall 2027 details; those belong to Stage 3.",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    started_at = now()
    source_commit = git_head()
    result = build_candidate_funnel(REPO_ROOT, OUTPUT_DIR)
    if result["validation"]["status"] != "PASS":
        raise RuntimeError(f"Stage 2 acceptance failed: {result['validation']}")
    write_report(result)

    progress_path = REPO_ROOT / "state/progress.json"
    progress = read_json(progress_path)
    pass2 = dict(progress.get("pass2", {}))
    stage_status = dict(pass2.get("stage_status", {}))
    stage_status["2"] = "complete"
    pass2.update(
        {
            "current_stage": 2,
            "last_completed_stage": 2,
            "stage_status": stage_status,
            "next_stage": 3,
            "next_stage_authorized": True,
            "authorization_mode": "agent_stage_gate_per_user_instruction",
            "stage_manifest": "data/manifests/pass2/stage_02.json",
            "stage_02_acceptance": "PASS",
        }
    )
    update_progress(
        progress_path,
        current_phase="pass2_stage_02_complete",
        pass2=pass2,
    )

    artifact_paths = [
        REPO_ROOT / "data/manifests/openalex_discovery.json",
        REPO_ROOT / "data/processed/openalex_institution_signals.csv",
        REPO_ROOT / "data/processed/openalex_faculty_signals.csv",
        REPO_ROOT / "src/graduate_audit/research_fit/openalex_discovery.py",
        REPO_ROOT / "src/graduate_audit/candidate_funnel.py",
        REPO_ROOT / "src/graduate_audit/schema.py",
        REPO_ROOT / "tests/test_candidate_funnel.py",
        REPO_ROOT / "scripts/build_stage_02.py",
        REPO_ROOT / "state/progress.json",
        *output_paths(),
    ]
    payload = {
        "manifest_version": "1.0",
        "schema_version": "2.0",
        "stage": 2,
        "name": "Rebuild the high-recall candidate funnel",
        "status": "complete",
        "decision": "PASS",
        "source_commit_before_stage": source_commit,
        "started_at": started_at,
        "completed_at": now(),
        "inputs": [file_record(path) for path in source_paths()],
        "outputs": [file_record(path) for path in output_paths()],
        "artifacts": [file_record(path) for path in artifact_paths],
        "validation": result["validation"],
        "counts": result["counts"],
        "source_counts": result["source_counts"],
        "unmatched_calendar_candidates": result["unmatched_calendar_candidates"],
        "failures": [],
        "blockers": [],
        "unresolved_coverage": [
            "European registry coverage remains 3,628 of 4,462 reported filtered ROR records.",
            "University of Limerick is an in-scope Calendar seed absent from the frozen registry snapshot.",
            "EHESO/ETER and several national registries remain blocked.",
            f"{result['counts']['catalog_verification_required'] + result['counts']['manual_secondary_review']} "
            "active candidates require exact official-program catalog resolution.",
            f"{result['counts']['openalex_unmatched_educational_institutions']} educational OpenAlex "
            "institutions could not be normalized to the regional registry.",
            "Most OpenAlex faculty affiliations remain publication-time-only or unmatched.",
            "Program eligibility, funding, language, and Fall 2027 evidence remain for Stage 3.",
        ],
    }
    write_json(MANIFEST_PATH, payload)
    print(f"Stage 2 manifest: {payload['decision']}")
    print(result["counts"])


if __name__ == "__main__":
    main()
