from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping


ADMISSION_POSITIONS = {
    "Strongest Realistic Option",
    "Competitive",
    "High Reach",
    "Extreme Reach",
    "Eligibility Concern",
    "Insufficient Evidence",
}

RECOMMENDATION_TIERS = {
    "Strongest Realistic Options",
    "Competitive Options",
    "High Reaches",
    "Extreme Reaches",
}

RESEARCH_DEGREE_TYPES = {
    "PhD",
    "Direct-entry PhD",
    "Integrated or structured doctorate",
    "PhD requiring a master's",
    "Thesis or research master's",
    "Project-based master's with substantial research",
}


def validate_recommended(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    rows = list(rows)
    ranks = [int(row["Overall Rank"]) for row in rows]
    errors: list[str] = []
    if ranks != list(range(1, len(rows) + 1)):
        errors.append("Overall ranks must be contiguous and ordered")
    if not 10 <= len(rows) <= 15:
        errors.append("Recommended portfolio must contain 10 to 15 programs")
    if sum(row.get("Recommendation Tier") == "Extreme Reaches" for row in rows) > 2:
        errors.append("At most two extreme reaches are allowed")
    for row in rows:
        if row.get("Degree Type") not in RESEARCH_DEGREE_TYPES:
            errors.append(f"Non-research degree: {row.get('University')} / {row.get('Exact Program')}")
        if row.get("Recommendation Tier") not in RECOMMENDATION_TIERS:
            errors.append(f"Unknown tier: {row.get('Recommendation Tier')}")
        if row.get("Relative Admission Position") not in ADMISSION_POSITIONS:
            errors.append(f"Unknown admission position: {row.get('Relative Admission Position')}")
        if str(row.get("International Funding Eligible", "")).casefold() != "yes":
            errors.append(f"International funding not verified: {row.get('University')}")
        if str(row.get("Academic Eligibility Verified", "")).casefold() != "yes":
            errors.append(f"Academic eligibility not verified: {row.get('University')}")
        for field in ("Official Program URL", "Official Funding URL", "Admissions Evidence URL"):
            if not str(row.get(field, "")).startswith("http"):
                errors.append(f"Missing {field}: {row.get('University')}")
        if str(row.get("Recommended Decision", "")).casefold().startswith("conditional"):
            errors.append(f"Conditional program mixed into ranking: {row.get('University')}")
    return {
        "passed": not errors,
        "errors": errors,
        "recommended_count": len(rows),
        "tier_counts": dict(Counter(str(row["Recommendation Tier"]) for row in rows)),
    }


def classify_funding_claim(*, reviewed_decision: str, source_url: str, claim: str) -> str:
    """Return a human-reviewed classification without interpreting claim keywords."""
    if reviewed_decision not in {"Pass", "Conditional", "Fail"}:
        raise ValueError("Funding decisions must be explicit Pass, Conditional, or Fail")
    if not source_url.startswith("http") or not claim.strip():
        raise ValueError("A reviewed funding decision requires an official source and exact claim")
    return reviewed_decision
