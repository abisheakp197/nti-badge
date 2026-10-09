"""Standalone mode works with no federation."""
import asyncio
from lib.mode import get_mode, is_standalone, get_node_info
from lib.store import index_certificate, get_latest, list_all


def test_standalone_is_default(clean_env, temp_store):
    assert get_mode() == "standalone"
    assert is_standalone() is True


def test_standalone_can_index_and_retrieve(temp_store):
    async def flow():
        await index_certificate("test/a", {"score": 90, "tier": "Gold", "repo": "test/a"})
        entry = await get_latest("test/a")
        assert entry["score"] == 90
        entries = await list_all()
        assert len(entries) == 1
    asyncio.run(flow())


def test_standalone_federation_disabled(standalone_mode):
    info = get_node_info()
    assert info["federation_enabled"] is False
