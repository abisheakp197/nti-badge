# Submitting a Framework for Benchmarking


## How


Open a PR adding a new file under benchmarks/, e.g., benchmarks/llamaindex_bench.py.


The file must subclass FrameworkBenchmark and provide:
- build_bare_agent() -> AgentAdapter
- build_nti_agent() -> AgentAdapter
- framework_id, framework_name, framework_version


## Rules


- Bare and with_nti must run the same agent code, just with/without NTI callback
- No mocks that hide real behavior
- Provide a link to the framework's official repo


## Verification


Once merged, the next benchmark run will include your framework. Results will be signed and published in results/.
