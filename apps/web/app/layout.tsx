import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ChipForge — Web AI IDE for chip design',
  description:
    'Browser-native IDE for RTL design, verification, synthesis, and simulation, with an AI copilot.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="h-screen overflow-hidden">{children}</body>
    </html>
  );
}
