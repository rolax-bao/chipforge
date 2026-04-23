# Contributing to ChipForge

Thanks for your interest! This doc covers the workflow, code style, and PR expectations.

## Workflow

1. Create a feature branch from `main`: `git checkout -b devin/<timestamp>-<short-description>` (or your own naming).
2. Make focused changes — one concern per PR.
3. Run `pnpm lint && pnpm typecheck && pnpm test` (JS) and `uv run ruff check . && uv run pytest` (Python) before pushing.
4. Open a PR against `main`. Fill out the PR template.
5. CI must be green before merge.

## Code Style

- **TypeScript**: ESLint + Prettier (config in root). 2-space indent, single quotes, trailing commas.
- **Python**: Ruff (lint + format) + Pyright (typecheck). 4-space indent. Type-annotate all public functions.
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.

## Directory Conventions

- New UI components go under `apps/web/components/` or shared ones under `packages/ui/`.
- New API routes go under `apps/api/chipforge_api/routes/`, services under `services/`.
- LLM prompts live in `docs/prompts/` as YAML and are loaded by `apps/api/chipforge_api/ai/`.

## PR Expectations

- Include a summary of **what** and **why**.
- Link to any related issue or architecture doc section.
- For UI changes, include a screenshot or short recording.
- For API changes, include example request/response.
- Add or update tests for any new behavior.

## Architecture Decisions

Non-trivial design choices go in `docs/adr/` as numbered ADRs. See `docs/adr/0001-monorepo-layout.md` for the template.
