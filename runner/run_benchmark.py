"""Run benchmark across all frameworks."""


import json
from pathlib import Path
from datetime import datetime, timezone


from benchmarks import ALL_BENCHMARKS




def run_all(progress_cb=None) -> dict:
    results = []
    for i, cls in enumerate(ALL_BENCHMARKS):
        if progress_cb:
            progress_cb(i, len(ALL_BENCHMARKS), cls.framework_name)
        bench = cls()
        results.append(bench.run())


    return {
        "spec": "NTI-Benchmark/1",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "framework_count": len(results),
        "attack_count": results[0]["attack_count"] if results else 0,
        "results": results,
    }




def save_results(data: dict, output_dir: str = "results") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = data["run_at"].replace(":", "-").replace(".", "-")
    path = out / f"benchmark-{ts}.json"
    path.write_text(json.dumps(data, indent=2))
    return path
