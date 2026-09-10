from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

import requests
import yaml

from graduate_audit.io import write_csv, write_json
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
    program_id,
    source_id,
)
from graduate_audit.validation import validate_outputs


ACCESS_DATE = date.today().isoformat()
DATA_CENTER_URL = "https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx"
GRADUATE_AWARD_LEVELS = {"7", "17", "18", "19"}

DATASETS = {
    "HD2024": {
        "url": "https://nces.ed.gov/ipeds/datacenter/data/HD2024.zip",
        "member": "HD2024.csv",
        "sha256": "d98425c123d7c0e872aec6e83960dfb501884818bf17385c340790f3d1f28345",
        "last_modified": "2025-09-21T20:40:58Z",
        "release": "2024-25 provisional",
        "description": "IPEDS 2024 directory information",
    },
    "IC2024": {
        "url": "https://nces.ed.gov/ipeds/datacenter/data/IC2024.zip",
        "member": "IC2024.csv",
        "sha256": "924f04f0afd953633a34bbc2ad1beaa65fdbf2a7ba25ebe364bac7469a976288",
        "last_modified": "2025-09-21T20:41:04Z",
        "release": "2024-25 provisional",
        "description": "IPEDS institutional educational offerings",
    },
    "C2024_A": {
        "url": "https://nces.ed.gov/ipeds/datacenter/data/C2024_A.zip",
        "member": "C2024_a.csv",
        "sha256": "03234cc27fe4e7eb835a66d4f37aaec11bdac8dfa278f971584e1b20d03e1159",
        "last_modified": "2025-09-21T20:40:37Z",
        "release": "2023-24 provisional",
        "description": "IPEDS completions by 6-digit CIP and award level",
    },
    "C2023_A": {
        "url": "https://nces.ed.gov/ipeds/datacenter/data/C2023_A.zip",
        "member": "C2023_a_RV.csv",
        "sha256": "651d95b6405bb86c6c14884ed54225a27492199d21d8acd63cda2581aa60838a",
        "last_modified": "2025-09-21T20:41:09Z",
        "release": "2022-23 final/revised member",
        "description": "IPEDS completions by 6-digit CIP and award level",
    },
    "C2022_A": {
        "url": "https://nces.ed.gov/ipeds/datacenter/data/C2022_A.zip",
        "member": "c2022_a_rv.csv",
        "sha256": "f81b8390d1758ac710b85a1d5a7af51372770335a02c0d06802a46d3a068126c",
        "last_modified": "2024-06-05T13:45:15Z",
        "release": "2021-22 final/revised member",
        "description": "IPEDS completions by 6-digit CIP and award level",
    },
}

CIP_TITLES = {
    "11.0101": "Computer and Information Sciences, General",
    "11.0102": "Artificial Intelligence",
    "11.0103": "Information Technology",
    "11.0104": "Informatics",
    "11.0105": "Human-Centered Technology Design",
    "11.0199": "Computer and Information Sciences, Other",
    "11.0401": "Information Science/Studies",
    "11.0701": "Computer Science",
    "11.0901": "Computer Systems Networking and Telecommunications",
    "11.0902": "Cloud Computing",
    "11.0999": "Computer Systems Networking and Telecommunications, Other",
    "11.1003": "Computer and Information Systems Security/Auditing/Information Assurance",
    "14.0901": "Computer Engineering, General",
    "14.0902": "Computer Hardware Engineering",
    "14.0903": "Computer Software Engineering",
    "14.0999": "Computer Engineering, Other",
    "14.1001": "Electrical and Electronics Engineering",
    "14.4201": "Mechatronics, Robotics, and Automation Engineering",
    "30.7001": "Data Science, General",
    "30.7101": "Data Analytics, General",
    "43.0403": "Cyber/Computer Forensics and Counterterrorism",
}

HIGHEST_OFFERING = {
    "7": "Master's degree",
    "8": "Post-master's certificate",
    "9": "Doctor's degree",
}

GRADUATE_DEGREE_LEVELS = {
    "LEVEL7": "Master's degree",
    "LEVEL17": "Doctor's degree-research/scholarship",
    "LEVEL18": "Doctor's degree-professional practice",
    "LEVEL19": "Doctor's degree-other",
}

SECTOR_LABELS = {
    "0": "Administrative unit",
    "1": "Public, 4-year or above",
    "2": "Private nonprofit, 4-year or above",
    "3": "Private for-profit, 4-year or above",
    "4": "Public, 2-year",
    "5": "Private nonprofit, 2-year",
    "6": "Private for-profit, 2-year",
    "7": "Public, less-than-2-year",
    "8": "Private nonprofit, less-than-2-year",
    "9": "Private for-profit, less-than-2-year",
    "99": "Sector unknown",
}

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
    "AS": "American Samoa", "FM": "Federated States of Micronesia", "GU": "Guam",
    "MH": "Marshall Islands", "MP": "Northern Mariana Islands", "PR": "Puerto Rico",
    "PW": "Palau", "VI": "U.S. Virgin Islands",
}

STATE_CODES = set(STATE_NAMES) - {"DC", "AS", "FM", "GU", "MH", "MP", "PR", "PW", "VI"}
OTHER_JURISDICTIONS = {"AS", "FM", "GU", "MH", "MP", "PR", "PW", "VI"}

# These pages were opened and checked on the access date. They are intentionally a
# small spot-check layer; the exhaustive output remains a mechanical IPEDS screen.
OFFICIAL_PROGRAM_CHECKS = {
    "211440": {
        "program_name": "Software Engineering Ph.D.",
        "url": "https://se-phd.isri.cmu.edu/",
        "department": "Software and Societal Systems Department",
        "claim": "Official program page describes an active Software Engineering Ph.D. focused on complex software systems in an AI future.",
        "fit": "Strong topical overlap with AI-assisted software engineering, reliability, assurance, and software security.",
    },
    "139755": {
        "program_name": "Ph.D. in Computer Science",
        "url": "https://www.cc.gatech.edu/degree-programs/phd-computer-science",
        "department": "College of Computing",
        "claim": "Official program page describes an active research-oriented Ph.D. in Computer Science culminating in dissertation research.",
        "fit": "Broad computing research route that warrants faculty-level software engineering, systems, AI, and security review.",
    },
    "228778": {
        "program_name": "Ph.D. in Computer Science",
        "url": "https://www.cs.utexas.edu/graduate/research-degrees",
        "department": "Department of Computer Science",
        "claim": "Official research-degrees page describes an active Ph.D. with early research immersion and dissertation credit.",
        "fit": "Broad research program with relevant programming languages, systems, AI, and reliability directions requiring faculty verification.",
    },
    "110653": {
        "program_name": "Ph.D. in Software Engineering",
        "url": "https://informatics.ics.uci.edu/phd-software-engineering/",
        "department": "Department of Informatics",
        "claim": "Official program page describes an active Software Engineering Ph.D. addressing software quality, debugging, development infrastructure, and empirical work.",
        "fit": "Direct overlap with software repair, testing, reliability, and AI-assisted development.",
    },
    "233921": {
        "program_name": "Ph.D. in Computer Science and Applications",
        "url": "https://website.cs.vt.edu/academic/graduate/future-grads.html",
        "department": "Department of Computer Science",
        "claim": "Official graduate-program page lists an active research Ph.D. and research-track funding opportunities.",
        "fit": "Broad research route with software engineering, systems, and security potential requiring faculty-level review.",
    },
    "232186": {
        "program_name": "Ph.D. in Computer Science",
        "url": "https://cs.gmu.edu/academics/graduate-programs",
        "department": "Department of Computer Science",
        "claim": "Official graduate-program page lists an active Ph.D. in Computer Science and research collaboration with faculty.",
        "fit": "Computing and software-security breadth warrants deep faculty and funding review.",
    },
    "199193": {
        "program_name": "Ph.D. in Computer Science",
        "url": "https://csc.ncsu.edu/academics/graduate/phd/",
        "department": "Department of Computer Science",
        "claim": "Official program page describes a 72-credit Ph.D. beyond the bachelor's degree with research, advisor, and dissertation requirements.",
        "fit": "Strong software engineering, security, systems, and AI breadth; direct-from-bachelor structure is explicitly described.",
        "direct_from_bachelors": "Yes; official page defines requirements beyond the bachelor's degree",
    },
    "214777": {
        "program_name": "Ph.D. in Computer Science and Engineering",
        "url": "https://www.eecs.psu.edu/students/graduate/Graduate-Degree-Programs-CSE.aspx",
        "department": "School of Electrical Engineering and Computer Science",
        "claim": "Official graduate-degree page lists an active Computer Science and Engineering Ph.D. with a required research experience.",
        "fit": "Broad computing route requiring faculty-level software engineering, AI, systems, and security review.",
    },
    "209542": {
        "program_name": "Ph.D. in Computer Science",
        "url": "https://engineering.oregonstate.edu/academics/programs/computer-science/graduate",
        "department": "School of Electrical Engineering and Computer Science",
        "claim": "Official graduate-program page lists an active Computer Science Ph.D. and research areas including AI, cybersecurity, and software engineering.",
        "fit": "Explicit software engineering, AI, and cybersecurity breadth warrants deep faculty review.",
    },
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(url: str, destination: Path) -> None:
    partial = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=(30, 180)) as response:
        response.raise_for_status()
        with partial.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    partial.replace(destination)


def _ensure_dataset(name: str, cache_dir: Path) -> tuple[Path, dict[str, object]]:
    spec = DATASETS[name]
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{name}.zip"
    if not path.exists() or _sha256(path) != spec["sha256"]:
        _download(str(spec["url"]), path)
    actual_hash = _sha256(path)
    if actual_hash != spec["sha256"]:
        raise RuntimeError(
            f"{name} checksum mismatch: expected {spec['sha256']}, got {actual_hash}"
        )
    with zipfile.ZipFile(path) as archive:
        members = {item.filename: item.file_size for item in archive.infolist()}
        if spec["member"] not in members:
            raise RuntimeError(f"{name} does not contain frozen member {spec['member']}")
    return path, {
        "dataset": name,
        "url": spec["url"],
        "selected_member": spec["member"],
        "sha256": actual_hash,
        "last_modified": spec["last_modified"],
        "bytes": path.stat().st_size,
        "release": spec["release"],
        "description": spec["description"],
        "zip_members": members,
    }


def _read_zip_rows(path: Path, member: str) -> Iterable[dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        with archive.open(member) as raw:
            with io.TextIOWrapper(raw, encoding="utf-8-sig", newline="") as text:
                yield from csv.DictReader(text)


def _normalized_code(value: str) -> str:
    stripped = value.strip().lstrip("0")
    return stripped or "0"


def _website(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if not value.lower().startswith(("http://", "https://")):
        value = f"https://{value}"
    return value.rstrip("/")


def _jurisdiction_group(state_code: str) -> str:
    if state_code in STATE_CODES:
        return "US state"
    if state_code == "DC":
        return "District of Columbia"
    return "IPEDS other jurisdiction"


def _institution_base(row: dict[str, str], offerings: dict[str, str] | None) -> dict[str, object]:
    unitid = row["UNITID"]
    state_code = row.get("STABBR", "")
    verified_levels = [
        label
        for variable, label in GRADUATE_DEGREE_LEVELS.items()
        if offerings and offerings.get(variable) == "1"
    ]
    offering = (
        "; ".join(verified_levels)
        if verified_levels
        else f"{HIGHEST_OFFERING.get(row.get('HLOFFER', ''), 'Graduate level')} (HD fallback)"
    )
    return {
        "institution_id": f"us:ipeds:{unitid}",
        "institution_name": row["INSTNM"],
        "alternate_names": row.get("IALIAS", ""),
        "country": "United States",
        "region": _jurisdiction_group(state_code),
        "institution_type": SECTOR_LABELS.get(row.get("SECTOR", ""), "Unknown"),
        "recognition_status": "Indexed by IPEDS; accreditation requires separate verification",
        "active_status": "Active in HD2024 (CYACTIVE=1)",
        "official_website": _website(row.get("WEBADDR", "")),
        "source_database": "NCES IPEDS HD2024 and IC2024",
        "dataset_release": "2024-25 provisional; downloaded as frozen HD2024/IC2024 archives",
        "access_date": ACCESS_DATE,
        "graduate_degree_authority": f"{offering}; IPEDS HLOFFER={row.get('HLOFFER', '')}",
        "ror_id": "",
        "ipeds_unitid": unitid,
        "eter_id": "",
        "dli_number": "",
        "manual_verification": "No; mechanical IPEDS screen",
        "notes": (
            f"IPEDS location {STATE_NAMES.get(state_code, state_code or 'unknown')} "
            f"({state_code or 'no code'}); active degree-granting institution with "
            f"master's or doctoral authority established from IC level indicators or HD highest-offering fallback."
        ),
    }


def _blank_program() -> dict[str, object]:
    return {column: "" for column in PROGRAM_COLUMNS}


def _build_outputs(cache_dir: Path) -> tuple[dict[str, list[dict[str, object]]], dict[str, object]]:
    dataset_paths: dict[str, Path] = {}
    dataset_records: list[dict[str, object]] = []
    for name in DATASETS:
        dataset_paths[name], record = _ensure_dataset(name, cache_dir)
        dataset_records.append(record)

    topic_config = yaml.safe_load((_repo_root() / "config" / "research_topics.yaml").read_text(encoding="utf-8"))
    primary = set(topic_config["us_cip_2020"]["primary"])
    secondary = set(topic_config["us_cip_2020"]["secondary_review_only"])
    configured_cips = primary | secondary

    hd_rows = list(_read_zip_rows(dataset_paths["HD2024"], str(DATASETS["HD2024"]["member"])))
    ic_rows = list(_read_zip_rows(dataset_paths["IC2024"], str(DATASETS["IC2024"]["member"])))
    ic_by_unitid = {row["UNITID"]: row for row in ic_rows}
    universe_hd = {
        row["UNITID"]: row
        for row in hd_rows
        if row.get("CYACTIVE") == "1"
        and row.get("DEGGRANT") == "1"
        and (
            row.get("HLOFFER") in {"7", "9"}
            or (
                row.get("HLOFFER") == "8"
                and any(
                    ic_by_unitid.get(row["UNITID"], {}).get(variable) == "1"
                    for variable in GRADUATE_DEGREE_LEVELS
                )
            )
        )
    }

    signals: dict[tuple[str, str], dict[str, object]] = {}
    completion_rows_scanned: dict[str, int] = {}
    qualifying_rows: dict[str, int] = {}
    signal_rows_outside_current_universe: set[str] = set()
    for dataset_name in ("C2022_A", "C2023_A", "C2024_A"):
        member = str(DATASETS[dataset_name]["member"])
        scanned = 0
        qualified = 0
        for row in _read_zip_rows(dataset_paths[dataset_name], member):
            scanned += 1
            cip = row.get("CIPCODE", "").strip()
            if (
                _normalized_code(row.get("MAJORNUM", "")) != "1"
                or _normalized_code(row.get("AWLEVEL", "")) not in GRADUATE_AWARD_LEVELS
                or cip not in configured_cips
            ):
                continue
            try:
                completions = int(row.get("CTOTALT", "") or 0)
            except ValueError:
                completions = 0
            if completions <= 0:
                continue
            qualified += 1
            unitid = row["UNITID"]
            if unitid not in universe_hd:
                signal_rows_outside_current_universe.add(unitid)
                continue
            key = (unitid, cip)
            signal = signals.setdefault(
                key,
                {
                    "years": set(),
                    "award_levels": set(),
                    "completions_by_year": {},
                    "source_datasets": set(),
                },
            )
            academic_year = {
                "C2022_A": "2021-22",
                "C2023_A": "2022-23",
                "C2024_A": "2023-24",
            }[dataset_name]
            signal["years"].add(academic_year)
            signal["award_levels"].add(_normalized_code(row.get("AWLEVEL", "")))
            signal["source_datasets"].add(dataset_name)
            signal["completions_by_year"][academic_year] = (
                int(signal["completions_by_year"].get(academic_year, 0)) + completions
            )
        completion_rows_scanned[dataset_name] = scanned
        qualifying_rows[dataset_name] = qualified

    signals_by_unitid: dict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)
    for (unitid, cip), signal in signals.items():
        signals_by_unitid[unitid].append((cip, signal))

    institutions: list[dict[str, object]] = []
    programs: list[dict[str, object]] = []
    exclusions: list[dict[str, object]] = []
    sources: list[dict[str, object]] = []
    program_evidence: list[dict[str, object]] = []

    hd_url = str(DATASETS["HD2024"]["url"])
    for unitid in sorted(universe_hd, key=int):
        hd = universe_hd[unitid]
        offerings = ic_by_unitid.get(unitid)
        institution = _institution_base(hd, offerings)
        institution_signals = signals_by_unitid.get(unitid, [])
        has_primary = any(cip in primary for cip, _ in institution_signals)
        if unitid in OFFICIAL_PROGRAM_CHECKS:
            institution["screening_status"] = "preliminary_fit"
            institution["relevant_graduate_field_signal"] = "Configured graduate CIP signal plus official program-page spot check"
            institution["manual_verification"] = "Yes; official program page spot-checked"
        elif institution_signals:
            institution["screening_status"] = "preliminary_fit"
            institution["relevant_graduate_field_signal"] = (
                "Primary configured graduate CIP completion signal"
                if has_primary
                else "Secondary review-only graduate CIP completion signal"
            )
        else:
            institution["screening_status"] = "no_relevant_graduate_field"
            institution["relevant_graduate_field_signal"] = "No configured 2022-2024 graduate first-major CIP completion signal"
            institution["exclusion_reason"] = (
                "No configured primary or secondary CIP completion signal in the three frozen "
                "IPEDS graduate first-major completions files; catalog-only and new programs remain a known gap."
            )
            exclusions.append(
                {
                    "institution_id": institution["institution_id"],
                    "institution_name": institution["institution_name"],
                    "country": "United States",
                    "program_id": "",
                    "program_name": "",
                    "stage_of_exclusion": "mechanical_program_screening",
                    "primary_exclusion_reason": institution["exclusion_reason"],
                    "supporting_evidence": (
                        "No positive-completion row at award levels 7/17/18/19 for any configured "
                        "primary or secondary CIP in C2022_A, C2023_A, or C2024_A."
                    ),
                    "source_url": DATA_CENTER_URL,
                    "confidence": "medium",
                    "manual_verification": "No",
                    "date_checked": ACCESS_DATE,
                }
            )
        institutions.append(institution)
        verified_ic_authority = bool(
            offerings
            and any(offerings.get(variable) == "1" for variable in GRADUATE_DEGREE_LEVELS)
        )
        authority_url = str(DATASETS["IC2024" if verified_ic_authority else "HD2024"]["url"])
        sources.extend(
            [
                {
                    "source_id": source_id(hd_url),
                    "institution_id": institution["institution_id"],
                    "institution_name": institution["institution_name"],
                    "program_id": "",
                    "program_or_professor": "",
                    "claim_type": "institution_status",
                    "exact_claim_supported": "Institution is active and degree-granting in IPEDS HD2024.",
                    "source_title": "IPEDS HD2024 directory information",
                    "publisher": "National Center for Education Statistics",
                    "publication_date": "2025-09-21",
                    "url": hd_url,
                    "source_type": "official complete data file",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "admissions_cycle": "",
                    "confidence": "high",
                    "verification_status": "checksum verified",
                    "access_note": "Claim derived from CYACTIVE=1 and DEGGRANT=1.",
                },
                {
                    "source_id": source_id(authority_url),
                    "institution_id": institution["institution_id"],
                    "institution_name": institution["institution_name"],
                    "program_id": "",
                    "program_or_professor": "",
                    "claim_type": "graduate_degree_authority",
                    "exact_claim_supported": str(institution["graduate_degree_authority"]),
                    "source_title": (
                        "IPEDS IC2024 educational offerings"
                        if verified_ic_authority
                        else "IPEDS HD2024 directory information"
                    ),
                    "publisher": "National Center for Education Statistics",
                    "publication_date": "2025-09-21",
                    "url": authority_url,
                    "source_type": "official complete data file",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "admissions_cycle": "",
                    "confidence": "high",
                    "verification_status": "checksum verified",
                    "access_note": (
                        "Claim derived from IC award-level indicators."
                        if verified_ic_authority
                        else "IC response unavailable; claim uses HD highest-offering fallback."
                    ),
                },
            ]
        )

    institution_lookup = {str(row["ipeds_unitid"]): row for row in institutions}
    for (unitid, cip), signal in sorted(signals.items(), key=lambda item: (int(item[0][0]), item[0][1])):
        institution = institution_lookup[unitid]
        title = CIP_TITLES.get(cip, f"CIP {cip}")
        tier = "primary" if cip in primary else "secondary review-only"
        degree = "Unclear"
        mechanical_name = f"IPEDS discovery signal: {title} (CIP {cip})"
        pid = program_id(str(institution["institution_id"]), degree, mechanical_name)
        years = sorted(signal["years"])
        award_levels = sorted(signal["award_levels"], key=int)
        totals = signal["completions_by_year"]
        program = _blank_program()
        program.update(
            {
                "program_id": pid,
                "institution_id": institution["institution_id"],
                "institution_name": institution["institution_name"],
                "country": "United States",
                "program_name": mechanical_name,
                "degree_type": degree,
                "direct_from_bachelors_eligible": "Unverified",
                "international_student_eligible": "Unverified",
                "language_of_instruction": "Unverified",
                "current_program_status": "Recent completions observed; current official catalog status not yet verified",
                "preliminary_fit": f"Configured {tier} discovery signal",
                "screening_decision": (
                    "advance_to_official_review" if cip in primary else "secondary_signal_manual_review"
                ),
                "exclusion_reason": "",
                "deadline_cycle_status": "Fall 2027 not yet published/verified",
                "funding_status": "Unverified",
                "admission_plausibility": "Insufficient evidence",
                "recommendation": "Investigate Further",
                "biggest_risk": "IPEDS completion code is only a discovery signal, not proof of a current matching program.",
                "unresolved_question": "Does the current official catalog contain a research graduate program matching the applicant's topics?",
                "verification_status": "Mechanical IPEDS discovery signal only",
                "notes": (
                    f"Observed academic years: {', '.join(years)}; award levels: {', '.join(award_levels)}; "
                    f"completions by year: {json.dumps(totals, sort_keys=True)}."
                ),
            }
        )
        programs.append(program)
        for dataset_name in sorted(signal["source_datasets"]):
            dataset_url = str(DATASETS[dataset_name]["url"])
            sources.append(
                {
                    "source_id": source_id(dataset_url),
                    "institution_id": institution["institution_id"],
                    "institution_name": institution["institution_name"],
                    "program_id": pid,
                    "program_or_professor": mechanical_name,
                    "claim_type": "graduate_field_completion_signal",
                    "exact_claim_supported": (
                        f"Positive first-major graduate completion count reported for CIP {cip} ({title}); "
                        f"this is a discovery signal only."
                    ),
                    "source_title": f"IPEDS {dataset_name} completions by CIP and award level",
                    "publisher": "National Center for Education Statistics",
                    "publication_date": "",
                    "url": dataset_url,
                    "source_type": "official complete data file",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "admissions_cycle": "",
                    "confidence": "high for completion signal; low for current program equivalence",
                    "verification_status": "checksum verified",
                    "access_note": "Filtered to MAJORNUM=1, graduate award levels 7/17/18/19, and CTOTALT>0.",
                }
            )

    for unitid, check in OFFICIAL_PROGRAM_CHECKS.items():
        institution = institution_lookup.get(unitid)
        if institution is None:
            continue
        pid = program_id(str(institution["institution_id"]), "PhD", str(check["program_name"]))
        program = _blank_program()
        program.update(
            {
                "program_id": pid,
                "institution_id": institution["institution_id"],
                "institution_name": institution["institution_name"],
                "country": "United States",
                "program_name": check["program_name"],
                "degree_type": "PhD",
                "department": check["department"],
                "official_program_url": check["url"],
                "thesis_dissertation_requirement": "Dissertation/research doctorate described on official page",
                "direct_from_bachelors_eligible": check.get("direct_from_bachelors", "Unverified"),
                "international_student_eligible": "Unverified",
                "language_of_instruction": "English (official US program page; international language rules not yet verified)",
                "current_program_status": "Active on official program page at access date",
                "preliminary_fit": check["fit"],
                "screening_decision": "advance_to_deep_review",
                "deadline_cycle_status": "Fall 2027 not yet published/verified",
                "funding_status": "Unverified in this mechanical-screening phase",
                "admission_plausibility": "Insufficient evidence",
                "recommendation": "Investigate Further",
                "biggest_risk": "Faculty fit, supervision authority, funding, and Fall 2027 admissions details remain unverified.",
                "unresolved_question": "Which current supervisors match the applicant and are eligible/available to advise Fall 2027 entrants?",
                "verification_status": "Official program page spot-checked; deep review pending",
                "notes": check["claim"],
            }
        )
        programs.append(program)
        program_evidence.append(
            {
                "institution_id": institution["institution_id"],
                "institution_name": institution["institution_name"],
                "program_id": pid,
                "program_name": check["program_name"],
                "claim_type": "program_status_and_structure",
                "exact_claim_supported": check["claim"],
                "official_url": check["url"],
                "date_accessed": ACCESS_DATE,
                "verification_status": "opened official page",
                "notes": "Spot check only; no recruiting inference and no faculty/funding conclusion.",
            }
        )
        sources.append(
            {
                "source_id": source_id(str(check["url"])),
                "institution_id": institution["institution_id"],
                "institution_name": institution["institution_name"],
                "program_id": pid,
                "program_or_professor": check["program_name"],
                "claim_type": "program_status_and_structure",
                "exact_claim_supported": check["claim"],
                "source_title": check["program_name"],
                "publisher": institution["institution_name"],
                "publication_date": "",
                "url": check["url"],
                "source_type": "official program page",
                "official_or_secondary": "official",
                "date_accessed": ACCESS_DATE,
                "admissions_cycle": "Current page; Fall 2027 cycle not verified",
                "confidence": "high for page content; medium for future availability",
                "verification_status": "opened official page",
                "access_note": "No inference about faculty recruiting or funding was made.",
            }
        )

    jurisdiction_counts = Counter(str(row["region"]) for row in institutions)
    state_counts = Counter(universe_hd[str(row["ipeds_unitid"])].get("STABBR", "") for row in institutions)
    institution_status_counts = Counter(str(row["screening_status"]) for row in institutions)
    signal_tier_counts = Counter(
        "primary" if cip in primary else "secondary_review_only" for _, cip in signals
    )
    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "access_date": ACCESS_DATE,
        "method": {
            "universe_filter": (
                "HD2024 CYACTIVE=1 AND DEGGRANT=1, with HLOFFER 7/9 or HLOFFER=8 "
                "plus a positive IC2024 master's/doctoral level indicator"
            ),
            "program_signal_filter": (
                "C2022_A/C2023_A/C2024_A revised member where MAJORNUM=1, "
                "AWLEVEL in (7,17,18,19), configured CIP, and CTOTALT>0"
            ),
            "important_limitations": [
                "IPEDS completions lag current catalogs and omit new or not-yet-completing programs.",
                "CIP assignment does not prove research fit, current program operation, direct entry, funding, or faculty availability.",
                "IPEDS inclusion is not a substitute for institution-level accreditation verification.",
                "Only a small official-page spot check was completed; remaining candidates require deep review.",
            ],
        },
        "datasets": dataset_records,
        "counts": {
            "hd_rows_total": len(hd_rows),
            "ic_rows_total": len(ic_rows),
            "active_graduate_degree_granting_institutions": len(institutions),
            "institutions_with_any_configured_signal": len(signals_by_unitid),
            "institutions_with_primary_signal": len({u for (u, c) in signals if c in primary}),
            "institutions_with_secondary_only_signal": len(
                {u for (u, _) in signals}
                - {u for (u, c) in signals if c in primary}
            ),
            "institutions_without_configured_signal": len(exclusions),
            "mechanical_program_signal_rows": len(signals),
            "official_program_spot_checks": len(program_evidence),
            "program_rows_total": len(programs),
            "source_claim_rows": len(sources),
            "completion_rows_scanned": completion_rows_scanned,
            "qualifying_completion_rows_before_current_universe_join": qualifying_rows,
            "signal_unitids_outside_current_universe": len(signal_rows_outside_current_universe),
        },
        "institution_status_counts": dict(sorted(institution_status_counts.items())),
        "jurisdiction_group_counts": dict(sorted(jurisdiction_counts.items())),
        "state_or_jurisdiction_counts": dict(sorted(state_counts.items())),
        "signal_tier_counts_by_institution_cip": dict(sorted(signal_tier_counts.items())),
        "signal_unitids_outside_current_universe": sorted(signal_rows_outside_current_universe),
        "blocked_sources": [],
    }
    outputs = {
        "institutions": institutions,
        "programs": programs,
        "exclusions": exclusions,
        "sources": sources,
        "program_evidence": program_evidence,
    }
    return outputs, metadata


def run(output_dir: Path, manifest_dir: Path, evidence_dir: Path, cache_dir: Path) -> dict[str, object]:
    outputs, metadata = _build_outputs(cache_dir)
    write_csv(output_dir / "institution_universe.csv", outputs["institutions"], INSTITUTION_COLUMNS)
    write_csv(output_dir / "program_screening.csv", outputs["programs"], PROGRAM_COLUMNS)
    write_csv(output_dir / "exclusion_log.csv", outputs["exclusions"], EXCLUSION_COLUMNS)
    write_csv(output_dir / "source_ledger.csv", outputs["sources"], SOURCE_COLUMNS)
    write_csv(
        evidence_dir / "official_program_verification.csv",
        outputs["program_evidence"],
        (
            "institution_id", "institution_name", "program_id", "program_name", "claim_type",
            "exact_claim_supported", "official_url", "date_accessed", "verification_status", "notes",
        ),
    )
    validation = validate_outputs(output_dir)
    metadata["validation"] = validation
    write_json(manifest_dir / "ipeds_release_manifest.json", {"datasets": metadata["datasets"]})
    write_json(manifest_dir / "coverage.json", metadata)
    return metadata


def _default_paths() -> tuple[Path, Path, Path, Path]:
    root = _repo_root()
    return (
        root / "data" / "processed" / "regions" / "us",
        root / "data" / "manifests" / "us",
        root / "evidence" / "programs" / "us",
        Path(tempfile.gettempdir()) / "graduate_audit_us_ipeds",
    )


def main() -> int:
    default_output, default_manifest, default_evidence, default_cache = _default_paths()
    parser = argparse.ArgumentParser(description="Build the frozen U.S. IPEDS universe and mechanical CIP screen.")
    parser.add_argument("--output-dir", type=Path, default=default_output)
    parser.add_argument("--manifest-dir", type=Path, default=default_manifest)
    parser.add_argument("--evidence-dir", type=Path, default=default_evidence)
    parser.add_argument("--cache-dir", type=Path, default=default_cache)
    args = parser.parse_args()
    metadata = run(args.output_dir, args.manifest_dir, args.evidence_dir, args.cache_dir)
    print(json.dumps({"counts": metadata["counts"], "validation": metadata["validation"]}, indent=2))
    return 0 if metadata["validation"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
