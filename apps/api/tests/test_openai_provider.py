"""Tests for :class:`OpenAIProvider`.

None of these tests make a real network call. We inject an ``AsyncMock``
client so the test suite is deterministic and works without an API key.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from chipforge_api.ai import Message, OpenAIProvider, OpenAIProviderError


def _make_stream_chunk(content: str | None) -> SimpleNamespace:
    """Shape-compatible stand-in for an OpenAI streaming chunk."""
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=content))])


class _AsyncIter:
    """Minimal async iterator that yields preset chunks."""

    def __init__(self, chunks: list[Any]) -> None:
        self._chunks = list(chunks)

    def __aiter__(self) -> _AsyncIter:
        return self

    async def __anext__(self) -> Any:
        if not self._chunks:
            raise StopAsyncIteration
        return self._chunks.pop(0)


def _fake_client(stream_chunks: list[Any] | None = None, completion: Any = None) -> AsyncMock:
    """Build a client whose ``chat.completions.create`` returns our fake stream."""
    client = AsyncMock()
    if stream_chunks is not None:

        async def _create(**_kwargs: Any) -> _AsyncIter:
            return _AsyncIter(stream_chunks)

        client.chat.completions.create = _create  # type: ignore[method-assign]
    if completion is not None:
        client.chat.completions.create = AsyncMock(return_value=completion)  # type: ignore[method-assign]
    return client


@pytest.mark.asyncio
async def test_chat_yields_only_non_empty_content() -> None:
    chunks = [
        _make_stream_chunk("Hello "),
        _make_stream_chunk(None),  # role / stop chunk — skipped
        _make_stream_chunk("world"),
        _make_stream_chunk(""),  # empty — skipped
    ]
    provider = OpenAIProvider(client=_fake_client(stream_chunks=chunks))

    tokens: list[str] = []
    async for t in provider.chat([Message(role="user", content="hi")]):
        tokens.append(t)

    assert tokens == ["Hello ", "world"]


@pytest.mark.asyncio
async def test_chat_handles_empty_choices_list() -> None:
    chunks = [
        SimpleNamespace(choices=[]),  # corner case: no choices on chunk
        _make_stream_chunk("ok"),
    ]
    provider = OpenAIProvider(client=_fake_client(stream_chunks=chunks))

    tokens = [t async for t in provider.chat([Message(role="user", content="hi")])]
    assert tokens == ["ok"]


@pytest.mark.asyncio
async def test_chat_forwards_model_and_temperature() -> None:
    seen: dict[str, Any] = {}

    async def _create(**kwargs: Any) -> _AsyncIter:
        seen.update(kwargs)
        return _AsyncIter([_make_stream_chunk("x")])

    client = AsyncMock()
    client.chat.completions.create = _create  # type: ignore[method-assign]
    provider = OpenAIProvider(client=client, default_model="gpt-default")

    async for _ in provider.chat(
        [Message(role="user", content="hi")],
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=123,
    ):
        pass

    assert seen["model"] == "gpt-4o-mini"
    assert seen["messages"] == [{"role": "user", "content": "hi"}]
    assert seen["temperature"] == 0.7
    assert seen["max_tokens"] == 123
    assert seen["stream"] is True


@pytest.mark.asyncio
async def test_chat_uses_default_model_when_none() -> None:
    seen: dict[str, Any] = {}

    async def _create(**kwargs: Any) -> _AsyncIter:
        seen.update(kwargs)
        return _AsyncIter([_make_stream_chunk("x")])

    client = AsyncMock()
    client.chat.completions.create = _create  # type: ignore[method-assign]
    provider = OpenAIProvider(client=client, default_model="gpt-default")

    async for _ in provider.chat([Message(role="user", content="hi")]):
        pass

    assert seen["model"] == "gpt-default"
    assert "max_tokens" not in seen  # not forwarded when caller didn't set one


@pytest.mark.asyncio
async def test_complete_returns_assistant_content() -> None:
    completion = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="module foo();\n"))]
    )
    provider = OpenAIProvider(client=_fake_client(completion=completion))

    out = await provider.complete("module foo(")
    assert out == "module foo();\n"


@pytest.mark.asyncio
async def test_complete_returns_empty_when_no_choices() -> None:
    completion = SimpleNamespace(choices=[])
    provider = OpenAIProvider(client=_fake_client(completion=completion))
    assert await provider.complete("prompt") == ""


@pytest.mark.asyncio
async def test_embed_batches_and_returns_vectors() -> None:
    resp = SimpleNamespace(
        data=[
            SimpleNamespace(embedding=[0.1, 0.2]),
            SimpleNamespace(embedding=[0.3, 0.4]),
        ]
    )
    client = AsyncMock()
    client.embeddings.create = AsyncMock(return_value=resp)
    provider = OpenAIProvider(client=client)

    vecs = await provider.embed(["hello", "world"])
    assert vecs == [[0.1, 0.2], [0.3, 0.4]]


@pytest.mark.asyncio
async def test_embed_short_circuits_on_empty_input() -> None:
    client = AsyncMock()
    provider = OpenAIProvider(client=client)
    assert await provider.embed([]) == []
    client.embeddings.create.assert_not_called()


def test_from_settings_rejects_empty_api_key() -> None:
    with pytest.raises(OpenAIProviderError):
        OpenAIProvider.from_settings(api_key="", base_url="x", default_model="y")
