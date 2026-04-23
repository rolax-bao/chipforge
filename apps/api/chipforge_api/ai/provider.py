"""LLMProvider protocol and reference MockProvider.

This file establishes the interface that all concrete AI backends
(OpenAI, Anthropic, vLLM, Ollama) must satisfy. Real providers land in PR #7.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class Message:
    """A single chat message."""

    role: Literal["system", "user", "assistant"]
    content: str


class LLMProvider(Protocol):
    """Common interface across all model providers."""

    name: str

    async def chat(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Yield assistant tokens as they are produced."""
        ...

    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        max_tokens: int = 256,
    ) -> str:
        """One-shot completion (used for inline / FIM completion in PR #9)."""
        ...

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Return dense embeddings for a batch of texts."""
        ...


class MockProvider:
    """Deterministic, dependency-free provider for tests and offline dev."""

    name = "mock"

    async def chat(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        last_user = next((m for m in reversed(messages) if m.role == "user"), None)
        prefix = "[mock] " if last_user is None else f"[mock reply to: {last_user.content[:40]!r}] "
        for chunk in (prefix, "real providers land in PR #7. "):
            yield chunk

    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        max_tokens: int = 256,
    ) -> str:
        return f"// mock completion for: {prompt[:60]}\n"

    async def embed(self, texts: list[str]) -> list[list[float]]:
        # Trivial deterministic "embedding": length-3 float vector per text.
        return [[float(len(t)), 0.0, 0.0] for t in texts]
