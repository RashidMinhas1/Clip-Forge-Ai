# ClipForge AI — Global Engineering & Development Rules

> **Status**: LOCKED (Foundation Phase Verified)  
> **Scope**: Master Application & Development Governance  
> **Version**: 1.1.0  

---

## 1. Development & Chat Workflow Rules

### 1.1 Milestone Execution Lifecycle
Every interaction and feature engineering task must strictly follow this milestone execution lifecycle:

```
PLANNING
   ↓
ANALYSIS
   ↓
IMPLEMENTATION / REFACTOR PLAN
   ↓
FEATURE AGENT DOCUMENTATION (.agent.md)
   ↓
USER REVIEW / APPROVAL
   ↓
MILESTONE BRANCH
   ↓
IMPLEMENTATION
   ↓
TESTING
   ↓
VERIFICATION
   ↓
FIXES IF REQUIRED
   ↓
RE-VERIFICATION
   ↓
VERIFICATION REPORT (milestone-XXX-verification-report.md)
   ↓
USER APPROVAL
   ↓
GITHUB PUSH
   ↓
MERGE / PULL
   ↓
MILESTONE LOCKED
```

### 1.2 Development Execution Directives
- **Planning First**: Analysis, implementation plans (`/docs/milestones/milestone-XXX/milestone-XXX-plan.md`), and feature agent files (`/docs/features/FEATURE_NAME.agent.md`) MUST be created and approved *before* writing code.
- **Verification Mandatory**: A milestone is NOT complete merely because code exists. A milestone is complete ONLY after passing all functional, security, performance, media, and UI tests recorded in a formal Verification Report (`milestone-XXX-verification-report.md`).
- **Sequential Approval**: Never start implementation on a milestone without explicit user approval of the implementation plan and feature agent files.
- **Dynamic Milestone Scope**: The application does not enforce a hardcoded number of future product milestones; product milestone allocation is finalized post-PRD creation.

---

## 2. Application Engineering Rules

### 2.1 Core Architectural Principles
- **Modular Monolith**: Maintain a cohesive modular monolith structure (`Next.js + FastAPI + PostgreSQL + Redis + Taskiq + FFmpeg`). Microservices, Kubernetes, or Kafka are strictly forbidden unless explicit throughput metrics require isolation.
- **Layered Separation**: Enforce clear boundaries:
  `Frontend → API Layer → Service / Application Layer → Domain Logic → Infrastructure (DB, AI Router, Media Engine, Taskiq/Redis Queue, Storage)`.
- **Stateless API & Async Background Jobs**: HTTP requests must NEVER block on long-running media ingestion, transcription, AI clip extraction, or FFmpeg rendering tasks. All long-running operations MUST be offloaded to **Taskiq + Redis** background workers with state machines (`QUEUED`, `PROCESSING`, `PROGRESS`, `COMPLETED`, `FAILED`).

### 2.2 Feature Agent (`.agent.md`) System
- Every technical feature MUST have its own standalone specification file in `docs/features/FEATURE_NAME.agent.md`.
- Never rely on a single generic agent file.
- The `.agent.md` file serves as the **authoritative behavioral specification**. Implementation must conform to `.agent.md`.
- Behavior changes require updating `.agent.md` -> re-plan -> user approval -> update code -> verify.

### 2.3 No Fake Success & No Silent Mock Fallbacks
- NEVER return fake mock data in production or runtime flows to simulate success.
- NEVER replace a failed real AI call with static hardcoded fallback data.
- System states must explicitly distinguish: `REAL RESULT`, `MOCK RESULT` (test environment only), `PENDING`, `PROGRESS`, `FAILED`, `ERROR`.
- If an external provider fails, capture the error, sanitize logs, present a safe user error message, and offer retry mechanisms.

### 2.4 Application-Level Tenant Isolation & Data Privacy
- **Application-Level Authorization**: Security boundaries are governed by explicit application-level ownership checks (`WHERE user_id = authenticated_user.id`) for all user-owned entities (Projects, Sources, Videos, Transcripts, Clips, Edits, Captions, Render Jobs, Exports, AI Jobs).
- **PostgreSQL Row-Level Security (RLS)**: PostgreSQL RLS may be evaluated as a future defense-in-depth layer, but application-level tenant isolation is the active security boundary.
- **File System Isolation**: Video files, audio clips, thumbnails, and transcripts must be stored in isolated user directories and purged automatically upon job completion or failure.
- **Authorized Media Access**: Pre-signed URLs or authenticated streaming endpoints must validate authorization headers before serving media streams.

### 2.5 Security & Secret Safety
- Hardcoding secrets, API keys, credentials, or private tokens in code, comments, or UI bundles is strictly prohibited.
- All secrets must be loaded via environment variables validated on server startup (`pydantic-settings`).
- Pre-commit checks must ensure `.env` and sensitive media files are never committed or pushed to GitHub.

---

## 3. Git & Branching Strategy

- **Main Branch Protection**: Direct commits or pushes to `main` are strictly forbidden.
- **Milestone Branching Pattern**: All work happens in isolated feature/milestone branches using the naming convention `milestone/XXX-name` (e.g., `milestone/001-foundation`).
- **Merge Criteria**: Merges to `main` require a clean verification report (`PASS` status) and explicit user approval.
