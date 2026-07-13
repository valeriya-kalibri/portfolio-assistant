import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ask Lera — AI Portfolio Assistant",
  description: "Ask an AI assistant about Valeriya Paine's background, skills, and projects.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-neutral-950 text-neutral-100 antialiased">{children}</body>
    </html>
  );
}
