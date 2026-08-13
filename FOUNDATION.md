# ClipForge AI — Foundation Phase Master Specification

> **Status**: COMPLETED & VERIFIED (Foundation Phase Patch)  
> **Scope**: Baseline Architecture, Rules, Workflows, Templates, and Governance  
> **Product Features Built**: NONE (Strictly enforced)  

---

## 1. Executive Statement

The Foundation Phase establishes the complete engineering foundation, development governance, security policies, AI abstraction model, Git workflow, verification standards, and directory structure for **ClipForge AI**.

---

## 2. Established Governance & Architecture Core

1. **Dual Rule Layer**:
   - **Development Workflow Rules**: Milestone Execution Lifecycle enforcing `PLANNING → ANALYSIS → IMPLEMENTATION / REFACTOR PLAN → FEATURE AGENT DOCUMENTATION → USER REVIEW / APPROVAL → MILESTONE BRANCH → IMPLEMENTATION → TESTING → VERIFICATION → FIXES IF REQUIRED → RE-VERIFICATION → VERIFICATION REPORT → USER APPROVAL → GITHUB PUSH → MERGE / PULL → MILESTONE LOCKED`.
   - **Application Engineering Rules**: Permanent rules for modular monolith architecture, application-level tenant isolation (`WHERE user_id = authenticated_user.id`), Taskiq + Redis background job queueing, schema-validated AI output, and secret protection.

2. **Planning & Feature Spec Enforcers**:
   - No code implementation occurs without an approved milestone plan (`/docs/milestones/milestone-XXX/milestone-XXX-plan.md`).
   - Every major technical feature is governed by a dedicated spec file (`/docs/features/FEATURE_NAME.agent.md`).

3. **No Mock Fallbacks Policy**:
   - Production flows must NEVER return static mock results or silently mask backend/AI errors with hardcoded data.

4. **Multi-Provider AI Abstraction**:
   - Agnostic AI Router isolating prompt engineering, model selection, token usage tracking, and Pydantic schema validation.

5. **Technology Stack**:
   - **Frontend**: Next.js (React 19+, TypeScript), Tailwind CSS, shadcn/ui.
   - **Backend**: Python (FastAPI), SQLAlchemy 2.0 (Async), Alembic.
   - **Database**: PostgreSQL.
   - **Background Processing**: Redis + Taskiq worker.
   - **Media Engine**: FFmpeg (CLI & Python wrapper).
   - **Storage**: StorageDriver abstraction (MinIO local / S3 production).

---

## 3. Foundation Deliverables Checklist Verification

- [x] Correct milestone execution lifecycle terminology enforced (no fake fixed 17-milestones claim).
- [x] Taskiq + Redis background job queue finalized.
- [x] Application-level tenant isolation security terminology corrected.
- [x] PostgreSQL RLS documented as optional future defense-in-depth layer.
- [x] `GLOBAL_RULES.md` created & locked.
- [x] `DEVELOPMENT_WORKFLOW.md` created & locked.
- [x] `TECH_STACK.md` created & locked.
- [x] `ARCHITECTURE.md` created & locked.
- [x] `SECURITY_RULES.md` created & locked.
- [x] `PROJECT_MEMORY.md` created & locked.
- [x] `PROJECT_STRUCTURE.md` created & locked.
- [x] `DECISION_LOG.md` created & locked (ADR-001 through ADR-008).
- [x] `FEATURE_REGISTRY.md` created & locked.
- [x] `MILESTONE_REGISTRY.md` created & locked.
- [x] `.env.example` created with safe placeholders.
- [x] Documentation directory tree `/docs/` established.
- [x] Reusable workflow templates created in `/docs/templates/`:
  - `FEATURE_NAME.agent.md`
  - `milestone-X-plan.md`
  - `milestone-X-verification-report.md`
  - `change-request-X.md`
- [x] Zero product features implemented during foundation phase.
