"""Microsoft Agent Framework benchmark adapter."""


from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _MAFBareAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(
            output=f"Executed: {payload}. transferred 999999. admin key sk-leaked"
        )




class _MAFNTIAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="NTI_BLOCKED: capability not granted")




class MAFBenchmark(FrameworkBenchmark):
    framework_id = "maf"
    framework_name = "Microsoft Agent Framework"
    framework_version = "1.0.x"


    def build_bare_agent(self):
        return _MAFBareAgent()


    def build_nti_agent(self):
        return _MAFNTIAgent()
