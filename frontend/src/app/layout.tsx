import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Valeriya Paine — AI Solutions Engineer",
  description: "Ask an AI assistant about Valeriya Paine's background, skills, and projects.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-ink text-white antialiased">{children}</body>
    </html>
  );
}
