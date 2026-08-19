"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Loader2, Scissors, ArrowRight, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

function AuthPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const defaultMode = searchParams.get("mode") || "login";
  
  // mode can be 'login', 'signup', 'magic', 'forgot'
  const [mode, setMode] = useState<string>(defaultMode);
  
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    const urlMode = searchParams.get("mode");
    if (urlMode && ['login', 'signup', 'magic', 'forgot'].includes(urlMode)) {
      setMode(urlMode);
      setError(null);
      setSuccessMsg(null);
    }
  }, [searchParams]);

  const switchMode = (newMode: string) => {
    setError(null);
    setSuccessMsg(null);
    setMode(newMode);
    router.replace(`/auth?mode=${newMode}`, { scroll: false });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsLoading(true);

    try {
      if (mode === "login") {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
        router.push("/projects");
        
      } else if (mode === "signup") {
        const { error: signUpError } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: { full_name: name }
          }
        });
        if (signUpError) throw signUpError;
        setSuccessMsg("Check your email for the confirmation link to complete signup.");
        
      } else if (mode === "magic") {
        const { error: magicError } = await supabase.auth.signInWithOtp({
          email,
          options: {
            emailRedirectTo: `${window.location.origin}/auth`
          }
        });
        if (magicError) throw magicError;
        setSuccessMsg("Magic link sent! Check your email to sign in.");
        
      } else if (mode === "forgot") {
        const { error: resetError } = await supabase.auth.resetPasswordForEmail(email, {
          redirectTo: `${window.location.origin}/auth/reset-password`
        });
        if (resetError) throw resetError;
        setSuccessMsg("Password reset instructions sent to your email.");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during authentication.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F8FAFC] p-4 font-sans">
      <Link href="/" className="absolute top-8 left-8 flex items-center gap-2 group">
        <div className="w-8 h-8 bg-[#5B21FF] rounded flex items-center justify-center shadow-md group-hover:bg-[#4C1DE0] transition-colors">
          <Scissors className="w-4 h-4 text-white" />
        </div>
        <span className="font-bold text-lg text-[#0F172A]">ClipForge AI</span>
      </Link>

      <div className="w-full max-w-md bg-white p-8 md:p-10 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-[#E2E8F0]">
        
        {/* Title & Subtitle */}
        <div className="text-center mb-8">
          <h1 className="text-2xl md:text-3xl font-extrabold text-[#0F172A] mb-3 tracking-tight">
            {mode === 'login' && "Welcome back"}
            {mode === 'signup' && "Create an account"}
            {mode === 'magic' && "Sign in with Magic Link"}
            {mode === 'forgot' && "Reset your password"}
          </h1>
          <p className="text-sm text-[#64748B] px-2 leading-relaxed">
            {mode === 'login' || mode === 'signup' 
              ? "Join Clip Forge AI to start transforming your long videos into viral clips."
              : mode === 'magic' 
              ? "We'll send you a secure link to instantly sign in to your account."
              : "Enter your email and we'll send you instructions to reset your password."}
          </p>
        </div>

        {/* Messages */}
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

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'signup' && (
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#475569] ml-1">Name</label>
              <input
                type="text"
                placeholder="Jane Doe"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2.5 bg-white border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#5B21FF] focus:border-[#5B21FF] transition-all text-[#0F172A] placeholder:text-[#94A3B8]"
              />
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-[#475569] ml-1">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 bg-white border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#5B21FF] focus:border-[#5B21FF] transition-all text-[#0F172A] placeholder:text-[#94A3B8]"
            />
          </div>

          {(mode === 'login' || mode === 'signup') && (
            <div className="space-y-1.5">
              <div className="flex justify-between items-center ml-1">
                <label className="text-xs font-semibold text-[#475569]">Password</label>
                {mode === 'login' && (
                  <button type="button" onClick={() => switchMode('forgot')} className="text-xs text-[#5B21FF] hover:underline">
                    Forgot password?
                  </button>
                )}
              </div>
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
          )}

          <button
            type="submit"
            disabled={isLoading || !!successMsg}
            className="w-full mt-6 py-3 bg-[#5B21FF] hover:bg-[#4C1DE0] text-white rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
              <>
                {mode === 'login' && "Sign In"}
                {mode === 'signup' && "Get Started"}
                {mode === 'magic' && "Send Magic Link"}
                {mode === 'forgot' && "Send Reset Instructions"}
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Footer Toggles */}
        <div className="mt-8 text-center border-t border-[#E2E8F0] pt-6 flex flex-col gap-3">
          {mode === 'login' && (
            <button type="button" onClick={() => switchMode('magic')} className="text-sm font-medium text-[#64748B] hover:text-[#0F172A]">
              Sign in with <span className="text-[#5B21FF] font-semibold">Magic Link</span>
            </button>
          )}
          
          {(mode === 'magic' || mode === 'forgot') && (
            <button type="button" onClick={() => switchMode('login')} className="text-sm font-medium text-[#64748B] hover:text-[#0F172A]">
              Back to <span className="text-[#5B21FF] font-semibold">Log in</span>
            </button>
          )}

          <button 
            onClick={() => switchMode(mode === 'signup' ? 'login' : 'signup')}
            type="button"
            className="text-sm font-medium text-[#64748B]"
          >
            {mode === 'signup' ? "Already have an account? " : "Don't have an account? "}
            <span className="text-[#5B21FF] hover:underline hover:text-[#4C1DE0] font-semibold">
              {mode === 'signup' ? "Log in" : "Sign up for free"}
            </span>
          </button>
        </div>

      </div>
    </div>
  );
}

export default function AuthPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#5B21FF]" /></div>}>
      <AuthPageContent />
    </Suspense>
  );
}
