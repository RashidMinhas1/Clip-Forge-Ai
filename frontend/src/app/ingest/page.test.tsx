import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, vi, describe, beforeEach, afterEach } from "vitest";
import SourceIngestion from "./page";
import { cleanup } from "@testing-library/react";

// Mock the API client and global fetch
vi.mock("@/lib/api-client", () => ({
  apiClient: vi.fn(),
}));
import { apiClient } from "@/lib/api-client";

describe("SourceIngestion Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    cleanup();
  });

  test("renders the ingestion UI correctly", () => {
    render(<SourceIngestion />);
    expect(screen.getByText("Source Ingestion & Validation")).toBeDefined();
    expect(screen.getByPlaceholderText("https://youtube.com/watch?v=...")).toBeDefined();
    expect(screen.getByText("Upload Local")).toBeDefined();
  });

  test("handles YouTube URL ingestion submission and success", async () => {
    (apiClient as any).mockResolvedValueOnce({
      source_id: "yt-123",
      source_type: "youtube",
      title: "Test Video",
      ingestion_status: "accepted"
    });

    render(<SourceIngestion />);
    const input = screen.getByPlaceholderText("https://youtube.com/watch?v=...");
    fireEvent.change(input, { target: { value: "https://youtube.com/watch?v=123" } });
    
    const button = screen.getByText("Ingest YouTube");
    fireEvent.click(button);

    expect(apiClient).toHaveBeenCalledWith("/api/v1/sources/youtube", {
      method: "POST",
      body: JSON.stringify({ url: "https://youtube.com/watch?v=123" })
    });

    await waitFor(() => {
      expect(screen.getByText("Ingestion Result")).toBeDefined();
      expect(screen.getByText("yt-123")).toBeDefined();
    });
  });

  test("handles local file upload submission and failure", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      json: async () => ({
        detail: {
          error_message: "Unsupported file extension",
          ingestion_status: "failed"
        }
      })
    });

    render(<SourceIngestion />);
    
    const file = new File(["dummy content"], "test.mp4", { type: "video/mp4" });
    const fileInput = document.querySelector("input[type='file']") as HTMLInputElement;
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    const form = fileInput.closest("form")!;
    fireEvent.submit(form);

    await waitFor(() => {
      expect(screen.getByText(/Unsupported file extension/i)).toBeDefined();
    });
  });
});
