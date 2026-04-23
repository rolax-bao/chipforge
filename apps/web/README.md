# @chipforge/web

Next.js 14 frontend for ChipForge.

## Scripts

```bash
pnpm --filter @chipforge/web dev        # dev server on :3000
pnpm --filter @chipforge/web build
pnpm --filter @chipforge/web lint
pnpm --filter @chipforge/web typecheck
```

## Deploy (Vercel)

1. Import this repo into Vercel.
2. Set root directory to `apps/web`.
3. Add env vars from [`../../.env.example`](../../.env.example) under `NEXT_PUBLIC_*`.
4. `vercel.json` handles the monorepo build with pnpm + Turborepo.

## Layout

- `app/` — Next.js App Router entrypoints
- `components/` — UI components (AppShell, FileTree, EditorPlaceholder, AiSidebar, TopBar)
- `lib/` — client utilities (empty in skeleton)
- `workers/` — Web Worker entrypoints for EDA WASM (added in PR #10)
