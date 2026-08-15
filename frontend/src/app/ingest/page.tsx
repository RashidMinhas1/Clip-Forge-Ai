"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api-client";

interface SourceMetadata {
  source_id: string;
  source_type: string;
  title: string;
  duration?: number;
  width?: number;
  height?: number;
  fps?: number;
  video_codec?: string;
  has_audio?: boolean;
  ingestion_status: string;
  error_message?: string;
}

export default function SourceIngestion() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SourceMetadata | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleYoutubeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!youtubeUrl) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const data = await apiClient<SourceMetadata>("/api/v1/sources/youtube", {
        method: "POST",
        body: JSON.stringify({ url: youtubeUrl })
      });
      setResult(data);
    } catch (err: any) {
      if (err.data && typeof err.data === 'object') {
         setError(err.data.error_message || "Ingestion failed");
         setResult(err.data);
      } else {
         setError(err.message || "Failed to connect to backend");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      // apiClient stringifies objects, so for FormData we use fetch directly or bypass default headers
      const token = localStorage.getItem("auth_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/sources/local`, {
        method: "POST",
        body: formData,
        headers: token ? { "Authorization": `Bearer ${token}` } : {}
      });
      
      const data = await res.json();
      if (!res.ok) {
        if (data.detail && data.detail.error_message) {
           setError(data.detail.error_message);
           setResult(data.detail);
        } else {
           throw new Error(data.detail || "Upload failed");
        }
      } else {
        setResult(data);
      }
    } catch (err: any) {
      setError(err.message || "Failed to upload file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-background">
      <div className="max-w-2xl w-full p-6 bg-card border border-border rounded-lg shadow-sm">
        <h1 className="text-2xl font-semibold mb-6 text-center">
          Source Ingestion & Validation
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {/* YouTube Form */}
          <div className="space-y-4">
            <h2 className="text-lg font-medium">YouTube URL</h2>
            <form onSubmit={handleYoutubeSubmit} className="space-y-4">
              <input
                type="url"
                placeholder="https://youtube.com/watch?v=..."
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
                required
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !youtubeUrl}
                className="w-full py-2 px-4 bg-primary text-primary-foreground rounded-md disabled:opacity-50"
              >
                {loading ? "Processing..." : "Ingest YouTube"}
              </button>
            </form>
          </div>

          {/* Local File Form */}
          <div className="space-y-4">
            <h2 className="text-lg font-medium">Local Video</h2>
            <form onSubmit={handleFileSubmit} className="space-y-4">
              <input
                type="file"
                accept="video/mp4,video/quicktime,video/webm,video/x-matroska"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="w-full px-3 py-2 border rounded-md"
                required
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !file}
                className="w-full py-2 px-4 bg-primary text-primary-foreground rounded-md disabled:opacity-50"
              >
                {loading ? "Uploading..." : "Upload Local"}
              </button>
            </form>
          </div>
        </div>

        {/* Results */}
        <div aria-live="polite">
          {error && (
            <div className="p-4 mb-4 rounded-md bg-destructive/10 text-destructive border border-destructive/20 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}

          {result && (
            <div className={`p-4 rounded-md border text-sm space-y-2 ${result.ingestion_status === 'accepted' ? 'border-green-500 bg-green-500/10' : 'border-border'}`}>
              <h3 className="font-semibold mb-2">Ingestion Result</h3>
              <div className="grid grid-cols-2 gap-2">
                <div className="text-muted-foreground">Status:</div>
                <div className="font-mono">{result.ingestion_status}</div>
                
                <div className="text-muted-foreground">Source ID:</div>
                <div className="font-mono text-xs break-all">{result.source_id}</div>
                
                <div className="text-muted-foreground">Title:</div>
                <div className="truncate">{result.title || "N/A"}</div>
                
                {result.duration && (
                  <>
                    <div className="text-muted-foreground">Duration:</div>
                    <div>{result.duration.toFixed(2)}s</div>
                  </>
                )}
                
                {result.video_codec && (
                  <>
                    <div className="text-muted-foreground">Video:</div>
                    <div>{result.width}x{result.height} @ {result.fps}fps ({result.video_codec})</div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
