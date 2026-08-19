"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Loader2, Scissors, ArrowRight, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

function ResetPasswordContent() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Supabase automatically extracts the access_token from the hash
  // and establishes a session on this page. We just need to update the user.
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) {
        setError("Invalid or expired password reset link.");
      }
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!password) return;
    
    setError(null);
    setIsLoading(true);

    try {
      const { error: updateError } = await supabase.auth.updateUser({
        password: password
      });

      if (updateError) throw updateError;
      
      setSuccessMsg("Password updated successfully. You will be redirected shortly.");
      setTimeout(() => {
        router.push("/projects");
      }, 2000);
      
    } catch (err: any) {
      setError(err.message || "Failed to update password.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#F8FAFC] p-4 font-sans">
      <Link href="/" className="absolute top-8 left-8 flex items-center gap-2 group">
        <div className="w-8 h-8 bg-[#5B21FF] rounded flex items-center justify-center shadow-md group-hover:bg-[#4C1DE0] transition-colors">
          <Scissors className="w-4 h-4 text-white" />
        </div>
        <span className="font-bold text-lg text-[#0F172A]">ClipForge AI</span>
      </Link>

      <div className="w-full max-w-md bg-white p-8 md:p-10 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#E2E8F0]">
        
        <div className="text-center mb-8">
          <h1 className="text-2xl font-extrabold text-[#0F172A] mb-3 tracking-tight">
            Reset Password
          </h1>
          <p className="text-sm text-[#64748B] px-2 leading-relaxed">
            Please enter your new password below.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-3 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100 text-center">
            {error}
          </div>
        )}
        
        {successMsg && (
          <div className="mb-6 p-3 bg-green-50 text-green-700 text-xs rounded-lg border border-green-100 text-center">
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-[#475569] ml-1">New Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Create a strong password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 bg-white border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#5B21FF] focus:border-[#5B21FF] transition-all text-[#0F172A] placeholder:text-[#94A3B8] pr-10"
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#94A3B8] hover:text-[#475569] transition-colors"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading || !!successMsg}
            className="w-full mt-6 py-3 bg-[#5B21FF] hover:bg-[#4C1DE0] text-white rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
              <>
                Update Password
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-[#E2E8F0] text-center">
          <Link href="/auth?mode=login" className="text-sm font-medium text-[#64748B] hover:text-[#0F172A] transition-colors">
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#5B21FF]" /></div>}>
      <ResetPasswordContent />
    </Suspense>
  );
}
