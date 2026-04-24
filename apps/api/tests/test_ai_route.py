"""End-to-end tests for ``POST /ai/chat``.

These tests use FastAPI's ``TestClient`` against the real app factory
and override the ``get_provider`` dependency to inject a deterministic
mock. No network, no OpenAI key.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi.testclient import TestClient

from chipforge_api.ai import Message
from chipforge_api.main import create_app
from chipforge_api.routes.ai import get_provider


class _ScriptedProvider:
    """Provider that yields a fixed sequence of tokens."""

    name = "scripted"

    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens

    async def chat(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        for t in self._tokens:
            yield t

    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        max_tokens: int = 256,
    ) -> str:
        return "".join(self._tokens)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


def _make_client(tokens: list[str]) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_provider] = lambda: _ScriptedProvider(tokens)
    return TestClient(app)


def test_chat_streams_sse_token_events() -> None:
    client = _make_client(["Hello, ", "world!"])

    with client.stream(
        "POST",
        "/ai/chat",
        json={"messages": [{"role": "user", "content": "hi"}]},
    ) as resp:
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")
        body = b"".join(resp.iter_bytes()).decode()

    # Expect two token events then a terminal done event, in order.
    assert 'data: {"token": "Hello, "}' in body
    assert 'data: {"token": "world!"}' in body
    assert "event: done" in body
    assert body.index("Hello, ") < body.index("world!") < body.index("event: done")


def test_chat_rejects_request_without_user_message() -> None:
    client = _make_client(["irrelevant"])

    resp = client.post(
        "/ai/chat",
        json={"messages": [{"role": "system", "content": "be helpful"}]},
    )
    assert resp.status_code == 400
    assert "user message" in resp.json()["detail"]


def test_chat_rejects_empty_messages_list() -> None:
    client = _make_client(["x"])

    resp = client.post("/ai/chat", json={"messages": []})
    # Pydantic v2 validation error → 422
    assert resp.status_code == 422
