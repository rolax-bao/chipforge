"""Tests for provider selection in :mod:`chipforge_api.ai.factory`."""

from __future__ import annotations

from chipforge_api.ai import MockProvider, OpenAIProvider, build_provider
from chipforge_api.config import Settings


def test_default_settings_select_mock_provider() -> None:
    provider = build_provider(Settings(ai_provider="mock"))
    assert isinstance(provider, MockProvider)


def test_openai_with_empty_key_falls_back_to_mock() -> None:
    # AI_PROVIDER=openai but no key → mock (documented behavior).
    provider = build_provider(Settings(ai_provider="openai", openai_api_key=""))
    assert isinstance(provider, MockProvider)


def test_openai_with_key_returns_openai_provider() -> None:
    settings = Settings(
        ai_provider="openai",
        openai_api_key="sk-test-not-real",
        openai_base_url="https://api.openai.com/v1",
        openai_model="gpt-4o-mini",
    )
    provider = build_provider(settings)
    assert isinstance(provider, OpenAIProvider)
    assert provider.name == "openai"


def test_unwired_provider_falls_back_to_mock() -> None:
    # anthropic / vllm / ollama land in later PRs; for now → mock.
    for name in ("anthropic", "vllm", "ollama"):
        provider = build_provider(Settings(ai_provider=name))  # type: ignore[arg-type]
        assert isinstance(provider, MockProvider), f"{name} should fall back"
