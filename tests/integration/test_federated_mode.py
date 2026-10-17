"""Federated mode enables federation, keeps node features."""

import asyncio
from pathlib import Path

from lib.federation_client import can_announce
from lib.mode import get_hub_urls, get_mode, is_federated
from lib.store import get_latest, index_certificate


def test_federated_mode_active(federated_mode: str) -> None:
    assert get_mode() == "federated"
    assert is_federated() is True
    assert len(get_hub_urls()) == 2


def test_federated_can_announce(federated_mode: str) -> None:
    assert can_announce() is True


def test_standalone_cannot_announce(standalone_mode: str) -> None:
    assert can_announce() is False


def test_federated_still_serves_badges(federated_mode: str, temp_store: Path) -> None:
    async def flow() -> None:
        await index_certificate("test/b", {"score": 88, "repo": "test/b"})
        e = await get_latest("test/b")
        assert e is not None
        assert e["score"] == 88

    asyncio.run(flow())
