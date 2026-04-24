'use client';

import { useMemo } from 'react';
import { AiSidebar } from './AiSidebar';
import { EditorArea } from './EditorArea';
import { FileTree } from './FileTree';
import { TopBar } from './TopBar';
import { SAMPLE_FILES } from '@/lib/sample-project';
import { useWorkspace } from '@/lib/workspace-store';

export function AppShell() {
  const workspace = useWorkspace(SAMPLE_FILES);
  const files = useMemo(() => Object.values(workspace.state.files), [workspace.state.files]);

  return (
    <div className="flex h-screen flex-col bg-background text-foreground">
      <TopBar />
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-64 shrink-0 border-r border-border bg-panel">
          <FileTree
            files={files}
            activePath={workspace.state.activePath}
            onOpen={workspace.openFile}
          />
        </aside>
        <main className="flex flex-1 flex-col overflow-hidden">
          <EditorArea workspace={workspace} />
        </main>
        <aside className="w-96 shrink-0 border-l border-border bg-panel">
          <AiSidebar />
        </aside>
      </div>
    </div>
  );
}
