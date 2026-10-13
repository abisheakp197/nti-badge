"""Every framework adapter must produce different bare vs NTI scores."""


import pytest
from benchmarks import ALL_BENCHMARKS




@pytest.mark.parametrize("bench_cls", ALL_BENCHMARKS)
def test_adapter_produces_different_scores(bench_cls):
    b = bench_cls()
    result = b.run()
    assert result["bare"]["score"] != result["with_nti"]["score"]




@pytest.mark.parametrize("bench_cls", ALL_BENCHMARKS)
def test_adapter_nti_improves(bench_cls):
    b = bench_cls()
    result = b.run()
    assert result["delta"] > 0




@pytest.mark.parametrize("bench_cls", ALL_BENCHMARKS)
def test_adapter_has_metadata(bench_cls):
    b = bench_cls()
    assert b.framework_id
    assert b.framework_name
    assert b.framework_version
