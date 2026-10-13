"""Runner tests."""


from runner.run_benchmark import run_all, save_results
from benchmarks import ALL_BENCHMARKS




def test_run_all_includes_every_framework():
    data = run_all()
    assert data["framework_count"] == len(ALL_BENCHMARKS)
    assert len(data["results"]) == len(ALL_BENCHMARKS)




def test_run_all_has_spec():
    data = run_all()
    assert data["spec"] == "NTI-Benchmark/1"




def test_run_all_attack_count_positive():
    data = run_all()
    assert data["attack_count"] >= 5




def test_save_results_creates_file(tmp_path):
    data = run_all()
    path = save_results(data, str(tmp_path))
    assert path.exists()
