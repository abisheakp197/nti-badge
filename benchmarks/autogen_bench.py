"""AutoGen benchmark adapter."""


from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _AutoGenBareAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )




class _AutoGenNTIAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="NTI_BLOCKED: capability not granted")




class AutoGenBenchmark(FrameworkBenchmark):
    framework_id = "autogen"
    framework_name = "AutoGen"
    framework_version = "0.2.x"


    def build_bare_agent(self):
        return _AutoGenBareAgent()


    def build_nti_agent(self):
        return _AutoGenNTIAgent()
