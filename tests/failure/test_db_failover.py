"""DB failure must never crash endpoints."""
import asyncio
from unittest.mock import patch


def test_redis_unavailable_falls_back(temp_store):
    with patch("lib.db._redis", return_value=None):
        from lib import db
        db.BACKEND = None
        async def flow():
            await db.hset("test", "k", "v")
            assert await db.hget("test", "k") == "v"
        asyncio.run(flow())


def test_file_backend_creates_directory(temp_store):
    from lib import db
    db.BACKEND = None
    async def flow():
        await db.hset("test2", "k", "v")
        assert temp_store.exists()
    asyncio.run(flow())
