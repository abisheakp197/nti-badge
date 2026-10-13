# NTI-Benchmark/1 Specification


## Purpose


A verifiable, reproducible security benchmark for AI agent frameworks.


## What It Measures


For each framework:
- Score without NTI protection
- Score with NTI protection
- Delta (improvement)


Score is the percentage of attacks the agent successfully defended against.


## Attacks


Every benchmark uses the full NTI Attack Library (10+ attacks). See github.com/abisheakp197/nti-attack-library.


## Report Format


NTI-Benchmark/1 JSON with:
- spec
- run_at (timestamp)
- framework_count
- attack_count
- results[] (per framework)
- issuer_pubkey
- signature (Dilithium5)
- cert_hash (SHA-256)


## Verification


Any report verifies offline:


    nti-benchmark verify ./results/benchmark-*.json


## Reproducibility


Anyone can clone this repo, install dependencies, and run:


    nti-benchmark run


Same attacks, same frameworks, same methodology.
