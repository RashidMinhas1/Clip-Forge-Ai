# ClipForge AI — Technical Architecture & System Blueprint

> **Status**: LOCKED (Foundation Phase)  
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
| AI Intelligence Engine|                 | Framing & Render Engine|                 | Job & Queue System    |
|  - AI Provider Router |                 |  - FFmpeg Processing  |                 |  - Redis Worker       |
|  - Vitality Scoring   |                 |  - Caption Overlay    |                 |  - Async State Machine|
|  - Clip Boundary Eval |                 |  - Aspect Conversion  |                 |  - Telemetry & Retries|
+-----------------------+                 +-----------------------+                 +-----------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |          Infrastructure Layer         |
                                  |  - PostgreSQL (SQLAlchemy ORM)        |
                                  |  - Storage Abstraction (MinIO / S3)   |
                                  |  - Redis Cache & Task Queue           |
                                  +---------------------------------------+
```

---

## 2. Subsystem Boundaries & Responsibilities

1. **API Gateway Layer**: Authentication, CORS policies, rate limiting, request validation (`Pydantic`), uniform response error wrapping.
2. **Project & User Subsystem**: Manages user accounts, authentication tokens, isolated project workspaces, and strict relational access boundaries.
3. **Source Processing Subsystem**: Manages local video upload streams and YouTube source downloads. Performs FFmpeg video stream inspection (resolution, framerate, audio streams, codecs, duration).
4. **Transcription Subsystem**: Manages audio extraction (`16kHz mono WAV`) and dispatches background transcription jobs. Converts raw transcript files into structured word-level timestamp objects.
5. **AI Intelligence Engine (Multi-Provider Abstraction)**: Orchestrates LLM prompt execution for vitality scoring, clip boundary detection, hook scoring, and standalone context evaluation. Enforces JSON schema validation before passing clip suggestions to application state.
6. **Framing & Render Engine**: Coordinates complex FFmpeg commands to crop aspect ratios (`9:16`, `1:1`, `16:9`), track speaker visual focus, burn customizable dynamic subtitles, and generate final production media artifacts.
7. **Job & Queue Subsystem**: Redis-backed async task processor managing background queues (`default`, `media_heavy`, `ai_analysis`). Provides real-time job status notifications and progress tracking (`0% - 100%`).

---

## 3. Storage Architecture & Privacy Boundaries

- All temporary processing assets (`/tmp/job-id/...`) are strictly isolated by `user_id` and `project_id`.
- Audio streams, thumbnails, rendered clip previews, and master video files are stored under deterministic, non-guessable paths (`storage/{user_id}/{project_id}/{asset_type}/{hash}.ext`).
- Direct public access to media paths is disabled. Media streams are delivered strictly via authorized pre-signed URLs or validated FastAPI streaming routes.
