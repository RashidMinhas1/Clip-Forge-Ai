import { useState, useCallback } from 'react';

export interface RenderJobResponse {
  id: string;
  clip_id: string;
  project_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  output_path: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export function useRender() {
  const [isRendering, setIsRendering] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const pollJob = useCallback(async (id: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/renders/${id}`);
      if (!res.ok) throw new Error('Failed to fetch render status');
      
      const job: RenderJobResponse = await res.json();
      setProgress(job.progress);

      if (job.status === 'completed') {
        setIsRendering(false);
        // Handle success, maybe return download link
      } else if (job.status === 'failed') {
        setError(job.error_message || 'Rendering failed');
        setIsRendering(false);
      } else {
        setTimeout(() => pollJob(id), 2000);
      }
    } catch (err: any) {
      setError(err.message);
      setIsRendering(false);
    }
  }, []);

  const startRender = async (clipId: string) => {
    setIsRendering(true);
    setError(null);
    setProgress(0);
    
    try {
      const res = await fetch(`http://localhost:8000/api/v1/renders/${clipId}`, {
        method: 'POST',
      });
      
      if (!res.ok) throw new Error('Failed to start render');
      
      const job: RenderJobResponse = await res.json();
      setJobId(job.id);
      pollJob(job.id);
    } catch (err: any) {
      setError(err.message);
      setIsRendering(false);
    }
  };

  return {
    isRendering,
    progress,
    error,
    startRender,
    jobId
  };
}
