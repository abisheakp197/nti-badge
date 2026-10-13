"""Cross-tool integration: scanner, attack, benchmark chain."""


import subprocess
import sys
from pathlib import Path




def test_nti_scanner_can_scan_a_file(tmp_path):
    f = tmp_path / "agent.py"
    f.write_text("from langchain.agents import AgentExecutor\n")
    from nti_scanner.scanner import scan_directory
    result = scan_directory(tmp_path)
    assert result.files_scanned == 1




def test_nti_attack_loads_all_attacks():
    from nti_attack.runner import load_all_attacks
    attacks = load_all_attacks()
    assert len(attacks) >= 5




def test_benchmark_uses_nti_attack():
    from benchmarks import ALL_BENCHMARKS
    b = ALL_BENCHMARKS[0]()
    result = b.run()
    assert result["attack_count"] >= 5
