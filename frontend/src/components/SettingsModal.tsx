"use client";

import { useState, useEffect } from "react";
import { X, Loader2, UserCircle, Lock, Save, LogOut, Cpu } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";

export function SettingsModal({ onClose }: { onClose: () => void }) {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState<"profile" | "security" | "integrations">("profile");

  const [displayName, setDisplayName] = useState(user?.user_metadata?.full_name || "");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [ollamaUrl, setOllamaUrl] = useState("http://localhost:11434");
  const [ollamaModel, setOllamaModel] = useState("llama3");
  const [openRouterKey, setOpenRouterKey] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    // Load integration settings from local storage
    const storedUrl = localStorage.getItem("ollama_url");
    const storedModel = localStorage.getItem("ollama_model");
    const storedKey = localStorage.getItem("openrouter_key");
    if (storedUrl) setOllamaUrl(storedUrl);
    if (storedModel) setOllamaModel(storedModel);
    if (storedKey) setOpenRouterKey(storedKey);
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);

    const { error } = await supabase.auth.updateUser({
      data: { full_name: displayName }
    });

    setIsLoading(false);
    if (error) {
      setMessage({ type: "error", text: error.message });
    } else {
      setMessage({ type: "success", text: "Profile updated successfully!" });
    }
  };

  const handleUpdatePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage({ type: "error", text: "Passwords do not match." });
      return;
    }
    if (password.length < 6) {
      setMessage({ type: "error", text: "Password must be at least 6 characters." });
      return;
    }

    setIsLoading(true);
    setMessage(null);

    const { error } = await supabase.auth.updateUser({ password });

    setIsLoading(false);
    if (error) {
      setMessage({ type: "error", text: error.message });
    } else {
      setMessage({ type: "success", text: "Password updated successfully!" });
      setPassword("");
      setConfirmPassword("");
    }
  };

  const handleUpdateIntegrations = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage(null);
    try {
      localStorage.setItem("ollama_url", ollamaUrl);
      localStorage.setItem("ollama_model", ollamaModel);
      localStorage.setItem("openrouter_key", openRouterKey);
      setMessage({ type: "success", text: "Integration settings saved locally." });
    } catch (err: any) {
      setMessage({ type: "error", text: "Failed to save settings." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-2xl w-full max-w-2xl border border-[#E2E8F0] flex overflow-hidden h-[500px]">
        {/* Sidebar */}
        <div className="w-48 bg-[#F8FAFC] border-r border-[#E2E8F0] p-4 flex flex-col shrink-0">
          <h2 className="text-sm font-bold text-[#0F172A] mb-4 px-2">Settings</h2>
          <nav className="space-y-1 flex-1">
            <button
              onClick={() => { setActiveTab("profile"); setMessage(null); }}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                activeTab === "profile" ? "bg-[#EDE9FF] text-[#5B21FF]" : "text-[#64748B] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
              }`}
            >
              <UserCircle className="w-4 h-4 shrink-0" />
              Profile
            </button>
            <button
              onClick={() => { setActiveTab("security"); setMessage(null); }}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                activeTab === "security" ? "bg-[#EDE9FF] text-[#5B21FF]" : "text-[#64748B] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
              }`}
            >
              <Lock className="w-4 h-4 shrink-0" />
              Security
            </button>
            <button
              onClick={() => { setActiveTab("integrations"); setMessage(null); }}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                activeTab === "integrations" ? "bg-[#EDE9FF] text-[#5B21FF]" : "text-[#64748B] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
              }`}
            >
              <Cpu className="w-4 h-4 shrink-0" />
              AI Integrations
            </button>
          </nav>

          <div className="pt-4 border-t border-[#E2E8F0]">
            <button
              onClick={() => {
                logout();
                onClose();
              }}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-md text-xs font-medium text-[#EF4444] hover:bg-[#FEF2F2] transition-colors"
            >
              <LogOut className="w-4 h-4 shrink-0" />
              Sign Out
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 flex flex-col">
          <header className="flex items-center justify-between px-6 py-4 border-b border-[#E2E8F0]">
            <h3 className="text-sm font-semibold text-[#0F172A]">
              {activeTab === "profile" && "Public Profile"}
              {activeTab === "security" && "Security & Password"}
              {activeTab === "integrations" && "AI Integrations"}
            </h3>
            <button onClick={onClose} className="text-[#94A3B8] hover:text-[#0F172A] transition-colors p-1 rounded-md hover:bg-[#F1F5F9]">
              <X className="w-4 h-4" />
            </button>
          </header>

          <div className="flex-1 overflow-y-auto p-6">
            {message && (
              <div className={`mb-6 p-3 rounded-md text-xs font-medium flex items-center gap-2 ${
                message.type === "success" ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"
              }`}>
                {message.text}
              </div>
            )}

            {activeTab === "profile" && (
              <form onSubmit={handleUpdateProfile} className="space-y-5 max-w-sm">
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Email address</label>
                  <input
                    type="email"
                    value={user?.email || ""}
                    disabled
                    className="w-full border border-[#E2E8F0] bg-[#F8FAFC] rounded-md px-3 py-2 text-sm text-[#94A3B8] cursor-not-allowed"
                  />
                  <p className="text-[10px] text-[#94A3B8] mt-1.5">Email address cannot be changed currently.</p>
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Display name</label>
                  <input
                    type="text"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="Enter your name"
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                </div>

                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-primary text-xs py-2 px-4 inline-flex"
                  >
                    {isLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin mr-1.5" /> : <Save className="w-3.5 h-3.5 mr-1.5" />}
                    Save Changes
                  </button>
                </div>
              </form>
            )}

            {activeTab === "security" && (
              <form onSubmit={handleUpdatePassword} className="space-y-5 max-w-sm">
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">New password</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Min. 6 characters"
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Confirm new password</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                </div>

                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={isLoading || !password || !confirmPassword}
                    className="btn-primary text-xs py-2 px-4 inline-flex"
                  >
                    {isLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin mr-1.5" /> : <Lock className="w-3.5 h-3.5 mr-1.5" />}
                    Update Password
                  </button>
                </div>
              </form>
            )}

            {activeTab === "integrations" && (
              <form onSubmit={handleUpdateIntegrations} className="space-y-5 max-w-sm">
                <div className="p-3 bg-blue-50 border border-blue-200 rounded-md text-xs text-blue-800 mb-4">
                  <strong>Note:</strong> ClipForge AI prefers Free-First routing. Set up local models with Ollama, or use OpenRouter for free models.
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Ollama Base URL</label>
                  <input
                    type="url"
                    value={ollamaUrl}
                    onChange={(e) => setOllamaUrl(e.target.value)}
                    placeholder="http://localhost:11434"
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">Ollama Default Model</label>
                  <input
                    type="text"
                    value={ollamaModel}
                    onChange={(e) => setOllamaModel(e.target.value)}
                    placeholder="llama3"
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                </div>

                <div className="border-t border-[#E2E8F0] pt-4 mt-2">
                  <label className="block text-xs font-medium text-[#64748B] mb-1.5">OpenRouter API Key (Optional)</label>
                  <input
                    type="password"
                    value={openRouterKey}
                    onChange={(e) => setOpenRouterKey(e.target.value)}
                    placeholder="sk-or-..."
                    className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A]"
                  />
                  <p className="text-[10px] text-[#94A3B8] mt-1.5">Used as a fallback when Ollama is unavailable.</p>
                </div>

                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-primary text-xs py-2 px-4 inline-flex"
                  >
                    {isLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin mr-1.5" /> : <Save className="w-3.5 h-3.5 mr-1.5" />}
                    Save Integrations
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
