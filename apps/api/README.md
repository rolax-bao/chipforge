# chipforge-api

FastAPI backend for ChipForge.

## Run locally

```bash
cd apps/api
uv sync
cp ../../.env.example ../../.env
uv run uvicorn chipforge_api.main:app --reload --port 8000
```

Then visit http://localhost:8000/docs.

## Tests

```bash
uv run pytest
uv run ruff check .
uv run pyright
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
  - `routes/` — HTTP route modules (currently just `health`)
  - `ai/` — `LLMProvider` protocol + `MockProvider`; real backends land in PR #7
  - `rag/` — retrieval-augmented generation (PR #13)
  - `jobs/` — async job orchestration (PR #15)
  - `models/`, `services/` — ORM + business logic (filled incrementally)
- `alembic/` — DB migrations (first migration lands in PR #3)
- `tests/` — pytest suite
