"""Async engine + session factory.

The engine is lazily constructed on first use so that test suites
(which monkeypatch ``DATABASE_URL``) pick up the override. Call
:func:`dispose_engine` to reset — tests do that in fixtures.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import cast

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from chipforge_api.config import get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Return (and cache) the async engine for the current settings."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            future=True,
        )
    return _engine


def async_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return a shared session factory bound to the cached engine."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return cast(async_sessionmaker[AsyncSession], _session_factory)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency — yields an :class:`AsyncSession` per request."""
    factory = async_session_factory()
    async with factory() as session:
        yield session


async def dispose_engine() -> None:
    """Close the engine. Call on app shutdown or when resetting settings."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None
