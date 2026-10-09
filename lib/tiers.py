"""Compliance tier logic."""
from lib.spec import tier_for_score, TIERS




TIER_COLORS = {
    "Platinum": "#e5e4e2",
    "Gold": "#ffd700",
    "Silver": "#c0c0c0",
    "Bronze": "#cd7f32",
    "Unranked": "#6b7280",
}


TIER_BADGES = {
    "Platinum": "🏆",
    "Gold": "🥇",
    "Silver": "🥈",
    "Bronze": "🥉",
    "Unranked": "⬜",
}




def assign_tier(score: int) -> str:
    return tier_for_score(score)




def tier_metadata(tier: str) -> dict:
    return {
        "name": tier,
        "color": TIER_COLORS.get(tier, "#888"),
        "emoji": TIER_BADGES.get(tier, ""),
        "threshold": TIERS.get(tier, 0),
    }
