"""Hub mode adds aggregation endpoints."""
import asyncio
from lib.mode import get_mode, is_hub
from lib.hub_store import register_node, list_nodes, register_hub, list_hubs


def test_hub_mode_active(hub_mode):
    assert get_mode() == "hub"
    assert is_hub() is True


def test_register_and_list_nodes(hub_mode, temp_store):
    async def flow():
        entry = await register_node("https://node1.example.com", {"name": "Node 1"})
        assert entry["url"] == "https://node1.example.com"
        nodes = await list_nodes()
        assert len(nodes) == 1
        assert nodes[0]["name"] == "Node 1"
    asyncio.run(flow())


def test_register_and_list_hubs(hub_mode, temp_store):
    async def flow():
        await register_hub("https://hub1.example.com", {"name": "Hub 1"})
        hubs = await list_hubs()
        assert len(hubs) == 1
    asyncio.run(flow())


def test_hub_handles_duplicate(hub_mode, temp_store):
    async def flow():
        await register_node("https://dup.example.com", {"name": "Dup"})
        await register_node("https://dup.example.com", {"name": "Dup Updated"})
        nodes = await list_nodes()
        assert len(nodes) == 1
        assert nodes[0]["name"] == "Dup Updated"
    asyncio.run(flow())
