"use client";

import { useState } from "react";
import { useProject } from "@/contexts/ProjectContext";
import {
  PlusCircle,
  Loader2,
  FolderOpen,
  Check,
  Scissors,
  LayoutDashboard,
  Video,
  Sparkles,
  Upload,
  ChevronRight,
  Zap,
  Clock,
  Film,
  Search,
  X,
} from "lucide-react";
import Link from "next/link";

const navItems = [
  { label: "Projects", icon: LayoutDashboard, href: "/projects", active: true },
  { label: "Ingest Video", icon: Upload, href: "/ingest", active: false },
  { label: "AI Clips", icon: Sparkles, href: "/ingest", active: false },
  { label: "Pricing", icon: Zap, href: "/pricing", active: false },
];

function StatCard({ icon: Icon, label, value, accent }: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  accent: string;
}) {
  return (
    <div className="bg-white border border-[#E2E8F0] rounded-lg p-5 flex items-center gap-4">
      <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0" style={{ background: accent + "18" }}>
        <Icon className="w-5 h-5" style={{ color: accent }} />
      </div>
      <div>
        <p className="text-xs text-[#94A3B8] font-medium">{label}</p>
        <p className="text-xl font-bold text-[#0F172A] mt-0.5">{value}</p>
      </div>
    </div>
  );
}

export default function ProjectsPage() {
  const { projects, activeProject, loading, error, createProject, setActiveProject } = useProject();
  const [newProjectName, setNewProjectName] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [search, setSearch] = useState("");

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;
    setIsCreating(true);
    try {
      await createProject(newProjectName.trim());
      setNewProjectName("");
      setShowCreateModal(false);
    } catch (_) { /* handled in context */ } finally {
      setIsCreating(false);
    }
  };

  const filtered = projects.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex min-h-screen" style={{ background: "#F8FAFC" }}>
      {/* ── Sidebar ── */}
      <aside className="w-56 bg-white border-r border-[#E2E8F0] flex flex-col shrink-0">
        {/* Logo */}
        <div className="flex items-center gap-2 px-5 h-14 border-b border-[#E2E8F0]">
          <div className="w-6 h-6 bg-[#5B21FF] rounded flex items-center justify-center">
            <Scissors className="text-white w-3.5 h-3.5" />
          </div>
          <span className="font-bold text-[#0F172A] text-sm">ClipForge AI</span>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-3 space-y-0.5">
          {navItems.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                item.active
                  ? "bg-[#EDE9FF] text-[#5B21FF]"
                  : "text-[#64748B] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
              }`}
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {item.label}
            </Link>
          ))}
        </nav>

        {/* Active project chip */}
        <div className="p-3 border-t border-[#E2E8F0]">
          {activeProject ? (
            <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-md p-3">
              <p className="text-[10px] text-[#94A3B8] font-semibold uppercase tracking-wider mb-1">Active</p>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
                <p className="text-xs font-medium text-[#0F172A] truncate">{activeProject.name}</p>
              </div>
            </div>
          ) : (
            <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-md px-3 py-2">
              <p className="text-xs text-[#94A3B8]">No active project</p>
            </div>
          )}
        </div>
      </aside>

      {/* ── Main ── */}
      <div className="flex-1 flex flex-col min-h-screen overflow-auto">
        {/* Top header */}
        <header className="bg-white border-b border-[#E2E8F0] h-14 px-8 flex items-center justify-between sticky top-0 z-10">
          <div>
            <h1 className="text-sm font-semibold text-[#0F172A]">Projects</h1>
            <p className="text-xs text-[#94A3B8]">Manage your video workspaces</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary text-xs py-1.5 px-4"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            New project
          </button>
        </header>

        <div className="p-8 space-y-7 flex-1">
          {/* Error */}
          {error && (
            <div className="flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
              <X className="w-4 h-4 shrink-0" />
              Backend not reachable — start the server on port 8000 to load projects.
            </div>
          )}

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard icon={FolderOpen} label="Total Projects" value={projects.length} accent="#5B21FF" />
            <StatCard icon={Film}       label="Completed"      value={projects.filter(p => p.status === "active").length} accent="#16A34A" />
            <StatCard icon={Clock}      label="Processing"     value={projects.filter(p => p.status === "processing").length} accent="#EA580C" />
            <StatCard icon={Zap}        label="AI Providers"   value="3 Ready" accent="#DB2777" />
          </div>

          {/* Quick actions */}
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { title: "Ingest from YouTube", desc: "Paste a URL — we handle the download and validation.", icon: Video,    accent: "#5B21FF", href: "/ingest" },
              { title: "Upload Local File",   desc: "MP4, MOV, MKV or WebM directly from your drive.",    icon: Upload,   accent: "#EA580C", href: "/ingest" },
              { title: "AI Clip Discovery",   desc: "Score & rank candidate clips with your LLM of choice.", icon: Sparkles, accent: "#DB2777", href: "/ingest" },
            ].map((item) => (
              <Link
                key={item.title}
                href={item.href}
                className="bg-white border border-[#E2E8F0] rounded-lg p-5 flex items-start gap-4 hover:border-[#C4B5FD] transition-colors group"
              >
                <div className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 mt-0.5" style={{ background: item.accent + "18" }}>
                  <item.icon className="w-5 h-5" style={{ color: item.accent }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold mb-0.5" style={{ color: "#0F172A" }}>{item.title}</p>
                  <p className="text-xs leading-relaxed" style={{ color: "#94A3B8" }}>{item.desc}</p>
                </div>
                <ChevronRight className="w-4 h-4 shrink-0 mt-1 transition-colors" style={{ color: "#CBD5E1" }} />
              </Link>
            ))}
          </div>

          {/* Projects list */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-[#0F172A]">Your projects</h2>
              {projects.length > 0 && (
                <div className="relative">
                  <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="pl-8 pr-3 py-1.5 text-xs bg-white border border-[#E2E8F0] rounded-md focus:outline-none focus:ring-1 focus:ring-[#5B21FF] w-44 text-[#0F172A] placeholder:text-[#94A3B8]"
                  />
                </div>
              )}
            </div>

            {loading ? (
              <div className="flex justify-center py-16">
                <Loader2 className="w-6 h-6 animate-spin text-[#94A3B8]" />
              </div>
            ) : filtered.length === 0 ? (
              <div className="bg-white border border-dashed border-[#CBD5E1] rounded-lg py-16 text-center">
                <div className="w-10 h-10 bg-[#EDE9FF] rounded-lg flex items-center justify-center mx-auto mb-3">
                  <FolderOpen className="w-5 h-5 text-[#5B21FF]" />
                </div>
                <p className="text-sm font-medium text-[#0F172A] mb-1">No projects yet</p>
                <p className="text-xs text-[#94A3B8] mb-6">Create one to get started.</p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="btn-primary text-xs py-1.5 px-4 mx-auto"
                >
                  <PlusCircle className="w-3.5 h-3.5" />
                  Create project
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                {filtered.map((project) => {
                  const isActive = activeProject?.id === project.id;
                  return (
                    <div
                      key={project.id}
                      className={`bg-white border rounded-lg px-5 py-4 flex items-center justify-between transition-colors ${
                        isActive ? "border-[#C4B5FD]" : "border-[#E2E8F0] hover:border-[#CBD5E1]"
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${
                          isActive ? "bg-[#EDE9FF]" : "bg-[#F8FAFC]"
                        }`}>
                          <FolderOpen className={`w-4 h-4 ${isActive ? "text-[#5B21FF]" : "text-[#94A3B8]"}`} />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-[#0F172A]">{project.name}</span>
                            {isActive && (
                              <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-[#5B21FF] bg-[#EDE9FF] border border-[#C4B5FD] px-2 py-0.5 rounded-full uppercase tracking-wide">
                                <Check className="w-2.5 h-2.5" /> Active
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-3 mt-0.5">
                            <span className="text-xs text-[#94A3B8]">
                              {new Date(project.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
                            </span>
                            <span className="flex items-center gap-1 text-xs text-[#94A3B8]">
                              <span className={`w-1.5 h-1.5 rounded-full ${project.status === "active" ? "bg-green-500" : "bg-amber-400"}`} />
                              <span className="capitalize">{project.status}</span>
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        {!isActive && (
                          <button
                            onClick={() => setActiveProject(project)}
                            className="btn-secondary text-xs py-1.5 px-3"
                          >
                            Activate
                          </button>
                        )}
                        {isActive && (
                          <Link
                            href="/ingest"
                            className="btn-primary text-xs py-1.5 px-3"
                          >
                            Open
                          </Link>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ── Create Modal ── */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/30"
            onClick={() => setShowCreateModal(false)}
          />
          <div className="relative bg-white rounded-xl shadow-xl p-7 w-full max-w-sm border border-[#E2E8F0]">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-sm font-semibold text-[#0F172A]">New project</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-[#94A3B8] hover:text-[#0F172A] transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-[#64748B] mb-1.5">Project name</label>
                <input
                  type="text"
                  placeholder="e.g. Podcast Season 2"
                  className="w-full border border-[#E2E8F0] rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#5B21FF] focus:border-[#5B21FF] text-[#0F172A] placeholder:text-[#CBD5E1]"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  disabled={isCreating}
                  autoFocus
                />
              </div>
              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn-secondary flex-1 text-xs py-2"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isCreating || !newProjectName.trim()}
                  className="btn-primary flex-1 text-xs py-2"
                >
                  {isCreating ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <PlusCircle className="w-3.5 h-3.5" />}
                  {isCreating ? "Creating..." : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
