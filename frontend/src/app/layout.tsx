import type { Metadata } from "next";
import { ProjectProvider } from "@/contexts/ProjectContext";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClipForge AI",
  description: "AI-powered platform to transform long-form video content into short, caption-ready clips.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen flex flex-col">
        {/* Semantic accessibility defaults */}
        <header className="sr-only">ClipForge AI Application Header</header>
        <ProjectProvider>
          <main className="flex-1 flex flex-col">{children}</main>
        </ProjectProvider>
      </body>
    </html>
  );
}
