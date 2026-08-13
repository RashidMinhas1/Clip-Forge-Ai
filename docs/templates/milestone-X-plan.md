# Milestone Implementation Plan: [MILESTONE_NAME]

> **Milestone ID**: MS-XXX  
> **Target Branch**: `milestone/XXX-name`  
> **Document Location**: `/docs/milestones/milestone-XXX/milestone-XXX-plan.md`  
> **Status**: PROPOSED / APPROVED / LOCKED  

---

## 1. Objective
[Brief description of the problem, value proposition, and expected deliverables.]

## 2. Existing Architecture & Baseline State
[Current codebase architecture and state prior to implementing this milestone.]

## 3. Requirements
- **Functional Requirements**: [Detailed list]
- **Non-Functional Requirements**: [Performance, latency, security]

## 4. User Flow
[Step-by-step end-to-end user interaction sequence.]

## 5. Technical Approach & Subsystem Impact

### 5.1 Backend Changes (FastAPI)
[API routes, controllers, services, async worker queues.]

### 5.2 Frontend Changes (Next.js + Tailwind + shadcn/ui)
[UI pages, state management, components, interactive hooks.]

### 5.3 Database Changes (PostgreSQL + SQLAlchemy + Alembic)
[Tables, columns, indexes, foreign key constraints, migration scripts.]

### 5.4 AI Router & Prompt Changes
[LLM prompt templates, provider adapters, schema validation.]

### 5.5 File & Media Processing (FFmpeg / Storage)
[FFmpeg filter graphs, temporary directories, S3/local storage driver actions.]

## 6. File Matrix

#### [NEW] [`path/to/newfile.py`](file:///path/to/newfile.py)
- Description of purpose.

#### [MODIFY] [`path/to/existingfile.ts`](file:///path/to/existingfile.ts)
- Summary of modifications.

#### [DELETE] [`path/to/obsolete.py`](file:///path/to/obsolete.py)
- Reason for removal.

## 7. Security & Data Privacy Impact
- User ownership check (`WHERE user_id = current_user.id`) enforced on all queries.
- Secret protection audit verified.
- File path sanitization checks.

## 8. UX & UI Impact
- Loading states (skeletons / progress bars).
- Empty states & error toasts.
- Responsive layout verification.

## 9. Dependencies & Migration Requirements
- New Python packages / npm modules.
- Database migration script execution (`alembic upgrade head`).

## 10. Testing Strategy
- **Unit Tests**: Pytest / Jest unit test suites.
- **Integration Tests**: API route & DB transaction tests.
- **UI Tests**: Component rendering & user interaction flow.

## 11. Verification Strategy & Acceptance Criteria
- List of functional, media, security, and UI checks to perform for verification report.

## 12. Risks & Rollback Strategy
- Identified technical risks.
- Step-by-step git & database rollback commands.

## 13. Definition of Done
- [ ] Code implemented on `milestone/XXX-name` branch.
- [ ] Automated tests pass (100%).
- [ ] Verification report generated and marked `PASS`.
- [ ] User review and explicit authorization received.
