"""NTI deployment mode system.

Standalone (default): Private node. No federation. No hub.
Federated: Node publishes its index to one or more hubs.
Hub: Node aggregates indexes from other nodes. Can federate with other hubs.
"""

import os
from typing import Literal


Mode = Literal["standalone", "federated", "hub"]


def get_mode() -> Mode:
    raw = os.environ.get("NTI_MODE", "standalone").strip().lower()
    if raw not in ("standalone", "federated", "hub"):
        return "standalone"
    return raw  # type: ignore


def is_standalone() -> bool:
    return get_mode() == "standalone"


def is_federated() -> bool:
    return get_mode() == "federated"


def is_hub() -> bool:
    return get_mode() == "hub"


def get_hub_urls() -> list:
    raw = os.environ.get("NTI_HUB_URLS", "").strip()
    if not raw:
        return []
    return [u.strip().rstrip("/") for u in raw.split(",") if u.strip()]


def get_node_info() -> dict:
    return {
        "mode": get_mode(),
        "node_url": os.environ.get("NTI_NODE_URL", "").rstrip("/"),
        "node_name": os.environ.get("NTI_NODE_NAME", "unnamed-node"),
        "node_description": os.environ.get("NTI_NODE_DESCRIPTION", ""),
        "federation_enabled": not is_standalone(),
        "hub_enabled": is_hub(),
        "hub_urls": get_hub_urls(),
        "contact": os.environ.get("NTI_NODE_CONTACT", ""),
    }
