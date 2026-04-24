"""Shared pytest fixtures.

``DATABASE_URL`` selects the live Postgres the integration tests run
against — CI supplies a service container and local dev uses
``docker compose up -d postgres``. Tests that don't need a DB simply
don't request any of the fixtures below.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DEFAULT_DATABASE_URL = "postgresql+asyncpg://chipforge:chipforge@localhost:5432/chipforge"


def _database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


@pytest.fixture(scope="session")
def database_url() -> str:
    return _database_url()


@pytest_asyncio.fixture()
async def engine() -> AsyncIterator[AsyncEngine]:
    """Per-test async engine. Cheap; keeps settings mutations isolated."""
    eng = create_async_engine(_database_url(), pool_pre_ping=True, future=True)
    try:
        yield eng
    finally:
        await eng.dispose()
