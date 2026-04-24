"""AI gateway HTTP routes.

Single endpoint ``POST /ai/chat`` streams assistant tokens as
Server-Sent Events. The body is a list of ``{role, content}`` messages
matching :class:`chipforge_api.ai.provider.Message`.

Why SSE rather than WebSocket: this endpoint is strictly one-way
(server → client) and SSE round-trips through HTTP intermediaries
cleanly. Multi-turn chat + cancellation will move to WS in PR #9 if
needed.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from chipforge_api.ai import LLMProvider, Message, build_provider

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=4096)


def get_provider() -> LLMProvider:
    """FastAPI dependency — overridden in tests via ``app.dependency_overrides``."""
    return build_provider()


async def _sse_stream(
    provider: LLMProvider,
    request: ChatRequest,
) -> AsyncIterator[bytes]:
    domain_messages = [Message(role=m.role, content=m.content) for m in request.messages]
    try:
        async for token in provider.chat(
            domain_messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        ):
            # One SSE event per token, JSON payload so the client can
            # distinguish token chunks from future metadata events.
            yield f"data: {json.dumps({'token': token})}\n\n".encode()
    except Exception as exc:  # pragma: no cover - defensive
        payload = json.dumps({"error": type(exc).__name__, "detail": str(exc)})
        yield f"event: error\ndata: {payload}\n\n".encode()
        return
    yield b"event: done\ndata: {}\n\n"


ProviderDep = Depends(get_provider)


@router.post("/chat")
async def chat(
    request: ChatRequest,
    provider: LLMProvider = ProviderDep,
) -> StreamingResponse:
    """Stream assistant tokens as Server-Sent Events."""
    if not any(m.role == "user" for m in request.messages):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="at least one user message is required",
        )
    return StreamingResponse(
        _sse_stream(provider, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )
