import Link from "next/link";
import { ArrowRight, Video, Scissors, Sparkles, CheckCircle2, Youtube } from "lucide-react";
import { Navbar } from "@/components/Navbar";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: "#F8FAFC", color: "#0F172A" }}>
      <Navbar />

      <main className="flex-1">
        {/* ── Hero ── */}
        <section className="pt-24 pb-28 px-4 text-center">
          <div className="inline-flex items-center gap-1.5 text-xs font-medium text-[#5B21FF] bg-[#EDE9FF] border border-[#C4B5FD] px-3 py-1 rounded-full mb-10 tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            ClipForge AI 1.0 — Now Available
          </div>

          <h1 className="text-[3.25rem] md:text-[4.5rem] font-extrabold tracking-[-0.03em] leading-[1.1] text-[#0F172A] max-w-3xl mx-auto mb-6">
            Turn long videos into{" "}
            <span className="text-[#5B21FF]">viral clips</span>{" "}
            with AI.
          </h1>

          <p className="text-lg text-[#64748B] max-w-xl mx-auto mb-12 leading-relaxed">
            Automatically find engaging moments, add captions, and format for TikTok, Shorts, and Reels — in one click.
          </p>

          {/* CTA input row */}
          <div className="max-w-lg mx-auto flex items-center gap-0 bg-white border border-[#CBD5E1] rounded-xl overflow-hidden shadow-sm">
            <div className="flex items-center gap-2 flex-1 px-4">
              <Youtube className="w-4 h-4 text-[#94A3B8] shrink-0" />
              <input
                type="text"
                placeholder="Paste YouTube URL..."
                className="w-full py-3.5 text-sm bg-transparent border-none outline-none placeholder:text-[#94A3B8] text-[#0F172A]"
              />
            </div>
            <Link
              href="/auth?mode=signup"
              className="btn-primary rounded-none rounded-r-xl py-3.5 px-6 text-sm font-semibold whitespace-nowrap"
            >
              Get Started
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="mt-6 flex items-center justify-center gap-6 text-sm text-[#94A3B8]">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#5B21FF]" />
              No credit card
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#5B21FF]" />
              Free tier available
            </span>
          </div>
        </section>

        {/* ── Trust bar ── */}
        <section className="py-10 border-y border-[#E2E8F0] bg-white">
          <p className="text-center text-xs font-semibold text-[#94A3B8] tracking-widest uppercase mb-8">
            Trusted by creators and agencies
          </p>
          <div className="flex flex-wrap justify-center gap-12 opacity-40 grayscale">
            <span className="text-lg font-bold font-serif text-[#0F172A]">CreatorMedia</span>
            <span className="text-lg font-bold text-[#0F172A]">ViralTech</span>
            <span className="text-lg font-bold text-[#0F172A]">StudioPro</span>
            <span className="text-lg font-bold font-mono text-[#0F172A]">NEXTGEN</span>
          </div>
        </section>

        {/* ── Features ── */}
        <section id="features" className="py-24 px-4">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-[#0F172A] mb-4">
                Everything you need to repurpose content fast.
              </h2>
              <p className="text-[#64748B] text-base max-w-xl mx-auto">
                Built on a real AI pipeline — not a wrapper. ClipForge runs local or cloud models to understand your video.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  icon: Video,
                  title: "Multi-Source Ingestion",
                  body: "Import from local files, YouTube URLs, or Google Drive. Our pipeline validates and normalises every format automatically.",
                  color: "#5B21FF",
                },
                {
                  icon: Sparkles,
                  title: "AI Clip Discovery",
                  body: "Whisper transcribes your video at word-level accuracy, then an LLM scores each segment for hook strength and viral potential.",
                  color: "#DB2777",
                },
                {
                  icon: Scissors,
                  title: "Local & Cloud LLMs",
                  body: "Connect OpenAI, OpenRouter, or Gemini for cloud power — or keep everything private with Ollama running on your own machine.",
                  color: "#EA580C",
                },
              ].map((f) => (
                <div
                  key={f.title}
                  className="bg-white border border-[#E2E8F0] rounded-xl p-7 hover:border-[#C4B5FD] transition-colors"
                >
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center mb-5"
                    style={{ background: f.color + "15" }}
                  >
                    <f.icon className="w-5 h-5" style={{ color: f.color }} />
                  </div>
                  <h3 className="text-base font-semibold text-[#0F172A] mb-2">{f.title}</h3>
                  <p className="text-sm text-[#64748B] leading-relaxed">{f.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── CTA ── */}
        <section className="py-20 px-4 bg-[#0F172A] text-white text-center">
          <div className="max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">
              Ready to scale your content?
            </h2>
            <p className="text-[#94A3B8] mb-10 text-base leading-relaxed">
              Join creators turning long-form video into months of social content — automatically.
            </p>
            <Link
              href="/auth?mode=signup"
              className="inline-flex items-center gap-2 bg-[#5B21FF] hover:bg-[#4c1aee] text-white text-sm font-semibold px-6 py-3 rounded-lg border border-[#4c1aee] transition-colors"
            >
              Start for Free
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </section>
      </main>

      {/* ── Footer ── */}
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
          <div className="flex gap-6 text-sm text-[#64748B]">
            <Link href="#" className="hover:text-[#0F172A] transition-colors">Privacy</Link>
            <Link href="#" className="hover:text-[#0F172A] transition-colors">Terms</Link>
            <Link href="#" className="hover:text-[#0F172A] transition-colors">Contact</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
