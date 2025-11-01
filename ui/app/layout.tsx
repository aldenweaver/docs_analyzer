import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Documentation Analyzer",
  description: "Analyze and fix documentation quality issues with AI-powered insights",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background">
        {children}
      </body>
    </html>
  );
}
