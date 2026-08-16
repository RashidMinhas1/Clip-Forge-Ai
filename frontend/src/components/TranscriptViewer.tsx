"use client";

import { useState } from "react";
import {
  TranscriptResponse,
  TranscriptSegment,
} from "@/lib/api/transcriptClient";
import {
  ChevronDown,
  ChevronRight,
  Clock,
  Globe,
  Cpu,
  AlertCircle,
} from "lucide-react";

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  const ms = Math.floor((seconds % 1) * 100);
  return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}.${ms.toString().padStart(2, "0")}`;
}

function SegmentRow({ segment }: { segment: TranscriptSegment }) {
  const [expanded, setExpanded] = useState(false);
  const hasWords = segment.words && segment.words.length > 0;

  return (
    <div className="border-b border-slate-100 last:border-b-0">
      <button
        onClick={() => hasWords && setExpanded(!expanded)}
        className={`w-full text-left px-5 py-4 flex items-start gap-4 hover:bg-slate-50/80 transition-colors ${hasWords ? "cursor-pointer" : "cursor-default"}`}
      >
        <span className="text-xs font-mono text-purple-600 bg-purple-50 px-2 py-1 rounded-lg mt-0.5 flex-shrink-0 font-bold">
          {formatTime(segment.start_time)}
        </span>
        <p className="text-[#1A1A2E] text-sm leading-relaxed font-medium flex-1">
          {segment.text}
        </p>
        {hasWords && (
          <span className="text-slate-400 mt-1 flex-shrink-0">
            {expanded ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </span>
        )}
      </button>

      {expanded && hasWords && (
        <div className="px-5 pb-4 pl-20">
          <div className="flex flex-wrap gap-1.5">
            {segment.words.map((w, i) => (
              <span
                key={i}
                className="inline-flex items-baseline gap-1 text-xs bg-slate-50 border border-slate-100 rounded-lg px-2 py-1"
                title={`${formatTime(w.start_time)} → ${formatTime(w.end_time)}${w.probability !== null ? ` (${(w.probability * 100).toFixed(0)}%)` : ""}`}
              >
                <span className="font-medium text-[#1A1A2E]">{w.word}</span>
                <span className="text-slate-400 font-mono text-[10px]">
                  {formatTime(w.start_time)}
                </span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function TranscriptViewer({
  transcript,
}: {
  transcript: TranscriptResponse;
}) {
  if (transcript.status === "failed") {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
        <AlertCircle className="w-8 h-8 text-red-400 mx-auto mb-3" />
        <p className="font-bold text-red-700 mb-1">Transcription Failed</p>
        <p className="text-red-600 text-sm">
          {transcript.error_message || "An unknown error occurred."}
        </p>
      </div>
    );
  }

  if (
    transcript.status === "queued" ||
    transcript.status === "processing"
  ) {
    return (
      <div className="bg-purple-50 border border-purple-200 rounded-2xl p-6 text-center">
        <div className="w-8 h-8 border-3 border-purple-300 border-t-purple-600 rounded-full animate-spin mx-auto mb-3" />
        <p className="font-bold text-purple-700 mb-1">
          {transcript.status === "queued"
            ? "Queued for transcription..."
            : "Transcribing..."}
        </p>
        <p className="text-purple-500 text-sm">
          This may take a few minutes depending on the video length.
        </p>
      </div>
    );
  }

  // Status: completed
  return (
    <div className="bg-white border border-slate-200 rounded-3xl shadow-sm overflow-hidden">
      {/* Metadata header */}
      <div className="px-6 py-4 bg-slate-50 border-b border-slate-100 flex flex-wrap gap-5 text-sm">
        {transcript.language && (
          <div className="flex items-center gap-1.5 text-slate-600">
            <Globe className="w-4 h-4 text-purple-500" />
            <span className="font-semibold">
              {transcript.language.toUpperCase()}
            </span>
          </div>
        )}
        {transcript.duration && (
          <div className="flex items-center gap-1.5 text-slate-600">
            <Clock className="w-4 h-4 text-purple-500" />
            <span className="font-semibold">
              {formatTime(transcript.duration)}
            </span>
          </div>
        )}
        {transcript.model_used && (
          <div className="flex items-center gap-1.5 text-slate-600">
            <Cpu className="w-4 h-4 text-purple-500" />
            <span className="font-semibold">{transcript.model_used}</span>
          </div>
        )}
      </div>

      {/* Segments */}
      <div className="divide-y divide-slate-100">
        {transcript.segments.length === 0 ? (
          <div className="p-8 text-center text-slate-400 font-medium">
            No transcript segments found.
          </div>
        ) : (
          transcript.segments.map((segment) => (
            <SegmentRow key={segment.id} segment={segment} />
          ))
        )}
      </div>
    </div>
  );
}
