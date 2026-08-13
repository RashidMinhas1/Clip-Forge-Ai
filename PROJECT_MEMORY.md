# ClipForge AI — Project Memory & Orientation

> **Status**: ACTIVE (MS-002 Verified — Application Runtime & Infrastructure)  
> **Purpose**: High-density context document for rapid onboarding of AI agents and human developers.

---

## 1. Executive Summary

ClipForge AI is an advanced AI-powered short-form video clip generation platform. It automatically processes long-form videos (uploaded locally or ingested via YouTube), performs speech-to-text transcription, executes multi-dimensional AI vitality scoring to identify compelling short clips, and provides a lightweight editor for visual framing, dynamic caption styling, and automated FFmpeg video rendering.

---

## 2. Current Project State

- **Current Lifecycle Stage**: `MS-002 VERIFICATION PASS — AWAITING MERGE & LOCK`
- **Product Features State**: `0% Implemented` (Product features strictly barred until post-MS-002).
- **Git Branch**: `milestone/002-application-runtime-infrastructure`
- **GitHub Sync**: Branch pushed to `https://github.com/RashidMinhas1/Clip-Forge-Ai.git` — awaiting user approval for merge.
- **Next Required Stage**: `USER APPROVAL → MERGE → MILESTONE LOCK → MS-003 PLANNING`.
- **MS-002 Verification Status**: `PASS WITH ENVIRONMENTAL EXCEPTION` — all application-level tests passed; Docker container verification BLOCKED (Docker Desktop unavailable in verification environment).

---

## 3. Core Architectural Decisions

1. **Tech Stack**: Next.js (TypeScript + Tailwind CSS + shadcn/ui) + FastAPI (Python 3.11+) + PostgreSQL (SQLAlchemy Async) + Taskiq + Redis + FFmpeg.
2. **Background Jobs**: Taskiq + Redis (selected for Python `asyncio` native compatibility, FastAPI integration, and lightweight execution for AI/media workloads).
3. **Rule Layers**: Enforces Dual Rule System (Development/Chat Workflow Rules vs Application Engineering Rules).
4. **Security Model**: Application-level tenant isolation (`WHERE user_id = authenticated_user.id`). PostgreSQL RLS reserved for future defense-in-depth evaluation.
5. **Feature Agent Rule**: Every major capability requires a dedicated `docs/features/FEATURE_NAME.agent.md` file governing behavioral logic, validation rules, AI output schemas, and forbidden behavior.
6. **Planning Enforcer**: No code execution without an approved `/docs/milestones/milestone-XXX/milestone-XXX-plan.md`.
7. **No Mock Fallbacks**: Production code must NEVER return static fake AI outputs or hide API failures.

---

## 4. Key Directory Sitemap

```
/
├── GLOBAL_RULES.md            <- Universal engineering & workflow rules
├── DEVELOPMENT_WORKFLOW.md   <- Milestone execution lifecycle protocol
├── TECH_STACK.md             <- Full stack evaluation and driver matrix
├── ARCHITECTURE.md           <- Modular monolith blueprint & Taskiq architecture
├── SECURITY_RULES.md         <- Application tenant isolation & security rules
├── PROJECT_STRUCTURE.md      <- Full directory layout map
├── FEATURE_REGISTRY.md       <- Index of feature agent specs
├── MILESTONE_REGISTRY.md     <- Index of project milestones and status
├── DECISION_LOG.md           <- Architectural Decision Records (ADRs)
└── docs/                     <- Central documentation repository
    ├── architecture/         <- Architectural diagrams & specs
    ├── product/              <- PRD and product vision
    ├── milestones/           <- Milestone plans and verification reports
    ├── features/             <- Mandatory FEATURE_NAME.agent.md files
    ├── verification/         <- System verification logs
    ├── security/             <- Security audits & secret handling rules
    ├── decisions/            <- Change requests and ADR files
    └── templates/            <- Reusable milestone, agent, & verification templates
```
