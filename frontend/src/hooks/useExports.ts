import { useState, useCallback, useEffect } from "react";

export interface RenderJob {
  id: string;
  clip_id: string;
  project_id: string;
  status: string;
  progress: number;
  output_path: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export function useExports(projectId: string) {
  const [exports, setExports] = useState<RenderJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchExports = useCallback(async () => {
    try {
      const response = await fetch(`/api/v1/projects/${projectId}/exports`);
      if (!response.ok) {
        throw new Error("Failed to fetch exports");
      }
      const data = await response.json();
      setExports(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to load exports");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    if (projectId) {
      fetchExports();
    }
  }, [projectId, fetchExports]);

  const retryExport = async (jobId: string) => {
    try {
      const response = await fetch(`/api/v1/renders/${jobId}/retry`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error("Failed to retry export");
      }
      await fetchExports();
    } catch (err: any) {
      throw new Error(err.message || "Failed to retry export");
    }
  };

  const downloadVideo = (jobId: string) => {
    window.location.href = `/api/v1/exports/${jobId}/download/video`;
  };

  const downloadCaptions = (jobId: string, format: string) => {
    window.location.href = `/api/v1/exports/${jobId}/download/captions?format=${format}`;
  };

  return { exports, loading, error, fetchExports, retryExport, downloadVideo, downloadCaptions };
}
