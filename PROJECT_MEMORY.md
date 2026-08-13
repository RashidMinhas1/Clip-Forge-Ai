# ClipForge AI — Project Memory & Orientation

> **Status**: ACTIVE (Updated Foundation Phase)  
> **Purpose**: High-density context document for rapid onboarding of AI agents and human developers.

---

## 1. Executive Summary

ClipForge AI is an advanced AI-powered short-form video clip generation platform. It automatically processes long-form videos (uploaded locally or ingested via YouTube), performs speech-to-text transcription, executes multi-dimensional AI vitality scoring to identify compelling short clips, and provides a lightweight editor for visual framing, dynamic dynamic caption styling, and automated FFmpeg video rendering.

---

## 2. Current Project State

- **Current Lifecycle Stage**: `FOUNDATION PHASE` (Complete engineering governance established).
- **Product Features State**: `0% Implemented` (Product features strictly barred during foundation phase).
- **Git Branch**: `milestone/001-foundation`
- **Next Required Stage**: `PRD GATE` (Waiting for explicit user review & authorization).

---

## 3. Core Architectural Decisions

1. **Tech Stack**: Next.js (TypeScript + Tailwind CSS + shadcn/ui) + FastAPI (Python 3.11+) + PostgreSQL (SQLAlchemy Async) + Redis (Taskiq worker queue) + FFmpeg.
2. **Rule Layers**: Enforces Dual Rule System (Development/Chat Workflow Rules vs Application Engineering Rules).
3. **Feature Agent Rule**: Every major capability requires a dedicated `docs/features/FEATURE_NAME.agent.md` file governing behavioral logic, validation rules, AI output schemas, and forbidden behavior.
4. **Planning Enforcer**: No code execution without an approved `/docs/milestones/milestone-XXX/milestone-XXX-plan.md`.
5. **No Mock Fallbacks**: Production code must NEVER return static fake AI outputs or hide API failures.

---

## 4. Key Directory Sitemap

```
/
├── GLOBAL_RULES.md            <- Universal engineering & workflow rules
├── DEVELOPMENT_WORKFLOW.md   <- 17-stage development lifecycle protocol
├── TECH_STACK.md             <- Full stack evaluation and driver matrix
├── ARCHITECTURE.md           <- High-level modular monolith diagram
├── SECURITY_RULES.md         <- Secrets, user isolation & input protection
├── PROJECT_STRUCTURE.md      <- Full directory layout map
├── FEATURE_REGISTRY.md       <- Index of all feature agent specs
├── MILESTONE_REGISTRY.md     <- Index of project milestones and status
├── DECISION_LOG.md           <- Architecture Decision Records (ADRs)
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
