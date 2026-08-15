'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled';

export interface RenderJob {
  id: string;
  status: JobStatus;
  progress: number;
  error_message?: string;
}

export function useRenderJobRealtime(jobId: string | null) {
  const [job, setJob] = useState<RenderJob | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;

    // Fetch initial job state (Fallback/Initial Load)
    const fetchJob = async () => {
      const { data, error } = await supabase
        .from('render_jobs')
        .select('id, status, progress, error_message')
        .eq('id', jobId)
        .single();
      
      if (error) {
        setError(error.message);
      } else if (data) {
        setJob(data as RenderJob);
      }
    };
    fetchJob();

    // Setup Realtime Subscription
    // Filtering by user_id is automatically enforced by RLS when connecting to realtime channel
    // We explicitly filter by id on the channel payload for targeted updates
    const channel = supabase
      .channel(`render_job_${jobId}`)
      .on(
        'postgres_changes',
        {
          event: 'UPDATE',
          schema: 'public',
          table: 'render_jobs',
          filter: `id=eq.${jobId}`,
        },
        (payload) => {
          const updatedJob = payload.new as RenderJob;
          setJob((prev) => (prev ? { ...prev, ...updatedJob } : updatedJob));
        }
      )
      .subscribe((status) => {
        if (status === 'SUBSCRIBED') {
          console.log(`Subscribed to realtime updates for job ${jobId}`);
        } else if (status === 'CHANNEL_ERROR') {
          setError('Failed to connect to realtime updates.');
        }
      });

    return () => {
      supabase.removeChannel(channel);
    };
  }, [jobId]);

  return { job, error };
}
