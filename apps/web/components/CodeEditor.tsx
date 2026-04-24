'use client';

import dynamic from 'next/dynamic';
import { useCallback } from 'react';
import type { OnMount } from '@monaco-editor/react';
import { registerVerilogLanguage } from '@/lib/verilog-language';
import type { LanguageId } from '@/lib/sample-project';

// Load Monaco client-side only; it ships non-trivial JS and hits the DOM.
const Monaco = dynamic(() => import('@monaco-editor/react').then((m) => m.default), {
  ssr: false,
  loading: () => (
    <div className="flex h-full items-center justify-center text-xs text-muted">
      Loading Monaco editor…
    </div>
  ),
});

type CodeEditorProps = {
  path: string;
  value: string;
  language: LanguageId;
  onChange: (next: string) => void;
};

// Map our internal LanguageId → Monaco's language id. Verilog/SystemVerilog are
// custom-registered at first mount; markdown/plaintext are built-in.
function toMonacoLanguage(lang: LanguageId): string {
  switch (lang) {
    case 'verilog':
      return 'verilog';
    case 'systemverilog':
      return 'systemverilog';
    case 'markdown':
      return 'markdown';
    default:
      return 'plaintext';
  }
}

export function CodeEditor({ path, value, language, onChange }: CodeEditorProps) {
  const handleMount = useCallback<OnMount>((_editor, monaco) => {
    registerVerilogLanguage(monaco);
    monaco.editor.defineTheme('chipforge-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#0b1020',
      },
    });
    monaco.editor.setTheme('chipforge-dark');
  }, []);

  return (
    <Monaco
      key={path}
      path={path}
      value={value}
      language={toMonacoLanguage(language)}
      onMount={handleMount}
      onChange={(next) => onChange(next ?? '')}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 13,
        fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
        wordWrap: 'on',
        scrollBeyondLastLine: false,
        renderLineHighlight: 'line',
        smoothScrolling: true,
        automaticLayout: true,
        tabSize: 2,
      }}
    />
  );
}
