from graduate_audit.schema import canonical_url, program_id, source_id


def test_source_id_ignores_tracking_parameters():
    clean = "https://example.edu/program"
    tracked = "https://example.edu/program/?utm_source=test"
    assert source_id(clean) == source_id(tracked)


def test_program_id_is_deterministic():
    assert program_id("us:ipeds:1", "PhD", "Computer Science") == program_id(
        "us:ipeds:1", "PhD", "Computer Science"
    )


def test_canonical_url_sorts_query_parameters():
    assert canonical_url("HTTPS://EXAMPLE.EDU/x/?b=2&a=1") == "https://example.edu/x?a=1&b=2"

