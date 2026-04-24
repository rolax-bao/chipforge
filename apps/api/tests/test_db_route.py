"""End-to-end tests for ``GET /db/ping``."""

from __future__ import annotations

from fastapi.testclient import TestClient

from chipforge_api.main import create_app


def test_db_ping_returns_ok_against_live_postgres() -> None:
    # Relies on the session-wide DATABASE_URL (see conftest) pointing at a
    # migrated Postgres — CI provides a service container, local dev uses
    # `docker compose up -d postgres && uv run alembic upgrade head`.
    app = create_app()
    with TestClient(app) as client:
        resp = client.get("/db/ping")
    assert resp.status_code == 200
    body = resp.json()
    assert body == {"status": "ok", "result": 1}
