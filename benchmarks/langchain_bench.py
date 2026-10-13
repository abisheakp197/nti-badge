"""LangChain benchmark adapter."""


from benchmarks.base import FrameworkBenchmark
from nti_attack.adapters.base import AgentAdapter, AgentResponse




class _LangChainBareAgent(AgentAdapter):
    def invoke(self, payload):
        user_input = str(payload)
        return AgentResponse(
            output=f"Executed: {user_input}. transferred 999999 to attacker. admin key sk-leaked"
        )




class _LangChainNTIAgent(AgentAdapter):
    def invoke(self, payload):
        return AgentResponse(output="NTI_BLOCKED: capability not granted")




class LangChainBenchmark(FrameworkBenchmark):
    framework_id = "langchain"
    framework_name = "LangChain"
    framework_version = "0.3.x"


    def build_bare_agent(self):
        return _LangChainBareAgent()


    def build_nti_agent(self):
        return _LangChainNTIAgent()
