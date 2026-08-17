"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";

interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function checkHealth() {
      try {
        const data = await apiClient<HealthResponse>("/api/v1/health");
        setHealth(data);
      } catch (err: any) {
        setError(err.message || "Failed to connect to backend");
      } finally {
        setLoading(false);
      }
    }

    checkHealth();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-background">
      <div className="max-w-md w-full p-6 bg-card border border-border rounded-lg shadow-sm">
        <h1 className="text-2xl font-semibold mb-4 text-center">
          DEVELOPER / INFRASTRUCTURE VERIFICATION UI
        </h1>
        <p className="text-muted-foreground text-center mb-6">
          This UI exists solely to verify frontend → API client → FastAPI communication.
        </p>
        
        <div className="space-y-4">
          <div className="p-4 rounded-md bg-secondary flex items-center justify-between">
            <span className="font-medium">Backend Status:</span>
            {loading ? (
              <span className="text-muted-foreground" aria-live="polite">Loading...</span>
            ) : error ? (
              <span className="text-destructive font-semibold" aria-live="assertive">Offline</span>
            ) : (
              <span className="text-green-500 font-semibold" aria-live="polite">Online</span>
            )}
          </div>

          {error && (
            <div className="p-4 rounded-md bg-destructive/10 text-destructive border border-destructive/20 text-sm">
              <strong>Error:</strong> {error}
            </div>
          )}

          {health && (
            <div className="p-4 rounded-md border border-border text-sm space-y-2">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Version:</span>
                <span>{health.version}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Status:</span>
                <span>{health.status}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Timestamp:</span>
                <span>{new Date(health.timestamp).toLocaleString()}</span>
              </div>
            </div>
          )}

          <div className="pt-6 flex justify-center">
            <a 
              href="/projects" 
              className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 transition-colors"
            >
              Enter Application UI (Projects)
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
