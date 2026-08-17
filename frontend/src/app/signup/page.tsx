import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute top-0 w-full h-full bg-hero-gradient opacity-40 pointer-events-none" />
      
      <div className="w-full max-w-md bg-card p-8 rounded-2xl shadow-xl border border-border/50 relative z-10 flex flex-col items-center text-center">
        
        <div className="w-12 h-12 bg-brand-light rounded-xl flex items-center justify-center mb-6">
          <Sparkles className="text-brand-purple w-6 h-6" />
        </div>
        
        <h1 className="text-3xl font-bold tracking-tight mb-2">Create an Account</h1>
        <p className="text-muted-foreground mb-8">
          Join Clip Forge AI to start transforming your long videos into viral clips.
        </p>

        {/* Placeholder form elements to make it look like a real signup */}
        <div className="w-full space-y-4 mb-8">
          <div className="space-y-2 text-left">
            <label className="text-sm font-medium text-foreground">Name</label>
            <input 
              type="text" 
              placeholder="Jane Doe" 
              className="w-full px-4 py-3 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-purple/50"
              disabled
            />
          </div>
          <div className="space-y-2 text-left">
            <label className="text-sm font-medium text-foreground">Email</label>
            <input 
              type="email" 
              placeholder="you@example.com" 
              className="w-full px-4 py-3 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-purple/50"
              disabled
            />
          </div>
          <div className="space-y-2 text-left">
            <label className="text-sm font-medium text-foreground">Password</label>
            <input 
              type="password" 
              placeholder="Create a strong password" 
              className="w-full px-4 py-3 bg-secondary/30 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-purple/50"
              disabled
            />
          </div>
        </div>

        <Link 
          href="/projects" 
          className="w-full bg-brand-purple hover:bg-brand-purple/90 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all shadow-md shadow-brand-purple/20 group"
        >
          Get Started
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </Link>
        
        <p className="mt-6 text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/login" className="text-brand-purple font-medium hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
