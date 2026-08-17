import Link from "next/link";
import { Scissors } from "lucide-react";

export function Navbar() {
  return (
    <nav className="w-full border-b border-[#E2E8F0] bg-white sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-14">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-[#5B21FF] rounded-md flex items-center justify-center">
              <Scissors className="text-white w-3.5 h-3.5" />
            </div>
            <Link href="/" className="font-bold text-[#0F172A] text-base tracking-tight">
              ClipForge AI
            </Link>
          </div>

          {/* Nav links */}
          <div className="hidden md:flex items-center gap-7 text-sm text-[#64748B]">
            <Link href="/#features" className="hover:text-[#0F172A] transition-colors">Features</Link>
            <Link href="/#how-it-works" className="hover:text-[#0F172A] transition-colors">How it works</Link>
            <Link href="/pricing" className="hover:text-[#0F172A] transition-colors">Pricing</Link>
          </div>

          {/* Auth actions */}
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm text-[#64748B] hover:text-[#0F172A] transition-colors font-medium"
            >
              Sign in
            </Link>
            <Link
              href="/signup"
              className="btn-primary text-sm py-1.5 px-4"
            >
              Sign up free
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
