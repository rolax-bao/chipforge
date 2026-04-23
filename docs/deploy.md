# Deployment

ChipForge MVP targets **Vercel (web) + Fly.io (api)** for preview/staging and a docker-compose stack for local dev. A Kubernetes Helm chart is planned for V1+.

## Vercel (frontend)

1. Import this repo in the Vercel dashboard.
2. Set **Root Directory** to `apps/web`.
3. The included `apps/web/vercel.json` runs the monorepo install and build via pnpm + Turborepo.
4. Add env vars:
   - `NEXT_PUBLIC_API_BASE_URL` → the Fly.io API URL (e.g. `https://chipforge-api.fly.dev`)
   - `NEXT_PUBLIC_APP_NAME` → `ChipForge`

## Fly.io (backend)

First-time setup:

```bash
cd apps/api
fly launch --no-deploy --copy-config --config fly.toml
# attach a managed Postgres
fly postgres create --name chipforge-db --region iad
fly postgres attach chipforge-db

# set secrets (example)
fly secrets set \
  JWT_SECRET=$(openssl rand -hex 32) \
  AI_PROVIDER=mock \
  REDIS_URL=rediss://… \
  S3_ENDPOINT_URL=https://… \
  S3_ACCESS_KEY=… \
  S3_SECRET_KEY=…
```

Deploy:

```bash
fly deploy --config apps/api/fly.toml
```

CI can deploy automatically via `flyctl deploy --remote-only` once a `FLY_API_TOKEN` repo secret is added.

## Self-hosted (single tenant)

For enterprise use (priority per the product decision), run the full stack with Docker Compose:

```bash
docker compose -f infra/docker-compose.yml --profile full up -d
```

See [`../infra/README.md`](../infra/README.md) for details.
