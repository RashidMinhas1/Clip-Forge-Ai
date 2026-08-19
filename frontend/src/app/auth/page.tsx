"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Loader2, Scissors, ArrowRight } from "lucide-react";
import Link from "next/link";

function AuthPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const defaultMode = searchParams.get("mode") === "login" ? "login" : "signup";
  
  const [isLogin, setIsLogin] = useState(defaultMode === "login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Update state if URL changes
  useEffect(() => {
    setIsLogin(searchParams.get("mode") === "login");
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      if (isLogin) {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
        router.push("/projects");
      } else {
        const { error: signUpError } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              full_name: name,
            }
          }
        });
        if (signUpError) throw signUpError;
        
        // Auto sign in after sign up is standard for Supabase if email confirmation is off
        router.push("/projects");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during authentication.");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setError(null);
    setIsLogin(!isLogin);
    // Optional: update the URL silently
    router.replace(`/auth?mode=${!isLogin ? "login" : "signup"}`, { scroll: false });
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
            {isLogin ? "Welcome back" : "Create an account"}
          </h1>
          <p className="text-sm text-[#64748B] px-2 leading-relaxed">
            Join Clip Forge AI to start transforming your long videos into viral clips.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-3 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100 text-center">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#475569] ml-1">Name</label>
              <input
                type="text"
                placeholder="Jane Doe"
                required={!isLogin}
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

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-[#475569] ml-1">Password</label>
            <input
              type="password"
              placeholder="Create a strong password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 bg-white border border-[#E2E8F0] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#5B21FF] focus:border-[#5B21FF] transition-all text-[#0F172A] placeholder:text-[#94A3B8]"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-6 py-3 bg-[#5B21FF] hover:bg-[#4C1DE0] text-white rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
              <>
                {isLogin ? "Sign In" : "Get Started"}
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Footer Toggle */}
        <div className="mt-8 text-center border-t border-[#E2E8F0] pt-6">
          <button 
            onClick={toggleMode}
            type="button"
            className="text-sm font-medium text-[#64748B]"
          >
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span className="text-[#5B21FF] hover:underline hover:text-[#4C1DE0] font-semibold">
              {isLogin ? "Sign up for free" : "Log in"}
            </span>
          </button>
        </div>

      </div>
    </div>
  );
}

import { Suspense } from 'react';

export default function AuthPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-[#5B21FF]" /></div>}>
      <AuthPageContent />
    </Suspense>
  );
}
