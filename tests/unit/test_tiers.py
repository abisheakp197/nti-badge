"""Unit tests for lib/tiers.py"""
from lib.tiers import assign_tier, tier_metadata


def test_tier_boundaries():
    assert assign_tier(100) == "Platinum"
    assert assign_tier(95) == "Platinum"
    assert assign_tier(94) == "Gold"
    assert assign_tier(85) == "Gold"
    assert assign_tier(84) == "Silver"
    assert assign_tier(70) == "Silver"
    assert assign_tier(69) == "Bronze"
    assert assign_tier(50) == "Bronze"
    assert assign_tier(49) == "Unranked"


def test_tier_metadata():
    m = tier_metadata("Platinum")
    assert m["name"] == "Platinum"
    assert "color" in m
    assert "emoji" in m
