"""initial core schema: users, projects, files, file_versions, chat_sessions, chat_messages

Also enables the pgvector extension so PR #11 can add embedding columns
without a separate extension migration. The sequence of CREATE TABLEs
mirrors ORM definitions in :mod:`chipforge_api.models` and was bootstrapped
from Alembic autogenerate, then hand-tidied for readability.

Revision ID: 0001_initial_core_schema
Revises:
Create Date: 2026-04-24

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_initial_core_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


TIMESTAMP_COLS = (
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
)


def upgrade() -> None:
    # RAG embeddings land in PR #11; enable the extension now so adding
    # a vector column later is a single ALTER TABLE.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("github_id", sa.String(length=64), nullable=True),
        *TIMESTAMP_COLS,
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("github_id", name="uq_users_github_id"),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "owner_id",
            sa.UUID(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        *TIMESTAMP_COLS,
        sa.UniqueConstraint("owner_id", "name", name="uq_projects_owner_name"),
    )
    op.create_index("ix_projects_owner_id", "projects", ["owner_id"])

    op.create_table(
        "files",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "project_id",
            sa.UUID(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.Column(
            "language",
            sa.String(length=40),
            nullable=False,
            server_default=sa.text("'plaintext'"),
        ),
        *TIMESTAMP_COLS,
        sa.UniqueConstraint("project_id", "path", name="uq_files_project_path"),
    )
    op.create_index("ix_files_project_id", "files", ["project_id"])

    op.create_table(
        "file_versions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "file_id",
            sa.UUID(),
            sa.ForeignKey("files.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "author_id",
            sa.UUID(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_file_versions_file_id_created_at",
        "file_versions",
        ["file_id", "created_at"],
    )

    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "project_id",
            sa.UUID(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.UUID(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False,
            server_default=sa.text("'New chat'"),
        ),
        *TIMESTAMP_COLS,
    )
    op.create_index("ix_chat_sessions_project_id", "chat_sessions", ["project_id"])
    op.create_index("ix_chat_sessions_user_id", "chat_sessions", ["user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "session_id",
            sa.UUID(),
            sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_chat_messages_session_id_created_at",
        "chat_messages",
        ["session_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_chat_messages_session_id_created_at", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("ix_chat_sessions_user_id", table_name="chat_sessions")
    op.drop_index("ix_chat_sessions_project_id", table_name="chat_sessions")
    op.drop_table("chat_sessions")
    op.drop_index("ix_file_versions_file_id_created_at", table_name="file_versions")
    op.drop_table("file_versions")
    op.drop_index("ix_files_project_id", table_name="files")
    op.drop_table("files")
    op.drop_index("ix_projects_owner_id", table_name="projects")
    op.drop_table("projects")
    op.drop_table("users")
    # We intentionally don't drop the 'vector' extension — other
    # deployments may share the DB cluster; a future migration can
    # drop it explicitly if this is the only user.
