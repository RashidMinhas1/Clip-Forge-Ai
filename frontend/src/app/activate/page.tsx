"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { apiClient } from "@/lib/api-client";
import { Loader2, Key, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function ActivatePage() {
  const router = useRouter();
  const { user, isActivated, isLoading: authLoading } = useAuth();
  const [activationKey, setActivationKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    // If auth finishes loading and user is already activated, redirect to projects
    if (!authLoading && isActivated) {
      router.push("/projects");
    }
  }, [authLoading, isActivated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activationKey) return;
    
    setError(null);
    setIsLoading(true);

    try {
      const res = await apiClient<{activated: boolean}>("/api/v1/access/activate", {
        method: "POST",
        body: JSON.stringify({ activation_key: activationKey }),
      });
      
      if (res.activated) {
        setSuccess(true);
        // Force reload to update context properly or just push
        setTimeout(() => {
          window.location.href = "/projects";
        }, 1000);
      }
    } catch (err: any) {
      setError(err.message || "Invalid activation key.");
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || (isActivated && !success)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8FAFC]">
        <Loader2 className="w-8 h-8 animate-spin text-[#5B21FF]" />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#F8FAFC] p-4 font-sans">
      <div className="w-full max-w-md bg-white p-8 md:p-10 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#E2E8F0] text-center">
        
        <div className="w-16 h-16 bg-[#F1F5F9] rounded-full flex items-center justify-center mx-auto mb-6">
          <Key className="w-8 h-8 text-[#5B21FF]" />
        </div>

        <h1 className="text-2xl font-extrabold text-[#0F172A] mb-3 tracking-tight">
          Application Access
        </h1>
        <p className="text-sm text-[#64748B] px-2 mb-8 leading-relaxed">
          Clip Forge AI requires an activation key to proceed. Please enter it below.
        </p>

        {error && (
          <div className="mb-6 p-3 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100 text-center">
            {error}
          </div>
        )}

        {success ? (
          <div className="p-4 bg-green-50 text-green-700 text-sm font-medium rounded-lg border border-green-200 text-center flex flex-col items-center gap-2">
            Application access granted. Redirecting...
            <Loader2 className="w-4 h-4 animate-spin mt-2" />
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5 text-left">
              <label className="text-xs font-semibold text-[#475569] ml-1">Activation Key</label>
              <input
                type="password"
                placeholder="Enter activation key"
                required
                value={activationKey}
                onChange={(e) => setActivationKey(e.target.value)}
                className="w-full px-4 py-2.5 bg-white border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#5B21FF] focus:border-[#5B21FF] transition-all text-[#0F172A] placeholder:text-[#94A3B8]"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !activationKey}
              className="w-full mt-6 py-3 bg-[#5B21FF] hover:bg-[#4C1DE0] text-white rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                <>
                  Activate
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        )}

        <div className="mt-8 pt-6 border-t border-[#E2E8F0]">
          <Link href="/auth?mode=login" className="text-sm font-medium text-[#64748B] hover:text-[#0F172A] transition-colors">
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
