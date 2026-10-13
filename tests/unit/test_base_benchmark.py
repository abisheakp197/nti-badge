"""FrameworkBenchmark contract tests."""


import pytest
from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _Bare(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="transferred 999999 admin key sk-leaked deleted drop")




class _NTI(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="NTI_BLOCKED: capability not granted")




class _TestBench(FrameworkBenchmark):
    framework_id = "test"
    framework_name = "Test"
    framework_version = "0.0.1"
    def build_bare_agent(self): return _Bare()
    def build_nti_agent(self): return _NTI()




def test_bare_and_nti_agents_differ():
    b = _TestBench()
    bare = b.build_bare_agent().invoke("x").output
    nti = b.build_nti_agent().invoke("x").output
    assert bare != nti




def test_run_returns_expected_keys():
    b = _TestBench()
    result = b.run()
    assert "framework_id" in result
    assert "bare" in result
    assert "with_nti" in result
    assert "delta" in result




def test_bare_score_lower_than_nti():
    b = _TestBench()
    result = b.run()
    assert result["bare"]["score"] < result["with_nti"]["score"]




def test_delta_is_positive():
    b = _TestBench()
    result = b.run()
    assert result["delta"] > 0
