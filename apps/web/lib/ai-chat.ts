// Minimal Server-Sent Events client for POST /ai/chat.
//
// The route emits one event per token as `data: {"token":"..."}` and a
// terminal `event: done` frame. We parse just enough of the SSE grammar
// to yield tokens — no EventSource, because EventSource cannot POST.

export type ChatRole = 'system' | 'user' | 'assistant';

export type ChatMessage = {
  role: ChatRole;
  content: string;
};

export type StreamChatInit = {
  messages: ChatMessage[];
  apiBaseUrl?: string;
  signal?: AbortSignal;
};

const DEFAULT_API_BASE_URL = 'http://localhost:8000';

export function getApiBaseUrl(): string {
  const fromEnv = process.env.NEXT_PUBLIC_API_BASE_URL;
  return fromEnv && fromEnv.trim().length > 0 ? fromEnv : DEFAULT_API_BASE_URL;
}

export async function* streamChat({
  messages,
  apiBaseUrl,
  signal,
}: StreamChatInit): AsyncGenerator<string, void, void> {
  const baseUrl = apiBaseUrl ?? getApiBaseUrl();
  const response = await fetch(`${baseUrl}/ai/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
    },
    body: JSON.stringify({ messages }),
    signal,
  });

  if (!response.ok || !response.body) {
    const detail = await safeReadText(response);
    throw new Error(`chat request failed (${response.status}): ${detail}`);
  }

  const decoder = new TextDecoder('utf-8');
  const reader = response.body.getReader();
  let buffer = '';

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      // SSE frames are separated by a blank line (\n\n). Process every
      // complete frame; keep the incomplete tail in `buffer`.
      let sep = buffer.indexOf('\n\n');
      while (sep !== -1) {
        const frame = buffer.slice(0, sep);
        buffer = buffer.slice(sep + 2);
        const token = parseFrame(frame);
        if (token !== null) yield token;
        sep = buffer.indexOf('\n\n');
      }
    }
  } finally {
    reader.releaseLock();
  }
}

function parseFrame(frame: string): string | null {
  let event = 'message';
  const dataLines: string[] = [];
  for (const rawLine of frame.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith(':')) continue;
    if (line.startsWith('event:')) {
      event = line.slice(6).trim();
    } else if (line.startsWith('data:')) {
      dataLines.push(line.slice(5).trim());
    }
  }
  if (event !== 'message' || dataLines.length === 0) return null;
  try {
    const payload = JSON.parse(dataLines.join('\n')) as { token?: unknown };
    return typeof payload.token === 'string' ? payload.token : null;
  } catch {
    return null;
  }
}

async function safeReadText(response: Response): Promise<string> {
  try {
    return (await response.text()).slice(0, 500);
  } catch {
    return '<unreadable body>';
  }
}
