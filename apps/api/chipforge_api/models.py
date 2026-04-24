"""ORM models for the ChipForge core schema.

Six tables cover the MVP's persistent state:

* ``users`` — minimal identity, populated by GitHub OAuth in PR #4.
* ``projects`` — owned by a user, holds files + chat sessions.
* ``files`` — path metadata inside a project (content lives in versions).
* ``file_versions`` — append-only content history; latest version per file
  is the source of truth for "current" text.
* ``chat_sessions`` — a named AI conversation scoped to a project.
* ``chat_messages`` — append-only chat turns, feeds the RAG pipeline.

Vector embeddings for files (pgvector column) land in PR #11 when RAG
goes online; the extension is enabled in the initial migration so
adding a column later is a one-liner.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chipforge_api.db.base import Base, CreatedAtMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_id: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)

    projects: Mapped[list[Project]] = relationship(
        back_populates="owner", cascade="all, delete", passive_deletes=True
    )


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("owner_id", "name", name="uq_projects_owner_name"),)

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    owner: Mapped[User] = relationship(back_populates="projects")
    files: Mapped[list[File]] = relationship(
        back_populates="project", cascade="all, delete", passive_deletes=True
    )
    chat_sessions: Mapped[list[ChatSession]] = relationship(
        back_populates="project", cascade="all, delete", passive_deletes=True
    )


class File(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "files"
    __table_args__ = (UniqueConstraint("project_id", "path", name="uq_files_project_path"),)

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    # Human-friendly language id (verilog / systemverilog / markdown / ...).
    # Not a DB enum so new languages don't require a migration.
    language: Mapped[str] = mapped_column(String(40), nullable=False, default="plaintext")

    project: Mapped[Project] = relationship(back_populates="files")
    versions: Mapped[list[FileVersion]] = relationship(
        back_populates="file", cascade="all, delete-orphan", passive_deletes=True
    )


class FileVersion(Base, UUIDMixin, CreatedAtMixin):
    __tablename__ = "file_versions"
    __table_args__ = (Index("ix_file_versions_file_id_created_at", "file_id", "created_at"),)

    file_id: Mapped[UUID] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    file: Mapped[File] = relationship(back_populates="versions")


class ChatSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "chat_sessions"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, default="New chat")

    project: Mapped[Project] = relationship(back_populates="chat_sessions")
    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="session", cascade="all, delete-orphan", passive_deletes=True
    )


class ChatMessage(Base, UUIDMixin, CreatedAtMixin):
    __tablename__ = "chat_messages"
    __table_args__ = (Index("ix_chat_messages_session_id_created_at", "session_id", "created_at"),)

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[ChatSession] = relationship(back_populates="messages")
