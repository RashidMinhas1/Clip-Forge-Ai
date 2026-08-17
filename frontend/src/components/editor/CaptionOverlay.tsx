import React from 'react';
import { CaptionChunk, CaptionConfig } from '@/hooks/useCaptions';

interface Props {
  chunks: CaptionChunk[];
  config: CaptionConfig | null;
  currentTime: number;
}

export function CaptionOverlay({ chunks, config, currentTime }: Props) {
  if (!config) return null;

  // Find active chunk
  const activeChunk = chunks.find(
    chunk => currentTime >= chunk.start_time && currentTime <= chunk.end_time
  );

  if (!activeChunk) return null;

  const style: React.CSSProperties = {
    color: config.text_color || '#ffffff',
    fontFamily: config.font_family || 'sans-serif',
    fontSize: config.font_size ? `${config.font_size}px` : '24px',
    backgroundColor: config.bg_color ? `${config.bg_color}99` : 'transparent', // 99 for alpha
    padding: '8px 16px',
    borderRadius: '8px',
    textAlign: 'center',
  };

  return (
    <div 
      className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2 w-[80%] flex justify-center items-center pointer-events-none"
      dir={config.is_rtl ? "rtl" : "ltr"}
    >
      <div style={style} className="drop-shadow-lg font-bold leading-tight flex flex-wrap justify-center gap-x-2 gap-y-1">
        {activeChunk.words.map((word, i) => {
          const isActive = currentTime >= word.start_time && currentTime <= word.end_time;
          return (
            <span 
              key={i} 
              style={{ 
                color: isActive ? (config.highlight_color || '#ffff00') : 'inherit',
                transform: isActive ? 'scale(1.1)' : 'scale(1)',
                transition: 'transform 0.1s ease-in-out, color 0.1s ease-in-out',
                display: 'inline-block'
              }}
            >
              {word.word}
            </span>
          );
        })}
      </div>
    </div>
  );
}
