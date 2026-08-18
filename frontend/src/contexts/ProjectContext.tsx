"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Project, projectApi } from "@/lib/api/projectClient";

interface ProjectContextType {
  activeProject: Project | null;
  projects: Project[];
  loading: boolean;
  error: string | null;
  setActiveProject: (project: Project | null) => void;
  refreshProjects: () => Promise<void>;
  createProject: (name: string) => Promise<Project>;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

export function ProjectProvider({ children }: { children: ReactNode }) {
  const [activeProject, setActiveProjectState] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    try {
      const data = await projectApi.listProjects();
      setProjects(data);
      return data;
    } catch (err: any) {
      setError(err.message || "Failed to load projects");
      return [];
    }
  };

  const loadActiveProject = async (allProjects: Project[]) => {
    const storedId = localStorage.getItem("clipforge_active_project_id");
    if (!storedId) return;

    // Check if the project is in the list
    const found = allProjects.find((p) => p.id === storedId);
    if (found) {
      setActiveProjectState(found);
      return;
    }

    // Otherwise try to fetch it directly
    try {
      const project = await projectApi.getProject(storedId);
      setActiveProjectState(project);
    } catch (err) {
      // It might have been deleted or not exist
      localStorage.removeItem("clipforge_active_project_id");
      setActiveProjectState(null);
    }
  };

  const setActiveProject = (project: Project | null) => {
    setActiveProjectState(project);
    if (project) {
      localStorage.setItem("clipforge_active_project_id", project.id);
    } else {
      localStorage.removeItem("clipforge_active_project_id");
    }
  };

  const createProject = async (name: string) => {
    setLoading(true);
    try {
      const project = await projectApi.createProject({ name });
      await fetchProjects();
      setActiveProject(project);
      setError(null);
      return project;
    } catch (err: any) {
      setError(err.message || "Failed to create project");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const { token, isLoading: authLoading } = useAuth();

  const refreshProjects = async () => {
    if (!token) {
      setProjects([]);
      setActiveProjectState(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    const data = await fetchProjects();
    await loadActiveProject(data);
    setLoading(false);
  };

  useEffect(() => {
    if (!authLoading) {
      refreshProjects();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token, authLoading]);

  return (
    <ProjectContext.Provider
      value={{
        activeProject,
        projects,
        loading,
        error,
        setActiveProject,
        refreshProjects,
        createProject,
      }}
    >
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const context = useContext(ProjectContext);
  if (context === undefined) {
    throw new Error("useProject must be used within a ProjectProvider");
  }
  return context;
}
