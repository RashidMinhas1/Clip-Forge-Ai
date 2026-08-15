# Supabase Implementation Plan

## Goal Description

Integrate Supabase into Clip Forge AI as the cloud persistence and authentication layer while preserving the existing application architecture, modular monolith design, and local processing workflow (FFmpeg, Taskiq, Redis). Since the project has completed its foundation (MS-001, MS-002) and MS-003 (Database & Persistence) has not yet been implemented, this plan replaces the raw PostgreSQL/SQLAlchemy architecture with a Supabase-backed architecture.

## Target Architecture

The application will replace the originally planned raw PostgreSQL + SQLAlchemy stack with Supabase. Supabase will act as the Backend-as-a-Service for Auth, Database, Storage, and Realtime.

## User Review Required

> [!IMPORTANT]
> The original MS-003 plan called for `SQLAlchemy 2.0 (Async) + Alembic` with raw PostgreSQL. By adopting Supabase, we are shifting to a BaaS model. We will use the Supabase JS client on the frontend and the Supabase Python client on the backend (FastAPI), replacing the need for Alembic and SQLAlchemy.
> Please confirm if this is acceptable, or if you still want SQLAlchemy to interface with the Supabase PostgreSQL database.

## Open Questions

> [!WARNING]
> 1. Should we use the Supabase Python client for all backend DB interactions, or keep SQLAlchemy for ORM modeling and point it at the Supabase Postgres connection string?
> 2. For Authentication, do we want to use Next.js App Router Server Actions for Supabase Auth, or strictly use the FastAPI backend as a proxy for all Auth operations?

## Proposed Changes

### Configuration & Infrastructure

#### [MODIFY] [.env.example](file:///d:/Clip-Forge-Ai/.env.example)
Add Supabase environment variables: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.

#### [MODIFY] [backend/app/core/config.py](file:///d:/Clip-Forge-Ai/backend/app/core/config.py)
Add validation for Supabase environment variables using Pydantic settings.

### Database & Security

#### [NEW] [supabase/migrations/0001_initial_schema.sql](file:///d:/Clip-Forge-Ai/supabase/migrations/0001_initial_schema.sql)
Define minimum required Supabase schema (profiles, projects, project_sources, clips, render_jobs) and RLS policies.

### Authentication

#### [NEW] [frontend/src/lib/supabase.ts](file:///d:/Clip-Forge-Ai/frontend/src/lib/supabase.ts)
Initialize Supabase client for the browser environment.

#### [NEW] [frontend/src/app/auth/page.tsx](file:///d:/Clip-Forge-Ai/frontend/src/app/auth/page.tsx)
Build basic authentication UI (Login/Signup).

### Backend Supabase Client

#### [NEW] [backend/app/core/supabase.py](file:///d:/Clip-Forge-Ai/backend/app/core/supabase.py)
Initialize Supabase client (with Service Role Key) for secure server-side operations and token validation.

## Verification Plan

### Automated Tests
- Run backend unit tests for token validation (`pytest`).
- Run backend integration tests for Supabase API interactions (`pytest`).

### Manual Verification
- Attempt signup/login flow in the UI.
- Verify session persistence across page reloads.
- Verify RLS policies: Attempt to access another user's project ID manually in the browser.
- Verify Supabase environment variables are properly typed and loaded by FastAPI.
