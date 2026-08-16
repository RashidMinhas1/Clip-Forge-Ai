'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { discoverClips, getClipDiscoveryStatus, type ClipCandidate } from '@/lib/api';

export default function SourcePage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const sourceId = params.sourceId as string;

  const [loading, setLoading] = useState(false);
  const [candidates, setCandidates] = useState<ClipCandidate[]>([]);
  const [status, setStatus] = useState<string | null>(null);

  const handleDiscover = async () => {
    setLoading(true);
    try {
      const { runId } = await discoverClips(projectId, sourceId);
      setStatus('processing');
      
      const poll = setInterval(async () => {
        const result = await getClipDiscoveryStatus(projectId, sourceId, runId);
        if (result.status === 'completed') {
          clearInterval(poll);
          setCandidates(result.candidates || []);
          setStatus('completed');
          setLoading(false);
        } else if (result.status === 'failed') {
          clearInterval(poll);
          setStatus('failed');
          setLoading(false);
        }
      }, 5000);
    } catch (e) {
      console.error(e);
      setLoading(false);
      setStatus('error');
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Source Detail: {sourceId}</h1>
      {/* Existing MS-004/MS-005 components would be here */}
      
      <div className="mt-8 border-t pt-8">
        <h2 className="text-xl font-bold mb-4">Clip Discovery</h2>
        <button 
          onClick={handleDiscover} 
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? 'Discovering...' : 'Discover Clips'}
        </button>

        {status && <p className="mt-4">Status: {status}</p>}

        <div className="mt-8 grid grid-cols-1 gap-4">
          {candidates.map((clip) => (
            <div key={clip.id} className="border p-4 rounded shadow">
              <h3 className="font-bold text-lg">{clip.title}</h3>
              <p className="italic text-gray-600 mb-2">&quot;{clip.hook}&quot;</p>
              <p className="mb-2">{clip.transcript_excerpt}</p>
              <div className="flex justify-between text-sm text-gray-500">
                <span>Score: {clip.score} (Confidence: {clip.confidence})</span>
                <span>{clip.start_time} - {clip.end_time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
