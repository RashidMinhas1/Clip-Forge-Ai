import Link from "next/link";
import { CheckCircle2, Scissors } from "lucide-react";
import { Navbar } from "@/components/Navbar";

export default function PricingPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: "#F8FAFC" }}>
      <Navbar />

      <main className="flex-1">
        {/* Header */}
        <section className="pt-20 pb-12 px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-[#0F172A] mb-3">
            Simple, transparent pricing.
          </h1>
          <p className="text-[#64748B] text-base max-w-lg mx-auto">
            One plan for solo creators, one for teams, one for agencies. No hidden fees.
          </p>
        </section>

        {/* Cards */}
        <section className="pb-24 px-4">
          <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-5 items-start">

            {/* Free */}
            <div className="bg-white border border-[#E2E8F0] rounded-xl p-7 flex flex-col">
              <h3 className="text-sm font-semibold text-[#0F172A] mb-1">Local / Free</h3>
              <p className="text-xs text-[#94A3B8] mb-6">For solo creators on their own hardware.</p>
              <div className="mb-7">
                <span className="text-4xl font-bold text-[#0F172A]">$0</span>
                <span className="text-sm text-[#94A3B8] font-medium"> / month</span>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {[
                  "Local Ollama LLM integration",
                  "Whisper transcription",
                  "Manual local file uploads",
                  "Candidate review UI",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-[#0F172A]">
                    <CheckCircle2 className="w-4 h-4 text-[#5B21FF] shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                href="/signup"
                className="btn-secondary w-full justify-center text-sm py-2.5"
              >
                Get Started Free
              </Link>
            </div>

            {/* Pro — highlighted */}
            <div className="bg-[#0F172A] border border-[#1E293B] rounded-xl p-7 flex flex-col relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#5B21FF] text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-widest">
                Popular
              </div>
              <h3 className="text-sm font-semibold text-white mb-1">Creator Pro</h3>
              <p className="text-xs text-[#64748B] mb-6">Cloud AI with all integrations unlocked.</p>
              <div className="mb-7">
                <span className="text-4xl font-bold text-white">$29</span>
                <span className="text-sm text-[#64748B] font-medium"> / month</span>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {[
                  "OpenAI & OpenRouter integration",
                  "YouTube URL ingestion",
                  "Advanced AI Clip Discovery",
                  "Priority cloud processing",
                  "100 hours of video / month",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-[#CBD5E1]">
                    <CheckCircle2 className="w-4 h-4 text-[#5B21FF] shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                href="/signup"
                className="btn-primary w-full justify-center text-sm py-2.5"
              >
                Start Pro Trial
              </Link>
            </div>

            {/* Agency */}
            <div className="bg-white border border-[#E2E8F0] rounded-xl p-7 flex flex-col">
              <h3 className="text-sm font-semibold text-[#0F172A] mb-1">Agency</h3>
              <p className="text-xs text-[#94A3B8] mb-6">For teams managing multiple clients.</p>
              <div className="mb-7">
                <span className="text-4xl font-bold text-[#0F172A]">$99</span>
                <span className="text-sm text-[#94A3B8] font-medium"> / month</span>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {[
                  "Unlimited video processing",
                  "Custom branding & templates",
                  "Team collaboration tools",
                  "Full API access",
                  "24/7 priority support",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-[#0F172A]">
                    <CheckCircle2 className="w-4 h-4 text-[#5B21FF] shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                href="/signup"
                className="btn-secondary w-full justify-center text-sm py-2.5"
              >
                Contact Sales
              </Link>
            </div>

          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-[#E2E8F0] py-10 px-4">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-[#5B21FF] rounded flex items-center justify-center">
              <Scissors className="text-white w-3.5 h-3.5" />
            </div>
            <span className="font-bold text-[#0F172A]">ClipForge AI</span>
          </div>
          <p className="text-sm text-[#94A3B8]">
            &copy; {new Date().getFullYear()} ClipForge AI. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
