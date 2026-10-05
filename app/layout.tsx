import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Little Play Lab | Printable adventures for kids",
  description: "Original printable activities for curious kids aged 3–10. Download, print and play.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
