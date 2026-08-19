"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useProject } from "@/contexts/ProjectContext";
import { useAuth } from "@/contexts/AuthContext";
import { projectApi } from "@/lib/api/projectClient";
import { listClipCandidates, discoverClips, updateClipCandidateStatus, ClipCandidate } from "@/lib/api";
import { CandidateCard } from "@/components/CandidateCard";
import { SettingsModal } from "@/components/SettingsModal";
import Link from "next/link";
import {
  Scissors,
  LayoutDashboard,
  Upload,
  Sparkles,
  Film,
  Zap,
  FolderOpen,
  UserCircle,
  Loader2,
  Check,
  ChevronRight,
  Video
} from "lucide-react";

export default function ProjectDashboard() {
  const params = useParams();
  const projectId = params.projectId as string;
  const router = useRouter();
  const { activeProject, setActiveProject, projects } = useProject();
  const { user } = useAuth();

  const [projectDetails, setProjectDetails] = useState<any>(null);
  const [candidates, setCandidates] = useState<ClipCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [discoveringFor, setDiscoveringFor] = useState<string | null>(null);
  const [showSettingsModal, setShowSettingsModal] = useState(false);

  useEffect(() => {
    async function loadData() {
      if (!projectId) return;
      try {
        setLoading(true);
        const [projRes, candidatesRes] = await Promise.all([
          projectApi.getProject(projectId),
          listClipCandidates(projectId)
        ]);
        setProjectDetails(projRes);
        setCandidates(candidatesRes || []);
        
        // Ensure this is the active project in context
        if (activeProject?.id !== projectId) {
          const matched = projects.find(p => p.id === projectId);
          if (matched) setActiveProject(matched);
          else setActiveProject(projRes);
        }
      } catch (err) {
        console.error("Failed to load project details", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [projectId, activeProject?.id, projects, setActiveProject]);

  const handleDiscoverClips = async (sourceId: string) => {
    setDiscoveringFor(sourceId);
    try {
      await discoverClips(projectId, sourceId);
      // Wait a moment and refresh candidates
      setTimeout(async () => {
        const freshCandidates = await listClipCandidates(projectId);
        setCandidates(freshCandidates || []);
        setDiscoveringFor(null);
      }, 5000);
    } catch (err) {
      console.error(err);
      setDiscoveringFor(null);
    }
  };

  const handleUpdateStatus = async (candidateId: string, status: 'approved' | 'rejected') => {
    try {
      const updatedCandidate = await updateClipCandidateStatus(projectId, candidateId, status);
      setCandidates(prev => prev.map(c => c.id === candidateId ? updatedCandidate : c));
    } catch (error) {
      console.error('Failed to update status', error);
    }
  };

  const navItems = [
    { label: "Projects", icon: LayoutDashboard, href: "/projects", active: false },
    { label: "Ingest Video", icon: Upload, href: "/ingest", active: false },
    { label: "AI Clips", icon: Sparkles, href: `/projects/${projectId}`, active: true },
    { label: "Exports", icon: Film, href: `/projects/${projectId}/exports`, active: false },
    { label: "Pricing", icon: Zap, href: "/pricing", active: false },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F8FAFC]">
        <Loader2 className="w-8 h-8 animate-spin text-[#5B21FF]" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen" style={{ background: "#F8FAFC" }}>
      {/* ── Sidebar ── */}
      <aside className="w-56 bg-white border-r border-[#E2E8F0] flex flex-col shrink-0 sticky top-0 h-screen overflow-y-auto">
        <div className="flex items-center gap-2 px-5 h-14 border-b border-[#E2E8F0]">
          <div className="w-6 h-6 bg-[#5B21FF] rounded flex items-center justify-center">
            <Scissors className="text-white w-3.5 h-3.5" />
          </div>
          <span className="font-bold text-[#0F172A] text-sm">ClipForge AI</span>
        </div>

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

        <div className="p-3 border-t border-[#E2E8F0]">
          {activeProject && (
            <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-md p-3">
              <p className="text-[10px] text-[#94A3B8] font-semibold uppercase tracking-wider mb-1">Active</p>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
                <p className="text-xs font-medium text-[#0F172A] truncate">{activeProject.name}</p>
              </div>
            </div>
          )}
        </div>

        <div className="p-3 border-t border-[#E2E8F0]">
          <button
            onClick={() => setShowSettingsModal(true)}
            className="w-full text-left bg-[#F8FAFC] border border-[#E2E8F0] rounded-md p-3 flex items-center gap-3 hover:border-[#C4B5FD] hover:bg-white transition-colors group"
          >
            <div className="w-8 h-8 rounded-full bg-[#5B21FF] text-white flex items-center justify-center text-sm font-bold shrink-0">
              {user?.user_metadata?.full_name ? user.user_metadata.full_name[0].toUpperCase() : (user?.email ? user.email[0].toUpperCase() : <UserCircle className="w-5 h-5" />)}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold text-[#0F172A] truncate group-hover:text-[#5B21FF] transition-colors">
                {user?.user_metadata?.full_name || user?.email || "User Account"}
              </p>
              <p className="text-[10px] text-[#64748B] truncate">Manage settings</p>
            </div>
          </button>
        </div>
      </aside>

      {/* ── Main ── */}
      <div className="flex-1 flex flex-col min-h-screen">
        <header className="bg-white border-b border-[#E2E8F0] h-14 px-8 flex items-center justify-between sticky top-0 z-10">
          <div>
            <h1 className="text-sm font-semibold text-[#0F172A]">{projectDetails?.name || "Project Dashboard"}</h1>
            <div className="flex items-center text-xs text-[#94A3B8] gap-1">
              <Link href="/projects" className="hover:text-[#5B21FF]">Projects</Link>
              <ChevronRight className="w-3 h-3" />
              <span>{projectDetails?.name}</span>
            </div>
          </div>
          <Link
            href="/ingest"
            className="btn-primary text-xs py-1.5 px-4 flex items-center gap-2"
          >
            <Upload className="w-3.5 h-3.5" />
            Add Source
          </Link>
        </header>

        <div className="p-8 space-y-8 flex-1 overflow-auto">
          {/* Sources Section */}
          <section>
            <h2 className="text-lg font-bold text-[#0F172A] mb-4 flex items-center gap-2">
              <Video className="w-5 h-5 text-[#5B21FF]" />
              Sources
            </h2>
            {projectDetails?.sources && projectDetails.sources.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {projectDetails.sources.map((source: any) => (
                  <div key={source.id} className="bg-white border border-[#E2E8F0] rounded-lg p-5">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-semibold px-2 py-1 bg-slate-100 rounded uppercase tracking-wider text-slate-600">
                        {source.source_type}
                      </span>
                      <span className={`text-xs font-semibold px-2 py-1 rounded capitalize ${
                        source.ingestion_status === 'accepted' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                      }`}>
                        {source.ingestion_status}
                      </span>
                    </div>
                    <h3 className="font-medium text-[#0F172A] text-sm truncate mb-1" title={source.title || source.id}>
                      {source.title || `Source ${source.id.substring(0, 8)}`}
                    </h3>
                    <p className="text-xs text-[#64748B] mb-4">
                      {source.duration ? `${Math.round(source.duration)}s` : "Unknown duration"} • {source.has_audio ? "Audio" : "No Audio"}
                    </p>
                    
                    <button
                      onClick={() => handleDiscoverClips(source.id)}
                      disabled={discoveringFor === source.id || source.ingestion_status !== 'accepted'}
                      className="w-full flex items-center justify-center gap-2 btn-secondary py-1.5 text-xs bg-[#F8FAFC]"
                    >
                      {discoveringFor === source.id ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Sparkles className="w-3.5 h-3.5" />
                      )}
                      {discoveringFor === source.id ? "Discovering..." : "Discover AI Clips"}
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white border border-dashed border-[#CBD5E1] rounded-lg py-12 text-center">
                <Video className="w-8 h-8 text-[#94A3B8] mx-auto mb-3" />
                <p className="text-sm font-medium text-[#0F172A] mb-1">No sources yet</p>
                <p className="text-xs text-[#94A3B8] mb-4">Ingest a YouTube URL or upload a local file to get started.</p>
                <Link href="/ingest" className="btn-primary text-xs py-1.5 px-4 mx-auto inline-flex items-center gap-2">
                  <Upload className="w-3.5 h-3.5" />
                  Add Source
                </Link>
              </div>
            )}
          </section>

          {/* AI Candidates Section */}
          <section>
            <h2 className="text-lg font-bold text-[#0F172A] mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-[#DB2777]" />
              AI Clip Candidates
            </h2>
            {candidates.length > 0 ? (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {candidates.map((clip) => (
                  <CandidateCard key={clip.id} clip={clip} onUpdateStatus={handleUpdateStatus} />
                ))}
              </div>
            ) : (
              <div className="bg-white border border-dashed border-[#CBD5E1] rounded-lg py-12 text-center">
                <Sparkles className="w-8 h-8 text-[#94A3B8] mx-auto mb-3" />
                <p className="text-sm font-medium text-[#0F172A] mb-1">No clip candidates yet</p>
                <p className="text-xs text-[#94A3B8]">Click &quot;Discover AI Clips&quot; on a source to generate highlights.</p>
              </div>
            )}
          </section>
        </div>
      </div>
      
      {showSettingsModal && <SettingsModal onClose={() => setShowSettingsModal(false)} />}
    </div>
  );
}
