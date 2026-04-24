"""AI gateway package.

Holds the :class:`LLMProvider` protocol and concrete implementations
(Mock, OpenAI; Anthropic/vLLM/Ollama land in later PRs). Use
:func:`build_provider` to get the provider selected by environment
variables.
"""

from chipforge_api.ai.factory import build_provider
from chipforge_api.ai.openai_provider import OpenAIProvider, OpenAIProviderError
from chipforge_api.ai.provider import LLMProvider, Message, MockProvider

__all__ = [
    "LLMProvider",
    "Message",
    "MockProvider",
    "OpenAIProvider",
    "OpenAIProviderError",
    "build_provider",
]
