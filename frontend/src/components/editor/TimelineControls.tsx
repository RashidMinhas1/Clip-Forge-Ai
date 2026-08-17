import React from 'react';

interface TimelineControlsProps {
  startTime: number;
  endTime: number;
  duration: number;
  currentTime: number;
  onChangeStart: (newStart: number) => void;
  onChangeEnd: (newEnd: number) => void;
}

export const TimelineControls: React.FC<TimelineControlsProps> = ({
  startTime,
  endTime,
  duration,
  currentTime,
  onChangeStart,
  onChangeEnd
}) => {
  // Format seconds to mm:ss.ms
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 10);
    return `${m}:${s.toString().padStart(2, '0')}.${ms}`;
  };

  const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    if (val < endTime - 0.5) {
      onChangeStart(val);
    }
  };

  const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    if (val > startTime + 0.5) {
      onChangeEnd(val);
    }
  };

  const handleAdjustStart = (delta: number) => {
    const newVal = Math.max(0, startTime + delta);
    if (newVal < endTime - 0.5) onChangeStart(newVal);
  };

  const handleAdjustEnd = (delta: number) => {
    // Assume max duration is large if we don't have it, but usually we do
    const newVal = endTime + delta;
    if (newVal > startTime + 0.5) onChangeEnd(newVal);
  };

  return (
    <div className="bg-gray-900 text-white p-4 rounded-lg flex flex-col gap-4">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-semibold">Clip Bounds</span>
        <span className="text-xs text-gray-400 font-mono">
          {formatTime(currentTime)} / {formatTime(endTime - startTime)}
        </span>
      </div>
      
      <div className="flex flex-col gap-4">
        {/* Start Time Control */}
        <div className="flex items-center gap-3">
          <span className="text-xs w-10 text-gray-400">Start</span>
          <button 
            onClick={() => handleAdjustStart(-1)}
            className="w-8 h-8 rounded bg-gray-800 hover:bg-gray-700 flex items-center justify-center"
          >-1s</button>
          <input 
            type="range" 
            min="0" 
            max={Math.max(duration || 100, endTime + 10)} 
            step="0.1"
            value={startTime}
            onChange={handleStartChange}
            className="flex-1 accent-indigo-500 h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer"
          />
          <button 
            onClick={() => handleAdjustStart(1)}
            className="w-8 h-8 rounded bg-gray-800 hover:bg-gray-700 flex items-center justify-center"
          >+1s</button>
          <span className="text-sm font-mono w-14 text-right">{formatTime(startTime)}</span>
        </div>

        {/* End Time Control */}
        <div className="flex items-center gap-3">
          <span className="text-xs w-10 text-gray-400">End</span>
          <button 
            onClick={() => handleAdjustEnd(-1)}
            className="w-8 h-8 rounded bg-gray-800 hover:bg-gray-700 flex items-center justify-center"
          >-1s</button>
          <input 
            type="range" 
            min="0" 
            max={Math.max(duration || 100, endTime + 10)} 
            step="0.1"
            value={endTime}
            onChange={handleEndChange}
            className="flex-1 accent-indigo-500 h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer"
          />
          <button 
            onClick={() => handleAdjustEnd(1)}
            className="w-8 h-8 rounded bg-gray-800 hover:bg-gray-700 flex items-center justify-center"
          >+1s</button>
          <span className="text-sm font-mono w-14 text-right">{formatTime(endTime)}</span>
        </div>
      </div>
    </div>
  );
};
