---
id: project-persistence
name: Project Persistence & Database Schema
status: PROPOSED
description: "Handles the persistent storage of user workspaces (Projects) and their ingested media assets (Sources) using PostgreSQL and SQLAlchemy."
---

# Feature Agent: Project Persistence

## 1. Purpose
To introduce a secure, scalable, and transactional persistent data layer for Clip Forge AI, enabling the system to remember user sessions, group media assets, and transition PostgreSQL from infrastructure to the primary product database.

## 2. User Value
Users can create multiple distinct projects, upload multiple video sources to a specific project, and safely return to their workspace later without losing their progress or ingestion data.

## 3. Scope
- PostgreSQL database integration via asyncpg.
- SQLAlchemy 2.0 ORM modeling.
- Alembic schema migrations.
- `Project` and `Source` entity design and implementation.
- API endpoints for Project CRUD operations.
- Integration with the existing MS-003 Source Ingestion workflow to persist metadata.

## 4. Architecture
- **Data Layer:** PostgreSQL -> `asyncpg` -> SQLAlchemy -> Alembic
- **Pattern:** Repository Pattern
- **Models:** `Project` (1) ---> (N) `Source`

## 5. Inputs
- HTTP Requests creating, retrieving, or deleting Projects.
- `SourceMetadata` objects produced by the MS-003 Ingestion Service.

## 6. Outputs
- Persistent Database Rows (`projects` table, `sources` table).
- HTTP Responses representing Project JSON schemas.

## 7. Database Boundaries
- All database interactions are scoped to the backend (FastAPI).
- The frontend never connects directly to the database.
- SQLAlchemy parameterized queries are strictly enforced.

## 8. API Boundaries
- `POST /api/v1/projects`
- `GET /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `DELETE /api/v1/projects/{project_id}`

## 9. Security Boundaries
- Secrets (Database connection strings) are loaded strictly via `.env` / environment variables.
- Raw stack traces from database exceptions (e.g. `sqlalchemy.exc.IntegrityError`) must be caught and sanitized before returning to the client.
- Primary keys are UUIDs to prevent enumeration.

## 10. Testing Requirements
- **Migration Tests:** Ensure Alembic `upgrade head` succeeds on an empty database.
- **Repository Tests:** Verify CRUD operations using a test database.
- **Integration Tests:** End-to-end FastAPI endpoint tests for Project creation and deletion.
- **Regression Tests:** MS-003 ingestion tests must continue to pass, now verifying that a `Source` row is created.

## 11. Dependencies
- MS-002: Infrastructure (PostgreSQL container)
- MS-003: Source Ingestion (The `SourceMetadata` payload)

## 12. Non-Goals
- Background processing queues (e.g. Taskiq).
- User authentication or multi-tenant authorization (Supabase Auth).
- Video rendering or AI provider integration.

## 13. Acceptance Criteria
1. PostgreSQL is successfully queried by FastAPI endpoints.
2. Alembic migrations manage the `projects` and `sources` tables.
3. The frontend can create and list Projects via API.
4. Uploading or ingesting a YouTube URL successfully persists the generated `SourceMetadata` to the `sources` table, associated with the correct `project_id`.

## 14. Failure Handling
- **Database Unavailable:** Endpoints safely return HTTP 500 without crashing the main application server.
- **Ingestion Failure:** If FFprobe validation fails during ingestion, a `Source` row is still persisted with an `invalid` status and the respective error message for user visibility.

## 15. Integration with MS-003
The existing MS-003 `IngestionService` logic will remain structurally intact but will be extended to receive a `project_id`. Upon successful (or unsuccessful) metadata extraction, the resulting `SourceMetadata` object will be passed to a `SourceRepository` to persist the data to PostgreSQL before returning the HTTP response.
