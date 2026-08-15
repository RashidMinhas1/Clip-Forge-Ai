import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi, describe, beforeEach } from "vitest";
import SourceIngestion from "./page";

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
    
    const file = new File(["dummy content"], "test.txt", { type: "text/plain" });
    const input = screen.getByLabelText("Local Video", { selector: "input[type='file']" }) as HTMLInputElement;
    // We cannot reliably use getByLabelText since we didn't add id, so we use querySelector or assume it's the only file input
    const fileInput = document.querySelector("input[type='file']") as HTMLInputElement;
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    const button = screen.getByText("Upload Local");
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText("Unsupported file extension")).toBeDefined();
    });
  });
});
