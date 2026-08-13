# ClipForge AI — Development Workflow & Process Protocol

> **Status**: LOCKED (Foundation Phase)  
> **Audience**: Development Team, AI Assistants & Peer Engineers  

---

## 1. Governance & Dual-Layer Rules Overview

ClipForge AI strictly operates under two distinct rule layers:
1. **Development & Chat Workflow Rules**: Process guidelines governing planning, approval, git branching, verification, and code commits.
2. **Application Engineering Rules**: Technical governance for architecture, security, database models, AI abstractions, media pipelines, and error handling.

---

## 2. Standard Feature / Milestone Lifecycle

Every requirement goes through 17 explicit lifecycle stages:

```
[1. USER REQUIREMENT]
         ↓
[2. REQUIREMENT ANALYSIS] (Understand context & boundaries)
         ↓
[3. REQUIREMENT CLARIFICATION] (Ask explicit questions if ambiguous)
         ↓
[4. UPDATE PRODUCT REQUIREMENTS]
         ↓
[5. MILESTONE PLAN CREATION] (Save as /docs/milestones/milestone-XXX/milestone-XXX-plan.md)
         ↓
[6. FEATURE AGENT CREATION] (Save as /docs/features/FEATURE_NAME.agent.md)
         ↓
[7. USER REVIEW GATE] (Present plan & feature specs to user)
         ↓
[8. USER APPROVAL] (Explicit consent required to proceed)
         ↓
[9. GIT BRANCH CREATION] (git checkout -b milestone/XXX-feature-name)
         ↓
[10. BUILD / IMPLEMENTATION] (Write modular backend, frontend, & tests)
         ↓
[11. TESTING EXECUTION] (Run Unit, API, Integration, UI tests)
         ↓
[12. SYSTEM VERIFICATION] (Audit against functional, security, & UX rules)
         ↓
[13. DEFECT REMEDIATION & RE-TEST] (Fix bugs & re-verify)
         ↓
[14. VERIFICATION REPORT] (Save as milestone-XXX-verification-report.md)
         ↓
[15. USER FINAL REVIEW & APPROVAL]
         ↓
[16. COMMIT & GITHUB PUSH] (Push milestone branch)
         ↓
[17. MAIN BRANCH MERGE & LOCK] (Merge into main, lock milestone)
```

---

## 3. Mandatory Milestone Planning Gate

Implementation without an approved milestone plan is strictly forbidden. 
Every plan created in `/docs/milestones/milestone-XXX/milestone-XXX-plan.md` MUST contain:

1. **Objective**: Scope and value proposition.
2. **Existing Architecture**: Current baseline system state.
3. **Requirements**: Detailed functional & non-functional requirements.
4. **User Flow**: Step-by-step user journey.
5. **Technical Approach**: Backend, Frontend, Database, API, and AI architecture modifications.
6. **File Matrix**: Explicit list of files to [NEW], [MODIFY], or [DELETE].
7. **Security & Data Privacy Impact**: Secret handling, authorization, and isolation checks.
8. **UX & UI Impact**: Loading, empty, success, and error states.
9. **Testing Strategy**: Automated unit, integration, and manual test coverage.
10. **Verification Strategy**: Criteria for passing verification.
11. **Risks & Rollback Plan**: Pitfalls and step-by-step fallback execution.
12. **Acceptance Criteria & Definition of Done**: Concrete verification checklists.

---

## 4. Change Control Management Protocol

Once a milestone is marked **LOCKED**, no direct modifications to its code or spec are permitted without formal Change Control:

1. User requests modification to locked functionality.
2. Engineer generates a **Change Request Analysis** (`/docs/decisions/change-request-XXX.md`).
3. Impact is evaluated across: Existing behavior, Affected `.agent.md` specs, Database migrations, Security boundaries, Regression risks.
4. User reviews and approves the Change Request.
5. New implementation plan created → Executed → Verified → Locked.

---

## 5. Pre-Push Security & Git Checklist

Before pushing any commit to GitHub:
- [ ] `git status` clean of untracked credentials or temporary files.
- [ ] No API keys, database credentials, or secret strings present in code or docs.
- [ ] `.env` is omitted and `.gitignore` covers local media directories.
- [ ] Automated test suite runs with 100% pass rate.
- [ ] Verification report status is explicitly set to `PASS`.
