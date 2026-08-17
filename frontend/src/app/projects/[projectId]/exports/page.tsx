"use client";

import { use, useEffect } from "react";
import { useExports } from "@/hooks/useExports";
import { ExportCard } from "@/components/exports/ExportCard";
import { Loader2, Film, AlertCircle } from "lucide-react";

export default function ExportsPage({ params }: { params: Promise<{ projectId: string }> }) {
  const resolvedParams = use(params);
  const { exports, loading, error, retryExport, downloadVideo, downloadCaptions } = useExports(resolvedParams.projectId);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <Loader2 className="w-8 h-8 text-[#5B21FF] animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 p-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 flex items-center gap-3">
          <AlertCircle className="w-5 h-5" />
          <p className="font-medium">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col p-8 bg-[#F8FAFC] overflow-y-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[#0F172A]">Exports & Gallery</h1>
          <p className="text-[#64748B] mt-1">Manage and download your rendered clips</p>
        </div>
      </div>

      {exports.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-[#E2E8F0] rounded-2xl bg-white p-12 text-center">
          <div className="w-16 h-16 bg-[#F1F5F9] rounded-full flex items-center justify-center mb-4">
            <Film className="w-8 h-8 text-[#94A3B8]" />
          </div>
          <h3 className="text-lg font-bold text-[#0F172A] mb-2">No exports yet</h3>
          <p className="text-[#64748B] max-w-sm">
            You haven&apos;t rendered any clips in this project yet. Go to AI Clips and render a clip to see it here.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {exports.map((job) => (
            <ExportCard
              key={job.id}
              job={job}
              onRetry={retryExport}
              onDownloadVideo={downloadVideo}
              onDownloadCaptions={downloadCaptions}
            />
          ))}
        </div>
      )}
    </div>
  );
}
