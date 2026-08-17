import { useState, useEffect, useCallback } from 'react';

export interface CaptionWord {
  word: string;
  start_time: number;
  end_time: number;
  is_active?: boolean;
}

export interface CaptionChunk {
  text: string;
  start_time: number;
  end_time: number;
  words: CaptionWord[];
}

export interface CaptionConfig {
  preset_name: string;
  font_family: string | null;
  font_size: number | null;
  text_color: string | null;
  highlight_color: string | null;
  bg_color: string | null;
  is_rtl: boolean;
}

export function useCaptions(projectId: string, clipId: string) {
  const [chunks, setChunks] = useState<CaptionChunk[]>([]);
  const [config, setConfig] = useState<CaptionConfig | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCaptions = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await fetch(`/api/v1/projects/${projectId}/clips/${clipId}/captions`);
      if (!res.ok) throw new Error('Failed to load captions');
      const data = await res.json();
      setChunks(data.chunks);
      setConfig(data.config);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [projectId, clipId]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  const updateConfig = async (updateData: Partial<CaptionConfig>) => {
    if (!config) return;
    
    // Optimistic update
    setConfig(prev => prev ? { ...prev, ...updateData } : null);
    setIsSaving(true);
    
    try {
      const res = await fetch(`/api/v1/projects/${projectId}/clips/${clipId}/caption-config`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData),
      });
      if (!res.ok) throw new Error('Failed to save caption config');
      const data = await res.json();
      setConfig(data);
    } catch (err: any) {
      console.error(err);
      // Revert optimism if needed, but for simplicity just log error
      setError('Failed to save config');
    } finally {
      setIsSaving(false);
    }
  };

  return {
    chunks,
    config,
    isLoading,
    isSaving,
    error,
    updateConfig
  };
}
