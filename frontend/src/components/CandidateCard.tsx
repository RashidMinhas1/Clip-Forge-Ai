import React from 'react';
import { ClipCandidate } from '@/lib/api';
import Link from 'next/link';

interface CandidateCardProps {
  clip: ClipCandidate;
  onUpdateStatus: (candidateId: string, status: 'approved' | 'rejected') => void;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({ clip, onUpdateStatus }) => {
  return (
    <div className="border p-4 rounded shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-lg">{clip.title}</h3>
        <div>
          <span className={`px-2 py-1 rounded text-xs font-semibold mr-2 ${
            clip.status === 'approved' ? 'bg-green-100 text-green-800' :
            clip.status === 'rejected' ? 'bg-red-100 text-red-800' :
            'bg-gray-100 text-gray-800'
          }`}>
            {clip.status || 'pending'}
          </span>
        </div>
      </div>
      <p className="italic text-gray-600 mb-2">&quot;{clip.hook}&quot;</p>
      <p className="mb-2 text-sm">{clip.reason}</p>
      <p className="mb-4 text-sm bg-gray-50 p-2 rounded">{clip.transcript_excerpt}</p>
      <div className="flex justify-between text-sm text-gray-500 mb-4">
        <span>Score: {clip.score} (Confidence: {clip.confidence})</span>
        <span>{clip.start_time} - {clip.end_time}</span>
      </div>
      
      <div className="flex gap-2">
        <button 
          onClick={() => onUpdateStatus(clip.id, 'approved')}
          disabled={clip.status === 'approved'}
          className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-2 rounded text-sm transition-colors"
        >
          Approve
        </button>
        <button 
          onClick={() => onUpdateStatus(clip.id, 'rejected')}
          disabled={clip.status === 'rejected'}
          className="bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white px-4 py-2 rounded text-sm transition-colors"
        >
          Reject
        </button>
        {clip.status === 'approved' && (
          <Link 
            href={`/projects/${clip.project_id}/clips/${clip.id}/edit`}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded text-sm transition-colors ml-auto flex items-center justify-center"
          >
            Edit Clip
          </Link>
        )}
      </div>
    </div>
  );
};
