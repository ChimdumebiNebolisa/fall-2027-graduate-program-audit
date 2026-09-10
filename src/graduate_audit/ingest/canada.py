from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from graduate_audit.io import write_csv, write_json
from graduate_audit.schema import (
    EXCLUSION_COLUMNS,
    INSTITUTION_COLUMNS,
    PROGRAM_COLUMNS,
    SOURCE_COLUMNS,
    program_id,
    source_id,
)

ROOT = Path(__file__).resolve().parents[3]
ACCESS_DATE = "2026-09-09"
IRCC_URL = (
    "https://www.canada.ca/en/immigration-refugees-citizenship/services/"
    "study-canada/study-permit/prepare/designated-learning-institutions-list.html"
)
CICIC_URL = "https://www.cicic.ca/869/results.canada?t=1&search="
CICIC_DIRECTORY_URL = (
    "https://www.cicic.ca/871/read_more_information_about_the_directory_of_"
    "educational_institutions_in_canada.canada"
)
ROR_API = "https://api.ror.org/v2/organizations"
ROR_DOCS = "https://ror.readme.io/docs/rest-api"
USER_AGENT = "GraduateProgramAudit/0.1 (source-backed educational research)"


@dataclass(frozen=True)
class ProgramSeed:
    institution: str
    name: str
    department: str
    url: str
    language: str = "English"
    direct_entry: str = "Yes — research master's accepts a relevant bachelor's degree; detailed equivalency pending"
    thesis: str = "Thesis or research dissertation required"


# This is a positive-signal mechanical screen. A seed is emitted only after the
# official page can be opened and research/thesis language is found in its body.
# The later fit phase remains responsible for faculty, admissions and funding.
PROGRAM_SEEDS = (
    ProgramSeed("University of Alberta", "MSc in Computing Science (thesis)", "Department of Computing Science", "https://www.ualberta.ca/en/computing-science/graduate-studies/programs-and-admissions/index.html"),
    ProgramSeed("University of Calgary", "MSc in Computer Science (thesis)", "Department of Computer Science", "https://science.ucalgary.ca/computer-science/future-students/graduate/thesis-programs"),
    ProgramSeed("University of Lethbridge", "MSc in Computer Science", "Department of Mathematics and Computer Science", "https://www.ulethbridge.ca/future-student/graduate-studies/master-science/computer-science"),
    ProgramSeed("Simon Fraser University", "MSc in Computing Science", "School of Computing Science", "https://www.sfu.ca/fas/computing/future-students/graduate-students/programs/msc.html"),
    ProgramSeed("University of British Columbia", "MSc in Computer Science", "Department of Computer Science", "https://www.cs.ubc.ca/students/grad/admissions"),
    ProgramSeed("University of Northern British Columbia", "MSc in Computer Science", "Department of Computer Science", "https://www.unbc.ca/calendar/graduate/computer-science"),
    ProgramSeed("University of Victoria", "MSc in Computer Science", "Department of Computer Science", "https://www.uvic.ca/ecs/computerscience/programs/msc/index.php"),
    ProgramSeed("University of Manitoba", "MSc in Computer Science", "Department of Computer Science", "https://umanitoba.ca/graduate-studies/admissions/programs-of-study/computer-science-msc"),
    ProgramSeed("University of Winnipeg", "MSc in Applied Computer Science and Society", "Department of Applied Computer Science", "https://www.uwinnipeg.ca/graduate-studies/graduate-programs/applied-computer-science.html"),
    ProgramSeed("University of New Brunswick", "MCS in Computer Science (thesis)", "Faculty of Computer Science", "https://www.unb.ca/gradstudies/programs/computer-science.html"),
    ProgramSeed("Memorial University of Newfoundland", "MSc in Computer Science (thesis)", "Department of Computer Science", "https://www.mun.ca/become/graduate/programs-and-courses/computer-science/"),
    ProgramSeed("Acadia University", "MSc in Computer Science (thesis)", "Jodrey School of Computer Science", "https://www2.acadiau.ca/academics/graduate/computer-science.html"),
    ProgramSeed("Dalhousie University", "PhD in Computer Science", "Faculty of Computer Science", "https://www.dal.ca/study/programs/graduate-professional/computer-science-phd.html", direct_entry="No determination — master's expectation must be checked in the deep-review phase"),
    ProgramSeed("Brock University", "MSc in Computer Science", "Department of Computer Science", "https://brocku.ca/programs/graduate/msc-cosc/"),
    ProgramSeed("Carleton University", "MCS in Computer Science (thesis)", "School of Computer Science", "https://graduate.carleton.ca/program/computer-science-masters-programs/"),
    ProgramSeed("Lakehead University", "MSc in Computer Science (thesis)", "Department of Computer Science", "https://www.lakeheadu.ca/programs/graduate/programs/masters/computer-science"),
    ProgramSeed("Laurentian University", "MSc in Computational Sciences", "School of Natural Sciences", "https://laurentian.ca/academics/program/computational-sciences-msc"),
    ProgramSeed("McMaster University", "MSc in Computer Science", "Department of Computing and Software", "https://www.eng.mcmaster.ca/cas/degree-options/computer-science-msc/"),
    ProgramSeed("Ontario Tech University", "MSc in Computer Science", "Faculty of Science", "https://science.ontariotechu.ca/graduate/computer-science/index.php"),
    ProgramSeed("Queen's University", "MSc in Computing", "School of Computing", "https://www.cs.queensu.ca/graduate/msc/"),
    ProgramSeed("Toronto Metropolitan University", "MSc in Computer Science", "Department of Computer Science", "https://www.torontomu.ca/graduate/programs/computer-science/"),
    ProgramSeed("University of Ottawa", "MSc in Computer Science", "School of Electrical Engineering and Computer Science", "https://www.uottawa.ca/faculty-engineering/graduate-studies/programs/computer-science"),
    ProgramSeed("University of Guelph", "MSc in Computer Science", "School of Computer Science", "https://www.uoguelph.ca/programs/msc-computer-science"),
    ProgramSeed("University of Toronto", "MSc in Computer Science", "Department of Computer Science", "https://web.cs.toronto.edu/graduate/msc"),
    ProgramSeed("University of Waterloo", "MMath in Computer Science (thesis)", "Cheriton School of Computer Science", "https://uwaterloo.ca/computer-science/future-graduate-students/programs"),
    ProgramSeed("University of Windsor", "MSc in Computer Science", "School of Computer Science", "https://www.uwindsor.ca/graduate-studies/494/computer-science"),
    ProgramSeed("Western University", "MSc in Computer Science (thesis)", "Department of Computer Science", "https://www.csd.uwo.ca/graduate/current/degree_requirements.html"),
    ProgramSeed("Wilfrid Laurier University", "Master of Applied Computing (thesis stream)", "Department of Computer Science and Physics", "https://students.wlu.ca/programs/science/computer-science-and-physics/graduate-students/program-requirements/index.html"),
    ProgramSeed("University of Prince Edward Island", "MSc in Mathematical and Computational Sciences", "Faculty of Science", "https://www.upei.ca/programs/master-science-mathematical-and-computational-sciences"),
    ProgramSeed("University of Saskatchewan", "MSc in Computer Science", "Department of Computer Science", "https://grad.usask.ca/programs/computer-science.php"),
    ProgramSeed("Concordia University", "Master of Computer Science (thesis)", "Department of Computer Science and Software Engineering", "https://www.concordia.ca/academics/graduate/computer-science-mcompsc.html"),
    ProgramSeed("McGill University", "MSc in Computer Science (thesis)", "School of Computer Science", "https://coursecatalogue.mcgill.ca/en/graduate/science/computer-science/computer-science-thesis-msc/computer-science-thesis-msc.pdf"),
    ProgramSeed("Université Laval", "Maîtrise en informatique avec mémoire", "Département d'informatique et de génie logiciel", "https://www.ulaval.ca/etudes/programmes/maitrise-en-informatique-avec-memoire", language="French; English completion not established"),
    ProgramSeed("Université de Montréal", "Maîtrise en informatique", "Département d'informatique et de recherche opérationnelle", "https://admission.umontreal.ca/programmes/maitrise-en-informatique/", language="French; English completion not established"),
    ProgramSeed("Université de Sherbrooke", "Maîtrise en informatique", "Département d'informatique", "https://www.usherbrooke.ca/admission/programme/652/maitrise-en-informatique", language="French; English completion not established"),
    ProgramSeed("Université du Québec à Chicoutimi", "Maîtrise en informatique", "Département d'informatique et de mathématique", "https://programmes.uqac.ca/1641", language="French; English completion not established"),
    ProgramSeed("Université du Québec à Montréal", "Maîtrise en informatique", "Département d'informatique", "https://etudier.uqam.ca/programme?code=2014", language="French; English completion not established"),
    ProgramSeed("Institut national de la recherche scientifique", "Maîtrise en télécommunications", "Centre Énergie Matériaux Télécommunications", "https://inrs.ca/les-etudes/programmes-d-etudes/repertoire-des-programmes-d-etudes/maitrise-en-telecommunications-3404/", language="French"),
    ProgramSeed("École Polytechnique de Montréal", "Maîtrise recherche en génie informatique", "Département de génie informatique et génie logiciel", "https://www.polymtl.ca/programmes/programmes/maitrise-recherche-en-genie-informatique", language="French; English completion not established"),
    ProgramSeed("École de technologie supérieure", "Maîtrise en génie des technologies de l'information", "Département de génie logiciel et des TI", "https://www.etsmtl.ca/programmes-formations/maitrise-genie-technologies-information", language="French and English for the research MScA route"),
)

SPECIALTY_EXCLUSIONS = {
    "Alberta University of the Arts": "Official institutional scope is art and design; no computing research graduate degree identified.",
    "Emily Carr University of Art and Design": "Official institutional scope is art and design; no computing research graduate degree identified.",
    "Atlantic School of Theology": "Official institutional scope is theology; no computing research graduate degree identified.",
    "NSCAD University": "Official institutional scope is art and design; no computing research graduate degree identified.",
    "Canadian Forces College": "Official institutional scope is professional military education; no open computing research graduate route identified.",
    "OCAD University": "Official institutional scope is art and design; no computing research graduate degree identified in the mechanical title screen.",
    "The Michener Institute for Applied Health Sciences": "Official institutional scope is applied health sciences; no computing research graduate degree identified.",
    "Université de Hearst": "No computing research graduate degree identified in the institution's official program inventory.",
    "Conservatoire d'art dramatique de Québec": "Official institutional scope is dramatic arts; no computing research graduate degree identified.",
    "Conservatoire de musique de Gatineau": "Official institutional scope is music; no computing research graduate degree identified.",
    "Conservatoire de musique de Montréal": "Official institutional scope is music; no computing research graduate degree identified.",
    "Conservatoire de musique de Rimouski": "Official institutional scope is music; no computing research graduate degree identified.",
    "Conservatoire de musique de Trois-Rivières": "Official institutional scope is music; no computing research graduate degree identified.",
    "Conservatoire de musique de Val-d'Or": "Official institutional scope is music; no computing research graduate degree identified.",
    "Faculté de Théologie Évangélique de l’Université Acadia": "Official institutional scope is theology; no computing research graduate degree identified.",
    "École des Hautes Études Commerciales de Montréal": "Official institutional scope is management; no computing research thesis degree identified in the mechanical screen.",
    "École nationale d'administration publique": "Official institutional scope is public administration; no computing research graduate degree identified.",
    "College of Emmanuel and St Chad": "Official institutional scope is theology; no computing research graduate degree identified.",
    "Horizon College and Seminary Inc.": "Official institutional scope is theology; no computing research graduate degree identified.",
    "Lutheran Theological Seminary": "Official institutional scope is theology; no computing research graduate degree identified.",
    "St. Andrew’s College": "Official institutional scope is theology; no computing research graduate degree identified.",
}

PREFERRED_NAMES = {
    "O19305471522": "University of Waterloo",
    "O19332746152": "University of Toronto",
    "O19395164307": "Wilfrid Laurier University",
}

NAME_ALIASES = {
    "Simon Fraser University (SFU)": "Simon Fraser University",
    "University of British Columbia (UBC)": "University of British Columbia",
    "Toronto Metropolitan University (TMU)": "Toronto Metropolitan University",
    "Université d’Ottawa/University of Ottawa": "University of Ottawa",
    "University of Regina, including Campion College, First Nations University of Canada and Luther College": "University of Regina",
    "University of Saskatchewan, including St. Thomas More College": "University of Saskatchewan",
    "Université du Québec en Outaouais Pavillon Alexandre-Taché": "Université du Québec en Outaouais",
    "Faculté de Théologie Évangélique de l’Université Acadia": "Faculté de théologie évangélique",
}


def _request(session: requests.Session, method: str, url: str, **kwargs: Any) -> requests.Response:
    error: Exception | None = None
    for _ in range(3):
        try:
            response = session.request(method, url, timeout=45, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            error = exc
    raise RuntimeError(f"request failed: {url}: {error}")


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().casefold()
    value = value.replace("&", " and ")
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"\b(the|including|incorporated|inc)\b", " ", value)
    return " ".join(re.findall(r"[a-z0-9]+", value))


def _institution_id(dli_number: str) -> str:
    return f"ca:dli:{dli_number}"


def load_ircc() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    response = _request(session, "GET", IRCC_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        raise RuntimeError("IRCC DLI table was not present")
    table = max(tables, key=lambda element: len(element.find_all("tr")))
    rows: list[dict[str, Any]] = []
    for tr in table.find_all("tr")[1:]:
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all("td")]
        if len(cells) < 8:
            continue
        rows.append(
            {
                "province": cells[0],
                "name": cells[1],
                "dli_number": cells[2],
                "city": cells[3],
                "campus": cells[4],
                "graduate_program": cells[5],
                "pgwp_eligible": cells[6],
                "ownership": cells[7],
            }
        )
    if len(rows) < 1_000:
        raise RuntimeError(f"IRCC DLI parse was unexpectedly short: {len(rows)}")
    modified = soup.find("meta", attrs={"name": "dcterms.modified"})
    return rows, {
        "dataset": "IRCC Designated Learning Institutions list",
        "url": response.url,
        "page_modified": modified.get("content", "") if modified else "",
        "access_date": ACCESS_DATE,
        "http_status": response.status_code,
        "sha256": hashlib.sha256(response.content).hexdigest(),
        "campus_row_count": len(rows),
    }


def _parse_cicic_page(response: requests.Response) -> tuple[list[dict[str, str]], BeautifulSoup]:
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if table is None:
        raise RuntimeError("CICIC result table was not present")
    records: list[dict[str, str]] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) < 11:
            continue
        text = [cell.get_text(" ", strip=True) for cell in cells]
        link = cells[1].find("a")
        records.append(
            {
                "cicic_id": text[0],
                "name": text[1],
                "city": text[2],
                "province": text[7],
                "sector": text[8],
                "level": text[9],
                "legal_status": text[10],
                "url": urljoin(response.url, link.get("href", "")) if link else response.url,
            }
        )
    return records, soup


def load_cicic() -> tuple[list[dict[str, str]], dict[str, Any]]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    response = _request(session, "GET", CICIC_URL)
    records: list[dict[str, str]] = []
    page_hashes: list[str] = []
    page_count = 1
    for page in range(1, 20):
        page_records, soup = _parse_cicic_page(response)
        records.extend(page_records)
        page_hashes.append(hashlib.sha256(response.content).hexdigest())
        pager = soup.find("tr", class_="rgPager")
        if page == 1 and pager:
            match = re.search(r"in\s+(\d+)\s+pages", pager.get_text(" ", strip=True))
            page_count = int(match.group(1)) if match else 1
        if page >= page_count:
            break
        hidden = {
            element["name"]: element.get("value", "")
            for element in soup.select('input[type="hidden"][name]')
        }
        hidden["__EVENTTARGET"] = "ctl00$Main$EducationDirectory$gridresults$ctl00$ctl03$ctl01$ctl04"
        hidden["__EVENTARGUMENT"] = ""
        form = soup.find("form")
        if form is None:
            raise RuntimeError("CICIC paging form was not present")
        response = _request(session, "POST", urljoin(response.url, form.get("action", "")), data=hidden)
    unique = {record["cicic_id"]: record for record in records}
    return list(unique.values()), {
        "dataset": "CICIC Directory of Educational Institutions in Canada",
        "url": CICIC_URL,
        "directory_scope_url": CICIC_DIRECTORY_URL,
        "access_date": ACCESS_DATE,
        "page_count": page_count,
        "institution_count": len(unique),
        "page_sha256": page_hashes,
        "note": "CICIC states that the live directory contains only currently recognized, authorized, registered and/or licensed institutions.",
    }


def load_ror() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    params = {"filter": "country.country_code:CA,types:education,status:active", "page": 1}
    first = _request(session, "GET", ROR_API, params=params).json()
    count = int(first["number_of_results"])
    records = list(first["items"])

    def fetch(page: int) -> list[dict[str, Any]]:
        local = requests.Session()
        local.headers["User-Agent"] = USER_AGENT
        return _request(local, "GET", ROR_API, params={**params, "page": page}).json()["items"]

    pages = range(2, math.ceil(count / 20) + 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for page_records in executor.map(fetch, pages):
            records.extend(page_records)
    return records, {
        "dataset": "Research Organization Registry API v2",
        "url": ROR_API,
        "documentation": ROR_DOCS,
        "access_date": ACCESS_DATE,
        "reported_count": count,
        "retrieved_count": len(records),
        "filter": params["filter"],
        "note": "ROR supplies persistent cross-reference identifiers and official-domain metadata; it is not used as an accreditation authority.",
    }


def _ror_name(record: dict[str, Any]) -> str:
    for name in record.get("names", []):
        if "ror_display" in name.get("types", []):
            return name.get("value", "")
    return ""


def _ror_aliases(record: dict[str, Any]) -> list[str]:
    return [name.get("value", "") for name in record.get("names", []) if name.get("value")]


def _ror_website(record: dict[str, Any]) -> str:
    for link in record.get("links", []):
        if link.get("type") == "website":
            return link.get("value", "")
    domains = record.get("domains", [])
    return f"https://{domains[0]}" if domains else ""


def _best_match(name: str, province: str, records: list[dict[str, str]]) -> tuple[dict[str, str] | None, float]:
    target = _normalize(NAME_ALIASES.get(name, name))
    candidates = [record for record in records if record["province"] == province] or records
    scored = [
        (difflib.SequenceMatcher(None, target, _normalize(record["name"])).ratio(), record)
        for record in candidates
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored or scored[0][0] < 0.72:
        return None, scored[0][0] if scored else 0.0
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.02 and scored[0][0] < 0.95:
        return None, scored[0][0]
    return scored[0][1], scored[0][0]


def _match_ror(name: str, records: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, float]:
    target = _normalize(NAME_ALIASES.get(name, name))
    scored: list[tuple[float, dict[str, Any]]] = []
    for record in records:
        best = max(
            (difflib.SequenceMatcher(None, target, _normalize(alias)).ratio() for alias in _ror_aliases(record)),
            default=0.0,
        )
        scored.append((best, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored or scored[0][0] < 0.78:
        return None, scored[0][0] if scored else 0.0
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.02 and scored[0][0] < 0.96:
        return None, scored[0][0]
    return scored[0][1], scored[0][0]


def _fetch_program_page(seed: ProgramSeed) -> dict[str, Any]:
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en,fr;q=0.8"})
        response = _request(session, "GET", seed.url)
        raw = response.content[:5_000_000]
        content_type = response.headers.get("content-type", "")
        if "pdf" in content_type.casefold() or response.url.casefold().endswith(".pdf"):
            text = raw.decode("latin-1", errors="ignore")
            title = seed.name
        else:
            soup = BeautifulSoup(raw, "html.parser")
            for element in soup(["script", "style", "noscript", "svg"]):
                element.decompose()
            text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
            title = soup.title.get_text(" ", strip=True) if soup.title else seed.name
        lowered = text.casefold()
        degree_signal = any(term in lowered for term in ("computer science", "computing", "informatique", "information technology", "technologies de l’information", "telecommunications"))
        research_signal = any(term in lowered for term in ("thesis", "research", "mémoire", "memoire", "recherche", "dissertation"))
        return {
            "institution": seed.institution,
            "program": seed.name,
            "url": seed.url,
            "final_url": response.url,
            "http_status": response.status_code,
            "content_type": content_type,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "title": title,
            "degree_signal": degree_signal,
            "research_signal": research_signal,
            "verified": degree_signal and research_signal,
            "excerpt": text[:1_500],
        }
    except Exception as exc:  # preserve source failures instead of aborting the universe
        return {
            "institution": seed.institution,
            "program": seed.name,
            "url": seed.url,
            "verified": False,
            "error": str(exc),
        }


def _blank(columns: Iterable[str]) -> dict[str, Any]:
    return {column: "" for column in columns}


def build_outputs(
    ircc_rows: list[dict[str, Any]],
    cicic_rows: list[dict[str, str]],
    ror_rows: list[dict[str, Any]],
    *,
    output_dir: Path,
    manifest_dir: Path,
    evidence_dir: Path,
    manifests: dict[str, Any],
) -> dict[str, Any]:
    graduate_rows = [row for row in ircc_rows if row["graduate_program"] == "Yes"]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in graduate_rows:
        grouped[row["dli_number"]].append(row)

    page_checks: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for check in executor.map(_fetch_program_page, PROGRAM_SEEDS):
            page_checks[check["institution"]] = check

    seed_by_institution = {seed.institution: seed for seed in PROGRAM_SEEDS}
    institution_rows: list[dict[str, Any]] = []
    program_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    unresolved_cicic: list[dict[str, Any]] = []
    unresolved_ror: list[dict[str, Any]] = []

    for dli_number, campuses in sorted(grouped.items(), key=lambda item: (item[1][0]["province"], item[1][0]["name"].casefold())):
        source_names = sorted({row["name"] for row in campuses})
        preferred = PREFERRED_NAMES.get(dli_number)
        if preferred:
            name = preferred
        else:
            name = min(source_names, key=lambda candidate: ("including" in candidate.casefold(), len(candidate)))
        name = NAME_ALIASES.get(name, name)
        province = campuses[0]["province"]
        institution_id = _institution_id(dli_number)
        cicic, cicic_score = _best_match(name, province, cicic_rows)
        ror, ror_score = _match_ror(name, ror_rows)
        if cicic is None:
            unresolved_cicic.append({"institution": name, "province": province, "dli_number": dli_number, "best_score": round(cicic_score, 3)})
        if ror is None:
            unresolved_ror.append({"institution": name, "province": province, "dli_number": dli_number, "best_score": round(ror_score, 3)})

        seed = seed_by_institution.get(name)
        page = page_checks.get(name)
        specialty_reason = SPECIALTY_EXCLUSIONS.get(name)
        if seed and page and page.get("verified"):
            status = "preliminary_fit"
            exclusion_reason = ""
            field_signal = f"Official page verifies a research/thesis route: {seed.name}."
        elif specialty_reason:
            status = "no_relevant_graduate_field"
            exclusion_reason = specialty_reason
            field_signal = "Negative specialty/title screen; a manual catalog audit is still recommended."
        else:
            status = "indexed"
            exclusion_reason = ""
            if seed:
                field_signal = "Relevant program seed found, but the official page was blocked or lacked the required mechanical signals."
            else:
                field_signal = "No verified positive research-program signal in this bounded mechanical pass; no negative conclusion drawn."

        recognition = (
            f"CICIC {cicic['legal_status']} ({cicic['sector']} {cicic['level']})"
            if cicic
            else "Current IRCC public graduate DLI; exact CICIC name match unresolved"
        )
        website = _ror_website(ror) if ror else ""
        official_source = cicic["url"] if cicic else IRCC_URL
        institution_rows.append(
            {
                "institution_id": institution_id,
                "institution_name": name,
                "alternate_names": " | ".join(source_names),
                "country": "Canada",
                "region": f"Canada — {province}",
                "institution_type": campuses[0]["ownership"],
                "recognition_status": recognition,
                "active_status": "current",
                "official_website": website,
                "source_database": "IRCC DLI + CICIC live directory + ROR v2 cross-reference",
                "dataset_release": f"IRCC page modified {manifests['ircc'].get('page_modified', '')}; CICIC live directory; ROR API v2",
                "access_date": ACCESS_DATE,
                "graduate_degree_authority": "Verified by IRCC public-DLI graduate-program flag (master's/doctorate degree programs)",
                "relevant_graduate_field_signal": field_signal,
                "screening_status": status,
                "exclusion_reason": exclusion_reason,
                "ror_id": ror.get("id", "") if ror else "",
                "ipeds_unitid": "",
                "eter_id": "",
                "dli_number": dli_number,
                "manual_verification": "Complete for federal graduate-DLI flag; required for unresolved name/program screens",
                "notes": f"Collapsed {len(campuses)} IRCC campus rows. Cities: {' | '.join(sorted({row['city'] for row in campuses if row['city']}))}. CICIC match score={cicic_score:.3f}; ROR match score={ror_score:.3f}.",
            }
        )

        grad_claim = _blank(SOURCE_COLUMNS)
        grad_claim.update(
            {
                "source_id": source_id(IRCC_URL),
                "institution_id": institution_id,
                "institution_name": name,
                "claim_type": "graduate authority and international-student eligibility",
                "exact_claim_supported": "IRCC lists this DLI as a public institution offering PAL/TAL-exempt graduate degree programs at the master's or doctorate level.",
                "source_title": "Designated learning institutions list",
                "publisher": "Immigration, Refugees and Citizenship Canada",
                "publication_date": manifests["ircc"].get("page_modified", ""),
                "url": IRCC_URL,
                "source_type": "federal live directory",
                "official_or_secondary": "official",
                "date_accessed": ACCESS_DATE,
                "admissions_cycle": "Current status; not a Fall 2027 program-admission guarantee",
                "confidence": "High",
                "verification_status": "opened and parsed",
                "access_note": f"DLI {dli_number}; {len(campuses)} campus rows collapsed; page SHA-256 in manifest",
            }
        )
        source_rows.append(grad_claim)

        recognition_claim = _blank(SOURCE_COLUMNS)
        recognition_claim.update(
            {
                "source_id": source_id(official_source),
                "institution_id": institution_id,
                "institution_name": name,
                "claim_type": "recognition",
                "exact_claim_supported": recognition if cicic else "Exact CICIC directory-name match remains unresolved; no blanket recognition claim made.",
                "source_title": f"CICIC institution record — {cicic['name']}" if cicic else "CICIC current-directory scope and IRCC DLI record",
                "publisher": "Canadian Information Centre for International Credentials",
                "url": official_source,
                "source_type": "national authoritative directory",
                "official_or_secondary": "official/system authority",
                "date_accessed": ACCESS_DATE,
                "confidence": "High" if cicic else "Medium",
                "verification_status": "matched" if cicic else "manual match required",
                "access_note": f"CICIC normalized-name score {cicic_score:.3f}",
            }
        )
        source_rows.append(recognition_claim)

        if status == "no_relevant_graduate_field":
            exclusion_url = website or official_source
            exclusion_rows.append(
                {
                    "institution_id": institution_id,
                    "institution_name": name,
                    "country": "Canada",
                    "program_id": "",
                    "program_name": "",
                    "stage_of_exclusion": "mechanical program screening",
                    "primary_exclusion_reason": exclusion_reason,
                    "supporting_evidence": "Institutional specialty and official web/catalog title screen produced no relevant research graduate degree; negative finding remains marked for manual verification.",
                    "source_url": exclusion_url,
                    "confidence": "Medium",
                    "manual_verification": "Required before treating this negative screen as final",
                    "date_checked": ACCESS_DATE,
                }
            )
            exclusion_claim = _blank(SOURCE_COLUMNS)
            exclusion_claim.update(
                {
                    "source_id": source_id(exclusion_url),
                    "institution_id": institution_id,
                    "institution_name": name,
                    "claim_type": "mechanical exclusion",
                    "exact_claim_supported": exclusion_reason,
                    "source_title": "Official institutional website / program inventory",
                    "publisher": name,
                    "url": exclusion_url,
                    "source_type": "official institutional website",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "confidence": "Medium",
                    "verification_status": "negative mechanical screen; manual audit required",
                    "access_note": "Absence is not treated as conclusive beyond this screening phase.",
                }
            )
            source_rows.append(exclusion_claim)

        if status == "preliminary_fit" and seed and page:
            pid = program_id(institution_id, "Thesis or research master's", seed.name)
            program = _blank(PROGRAM_COLUMNS)
            program.update(
                {
                    "program_id": pid,
                    "institution_id": institution_id,
                    "institution_name": name,
                    "country": "Canada",
                    "program_name": seed.name,
                    "degree_type": "Thesis or research master's" if "PhD" not in seed.name else "PhD",
                    "department": seed.department,
                    "official_program_url": page.get("final_url", seed.url),
                    "thesis_dissertation_requirement": seed.thesis,
                    "research_credit_requirement": "Official page shows a thesis/research route; exact credits pending deep review",
                    "research_groups_labs": "Pending faculty/research-fit phase",
                    "direct_from_bachelors_eligible": seed.direct_entry,
                    "international_student_eligible": "Institution is a current DLI; program-specific eligibility pending",
                    "language_of_instruction": seed.language,
                    "current_program_status": "Official program page accessible on freeze date",
                    "preliminary_fit": "Positive computing/software/AI/security research-degree signal",
                    "screening_decision": "preliminary_fit",
                    "admissions_model": "Program application; supervisor rules pending deep review",
                    "faculty_contact_expectation": "Pending deep review",
                    "funding_model": "Pending deep review",
                    "funding_status": "Not assessed in mechanical screen",
                    "admission_plausibility": "Insufficient evidence",
                    "recommendation": "Investigate Further",
                    "biggest_risk": "Faculty fit, funding, and Fall 2027 details are not yet verified",
                    "unresolved_question": "Does the program have a matching supervisor and viable funding for Fall 2027?",
                    "single_professor_dependency": "Unknown",
                    "verification_status": "Official program existence/structure checked; deep review pending",
                    "notes": "Mechanical positive-signal screen only; not finally retained.",
                }
            )
            program_rows.append(program)
            program_claim = _blank(SOURCE_COLUMNS)
            program_claim.update(
                {
                    "source_id": source_id(page.get("final_url", seed.url)),
                    "institution_id": institution_id,
                    "institution_name": name,
                    "program_id": pid,
                    "program_or_professor": seed.name,
                    "claim_type": "program status and degree structure",
                    "exact_claim_supported": f"The official page identifies {seed.name} and contains research/thesis evidence.",
                    "source_title": page.get("title", seed.name),
                    "publisher": name,
                    "url": page.get("final_url", seed.url),
                    "source_type": "official program page",
                    "official_or_secondary": "official",
                    "date_accessed": ACCESS_DATE,
                    "admissions_cycle": "Current page; Fall 2027 dates not assumed",
                    "confidence": "High for program existence and research structure",
                    "verification_status": "opened",
                    "access_note": f"HTTP {page.get('http_status', '')}; page SHA-256 in evidence file",
                }
            )
            source_rows.append(program_claim)

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "institution_universe.csv", institution_rows, INSTITUTION_COLUMNS)
    write_csv(output_dir / "program_screening.csv", program_rows, PROGRAM_COLUMNS)
    write_csv(output_dir / "exclusion_log.csv", exclusion_rows, EXCLUSION_COLUMNS)
    write_csv(output_dir / "source_ledger.csv", source_rows, SOURCE_COLUMNS)
    write_json(evidence_dir / "official_program_page_checks.json", list(page_checks.values()))
    write_json(manifest_dir / "ircc_snapshot.json", manifests["ircc"])
    write_json(manifest_dir / "cicic_snapshot.json", manifests["cicic"])
    write_json(manifest_dir / "ror_snapshot.json", manifests["ror"])

    blocked = [check for check in page_checks.values() if not check.get("verified")]
    write_json(
        manifest_dir / "blocked_sources.json",
        {
            "access_date": ACCESS_DATE,
            "sources": [
                {
                    "institution": check["institution"],
                    "program": check["program"],
                    "url": check["url"],
                    "status": "blocked" if check.get("error") else "insufficient page signals",
                    "error": check.get("error", "Required degree/research terms were not both present in the opened content"),
                }
                for check in blocked
            ],
        },
    )
    coverage = {
        "generated_at": f"{ACCESS_DATE}T00:00:00Z",
        "scope": "All Canadian provinces and territories represented in the IRCC public-graduate-DLI flag",
        "ircc_all_campus_rows": len(ircc_rows),
        "ircc_public_graduate_campus_rows": len(graduate_rows),
        "institution_count_after_dli_deduplication": len(institution_rows),
        "duplicate_campus_rows_collapsed": len(graduate_rows) - len(institution_rows),
        "province_counts": dict(sorted(Counter(row["region"].replace("Canada — ", "") for row in institution_rows).items())),
        "status_counts": dict(sorted(Counter(row["screening_status"] for row in institution_rows).items())),
        "verified_program_candidate_count": len(program_rows),
        "mechanical_exclusion_count": len(exclusion_rows),
        "source_claim_count": len(source_rows),
        "cicic_exact_or_fuzzy_match_count": len(institution_rows) - len(unresolved_cicic),
        "cicic_unresolved_count": len(unresolved_cicic),
        "ror_match_count": len(institution_rows) - len(unresolved_ror),
        "ror_unresolved_count": len(unresolved_ror),
        "blocked_or_insufficient_program_page_count": len(blocked),
        "unresolved_cicic_matches": unresolved_cicic,
        "unresolved_ror_matches": unresolved_ror,
        "limitations": [
            "The universe is intentionally limited to current public DLIs that IRCC flags as offering master's/doctorate degree programs; private and non-DLI graduate institutions are outside this international-applicant universe.",
            "DLI campus rows are collapsed to one institution-level row per DLI number; affiliated colleges sharing a DLI remain alternate names rather than separate application targets.",
            "The program screen is a bounded official-page positive-signal pass, not deep faculty, funding, admissions, or Fall 2027 verification.",
            "An indexed status is unresolved, not a negative finding. Only narrow specialty institutions receive a no-relevant-field exclusion, and those exclusions remain manually reviewable.",
            "ROR identifiers are preserved only when name matching is unambiguous; ROR is not used as an accreditation authority.",
        ],
    }
    write_json(output_dir / "coverage.json", coverage)
    readme = f"""# Canada regional coverage

Frozen on {ACCESS_DATE}. This phase intersected the live IRCC DLI table's public graduate-program flag with the current CICIC directory and added ROR identifiers where name matching was unambiguous. Campus rows sharing a DLI number were collapsed.

- Institutions: {len(institution_rows)}
- IRCC graduate campus rows collapsed: {len(graduate_rows) - len(institution_rows)}
- Verified official research-program signals: {len(program_rows)}
- Narrow mechanical exclusions: {len(exclusion_rows)}
- Indexed for later review: {sum(row['screening_status'] == 'indexed' for row in institution_rows)}
- CICIC unresolved name matches: {len(unresolved_cicic)}
- ROR unresolved name matches: {len(unresolved_ror)}
- Blocked/insufficient official program pages: {len(blocked)}

`indexed` means unresolved, not excluded. No faculty recruitment, funding package, or Fall 2027 deadline claim is made in this regional phase.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")
    return coverage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the Canada public graduate-DLI universe and mechanical program screen")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data" / "processed" / "regions" / "canada")
    parser.add_argument("--manifest-dir", type=Path, default=ROOT / "data" / "manifests" / "canada")
    parser.add_argument("--evidence-dir", type=Path, default=ROOT / "evidence" / "programs" / "canada")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    ircc_rows, ircc_manifest = load_ircc()
    cicic_rows, cicic_manifest = load_cicic()
    ror_rows, ror_manifest = load_ror()
    coverage = build_outputs(
        ircc_rows,
        cicic_rows,
        ror_rows,
        output_dir=args.output_dir,
        manifest_dir=args.manifest_dir,
        evidence_dir=args.evidence_dir,
        manifests={"ircc": ircc_manifest, "cicic": cicic_manifest, "ror": ror_manifest},
    )
    print(json.dumps(coverage, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
