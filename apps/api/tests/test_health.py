"""Smoke tests for the health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from chipforge_api.main import app


def test_health_returns_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"]
    assert data["ai_provider"] in {"mock", "openai", "anthropic", "vllm", "ollama"}


def test_root_returns_message() -> None:
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "ChipForge" in response.json()["message"]
