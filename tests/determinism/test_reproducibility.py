"""Same input = same output. Always."""


from benchmarks import ALL_BENCHMARKS




def test_bare_score_deterministic():
    b = ALL_BENCHMARKS[0]()
    first = b.run()
    second = b.run()
    assert first["bare"]["score"] == second["bare"]["score"]




def test_nti_score_deterministic():
    b = ALL_BENCHMARKS[0]()
    first = b.run()
    second = b.run()
    assert first["with_nti"]["score"] == second["with_nti"]["score"]




def test_delta_deterministic():
    b = ALL_BENCHMARKS[0]()
    first = b.run()
    second = b.run()
    assert first["delta"] == second["delta"]
