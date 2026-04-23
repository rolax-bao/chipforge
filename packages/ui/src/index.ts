/**
 * @chipforge/ui — shared React components.
 *
 * Skeleton exports a single utility. Real components (Button, Dialog, Toast,
 * resizable panel wrapper) land as the UI grows, borrowing from shadcn/ui.
 */

export function cn(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}
