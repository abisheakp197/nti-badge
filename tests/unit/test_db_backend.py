"""Unit tests for lib/db.py backend selection."""
import pytest
from lib import db


def test_backend_file_when_no_env(clean_env):
    db.BACKEND = None
    assert db.get_backend() == "file"


def test_backend_redis_when_kv_url(monkeypatch):
    monkeypatch.setenv("KV_URL", "redis://localhost:6379")
    db.BACKEND = None
    assert db.get_backend() == "redis"


def test_backend_redis_when_redis_url(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "rediss://localhost:6379")
    db.BACKEND = None
    assert db.get_backend() == "redis"


def test_backend_upstash_rest(monkeypatch):
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://upstash.example.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "token123")
    db.BACKEND = None
    assert db.get_backend() == "upstash_rest"


def test_backend_info_structure(clean_env):
    db.BACKEND = None
    info = db.backend_info()
    assert "backend" in info
    assert "env_detected" in info
    assert info["backend"] == "file"


def test_kv_url_takes_priority_over_upstash(monkeypatch):
    monkeypatch.setenv("KV_URL", "redis://localhost")
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://upstash.example.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "token")
    db.BACKEND = None
    assert db.get_backend() == "redis"
