# ADR 0001: Monorepo layout (pnpm workspaces + Turborepo + uv)

- **Status**: Accepted
- **Date**: 2026-04-23

## Context

ChipForge has a TypeScript frontend (Next.js), a Python backend (FastAPI), and several
shared packages (AI types, Verilog language contribution, UI components, WASM wrappers).
Each technology has its own preferred monorepo tooling.

## Decision

Use **pnpm workspaces + Turborepo** for all JS/TS packages (apps/web, packages/\*), and
**uv** for the single Python package (apps/api). The two coexist at the repo root
without a cross-language meta-build; CI runs the JS and Python pipelines in separate
jobs.

- `pnpm-workspace.yaml` lists `apps/*` and `packages/*`.
- `turbo.json` declares `build`, `dev`, `lint`, `typecheck`, `test` tasks.
- `apps/api/pyproject.toml` + `uv.lock` manages the Python side independently.

## Consequences

- One `pnpm install` covers the entire JS graph including the Next.js app.
- Shared packages can import types/utilities without publishing.
- Python contributors don't need Node installed to iterate on the API (beyond running
  the combined `docker compose` stack).
- CI has two jobs (web, api) that can fail independently for clearer signals.

## Alternatives considered

- **Nx**: more features but heavier config; overkill at current scale.
- **Rush**: TypeScript-centric; awkward for Python.
- **Single tool (poetry workspaces, pants)**: poetry doesn't cover JS; pants has a steep
  learning curve and high CI cost for a 2-language repo.
