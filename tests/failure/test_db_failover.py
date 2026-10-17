"""DB failure must never crash endpoints."""

import asyncio
from pathlib import Path
from unittest.mock import patch

from lib import db


def test_redis_unavailable_falls_back(temp_store: Path) -> None:
    with patch("lib.db._redis", return_value=None):
        db.BACKEND = None

        async def flow() -> None:
            await db.hset("test", "k", "v")
            assert await db.hget("test", "k") == "v"

        asyncio.run(flow())


def test_file_backend_creates_directory(temp_store: Path) -> None:
    db.BACKEND = None

    async def flow() -> None:
        await db.hset("test2", "k", "v")
        assert temp_store.exists()

    asyncio.run(flow())
