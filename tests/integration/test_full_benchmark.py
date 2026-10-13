"""Full benchmark end-to-end."""


from runner.run_benchmark import run_all
from runner.attestation import sign_benchmark, verify_benchmark




def test_full_benchmark_signs_and_verifies():
    data = run_all()
    signed = sign_benchmark(data)
    assert verify_benchmark(signed) is True




def test_full_benchmark_has_all_frameworks():
    data = run_all()
    names = [r["framework_name"] for r in data["results"]]
    assert "LangChain" in names
    assert "CrewAI" in names
    assert "AutoGen" in names
    assert "Microsoft Agent Framework" in names
