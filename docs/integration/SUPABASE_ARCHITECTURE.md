# Supabase Architecture Plan

## A. Existing Architecture

- **Current Database**: None implemented yet (MS-003 is currently planned for raw PostgreSQL/SQLAlchemy).
- **Current Persistence**: None implemented yet.
- **Current Auth**: None implemented yet.
- **Current Storage**: MinIO/S3 StorageDriver planned, but not yet implemented (MS-004 planned).
- **Current Project Lifecycle**: Planned but not implemented.
- **Current Processing Lifecycle**: Taskiq + Redis background queues are planned, FastAPI gateway is present but has no job endpoints yet.

## B. Target Architecture

The application will replace the originally planned raw PostgreSQL + SQLAlchemy stack with Supabase. Supabase will act as the Backend-as-a-Service for Auth, Database, Storage, and Realtime.

```text
Frontend (Next.js)
↓
Application API / Server (FastAPI)
↓
Supabase
├── Auth (User management, JWT issuance)
├── PostgreSQL (Projects, sources, clips, jobs)
├── Storage (Source videos, thumbnails, exports)
└── Realtime (Job status updates)

Local Processing Layer (FastAPI/Taskiq Workers)
├── FFmpeg (Video processing)
├── Temporary Files (Split-screen renders, caches)
├── Transcription Processing (faster-whisper)
└── AI Intelligence Engine
```

### Database Design

The minimum required Supabase schema (to be implemented via migrations):
- `profiles`: user_id (PK, matches auth.users), updated_at
- `projects`: id (PK), user_id (FK), name, created_at, updated_at
- `project_sources`: id (PK), project_id (FK), user_id (FK), original_filename, storage_path, status, duration
- `clips`: id (PK), project_id (FK), user_id (FK), start_time, end_time, vitality_score, transcript_data
- `render_jobs`: id (PK), user_id (FK), project_id (FK), status (queued, processing, completed, failed), progress

*All tables will use UUIDs.*

### User Ownership Model & RLS

Every entity maps back to a `user_id`. RLS is mandatory for all user-owned tables.
- **SELECT/INSERT/UPDATE/DELETE** policies will check `auth.uid() = user_id`.

### Supabase Auth

Supabase Auth will handle signup/login. The FastAPI backend will validate the Supabase JWT using the Anon key or verify it via the Supabase Admin client for secure routes.

### Supabase Storage

Buckets:
1. `source-videos`: Raw uploaded/downloaded video files.
2. `project-assets`: Thumbnails and transcript files.
3. `exports`: Final rendered clips.

Path convention: `{user_id}/{project_id}/...`
*Storage RLS policies will restrict access to paths starting with `auth.uid()`.*

### API / Server Architecture

- **Frontend**: Handles public operations, Auth, and direct Realtime subscriptions.
- **FastAPI Backend**: Acts as a trusted service layer for media heavy-lifting and AI orchestration. Will use `SUPABASE_SERVICE_ROLE_KEY` for secure server-side operations (like updating job status or transcription results).

### Offline / Local Behavior

The target architecture respects local processing. Massive temporary video chunks, FFmpeg working files, and render caches will remain on local ephemeral storage (`/tmp/job-id/...`) processed by Taskiq workers, only pushing final artifacts to Supabase Storage.
