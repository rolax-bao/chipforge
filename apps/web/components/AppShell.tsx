import { FileTree } from './FileTree';
import { EditorPlaceholder } from './EditorPlaceholder';
import { AiSidebar } from './AiSidebar';
import { TopBar } from './TopBar';

export function AppShell() {
  return (
    <div className="flex h-screen flex-col bg-background text-foreground">
      <TopBar />
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-64 shrink-0 border-r border-border bg-panel">
          <FileTree />
        </aside>
        <main className="flex flex-1 flex-col overflow-hidden">
          <EditorPlaceholder />
        </main>
        <aside className="w-96 shrink-0 border-l border-border bg-panel">
          <AiSidebar />
        </aside>
      </div>
    </div>
  );
}
