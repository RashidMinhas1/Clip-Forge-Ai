# Milestone Implementation Plan: Application Runtime & Infrastructure

> **Milestone ID**: MS-002  
> **Target Branch**: `milestone/002-application-runtime-infrastructure` (Not yet created)  
> **Document Location**: `/docs/milestones/milestone-002/milestone-002-plan.md`  
> **Status**: APPROVED  

---

## 1. Objective
Establish the foundational application runtime for ClipForge AI, enabling Next.js (frontend) and FastAPI (backend) to operate locally via Docker Compose. Establish the UI shell, API communication protocols, safe retry policies, structured logging, configuration management, and cross-cutting testing and CI scaffolding.

## 2. Scope
### IN SCOPE:
- Next.js (React, TypeScript) initialization (using the current stable compatible version verified at implementation time).
- shadcn/ui & Tailwind CSS foundation (design tokens, global styles, layout shell, accessibility baseline).
- API client wrapper using native `fetch` with standardized error, timeout handling, and safe retry policy.
- Dynamic API configuration abstraction (no hard-coded environment URLs).
- FastAPI (Python) initialization with Pydantic configuration.
- Structured logging, global exception handling, CORS setup.
- Health endpoints (`/api/v1/health` for liveness, `/api/v1/ready` for dependency readiness if required).
- Docker Compose setup integrating frontend, backend, Redis (infrastructure only), and PostgreSQL (runtime container only).
- Basic test setup (Pytest for backend, Jest/Vitest for frontend).
- Basic CI engineering quality validation.
- Secret management and security foundation.

### OUT OF SCOPE (Strictly Forbidden):
- Product logic (upload, processing, rendering).
- Product Database schema, models, or Alembic migrations (Deferred to MS-003).
- Fake authentication (No fake login, no fake users, no fake sessions).
- AI provider integration.
- Taskiq workers or job state machines.

## 3. Existing Architecture & Baseline State
- **Current**: Repository contains only documentation (`docs/`, `FOUNDATION.md`, etc.). `frontend/` and `backend/` directories do not exist.
- **Foundation**: `ARCHITECTURE.md` mandates a Modular Monolith. The MS-002 implementation must adhere to these structural constraints.

## 4. Technical Implementation Plan

### 4.1. Project Structure
The repository will be extended to include:
```text
/frontend
  /src
    /app           (Next.js App Router)
    /components    (shadcn/ui base components, layouts)
    /lib           (API client, utils, config)
    /types
/backend
  /app
    /api           (Routers)
    /core          (Config, logging, exceptions)
    /main.py       (FastAPI entry point)
/infrastructure
  docker-compose.yml
/.env.example
.gitignore
```

### 4.2. Frontend Plan (Next.js + UI Foundation)
- Bootstrap Next.js App Router using the current stable version.
- Configure Tailwind CSS.
- Initialize `shadcn/ui` with neutral/dark mode tokens.
- Create a root `layout.tsx` (Application Shell).
- Implement reusable UI components: `Button`, `Card`, `Toast`, `LoadingSpinner`.
- **Accessibility Baseline**: Semantic HTML, keyboard navigation, visible focus states, form labels, accessible buttons, appropriate ARIA, and contrast.
- **API Architecture**: Create configuration abstractions to resolve browser/public API base URLs and internal server-side URLs dynamically without hard-coding environments. No secrets in `NEXT_PUBLIC_*` variables.
- **HTTP Client**: Use native `fetch`. Implement timeout handling, typed errors, response validation, and error normalization.
- **Health UI**: Create a DEVELOPER/INFRASTRUCTURE VERIFICATION UI only to verify frontend -> API client -> FastAPI communication.

### 4.3. Backend Plan (FastAPI)
- Bootstrap FastAPI application.
- `core/config.py`: Use `pydantic-settings` to parse environment variables.
- `core/logging.py`: Configure structured JSON logging.
- `main.py`: Attach CORS middleware, global exception handler.
- **Health & Readiness**: Implement `/api/v1/health` (Liveness) and optionally `/api/v1/ready` (Readiness).

### 4.4. Infrastructure Plan (Docker & Env)
- Create `Dockerfile` for frontend.
- Create `Dockerfile` for backend.
- Create `docker-compose.yml` to orchestrate `frontend`, `backend`, `redis`, and `postgres`.
- Redis is strictly for infrastructure readiness only.
- PostgreSQL is strictly a runtime container only — no product database implementation or schemas.

### 4.5. Testing & CI Plan
- **Backend**: Pytest framework, `test_health.py`, `test_config.py`.
- **Frontend**: Vitest/Jest framework, simple render tests.
- **CI Validation**: Create a basic CI pipeline to verify dependency installation, tests, linting, type checks, and frontend build. No production deployment CI/CD yet.

### 4.6. Security Plan
- Environment variable separation.
- Strict `.gitignore` to prevent tracking `.env`, API credentials, private keys, etc.
- Only `.env.example` with placeholders is committed.
- Secret scanning/audit enabled.
- No secrets in logs, frontend bundles, or error responses.
- Strict CORS configuration.
- Authentication architecture preparation (placeholders only).

### 4.7. Observability Plan
- Structured JSON logging on backend (Timestamp, Level, Message, RequestID).

## 5. File Matrix (Proposed)

#### [NEW] `backend/app/main.py`
- FastAPI application initialization, CORS, router mounting.
#### [NEW] `backend/app/core/config.py`
- Pydantic Settings class for validation.
#### [NEW] `backend/app/api/v1/health.py`
- Liveness and readiness routers.
#### [NEW] `frontend/src/app/layout.tsx`
- Root layout, font configuration, global providers.
#### [NEW] `frontend/src/app/page.tsx`
- Infrastructure verification page.
#### [NEW] `frontend/src/lib/api-client.ts`
- Native `fetch` wrapper with safe retry policy and timeout handling.
#### [NEW] `docker-compose.yml`
- Local development orchestration.
#### [NEW] `.github/workflows/ci.yml` (or similar CI config)
- Basic engineering quality validation.

## 6. Example User / System Behavior
**Scenario: System Startup & Liveness Verification**
1. **Developer**: Runs `docker-compose up`.
2. **System**: Starts Redis, PostgreSQL, Backend (port 8000), and Frontend (port 3000).
3. **Developer**: Opens `http://localhost:3000` in browser.
4. **Frontend**: Loads the application shell with accessibility defaults.
5. **Frontend API Client**: Resolves backend URL via safe configuration and fetches `/api/v1/health`.
6. **Backend**: Receives request, logs it securely, and returns `{"status": "alive"}`.
7. **Frontend**: Displays "Backend Status: Online" in the developer verification UI.

## 7. Database Boundary
- PostgreSQL container is included for infrastructure runtime readiness only.
- No product database implementation, no user/project models, no Alembic migrations.

## 8. Background-Job Boundary
- Redis container is included for infrastructure runtime readiness only.
- No Taskiq workers, no video processing jobs.

## 9. Dependency Analysis
**Inputs from MS-001**: Architecture guidelines, Stack choice, Global rules.
**MS-002 Outputs**: Running scaffolding, API client, Docker compose, test frameworks, CI.
**Dependencies for MS-003**: MS-003 needs this FastAPI app to attach SQLAlchemy, and this Next.js app to build persistence workflows.

## 10. Risk Analysis

| Risk | Impact | Probability | Mitigation | Verification |
| :--- | :--- | :--- | :--- | :--- |
| Docker networking issues between Next.js server-side and FastAPI | High | Medium | Use dynamic API config abstractions (internal vs external routing). | Execute E2E fetch during startup. |
| Secrets leaking to frontend/logs | Critical | Low | Strict config management, no `NEXT_PUBLIC_` secrets, structured logging filters. | CI secret scanning, code review. |
| Unsafe retries causing duplicates | High | Low | Implement explicit safe retry policy in the API client (GET/HEAD only). | Unit tests for API client behavior. |

## 11. Rollback Strategy
- Discard the `milestone/002-application-runtime-infrastructure` branch.
- Remove any created directories.

## 12. Acceptance Criteria
- [ ] API environment configuration is not hard-coded.
- [ ] Browser/public API URL and internal API URL are correctly separated where required.
- [ ] Safe retry policy is implemented/documented.
- [ ] No unsafe automatic mutation retries.
- [ ] Liveness and readiness semantics are correct.
- [ ] No fake authentication exists.
- [ ] No product database schema exists.
- [ ] Redis is infrastructure-only.
- [ ] CI validation is defined.
- [ ] Accessibility baseline is defined.
- [ ] Secret scanning/audit is performed.
- [ ] No sensitive environment files are tracked.
- [ ] Runtime health UI is explicitly infrastructure verification only.

## 13. Final Implementation Checklist (Post-Approval)
- [ ] Create branch `milestone/002-application-runtime-infrastructure`.
- [ ] Initialize Next.js, Tailwind, `components.json` (shadcn) with accessibility baseline.
- [ ] Initialize Python environment, basic FastAPI app, structured logging.
- [ ] Write API client (`fetch`) with safe retry policy and config abstractions.
- [ ] Write Dockerfiles and `docker-compose.yml`.
- [ ] Set up Pytest and Vitest/Jest.
- [ ] Configure CI workflow.
- [ ] Document verification report.
