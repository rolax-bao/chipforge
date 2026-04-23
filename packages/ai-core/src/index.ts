/**
 * @chipforge/ai-core — shared AI types and prompt-template loaders.
 *
 * The backend (`apps/api`) owns the real LLM provider implementations.
 * This package only contains types and templates shared between web and api.
 */

export type ChatRole = 'system' | 'user' | 'assistant';

export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export interface CompletionRequest {
  prompt: string;
  maxTokens?: number;
  stopSequences?: string[];
}

export interface TokenStreamEvent {
  type: 'delta' | 'done' | 'error';
  text?: string;
  error?: string;
}

/** Canonical names for the built-in prompt templates. Real content lives in `docs/prompts/*.yaml`. */
export const PROMPT_TEMPLATES = [
  'chat.verilog',
  'complete.inline',
  'generate.testbench',
  'generate.spec-to-rtl',
  'explain.lint',
  'analyze.waveform',
] as const;

export type PromptTemplateName = (typeof PROMPT_TEMPLATES)[number];
