"""AI gateway package.

Contains the LLMProvider protocol and concrete implementations
(Mock, OpenAI, Anthropic, vLLM, Ollama). Only the protocol and
MockProvider are wired up in the skeleton; real providers land in PR #7.
"""

from chipforge_api.ai.provider import LLMProvider, Message, MockProvider

__all__ = ["LLMProvider", "Message", "MockProvider"]
