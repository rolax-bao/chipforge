# Infra

Local dev stack and (later) production manifests.

## Local (docker-compose)

```bash
docker compose -f infra/docker-compose.yml up -d postgres redis minio
```

Bring up the full stack including the API container:

```bash
docker compose -f infra/docker-compose.yml --profile full up -d
```

Stop everything:

```bash
docker compose -f infra/docker-compose.yml down
```

## Production

- Frontend → Vercel (`apps/web/vercel.json`)
- Backend → Fly.io (`apps/api/fly.toml`)
- Database → Fly Postgres or Neon
- Object storage → S3 or MinIO
- Redis → Upstash or managed Redis

K8s Helm chart lands in a later PR (V1+).
