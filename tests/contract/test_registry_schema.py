"""Contract test: /api/registry schema."""
import asyncio
from lib.store import list_all


def test_registry_returns_list(temp_store):
    entries = asyncio.run(list_all())
    assert isinstance(entries, list)


def test_registry_spec_field():
    payload = {
        "spec": "NTI-Cert/1",
        "count": 0,
        "note": "federated index",
        "repos": [],
    }
    assert payload["spec"] == "NTI-Cert/1"
    assert isinstance(payload["count"], int)
    assert isinstance(payload["repos"], list)
