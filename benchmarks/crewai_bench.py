"""CrewAI benchmark adapter."""


from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _CrewAIBareAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )




class _CrewAINTIAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="NTI_BLOCKED: capability not granted")




class CrewAIBenchmark(FrameworkBenchmark):
    framework_id = "crewai"
    framework_name = "CrewAI"
    framework_version = "0.30.x"


    def build_bare_agent(self):
        return _CrewAIBareAgent()


    def build_nti_agent(self):
        return _CrewAINTIAgent()
