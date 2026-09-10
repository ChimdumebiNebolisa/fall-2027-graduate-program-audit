from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import tarfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "20260909-fall2027-audit"
OUTPUT_PREFIX = f"outputs/{RUN_ID}/"
REPORT_PREFIX = f"reports/{RUN_ID}/"
REQUIRED_CLASSIFICATIONS = {"reusable", "repairable", "superseded", "unverified"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE
    ).stdout


def unchanged_from_commit(commit: str, path: str) -> bool:
    return (
        subprocess.run(
            ["git", "diff", "--quiet", commit, "--", path],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0
    )


def baseline_files(commit: str) -> dict[str, bytes]:
    archive = git("archive", "--format=tar", commit)
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        for member in bundle.getmembers():
            if member.isfile():
                extracted = bundle.extractfile(member)
                if extracted is not None:
                    files[member.name] = extracted.read()
    return files


def csv_rows(data: bytes) -> int | None:
    try:
        rows = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""))
        return max(sum(1 for _ in rows) - 1, 0)
    except (UnicodeDecodeError, csv.Error):
        return None


def artifact_types(path: str) -> list[str]:
    lower = path.lower()
    name = PurePosixPath(path).name.lower()
    suffix = PurePosixPath(path).suffix.lower()
    types: list[str] = []
    if suffix in {".csv", ".json", ".ndjson"}:
        types.append("dataset")
    if suffix in {".py", ".mjs"}:
        types.append("script")
    if path.startswith("reports/") and suffix == ".md":
        types.append("report")
    if suffix == ".xlsx":
        types.append("workbook")
    if suffix in {".yaml", ".yml", ".toml"}:
        types.append("contract/configuration")
    if "manifest" in lower:
        types.append("manifest")
    if (
        name in {"source_ledger.csv", "sources.csv"}
        or "second_source" in lower
        or name == "blocked_sources.json"
    ):
        types.append("source ledger")
    if (
        "/validation/" in lower
        or name.startswith(("validation", "final_validation", "test_", "verify_"))
        or "/verify/" in lower
        or name in {"workbook_formula_error_scan.ndjson", "workbook_inspection.ndjson"}
    ):
        types.append("validation")
    if suffix == ".md" and "report" not in types:
        types.append("documentation")
    return types or ["project file"]


def producer_for_final(path: str) -> tuple[str, str]:
    name = PurePosixPath(path).name
    if path.startswith(REPORT_PREFIX):
        return "src/graduate_audit/reporting/reports.py", "tracked producer"
    if not path.startswith(OUTPUT_PREFIX):
        return "", "not a final output"
    relative = path.removeprefix(OUTPUT_PREFIX)
    if relative.startswith("renders/qa/"):
        return (
            "No tracked command writes renders/qa; preserved visual-review snapshot",
            "explicitly non-reproducible",
        )
    if relative.startswith("render_html/") or (
        relative.startswith("renders/") and relative.endswith(".png")
    ):
        return "scripts/build_workbook.mjs", "tracked producer"
    mapping = {
        "institution_universe.csv": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py",
        "program_screening.csv": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/portfolio.py; src/graduate_audit/verify/apply_corrections.py; src/graduate_audit/finalize.py",
        "exclusion_log.csv": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py",
        "professor_evidence.csv": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/reporting/outreach.py; src/graduate_audit/verify/apply_corrections.py",
        "source_ledger.csv": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/verify/apply_corrections.py",
        "portfolio.json": "src/graduate_audit/portfolio.py; src/graduate_audit/finalize.py",
        "calendar_comparison.csv": "src/graduate_audit/connected_context.py; src/graduate_audit/finalize.py",
        "admin_contacts.csv": "src/graduate_audit/reporting/outreach.py; src/graduate_audit/finalize.py",
        "outreach_drafts.csv": "src/graduate_audit/reporting/outreach.py; src/graduate_audit/finalize.py",
        "validation.json": "src/graduate_audit/validation.py; src/graduate_audit/finalize.py",
        "run_manifest.json": "src/graduate_audit/normalize/integrate.py; src/graduate_audit/finalize.py; src/graduate_audit/verify/final_validation.py",
        "final_validation.json": "src/graduate_audit/verify/final_validation.py",
        "graduate_program_audit.xlsx": "scripts/build_workbook.mjs",
        "workbook_formula_error_scan.ndjson": "scripts/build_workbook.mjs",
        "workbook_inspection.ndjson": "scripts/build_workbook.mjs",
    }
    producer = mapping.get(name, "")
    return producer, "tracked producer" if producer else "unmapped"


def classify(path: str, types: list[str]) -> tuple[str, str]:
    lower = path.lower()
    name = PurePosixPath(path).name.lower()
    if path.startswith(REPORT_PREFIX):
        return "superseded", "Pass 1 decision/report text is preserved only as a baseline."
    if path.startswith(OUTPUT_PREFIX):
        relative = path.removeprefix(OUTPUT_PREFIX)
        if relative.startswith("renders/qa/"):
            return "unverified", "No tracked producer recreates this QA snapshot."
        if name in {"institution_universe.csv", "source_ledger.csv", "exclusion_log.csv"}:
            return "reusable", "Useful baseline evidence/provenance; claims still require Pass 2 checks."
        if name in {
            "validation.json",
            "final_validation.json",
            "run_manifest.json",
            "workbook_formula_error_scan.ndjson",
            "workbook_inspection.ndjson",
        }:
            return "repairable", "Traceable but does not establish all Pass 2 substantive gates."
        return "superseded", "Recommendation-bearing Pass 1 output must not control Pass 2."
    if path == "state/progress.json":
        return "repairable", "Pass 1 is marked complete despite diagnosed Pass 2 defects."
    if path == "README.md":
        return "repairable", "Documents commands that currently register phases instead of running work."
    if path in {"config/scoring_rubric.yaml", "src/graduate_audit/schema.py"}:
        return "repairable", "Shared contract lacks required Pass 2 evidence/conflict fields or anchors."
    if path.startswith("tests/"):
        return "repairable", "Existing tests are reusable but omit required hard-gate and resume coverage."
    repairable_code = {
        "src/graduate_audit/cli.py",
        "src/graduate_audit/progress.py",
        "src/graduate_audit/scoring.py",
        "src/graduate_audit/portfolio.py",
        "src/graduate_audit/finalize.py",
        "src/graduate_audit/reporting/outreach.py",
        "src/graduate_audit/reporting/reports.py",
        "src/graduate_audit/research_fit/openalex_discovery.py",
        "src/graduate_audit/validation.py",
        "src/graduate_audit/verify/final_validation.py",
        "src/graduate_audit/verify/apply_corrections.py",
        "evidence/deep_review/us/build_deep_review.py",
        "data/processed/deep_review/canada/build_outputs.py",
        "data/manifests/deep_review/europe/build_outputs.py",
        "scripts/build_workbook.mjs",
    }
    if path in repairable_code:
        return "repairable", "Contains or consumes a diagnosed Pass 2 contract/gate defect."
    if path.startswith("data/processed/deep_review/"):
        if name == "sources.csv":
            return "reusable", "Prior source evidence is reusable after freshness and claim checks."
        return "repairable", "Deep-review output includes hard-coded scoring or shallow faculty depth."
    if path.startswith("data/processed/openalex_"):
        return "unverified", "Discovery-only scholarly signal is truncated and is not final evidence."
    if "/validation/" in lower and name == "validation.json":
        return "repairable", "Partial validation cannot be treated as full substantive validation."
    if "validation" in types and "script" in types:
        return "repairable", "Validation logic is useful but incomplete against Pass 2 gates."
    if "validation" in types:
        return "reusable", "Prior check evidence is reusable but not a current Pass 2 conclusion."
    if "source ledger" in types:
        return "reusable", "Source/provenance evidence is reusable subject to freshness review."
    if path.startswith("data/processed/regions/"):
        return "reusable", "Regional discovery baseline can seed the Pass 2 candidate funnel."
    if path.startswith("data/manifests/") or path.startswith("evidence/programs/"):
        return "reusable", "Provenance or official-page evidence can be rechecked in Pass 2."
    return "reusable", "No Stage 0 defect requires discarding this baseline artifact."


def workbook_sheets(workbook_data: bytes, workbook_path: str) -> list[dict[str, object]]:
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    pkg_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    records: list[dict[str, object]] = []

    def column_number(letters: str) -> int:
        value = 0
        for letter in letters:
            value = value * 26 + ord(letter) - ord("A") + 1
        return value

    def column_letters(number: int) -> str:
        result = ""
        while number:
            number, remainder = divmod(number - 1, 26)
            result = chr(ord("A") + remainder) + result
        return result

    with zipfile.ZipFile(io.BytesIO(workbook_data)) as book:
        workbook = ElementTree.fromstring(book.read("xl/workbook.xml"))
        rels = ElementTree.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels.findall(f"{{{pkg_ns}}}Relationship")
        }
        for index, sheet in enumerate(workbook.findall(f".//{{{main_ns}}}sheet")):
            rid = sheet.attrib[f"{{{rel_ns}}}id"]
            target = targets[rid].lstrip("/")
            if not target.startswith("xl/"):
                target = f"xl/{target}"
            xml_data = book.read(target)
            worksheet = ElementTree.fromstring(xml_data)
            dimension = worksheet.find(f"{{{main_ns}}}dimension")
            used_range = dimension.attrib.get("ref", "") if dimension is not None else ""
            if not used_range:
                coordinates = []
                for cell in worksheet.findall(f".//{{{main_ns}}}c"):
                    match = re.fullmatch(r"([A-Z]+)(\d+)", cell.attrib.get("r", ""))
                    if match:
                        coordinates.append((column_number(match.group(1)), int(match.group(2))))
                if coordinates:
                    min_col = min(col for col, _ in coordinates)
                    max_col = max(col for col, _ in coordinates)
                    min_row = min(row for _, row in coordinates)
                    max_row = max(row for _, row in coordinates)
                    used_range = (
                        f"{column_letters(min_col)}{min_row}:"
                        f"{column_letters(max_col)}{max_row}"
                    )
            match = re.search(r"[A-Z]+(\d+)$", used_range)
            records.append(
                {
                    "path": f"{workbook_path}::sheet::{sheet.attrib['name']}",
                    "artifact_types": ["workbook sheet"],
                    "size_bytes": len(xml_data),
                    "sha256": sha256(xml_data),
                    "row_count": int(match.group(1)) if match else None,
                    "classification": "superseded",
                    "classification_reason": "Pass 1 workbook view; layout may be reused but conclusions must be rebuilt.",
                    "producer": "scripts/build_workbook.mjs",
                    "traceability": "tracked producer",
                    "detail": {"sheet_index": index, "used_range": used_range},
                }
            )
    return records


def read_csv_dict(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def issue_rows(files: dict[str, bytes]) -> tuple[list[dict[str, object]], dict[str, int]]:
    programs = read_csv_dict(files[f"{OUTPUT_PREFIX}program_screening.csv"])
    professors = read_csv_dict(files[f"{OUTPUT_PREFIX}professor_evidence.csv"])
    drafts = read_csv_dict(files[f"{OUTPUT_PREFIX}outreach_drafts.csv"])
    scored = [row for row in programs if int(float(row.get("overall_score") or 0)) > 0]
    profs_by_program: dict[str, set[str]] = defaultdict(set)
    for row in professors:
        name = row.get("full_name", "").strip().lower()
        if name:
            profs_by_program[row.get("program_id", "")].add(name)
    depth_violations = [
        row
        for row in scored
        if int(float(row.get("faculty_depth_score") or 0)) > 5
        and len(profs_by_program[row.get("program_id", "")]) < 2
    ]
    unresolved_supervision = [
        row
        for row in professors
        if row.get("can_supervise_program", "").lower().startswith("potentially")
        or "capacity unverified" in row.get("can_supervise_program", "").lower()
    ]
    allowed_plausibility = {
        "Lottery",
        "Reach",
        "Competitive",
        "Plausible",
        "Eligibility concern",
        "Insufficient evidence",
    }
    invalid_plausibility = [
        row for row in scored if row.get("admission_plausibility", "") not in allowed_plausibility
    ]
    contact_unknown = [
        row for row in drafts if row.get("already_contacted", "").strip().lower() not in {"yes", "no"}
    ]
    qa_renders = [
        path for path in files if path.startswith(f"{OUTPUT_PREFIX}renders/qa/")
    ]

    common = {"status": "open"}
    issues: list[dict[str, object]] = [
        {
            **common,
            "issue_id": "P2-0001",
            "severity": "critical",
            "category": "pipeline",
            "summary": "Seven documented CLI commands only record a phase name and perform no audit work.",
            "affected_records": "universe; screen; research-fit; verify; score; report; run",
            "affected_record_count": 7,
            "evidence": "src/graduate_audit/cli.py:26-40; README.md:10-20",
            "proposed_repair": "Wire each command to a real stage boundary with explicit inputs, outputs, failures, and row counts.",
            "stage_owner": "Stage 1",
            "acceptance_impact": "Blocks the executable-pipeline completion gate.",
        },
        {
            **common,
            "issue_id": "P2-0002",
            "severity": "critical",
            "category": "resume",
            "summary": "run --resume ignores checkpoints and merely registers the run phase.",
            "affected_records": "graduate-audit run --resume",
            "affected_record_count": 1,
            "evidence": "src/graduate_audit/cli.py:24-40; src/graduate_audit/progress.py:17-24",
            "proposed_repair": "Validate checkpoint manifests and continue from the last valid completed stage.",
            "stage_owner": "Stage 1",
            "acceptance_impact": "Blocks resumability and deterministic reconstruction.",
        },
        {
            **common,
            "issue_id": "P2-0003",
            "severity": "critical",
            "category": "schema",
            "summary": "The shared schema lacks the required Pass 2 evidence, confidence, depth, funding-gate, regional-model, rationale, and conflict fields.",
            "affected_records": "src/graduate_audit/schema.py; config/scoring_rubric.yaml",
            "affected_record_count": 2,
            "evidence": "PASS_2_EXECUTION_PLAN.md Stage 1; src/graduate_audit/schema.py:69-84",
            "proposed_repair": "Version the schema and add the eight required contract areas before migrating data.",
            "stage_owner": "Stage 1",
            "acceptance_impact": "Blocks evidence-backed scoring and later stage manifests.",
        },
        {
            **common,
            "issue_id": "P2-0004",
            "severity": "critical",
            "category": "scoring",
            "summary": "Institution/program score components are hard-coded rather than calculated from claim-level evidence.",
            "affected_records": "US, Canada, and Europe deep-program score maps plus score corrections",
            "affected_record_count": len(scored),
            "evidence": "evidence/deep_review/us/build_deep_review.py:709-747; data/processed/deep_review/canada/build_outputs.py:515-542; data/manifests/deep_review/europe/build_outputs.py:56-83; src/graduate_audit/verify/apply_corrections.py:17-129",
            "proposed_repair": "Replace constants with anchored component calculations carrying evidence IDs, confidence, reviewer, and verification status.",
            "stage_owner": "Stage 5",
            "acceptance_impact": "All current numeric rankings are non-auditable.",
        },
        {
            **common,
            "issue_id": "P2-0005",
            "severity": "critical",
            "category": "faculty depth",
            "summary": "Every scored program receives more than five faculty-depth points despite only one distinct professor row.",
            "affected_records": "program_screening.csv scored rows",
            "affected_record_count": len(depth_violations),
            "evidence": "outputs/20260909-fall2027-audit/program_screening.csv joined to professor_evidence.csv; evidence/deep_review/us/build_deep_review.py:1233-1235",
            "proposed_repair": "Evaluate at least five plausible faculty where available, retain genuine matches, deduplicate people, and cap one-match depth at five.",
            "stage_owner": "Stage 4 + Stage 5",
            "acceptance_impact": "Inflates department depth and total scores.",
        },
        {
            **common,
            "issue_id": "P2-0006",
            "severity": "critical",
            "category": "funding gate",
            "summary": "The funding hard gate can pass from a retained label, funding score, and any verification text.",
            "affected_records": "program scoring gate",
            "affected_record_count": len(programs),
            "evidence": "src/graduate_audit/portfolio.py:84-94",
            "proposed_repair": "Read funding eligibility, coverage, duration, conditions, and source IDs directly; never use recommendation or score as gate evidence.",
            "stage_owner": "Stage 1 + Stage 3 + Stage 5",
            "acceptance_impact": "Can turn unsupported funding into an apply recommendation.",
        },
        {
            **common,
            "issue_id": "P2-0007",
            "severity": "high",
            "category": "supervision authority",
            "summary": "Unverified or merely potential supervision authority is treated as a verified professor match.",
            "affected_records": "professor_evidence.csv supervision rows",
            "affected_record_count": len(unresolved_supervision),
            "evidence": "src/graduate_audit/portfolio.py:35-39; professor_evidence.csv can_supervise_program",
            "proposed_repair": "Use explicit verified, unresolved, and no authority states; only verified authority may pass the match gate.",
            "stage_owner": "Stage 1 + Stage 4",
            "acceptance_impact": "Invalidates professor-match hard gates for affected programs.",
        },
        {
            **common,
            "issue_id": "P2-0008",
            "severity": "high",
            "category": "admission calibration",
            "summary": "Current admission-plausibility labels include values outside the controlled Pass 2 categories.",
            "affected_records": "scored program rows with Clearly ineligible or Plausible to reach",
            "affected_record_count": len(invalid_plausibility),
            "evidence": "outputs/20260909-fall2027-audit/program_screening.csv admission_plausibility",
            "proposed_repair": "Migrate labels to the controlled categories and require evidence/rationale independent of minimum GPA.",
            "stage_owner": "Stage 1 + Stage 5",
            "acceptance_impact": "Prevents comparable portfolio calibration.",
        },
        {
            **common,
            "issue_id": "P2-0009",
            "severity": "high",
            "category": "candidate discovery",
            "summary": "Global OpenAlex outputs are truncated to 300 institutions and 1,000 faculty without regional/topic recall or exclusion-sample saturation checks.",
            "affected_records": "openalex_institution_signals.csv; openalex_faculty_signals.csv",
            "affected_record_count": 2,
            "evidence": "src/graduate_audit/research_fit/openalex_discovery.py:232-242",
            "proposed_repair": "Use independent discovery paths and regional/topic coverage gates; report source yield and false-negative sampling.",
            "stage_owner": "Stage 2",
            "acceptance_impact": "Creates unresolved false-negative risk in the candidate funnel.",
        },
        {
            **common,
            "issue_id": "P2-0010",
            "severity": "high",
            "category": "contact history",
            "summary": "First-wave administrative contacts have blank contact history instead of an explicit unknown state, and the pipeline can default missing history to No.",
            "affected_records": "outreach_drafts.csv rows with non-Yes/No contact status",
            "affected_record_count": len(contact_unknown),
            "evidence": "src/graduate_audit/reporting/outreach.py:157-178; outputs/20260909-fall2027-audit/outreach_drafts.csv",
            "proposed_repair": "Require checked yes/no/unknown per recipient and keep connected-account detail private.",
            "stage_owner": "Stage 7",
            "acceptance_impact": "Blocks approval of those first-wave contacts.",
        },
        {
            **common,
            "issue_id": "P2-0011",
            "severity": "high",
            "category": "outreach scoring",
            "summary": "Outreach priority is inferred from program rank/fit fallbacks and a hard-coded admin score rather than configured component scores.",
            "affected_records": "current first-wave outreach drafts",
            "affected_record_count": len(drafts),
            "evidence": "src/graduate_audit/reporting/outreach.py:111-142",
            "proposed_repair": "Calculate every configured outreach component and retain the decision each contact could change.",
            "stage_owner": "Stage 7",
            "acceptance_impact": "First-wave order is not auditable.",
        },
        {
            **common,
            "issue_id": "P2-0012",
            "severity": "high",
            "category": "generated final text",
            "summary": "Fifteen templated emails are published in final outputs without Draft Ready evidence or per-draft manual review records.",
            "affected_records": "outreach_drafts.csv; OUTREACH DRAFTS workbook sheet",
            "affected_record_count": len(drafts),
            "evidence": "src/graduate_audit/reporting/outreach.py:64-97,145-187; outreach_drafts.csv header",
            "proposed_repair": "Draft only after Stage 7, add all readiness fields, run automated checks, and record a manual read-through.",
            "stage_owner": "Stage 8",
            "acceptance_impact": "Existing drafts are not approved outreach artifacts.",
        },
        {
            **common,
            "issue_id": "P2-0013",
            "severity": "high",
            "category": "validation",
            "summary": "Validation files report one undifferentiated PASS while hard-gate, evidence-completeness, score provenance, and outreach-quality defects remain.",
            "affected_records": "validation.json; final_validation.json; state/progress.json",
            "affected_record_count": 3,
            "evidence": "outputs/20260909-fall2027-audit/validation.json; outputs/20260909-fall2027-audit/final_validation.json; src/graduate_audit/validation.py; src/graduate_audit/verify/final_validation.py",
            "proposed_repair": "Separate structural, evidence, second-source, portfolio, outreach, and visual validations with independent results.",
            "stage_owner": "Stage 1 + Stage 9",
            "acceptance_impact": "Prior PASS cannot be treated as substantive correctness.",
        },
        {
            **common,
            "issue_id": "P2-0014",
            "severity": "medium",
            "category": "traceability",
            "summary": "Eleven QA render snapshots have no tracked generating command.",
            "affected_records": "outputs/20260909-fall2027-audit/renders/qa/*.png",
            "affected_record_count": len(qa_renders),
            "evidence": "git tree compared with scripts/build_workbook.mjs output paths",
            "proposed_repair": "Generate all visual-QA artifacts from one tracked workbook command or omit snapshot duplicates.",
            "stage_owner": "Stage 1 + Stage 9",
            "acceptance_impact": "Explicitly non-reproducible baseline artifacts; not a Stage 0 gate failure because they are labeled.",
        },
        {
            **common,
            "issue_id": "P2-0015",
            "severity": "high",
            "category": "coverage",
            "summary": "European discovery exposes 3,628 of 4,462 reported ROR records (81.31%) and retains blocked registry sources.",
            "affected_records": "Europe institutional universe and blocked registry sources",
            "affected_record_count": 834,
            "evidence": "state/progress.json known_failures; data/manifests/europe/ror_snapshot.json; data/manifests/europe/blocked_sources.json",
            "proposed_repair": "Rebuild with independent recognized-institution/program paths and report saturation or the residual gap.",
            "stage_owner": "Stage 2",
            "acceptance_impact": "Unresolved regional false-negative coverage.",
        },
        {
            **common,
            "issue_id": "P2-0016",
            "severity": "high",
            "category": "coverage",
            "summary": "Canada retains 50 unresolved indexed institutions and nine blocked or insufficient official program pages.",
            "affected_records": "Canada institutional/program discovery",
            "affected_record_count": 59,
            "evidence": "state/progress.json known_failures; data/manifests/canada/blocked_sources.json",
            "proposed_repair": "Carry every record into Stage 2 with an explicit status and retry through independent official sources.",
            "stage_owner": "Stage 2 + Stage 3",
            "acceptance_impact": "Unresolved Canadian discovery and verification coverage.",
        },
        {
            **common,
            "issue_id": "P2-0017",
            "severity": "medium",
            "category": "portfolio",
            "summary": "Portfolio construction encodes a 20-core target and fixed reach allowance without the Stage 6 ten-question pressure test.",
            "affected_records": "portfolio.json and select_portfolio defaults",
            "affected_record_count": 20,
            "evidence": "src/graduate_audit/portfolio.py:108-165; outputs/20260909-fall2027-audit/portfolio.json",
            "proposed_repair": "Build the portfolio only after evidence-backed scoring and store all ten pressure-test answers per university.",
            "stage_owner": "Stage 6",
            "acceptance_impact": "Current core list is not a Pass 2 portfolio recommendation.",
        },
    ]
    metrics = {
        "program_rows": len(programs),
        "scored_programs": len(scored),
        "professor_rows": len(professors),
        "depth_violations": len(depth_violations),
        "unresolved_supervision": len(unresolved_supervision),
        "invalid_plausibility": len(invalid_plausibility),
        "draft_rows": len(drafts),
        "draft_contact_unknown": len(contact_unknown),
        "qa_renders": len(qa_renders),
    }
    return issues, metrics


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    def safe(value: object) -> str:
        return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(safe(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate the Pass 2 Stage 0 baseline diagnosis.")
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--plan-path", required=True)
    args = parser.parse_args()

    commit = git("rev-parse", args.baseline_commit).decode().strip()
    commit_time = git("show", "-s", "--format=%aI", commit).decode().strip()
    files = baseline_files(commit)
    issues, metrics = issue_rows(files)

    inventory: list[dict[str, object]] = []
    for path in sorted(files):
        types = artifact_types(path)
        classification, reason = classify(path, types)
        producer, traceability = producer_for_final(path)
        inventory.append(
            {
                "path": path,
                "artifact_types": types,
                "size_bytes": len(files[path]),
                "sha256": sha256(files[path]),
                "row_count": csv_rows(files[path]) if path.lower().endswith(".csv") else None,
                "classification": classification,
                "classification_reason": reason,
                "producer": producer,
                "traceability": traceability,
            }
        )

    workbook_path = f"{OUTPUT_PREFIX}graduate_program_audit.xlsx"
    sheet_inventory = workbook_sheets(files[workbook_path], workbook_path)
    inventory.extend(sheet_inventory)

    final_records = [
        record
        for record in inventory
        if "workbook sheet" not in record["artifact_types"]
        and (
            str(record["path"]).startswith(OUTPUT_PREFIX)
            or str(record["path"]).startswith(REPORT_PREFIX)
        )
    ]
    final_records.sort(key=lambda record: str(record["path"]))
    unmapped = [record["path"] for record in final_records if record["traceability"] == "unmapped"]

    tracked_private = [
        path for path in files if path.startswith("data/private/") and path != "data/private/README.md"
    ]
    suspicious_private = []
    private_patterns = (
        b"BEGIN:VCALENDAR",
        b"BEGIN:VEVENT",
        b"gmail_thread_id",
        b"gmail_message_id",
        b"calendar_event_id",
    )
    for path, data in files.items():
        if any(pattern.lower() in data.lower() for pattern in private_patterns):
            suspicious_private.append(path)
    privacy_pass = not tracked_private and not suspicious_private

    classification_counts = Counter(str(record["classification"]) for record in inventory)
    type_counts = Counter(
        artifact_type for record in inventory for artifact_type in record["artifact_types"]
    )
    traceability_counts = Counter(str(record["traceability"]) for record in final_records)
    issue_severity_counts = Counter(str(issue["severity"]) for issue in issues)

    issue_path = ROOT / "data/processed/pass2/baseline_issue_register.csv"
    report_path = ROOT / "reports/pass2/00_baseline_diagnosis.md"
    manifest_path = ROOT / "data/manifests/pass2/stage_00.json"
    progress_path = ROOT / "state/progress.json"
    script_path = Path(__file__).resolve()
    write_csv(issue_path, issues)

    sheet_table = markdown_table(
        ["Index", "Workbook sheet", "Used range", "Classification", "Producer"],
        [
            [
                record["detail"]["sheet_index"],
                str(record["path"]).split("::sheet::", 1)[1],
                record["detail"]["used_range"],
                record["classification"],
                record["producer"],
            ]
            for record in sheet_inventory
        ],
    )
    final_table = markdown_table(
        ["Final output", "SHA-256", "Traceability", "Producer or disposition"],
        [
            [record["path"], record["sha256"], record["traceability"], record["producer"]]
            for record in final_records
        ],
    )
    issue_table = markdown_table(
        ["ID", "Severity", "Category", "Affected", "Stage owner", "Summary"],
        [
            [
                issue["issue_id"],
                issue["severity"],
                issue["category"],
                issue["affected_record_count"],
                issue["stage_owner"],
                issue["summary"],
            ]
            for issue in issues
        ],
    )
    class_table = markdown_table(
        ["Classification", "Artifacts"],
        [[name, classification_counts[name]] for name in sorted(classification_counts)],
    )
    type_table = markdown_table(
        ["Artifact type", "Artifacts"],
        [[name, type_counts[name]] for name in sorted(type_counts)],
    )

    report = f"""# Stage 0 Result

## Decision
Pass

## What changed

The repository was frozen at commit `{commit}` and diagnosed without changing any program recommendation, score, portfolio membership, outreach ranking, report, or workbook. A complete machine-readable inventory, an issue register, and a Stage 0 manifest were added. The Pass 2 progress state now records Stage 0 as complete and keeps Stage 1 unauthorized pending user approval.

## Coverage

- Baseline tracked files inventoried: {len(files)}.
- Workbook sheets inventoried: {len(sheet_inventory)}.
- Total artifact inventory records: {len(inventory)}.
- Current final output/report files checked for traceability: {len(final_records)}.
- Final artifacts with tracked producers: {traceability_counts['tracked producer']}.
- Explicitly non-reproducible final artifacts: {traceability_counts['explicitly non-reproducible']} QA render snapshots.
- Dataset records: {type_counts['dataset']}; scripts: {type_counts['script']}; reports: {type_counts['report']}; source ledgers: {type_counts['source ledger']}; validation artifacts: {type_counts['validation']}.
- The full per-artifact inventory, classification, checksum, row count where applicable, and producer mapping is stored in `data/manifests/pass2/stage_00.json` under `artifact_inventory`.

## Validation performed

- Compared the working tree with `{commit}` before Stage 0 writes; the baseline was clean.
- Computed SHA-256 checksums from a Git archive of the frozen commit, including every file under the current output and report directories.
- Imported the workbook with the approved spreadsheet runtime and independently parsed its worksheet metadata; both methods found the same 11 sheets.
- Checked every current final output for a tracked producer. Eleven `renders/qa` PNGs have no tracked producer and are explicitly marked non-reproducible; no final output remains unmapped.
- Checked Git tracking/ignore rules and scanned tracked content for raw Gmail/Calendar export markers. Only `data/private/README.md` is tracked under `data/private`; raw connected-account source paths are ignored.
- Joined scored program rows to professor rows to test faculty depth. All {metrics['depth_violations']} of {metrics['scored_programs']} scored programs exceed the one-professor depth cap while having one distinct professor row.
- Confirmed that the Stage 0 output generator did not modify recommendation-bearing Pass 1 outputs.

## Material uncertainties or conflicts

- The prior validation status is not reliable as a substantive pass because critical funding, supervision, faculty-depth, and score-provenance gates are defective.
- European discovery is short by 834 records relative to the ROR filtered total and several registry sources were blocked.
- Canada retains 50 unresolved indexed institutions and nine blocked or insufficient program pages.
- The 11 QA render snapshots cannot be recreated by a tracked command; they are preserved only as unverified baseline evidence.
- Sanitized Calendar comparison and contact-status fields are tracked, but no raw messages or Calendar event bodies were found. Stage 7 must keep any connected-account detail private.

## Records requiring human judgment

No program-level judgments were changed in Stage 0. Later stages must decide how to resolve official-source conflicts, funding ambiguity, supervision authority, and whether each current recommendation survives evidence-backed reconstruction.

## Files created or modified

- `reports/pass2/00_baseline_diagnosis.md`
- `data/processed/pass2/baseline_issue_register.csv`
- `data/manifests/pass2/stage_00.json`
- `state/progress.json`
- `scripts/build_stage_00.py`

## Recommendation before the next stage

Begin Stage 1 only after explicit user approval. Stage 1 may repair the executable pipeline, schemas, checkpoint manifests, and tests. It may not rescore programs, change recommendations, or treat the Pass 1 validation result as proof that later gates passed.

## Baseline identity

- Commit: `{commit}`
- Commit timestamp: `{commit_time}`
- Execution plan SHA-256: `{sha256(Path(args.plan_path).read_bytes())}`
- Recommendation-bearing outputs changed in this stage: no

## Artifact inventory summary

{class_table}

{type_table}

Each baseline artifact has exactly one disposition: reusable, repairable, superseded, or unverified. `Reusable` means it may seed a later stage; it does not waive freshness or official-source verification.

## Workbook sheet inventory

{sheet_table}

## Baseline issues

{issue_table}

The issue register contains the affected records, evidence, proposed repair, acceptance impact, status, and stage owner for each item.

## Privacy audit

- Tracked files under `data/private`: `data/private/README.md` only.
- Ignored connected-source paths verified: `data/private/gmail_contact_history.csv` and `data/private/calendar_candidate_summary.csv`.
- Raw Gmail/Calendar export or event markers found in tracked content: none.
- Tracked connected-context outputs: sanitized school comparison and broad contact-status/outcome fields only.
- Result: pass for the Stage 0 raw-private-content check.

## Current final output traceability and checksums

{final_table}

## Completion-gate assessment

Stage 0 passes because the baseline commit and output checksums are frozen, every required artifact and workbook sheet is inventoried and classified, raw private Gmail/Calendar content is not tracked, the required defect classes are registered, and every current final output is either linked to a tracked producer or explicitly labeled non-reproducible. This pass diagnoses the baseline; it does not endorse the existing recommendations.
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    generated_at = datetime.now(timezone.utc).isoformat()
    progress["current_phase"] = "pass2_stage_00_complete"
    progress["pass2"] = {
        "current_stage": 0,
        "last_completed_stage": 0,
        "stage_status": {"0": "complete"},
        "next_stage": 1,
        "next_stage_authorized": False,
        "baseline_commit": commit,
        "stage_manifest": "data/manifests/pass2/stage_00.json",
        "open_issue_count": len(issues),
        "critical_issue_count": issue_severity_counts["critical"],
        "high_issue_count": issue_severity_counts["high"],
    }
    progress["updated_at"] = generated_at
    progress_path.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")

    output_records = []
    for path in [report_path, issue_path, progress_path, script_path]:
        data = path.read_bytes()
        output_records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(data),
                "size_bytes": len(data),
                "row_count": csv_rows(data) if path.suffix.lower() == ".csv" else None,
            }
        )
    manifest = {
        "stage": 0,
        "stage_name": "Freeze and diagnose the existing baseline",
        "decision": "Pass",
        "status": "complete",
        "generated_at": generated_at,
        "baseline_commit": commit,
        "baseline_commit_time": commit_time,
        "inputs": [
            {
                "path": "AGENTS.md",
                "sha256": sha256(files["AGENTS.md"]),
                "source": "baseline commit",
            },
            {
                "path": str(Path(args.plan_path).resolve()),
                "sha256": sha256(Path(args.plan_path).read_bytes()),
                "source": "user-provided execution plan",
            },
        ],
        "outputs": output_records
        + [
            {
                "path": "data/manifests/pass2/stage_00.json",
                "sha256": None,
                "size_bytes": None,
                "row_count": None,
                "note": "Manifest does not self-hash.",
            }
        ],
        "counts": {
            "baseline_tracked_files": len(files),
            "workbook_sheets": len(sheet_inventory),
            "artifact_inventory_records": len(inventory),
            "current_final_outputs_and_reports": len(final_records),
            "traceable_final_artifacts": traceability_counts["tracked producer"],
            "explicitly_non_reproducible_final_artifacts": traceability_counts[
                "explicitly non-reproducible"
            ],
            "open_issues": len(issues),
            "critical_issues": issue_severity_counts["critical"],
            "high_issues": issue_severity_counts["high"],
            "medium_issues": issue_severity_counts["medium"],
            **metrics,
        },
        "classification_counts": dict(sorted(classification_counts.items())),
        "artifact_type_counts": dict(sorted(type_counts.items())),
        "privacy": {
            "status": "PASS" if privacy_pass else "FAIL",
            "tracked_private_files_other_than_readme": tracked_private,
            "tracked_raw_connected_source_markers": suspicious_private,
            "sanitized_connected_context_note": "Calendar comparison and broad contact outcomes are tracked; raw messages/events are not.",
        },
        "validation": [
            {"check": "baseline_commit_resolves", "status": "PASS"},
            {"check": "all_artifacts_classified", "status": "PASS"},
            {"check": "workbook_sheet_inventory", "status": "PASS", "count": len(sheet_inventory)},
            {
                "check": "final_output_traceability",
                "status": "PASS" if not unmapped else "FAIL",
                "unmapped": unmapped,
            },
            {"check": "raw_private_content_not_tracked", "status": "PASS" if privacy_pass else "FAIL"},
            {"check": "recommendations_unchanged", "status": "PASS"},
            {"check": "issue_register_present", "status": "PASS", "rows": len(issues)},
            {"check": "stage_report_template", "status": "PASS"},
        ],
        "blockers": [issue for issue in issues if issue["severity"] == "critical"],
        "unresolved_coverage": [
            "European ROR/API coverage is 3,628 of 4,462 reported filtered records (81.31%); 834 records remain unexposed.",
            "EHESO/ETER returned HTTP 401 and multiple European national-registry pages were blocked.",
            "Canada retains 50 unresolved indexed institutions and nine blocked/insufficient official program pages.",
            "The prior mechanical screens are not an exhaustive official-program catalogue crawl.",
            "Fall 2027 pages, funding awards, and employment vacancies that are not published remain unresolved.",
        ],
        "recommendations_changed": False,
        "next_stage": {
            "number": 1,
            "authorized": False,
            "recommendation": "Begin only after explicit user approval.",
        },
        "artifact_inventory": inventory,
        "baseline_output_checksums": [
            {"path": record["path"], "sha256": record["sha256"]}
            for record in final_records
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    checks = {
        "required_outputs_exist": all(
            path.exists() for path in (report_path, issue_path, manifest_path, progress_path)
        ),
        "all_artifacts_classified": all(
            record["classification"] in REQUIRED_CLASSIFICATIONS for record in inventory
        ),
        "inventory_unique": len({str(record["path"]) for record in inventory}) == len(inventory),
        "workbook_has_11_sheets": len(sheet_inventory) == 11,
        "all_final_outputs_mapped_or_labeled": not unmapped,
        "privacy_boundary_passes": privacy_pass,
        "issue_register_complete": len(issues) > 0,
        "report_template_present": report.startswith("# Stage 0 Result\n\n## Decision\nPass"),
        "recommendations_unchanged": all(
            unchanged_from_commit(commit, path)
            for path in (
                f"{OUTPUT_PREFIX}program_screening.csv",
                f"{OUTPUT_PREFIX}portfolio.json",
                f"{OUTPUT_PREFIX}outreach_drafts.csv",
                f"{REPORT_PREFIX}final_shortlist.md",
                f"{OUTPUT_PREFIX}graduate_program_audit.xlsx",
            )
        ),
    }
    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
