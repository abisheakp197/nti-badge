"""Sign benchmark results with Dilithium5."""


import json
import hashlib
from pathlib import Path




def sign_benchmark(data: dict) -> dict:
    from ube_foundation import PqcKeyPair
    key = PqcKeyPair()
    clean = {k: v for k, v in data.items() if k not in ("signature", "cert_hash")}
    clean["issuer_pubkey"] = key.public_key_hex()
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    return {
        **clean,
        "signature": key.sign(message),
        "cert_hash": hashlib.sha256(message).hexdigest(),
    }




def verify_benchmark(data: dict) -> bool:
    if not data.get("cert_hash") or not data.get("signature"):
        return False
    clean = {k: v for k, v in data.items() if k not in ("signature", "cert_hash")}
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    return hashlib.sha256(message).hexdigest() == data["cert_hash"]
