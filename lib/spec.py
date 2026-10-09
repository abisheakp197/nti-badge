"""NTI-Cert/1 specification constants."""


CERT_SPEC = "NTI-Cert/1"


SUPPORTED_PROFILES = {
    "NTI-1": {"min_score": 50, "pillars": ["Identity", "Governance", "Consensus", "Audit", "Persistence"]},
}


TIERS = {
    "Platinum": 95,
    "Gold": 85,
    "Silver": 70,
    "Bronze": 50,
    "Unranked": 0,
}


SEVERITY_LEVELS = ["critical", "high", "medium", "low", "info"]


# OIDC providers the badge accepts (multi-ecosystem)
SUPPORTED_OIDC_ISSUERS = {
    "github": "https://token.actions.githubusercontent.com",
    "gitlab": "https://gitlab.com",
    "google": "https://accounts.google.com",
    "bitbucket": "https://api.bitbucket.org/2.0/workspaces",
    "azure": "https://login.microsoftonline.com",
}


def tier_for_score(score: int) -> str:
    if score >= 95: return "Platinum"
    if score >= 85: return "Gold"
    if score >= 70: return "Silver"
    if score >= 50: return "Bronze"
    return "Unranked"
