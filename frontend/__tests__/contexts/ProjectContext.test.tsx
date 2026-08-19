import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectProvider, useProject } from '@/contexts/ProjectContext';
import { useAuth } from '@/contexts/AuthContext';
import { projectApi } from '@/lib/api/projectClient';

// Mock dependencies
vi.mock('@/contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}));

vi.mock('@/lib/api/projectClient', () => ({
  projectApi: {
    listProjects: vi.fn(),
    getProject: vi.fn(),
    createProject: vi.fn(),
  },
}));

const mockProjects = [
  { id: '1', name: 'Project 1', created_at: '2026-01-01' },
  { id: '2', name: 'Project 2', created_at: '2026-01-02' },
];

const TestComponent = () => {
  const { projects, activeProject, loading, createProject, setActiveProject } = useProject();

  if (loading) return <div>Loading Projects...</div>;

  return (
    <div>
      <div data-testid="active-project">{activeProject?.name || 'None'}</div>
      <ul data-testid="project-list">
        {projects.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
      <button onClick={() => createProject('New Project')}>Create</button>
      <button onClick={() => setActiveProject(projects[0])}>Set Active</button>
    </div>
  );
};

describe('ProjectContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    (useAuth as any).mockReturnValue({ token: 'fake-token', isLoading: false });
    (projectApi.listProjects as any).mockResolvedValue(mockProjects);
  });

  it('loads projects on mount if authenticated', async () => {
    render(
      <ProjectProvider>
        <TestComponent />
      </ProjectProvider>
    );

    expect(screen.getByText('Loading Projects...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.queryByText('Loading Projects...')).not.toBeInTheDocument();
    });

    expect(projectApi.listProjects).toHaveBeenCalled();
    expect(screen.getByText('Project 1')).toBeInTheDocument();
    expect(screen.getByText('Project 2')).toBeInTheDocument();
  });

  it('does not load projects if unauthenticated', async () => {
    (useAuth as any).mockReturnValue({ token: null, isLoading: false });

    render(
      <ProjectProvider>
        <TestComponent />
      </ProjectProvider>
    );

    await waitFor(() => {
      expect(screen.queryByText('Loading Projects...')).not.toBeInTheDocument();
    });

    expect(projectApi.listProjects).not.toHaveBeenCalled();
  });

  it('creates a new project and sets it as active', async () => {
    const newProject = { id: '3', name: 'New Project', created_at: '2026-01-03' };
    (projectApi.createProject as any).mockResolvedValue(newProject);
    (projectApi.listProjects as any)
      .mockResolvedValueOnce(mockProjects)
      .mockResolvedValueOnce([...mockProjects, newProject]);

    render(
      <ProjectProvider>
        <TestComponent />
      </ProjectProvider>
    );

    await waitFor(() => expect(screen.queryByText('Loading Projects...')).not.toBeInTheDocument());

    await userEvent.click(screen.getByText('Create'));

    await waitFor(() => {
      expect(projectApi.createProject).toHaveBeenCalledWith({ name: 'New Project' });
      expect(screen.getByTestId('active-project')).toHaveTextContent('New Project');
    });
  });

  it('restores active project from localStorage', async () => {
    localStorage.setItem('clipforge_active_project_id', '2');

    render(
      <ProjectProvider>
        <TestComponent />
      </ProjectProvider>
    );

    await waitFor(() => expect(screen.queryByText('Loading Projects...')).not.toBeInTheDocument());

    expect(screen.getByTestId('active-project')).toHaveTextContent('Project 2');
  });
});
