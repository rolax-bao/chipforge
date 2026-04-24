import { SAMPLE_PROJECT_NAME } from '@/lib/sample-project';

export function TopBar() {
  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-border bg-panel px-4">
      <div className="flex items-center gap-3">
        <span className="text-sm font-semibold tracking-wide text-accent">ChipForge</span>
        <span className="text-xs text-muted">MVP skeleton · week 2</span>
        <span
          className="ml-2 rounded border border-border bg-background px-2 py-0.5 text-xs text-muted"
          title="Persistence and multi-project support land in PR #5"
        >
          {SAMPLE_PROJECT_NAME}
        </span>
      </div>
      <div className="flex items-center gap-2 text-xs text-muted">
        <button
          type="button"
          className="rounded border border-border px-2 py-1 hover:bg-background disabled:cursor-not-allowed disabled:opacity-60"
          disabled
          title="Simulation runner coming in PR #10"
        >
          Run Simulation
        </button>
        <button
          type="button"
          className="rounded border border-border px-2 py-1 hover:bg-background disabled:cursor-not-allowed disabled:opacity-60"
          disabled
          title="Auth coming in PR #4"
        >
          Sign in
        </button>
      </div>
    </header>
  );
}
