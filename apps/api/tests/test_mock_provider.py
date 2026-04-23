"""Tests for the MockProvider reference implementation."""

from __future__ import annotations

import pytest

from chipforge_api.ai import Message, MockProvider


@pytest.mark.asyncio
async def test_mock_chat_yields_tokens() -> None:
    provider = MockProvider()
    chunks: list[str] = []
    async for chunk in provider.chat([Message(role="user", content="write a 4-bit adder")]):
        chunks.append(chunk)
    assert chunks, "MockProvider.chat must yield at least one chunk"
    assert "mock" in "".join(chunks).lower()


@pytest.mark.asyncio
async def test_mock_complete_returns_string() -> None:
    provider = MockProvider()
    out = await provider.complete("module adder(")
    assert isinstance(out, str)
    assert out


@pytest.mark.asyncio
async def test_mock_embed_shape() -> None:
    provider = MockProvider()
    vecs = await provider.embed(["hello", "world"])
    assert len(vecs) == 2
    assert all(len(v) == 3 for v in vecs)
