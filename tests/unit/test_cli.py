"""CLI smoke tests."""


import subprocess
import sys




def test_cli_help():
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "--help"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0
    assert "nti-benchmark" in r.stdout




def test_cli_run_subcommand_exists():
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "run", "--help"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0




def test_cli_verify_subcommand_exists():
    r = subprocess.run(
        [sys.executable, "-m", "cli.main", "verify", "--help"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0
