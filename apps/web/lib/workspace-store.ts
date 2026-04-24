'use client';

import { useCallback, useMemo, useState } from 'react';
import { SAMPLE_FILES, filesByPath, type FileEntry, type LanguageId } from './sample-project';

export type WorkspaceState = {
  files: Record<string, FileEntry>;
  openPaths: string[];
  activePath: string | null;
};

export type WorkspaceApi = {
  state: WorkspaceState;
  activeFile: FileEntry | null;
  openFile: (path: string) => void;
  closeFile: (path: string) => void;
  switchTo: (path: string) => void;
  updateContent: (path: string, content: string) => void;
  languageForPath: (path: string) => LanguageId;
};

function inferLanguage(path: string): LanguageId {
  if (path.endsWith('.sv') || path.endsWith('.svh')) return 'systemverilog';
  if (path.endsWith('.v') || path.endsWith('.vh')) return 'verilog';
  if (path.endsWith('.md')) return 'markdown';
  return 'plaintext';
}

// In-memory only. Persistence (IndexedDB / backend) is explicitly deferred
// to PR #5. A refresh loses edits by design.
export function useWorkspace(initial: FileEntry[] = SAMPLE_FILES): WorkspaceApi {
  const [files, setFiles] = useState<Record<string, FileEntry>>(() => filesByPath(initial));
  const [openPaths, setOpenPaths] = useState<string[]>(() =>
    initial.length ? [initial[0]!.path] : [],
  );
  const [activePath, setActivePath] = useState<string | null>(() =>
    initial.length ? initial[0]!.path : null,
  );

  const openFile = useCallback((path: string) => {
    setOpenPaths((prev) => (prev.includes(path) ? prev : [...prev, path]));
    setActivePath(path);
  }, []);

  const switchTo = useCallback((path: string) => {
    setActivePath(path);
  }, []);

  const closeFile = useCallback((path: string) => {
    setOpenPaths((prev) => {
      const next = prev.filter((p) => p !== path);
      setActivePath((active) => {
        if (active !== path) return active;
        if (next.length === 0) return null;
        const idx = prev.indexOf(path);
        return next[Math.min(idx, next.length - 1)] ?? null;
      });
      return next;
    });
  }, []);

  const updateContent = useCallback((path: string, content: string) => {
    setFiles((prev) => {
      const existing = prev[path];
      if (!existing) return prev;
      return { ...prev, [path]: { ...existing, content } };
    });
  }, []);

  const activeFile = activePath ? (files[activePath] ?? null) : null;

  const api = useMemo<WorkspaceApi>(
    () => ({
      state: { files, openPaths, activePath },
      activeFile,
      openFile,
      closeFile,
      switchTo,
      updateContent,
      languageForPath: inferLanguage,
    }),
    [files, openPaths, activePath, activeFile, openFile, closeFile, switchTo, updateContent],
  );

  return api;
}
