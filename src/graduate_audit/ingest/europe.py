from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import re
import time
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import requests
from bs4 import BeautifulSoup

from graduate_audit.io import write_csv, write_json
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
    program_id,
    slugify,
    source_id,
)

ROOT = Path(__file__).resolve().parents[3]
ACCESS_DATE = "2026-09-09"
ROR_RELEASE = "v2.10 (2026-07-20)"
ROR_RECORD_ID = "21458494"
ROR_RECORD_URL = f"https://zenodo.org/records/{ROR_RECORD_ID}"
ROR_API = "https://api.ror.org/v2/organizations"
USER_AGENT = "GraduateProgramAudit/0.1 (source-backed educational research)"

COUNTRIES = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DK": "Denmark",
    "EE": "Estonia",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LV": "Latvia",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SE": "Sweden",
    "GB": "United Kingdom",
    "NO": "Norway",
    "CH": "Switzerland",
    "IS": "Iceland",
}

# These are national or system-level authorities. They establish where the later
# institution-by-institution recognition check must be performed; ROR itself is
# intentionally never described as an accreditor.
REGISTRY_SOURCES = {
    "Austria": ("Agency for Quality Assurance and Accreditation Austria", "https://www.aq.ac.at/en/"),
    "Belgium": ("Flemish Higher Education Register", "https://www.highereducation.be/"),
    "Bulgaria": ("National Evaluation and Accreditation Agency", "https://www.neaa.government.bg/en/"),
    "Croatia": ("Agency for Science and Higher Education", "https://www.azvo.hr/en/"),
    "Cyprus": ("Cyprus Agency of Quality Assurance and Accreditation in Higher Education", "https://www.dipae.ac.cy/index.php/en/"),
    "Czechia": ("Ministry Register of Higher Education Institutions", "https://regvssp.msmt.cz/registrvssp/"),
    "Denmark": ("Danish Ministry of Higher Education and Science", "https://ufm.dk/en/education/higher-education/danish-universities"),
    "Estonia": ("Estonian Quality Agency for Education", "https://haka.ee/en/"),
    "Finland": ("Finnish Ministry of Education and Culture", "https://okm.fi/en/universities"),
    "France": ("French Ministry of Higher Education open data", "https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-principaux-etablissements-enseignement-superieur/"),
    "Germany": ("Higher Education Compass (German Rectors' Conference)", "https://www.hochschulkompass.de/en/higher-education-institutions.html"),
    "Greece": ("Hellenic Authority for Higher Education", "https://www.ethaae.gr/en/"),
    "Hungary": ("Hungarian Accreditation Committee", "https://www.mab.hu/en/"),
    "Ireland": ("Quality and Qualifications Ireland", "https://www.qqi.ie/what-we-do/the-qualifications-system/irish-register-of-qualifications"),
    "Italy": ("Italian Ministry of Universities and Research", "https://www.mur.gov.it/en"),
    "Latvia": ("AIKA Higher Education Institution List", "https://eplatforma.aika.lv/index.php?r=site%2Fhei-list"),
    "Lithuania": ("Centre for Quality Assessment in Higher Education", "https://www.skvc.lt/default/en/education-in-lithuania/higher-education-institutions"),
    "Luxembourg": ("Ministry of Research and Higher Education", "https://mesr.gouvernement.lu/en/enseignementsuperieur.html"),
    "Malta": ("Malta Further and Higher Education Authority", "https://mfhea.mt/higher-education-licensees/"),
    "Netherlands": ("Accreditation Organisation of the Netherlands and Flanders", "https://www.nvao.net/en/decisions/institutions"),
    "Poland": ("POL-on higher education information system", "https://polon.nauka.gov.pl/"),
    "Portugal": ("Directorate-General for Higher Education", "https://www.dges.gov.pt/en/pesquisa_cursos_instituicoes"),
    "Romania": ("Romanian Agency for Quality Assurance in Higher Education", "https://www.aracis.ro/en/"),
    "Slovakia": ("Slovak Higher Education Portal", "https://www.portalvs.sk/en/"),
    "Slovenia": ("Slovenian Quality Assurance Agency for Higher Education", "https://www.nakvis.si/?lang=en"),
    "Spain": ("Registry of Universities, Centres and Degrees", "https://www.educacion.gob.es/ruct/home"),
    "Sweden": ("Swedish Higher Education Authority", "https://www.uka.se/swedish-higher-education-authority"),
    "United Kingdom": ("GOV.UK recognised bodies and degree-awarding powers", "https://www.gov.uk/check-university-award-degree"),
    "Norway": ("Norwegian Agency for Quality Assurance in Education", "https://www.nokut.no/en/higher-education/"),
    "Switzerland": ("swissuniversities accredited higher education institutions", "https://www.swissuniversities.ch/en/topics/studying/accredited-swiss-higher-education-institutions"),
    "Iceland": ("Government of Iceland universities", "https://www.government.is/topics/education/universities/"),
}


@dataclass(frozen=True)
class ProgramSeed:
    institution: str
    country: str
    name: str
    degree_type: str
    department: str
    url: str
    direct_from_bachelors: str
    language: str
    funding_model: str
    admissions_model: str
    language_url: str = ""


# A bounded positive-signal screen, not a prestige list. Each row is emitted only
# when the official page is retrievable and contains doctoral/research language.
PROGRAM_SEEDS = (
    ProgramSeed("University of Oxford", "United Kingdom", "DPhil in Computer Science", "PhD", "Department of Computer Science", "https://www.ox.ac.uk/admissions/graduate/courses/dphil-computer-science", "Yes; four-year relevant bachelor's route is explicitly listed", "English (primarily English-speaking jurisdiction)", "University scholarships and studentships; deep verification pending", "Program application"),
    ProgramSeed("University of Cambridge", "United Kingdom", "PhD in Computer Science", "PhD", "Department of Computer Science and Technology", "https://www.cst.cam.ac.uk/admissions/phd", "Yes; master's is described as desirable rather than mandatory", "English (primarily English-speaking jurisdiction)", "University/department funding competitions; deep verification pending", "Program application with proposed supervisor"),
    ProgramSeed("University College London", "United Kingdom", "Computer Science MPhil/PhD", "Integrated or structured doctorate", "Department of Computer Science", "https://www.ucl.ac.uk/study/prospective-students/graduate/courses/computer-science-mphilphd", "Potentially; country-specific equivalency requires deep verification", "English (primarily English-speaking jurisdiction)", "Scholarship and project funding; no universal guarantee verified", "Program application; identify proposed supervisor"),
    ProgramSeed("Imperial College London", "United Kingdom", "PhD in Computing", "PhD", "Department of Computing", "https://www.imperial.ac.uk/computing/prospective-students/phd/", "Potentially; detailed credential equivalency requires deep verification", "English (primarily English-speaking jurisdiction)", "Department advertises funded studentships; award not automatic", "Program application"),
    ProgramSeed("ETH Zurich", "Switzerland", "Direct Doctorate in Computer Science", "Direct-entry PhD", "Department of Computer Science", "https://inf.ethz.ch/doctorate/direct-doctorate-computer-science.html", "Yes; explicitly for applicants with a bachelor's in computer science or related field", "English completion supported by official doctorate language policy", "Study scholarship followed by salaried doctoral employment; conditions pending deep verification", "Program application", "https://ethz.ch/students/en/doctorate/doctoral-thesis-examination.html"),
    ProgramSeed("ETH Zurich", "Switzerland", "Doctoral Study Programme in Computer Science", "PhD requiring a master's", "Department of Computer Science", "https://inf.ethz.ch/doctorate/doctoral-study-program.html", "No; official page requires a master's", "English completion supported by official doctorate language policy", "Normally salaried research-assistant employment", "Supervisor/position dependent", "https://ethz.ch/students/en/doctorate/doctoral-thesis-examination.html"),
    ProgramSeed("Saarland University", "Germany", "Saarbrücken Graduate School of Computer Science", "Integrated or structured doctorate", "Department of Computer Science", "https://www.uni-saarland.de/en/future/computerscience.html", "Yes; official page describes a bachelor's-entry route", "English evidence on official program page", "Bachelor's-entry scholarship stated; later funding needs deep verification", "Graduate-school application"),
    ProgramSeed("KU Leuven", "Belgium", "Doctoral Programme in Computer Science", "PhD requiring a master's", "Department of Computer Science", "https://www.kuleuven.be/english/apply/application-instructions/instructions-doctoral", "No; official instructions require a relevant master's or equivalent", "English mastery explicitly required", "Advertised PhD positions are financed; proposal route may require separate funding", "Vacancy or supervisor-initiated application"),
    ProgramSeed("Aalto University", "Finland", "Doctoral Programme in Science — Computer Science", "PhD requiring a master's", "School of Science", "https://www.aalto.fi/en/study-options/aalto-doctoral-programme-in-science-0", "No; relevant master's or equivalent required", "English is an official language of instruction and degree completion", "Salaried position, project funding, or grant; applicant provides funding plan", "Program application with supervising professor"),
    ProgramSeed("University of Helsinki", "Finland", "Doctoral Programme in Science — Computer Science", "PhD requiring a master's", "Faculty of Science", "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes/doctoral-programmes/doctoral-programme-science/admissions-doctoral-studies", "No; second-cycle degree required", "All doctoral programmes can be completed in English", "Study right does not itself imply funding", "Program application with coordinating academic", "https://www.helsinki.fi/en/admissions-and-education/apply-doctoral-programmes"),
    ProgramSeed("KTH Royal Institute of Technology", "Sweden", "Doctoral Programme in Computer Science", "PhD requiring a master's", "School of Electrical Engineering and Computer Science", "https://intra.kth.se/en/eecs/forskarutbildning/doctoral-programmes/computer-science-1.817607", "No; second-cycle qualification required", "English is standard in KTH research environments", "Position-funded; most doctoral students are employees", "Apply to an advertised doctoral position", "https://www.kth.se/en/sci/sci-arbetsmapp-dold/doktorandwebben/faq"),
    ProgramSeed("Technical University of Denmark", "Denmark", "PhD Programme — DTU Compute", "PhD requiring a master's", "Department of Applied Mathematics and Computer Science", "https://www.dtu.dk/english/education/phd/intro", "No; standard route requires master's-equivalent preparation", "English delivery plausible; explicit completion-language evidence unresolved", "Position-funded vacancies predominate", "Apply to advertised vacancy"),
    ProgramSeed("University of Tartu", "Estonia", "PhD in Information Technology — Computer Science", "PhD requiring a master's", "Institute of Computer Science", "https://ut.ee/en/curriculum/computer-science", "No; master's-equivalent eligibility requires deep verification", "English proficiency requirement shown on official curriculum page", "Position/study-place funding requires vacancy-level verification", "Program or position application"),
)

SEED_ROR_IDS = {
    "University of Oxford": "052gg0110",
    "University of Cambridge": "013meh722",
    "University College London": "02jx3x895",
    "Imperial College London": "041kmwe10",
    "ETH Zurich": "05a28rw58",
    "Saarland University": "01jdpyv68",
    "KU Leuven": "05f950310",
    "Aalto University": "020hwjq30",
    "University of Helsinki": "040af2s02",
    "KTH Royal Institute of Technology": "026vcq606",
    "Technical University of Denmark": "04qtj9h94",
    "University of Tartu": "03z77qz90",
}

NON_GRADUATE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bprimary school\b",
        r"\bsecondary school\b",
        r"\bhigh school\b",
        r"\bgrammar school\b",
        r"\bmiddle school\b",
        r"\bschool district\b",
        r"\bsixth form\b",
    )
)


def _get_json(url: str, *, timeout: int = 45, attempts: int = 4) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed after {attempts} attempts: {url}: {last_error}")


def _country_page(code: str, page: int) -> list[dict[str, Any]]:
    url = (
        f"{ROR_API}?filter=country.country_code:{code},types:education,status:active"
        f"&page={page}"
    )
    return _get_json(url)["items"]


def load_ror_api() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    first_pages: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(
                _get_json,
                f"{ROR_API}?filter=country.country_code:{code},types:education,status:active&page=1",
            ): code
            for code in COUNTRIES
        }
        for future in concurrent.futures.as_completed(futures):
            first_pages[futures[future]] = future.result()

    items: list[dict[str, Any]] = []
    tasks: list[tuple[str, int]] = []
    country_counts: dict[str, int] = {}
    for code, payload in first_pages.items():
        count = int(payload["number_of_results"])
        country_counts[COUNTRIES[code]] = count
        items.extend(payload["items"])
        tasks.extend((code, page) for page in range(2, math.ceil(count / 20) + 1))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(_country_page, code, page): (code, page) for code, page in tasks}
        for future in concurrent.futures.as_completed(futures):
            items.extend(future.result())

    # Filter-only aggregate paging is an explicitly documented API fallback: ROR
    # warns it may contain duplicates and omissions. Pull exact degree-awarding
    # seed records separately so a missing aggregate page can never trigger a
    # fuzzy join to a subsidiary.
    existing_ids = {record["id"].rstrip("/").rsplit("/", 1)[-1] for record in items}
    required_ids = sorted(set(SEED_ROR_IDS.values()) - existing_ids)
    if required_ids:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            exact = executor.map(lambda rid: _get_json(f"{ROR_API}/{rid}"), required_ids)
            items.extend(exact)

    return items, {
        "transport": "ROR API v2 country/type/status filtered snapshot",
        "endpoint": ROR_API,
        "country_counts_reported": country_counts,
        "api_completeness_warning": "ROR documents that filter-only aggregate paging can contain duplicates and omissions; use --bulk-zip for a complete release.",
        "exact_seed_records_added": required_ids,
    }


def load_ror_bulk(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with zipfile.ZipFile(path) as archive:
        candidates = [name for name in archive.namelist() if name.endswith(".json") and "schema" not in name.lower()]
        if not candidates:
            raise ValueError(f"no ROR JSON data file found in {path}")
        with archive.open(sorted(candidates)[0]) as handle:
            payload = json.load(handle)
    records = payload if isinstance(payload, list) else payload.get("items", payload.get("data", []))
    selected = []
    wanted_codes = set(COUNTRIES)
    for record in records:
        location = (record.get("locations") or [{}])[0].get("geonames_details", {})
        if (
            location.get("country_code") in wanted_codes
            and record.get("status") == "active"
            and "education" in record.get("types", [])
        ):
            selected.append(record)
    return selected, {
        "transport": "ROR v2 bulk JSON",
        "path": str(path),
        "sha256": digest,
        "member": sorted(candidates)[0],
    }


def _display_name(record: dict[str, Any]) -> str:
    names = record.get("names", [])
    for name in names:
        if "ror_display" in name.get("types", []):
            return name.get("value", "")
    return names[0].get("value", "") if names else ""


def _aliases(record: dict[str, Any]) -> list[str]:
    display = _display_name(record)
    return sorted({n.get("value", "") for n in record.get("names", []) if n.get("value") and n.get("value") != display})


def _website(record: dict[str, Any]) -> str:
    for link in record.get("links", []):
        if link.get("type") == "website":
            return link.get("value", "")
    return ""


def _country(record: dict[str, Any]) -> str:
    location = (record.get("locations") or [{}])[0].get("geonames_details", {})
    return COUNTRIES.get(location.get("country_code", ""), location.get("country_name", ""))


def _ror_suffix(record: dict[str, Any]) -> str:
    return record["id"].rstrip("/").rsplit("/", 1)[-1]


def _obviously_non_graduate(name: str) -> bool:
    return any(pattern.search(name) for pattern in NON_GRADUATE_PATTERNS)


def _fetch_page(url: str, timeout: int = 35) -> dict[str, Any]:
    checked_at = f"{ACCESS_DATE}T00:00:00Z"
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "en"},
                timeout=timeout,
                allow_redirects=True,
            )
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(attempt + 1)
    else:
        return {"url": url, "ok": False, "checked_at": checked_at, "error": str(last_error)}
    try:
        content_type = response.headers.get("content-type", "")
        if "html" not in content_type.lower() and not response.url.lower().endswith(".html"):
            return {
                "url": url,
                "final_url": response.url,
                "status_code": response.status_code,
                "ok": False,
                "checked_at": checked_at,
                "error": f"unsupported content type: {content_type}",
            }
        raw = response.content[:1_500_000]
        # html.parser is part of the standard library, so the regional pull also
        # runs in the base workspace before optional lxml wheels are installed.
        soup = BeautifulSoup(raw, "html.parser")
        for element in soup(["script", "style", "noscript", "svg"]):
            element.decompose()
        text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        lowered = text.lower()
        anchors = [lowered.find(word) for word in ("computer science", "doctoral", "phd", "dphil", "research")]
        start = max(0, min((position for position in anchors if position >= 0), default=0) - 160)
        excerpt = text[start : start + 1_200]
        return {
            "url": url,
            "final_url": response.url,
            "status_code": response.status_code,
            "ok": True,
            "checked_at": checked_at,
            "content_sha256": hashlib.sha256(raw).hexdigest(),
            "title": title,
            "excerpt": excerpt,
            "signals": {
                "doctoral": any(word in lowered for word in ("doctoral", "phd", "dphil", "doctorate")),
                "research": "research" in lowered,
                "computer_science": any(word in lowered for word in ("computer science", "computing", "informatics")),
                "english": "english" in lowered,
            },
        }
    except Exception as exc:
        return {"url": url, "ok": False, "checked_at": checked_at, "error": str(exc)}


def _match_seed(seed: ProgramSeed, records: list[dict[str, Any]]) -> dict[str, Any] | None:
    expected_id = SEED_ROR_IDS[seed.institution]
    for record in records:
        if _ror_suffix(record) == expected_id:
            if _country(record) != seed.country:
                raise ValueError(f"seed {seed.institution} expected {seed.country}, got {_country(record)}")
            return record
    return None


def _host(url: str) -> str:
    from urllib.parse import urlsplit

    return (urlsplit(url).hostname or "").lower().removeprefix("www.")


def _validate_seed_attachment(seed: ProgramSeed, record: dict[str, Any], final_url: str) -> None:
    expected_id = SEED_ROR_IDS[seed.institution]
    if _ror_suffix(record) != expected_id or _display_name(record) != seed.institution:
        raise ValueError(
            f"program seed attachment mismatch: {seed.institution} must attach to ror:{expected_id}, "
            f"not ror:{_ror_suffix(record)} / {_display_name(record)}"
        )
    page_host = _host(final_url)
    allowed_domains = {domain.lower().removeprefix("www.") for domain in record.get("domains", [])}
    allowed_domains.add(_host(_website(record)))
    allowed_domains.discard("")
    if allowed_domains and not any(page_host == domain or page_host.endswith(f".{domain}") for domain in allowed_domains):
        raise ValueError(
            f"official program domain {page_host} is not under degree-awarding institution domains "
            f"{sorted(allowed_domains)} for {seed.institution}"
        )


def _blank_program() -> dict[str, Any]:
    return {column: "" for column in PROGRAM_COLUMNS}


def _blank_source() -> dict[str, Any]:
    return {column: "" for column in SOURCE_COLUMNS}


def build_outputs(
    records: list[dict[str, Any]],
    *,
    transport: dict[str, Any],
    output_dir: Path,
    manifest_dir: Path,
    evidence_dir: Path,
) -> dict[str, Any]:
    raw_record_count = len(records)
    deduped = {record["id"]: record for record in records}
    records = sorted(deduped.values(), key=lambda item: (_country(item), _display_name(item).casefold()))

    page_urls = sorted({seed.url for seed in PROGRAM_SEEDS} | {seed.language_url for seed in PROGRAM_SEEDS if seed.language_url})
    registry_urls = sorted({url for _, url in REGISTRY_SOURCES.values()})
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        page_results = dict(zip(page_urls + registry_urls, executor.map(_fetch_page, page_urls + registry_urls)))

    program_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    program_institutions: set[str] = set()
    unresolved_seeds: list[dict[str, str]] = []

    for seed in PROGRAM_SEEDS:
        record = _match_seed(seed, records)
        page = page_results[seed.url]
        language_page = page_results.get(seed.language_url) if seed.language_url else None
        evidence = {
            "seed": seed.__dict__,
            "program_page": page,
            "language_page": language_page,
            "method": "bounded official-page positive-signal screen",
        }
        evidence_rows.append(evidence)
        if record is None:
            unresolved_seeds.append({"institution": seed.institution, "program": seed.name, "reason": "no unambiguous ROR match"})
            continue
        if not page.get("ok") or not page.get("signals", {}).get("doctoral") or not page.get("signals", {}).get("research"):
            unresolved_seeds.append({"institution": seed.institution, "program": seed.name, "reason": page.get("error", "required page signals absent")})
            continue

        _validate_seed_attachment(seed, record, page.get("final_url", seed.url))

        institution_id = f"ror:{_ror_suffix(record)}"
        pid = program_id(institution_id, seed.degree_type, seed.name)
        program_institutions.add(institution_id)
        language_verified = seed.country in {"United Kingdom", "Ireland", "Malta"} or (
            "English" in seed.language and (page.get("signals", {}).get("english") or (language_page and language_page.get("ok")))
        )
        row = _blank_program()
        row.update(
            {
                "program_id": pid,
                "institution_id": institution_id,
                "institution_name": _display_name(record),
                "country": seed.country,
                "program_name": seed.name,
                "degree_type": seed.degree_type,
                "department": seed.department,
                "official_program_url": page.get("final_url", seed.url),
                "thesis_dissertation_requirement": "Doctoral dissertation/thesis indicated; exact rules pending deep verification",
                "research_credit_requirement": "See official programme page; exact credit total pending deep verification",
                "research_groups_labs": "Computer science/informatics research signal verified; group-level fit pending",
                "direct_from_bachelors_eligible": seed.direct_from_bachelors,
                "international_student_eligible": "Plausible; country-specific eligibility and visa rules pending deep verification",
                "language_of_instruction": seed.language if language_verified else "English completion evidence unresolved",
                "current_program_status": "Official page accessible on freeze date",
                "preliminary_fit": "Yes — broad computer science/software/AI/security research scope",
                "screening_decision": "preliminary_fit" if language_verified else "investigate_further",
                "exclusion_reason": "" if language_verified else "Explicit official English-completion evidence not yet verified",
                "admissions_model": seed.admissions_model,
                "faculty_contact_expectation": "Pending faculty-level verification",
                "funding_model": seed.funding_model,
                "funding_status": "Preliminary only; no individual award or position verified",
                "phd_funding": seed.funding_model,
                "admission_plausibility": "Insufficient evidence",
                "recommendation": "Investigate Further",
                "biggest_risk": "No verified supervisor match or Fall 2027 vacancy/funding decision",
                "unresolved_question": "Does a matching supervisor or funded position accept Fall 2027 applicants?",
                "single_professor_dependency": "Unknown",
                "verification_status": "Official program page checked; deep admissions/faculty/funding review pending",
                "notes": "Mechanical regional screen only; not a final retention decision.",
            }
        )
        program_rows.append(row)

        claim = _blank_source()
        claim.update(
            {
                "source_id": source_id(page.get("final_url", seed.url)),
                "institution_id": institution_id,
                "institution_name": _display_name(record),
                "program_id": pid,
                "program_or_professor": seed.name,
                "claim_type": "program status and degree structure",
                "exact_claim_supported": f"Official page identifies {seed.name} as a doctoral research route; classified as {seed.degree_type} for mechanical screening.",
                "source_title": page.get("title", seed.name),
                "publisher": _display_name(record),
                "url": page.get("final_url", seed.url),
                "source_type": "official program page",
                "official_or_secondary": "official",
                "date_accessed": ACCESS_DATE,
                "admissions_cycle": "Current page at 2026-09-09; Fall 2027 details not assumed",
                "confidence": "High for existence; preliminary for eligibility/funding",
                "verification_status": "opened",
                "access_note": f"HTTP {page.get('status_code', '')}; SHA-256 captured in program evidence",
            }
        )
        source_rows.append(claim)
        if seed.language_url and language_page and language_page.get("ok"):
            language_claim = _blank_source()
            language_claim.update(
                {
                    "source_id": source_id(language_page.get("final_url", seed.language_url)),
                    "institution_id": institution_id,
                    "institution_name": _display_name(record),
                    "program_id": pid,
                    "program_or_professor": seed.name,
                    "claim_type": "language",
                    "exact_claim_supported": seed.language,
                    "source_title": language_page.get("title", "Official language guidance"),
                    "publisher": _display_name(record),
                    "url": language_page.get("final_url", seed.language_url),
                    "source_type": "official policy or admissions page",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "confidence": "High",
                    "verification_status": "opened",
                    "access_note": f"HTTP {language_page.get('status_code', '')}; SHA-256 captured in program evidence",
                }
            )
            source_rows.append(language_claim)

    institution_rows: list[dict[str, Any]] = []
    for record in records:
        name = _display_name(record)
        country = _country(record)
        institution_id = f"ror:{_ror_suffix(record)}"
        obvious_non_graduate = _obviously_non_graduate(name)
        if obvious_non_graduate:
            screening_status = "no_graduate_degree_authority"
            exclusion_reason = "Name explicitly identifies a primary/secondary-school entity; no graduate-degree signal in ROR metadata"
            graduate_authority = "No graduate-degree signal; excluded by narrow non-tertiary name rule"
        elif institution_id in program_institutions:
            screening_status = "preliminary_fit"
            exclusion_reason = ""
            graduate_authority = "Positive evidence from an official doctoral/research programme page"
        else:
            screening_status = "program_screened_out"
            exclusion_reason = "Outside the bounded positive-signal official-program seed screen; exhaustive catalog verification remains required"
            graduate_authority = "Unverified — institution-level national-registry cross-check required"

        institution_rows.append(
            {
                "institution_id": institution_id,
                "institution_name": name,
                "alternate_names": " | ".join(_aliases(record)),
                "country": country,
                "region": "Europe",
                "institution_type": " | ".join(record.get("types", [])),
                "recognition_status": "ROR v2 active education organization; ROR is not an accreditation authority",
                "active_status": record.get("status", ""),
                "official_website": _website(record),
                "source_database": "ROR v2; national recognition source directory",
                "dataset_release": ROR_RELEASE,
                "access_date": ACCESS_DATE,
                "graduate_degree_authority": graduate_authority,
                "relevant_graduate_field_signal": "Official doctoral computer-science route found" if institution_id in program_institutions else "No positive official-program seed signal; not a negative finding",
                "screening_status": screening_status,
                "exclusion_reason": exclusion_reason,
                "ror_id": record["id"],
                "ipeds_unitid": "",
                "eter_id": "",
                "dli_number": "",
                "manual_verification": "Required" if not obvious_non_graduate else "Rule reviewed",
                "notes": "EHESO/ETER crosswalk unavailable because the HEI API required authorization at freeze time.",
            }
        )
        ror_claim = _blank_source()
        ror_claim.update(
            {
                "source_id": source_id(ROR_RECORD_URL),
                "institution_id": institution_id,
                "institution_name": name,
                "claim_type": "institution index and active status",
                "exact_claim_supported": "ROR v2 lists this record as an active organization with education type; this does not by itself prove degree-awarding authority.",
                "source_title": "ROR Data v2.10",
                "publisher": "Research Organization Registry",
                "publication_date": "2026-07-20",
                "url": ROR_RECORD_URL,
                "source_type": "registry data dump / API snapshot",
                "official_or_secondary": "secondary discovery registry",
                "date_accessed": ACCESS_DATE,
                "confidence": "High for ROR metadata; not applicable to accreditation",
                "verification_status": "indexed",
                "access_note": transport["transport"],
            }
        )
        source_rows.append(ror_claim)
        if institution_id not in program_institutions:
            exclusion_rows.append(
                {
                    "institution_id": institution_id,
                    "institution_name": name,
                    "country": country,
                    "program_id": "",
                    "program_name": "",
                    "stage_of_exclusion": "institution universe" if obvious_non_graduate else "bounded mechanical program screen",
                    "primary_exclusion_reason": exclusion_reason,
                    "supporting_evidence": (
                        f"ROR display name: {name}; active education-type metadata contains no graduate-degree indicator."
                        if obvious_non_graduate
                        else "No exact official computer-science doctoral page was included in the bounded positive-signal seed set. This is a workflow disposition, not evidence that no relevant program exists."
                    ),
                    "source_url": _website(record) or record["id"],
                    "confidence": "High for explicit non-tertiary name" if obvious_non_graduate else "Low — exhaustive catalog review required",
                    "manual_verification": "Required",
                    "date_checked": ACCESS_DATE,
                }
            )

    registry_checks: list[dict[str, Any]] = []
    for country, (publisher, url) in REGISTRY_SOURCES.items():
        page = page_results[url]
        registry_checks.append({"country": country, "authority": publisher, **page})
        row = _blank_source()
        row.update(
            {
                "source_id": source_id(url),
                "program_or_professor": country,
                "claim_type": "national recognition authority",
                "exact_claim_supported": "Authority/source designated for institution-level recognition and degree-authority verification; no blanket recognition claim is made.",
                "source_title": page.get("title", publisher),
                "publisher": publisher,
                "url": page.get("final_url", url),
                "source_type": "national registry or quality-assurance authority",
                "official_or_secondary": "official/system authority",
                "date_accessed": ACCESS_DATE,
                "confidence": "High for source designation; institution-level check pending",
                "verification_status": "opened" if page.get("ok") else "blocked",
                "access_note": f"HTTP {page.get('status_code', '')}" if page.get("ok") else page.get("error", "blocked"),
            }
        )
        source_rows.append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "institution_universe.csv", institution_rows, INSTITUTION_COLUMNS)
    write_csv(output_dir / "program_screening.csv", program_rows, PROGRAM_COLUMNS)
    write_csv(output_dir / "exclusion_log.csv", exclusion_rows, EXCLUSION_COLUMNS)
    write_csv(output_dir / "source_ledger.csv", source_rows, SOURCE_COLUMNS)
    write_json(evidence_dir / "official_program_page_checks.json", evidence_rows)
    write_json(manifest_dir / "national_registry_checks.json", registry_checks)

    status_counts = Counter(row["screening_status"] for row in institution_rows)
    country_counts = Counter(row["country"] for row in institution_rows)
    program_country_counts = Counter(row["country"] for row in program_rows)
    blocked_registry = [row for row in registry_checks if not row.get("ok")]
    blocked_programs = [row for row in evidence_rows if not row["program_page"].get("ok")]
    coverage = {
        "generated_at": f"{ACCESS_DATE}T00:00:00Z",
        "scope_country_count": len(COUNTRIES),
        "institution_count": len(institution_rows),
        "program_candidate_count": len(program_rows),
        "exclusion_count": len(exclusion_rows),
        "source_claim_count": len(source_rows),
        "raw_api_record_rows": raw_record_count,
        "duplicate_ror_records_removed": raw_record_count - len(deduped),
        "reported_filtered_record_count": sum(transport.get("country_counts_reported", {}).values()),
        "api_unique_coverage_ratio": round(len(institution_rows) / sum(transport.get("country_counts_reported", {}).values()), 6) if transport.get("country_counts_reported") else 1.0,
        "institution_counts_by_country": dict(sorted(country_counts.items())),
        "program_counts_by_country": dict(sorted(program_country_counts.items())),
        "institution_status_counts": dict(sorted(status_counts.items())),
        "program_seed_count": len(PROGRAM_SEEDS),
        "unresolved_program_seeds": unresolved_seeds,
        "blocked_registry_source_count": len(blocked_registry),
        "blocked_program_page_count": len(blocked_programs),
        "transport": transport,
        "limitations": [
            "ROR education type is a discovery universe, not proof of recognition or graduate degree authority.",
            "EHESO/ETER HEI query returned HTTP 401 without an API key; ETER IDs and doctoral-award fields are absent.",
            "National authority URLs were checked, but institution-level national-registry matching remains incomplete.",
            "The API fallback is incomplete by design: ROR warns that filter-only aggregate paging can contain duplicates and omissions. The published bulk ZIP is required for a complete ROR universe.",
            "Program discovery is a bounded positive-signal seed screen, not an exhaustive crawl of all official catalogues.",
            "No program is finally retained: faculty supervision, Fall 2027 recruitment, eligibility, and funding require later phases.",
            "Absence from program_screening.csv must not be interpreted as absence of a relevant program.",
        ],
    }
    write_json(output_dir / "coverage.json", coverage)
    write_json(
        manifest_dir / "ror_snapshot.json",
        {
            "dataset": "Research Organization Registry",
            "release": ROR_RELEASE,
            "record_id": ROR_RECORD_ID,
            "record_url": ROR_RECORD_URL,
            "published": "2026-07-20",
            "bulk_zip_name": "v2.10-2026-07-20-ror-data.zip",
            "published_md5": "ad7e842ce1b296fc066a0babe86ec48e",
            "access_date": ACCESS_DATE,
            **transport,
        },
    )
    write_json(
        manifest_dir / "blocked_sources.json",
        {
            "access_date": ACCESS_DATE,
            "sources": [
                {
                    "name": "EHESO/ETER HEI API",
                    "url": "https://observatory.eter-project.com/api/v1/layer",
                    "status": "blocked",
                    "http_status": 401,
                    "impact": "No ETER identifiers or institution-level degree/doctoral-award fields could be cross-walked.",
                },
                *[
                    {"name": row["authority"], "url": row["url"], "status": "blocked", "error": row.get("error", "")}
                    for row in blocked_registry
                ],
                *[
                    {"name": row["seed"]["name"], "url": row["seed"]["url"], "status": "blocked", "error": row["program_page"].get("error", "")}
                    for row in blocked_programs
                ],
            ],
        },
    )
    return coverage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the European ROR discovery universe and bounded official-program screen")
    parser.add_argument("--bulk-zip", type=Path, help="Optional downloaded ROR v2 bulk ZIP; API snapshot is used when omitted")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data" / "processed" / "regions" / "europe")
    parser.add_argument("--manifest-dir", type=Path, default=ROOT / "data" / "manifests" / "europe")
    parser.add_argument("--evidence-dir", type=Path, default=ROOT / "evidence" / "programs" / "europe")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    if args.bulk_zip:
        records, transport = load_ror_bulk(args.bulk_zip)
    else:
        records, transport = load_ror_api()
    coverage = build_outputs(
        records,
        transport=transport,
        output_dir=args.output_dir,
        manifest_dir=args.manifest_dir,
        evidence_dir=args.evidence_dir,
    )
    print(json.dumps(coverage, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
