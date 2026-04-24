"""Integration tests against a live Postgres.

Exercises the migrated schema end-to-end: every table round-trips a row,
FK cascades work, and uniqueness constraints fire. Assumes ``alembic
upgrade head`` has been run against ``DATABASE_URL`` — both CI and the
``uv run pytest`` local recipe handle that.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from chipforge_api.models import (
    ChatMessage,
    ChatSession,
    File,
    FileVersion,
    Project,
    User,
)


async def _session(engine: AsyncEngine):
    factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return factory()


@pytest.mark.asyncio
async def test_pgvector_extension_is_enabled(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        row = await conn.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'vector'"))
        assert row.first() is not None, "pgvector extension missing — migration regressed"


@pytest.mark.asyncio
async def test_full_schema_roundtrip(engine: AsyncEngine) -> None:
    async with await _session(engine) as s:
        user = User(email=f"u-{uuid4().hex}@example.com", name="Alice")
        s.add(user)
        await s.flush()  # user.id materializes; needed for ChatSession.user_id below.

        project = Project(owner=user, name=f"proj-{uuid4().hex[:8]}")
        file = File(project=project, path="rtl/counter.v", language="verilog")
        version = FileVersion(file=file, content="module counter;\nendmodule\n")
        session = ChatSession(project=project, user_id=user.id, title="design review")
        msg_user = ChatMessage(session=session, role="user", content="explain this module")
        msg_assistant = ChatMessage(session=session, role="assistant", content="It's a counter.")

        s.add_all([project, file, version, session, msg_user, msg_assistant])
        await s.commit()

        # Re-fetch the message rows back ordered by created_at to check the index.
        messages = (
            (
                await s.execute(
                    select(ChatMessage)
                    .where(ChatMessage.session_id == session.id)
                    .order_by(ChatMessage.created_at)
                )
            )
            .scalars()
            .all()
        )
        assert [m.role for m in messages] == ["user", "assistant"]

        # Cleanup so later tests in the same process don't collide on unique email.
        await s.delete(user)
        await s.commit()


@pytest.mark.asyncio
async def test_unique_project_name_per_owner(engine: AsyncEngine) -> None:
    async with await _session(engine) as s:
        owner = User(email=f"owner-{uuid4().hex}@example.com")
        s.add(owner)
        await s.flush()
        s.add(Project(owner_id=owner.id, name="dup"))
        await s.commit()

    # Second session: inserting the same (owner_id, name) must blow up.
    async with await _session(engine) as s:
        owner_id = (
            await s.execute(select(User.id).where(User.email.like("owner-%")).limit(1))
        ).scalar_one()
        s.add(Project(owner_id=owner_id, name="dup"))
        with pytest.raises(IntegrityError):
            await s.commit()
        await s.rollback()

    # Cleanup.
    async with await _session(engine) as s:
        for u in (await s.execute(select(User).where(User.email.like("owner-%")))).scalars():
            await s.delete(u)
        await s.commit()


@pytest.mark.asyncio
async def test_cascade_delete_project_removes_files(engine: AsyncEngine) -> None:
    async with await _session(engine) as s:
        user = User(email=f"cascade-{uuid4().hex}@example.com")
        project = Project(owner=user, name="to-be-deleted")
        File(project=project, path="a.v", language="verilog")
        File(project=project, path="b.v", language="verilog")
        s.add_all([user, project])
        await s.commit()
        project_id = project.id

        await s.delete(project)
        await s.commit()

        remaining = (
            (await s.execute(select(File).where(File.project_id == project_id))).scalars().all()
        )
        assert remaining == []

        await s.delete(user)
        await s.commit()
