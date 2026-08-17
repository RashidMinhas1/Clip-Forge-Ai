# MS-015 — Security Hardening & Audit

## Status
PLANNING ONLY

## Previous Milestone
MS-014 — Export & Gallery

## Objective
Introduce robust security mechanisms to transition the MVP into a production-ready application. This includes full authentication/authorization, tenant isolation, rate limiting, CORS tightening, security headers, secret management, file-access safeguards, and audit reporting.

## Product Context
As the application prepares to handle sensitive media files, AI provider API keys, and multi-user data, strict tenant isolation and security safeguards are required. MS-015 hardens the backend and frontend infrastructure to meet production security standards, ensuring user data is isolated, API keys are protected, and abuse is mitigated.

## Authoritative Evidence
- `MILESTONE_REGISTRY.md`: MS-015 = Security Hardening & Audit (Full authentication/authorization, tenant isolation, rate limiting, CORS, security headers, secret management, file‑access safeguards, audit reporting.)
- `PRD.md`: Section 23 specifies Server-Side Secret Isolation, Application-Level Tenant Boundary, Media File Security, and Automatic Storage Cleanup.

## Scope

### Included
- **Authentication/Authorization**: JWT-based authentication flow for API requests. Middleware to validate user identity.
- **Tenant Isolation**: Adding `user_id` tracking to Projects, Sources, Transcripts, Clips, and Exports. Updating all repository queries to filter by `user_id`.
- **Media File Security**: Moving file storage into `/storage/{user_id}/...` structures. Securing download and playback routes with authentication checks.
- **Storage Cleanup**: Background job (Taskiq) to purge temporary files and processing chunks 6 hours after completion.
- **Rate Limiting**: Implementing API rate limiting (e.g., using Redis) for critical endpoints.
- **Security Headers & CORS**: Strict CORS configurations, HTTP security headers (HSTS, Content-Security-Policy, X-Frame-Options) on the backend.
- **Audit Reporting**: Basic audit logging for sensitive actions (project creation, deletion, export initiation).

### Explicitly Excluded
- Complex OAuth2 providers (Google/GitHub login) are excluded from this core hardening phase unless strictly necessary.
- Advanced Role-Based Access Control (RBAC) with granular permissions.
- MS-016+ features.
- Modifying locked milestone functional logic (rendering pipelines, AI workflows) beyond injecting the `user_id` tenant boundary.

## User Flow
1. User authenticates (via login page).
2. User's requests automatically include an Authorization token (managed by the frontend).
3. Backend middleware intercepts the request, verifies the token, and attaches the `user_id` to the request context.
4. User accesses Projects, seeing *only* their own projects.
5. User initiates rendering; temporary files are stored in their tenant-specific directory.
6. A background task runs periodically to clean up temporary artifacts.

## Architecture

### Backend
- **Middleware**: Introduce `SecurityHeadersMiddleware`.
- **Dependencies**: Create a `get_current_user` FastAPI dependency.
- **Services/Repositories**: Update all repositories to accept and filter by `user_id`.
- **Storage**: Refactor `storage.py` (or equivalent file handling logic) to use `{user_id}` in paths.
- **Tasks**: Create a Taskiq cron job for artifact cleanup.

### Frontend
- **Auth Provider**: Introduce an `AuthContext` in React.
- **API Interceptors**: Update `apiClient` to inject the Authorization header.
- **Routing**: Add authentication guards/redirects for protected routes (e.g. `/projects`).

### Database
- **New Tables**: `users`, `audit_logs`.
- **Modifications**: Add `user_id` foreign key to `projects` table (cascading automatically to downstream entities like sources and clips via relationships).
- **Migrations**: Alembic migration for adding `user_id` and the `users` table.

### AI
- No changes to AI logic, other than ensuring provider keys remain strictly server-side.

### Infrastructure
- Redis is required for rate limiting.
- Taskiq scheduler required for cleanup jobs.

## File Change Matrix

| File | Change Type | Purpose | Scope |
|------|-------------|---------|-------|
| `backend/app/api/deps.py` | New | `get_current_user` dependency | Backend |
| `backend/app/core/security.py` | New | JWT validation, password hashing | Backend |
| `backend/app/middleware/security.py` | New | Security headers and rate limiting | Backend |
| `backend/app/models/user.py` | New | User and AuditLog SQLAlchemy models | Database |
| `backend/app/models/project.py` | Modify | Add `user_id` foreign key | Database |
| `backend/app/api/v1/auth.py` | New | Login/registration endpoints | Backend |
| `backend/app/api/v1/*.py` | Modify | Inject `Depends(get_current_user)` | Backend |
| `backend/app/repositories/*.py` | Modify | Filter by `user_id` | Backend |
| `backend/app/tasks/cleanup.py` | New | Scheduled task for temp file cleanup | Background Jobs |
| `frontend/src/contexts/AuthContext.tsx` | New | Authentication state management | Frontend |
| `frontend/src/lib/api-client.ts` | Modify | Attach bearer tokens | Frontend |
| `frontend/src/app/login/page.tsx` | New | User login interface | Frontend |

## API Design

- `POST /api/v1/auth/login`: Authenticate and return JWT token.
- `POST /api/v1/auth/register`: Register a new user.
- `GET /api/v1/auth/me`: Get current user info.
- All existing endpoints (e.g., `/api/v1/projects`) modified to require bearer token and apply `user_id` filtering.

## Database Design

- `users`: `id` (UUID), `email` (String), `hashed_password` (String), `created_at` (DateTime), `is_active` (Boolean).
- `projects`: Add `user_id` (UUID, nullable=False, indexed).
- `audit_logs`: `id` (UUID), `user_id` (UUID), `action` (String), `resource_type` (String), `resource_id` (String), `timestamp` (DateTime), `ip_address` (String).

## Background Jobs

- **Job**: `cleanup_stale_artifacts`
- **Trigger**: Cron schedule (e.g., every 1 hour).
- **Inputs**: None.
- **Outputs**: Logs of deleted files.
- **Failure behavior**: Log and retry on next schedule.

## Frontend UX

- **Routes**: `/login`, `/register`.
- **States**: Loading states during auth checks. Unauthenticated users redirected to `/login`.
- **Interactions**: Logout button in the main layout/navigation.

## Testing Strategy

### Backend Tests
- Test unauthorized access to protected routes (401).
- Test cross-tenant access attempts (403/404).
- Test JWT generation and validation.
- Test rate limiting thresholds.

### Frontend Tests
- Test protected route redirects.
- Test login form validation and submission.

### Integration Tests
- Verify end-to-end auth flow and project isolation.

### Regression Tests
- Ensure clip generation and rendering still work seamlessly with the new `user_id` context.

## Acceptance Criteria
1. Unauthenticated requests to `/api/v1/projects/*` and other protected endpoints return 401 Unauthorized.
2. A user cannot access or modify projects, clips, or exports belonging to another user.
3. Media files are stored in `storage/{user_id}/...` structures.
4. Repeated requests exceeding rate limits return 429 Too Many Requests.
5. `SecurityHeadersMiddleware` injects strict headers (e.g., HSTS, X-Content-Type-Options) into all responses.
6. A scheduled Taskiq job successfully identifies and deletes temporary files older than 6 hours.

## Non-Goals
- Modifying the AI clipping engine logic.
- Implementing complex, custom-role RBAC.

## Dependencies
- Security packages for Python (`passlib`, `python-jose` or `PyJWT`, `bcrypt`).

## Risks
- **Data Migration**: Existing projects in the database do not have a `user_id`. A default migration user strategy will be required to avoid breaking existing data.

## Environmental Constraints
- Redis MUST be available for rate limiting.
- PostgreSQL MUST be available to test tenant isolation.

## Governance
- MS-014 remains LOCKED.
- MS-001–MS-014 remain protected.
- No implementation started.
- No dependencies installed.
- No source files modified.

## Implementation Readiness
READY FOR USER APPROVAL
