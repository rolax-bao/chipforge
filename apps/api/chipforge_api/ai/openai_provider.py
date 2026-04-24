"""OpenAI-backed implementation of :class:`LLMProvider`.

Streams tokens from the OpenAI Chat Completions API. Network calls are
fully handled by the async ``openai`` client; all business logic here is
just adaptation (our ``Message`` type → their schema, their SSE chunks →
our async string iterator).

No real API key is exercised at test time: every test in
``tests/test_openai_provider.py`` stubs the client via ``AsyncMock``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from chipforge_api.ai.provider import Message

if TYPE_CHECKING:
    from openai import AsyncOpenAI


class OpenAIProviderError(RuntimeError):
    """Raised when the OpenAI client cannot be constructed or used."""


class OpenAIProvider:
    """Concrete :class:`LLMProvider` backed by OpenAI's Chat Completions API.

    The client is injected for testability — production code calls
    :meth:`from_settings`, tests pass an ``AsyncMock``.
    """

    name = "openai"

    def __init__(
        self,
        client: AsyncOpenAI,
        *,
        default_model: str = "gpt-4o-mini",
        default_temperature: float = 0.2,
        embedding_model: str = "text-embedding-3-small",
    ) -> None:
        self._client = client
        self._default_model = default_model
        self._default_temperature = default_temperature
        self._embedding_model = embedding_model

    @classmethod
    def from_settings(
        cls,
        *,
        api_key: str,
        base_url: str,
        default_model: str,
    ) -> OpenAIProvider:
        """Build a provider from config. Fails fast if the SDK is absent."""
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover - dependency is declared
            raise OpenAIProviderError(
                "openai package is not installed; add it to apps/api/pyproject.toml"
            ) from exc

        if not api_key:
            raise OpenAIProviderError(
                "OPENAI_API_KEY is empty; set it or switch AI_PROVIDER to 'mock'"
            )

        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        return cls(client=client, default_model=default_model)

    async def chat(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Yield assistant tokens as they stream back from OpenAI."""
        payload: dict[str, Any] = {
            "model": model or self._default_model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else self._default_temperature,
            "stream": True,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        stream = await self._client.chat.completions.create(**payload)
        async for chunk in stream:
            # The SDK yields pydantic-like objects; choices[0].delta.content is
            # None on tool-call / role / stop chunks, which we skip.
            choices = getattr(chunk, "choices", None) or []
            if not choices:
                continue
            delta = getattr(choices[0], "delta", None)
            content = getattr(delta, "content", None) if delta is not None else None
            if content:
                yield content

    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        max_tokens: int = 256,
    ) -> str:
        """One-shot non-streaming completion used by inline-completion flows."""
        resp = await self._client.chat.completions.create(
            model=model or self._default_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens,
            stream=False,
        )
        choices = getattr(resp, "choices", None) or []
        if not choices:
            return ""
        message = getattr(choices[0], "message", None)
        return getattr(message, "content", "") or ""

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Batch-embed texts with the configured embedding model."""
        if not texts:
            return []
        resp = await self._client.embeddings.create(
            model=self._embedding_model,
            input=texts,
        )
        data = getattr(resp, "data", None) or []
        return [list(getattr(item, "embedding", []) or []) for item in data]
