'use client';

import { CodeEditor } from './CodeEditor';
import { TabBar } from './TabBar';
import type { WorkspaceApi } from '@/lib/workspace-store';

type EditorAreaProps = {
  workspace: WorkspaceApi;
};

export function EditorArea({ workspace }: EditorAreaProps) {
  const { state, activeFile, switchTo, closeFile, updateContent, languageForPath } = workspace;

  return (
    <div className="flex h-full flex-col">
      <TabBar
        openPaths={state.openPaths}
        activePath={state.activePath}
        onSwitch={switchTo}
        onClose={closeFile}
      />
      <div className="relative flex-1 overflow-hidden bg-background">
        {activeFile ? (
          <CodeEditor
            path={activeFile.path}
            value={activeFile.content}
            language={activeFile.language}
            onChange={(next) => updateContent(activeFile.path, next)}
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-muted">
            Open a file from the tree to start editing.
          </div>
        )}
      </div>
      <div className="flex items-center justify-between border-t border-border bg-panel px-3 py-1 text-xs text-muted">
        <span>In-memory workspace. Persistence lands in PR #5; AI completions in PR #7–#9.</span>
        <span>
          {activeFile ? `${languageForPath(activeFile.path)} · LF · UTF-8` : 'no file · —'}
        </span>
      </div>
    </div>
  );
}
