"""Shared fixtures. No mocks of real APIs."""


import pytest




@pytest.fixture
def benchmark_output_dir(tmp_path):
    return tmp_path / "results"




@pytest.fixture
def sample_benchmark_result():
    return {
        "framework_id": "test",
        "framework_name": "Test Framework",
        "framework_version": "0.0.1",
        "run_at": "2026-01-15T10:00:00+00:00",
        "bare": {"score": 30, "attacks_run": 10, "attacks_passed": 3, "attacks_failed": 7, "results": []},
        "with_nti": {"score": 98, "attacks_run": 10, "attacks_passed": 9, "attacks_failed": 1, "results": []},
        "delta": 68,
        "attack_count": 10,
    }
