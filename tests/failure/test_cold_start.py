"""Cold start: all modules import cleanly."""


def test_all_modules_import():
    import benchmarks
    import benchmarks.base
    import benchmarks.langchain_bench
    import benchmarks.crewai_bench
    import benchmarks.autogen_bench
    import benchmarks.maf_bench
    import runner
    import runner.run_benchmark
    import runner.attestation
    import cli
    import cli.main
    assert benchmarks is not None
    assert runner is not None
    assert cli is not None
