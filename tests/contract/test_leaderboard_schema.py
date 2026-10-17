"""Contract test: /api/leaderboard schema."""

import asyncio
from pathlib import Path

from lib.store import top_scores


def test_leaderboard_returns_list(temp_store: Path) -> None:
    result = asyncio.run(top_scores())
    assert isinstance(result, list)
