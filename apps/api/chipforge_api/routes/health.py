"""Health-check routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from chipforge_api import __version__
from chipforge_api.config import get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str
    ai_provider: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness probe used by Fly.io, Docker Compose, and uptime checks."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version=__version__,
        service=settings.app_name,
        ai_provider=settings.ai_provider,
    )


@router.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"message": "ChipForge API. See /docs for OpenAPI."}
