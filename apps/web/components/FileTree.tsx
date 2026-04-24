'use client';

import { clsx } from 'clsx';
import { useMemo } from 'react';
import { SAMPLE_PROJECT_NAME, type FileEntry } from '@/lib/sample-project';

type FileTreeProps = {
  files: FileEntry[];
  activePath: string | null;
  onOpen: (path: string) => void;
};

type TreeNode = {
  name: string;
  fullPath: string;
  children: TreeNode[];
  isFile: boolean;
};

function buildTree(files: FileEntry[]): TreeNode {
  const root: TreeNode = { name: SAMPLE_PROJECT_NAME, fullPath: '', children: [], isFile: false };
  for (const f of files) {
    const parts = f.path.split('/');
    let cursor = root;
    for (let i = 0; i < parts.length; i++) {
      const name = parts[i]!;
      const isFile = i === parts.length - 1;
      const fullPath = parts.slice(0, i + 1).join('/');
      let next = cursor.children.find((c) => c.name === name && c.isFile === isFile);
      if (!next) {
        next = { name, fullPath, children: [], isFile };
        cursor.children.push(next);
      }
      cursor = next;
    }
  }
  const sort = (node: TreeNode) => {
    node.children.sort((a, b) => {
      if (a.isFile !== b.isFile) return a.isFile ? 1 : -1; // folders first
      return a.name.localeCompare(b.name);
    });
    node.children.forEach(sort);
  };
  sort(root);
  return root;
}

function TreeList({
  nodes,
  depth,
  activePath,
  onOpen,
}: {
  nodes: TreeNode[];
  depth: number;
  activePath: string | null;
  onOpen: (path: string) => void;
}) {
  return (
    <ul className="space-y-0.5" role={depth === 0 ? 'tree' : 'group'}>
      {nodes.map((node) => (
        <li key={node.fullPath || node.name}>
          {node.isFile ? (
            <button
              type="button"
              role="treeitem"
              aria-selected={activePath === node.fullPath}
              onClick={() => onOpen(node.fullPath)}
              className={clsx(
                'flex w-full items-center rounded px-2 py-0.5 text-left text-sm',
                activePath === node.fullPath
                  ? 'bg-background text-accent'
                  : 'text-foreground hover:bg-background/40',
              )}
              style={{ paddingLeft: `${depth * 12 + 8}px` }}
              title={node.fullPath}
            >
              <span className="mr-1.5 text-muted">·</span>
              {node.name}
            </button>
          ) : (
            <>
              <div
                className="px-2 py-0.5 text-xs uppercase tracking-wide text-muted"
                style={{ paddingLeft: `${depth * 12 + 8}px` }}
              >
                {node.name}/
              </div>
              {node.children.length > 0 && (
                <TreeList
                  nodes={node.children}
                  depth={depth + 1}
                  activePath={activePath}
                  onOpen={onOpen}
                />
              )}
            </>
          )}
        </li>
      ))}
    </ul>
  );
}

export function FileTree({ files, activePath, onOpen }: FileTreeProps) {
  const root = useMemo(() => buildTree(files), [files]);

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-border px-3 py-2 text-xs uppercase tracking-wide text-muted">
        Files
      </div>
      <div className="flex-1 overflow-auto p-2 text-sm">
        <div className="mb-1 px-1 text-xs uppercase tracking-wide text-muted">{root.name}/</div>
        <TreeList nodes={root.children} depth={0} activePath={activePath} onOpen={onOpen} />
        <p className="mt-6 px-2 text-xs text-muted">
          File CRUD (create / rename / delete / persistence) lands in PR #5.
        </p>
      </div>
    </div>
  );
}
