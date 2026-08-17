import React, { useRef, useEffect } from 'react';

interface ClipPlayerProps {
  videoUrl: string;
  startTime: number;
  endTime: number;
  framingMode: string;
  onTimeUpdate?: (currentTime: number) => void;
}

export const ClipPlayer: React.FC<ClipPlayerProps> = ({
  videoUrl,
  startTime,
  endTime,
  framingMode,
  onTimeUpdate
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  // Handle loop between start and end time
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      if (onTimeUpdate) {
        onTimeUpdate(video.currentTime);
      }
      
      // Loop back to start if we reach the end time
      if (video.currentTime >= endTime) {
        video.currentTime = startTime;
        video.play().catch(e => console.error("Playback failed", e));
      }
      
      // Safety check if we somehow get before start time
      if (video.currentTime < startTime - 0.5) {
        video.currentTime = startTime;
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
    };
  }, [startTime, endTime, onTimeUpdate]);

  // When start time changes significantly, jump to it
  useEffect(() => {
    if (videoRef.current) {
      // Only jump if we are outside the bounds
      if (videoRef.current.currentTime < startTime || videoRef.current.currentTime > endTime) {
        videoRef.current.currentTime = startTime;
      }
    }
  }, [startTime, endTime]);

  // Determine styling based on framing mode
  let containerClasses = "relative w-full h-full bg-black overflow-hidden flex items-center justify-center";
  let videoClasses = "max-w-full max-h-full object-contain";

  if (framingMode === 'FACE_TRACK_9_16') {
    // Simulate a 9:16 vertical crop
    containerClasses = "relative h-full bg-black overflow-hidden flex items-center justify-center mx-auto";
    videoClasses = "h-full w-full object-cover";
  } else if (framingMode === 'SPLIT_SCREEN') {
    // Simulate split screen (top/bottom)
    containerClasses = "relative h-full bg-black overflow-hidden flex flex-col items-center justify-center mx-auto";
    videoClasses = "h-1/2 w-full object-cover border-b-2 border-gray-800";
  }

  const containerStyle = framingMode === 'FACE_TRACK_9_16' 
    ? { aspectRatio: '9/16', maxHeight: '100%' } 
    : framingMode === 'SPLIT_SCREEN'
    ? { aspectRatio: '9/16', maxHeight: '100%' }
    : {};

  return (
    <div className={containerClasses} style={containerStyle}>
      {framingMode === 'SPLIT_SCREEN' && (
        <video 
          src={videoUrl}
          className={videoClasses}
          muted
          playsInline
        />
      )}
      <video
        ref={videoRef}
        src={videoUrl}
        className={videoClasses}
        controls={framingMode === 'ORIGINAL'}
        autoPlay
        muted
        playsInline
      />
    </div>
  );
};
