"""Full benchmark completes in reasonable time."""


import time
from runner.run_benchmark import run_all




def test_full_benchmark_under_30_seconds():
    t0 = time.time()
    run_all()
    elapsed = time.time() - t0
    assert elapsed < 30.0, f"Took {elapsed:.2f}s"
