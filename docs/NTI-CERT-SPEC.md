# NTI-Cert/1 Specification


**Version:** 1.0
**Status:** Stable
**License:** Apache 2.0


## Purpose


NTI-Cert/1 is a portable, post-quantum-signed compliance certificate format for autonomous AI agent repositories. Any repo can produce an NTI-Cert/1 certificate. Any party can verify it offline. No central authority is required.


## Design Principles


1. **Portable** — the certificate travels with the code. It is never held hostage.
2. **Verifiable offline** — verification requires only the cert and the spec.
3. **Post-quantum** — Dilithium5 signatures (NIST Level 5).
4. **Commit-bound** — every cert references a specific commit SHA.
5. **Append-only** — certificates accumulate. History is the audit trail.
6. **Federated** — any party may index certs. No single registry is authoritative.
7. **Zero data custody** — registries index hashes only, never full payloads.


## Required Fields


| Field | Type | Description |
|---|---|---|
| spec | string | Always `"NTI-Cert/1"` |
| issuer | string | The repo that issued the cert |
| issued_at | string | ISO 8601 UTC timestamp |
| id | string | UUIDv4, unique per cert |
| repo | string | `owner/repo` format |
| commit_sha | string | Git commit the cert refers to |
| score | integer | 0–100 |
| profile | string | `"NTI-1"` |
| signature_alg | string | Always `"Dilithium5"` |
| issuer_pubkey | string | Hex-encoded Dilithium5 public key |
| signature | string | Hex-encoded Dilithium5 signature |
| cert_hash | string | SHA-256 of payload (excluding `signature` and `cert_hash`) |


## Optional Fields


| Field | Type | Description |
|---|---|---|
| tier | string | `Platinum` / `Gold` / `Silver` / `Bronze` / `Unranked` |
| commit_author | string | Email of the commit author |
| branch | string | Git branch |
| run_id | string | CI run identifier |
| findings_count | integer | Total findings from nti-scanner |
| language | string | Primary language |
| issuer_contact | string | Contact URL for the issuer |
| sbom | object | Optional SBOM attestation |


## Signature Algorithm


- **Algorithm:** CRYSTALS-Dilithium5 (NIST PQC Level 5)
- **Message:** JSON-serialized payload, `sort_keys=True`, without `signature` and `cert_hash`
- **Encoding:** Hex string


## Verification Algorithm


1. Remove `signature` and `cert_hash` from the payload
2. Serialize the remaining fields as JSON with `sort_keys=True`
3. Compute SHA-256 → must equal `cert_hash`
4. Use `issuer_pubkey` to verify `signature` against the message


## Federation Protocol


A federation node MUST expose at minimum:
- `POST /api/verify` — accepts signed cert submissions
- `GET /api/certificate?repo=...` — returns index entry for a repo
- `GET /api/federation` — manifest


A federation node MUST NOT:
- Store full certificates (only hashes + scores)
- Require registration to verify certificates
- Have any exclusive control over the cert format


## Reference Implementation


- Badge server: `github.com/abisheakp197/nti-badge`
- Verifier CLI: `pip install nti-scanner && nti-scanner verify ./nti-certificate.json`
- Core SDK: `pip install ube-foundation`


## Versioning


NTI-Cert/1 is frozen. Future versions will be NTI-Cert/2, etc. Backwards compatibility is required for index parsing.
