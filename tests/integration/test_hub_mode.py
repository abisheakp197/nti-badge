"""Hub mode adds aggregation endpoints."""

import asyncio
from pathlib import Path

from lib.hub_store import list_hubs, list_nodes, register_hub, register_node
from lib.mode import get_mode, is_hub


def test_hub_mode_active(hub_mode: str) -> None:
    assert get_mode() == "hub"
    assert is_hub() is True


def test_register_and_list_nodes(hub_mode: str, temp_store: Path) -> None:
    async def flow() -> None:
        entry = await register_node("https://node1.example.com", {"name": "Node 1"})
        assert entry["url"] == "https://node1.example.com"
        nodes = await list_nodes()
        assert len(nodes) == 1
        assert nodes[0]["name"] == "Node 1"

    asyncio.run(flow())


def test_register_and_list_hubs(hub_mode: str, temp_store: Path) -> None:
    async def flow() -> None:
        await register_hub("https://hub1.example.com", {"name": "Hub 1"})
        hubs = await list_hubs()
        assert len(hubs) == 1

    asyncio.run(flow())


def test_hub_handles_duplicate(hub_mode: str, temp_store: Path) -> None:
    async def flow() -> None:
        await register_node("https://dup.example.com", {"name": "Dup"})
        await register_node("https://dup.example.com", {"name": "Dup Updated"})
        nodes = await list_nodes()
        assert len(nodes) == 1
        assert nodes[0]["name"] == "Dup Updated"

    asyncio.run(flow())
