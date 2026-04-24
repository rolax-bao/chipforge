"""Provider selection: build the right :class:`LLMProvider` at runtime."""

from __future__ import annotations

from chipforge_api.ai.openai_provider import OpenAIProvider, OpenAIProviderError
from chipforge_api.ai.provider import LLMProvider, MockProvider
from chipforge_api.config import Settings, get_settings


def build_provider(settings: Settings | None = None) -> LLMProvider:
    """Return the provider selected by ``AI_PROVIDER`` / ``OPENAI_API_KEY``.

    Selection rules:

    * ``AI_PROVIDER=mock`` — always the mock.
    * ``AI_PROVIDER=openai`` + non-empty ``OPENAI_API_KEY`` — real OpenAI.
    * ``AI_PROVIDER=openai`` + empty key — falls back to mock (dev ergonomics;
      surfaces in ``/health`` as ``ai_provider=mock``, so it's not silent).
    * Any other value (``anthropic``/``vllm``/``ollama``) — not yet wired;
      falls back to mock. They land in later PRs.
    """
    settings = settings or get_settings()
    if settings.ai_provider == "openai" and settings.openai_api_key:
        try:
            return OpenAIProvider.from_settings(
                api_key=settings.openai_api_key,
                base_url=settings.openai_base_url,
                default_model=settings.openai_model,
            )
        except OpenAIProviderError:
            return MockProvider()
    return MockProvider()
