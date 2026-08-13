# ClipForge AI — Technical Architecture & System Blueprint

> **Status**: LOCKED (Foundation Phase Verified)  
> **Pattern**: Modular Monolith  

---

## 1. High-Level Modular Monolith Diagram

```
                                  +---------------------------------------+
                                  |            Next.js Frontend           |
                                  |  (React 19 + TypeScript + Tailwind)   |
                                  +---------------------------------------+
                                                      |
                                              REST API / WebSockets
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |           FastAPI Gateway             |
                                  | (Auth / Validation / CORS / Routing)  |
                                  +---------------------------------------+
                                                      |
    +-------------------------------------------------+-------------------------------------------------+
    |                                                 |                                                 |
    v                                                 v                                                 v
+-----------------------+                 +-----------------------+                 +-----------------------+
|  User & Project Subsys|                 | Source Processing Subsys|                 |  Transcription Subsys |
|  - Auth & Ownership   |                 |  - File Ingestion     |                 |  - Whisper/Provider   |
|  - Project Metadata   |                 |  - Youtube Ingestion  |                 |  - Word/Segment Sync  |
+-----------------------+                 +-----------------------+                 +-----------------------+
    |                                                 |                                                 |
    +-------------------------------------------------+-------------------------------------------------+
                                                      |
    +-------------------------------------------------+-------------------------------------------------+
    |                                                 |                                                 |
    v                                                 v                                                 v
+-----------------------+                 +-----------------------+                 +-----------------------+
| AI Intelligence Engine|                 | Framing & Render Engine|                 | Job & Queue Subsystem |
|  - AI Provider Router |                 |  - FFmpeg Processing  |                 |  - Taskiq Worker      |
|  - Vitality Scoring   |                 |  - Caption Overlay    |                 |  - Redis Queue        |
|  - Clip Boundary Eval |                 |  - Aspect Conversion  |                 |  - Async State Machine|
+-----------------------+                 +-----------------------+                 +-----------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |          Infrastructure Layer         |
                                  |  - PostgreSQL (SQLAlchemy ORM)        |
                                  |  - Storage Abstraction (MinIO / S3)   |
                                  |  - Redis Cache & Taskiq Worker Queue  |
                                  +---------------------------------------+
```

---

## 2. Subsystem Boundaries & Responsibilities

1. **API Gateway Layer**: Authentication, CORS policies, rate limiting, request validation (`Pydantic`), uniform response error wrapping.
2. **Project & User Subsystem**: Manages user accounts, authentication tokens, isolated project workspaces, and strict application-level authorization.
3. **Source Processing Subsystem**: Manages local video upload streams and YouTube source downloads. Performs FFmpeg video stream inspection (resolution, framerate, audio streams, codecs, duration).
4. **Transcription Subsystem**: Manages audio extraction (`16kHz mono WAV`) and dispatches Taskiq background transcription jobs. Converts raw transcript files into structured word-level timestamp objects.
5. **AI Intelligence Engine (Multi-Provider Abstraction)**: Orchestrates LLM prompt execution for vitality scoring, clip boundary detection, hook scoring, and standalone context evaluation. Enforces JSON schema validation before passing clip suggestions to application state.
6. **Framing & Render Engine**: Coordinates complex FFmpeg commands to crop aspect ratios (`9:16`, `1:1`, `16:9`), track speaker visual focus, burn customizable dynamic subtitles, and generate final production media artifacts via Taskiq workers.
7. **Job & Queue Subsystem (Taskiq + Redis)**: Redis-backed async task processor managing background task queues (`default`, `media_heavy`, `ai_analysis`). Provides real-time job status notifications and progress tracking (`0% - 100%`).

---

## 3. Storage Architecture & Privacy Boundaries

- **Application-Level Tenant Isolation**: Security boundaries are governed by explicit application-level ownership checks (`WHERE user_id = authenticated_user.id`) for all user-owned entities. PostgreSQL Row-Level Security (RLS) may be evaluated as a future defense-in-depth layer.
- All temporary processing assets (`/tmp/job-id/...`) are strictly isolated by `user_id` and `project_id`.
- Audio streams, thumbnails, rendered clip previews, and master video files are stored under deterministic, non-guessable paths (`storage/{user_id}/{project_id}/{asset_type}/{hash}.ext`).
- Direct public access to media paths is disabled. Media streams are delivered strictly via authorized pre-signed URLs or validated FastAPI streaming routes.
