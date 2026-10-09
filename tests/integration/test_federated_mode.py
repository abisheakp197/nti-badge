"""Federated mode enables federation, keeps node features."""
import asyncio
from lib.mode import get_mode, is_federated, get_hub_urls
from lib.federation_client import can_announce
from lib.store import index_certificate, get_latest


def test_federated_mode_active(federated_mode):
    assert get_mode() == "federated"
    assert is_federated() is True
    assert len(get_hub_urls()) == 2


def test_federated_can_announce(federated_mode):
    assert can_announce() is True


def test_standalone_cannot_announce(standalone_mode):
    assert can_announce() is False


def test_federated_still_serves_badges(federated_mode, temp_store):
    async def flow():
        await index_certificate("test/b", {"score": 88, "repo": "test/b"})
        e = await get_latest("test/b")
        assert e["score"] == 88
    asyncio.run(flow())
