# ChipForge

> Web AI IDE for chip design engineers — RTL, verification, synthesis, simulation with an AI copilot.

[![CI](https://github.com/rolax-bao/chipforge/actions/workflows/ci.yml/badge.svg)](https://github.com/rolax-bao/chipforge/actions/workflows/ci.yml)

ChipForge is a browser-native IDE that puts AI at the center of the digital-design workflow. Write Verilog / SystemVerilog, get inline completions, ask questions about your project, generate testbenches, run simulation in-browser (via WASM), and view waveforms — all without installing a local toolchain.

## Status

**Bootstrapping (MVP, week 1).** This PR sets up the monorepo skeleton, CI, Docker Compose, and deploy scaffolding. No feature code yet — see [`docs/architecture.md`](./docs/architecture.md) for the full technical proposal and roadmap.

## Repository Layout

```
chipforge/
├── apps/
│   ├── web/        # Next.js 14 frontend (Monaco editor + AI sidebar + waveform view)
│   └── api/        # FastAPI backend (auth, projects, AI gateway, job orchestrator)
├── packages/
│   ├── ai-core/        # Shared prompt templates & LLM types
│   ├── eda-wasm/       # WASM wrappers (iverilog, yosys, surfer)
│   ├── verilog-lang/   # Monaco language contribution for Verilog/SV
│   └── ui/             # Shared React components
├── runners/            # Sandboxed Docker images for server-side EDA jobs
│   ├── verilator/
│   └── yosys/
├── infra/              # docker-compose, k8s manifests (later)
└── docs/               # Architecture, ADRs, prompt templates
```

## Prerequisites

- Node.js >= 20 (see [`.nvmrc`](./.nvmrc))
- pnpm >= 9
- Python >= 3.11 (see [`.python-version`](./.python-version))
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker & Docker Compose

## Quick Start

```bash
# Install JS dependencies
pnpm install

# Install Python dependencies
cd apps/api && uv sync && cd ../..

# Copy env template
cp .env.example .env

# Start infrastructure (postgres, redis, minio)
docker compose -f infra/docker-compose.yml up -d postgres redis minio

# Run database migrations
cd apps/api && uv run alembic upgrade head && cd ../..

# Start the API (terminal 1)
cd apps/api && uv run uvicorn chipforge_api.main:app --reload --port 8000

# Start the web app (terminal 2)
pnpm --filter @chipforge/web dev
```

Open http://localhost:3000.

## Deployment

- **Frontend (Vercel)**: `apps/web/` is configured to deploy to Vercel. Point a Vercel project at this repo with root directory `apps/web`.
- **Backend (Fly.io)**: `apps/api/fly.toml` is the Fly.io config. Deploy with `fly deploy --config apps/api/fly.toml`.

See [`docs/deploy.md`](./docs/deploy.md) for detailed deploy instructions.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
