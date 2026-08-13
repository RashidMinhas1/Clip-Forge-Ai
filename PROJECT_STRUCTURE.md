# ClipForge AI — Project Directory Structure & Blueprint

> **Status**: LOCKED (Foundation Phase)  
> **Pattern**: Monorepo-style Modular Directory Layout  

---

## Complete Blueprint Map

```
ClipForge-Ai/
├── .env.example                     # Environment variable blueprint with safe placeholders
├── .gitignore                        # Git exclusion rules (Node, Python, media temp, secrets)
├── GLOBAL_RULES.md                   # Universal engineering governance
├── DEVELOPMENT_WORKFLOW.md          # 17-stage lifecycle protocol
├── TECH_STACK.md                    # Technology stack matrix & evaluation
├── ARCHITECTURE.md                  # Modular monolith architecture design
├── SECURITY_RULES.md                # Security, secret handling & data isolation rules
├── PROJECT_MEMORY.md                # Compact context onboarding guide
├── PROJECT_STRUCTURE.md             # File tree layout spec (This file)
├── FEATURE_REGISTRY.md              # Registry of feature specs (.agent.md files)
├── MILESTONE_REGISTRY.md            # Registry of all milestones & statuses
├── DECISION_LOG.md                  # Architectural Decision Records (ADRs)
│
├── docs/                            # Comprehensive System Documentation
│   ├── architecture/                # Subsystem architecture diagrams
│   ├── product/                     # PRD & UX journey maps
│   ├── milestones/                  # Milestone plans and verification reports
│   ├── features/                    # Dedicated feature agent specifications (.agent.md)
│   ├── verification/                # Milestone verification audit logs
│   ├── security/                    # Security threat models & privacy policies
│   ├── decisions/                   # Change requests & decision logs
│   └── templates/                   # Reusable workflow templates
│       ├── FEATURE_NAME.agent.md    # Template for feature agent specifications
│       ├── milestone-X-plan.md      # Template for milestone implementation plans
│       ├── milestone-X-verification-report.md # Template for milestone verification reports
│       └── change-request-X.md      # Template for change request analyses
│
├── apps/                            # Application Workspace (Target Layout for Implementation)
│   ├── web/                         # Frontend Application (Next.js 19 + TypeScript + Tailwind + shadcn/ui)
│   │   ├── public/                  # Static web assets
│   │   └── src/
│   │       ├── app/                 # App Router pages and API routes
│   │       ├── components/          # UI Components (shadcn/ui primitives + custom)
│   │       ├── hooks/               # Custom React hooks
│   │       ├── lib/                 # Frontend utilities & API client
│   │       ├── stores/              # Client state management
│   │       └── types/               # TypeScript interfaces & DTO definitions
│   │
│   └── api/                         # Backend Application (FastAPI + Python 3.11+)
│       ├── app/
│       │   ├── api/                 # API Endpoint routes (v1 router)
│       │   ├── core/                # Core config, security, DB session, exception handlers
│       │   ├── db/                  # SQLAlchemy models, migrations (Alembic)
│       │   ├── services/            # Business service logic (User, Project, Storage)
│       │   ├── ai/                  # AI Router & Provider Adapters (OpenAI, Gemini, etc.)
│       │   ├── media/               # FFmpeg wrapper, audio extraction, visual framing
│       │   ├── jobs/                # Taskiq/Redis background worker tasks
│       │   └── schemas/             # Pydantic schemas for request validation & AI output
│       └── tests/                   # Backend test suite (Pytest)
│           ├── unit/
│           ├── integration/
│           └── api/
```
