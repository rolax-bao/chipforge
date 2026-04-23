export function FileTree() {
  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-border px-3 py-2 text-xs uppercase tracking-wide text-muted">
        Files
      </div>
      <div className="flex-1 overflow-auto p-3 text-sm">
        <div className="mb-1 text-muted">example-project/</div>
        <ul className="ml-3 space-y-1 text-foreground">
          <li className="cursor-not-allowed opacity-70">rtl/counter.v</li>
          <li className="cursor-not-allowed opacity-70">tb/counter_tb.v</li>
          <li className="cursor-not-allowed opacity-70">README.md</li>
        </ul>
        <p className="mt-6 text-xs text-muted">
          File CRUD lands in PR #5. This is a static placeholder.
        </p>
      </div>
    </div>
  );
}
