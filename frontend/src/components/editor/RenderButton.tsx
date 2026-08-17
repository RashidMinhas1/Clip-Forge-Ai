'use client';

import React from 'react';
import { useRender } from '@/hooks/useRender';
import { Loader2, Video } from 'lucide-react';

interface RenderButtonProps {
  clipId: string;
}

export function RenderButton({ clipId }: RenderButtonProps) {
  const { isRendering, progress, error, startRender } = useRender();

  return (
    <div className="flex items-center gap-4">
      {error && (
        <span className="text-red-500 text-sm">{error}</span>
      )}
      
      <button
        onClick={() => startRender(clipId)}
        disabled={isRendering}
        className={`flex items-center gap-2 px-6 py-2 rounded-md font-semibold text-white transition-colors
          ${isRendering 
            ? 'bg-purple-600/50 cursor-not-allowed' 
            : 'bg-purple-600 hover:bg-purple-700 active:bg-purple-800'
          }`}
      >
        {isRendering ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Rendering... {Math.round(progress)}%
          </>
        ) : (
          <>
            <Video className="w-4 h-4" />
            Render Clip
          </>
        )}
      </button>
      
      {isRendering && (
        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-purple-600 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}
