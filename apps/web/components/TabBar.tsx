'use client';

import { clsx } from 'clsx';

type TabBarProps = {
  openPaths: string[];
  activePath: string | null;
  onSwitch: (path: string) => void;
  onClose: (path: string) => void;
};

function basename(path: string): string {
  const i = path.lastIndexOf('/');
  return i >= 0 ? path.slice(i + 1) : path;
}

export function TabBar({ openPaths, activePath, onSwitch, onClose }: TabBarProps) {
  if (openPaths.length === 0) {
    return (
      <div className="flex h-8 shrink-0 items-center border-b border-border bg-panel px-3 text-xs text-muted">
        No file open — pick one from the tree on the left.
      </div>
    );
  }

  return (
    <div
      role="tablist"
      aria-label="Open files"
      className="flex h-8 shrink-0 items-center gap-1 overflow-x-auto border-b border-border bg-panel px-2 text-xs"
    >
      {openPaths.map((path) => {
        const active = path === activePath;
        return (
          <div
            key={path}
            role="tab"
            aria-selected={active}
            className={clsx(
              'flex h-6 items-center gap-1.5 rounded px-2',
              active
                ? 'bg-background text-foreground'
                : 'text-muted hover:bg-background/40 hover:text-foreground',
            )}
          >
            <button
              type="button"
              onClick={() => onSwitch(path)}
              title={path}
              className="font-medium"
            >
              {basename(path)}
            </button>
            <button
              type="button"
              aria-label={`Close ${path}`}
              onClick={(e) => {
                e.stopPropagation();
                onClose(path);
              }}
              className="rounded px-1 text-muted hover:bg-border hover:text-foreground"
            >
              ×
            </button>
          </div>
        );
      })}
    </div>
  );
}
