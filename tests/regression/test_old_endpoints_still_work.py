"""Old API contract must not break."""

import asyncio
from pathlib import Path

from lib.store import list_all, list_by_org, top_scores


def test_list_all_returns_list(temp_store: Path) -> None:
    assert isinstance(asyncio.run(list_all()), list)


def test_top_scores_returns_list(temp_store: Path) -> None:
    assert isinstance(asyncio.run(top_scores()), list)


def test_list_by_org_returns_list(temp_store: Path) -> None:
    assert isinstance(asyncio.run(list_by_org("test")), list)
