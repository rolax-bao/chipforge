"""FastAPI application entrypoint."""

from __future__ import annotations

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chipforge_api import __version__
from chipforge_api.config import get_settings
from chipforge_api.routes import ai, health

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="ChipForge backend API — auth, projects, AI gateway, job orchestrator.",
        docs_url="/docs",
        redoc_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(ai.router)

    logger.info("app_initialized", version=__version__, ai_provider=settings.ai_provider)
    return app


app = create_app()
