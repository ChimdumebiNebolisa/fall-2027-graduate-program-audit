from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from graduate_audit.io import read_csv


def _table(headers: list[str], rows: list[list[object]]) -> str:
    if not rows:
        return "_No rows met this category._"
    head = "| " + " | ".join(headers) + " |"
    rule = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(value or "").replace("|", "\\|") for value in row) + " |" for row in rows]
    return "\n".join([head, rule, *body])


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def build_reports(output_dir: str | Path, reports_dir: str | Path) -> None:
    output_root = Path(output_dir)
    report_root = Path(reports_dir)
    report_root.mkdir(parents=True, exist_ok=True)

    institutions = read_csv(output_root / "institution_universe.csv")
    programs = read_csv(output_root / "program_screening.csv")
    professors = read_csv(output_root / "professor_evidence.csv")
    exclusions = read_csv(output_root / "exclusion_log.csv")
    sources = read_csv(output_root / "source_ledger.csv")
    calendar = read_csv(output_root / "calendar_comparison.csv") if (output_root / "calendar_comparison.csv").exists() else []
    portfolio = _load_json(output_root / "portfolio.json")
    manifest = _load_json(output_root / "run_manifest.json")
    validation = _load_json(output_root / "validation.json")

    region_counts = Counter(row.get("region", "Unspecified") for row in institutions)
    status_counts = Counter(row.get("screening_status", "") for row in institutions)
    exclusion_counts = Counter(row.get("primary_exclusion_reason", "") for row in exclusions)
    reviewed = [row for row in programs if row.get("verification_status", "").lower() not in {"", "mechanical", "preliminary"}]
    retained = [row for row in programs if row.get("screening_decision", "").lower() == "retained"]
    recommended_professors = [
        row for row in professors if row.get("outreach_priority", "").lower() in {"first wave", "first-wave", "high"}
    ]

    coverage = f"""# Coverage Report — Fall 2027 Graduate Program Audit

Evidence date: {manifest.get('current_date', 'not recorded')}  
Validation: {validation.get('status', 'not yet run')}

## Coverage funnel

{_table(['Measure', 'Count'], [
    ['Institutions indexed', len(institutions)],
    ['Programs mechanically screened', len(programs)],
    ['Programs deeply reviewed', len(reviewed)],
    ['Programs retained', len(retained)],
    ['Professors evaluated', len(professors)],
    ['First-wave professors', len(recommended_professors)],
    ['Source claims', len(sources)],
])}

## Institutions by region

{_table(['Region', 'Institutions'], [[key, value] for key, value in sorted(region_counts.items())])}

## Final institution statuses

{_table(['Status', 'Count'], [[key, value] for key, value in status_counts.most_common()])}

## Leading exclusion reasons

{_table(['Reason', 'Count'], [[key, value] for key, value in exclusion_counts.most_common(20)])}

## Coverage limitations

- U.S. discovery uses official IPEDS degree and completion records; CIP completions are lagging positive signals and do not prove current research fit.
- Canada uses the IRCC DLI list, CICIC, ROR cross-references, and bounded official-program checks. Unresolved indexed providers are not silently treated as negatives.
- Europe/UK coverage uses the ROR education-organization universe plus national-registry checks and bounded program seeds. ROR is not an accreditation registry, and its API paging did not expose every reported record; the manifest preserves the exact coverage ratio.
- Official pages that blocked access, contradicted another official source, or did not publish Fall 2027 data remain explicitly unresolved.
- “Programs screened” includes mechanical field-signal rows. Only “deeply reviewed” rows received faculty, funding, eligibility, and deadline analysis.

The search is broad and auditable within the frozen source universes, but it is not claimed to be an exhaustive crawl of every official graduate catalogue.
"""
    (report_root / "coverage_report.md").write_text(coverage, encoding="utf-8")

    def portfolio_rows(kind: str) -> list[list[object]]:
        return [
            [r.get("institution_name"), r.get("program_name"), r.get("overall_score"), r.get("admission_plausibility"), r.get("recommendation"), r.get("biggest_risk")]
            for r in portfolio.get(kind, [])
        ]

    shortlist = f"""# Final Shortlist — Fall 2027

The portfolio applies eligibility and funding gates before score ranking. Scores are comparative evidence summaries, not admission probabilities.

## Recommended core

{_table(['University', 'Program', 'Score', 'Plausibility', 'Recommendation', 'Biggest risk'], portfolio_rows('core'))}

## Reserve

{_table(['University', 'Program', 'Score', 'Plausibility', 'Recommendation', 'Biggest risk'], portfolio_rows('reserve'))}

## Monitor for 2027 positions

{_table(['University', 'Program', 'Score', 'Plausibility', 'Recommendation', 'Biggest risk'], portfolio_rows('monitor_for_2027_position'))}

## Calendar comparison

{_table(['Previous candidate', 'Previous category', 'New outcome', 'Reason'], [[r.get('existing_calendar_school'), r.get('previous_category'), r.get('new_status'), r.get('reason')] for r in calendar])}

## Decision rule

Submit core applications only after the unresolved question in each program row is either answered or judged non-material. Reserve programs are substitutes, not automatic additions. Position-based European routes remain monitoring items until a funded opening is actually advertised.
"""
    (report_root / "final_shortlist.md").write_text(shortlist, encoding="utf-8")

    methodology = """# Methodology

## Scope and universe

The audit covers the United States, Canada, the EU-27, Ireland, the United Kingdom, Norway, Switzerland, and Iceland. U.S. records use IPEDS UnitID; Canadian records use DLI numbers with CICIC/ROR cross-references; European records use ROR IDs and national-registry checks where available.

## Screening sequence

1. Freeze official registry datasets and checksums.
2. Normalize institutions and assign every indexed record a status.
3. Use official field/program signals for mechanical screening.
4. Use 2022–present scholarly discovery to find research-fit candidates.
5. Verify programs, faculty appointments, supervision, funding, eligibility, deadlines, fees, and contact norms on official pages.
6. Apply hard gates, score survivors, pressure-test the portfolio, and independently recheck finalists and an exclusion sample.

## Score and hard gates

The 100-point score is professor alignment 30, department depth 15, funding/net viability 25, eligibility/plausibility 15, degree/admissions alignment 10, and application economics 5. A recognized active institution, relevant research program, international eligibility, bachelor's-entry or suitable research-master's route, verified supervisor match, credible funding/full scholarship, and compatible degree structure are hard gates. Prestige and rankings are not inputs.

## Evidence rules

The hierarchy is government/recognized registries; official graduate, department, funding, fee, and handbook pages; official faculty/lab pages; recent papers/projects; and scholarly indexes for discovery. Search snippets are never final evidence. Recruiting is “confirmed” only with a current explicit statement or opening. Silence is recorded as unknown, not as a negative. Older deadlines retain their actual cycle label, and no unpublished Fall 2027 date is inferred.

## Funding definitions

“Normally funded” requires credible program-level evidence of tuition support and stipend/salary, not merely the existence of assistantships. Canadian research-master's support is distinguished as guaranteed, competitive, or supervisor-dependent. UK/European awards must cover the international rate to be financially viable. Employment-based European PhDs are monitored until a specific opening exists.

## Admissions-plausibility limits

Plausibility categories are qualitative assessments against published requirements and the supplied applicant record. They are not probabilities and do not use rankings or anecdotal admissions profiles.

## Privacy and non-mutation

Calendar and Gmail checks are bounded to graduate-school context. No Calendar event was changed. No Gmail draft was created and no email was sent. Only broad prior-contact outcomes are retained in final outputs.
"""
    (report_root / "methodology.md").write_text(methodology, encoding="utf-8")

    risks = Counter(row.get("biggest_risk", "Unspecified") for row in retained)
    countries = Counter(row.get("country", "") for row in retained)
    strategic = f"""# Strategic Findings

## Portfolio shape

{_table(['Country', 'Retained programs'], [[key, value] for key, value in countries.most_common()])}

The portfolio deliberately favors funded PhDs and research master's routes with identifiable supervisors. It does not preserve a university merely because it was previously considered.

## Recurrent risks

{_table(['Risk', 'Programs'], [[key, value] for key, value in risks.most_common(15)])}

## Interpretation

- The strongest signal is the intersection of sustained faculty work in software engineering/program analysis and a department with more than one plausible supervisor.
- A single exceptional match can remain viable, but it carries an explicit single-professor dependency warning.
- Funding uncertainty, especially for research master's and international-fee differentials, is a gating question rather than a small score penalty.
- European faculty fit alone is not an application route. Master's-required doctorates are future routes, and employment doctorates remain monitors until a funded vacancy exists.
- Application effort should first resolve the small number of questions that can flip a program from viable to non-viable: supervisor capacity, funding coverage, and degree-entry eligibility.
"""
    (report_root / "strategic_findings.md").write_text(strategic, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--reports-dir", required=True)
    args = parser.parse_args()
    build_reports(args.output_dir, args.reports_dir)


if __name__ == "__main__":
    main()
