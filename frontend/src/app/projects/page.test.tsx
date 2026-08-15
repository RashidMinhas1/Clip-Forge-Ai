import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi, describe, beforeEach, afterEach } from "vitest";
import ProjectsPage from "./page";
import { cleanup } from "@testing-library/react";

// Mock ProjectContext
const mockUseProject = vi.fn();
vi.mock("@/contexts/ProjectContext", () => ({
  useProject: () => mockUseProject()
}));

const mockProjects = [
  { id: "proj-1", name: "Alpha", status: "active", created_at: "2026-08-15T00:00:00Z" },
  { id: "proj-2", name: "Beta", status: "active", created_at: "2026-08-16T00:00:00Z" },
];

describe("Projects Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  test("renders project list correctly", () => {
    mockUseProject.mockReturnValue({
      activeProject: null,
      projects: mockProjects,
      loading: false,
      error: null,
      setActiveProject: vi.fn(),
      createProject: vi.fn(),
    });

    render(<ProjectsPage />);
    expect(screen.getByText("Projects")).toBeDefined();
    expect(screen.getByText("Alpha")).toBeDefined();
    expect(screen.getByText("Beta")).toBeDefined();
    // Two Set Active buttons
    expect(screen.getAllByText("Set Active").length).toBe(2);
  });

  test("shows active project correctly", () => {
    mockUseProject.mockReturnValue({
      activeProject: mockProjects[0],
      projects: mockProjects,
      loading: false,
      error: null,
      setActiveProject: vi.fn(),
      createProject: vi.fn(),
    });

    render(<ProjectsPage />);
    expect(screen.getByText("Active")).toBeDefined();
    expect(screen.getByText("Open Project")).toBeDefined();
    // One Set Active button for Beta
    expect(screen.getAllByText("Set Active").length).toBe(1);
  });

  test("handles project creation", async () => {
    const createProjectMock = vi.fn().mockResolvedValue(mockProjects[0]);
    mockUseProject.mockReturnValue({
      activeProject: null,
      projects: [],
      loading: false,
      error: null,
      setActiveProject: vi.fn(),
      createProject: createProjectMock,
    });

    render(<ProjectsPage />);
    const input = screen.getByPlaceholderText("Project Name...");
    fireEvent.change(input, { target: { value: "New Proj" } });
    
    const button = screen.getByText("Create Project");
    fireEvent.click(button);

    expect(createProjectMock).toHaveBeenCalledWith("New Proj");
  });

  test("handles setting active project", () => {
    const setActiveProjectMock = vi.fn();
    mockUseProject.mockReturnValue({
      activeProject: null,
      projects: [mockProjects[0]],
      loading: false,
      error: null,
      setActiveProject: setActiveProjectMock,
      createProject: vi.fn(),
    });

    render(<ProjectsPage />);
    const button = screen.getByText("Set Active");
    fireEvent.click(button);

    expect(setActiveProjectMock).toHaveBeenCalledWith(mockProjects[0]);
  });
});
