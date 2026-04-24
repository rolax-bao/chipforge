# chipforge-api

FastAPI backend for ChipForge.

## Run locally

```bash
# from repo root
docker compose -f infra/docker-compose.yml up -d postgres

cd apps/api
uv sync --extra dev
cp ../../.env.example ../../.env
uv run alembic upgrade head
uv run uvicorn chipforge_api.main:app --reload --port 8000
```

Then visit http://localhost:8000/docs. Confirm the DB is wired via `GET /db/ping`.

## Tests

```bash
# Integration tests hit the live Postgres above.
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## Migrations

```bash
# Autogenerate a new migration after changing ORM models:
uv run alembic revision --autogenerate -m "describe the change"

# Apply / roll back:
uv run alembic upgrade head
uv run alembic downgrade -1
```

## Deploy (Fly.io)

```bash
fly launch --no-deploy --copy-config --config apps/api/fly.toml
fly secrets set JWT_SECRET=... DATABASE_URL=... --config apps/api/fly.toml
fly deploy --config apps/api/fly.toml
```

## Layout

- `chipforge_api/` — application package
  - `main.py` — FastAPI factory
  - `config.py` — `Settings` via pydantic-settings
  - `routes/` — HTTP route modules (`health`, `ai`, `db`)
  - `ai/` — `LLMProvider` protocol, `MockProvider`, `OpenAIProvider`, `build_provider()`
  - `db/` — declarative `Base`, async engine + session factory
  - `models.py` — ORM schema (users, projects, files, file_versions, chat_sessions, chat_messages)
  - `rag/` — retrieval-augmented generation (PR #11)
  - `jobs/` — async job orchestration (PR #15)
  - `services/` — business logic (filled incrementally)
- `alembic/` — DB migrations; first migration lives in `alembic/versions/20260424_0001_initial_core_schema.py`
- `tests/` — pytest suite
