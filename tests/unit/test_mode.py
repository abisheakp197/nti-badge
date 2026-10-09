"""Unit tests for lib/mode.py"""
import pytest
from lib.mode import (
    get_mode, is_standalone, is_federated, is_hub, get_hub_urls, get_node_info
)


def test_default_mode_is_standalone(clean_env):
    assert get_mode() == "standalone"
    assert is_standalone() is True
    assert is_federated() is False
    assert is_hub() is False


def test_federated_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "federated")
    assert get_mode() == "federated"
    assert is_federated() is True
    assert is_hub() is False


def test_hub_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "hub")
    assert get_mode() == "hub"
    assert is_hub() is True


def test_invalid_mode_falls_back_to_standalone(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "garbage")
    assert get_mode() == "standalone"


def test_case_insensitive_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "HUB")
    assert get_mode() == "hub"


def test_hub_urls_parsing(monkeypatch):
    monkeypatch.setenv("NTI_HUB_URLS", "https://a.com, https://b.com , https://c.com")
    urls = get_hub_urls()
    assert urls == ["https://a.com", "https://b.com", "https://c.com"]


def test_hub_urls_empty(clean_env):
    assert get_hub_urls() == []


def test_node_info_shape(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "hub")
    monkeypatch.setenv("NTI_NODE_URL", "https://node.example/")
    monkeypatch.setenv("NTI_NODE_NAME", "my-node")
    info = get_node_info()
    assert info["mode"] == "hub"
    assert info["node_url"] == "https://node.example"
    assert info["hub_enabled"] is True
    assert info["federation_enabled"] is True
