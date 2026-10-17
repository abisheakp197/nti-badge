"""Standalone mode works with no federation."""

import asyncio
from pathlib import Path

from lib.mode import get_mode, get_node_info, is_standalone
from lib.store import get_latest, index_certificate, list_all


def test_standalone_is_default(clean_env: None, temp_store: Path) -> None:
    assert get_mode() == "standalone"
    assert is_standalone() is True


def test_standalone_can_index_and_retrieve(temp_store: Path) -> None:
    async def flow() -> None:
        await index_certificate("test/a", {"score": 90, "tier": "Gold", "repo": "test/a"})
        entry = await get_latest("test/a")
        assert entry is not None
        assert entry["score"] == 90
        entries = await list_all()
        assert len(entries) == 1

    asyncio.run(flow())


def test_standalone_federation_disabled(standalone_mode: str) -> None:
    info = get_node_info()
    assert info["federation_enabled"] is False
