# ClipForge AI — Global Engineering & Development Rules

> **Status**: LOCKED (Foundation Phase)  
> **Scope**: Master Application & Development Governance  
> **Version**: 1.0.0  

---

## 1. Development & Chat Workflow Rules

### 1.1 Strict Gatekeeping Cycle
Every interaction and feature engineering task must strictly follow this sequential cycle:

```
USER REQUIREMENT
      ↓
UNDERSTAND REQUIREMENT
      ↓
ANALYZE REQUIREMENT
      ↓
ASK QUESTIONS IF NECESSARY
      ↓
UPDATE PRODUCT REQUIREMENTS
      ↓
PLAN
      ↓
CREATE IMPLEMENTATION / REFACTOR PLAN
      ↓
CREATE / UPDATE FEATURE AGENT FILE (.agent.md)
      ↓
USER REVIEW & APPROVAL
      ↓
CREATE MILESTONE BRANCH
      ↓
BUILD / IMPLEMENT
      ↓
TEST & VERIFY
      ↓
FIX ISSUES & RE-VERIFY
      ↓
VERIFICATION REPORT (milestone-X-verification-report.md)
      ↓
USER REVIEW & APPROVAL
      ↓
COMMIT & PUSH TO GITHUB
      ↓
MERGE / PULL INTO MAIN DEVELOPMENT LINE
      ↓
MILESTONE LOCKED
```

### 1.2 Development Execution Directives
- **Planning First**: Analysis, implementation plans, and `.agent.md` files MUST be created and approved *before* writing code.
- **Verification Mandatory**: A milestone is NOT complete merely because code exists. A milestone is complete ONLY after passing all functional, security, performance, media, and UI tests recorded in a formal Verification Report.
- **Sequential Approval**: Never start implementation on a milestone without explicit user approval of the implementation plan and feature agent files.

---

## 2. Application Engineering Rules

### 2.1 Core Architectural Principles
- **Modular Monolith**: Maintain a cohesive modular monolith structure. Microservices are strictly forbidden unless explicit throughput metrics require isolation.
- **Layered Separation**: Enforce clear boundaries:
  `Frontend → API Layer → Service / Application Layer → Domain Logic → Infrastructure (DB, AI Router, Media Engine, Queue, Storage)`.
- **Stateless API & Async Background Jobs**: HTTP requests must NEVER block on long-running media ingestion, transcription, AI clip extraction, or FFmpeg rendering tasks. All long-running operations MUST be offloaded to Redis + Python background workers with state machines (`QUEUED`, `PROCESSING`, `PROGRESS`, `COMPLETED`, `FAILED`).

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

### 2.4 User Isolation & Data Privacy
- Every database query touching user entities MUST enforce ownership checks (`where user_id = current_user.id`).
- Temporary processing files (video chunks, raw transcripts, FFmpeg intermediate frames) must be stored in isolated directories and purged automatically upon job completion or failure.
- File download/stream endpoints must validate authentication and authorization headers before serving media streams.

### 2.5 Security & Secret Safety
- Hardcoding secrets, API keys, credentials, or private tokens in code, comments, or UI bundles is strictly prohibited.
- All secrets must be loaded via environment variables validated on server startup (`pydantic-settings`).
- Pre-commit checks must ensure `.env` and sensitive media files are never committed or pushed to GitHub.

---

## 3. Git & Branching Strategy

- **Main Branch Protection**: Direct commits or pushes to `main` are strictly forbidden.
- **Milestone Branching Pattern**: All work happens in isolated feature/milestone branches using the naming convention `milestone/XXX-name` (e.g., `milestone/001-foundation`).
- **Merge Criteria**: Merges to `main` require a clean verification report (`PASS` status) and explicit user approval.
