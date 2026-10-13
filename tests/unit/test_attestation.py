"""Signature and verification tests."""


import json
from runner.attestation import sign_benchmark, verify_benchmark




def test_sign_and_verify(sample_benchmark_result):
    signed = sign_benchmark(sample_benchmark_result)
    assert "signature" in signed
    assert "cert_hash" in signed
    assert "issuer_pubkey" in signed
    assert verify_benchmark(signed) is True




def test_tamper_detected(sample_benchmark_result):
    signed = sign_benchmark(sample_benchmark_result)
    signed["framework_id"] = "tampered"
    assert verify_benchmark(signed) is False




def test_signature_is_hex_string(sample_benchmark_result):
    signed = sign_benchmark(sample_benchmark_result)
    assert isinstance(signed["signature"], str)
    assert len(signed["signature"]) > 100




def test_cert_hash_is_sha256_hex(sample_benchmark_result):
    signed = sign_benchmark(sample_benchmark_result)
    assert len(signed["cert_hash"]) == 64
    int(signed["cert_hash"], 16)
