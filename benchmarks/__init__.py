"""Framework benchmarks."""


from benchmarks.langchain_bench import LangChainBenchmark
from benchmarks.crewai_bench import CrewAIBenchmark
from benchmarks.autogen_bench import AutoGenBenchmark
from benchmarks.maf_bench import MAFBenchmark


ALL_BENCHMARKS = [
    LangChainBenchmark,
    CrewAIBenchmark,
    AutoGenBenchmark,
    MAFBenchmark,
]


__all__ = ["ALL_BENCHMARKS", "LangChainBenchmark", "CrewAIBenchmark", "AutoGenBenchmark", "MAFBenchmark"]
