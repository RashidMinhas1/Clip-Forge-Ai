"use client";

import { useState } from "react";
import { useProject } from "@/contexts/ProjectContext";
import { PlusCircle, Loader2, FolderOpen, Check } from "lucide-react";
import Link from "next/link";

export default function ProjectsPage() {
  const { projects, activeProject, loading, error, createProject, setActiveProject } = useProject();
  const [newProjectName, setNewProjectName] = useState("");
  const [isCreating, setIsCreating] = useState(false);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    setIsCreating(true);
    try {
      await createProject(newProjectName);
      setNewProjectName("");
    } catch (err) {
      // Error is handled in context, could show toast here
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen p-8 bg-background max-w-4xl mx-auto w-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Projects</h1>
          <p className="text-muted-foreground mt-2">Manage and switch between your video processing projects.</p>
        </div>
      </div>

      {error && (
        <div className="bg-destructive/10 text-destructive border border-destructive/20 rounded-md p-4 mb-8">
          {error}
        </div>
      )}

      <div className="bg-card border border-border rounded-lg shadow-sm p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Create New Project</h2>
        <form onSubmit={handleCreate} className="flex gap-4">
          <input
            type="text"
            placeholder="Project Name..."
            className="flex-1 bg-background border border-border rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            disabled={isCreating}
          />
          <button
            type="submit"
            disabled={isCreating || !newProjectName.trim()}
            className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isCreating ? <Loader2 className="w-4 h-4 animate-spin" /> : <PlusCircle className="w-4 h-4" />}
            Create Project
          </button>
        </form>
      </div>

      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Your Projects</h2>
        
        {loading ? (
          <div className="flex justify-center p-8">
            <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center p-8 bg-secondary/50 rounded-lg border border-border border-dashed">
            <p className="text-muted-foreground">No projects found. Create one to get started.</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {projects.map((project) => (
              <div
                key={project.id}
                className={`p-6 rounded-lg border flex items-center justify-between transition-colors ${
                  activeProject?.id === project.id
                    ? "border-primary bg-primary/5"
                    : "border-border bg-card hover:bg-secondary/50"
                }`}
              >
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="font-semibold text-lg">{project.name}</h3>
                    {activeProject?.id === project.id && (
                      <span className="bg-primary text-primary-foreground text-xs px-2 py-0.5 rounded-full flex items-center gap-1 font-medium">
                        <Check className="w-3 h-3" /> Active
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-muted-foreground flex gap-4">
                    <span>Created: {new Date(project.created_at).toLocaleDateString()}</span>
                    <span className="capitalize">Status: {project.status}</span>
                  </div>
                </div>

                <div className="flex gap-3">
                  {activeProject?.id !== project.id && (
                    <button
                      onClick={() => setActiveProject(project)}
                      className="px-4 py-2 border border-border rounded-md hover:bg-secondary transition-colors text-sm font-medium"
                    >
                      Set Active
                    </button>
                  )}
                  {activeProject?.id === project.id && (
                    <Link
                      href="/ingest"
                      className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors text-sm font-medium flex items-center gap-2"
                    >
                      <FolderOpen className="w-4 h-4" />
                      Open Project
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
