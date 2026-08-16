# MS-005 Transcription Service - Agent Instructions

## 1. Milestone Boundaries
- **IN SCOPE:** Audio extraction (FFmpeg), `faster-whisper` local transcription (Primary), OpenAI Whisper API isolated adapter (Fallback), `Transcript` DB models, asynchronous API endpoints, UI transcript view.
- **OUT OF SCOPE:** Background Job Infrastructure (Taskiq, Celery, BackgroundTasks), Universal AI Provider Manager, AI Clip Discovery, Manual Clipping, Caption rendering, Social publishing.

## 2. Allowed Files and Modules
- `backend/app/db/models.py` (Append Transcript, TranscriptSegment, TranscriptWord models)
- `backend/alembic/versions/*` (Create new migration)
- `backend/app/api/v1/transcripts.py` or modifying `projects.py`/`sources.py` (New routes)
- `backend/app/services/transcription.py` (New service defining the domain logic)
- `backend/app/repositories/transcript.py` (New repository)
- `backend/requirements.txt` (Add `faster-whisper`, `openai`)
- `frontend/src/app/projects/[id]/page.tsx` (Add UI for viewing transcript)
- `frontend/src/components/*` (Add Transcript components)

## 3. Forbidden Actions
- Do NOT rewrite existing MS-002, MS-003, or MS-004 logic destructively.
- Do NOT introduce Taskiq, Redis, Celery, or FastAPI BackgroundTasks for background job execution. Build the service interface cleanly so jobs can be integrated in later milestones.
- Do NOT build the Universal AI Provider Manager (MS-006). OpenAI integration must be an isolated adapter.
- Do NOT automatically download huge AI models on startup.
- Do NOT require GPU or assume CUDA exists.

## 4. Coding Requirements
- `faster-whisper` must be CPU-compatible and configurable (model size, compute type, device).
- Ensure audio extraction handles missing audio tracks gracefully.
- Validate incoming media source before beginning transcription.
- Implement API routes to return a job ID and status to avoid blocking HTTP requests.
- No `shell=True` in FFmpeg execution.

## 5. Security & Resource Rules
- NEVER hardcode OpenAI API keys. Read from environment variables.
- Do NOT expose raw provider credentials or detailed crash stack traces to the frontend.
- Validate `project_id` and `source_id` ownership before processing.
- Clean up all temporary extracted audio files from the filesystem after transcription completes.

## 6. Testing & Regression Requirements
- Mock `faster-whisper` and OpenAI API completely in tests. Do NOT download real models or make real network requests in the CI/test suite.
- Write unit tests for the `TranscriptionService`, failure recovery, language detection, and cleanup logic.
- Write API integration tests verifying validation and status transitions.
- Frontend tests must cover all states: No transcript, Queued, Processing, Completed, Failed.
- Existing tests in `tests/api/v1/` and `tests/test_source_ingestion.py` MUST NOT FAIL.

## 7. Verification Requirements
- Docker and PostgreSQL environment blocks are acceptable. Do not fake a pass for runtime verification if the environment is missing.
- Ensure all logic is verifiable via unit/integration tests running on mock data and SQLite.
