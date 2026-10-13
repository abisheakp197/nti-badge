# Benchmark Methodology


## Framework Selection


We benchmark the four leading AI agent frameworks:
- LangChain
- CrewAI
- AutoGen
- Microsoft Agent Framework


## Attack Suite


All attacks come from nti-attack-library. Every attack maps to a real CWE and an NTI-scanner detection rule.


## Two Configurations Per Framework


1. Bare: the framework with no security layer
2. With NTI: the same framework wrapped with NTI's guardrail


The delta between these two numbers is the value NTI adds.


## Fairness


- No framework is favored. Same attacks against all.
- Scores are deterministic. Same input = same output.
- Results are signed. Anyone can reproduce and verify.


## Limitations


- Benchmarks use simulated agents for reproducibility
- Real production agents may vary
- The NTI with_nti score assumes the framework is properly wrapped
