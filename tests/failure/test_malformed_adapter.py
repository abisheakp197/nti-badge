"""Broken adapters must not crash the benchmark runner."""


from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _Crash(AgentAdapter):
    def invoke(self, payload):
        raise RuntimeError("boom")




class _Break(FrameworkBenchmark):
    framework_id = "broken"
    framework_name = "Broken"
    framework_version = "0.0.1"
    def build_bare_agent(self): return _Crash()
    def build_nti_agent(self): return _Crash()




def test_broken_adapter_does_not_crash_run():
    b = _Break()
    result = b.run()
    assert "bare" in result
    assert "with_nti" in result
