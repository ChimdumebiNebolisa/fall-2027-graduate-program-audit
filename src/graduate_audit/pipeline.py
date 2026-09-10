from __future__ import annotations

import hashlib
import json
import os
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .hard_gates import VERIFIED_FUNDING_VALUES, evaluate_hard_gates
from .io import read_csv, read_json, write_csv, write_json
from .portfolio import select_portfolio
from .schema import (
    INSTITUTION_COLUMNS_V2,
    OUTREACH_PRIORITY_COLUMNS_V2,
    PASS2_SCHEMA_VERSION,
    PROFESSOR_COLUMNS_V2,
    PROGRAM_COLUMNS_V2,
    SCORE_COMPONENT_COLUMNS_V2,
    SOURCE_COLUMNS_V2,
)
from .scoring import calculate_score

PIPELINE_STAGES = (
    "discovery",
    "screening",
    "research_fit",
    "verification",
    "scoring",
    "portfolio",
    "outreach",
    "reporting",
)

COMPONENTS = {
    "professor_alignment": ("professor_fit_score", 30),
    "department_program_depth": ("faculty_depth_score", 15),
    "funding_net_viability": ("funding_score", 25),
    "eligibility_credential_plausibility": ("eligibility_score", 15),
    "degree_admissions_alignment": ("degree_admissions_score", 10),
    "application_economics": ("application_economics_score", 5),
}

TRUE_VALUES = {True, 1, "1", "true", "yes", "verified", "eligible"}
CONFIDENCE_ORDER = {"low": 1, "medium": 2, "high": 3}


class PipelineError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _truthy(value: object) -> bool:
    return value if isinstance(value, bool) else str(value or "").strip().lower() in TRUE_VALUES


def _number(value: object) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError) as error:
        raise PipelineError(f"expected a numeric score, received {value!r}") from error


def _split_refs(value: object) -> list[str]:
    normalized = str(value or "").replace(";", "|")
    return [item.strip() for item in normalized.split("|") if item.strip()]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _row_count(path: Path) -> int | None:
    if path.suffix.lower() == ".csv":
        return len(read_csv(path))
    if path.suffix.lower() == ".json":
        payload = read_json(path)
        if isinstance(payload, list):
            return len(payload)
        if isinstance(payload, dict):
            lists = [value for value in payload.values() if isinstance(value, list)]
            return sum(len(value) for value in lists) if lists else None
    return None


def _file_record(path: Path) -> dict[str, object]:
    resolved = path.resolve()
    stat = resolved.stat()
    return {
        "path": str(resolved),
        "sha256": _sha256(resolved),
        "bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "row_count": _row_count(resolved),
    }


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


class AuditPipeline:
    def __init__(self, input_dir: str | Path, work_dir: str | Path, *, region: str = "all") -> None:
        self.input_dir = Path(input_dir).resolve()
        self.work_dir = Path(work_dir).resolve()
        self.region = region
        if region not in {"us", "canada", "europe", "all"}:
            raise ValueError(f"unsupported region: {region}")

    @property
    def manifest_dir(self) -> Path:
        return self.work_dir / "manifests"

    def run(self, *, resume: bool) -> dict[str, object]:
        executed: list[str] = []
        skipped: list[str] = []
        must_execute = not resume
        for stage in PIPELINE_STAGES:
            if not must_execute and self.checkpoint_is_valid(stage):
                skipped.append(stage)
                continue
            must_execute = True
            self._execute(stage)
            executed.append(stage)
        return {
            "status": "complete",
            "executed": executed,
            "skipped": skipped,
            "last_valid_checkpoint": self.last_valid_checkpoint(),
        }

    def run_stage(self, stage: str) -> dict[str, object]:
        if stage not in PIPELINE_STAGES:
            raise ValueError(f"unknown pipeline stage: {stage}")
        index = PIPELINE_STAGES.index(stage)
        if index:
            dependency = PIPELINE_STAGES[index - 1]
            if not self.checkpoint_is_valid(dependency):
                raise PipelineError(
                    f"{stage} requires a valid {dependency} checkpoint; run the preceding stage first"
                )
        self._execute(stage)
        return {
            "status": "complete",
            "executed": [stage],
            "skipped": [],
            "last_valid_checkpoint": self.last_valid_checkpoint(),
        }

    def validate(self) -> dict[str, object]:
        validity = {stage: self.checkpoint_is_valid(stage) for stage in PIPELINE_STAGES}
        failures = [stage for stage, valid in validity.items() if not valid]
        return {
            "status": "PASS" if not failures else "FAIL",
            "schema_version": PASS2_SCHEMA_VERSION,
            "checked_at": _now(),
            "checkpoints": validity,
            "failures": failures,
            "last_valid_checkpoint": self.last_valid_checkpoint(),
        }

    def last_valid_checkpoint(self) -> str | None:
        last_valid = None
        for stage in PIPELINE_STAGES:
            if not self.checkpoint_is_valid(stage):
                break
            last_valid = stage
        return last_valid

    def checkpoint_is_valid(self, stage: str) -> bool:
        checkpoint_path = self.manifest_dir / f"{stage}.json"
        payload = read_json(checkpoint_path)
        if not isinstance(payload, dict):
            return False
        if (
            payload.get("status") != "complete"
            or payload.get("stage") != stage
            or payload.get("schema_version") != PASS2_SCHEMA_VERSION
            or payload.get("parameters") != self._stage_parameters(stage)
        ):
            return False
        records = list(payload.get("inputs", [])) + list(payload.get("outputs", []))
        if not records:
            return False
        for record in records:
            path = Path(str(record.get("path", "")))
            if not path.is_file() or record.get("sha256") != _sha256(path):
                return False
        return True

    def _execute(self, stage: str) -> None:
        started_at = _now()
        run_id = str(uuid.uuid4())
        inputs = self._stage_inputs(stage)
        outputs = self._stage_outputs(stage)
        try:
            missing = [str(path) for path in inputs if not path.is_file()]
            if missing:
                raise PipelineError(f"missing required input files: {missing}")
            runner: Callable[[], None] = getattr(self, f"_{stage}")
            runner()
            missing_outputs = [str(path) for path in outputs if not path.is_file()]
            if missing_outputs:
                raise PipelineError(f"stage did not create expected outputs: {missing_outputs}")
            payload = {
                "schema_version": PASS2_SCHEMA_VERSION,
                "stage": stage,
                "status": "complete",
                "run_id": run_id,
                "started_at": started_at,
                "completed_at": _now(),
                "parameters": self._stage_parameters(stage),
                "inputs": [_file_record(path) for path in inputs],
                "outputs": [_file_record(path) for path in outputs],
                "failures": [],
            }
        except Exception as error:
            payload = {
                "schema_version": PASS2_SCHEMA_VERSION,
                "stage": stage,
                "status": "failed",
                "run_id": run_id,
                "started_at": started_at,
                "completed_at": _now(),
                "parameters": self._stage_parameters(stage),
                "inputs": [_file_record(path) for path in inputs if path.is_file()],
                "outputs": [_file_record(path) for path in outputs if path.is_file()],
                "failures": [{"type": type(error).__name__, "message": str(error)}],
            }
            write_json(self.manifest_dir / f"{stage}.json", payload)
            raise
        write_json(self.manifest_dir / f"{stage}.json", payload)

    def _stage_inputs(self, stage: str) -> list[Path]:
        inputs = {
            "discovery": [
                self.input_dir / "institutions.csv",
                self.input_dir / "program_candidates.csv",
            ],
            "screening": [
                self.work_dir / "discovery" / "institutions.csv",
                self.work_dir / "discovery" / "program_candidates.csv",
            ],
            "research_fit": [self.work_dir / "screening" / "programs.csv"],
            "verification": [
                self.work_dir / "research_fit" / "programs.csv",
                self.input_dir / "program_evidence.csv",
                self.input_dir / "professor_evidence.csv",
                self.input_dir / "score_components.csv",
                self.input_dir / "source_ledger.csv",
            ],
            "scoring": [
                self.work_dir / "evidence" / "program_evidence.csv",
                self.work_dir / "evidence" / "professor_evidence.csv",
                self.work_dir / "evidence" / "score_components.csv",
            ],
            "portfolio": [self.work_dir / "scoring" / "program_scores.csv"],
            "outreach": [
                self.work_dir / "portfolio" / "portfolio.json",
                self.work_dir / "evidence" / "professor_evidence.csv",
                self.work_dir / "scoring" / "program_scores.csv",
            ],
            "reporting": [
                self.work_dir / "discovery" / "institutions.csv",
                self.work_dir / "screening" / "programs.csv",
                self.work_dir / "evidence" / "program_evidence.csv",
                self.work_dir / "evidence" / "professor_evidence.csv",
                self.work_dir / "evidence" / "source_ledger.csv",
                self.work_dir / "scoring" / "program_scores.csv",
                self.work_dir / "portfolio" / "portfolio.json",
                self.work_dir / "outreach" / "outreach_priority.csv",
            ],
        }
        package_root = Path(__file__).resolve().parent
        implementation_inputs = [package_root / "pipeline.py", package_root / "schema.py"]
        if stage == "scoring":
            implementation_inputs.extend(
                [package_root / "hard_gates.py", package_root / "scoring.py"]
            )
        if stage == "portfolio":
            implementation_inputs.append(package_root / "portfolio.py")
        return inputs[stage] + implementation_inputs

    def _stage_parameters(self, stage: str) -> dict[str, str]:
        return {} if stage == "discovery" else {"region": self.region}

    def _stage_outputs(self, stage: str) -> list[Path]:
        outputs = {
            "discovery": [
                self.work_dir / "discovery" / "institutions.csv",
                self.work_dir / "discovery" / "program_candidates.csv",
            ],
            "screening": [self.work_dir / "screening" / "programs.csv"],
            "research_fit": [self.work_dir / "research_fit" / "programs.csv"],
            "verification": [
                self.work_dir / "evidence" / "program_evidence.csv",
                self.work_dir / "evidence" / "professor_evidence.csv",
                self.work_dir / "evidence" / "score_components.csv",
                self.work_dir / "evidence" / "source_ledger.csv",
            ],
            "scoring": [self.work_dir / "scoring" / "program_scores.csv"],
            "portfolio": [self.work_dir / "portfolio" / "portfolio.json"],
            "outreach": [self.work_dir / "outreach" / "outreach_priority.csv"],
            "reporting": [
                self.work_dir / "reports" / "audit_report.md",
                self.work_dir / "reports" / "run_summary.json",
            ],
        }
        return outputs[stage]

    def _discovery(self) -> None:
        institutions = read_csv(self.input_dir / "institutions.csv")
        candidates = read_csv(self.input_dir / "program_candidates.csv")
        institution_ids = [row.get("institution_id", "") for row in institutions]
        if not institutions or not candidates:
            raise PipelineError("discovery inputs must contain institutions and program candidates")
        if any(not value for value in institution_ids) or len(set(institution_ids)) != len(institution_ids):
            raise PipelineError("institution IDs must be populated and unique")
        known_institutions = set(institution_ids)
        program_ids = [row.get("program_id", "") for row in candidates]
        if any(not value for value in program_ids) or len(set(program_ids)) != len(program_ids):
            raise PipelineError("program IDs must be populated and unique")
        unknown = sorted(
            {row.get("institution_id", "") for row in candidates} - known_institutions
        )
        if unknown:
            raise PipelineError(f"program candidates reference unknown institutions: {unknown}")
        for row in institutions:
            row["schema_version"] = PASS2_SCHEMA_VERSION
        for row in candidates:
            row["schema_version"] = PASS2_SCHEMA_VERSION
        write_csv(
            self.work_dir / "discovery" / "institutions.csv",
            institutions,
            INSTITUTION_COLUMNS_V2,
        )
        write_csv(
            self.work_dir / "discovery" / "program_candidates.csv",
            candidates,
            PROGRAM_COLUMNS_V2,
        )

    def _screening(self) -> None:
        institutions = {
            row["institution_id"]: row
            for row in read_csv(self.work_dir / "discovery" / "institutions.csv")
        }
        programs = read_csv(self.work_dir / "discovery" / "program_candidates.csv")
        screened: list[dict[str, str]] = []
        for row in programs:
            institution = institutions[row["institution_id"]]
            if self.region != "all" and institution.get("region", "").lower() != self.region:
                continue
            failures = [
                name
                for name in (
                    "recognized_active_institution",
                    "relevant_research_program",
                    "international_student_eligible",
                    "bachelor_entry_or_research_masters_route",
                    "compatible_degree_structure",
                )
                if not _truthy(row.get(name))
            ]
            row["schema_version"] = PASS2_SCHEMA_VERSION
            row["screening_decision"] = "excluded" if failures else "retained"
            row["exclusion_reason"] = ", ".join(failures)
            row["preliminary_fit"] = "preliminary"
            screened.append(row)
        if not screened:
            raise PipelineError(f"screening produced no rows for region {self.region}")
        write_csv(self.work_dir / "screening" / "programs.csv", screened, PROGRAM_COLUMNS_V2)

    def _research_fit(self) -> None:
        programs = read_csv(self.work_dir / "screening" / "programs.csv")
        for row in programs:
            signal = row.get("exact_research_fit_signal", "").strip()
            if row.get("screening_decision") == "retained" and signal:
                row["preliminary_fit"] = "verified_signal"
            elif row.get("screening_decision") == "retained":
                row["preliminary_fit"] = "unresolved"
                row["screening_decision"] = "investigate_further"
                row["unresolved_conflicts"] = "; ".join(
                    value
                    for value in (row.get("unresolved_conflicts", ""), "research-fit signal missing")
                    if value
                )
        write_csv(self.work_dir / "research_fit" / "programs.csv", programs, PROGRAM_COLUMNS_V2)

    def _verification(self) -> None:
        programs = read_csv(self.work_dir / "research_fit" / "programs.csv")
        evidence_rows = read_csv(self.input_dir / "program_evidence.csv")
        professors = read_csv(self.input_dir / "professor_evidence.csv")
        components = read_csv(self.input_dir / "score_components.csv")
        sources = read_csv(self.input_dir / "source_ledger.csv")
        program_ids = {row["program_id"] for row in programs}
        evidence_by_program = {row.get("program_id", ""): row for row in evidence_rows}
        if program_ids != set(evidence_by_program):
            missing = sorted(program_ids - set(evidence_by_program))
            extra = sorted(set(evidence_by_program) - program_ids)
            raise PipelineError(f"program evidence mismatch; missing={missing}, extra={extra}")
        source_by_id = {row.get("source_id", ""): row for row in sources}
        if "" in source_by_id or len(source_by_id) != len(sources):
            raise PipelineError("source IDs must be populated and unique")

        for evidence in evidence_rows:
            if evidence.get("funding_gate_status", "").lower() in VERIFIED_FUNDING_VALUES:
                references = _split_refs(evidence.get("funding_gate_evidence"))
                official_verified = [
                    source_by_id.get(reference, {})
                    for reference in references
                    if source_by_id.get(reference, {}).get("official_or_secondary", "").lower()
                    == "official"
                    and source_by_id.get(reference, {}).get("verification_status", "").lower()
                    == "verified"
                ]
                if not references or not official_verified:
                    raise PipelineError(
                        f"{evidence['program_id']} has verified funding without verified official evidence"
                    )

        for professor in professors:
            if professor.get("program_id", "") not in program_ids:
                raise PipelineError(f"professor references unknown program: {professor.get('program_id')}")
            if (
                professor.get("can_supervise_program", "").lower() == "verified"
                and professor.get("verification_status", "").lower() == "verified"
            ):
                references = _split_refs(professor.get("evidence_ids"))
                if not professor.get("official_faculty_url") or any(
                    reference not in source_by_id for reference in references
                ) or not references:
                    raise PipelineError(
                        f"{professor.get('professor_id')} lacks traceable supervision evidence"
                    )

        for component in components:
            if component.get("program_id", "") not in program_ids:
                raise PipelineError(f"score component references unknown program: {component.get('program_id')}")
            references = _split_refs(component.get("evidence_ids"))
            if _number(component.get("score")) > 0 and not references:
                raise PipelineError(
                    f"positive score component lacks evidence: {component.get('program_id')} / "
                    f"{component.get('component')}"
                )
            unknown_references = sorted(set(references) - set(source_by_id))
            if unknown_references:
                raise PipelineError(f"score component has unknown evidence IDs: {unknown_references}")

        merged_programs = []
        for row in programs:
            merged = {**row, **evidence_by_program[row["program_id"]]}
            merged["schema_version"] = PASS2_SCHEMA_VERSION
            merged_programs.append(merged)
        for row in professors:
            row["schema_version"] = PASS2_SCHEMA_VERSION
        for row in components:
            row["schema_version"] = PASS2_SCHEMA_VERSION
        for row in sources:
            row["schema_version"] = PASS2_SCHEMA_VERSION
        write_csv(
            self.work_dir / "evidence" / "program_evidence.csv",
            merged_programs,
            PROGRAM_COLUMNS_V2,
        )
        write_csv(
            self.work_dir / "evidence" / "professor_evidence.csv",
            professors,
            PROFESSOR_COLUMNS_V2,
        )
        write_csv(
            self.work_dir / "evidence" / "score_components.csv",
            components,
            SCORE_COMPONENT_COLUMNS_V2,
        )
        write_csv(
            self.work_dir / "evidence" / "source_ledger.csv",
            sources,
            SOURCE_COLUMNS_V2,
        )

    def _scoring(self) -> None:
        programs = read_csv(self.work_dir / "evidence" / "program_evidence.csv")
        professors = read_csv(self.work_dir / "evidence" / "professor_evidence.csv")
        components = read_csv(self.work_dir / "evidence" / "score_components.csv")
        components_by_program: dict[str, list[dict[str, str]]] = defaultdict(list)
        for component in components:
            components_by_program[component["program_id"]].append(component)

        scored: list[dict[str, str]] = []
        for row in programs:
            program_components = components_by_program[row["program_id"]]
            names = [component.get("component", "") for component in program_components]
            if set(names) != set(COMPONENTS) or len(names) != len(COMPONENTS):
                raise PipelineError(
                    f"{row['program_id']} must have exactly one row for every score component"
                )
            component_evidence: dict[str, dict[str, object]] = {}
            for component in program_components:
                component_name = component["component"]
                output_field, maximum = COMPONENTS[component_name]
                score = _number(component.get("score"))
                declared_maximum = _number(component.get("max_score"))
                if declared_maximum != maximum or not 0 <= score <= maximum:
                    raise PipelineError(
                        f"invalid {component_name} score for {row['program_id']}: "
                        f"{score}/{declared_maximum}"
                    )
                row[output_field] = str(score)
                component_evidence[component_name] = {
                    "score": score,
                    "maximum": maximum,
                    "rubric_anchor": component.get("rubric_anchor", ""),
                    "evidence_ids": _split_refs(component.get("evidence_ids")),
                    "evidence_completeness": component.get("evidence_completeness", ""),
                    "score_confidence": component.get("score_confidence", ""),
                }

            gate_result = evaluate_hard_gates(row, professors)
            if gate_result.distinct_verified_professor_count < 2 and _number(
                row.get("faculty_depth_score")
            ) > 5:
                raise PipelineError(
                    f"{row['program_id']} claims more than 5 faculty-depth points with fewer "
                    "than two distinct verified professors"
                )
            completeness_values = {
                component.get("evidence_completeness", "").lower()
                for component in program_components
            }
            row["evidence_completeness"] = (
                "complete"
                if completeness_values == {"complete"}
                and row.get("evidence_completeness", "").lower() == "complete"
                else "partial"
            )
            confidence_values = [
                component.get("score_confidence", "").lower()
                for component in program_components
            ] + [row.get("score_confidence", "").lower()]
            row["score_confidence"] = min(
                (value for value in confidence_values if value in CONFIDENCE_ORDER),
                key=CONFIDENCE_ORDER.get,
                default="low",
            )
            conflicts = list(
                dict.fromkeys(
                    value
                    for value in [row.get("unresolved_conflicts", "")]
                    + [component.get("unresolved_conflicts", "") for component in program_components]
                    if value
                )
            )
            row["unresolved_conflicts"] = "; ".join(conflicts)
            row["score_component_evidence"] = json.dumps(
                component_evidence, sort_keys=True, separators=(",", ":")
            )
            row["distinct_verified_professor_count"] = str(
                gate_result.distinct_verified_professor_count
            )
            row["hard_gate_failures"] = "|".join(gate_result.failures)
            score_input: dict[str, object] = {
                **row,
                **gate_result.gates,
                "material_unresolved_gate": bool(conflicts),
            }
            result = calculate_score(score_input)
            row["research_fit_score"] = str(result.research_fit_score)
            row["overall_score"] = str(result.overall_score)
            row["recommendation"] = result.recommendation
            row["schema_version"] = PASS2_SCHEMA_VERSION
            scored.append(row)
        write_csv(
            self.work_dir / "scoring" / "program_scores.csv",
            scored,
            PROGRAM_COLUMNS_V2,
        )

    def _portfolio(self) -> None:
        programs = read_csv(self.work_dir / "scoring" / "program_scores.csv")
        write_json(self.work_dir / "portfolio" / "portfolio.json", select_portfolio(programs))

    def _outreach(self) -> None:
        portfolio = read_json(self.work_dir / "portfolio" / "portfolio.json")
        programs = {
            row["program_id"]: row
            for row in read_csv(self.work_dir / "scoring" / "program_scores.csv")
        }
        professors = read_csv(self.work_dir / "evidence" / "professor_evidence.csv")
        selected_programs = {
            row.get("program_id", "")
            for key in ("core", "reserve", "monitor_for_2027_position")
            for row in portfolio.get(key, [])
        }
        rows: list[dict[str, str]] = []
        for professor in professors:
            program_id = professor.get("program_id", "")
            if program_id not in selected_programs:
                continue
            if (
                professor.get("can_supervise_program", "").lower() != "verified"
                or professor.get("verification_status", "").lower() != "verified"
            ):
                continue
            program = programs[program_id]
            rows.append(
                {
                    "schema_version": PASS2_SCHEMA_VERSION,
                    "program_id": program_id,
                    "institution_name": program.get("institution_name", ""),
                    "contact_type": "professor",
                    "contact_name": professor.get("full_name", ""),
                    "official_contact": professor.get("official_email")
                    or professor.get("official_faculty_url", ""),
                    "information_gap": program.get("unresolved_question", "")
                    or program.get("unresolved_conflicts", ""),
                    "outreach_status": "manual_review_required",
                    "evidence_ids": professor.get("evidence_ids", ""),
                }
            )
        write_csv(
            self.work_dir / "outreach" / "outreach_priority.csv",
            rows,
            OUTREACH_PRIORITY_COLUMNS_V2,
        )

    def _reporting(self) -> None:
        institutions = read_csv(self.work_dir / "discovery" / "institutions.csv")
        screened = read_csv(self.work_dir / "screening" / "programs.csv")
        program_evidence = read_csv(self.work_dir / "evidence" / "program_evidence.csv")
        professors = read_csv(self.work_dir / "evidence" / "professor_evidence.csv")
        sources = read_csv(self.work_dir / "evidence" / "source_ledger.csv")
        scores = read_csv(self.work_dir / "scoring" / "program_scores.csv")
        portfolio = read_json(self.work_dir / "portfolio" / "portfolio.json")
        outreach = read_csv(self.work_dir / "outreach" / "outreach_priority.csv")
        summary = {
            "schema_version": PASS2_SCHEMA_VERSION,
            "generated_at": _now(),
            "counts": {
                "institutions": len(institutions),
                "screened_programs": len(screened),
                "verified_program_records": len(program_evidence),
                "professor_records": len(professors),
                "sources": len(sources),
                "scored_programs": len(scores),
                "core": len(portfolio.get("core", [])),
                "reserve": len(portfolio.get("reserve", [])),
                "monitor": len(portfolio.get("monitor_for_2027_position", [])),
                "outreach_candidates": len(outreach),
            },
            "recommendations": {
                row["program_id"]: row.get("recommendation", "") for row in scores
            },
            "unresolved_conflicts": {
                row["program_id"]: row.get("unresolved_conflicts", "")
                for row in scores
                if row.get("unresolved_conflicts", "")
            },
        }
        write_json(self.work_dir / "reports" / "run_summary.json", summary)
        counts = summary["counts"]
        lines = [
            "# Graduate audit pipeline report",
            "",
            f"Schema version: {PASS2_SCHEMA_VERSION}",
            "",
            "## Counts",
            "",
        ]
        lines.extend(f"- {name.replace('_', ' ').title()}: {value}" for name, value in counts.items())
        lines.extend(["", "## Program decisions", ""])
        lines.extend(
            f"- {row.get('institution_name')}: {row.get('program_name')} — "
            f"{row.get('recommendation')} ({row.get('overall_score')}/100)"
            for row in scores
        )
        lines.extend(["", "Unresolved conflicts remain explicit in `run_summary.json`.", ""])
        _write_text(self.work_dir / "reports" / "audit_report.md", "\n".join(lines))
