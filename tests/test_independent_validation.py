from graduate_audit.independent_validation import (
    build_core_claim_rechecks,
    cycle_label_is_safe,
    portfolio_economics,
    recalculate_scores,
    verify_distinct_professor_counts,
)


def test_recalculate_scores_requires_six_components_and_exact_total():
    scores = [{"program_id": "p", "institution_name": "U", "overall_score": "21"}]
    evidence = [
        {"program_id": "p", "component": f"c{i}", "component_score": str(i)}
        for i in range(1, 7)
    ]
    assert recalculate_scores(scores, evidence)[0]["status"] == "pass"


def test_recalculate_scores_detects_difference():
    scores = [{"program_id": "p", "institution_name": "U", "overall_score": "20"}]
    evidence = [
        {"program_id": "p", "component": f"c{i}", "component_score": str(i)}
        for i in range(1, 7)
    ]
    result = recalculate_scores(scores, evidence)[0]
    assert result["status"] == "fail"
    assert result["difference"] == 1


def test_distinct_professor_recount_deduplicates():
    scores = [{"program_id": "p", "institution_name": "U", "distinct_verified_strong_matches": "1"}]
    matches = [
        {"program_id": "p", "professor_id": "a", "verification_status": "verified_strong_match", "fit_strength": "Strong"},
        {"program_id": "p", "professor_id": "a", "verification_status": "verified_strong_match", "fit_strength": "Strong"},
        {"program_id": "p", "professor_id": "b", "verification_status": "unverified", "fit_strength": "Strong"},
    ]
    assert verify_distinct_professor_counts(scores, matches)[0]["status"] == "pass"


def test_cycle_label_requires_explicit_or_caveated_cycle():
    assert cycle_label_is_safe("2026-12-15", "Fall 2027 current application page")
    assert cycle_label_is_safe("December 15", "Recurring deadline; confirm Fall 2027")
    assert not cycle_label_is_safe("December 15", "Current page")


def test_core_claim_rechecks_create_five_domains():
    core = [{"program_id": "p", "institution_name": "U"}]
    verification = [{
        "verified_program_id": "p", "exact_degree_program_name": "PhD", "funding_model": "funded",
        "bachelors_entry_eligibility": "yes", "fall_2027_deadline": "2026-12-15",
        "deadline_cycle_label": "Fall 2027", "largest_unresolved_question": "none",
    }]
    sources = [{
        "candidate_program_id": "p", "official_or_secondary": "official", "claim_categories": "program|funding|eligibility|deadline",
        "stage3_source_id": "s", "url": "https://example.edu/p",
    }]
    professors = [{"program_id": "p", "full_name": "Prof", "verification_status": "verified_strong_match", "source_ids": "f"}]
    professor_sources = [{"stage4_source_id": "f", "official_or_secondary": "official", "url": "https://example.edu/f"}]
    rows = build_core_claim_rechecks(core, verification, sources, professors, professor_sources)
    assert {row["domain"] for row in rows} == {"program", "faculty", "funding", "eligibility", "deadline"}
    assert all(row["evidence_status"] == "verified_single_source" for row in rows)


def test_portfolio_economics_preserves_unknown_fees():
    core = [{"institution_id": "u1", "degree_type": "PhD", "region": "us", "application_fee": "50", "fee_currency": "USD", "all_hard_gates_pass": True}]
    reserve = [{"institution_id": "u2", "degree_type": "MASc", "region": "canada", "application_fee": "unknown", "fee_currency": "CAD", "all_hard_gates_pass": True}]
    result = portfolio_economics(core, reserve)
    assert result["known_fee_totals_by_currency"] == {"USD": 50.0}
    assert result["unknown_or_non_numeric_fee_programs"] == 1
    assert result["single_program_per_university"]
