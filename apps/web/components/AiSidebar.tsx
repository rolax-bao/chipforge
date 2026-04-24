'use client';

import { useCallback, useRef, useState } from 'react';
import { type ChatMessage, streamChat } from '@/lib/ai-chat';

type Exchange = {
  id: number;
  prompt: string;
  reply: string;
  error: string | null;
  streaming: boolean;
};

let nextId = 1;

export function AiSidebar() {
  const [input, setInput] = useState('');
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendPrompt = useCallback(
    async (prompt: string) => {
      const trimmed = prompt.trim();
      if (!trimmed || streaming) return;

      const id = nextId++;
      setExchanges((prev) => [
        ...prev,
        { id, prompt: trimmed, reply: '', error: null, streaming: true },
      ]);
      setInput('');
      setStreaming(true);

      const controller = new AbortController();
      abortRef.current = controller;

      const messages: ChatMessage[] = [
        {
          role: 'system',
          content:
            'You are an expert chip design copilot. Keep answers terse and Verilog-literate.',
        },
        { role: 'user', content: trimmed },
      ];

      try {
        for await (const token of streamChat({ messages, signal: controller.signal })) {
          setExchanges((prev) =>
            prev.map((x) => (x.id === id ? { ...x, reply: x.reply + token } : x)),
          );
        }
        setExchanges((prev) => prev.map((x) => (x.id === id ? { ...x, streaming: false } : x)));
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        setExchanges((prev) =>
          prev.map((x) =>
            x.id === id ? { ...x, streaming: false, error: message || 'request failed' } : x,
          ),
        );
      } finally {
        setStreaming(false);
        abortRef.current = null;
      }
    },
    [streaming],
  );

  const onKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        void sendPrompt(input);
      }
    },
    [input, sendPrompt],
  );

  const cancel = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-border px-3 py-2 text-xs uppercase tracking-wide text-muted">
        <span>AI Copilot</span>
        <span className="text-[10px] normal-case text-muted">⌘/Ctrl + Enter to send</span>
      </div>

      <div className="flex-1 space-y-3 overflow-auto p-3 text-sm">
        {exchanges.length === 0 && (
          <div className="rounded border border-border bg-background p-3 text-muted">
            <p className="mb-2 font-medium text-foreground">Hello, chip designer 👋</p>
            <p className="text-xs">
              Ask anything about RTL, testbenches, lint, or waveforms. Responses stream from{' '}
              <code className="mx-1 rounded bg-panel px-1">/ai/chat</code>. Provider selection (mock
              vs OpenAI) is driven by backend env vars.
            </p>
          </div>
        )}

        {exchanges.map((x) => (
          <div key={x.id} className="space-y-2">
            <div className="rounded border border-border bg-background p-2">
              <div className="text-[10px] uppercase tracking-wide text-muted">you</div>
              <pre className="mt-1 whitespace-pre-wrap text-foreground">{x.prompt}</pre>
            </div>
            <div className="rounded border border-border bg-background p-2">
              <div className="text-[10px] uppercase tracking-wide text-muted">
                assistant{x.streaming ? ' · streaming…' : ''}
              </div>
              {x.error ? (
                <pre className="mt-1 whitespace-pre-wrap text-red-400">
                  {x.error}
                  {'\n'}
                  (Is the API running at NEXT_PUBLIC_API_BASE_URL? With mock provider this still
                  works offline.)
                </pre>
              ) : (
                <pre className="mt-1 whitespace-pre-wrap text-foreground">
                  {x.reply || (x.streaming ? '…' : '')}
                </pre>
              )}
            </div>
          </div>
        ))}
      </div>

      <form
        className="border-t border-border p-3"
        onSubmit={(e) => {
          e.preventDefault();
          void sendPrompt(input);
        }}
      >
        <textarea
          rows={3}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask about your design…"
          aria-label="Ask the AI copilot"
          className="w-full resize-none rounded border border-border bg-background p-2 text-sm placeholder:text-muted focus:outline-none focus:ring-1 focus:ring-accent"
        />
        <div className="mt-2 flex items-center justify-between gap-2">
          <span className="text-[10px] text-muted">
            Single-turn only in PR #7. Multi-turn + history land in PR #9.
          </span>
          <div className="flex gap-2">
            {streaming && (
              <button
                type="button"
                onClick={cancel}
                className="rounded border border-border px-2 py-1 text-xs text-foreground hover:bg-panel"
              >
                Cancel
              </button>
            )}
            <button
              type="submit"
              disabled={streaming || input.trim().length === 0}
              className="rounded border border-accent bg-accent/20 px-3 py-1 text-xs font-medium text-foreground disabled:cursor-not-allowed disabled:opacity-50"
            >
              {streaming ? 'Streaming…' : 'Send'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
