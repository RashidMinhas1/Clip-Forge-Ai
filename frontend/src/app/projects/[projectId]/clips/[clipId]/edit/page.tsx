'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useClipEditor } from '@/hooks/useClipEditor';
import { useCaptions } from '@/hooks/useCaptions';
import { ClipPlayer } from '@/components/editor/ClipPlayer';
import { TimelineControls } from '@/components/editor/TimelineControls';
import { FramingSelector } from '@/components/editor/FramingSelector';
import { CaptionStylePanel } from '@/components/editor/CaptionStylePanel';
import { RenderButton } from '@/components/editor/RenderButton';
import Link from 'next/link';

export default function ClipEditorPage({ params }: { params: { projectId: string, clipId: string } }) {
  const router = useRouter();
  const { projectId, clipId } = params;
  
  const {
    clip,
    isLoading: isClipLoading,
    isSaving: isClipSaving,
    error: clipError,
    startTime,
    endTime,
    framingMode,
    updateEdit
  } = useClipEditor(projectId, clipId);

  const {
    chunks,
    config: captionConfig,
    isLoading: isCaptionsLoading,
    isSaving: isCaptionsSaving,
    error: captionsError,
    updateConfig
  } = useCaptions(projectId, clipId);

  const [currentTime, setCurrentTime] = useState(0);

  const isLoading = isClipLoading || isCaptionsLoading;
  const isSaving = isClipSaving || isCaptionsSaving;
  const error = clipError || captionsError;

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !clip) {
    return (
      <div className="flex flex-col h-screen items-center justify-center bg-gray-50 text-center p-4">
        <h2 className="text-2xl font-bold text-red-600 mb-2">Error Loading Editor</h2>
        <p className="text-gray-600 mb-6">{error || 'Clip not found'}</p>
        <Link href={`/projects/${projectId}`} className="text-indigo-600 hover:underline">
          Return to Project
        </Link>
      </div>
    );
  }

  // Use a placeholder video URL if the backend doesn't provide one
  const videoUrl = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

  return (
    <div className="flex flex-col h-screen bg-gray-50 overflow-hidden">
      {/* Top Navbar */}
      <header className="bg-white border-b h-16 flex items-center justify-between px-6 shrink-0 z-10">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => router.push(`/projects/${projectId}`)}
            className="text-gray-500 hover:text-gray-900"
          >
            &larr; Back to Candidate Review
          </button>
          <div className="h-6 w-px bg-gray-300"></div>
          <h1 className="font-semibold text-gray-900 truncate max-w-md">{clip.title}</h1>
        </div>
        
        <div className="flex items-center gap-4">
          {isSaving ? (
            <span className="text-sm text-gray-500 flex items-center gap-2">
              <div className="w-3 h-3 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
              Saving...
            </span>
          ) : (
            <span className="text-sm text-green-600 flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
              Saved
            </span>
          )}
          <RenderButton clipId={clipId} />
          <button 
            onClick={() => router.push(`/projects/${projectId}`)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
          >
            Done
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column: Player & Timeline */}
        <div className="flex-1 flex flex-col p-6 overflow-hidden">
          {/* Player Container */}
          <div className="flex-1 bg-gray-900 rounded-lg shadow-inner overflow-hidden mb-6 flex items-center justify-center">
            <ClipPlayer 
              videoUrl={videoUrl}
              startTime={startTime}
              endTime={endTime}
              framingMode={framingMode}
              onTimeUpdate={setCurrentTime}
              chunks={chunks}
              captionConfig={captionConfig}
            />
          </div>

          {/* Timeline Controls */}
          <div className="shrink-0 h-40">
            <TimelineControls 
              startTime={startTime}
              endTime={endTime}
              duration={clip.duration}
              currentTime={currentTime}
              onChangeStart={(s) => updateEdit(s, endTime, framingMode)}
              onChangeEnd={(e) => updateEdit(startTime, e, framingMode)}
            />
          </div>
        </div>

        {/* Right Column: Settings */}
        <div className="w-80 bg-white border-l overflow-y-auto shrink-0 p-6 shadow-sm">
          <div className="mb-8">
            <h2 className="text-lg font-bold text-gray-900 mb-2">Clip Info</h2>
            <div className="p-4 bg-gray-50 rounded-lg text-sm text-gray-700 border">
              <p className="mb-2"><span className="font-semibold">Score:</span> {clip.score}/10</p>
              <p className="mb-2"><span className="font-semibold">Hook:</span> &quot;{clip.hook}&quot;</p>
              <p><span className="font-semibold">Excerpt:</span> {clip.transcript_excerpt}</p>
            </div>
          </div>

          <div className="mb-8 pt-6 border-t">
            <FramingSelector 
              currentMode={framingMode}
              onChangeMode={(m) => updateEdit(startTime, endTime, m)}
            />
          </div>
          
          <div className="mb-8 pt-6 border-t">
            <CaptionStylePanel
              config={captionConfig}
              onUpdate={updateConfig}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
