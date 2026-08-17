'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { apiClient } from '@/lib/api-client';

export default function ClaimProjectPage({ params }: { params: { id: string } }) {
  const [status, setStatus] = useState<'idle' | 'claiming' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const { user } = useAuth();
  const router = useRouter();

  const handleClaim = async () => {
    setStatus('claiming');
    setErrorMessage('');
    try {
      await apiClient(`/api/v1/projects/${params.id}/claim`, {
        method: 'POST',
      });
      setStatus('success');
      setTimeout(() => {
        router.push(`/projects/${params.id}`);
      }, 1500);
    } catch (error: any) {
      setStatus('error');
      setErrorMessage(error.message || 'Failed to claim project');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-md border border-gray-200 dark:border-gray-700 text-center">
        <div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
            Claim Legacy Project
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            You are logged in as {user?.email}. Claim this legacy project to associate it with your account.
          </p>
        </div>
        
        {status === 'error' && (
          <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-3 rounded-md text-sm">
            {errorMessage}
          </div>
        )}
        
        {status === 'success' && (
          <div className="bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 p-3 rounded-md text-sm">
            Project successfully claimed! Redirecting...
          </div>
        )}

        <button
          onClick={handleClaim}
          disabled={status === 'claiming' || status === 'success'}
          className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {status === 'claiming' ? 'Claiming...' : 'Claim Project'}
        </button>
      </div>
    </div>
  );
}
