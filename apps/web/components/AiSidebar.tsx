export function AiSidebar() {
  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-border px-3 py-2 text-xs uppercase tracking-wide text-muted">
        AI Copilot
      </div>
      <div className="flex-1 overflow-auto p-3 text-sm">
        <div className="rounded border border-border bg-background p-3 text-muted">
          <p className="mb-2 font-medium text-foreground">Hello, chip designer 👋</p>
          <p className="text-xs">
            This is a placeholder. In PR #7 the sidebar will connect to the backend
            <code className="mx-1 rounded bg-panel px-1">/ai/chat</code>
            streaming endpoint. Inline completion lands in PR #9.
          </p>
        </div>
      </div>
      <div className="border-t border-border p-3">
        <textarea
          rows={3}
          disabled
          placeholder="Ask about your design…  (disabled in skeleton PR)"
          className="w-full resize-none rounded border border-border bg-background p-2 text-sm placeholder:text-muted focus:outline-none"
        />
      </div>
    </div>
  );
}
