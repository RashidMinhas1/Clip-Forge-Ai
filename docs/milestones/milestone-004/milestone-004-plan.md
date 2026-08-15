# MS-004 Database Schema & Persistence

**Status**: AWAITING APPROVAL

## 1. Purpose
The purpose of MS-004 is to introduce the persistent data layer required to store and retrieve Clip Forge AI projects and their associated source metadata. This milestone officially transitions the PostgreSQL database (provisioned in MS-002) from an infrastructure component into the active product persistence database.

## 2. Current Project State
- **MS-001 Foundation**: LOCKED
- **MS-002 Runtime & Infrastructure**: LOCKED
- **MS-003 Source Ingestion**: LOCKED
- **MS-004 Database Persistence**: PLANNING ONLY

## 3. Problem Being Solved
Currently, MS-003 ingests local and YouTube sources and returns an in-memory `SourceMetadata` object to the client, but the application lacks a database to remember sessions, store projects, or associate multiple ingested sources into a cohesive workspace. We need a secure, scalable persistence layer.

## 4. Goals
- Define and implement PostgreSQL database connection, pooling, and configuration within FastAPI.
- Establish the data-access layer using SQLAlchemy (Async).
- Implement database migrations using Alembic.
- Design and persist the `Project` and `Source` entities.
- Integrate persistence safely with the existing MS-003 ingestion workflow.
- Ensure all DB credentials rely strictly on environment variables.

## 5. Non-goals (Out of Scope)
- Authentication / Login / User management
- AI Providers / OpenAI / OpenRouter / Gemini / Ollama
- Transcription
- AI clip discovery / Clip scoring
- Timeline editor / Captions / Rendering / Export / Social publishing
- Taskiq / Celery / Background workers / Redis job processing
- Advanced dashboard / Billing / Payments

## 6. Architecture
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (asyncio with `asyncpg`)
- **Migrations**: Alembic
- **Pattern**: Repository pattern abstracting database access from the Service layer.
- **Layers**:
  - `routers` -> `services` -> `repositories` -> `models`

## 7. Database Architecture
- Using an asynchronous connection pool managed by SQLAlchemy (`create_async_engine`).
- Dependency injection (`get_db`) yields database sessions for FastAPI endpoints.
- Transaction handling boundaries placed in the Service layer or via context managers.

## 8. Entity Model Proposal

### Project
Represents a user's workspace/session.
- `id`: UUID (Primary Key)
- `name`: String (Project title)
- `status`: String (active, archived)
- `created_at`: DateTime (UTC)
- `updated_at`: DateTime (UTC)

### Source
Represents an ingested media asset.
- `id`: UUID (Primary Key)
- `project_id`: UUID (Foreign Key -> Project.id)
- `source_type`: String (local, youtube)
- `original_url`: String (nullable)
- `normalized_url`: String (nullable)
- `provider`: String (nullable)
- `provider_video_id`: String (nullable)
- `title`: String (nullable)
- `duration`: Float (nullable)
- `width`: Integer (nullable)
- `height`: Integer (nullable)
- `fps`: Float (nullable)
- `video_codec`: String (nullable)
- `audio_codec`: String (nullable)
- `has_audio`: Boolean
- `container`: String (nullable)
- `file_size`: BigInteger (nullable)
- `local_storage_reference`: String (nullable)
- `ingestion_status`: String
- `validation_status`: String
- `created_at`: DateTime (UTC)
- `error_code`: String (nullable)
- `error_message`: String (nullable)

## 9. Relationship Model
```
[Project] 1 <-----> N [Source]
```
A project can contain multiple sources. Deleting a project cascades to delete its associated sources.

## 10. Field Definitions
- **UUIDs** are used for all Primary Keys to prevent enumeration and prepare for decentralized generation.
- **Timestamps** are always UTC timezones.
- **Status fields** utilize strict string enums matching the Pydantic models.

## 11. Constraints
- Foreign Key: `Source.project_id` references `Project.id` with `ON DELETE CASCADE`.
- Nullability matches exactly what `SourceMetadata` from MS-003 can optionally provide.

## 12. Index Strategy
- Primary Keys (`id`) are implicitly indexed.
- Foreign Keys (`project_id`) are indexed for efficient joins and deletions.

## 13. Migration Strategy
- Alembic will generate deterministic Python migration scripts.
- Migrations will be reviewable, reversible (`upgrade()` / `downgrade()`), and environment-safe.
- A single initial migration `create_project_and_source_tables` will be introduced.

## 14. Repository / Data-Access Architecture
- `ProjectRepository`: handles CRUD for `Project` (create, get_by_id, list, delete).
- `SourceRepository`: handles CRUD for `Source` (create, get_by_project, delete).

## 15. Service Layer Architecture
- `ProjectService`: Coordinates project creation and deletion.
- `IngestionService` (Existing from MS-003): Will be updated to accept a `project_id`, perform the current ingestion workflow, and finally persist the `SourceMetadata` result via `SourceRepository`.

## 16. API Contract Proposal
- `POST /api/v1/projects` - Create a new project workspace.
- `GET /api/v1/projects` - List available projects.
- `GET /api/v1/projects/{project_id}` - Retrieve a specific project and its sources.
- `DELETE /api/v1/projects/{project_id}` - Delete a project.
- *Updated* MS-003 endpoints to optionally accept `project_id`.

## 17. MS-003 Integration Strategy
Existing Flow: Ingestion -> Validation -> Media Metadata Extraction -> Return JSON.
New Flow: Ingestion -> Validation -> Media Metadata Extraction -> **Persist to Database** -> Return JSON.
If ingestion fails (e.g., corrupted media), a Source record is still created with an `error` ingestion_status for debugging/user visibility.

## 18. Frontend Impact
- Introduce a minimal Project Dashboard to test creating and loading projects.
- Pass `project_id` when uploading/ingesting new sources.
- *No complex timeline editors or dashboards yet.*

## 19. Configuration / Environment Variables
- `DATABASE_URL`: Injected securely via `.env`. E.g., `postgresql+asyncpg://clipforge:password@db:5432/clipforge`
- SQLAlchemy connects solely based on this URL.

## 20. Security Requirements
- NO secrets or credentials committed to git.
- Parameterized queries enforced by SQLAlchemy (no raw string formatting).
- UUIDs hide project creation rates and identity.
- Database runs locally behind a secure network boundary (Docker bridge or local loopback).

## 21. Error Handling
- Database connection errors are caught safely and translated to generic `500 Internal Server Error` to avoid leaking table/schema names.
- Invalid UUID queries result in safe `404 Not Found`.
- Integrity errors result in safe `400 Bad Request`.

## 22. Testing Strategy
- **Unit Tests**: Test repository logic with mocked SQLAlchemy sessions.
- **Integration Tests**: In-memory SQLite or temporary Postgres instance for Alembic migration testing and endpoint CRUD.
- **API Tests**: Validate HTTP responses and schemas.

## 23. Regression Strategy
- Rerun existing MS-002 Health & Readiness checks (update Readiness to check DB ping).
- Rerun existing MS-003 local and YouTube ingestion tests.

## 24. Acceptance Criteria
- Database connection succeeds via FastAPI.
- Alembic migrations apply cleanly from an empty database.
- Projects can be created, retrieved, and deleted via API.
- MS-003 ingested sources are successfully persisted into the `Source` table.

## 25. Verification Strategy
- A new automated test suite `tests/test_projects.py` and `tests/test_database.py`.
- Final manual run of the CLI `npm run dev` and creating a project in the UI.

## 26. Rollback Strategy
- Alembic `downgrade` command allows reversing the schema.
- Revert the Git commit to restore memory-only MS-003 ingestion.

## 27. Risks
- Asynchronous database drivers (`asyncpg`) can be tricky to configure for tests (e.g. nested event loops). Mitigation: use proper `pytest-asyncio` fixtures.

## 28. Dependencies
- MS-001, MS-002, MS-003 (All Completed and Locked).
- `asyncpg`, `sqlalchemy`, `alembic` (To be installed during implementation).

## 29. Implementation Sequence
1. Install requirements (`asyncpg`, `sqlalchemy`, `alembic`).
2. Configure Database core module and session maker.
3. Define SQLAlchemy declarative base and models (`Project`, `Source`).
4. Initialize Alembic and generate initial migration.
5. Create Repositories.
6. Create Services and update MS-003 ingestion logic.
7. Implement API Endpoints.
8. Add Backend Tests.
9. Implement minimal Frontend UI for Project creation.
10. Final Audit and Verification.

## 30. Explicit Out-of-Scope List
- Any Authentication
- Any Supabase integration (strictly standard Postgres + SQLAlchemy)
- Taskiq Background Jobs
- Transcriptions or AI Providers
