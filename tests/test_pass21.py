from __future__ import annotations

import csv
import json
from pathlib import Path
import zipfile

import pytest

from graduate_audit.pass21 import classify_funding_claim, validate_recommended


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "20260911-pass21-final"


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUTPUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def test_final_ranking_is_a_valid_program_first_portfolio() -> None:
    rows = read_csv("final_ranking.csv")
    validation = validate_recommended(rows)

    assert validation["passed"], validation["errors"]
    assert validation["recommended_count"] == 15
    assert validation["tier_counts"] == {
        "Strongest Realistic Options": 5,
        "Competitive Options": 6,
        "High Reaches": 3,
        "Extreme Reaches": 1,
    }
    assert all(row["Degree Type"] in {
        "PhD",
        "Direct-entry PhD",
        "Integrated or structured doctorate",
        "PhD requiring a master's",
        "Thesis or research master's",
        "Project-based master's with substantial research",
    } for row in rows)
    assert all(row["International Funding Eligible"] == "Yes" for row in rows)
    assert all(row["Academic Eligibility Verified"] == "Yes" for row in rows)
    assert all(row["Recommended Decision"].startswith("Apply") for row in rows)


def test_funding_repair_is_explicit_and_complete() -> None:
    rows = read_csv("funding_contradiction_audit.csv")

    assert len(rows) == 46
    assert sum(row["Contradiction Direction"] == "Stage 3 pass → Stage 5 fail" for row in rows) == 44
    assert sum(row["Contradiction Direction"] == "Stage 3 inquiry → Stage 5 pass" for row in rows) == 2
    assert sum(row["Pass 2.1 Funding Decision"] == "Pass" for row in rows) == 17
    assert sum(row["Pass 2.1 Funding Decision"] == "Conditional" for row in rows) == 29
    assert all(row["Exact Reviewed Claim"].strip() for row in rows)
    assert all(row["Official Funding URL"].startswith("http") for row in rows)
    assert all(row["Verification Status"] == "Manual claim-level review; no keyword classification" for row in rows)


def test_funding_classifier_uses_the_reviewed_decision_not_keywords() -> None:
    claim = "Funding is guaranteed and covers tuition and a stipend."

    assert classify_funding_claim(
        reviewed_decision="Conditional",
        source_url="https://example.edu/funding",
        claim=claim,
    ) == "Conditional"
    with pytest.raises(ValueError):
        classify_funding_claim(
            reviewed_decision="guaranteed",
            source_url="https://example.edu/funding",
            claim=claim,
        )


def test_conditional_programs_are_separate_and_decision_changing() -> None:
    ranking = {(row["University"], row["Exact Program"]) for row in read_csv("final_ranking.csv")}
    questions = read_csv("open_questions.csv")

    assert len(questions) == 8
    assert all((row["University"], row["Program"]) not in ranking for row in questions)
    assert all(row["Question"].strip() and row["Why the Answer Matters"].strip() for row in questions)
    assert all(row["Current Decision Without Reply"].startswith("Do not") for row in questions)


def test_uiuc_and_uic_admission_repairs_are_preserved() -> None:
    exclusions = read_csv("exclusions.csv")
    uiuc = next(row for row in exclusions if row["University"] == "University of Illinois Urbana-Champaign")
    uic = next(row for row in exclusions if row["University"] == "University of Illinois Chicago")

    assert uiuc["Revised Status"] == "Do Not Apply"
    assert "3.40" in uiuc["Primary Exclusion Reason"]
    assert "rare-exception" in uiuc["Primary Exclusion Reason"]
    assert uic["Revised Status"] == "Conditional"
    assert "final-60" in uic["Reconsideration Condition"].casefold()
    assert "3.50" in uic["Reconsideration Condition"]


def test_exclusion_audit_reopen_and_unresolved_rows_are_retained() -> None:
    exclusions = read_csv("exclusions.csv")
    institution_audits = [
        row for row in exclusions
        if row["Program"] == "Institution-level exclusion audit; no exact recommended program"
    ]

    assert len(institution_audits) == 17
    assert all(row["Revised Status"] == "Do Not Apply" for row in institution_audits)
    assert all(row["Evidence URL"].startswith("http") for row in institution_audits)


def test_fee_math_and_change_counts_match_generated_validation() -> None:
    ranking = read_csv("final_ranking.csv")
    validation = json.loads((OUTPUT / "validation.json").read_text(encoding="utf-8"))

    assert sum(int(row["Application Fee"]) for row in ranking) == 1105
    assert validation["fee_total_before_confirmed_waivers_usd"] == 1105
    assert validation["fee_total_after_confirmed_waivers_usd"] == 1010
    assert validation["fully_funded_program_count"] == 14
    assert validation["previous_selections_removed"] == 15
    assert validation["previously_excluded_restored"] == 8


def test_workbook_source_data_has_exactly_four_requested_tabs_and_no_outreach_tracking() -> None:
    data = json.loads((ROOT / "data" / "processed" / "pass21" / "workbook_data.json").read_text(encoding="utf-8"))

    assert set(data) == {"final_ranking", "evidence", "exclusions", "open_questions"}
    headers = {key: set(rows[0]) for key, rows in data.items()}
    forbidden = {"Professor Outreach", "Recruiting Status", "Outreach Draft", "Contacted"}
    assert all(not (columns & forbidden) for columns in headers.values())


def test_exported_workbook_is_a_four_sheet_openxml_package() -> None:
    workbook = OUTPUT / "graduate_program_audit_pass21_20260911.xlsx"

    assert workbook.stat().st_size > 10_000
    with zipfile.ZipFile(workbook) as archive:
        names = set(archive.namelist())
        workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
        assert {f"xl/worksheets/sheet{index}.xml" for index in range(1, 5)} <= names
        assert {f"xl/tables/table{index}.xml" for index in range(1, 5)} <= names
        for sheet_name in ("FINAL RANKING", "FUNDING AND ADMISSIONS EVIDENCE", "EXCLUSIONS", "OPEN QUESTIONS"):
            assert sheet_name in workbook_xml


def test_evidence_urls_and_workbook_qa_are_complete() -> None:
    evidence = read_csv("funding_and_admissions_evidence.csv")
    exclusions = read_csv("exclusions.csv")
    qa = json.loads((OUTPUT / "workbook_qa.json").read_text(encoding="utf-8"))

    assert len(evidence) == 23
    assert all(row["Source URL"].startswith("http") for row in evidence)
    assert all(row["Official Program URL"].startswith("http") for row in evidence)
    assert all(row["Official Funding URL"].startswith("http") for row in evidence)
    assert all(row["Evidence URL"].startswith("http") for row in exclusions)
    assert qa["sheet_count"] == 4
    assert qa["expected_rows"] == {
        "FINAL RANKING": 15,
        "FUNDING AND ADMISSIONS EVIDENCE": 23,
        "EXCLUSIONS": 168,
        "OPEN QUESTIONS": 8,
    }
    assert "matched 0 entries" in qa["formula_error_scan"]
    assert qa["visual_review_status"] == "passed"
    assert qa["visually_reviewed_sheet_count"] == 4
