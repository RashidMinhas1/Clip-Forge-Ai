import { useState, useEffect, useCallback, useRef } from 'react';
import { ClipCandidate, getClip, updateClipEdit } from '@/lib/api';

export function useClipEditor(projectId: string, clipId: string) {
  const [clip, setClip] = useState<ClipCandidate | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Local state for immediate UI feedback
  const [startTime, setStartTime] = useState<number>(0);
  const [endTime, setEndTime] = useState<number>(0);
  const [framingMode, setFramingMode] = useState<string>('ORIGINAL');

  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch initial data
  useEffect(() => {
    let isMounted = true;
    const fetchClip = async () => {
      try {
        setIsLoading(true);
        const data = await getClip(projectId, clipId);
        if (isMounted) {
          setClip(data);
          setStartTime(data.start_time);
          setEndTime(data.end_time);
          setFramingMode(data.framing_mode || 'ORIGINAL');
        }
      } catch (err: any) {
        if (isMounted) setError(err.message || 'Failed to load clip');
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };
    fetchClip();
    return () => { isMounted = false; };
  }, [projectId, clipId]);

  // Autosave function
  const autosave = useCallback(async (newStart: number, newEnd: number, newMode: string) => {
    try {
      setIsSaving(true);
      setError(null);
      await updateClipEdit(projectId, clipId, {
        start_time: newStart,
        end_time: newEnd,
        framing_mode: newMode
      });
    } catch (err: any) {
      setError(err.message || 'Failed to save changes');
    } finally {
      setIsSaving(false);
    }
  }, [projectId, clipId]);

  // Debounced update wrapper
  const updateEdit = useCallback((newStart: number, newEnd: number, newMode: string) => {
    setStartTime(newStart);
    setEndTime(newEnd);
    setFramingMode(newMode);

    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setTimeout(() => {
      autosave(newStart, newEnd, newMode);
    }, 1000);
  }, [autosave]);

  return {
    clip,
    isLoading,
    isSaving,
    error,
    startTime,
    endTime,
    framingMode,
    updateEdit
  };
}
