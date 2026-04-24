"""Database-health routes.

A single ``/db/ping`` endpoint that runs ``SELECT 1`` against the async
engine. Returns 503 when the DB is unreachable. Used by the Docker
health check + future monitoring.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text

from chipforge_api.db import get_engine

router = APIRouter(prefix="/db", tags=["db"])


class DbPingResponse(BaseModel):
    status: str
    result: int


@router.get("/ping", response_model=DbPingResponse)
async def ping() -> DbPingResponse:
    engine = get_engine()
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar_one()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"database unreachable: {type(exc).__name__}: {exc}",
        ) from exc

    return DbPingResponse(status="ok", result=int(value))
