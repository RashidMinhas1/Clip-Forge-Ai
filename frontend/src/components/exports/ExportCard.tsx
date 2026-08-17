import React, { useState } from "react";
import { Download, RefreshCw, AlertCircle, CheckCircle2, XCircle, FileVideo, FileText, ChevronDown } from "lucide-react";
import { RenderJob } from "@/hooks/useExports";

interface ExportCardProps {
  job: RenderJob;
  onRetry: (jobId: string) => void;
  onDownloadVideo: (jobId: string) => void;
  onDownloadCaptions: (jobId: string, format: string) => void;
}

export function ExportCard({ job, onRetry, onDownloadVideo, onDownloadCaptions }: ExportCardProps) {
  const [showDropdown, setShowDropdown] = useState(false);
  const [isRetrying, setIsRetrying] = useState(false);

  const handleRetry = async () => {
    setIsRetrying(true);
    try {
      await onRetry(job.id);
    } finally {
      setIsRetrying(false);
    }
  };

  const getStatusIcon = () => {
    switch (job.status) {
      case "completed": return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case "failed": return <XCircle className="w-5 h-5 text-red-500" />;
      default: return <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />;
    }
  };

  const formattedDate = new Date(job.created_at).toLocaleString();

  return (
    <div className="bg-white border border-[#E2E8F0] rounded-xl overflow-hidden shadow-sm flex flex-col">
      <div className="aspect-video bg-[#F1F5F9] relative flex items-center justify-center">
        {job.status === "completed" ? (
          <video 
            src={`/api/v1/exports/${job.id}/download/video`} 
            className="w-full h-full object-contain bg-black"
            controls 
            preload="metadata"
          />
        ) : (
          <div className="flex flex-col items-center text-[#64748B]">
            {job.status === "failed" ? (
              <AlertCircle className="w-10 h-10 mb-2 text-red-400" />
            ) : (
              <RefreshCw className="w-10 h-10 mb-2 animate-spin text-blue-400" />
            )}
            <span className="text-sm font-medium capitalize">{job.status}</span>
          </div>
        )}
      </div>

      <div className="p-4 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-semibold text-[#0F172A] truncate" title={job.id}>
              Render: {job.id.slice(0, 8)}
            </h3>
            <p className="text-xs text-[#64748B]">{formattedDate}</p>
          </div>
          {getStatusIcon()}
        </div>

        {job.error_message && (
          <p className="text-xs text-red-500 mt-2 line-clamp-2" title={job.error_message}>
            {job.error_message}
          </p>
        )}

        <div className="mt-auto pt-4 relative">
          {job.status === "completed" && (
            <div className="flex gap-2 relative">
              <button
                onClick={() => onDownloadVideo(job.id)}
                className="flex-1 flex items-center justify-center gap-2 bg-[#5B21FF] hover:bg-[#4C1DE0] text-white py-2 px-3 rounded-lg text-sm font-medium transition-colors"
              >
                <Download className="w-4 h-4" />
                Video
              </button>
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="flex items-center justify-center gap-2 bg-[#F1F5F9] hover:bg-[#E2E8F0] text-[#0F172A] py-2 px-3 rounded-lg text-sm font-medium transition-colors"
                >
                  <FileText className="w-4 h-4" />
                  <ChevronDown className="w-4 h-4" />
                </button>
                
                {showDropdown && (
                  <>
                    <div 
                      className="fixed inset-0 z-10" 
                      onClick={() => setShowDropdown(false)}
                    />
                    <div className="absolute right-0 bottom-full mb-2 w-32 bg-white rounded-lg shadow-lg border border-[#E2E8F0] overflow-hidden z-20">
                      {(["srt", "vtt", "txt", "json"]).map((fmt) => (
                        <button
                          key={fmt}
                          onClick={() => {
                            onDownloadCaptions(job.id, fmt);
                            setShowDropdown(false);
                          }}
                          className="w-full text-left px-4 py-2 text-sm text-[#0F172A] hover:bg-[#F8FAFC] uppercase font-medium"
                        >
                          .{fmt}
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
          
          {job.status === "failed" && (
            <button
              onClick={handleRetry}
              disabled={isRetrying}
              className="w-full flex items-center justify-center gap-2 bg-[#F1F5F9] hover:bg-[#E2E8F0] text-[#0F172A] py-2 px-3 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isRetrying ? "animate-spin" : ""}`} />
              {isRetrying ? "Retrying..." : "Retry Render"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
