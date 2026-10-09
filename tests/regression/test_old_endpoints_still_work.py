"""Old API contract must not break."""
import asyncio
from lib.store import list_all, top_scores, list_by_org


def test_list_all_returns_list(temp_store):
    assert isinstance(asyncio.run(list_all()), list)


def test_top_scores_returns_list(temp_store):
    assert isinstance(asyncio.run(top_scores()), list)


def test_list_by_org_returns_list(temp_store):
    assert isinstance(asyncio.run(list_by_org("test")), list)
