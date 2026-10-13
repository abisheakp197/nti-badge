"""These tests run FIRST. If any of them fail, the entire ecosystem is broken.
Every test here imports and calls a REAL external API. No mocks."""


import pytest




class TestUbeFoundationAPI:
    def test_pqc_key_pair_constructor(self):
        from ube_foundation import PqcKeyPair
        key = PqcKeyPair()
        assert key is not None


    def test_pqc_key_pair_has_correct_methods(self):
        from ube_foundation import PqcKeyPair
        key = PqcKeyPair()
        assert callable(getattr(key, "sign"))
        assert callable(getattr(key, "sign_bytes"))
        assert callable(getattr(key, "verify"))
        assert callable(getattr(key, "public_key_hex"))


    def test_pqc_sign_returns_hex_string(self):
        from ube_foundation import PqcKeyPair
        key = PqcKeyPair()
        sig = key.sign(b"test")
        assert isinstance(sig, str)
        assert len(sig) > 100


    def test_pqc_verify_roundtrip(self):
        from ube_foundation import PqcKeyPair
        key = PqcKeyPair()
        msg = b"verify roundtrip"
        sig = key.sign(msg)
        assert key.verify(msg, sig) is True


    def test_pqc_verify_rejects_tampered(self):
        from ube_foundation import PqcKeyPair
        key = PqcKeyPair()
        msg = b"original message"
        sig = key.sign(msg)
        assert key.verify(b"tampered message", sig) is False


    def test_trust_engine_constructor(self):
        from ube_foundation import TrustEngine
        engine = TrustEngine()
        assert engine is not None


    def test_trust_engine_evaluate_returns_json(self):
        import json
        from ube_foundation import TrustEngine
        engine = TrustEngine()
        engine.grant("test_actor", "read")
        req = {
            "id": "req-1", "actor": "test_actor", "capability": "read",
            "action": "read", "input": {},
            "signature": None, "pqc_signature": None,
            "public_key": None, "pqc_public_key": None,
            "token": None, "identity_claim": None,
        }
        raw = engine.evaluate(json.dumps(req))
        decision = json.loads(raw)
        assert decision["decision"] == "Allow"




class TestNtiAttackAPI:
    def test_load_all_attacks(self):
        from nti_attack.runner import load_all_attacks
        attacks = load_all_attacks()
        assert len(attacks) >= 5


    def test_build_report(self):
        from nti_attack.attestation import build_report
        from nti_attack.core import AttackResult
        results = [AttackResult(attack_id="X", passed=True, severity="high")]
        report = build_report("agent-x", "sha", results)
        assert report["resistance_score"] == 100


    def test_sign_and_verify_report(self):
        from nti_attack.attestation import build_report, sign_report, verify_report
        from nti_attack.core import AttackResult
        results = [AttackResult(attack_id="X", passed=True, severity="high")]
        report = build_report("agent-x", "sha", results)
        signed = sign_report(report)
        v = verify_report(signed)
        assert v["ok"] is True


    def test_adapter_interface(self):
        from nti_attack.adapters.base import AgentAdapter, AgentResponse
        assert AgentAdapter is not None
        resp = AgentResponse(output="ok")
        assert resp.output == "ok"




class TestNtiScannerAPI:
    def test_parse_python_file(self, tmp_path):
        from nti_scanner.ast_analysis.parser import parse_python_file
        f = tmp_path / "sample.py"
        f.write_text("x = 1")
        tree = parse_python_file(f)
        assert tree is not None


    def test_detect_frameworks(self, tmp_path):
        from nti_scanner.ast_analysis.parser import parse_python_file
        from nti_scanner.framework.detector import detect_frameworks
        f = tmp_path / "sample.py"
        f.write_text("from langchain.agents import AgentExecutor")
        tree = parse_python_file(f)
        frameworks = detect_frameworks({f: tree})
        assert "langchain" in frameworks


    def test_scan_directory(self, tmp_path):
        from nti_scanner.scanner import scan_directory
        f = tmp_path / "agent.py"
        f.write_text("x = 1")
        result = scan_directory(tmp_path)
        assert result.files_scanned >= 1
        assert isinstance(result.nti1_score, int)
