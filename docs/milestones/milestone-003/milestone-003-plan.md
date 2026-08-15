# MS-003 Implementation Plan: Source Ingestion & Validation

**Status**: PROPOSED

## 1. Objective
Build the source-ingestion foundation that allows ClipForge AI to safely accept supported video sources (local upload and YouTube URLs) and validate their media metadata before any transcription, clipping, AI analysis, editing, or rendering occurs. This milestone establishes the secure media perimeter for all subsequent processing.

## 2. Scope
### A. Local Video Upload
- Accept supported local video files (`.mp4`, `.mov`, `.webm`, `.mkv`).
- Validate file type and size limits (e.g., 2GB max).
- Generate safe internal identifiers.
- Store source metadata.
- Prevent unsafe/untrusted filenames from becoming filesystem paths.

### B. YouTube Source Ingestion (via yt-dlp)
- Accept a YouTube URL.
- Validate URL format and normalize supported forms.
- Use `yt-dlp` for metadata extraction, availability validation, and media info extraction.
- Perform controlled source download to temporary/local storage.
- Do not implement unrelated YouTube discovery functionality.

### C. Media Validation (via FFprobe)
- Independently inspect acquired media using `ffprobe` to determine: duration, width, height, fps, video/audio codecs, audio presence, container, and bitrate.

### D. Source Validation States
- Track explicit validation states: `accepted`, `invalid`, `unsupported`, `corrupted`, `unavailable`, `processing`, `failed`.

### E. Storage Abstraction
- Create an abstraction/interface for source storage (local storage initially) to decouple the application from permanent storage implementations.

### F. Source Metadata Contract
- Define a normalized source metadata structure.

### G. Error Handling & Security
- Standardize error mapping from `yt-dlp` and `ffprobe` failures.
- Address path traversal, command injection, and arbitrary file execution risks.

## 3. Out of Scope
- Transcription (`faster-whisper`, OpenAI).
- AI provider integration, AI clip discovery, vitality scoring.
- Manual clipping, silence detection, timeline editor, captions.
- FFmpeg video rendering, export, social publishing.
- Taskiq workers and Redis job processing (background jobs deferred to designated background-job milestone).
- Persistent job queue and distributed retry orchestration.
- Any background execution coupling (e.g., FastAPI `BackgroundTasks`); MS-003 implements purely synchronous domain logic for testing, while keeping the API boundary thin.

## 4. Existing Architecture / Dependencies
- **FastAPI Backend**: Serves API routes and integrates ingestion services.
- **Next.js Frontend**: Provides the UI for uploading files and inputting YouTube URLs.
- **New Dependencies**: 
  - `yt-dlp` (Python package) for YouTube acquisition.
  - `ffprobe` (System executable) for media inspection.
  - `python-multipart` for handling local file uploads.

- **Service Layer**: Implement `backend/app/services/source/` with an independently testable domain boundary:
  - `SourceIngestionService` coordinating the workflow.
  - `YouTubeSourceProvider` (`youtube.py`) encapsulating `yt-dlp` integration without API awareness.
  - `validator.py` (URL and file validation), `media_probe.py` (`ffprobe` logic), and `storage.py` (storage abstraction).
- **Metadata-First Strategy for YouTube**: 
  1. Validate URL.
  2. Extract metadata via `yt-dlp` (no download).
  3. Validate metadata against limits (duration, size).
  4. Perform controlled download.
  5. Validate downloaded file via `ffprobe`.
- **Local Upload**: Receive file chunks, save safely, run `ffprobe`.

## 6. Frontend Plan
- Create a Source Input UI component allowing file drag-and-drop and YouTube URL input.
- Handle loading, progress, and error states gracefully.
- Interface with MS-003 backend API endpoints.

- Define Pydantic schemas for request/response payloads and the normalized source metadata contract.
- Implement storage abstraction mapping safe UUIDs to filesystem paths.
- Ensure API routes remain extremely thin. They only validate the request, call the `SourceIngestionService`, and return the result. No `yt-dlp` commands will ever reside in a route.

## 8. Media Processing Plan
- **yt-dlp**: Responsible exclusively for YouTube extraction and acquisition.
- **ffprobe**: Responsible for independent media inspection and validation.
- **FFmpeg**: Explicitly NOT used for transcoding or remuxing in MS-003.

## 9. Storage Plan
- **Temporary Source Storage**: Define a local scratch directory (e.g., `storage/tmp/`).
- **Filename Strategy**: Discard user filenames. Generate UUIDs (e.g., `{uuid}.mp4`).
- **Limits & Cleanup**: Enforce max file size (2GB) and duration. Clean up incomplete downloads and failed validations immediately.

## 10. API Contract
### `POST /api/v1/sources/upload`
- **Purpose**: Upload a local video file.
- **Request**: `multipart/form-data` with `file`.
- **Response**: Source Metadata JSON.

### `POST /api/v1/sources/youtube`
- **Purpose**: Submit a YouTube URL for ingestion.
- **Request**: JSON `{ "url": "..." }`.
- **Response**: Source Metadata JSON (with state `processing` or `accepted`).

### `GET /api/v1/sources/{source_id}`
- **Purpose**: Retrieve source metadata.
- **Response**: Source Metadata JSON.

### `GET /api/v1/sources/{source_id}/status`
- **Purpose**: Check validation/ingestion status.
- **Response**: Status JSON.

*Normalized Source Metadata Contract:*
`source_id`, `source_type`, `original_url`, `normalized_url`, `provider`, `provider_video_id`, `title`, `duration`, `width`, `height`, `fps`, `video_codec`, `audio_codec`, `has_audio`, `container`, `file_size`, `local_storage_reference`, `ingestion_status`, `validation_status`, `created_at`.

## 11. Security Plan
- **yt-dlp Safety**: Use Python `yt-dlp` library directly (no shell strings). Normalize URLs. Restrict to YouTube domains.
- **Path Traversal**: Store files using generated UUIDs in controlled directories. Never use user-provided filenames for storage paths.
- **Command Injection**: Use safe subprocess arguments (list form, `shell=False`) for `ffprobe`.
- **File Limits**: Reject oversized uploads/streams to prevent DoS.

## 12. Error Handling
Map `yt-dlp` and `ffprobe` exceptions to sanitized application errors:
- `INVALID_SOURCE_URL`: Malformed or non-YouTube URL.
- `SOURCE_UNAVAILABLE`: Video deleted or private.
- `SOURCE_RESTRICTED`: Age-restricted or geo-blocked.
- `SOURCE_DOWNLOAD_FAILED`: Network/extraction failure.
- `SOURCE_TIMEOUT`: Metadata or download took too long.
- `UNSUPPORTED_MEDIA`: Format not accepted.
- `SOURCE_SIZE_LIMIT_EXCEEDED`: Exceeds 2GB or duration limits.
- `MEDIA_VALIDATION_FAILED`: `ffprobe` cannot parse or indicates corruption.
Raw stack traces will be logged server-side only.

## 13. Testing Strategy
- **Unit Tests**: Execute `yt-dlp` via the service abstraction. Mock `yt-dlp` responses for valid/invalid URLs, timeouts, and download failures. Unit tests MUST NOT require real YouTube downloads. Test filename sanitization and error mapping.
- **Integration Tests**: Upload -> Validation flow. Optional real-YouTube integration tests must be explicitly opt-in and environment-controlled.
- **Security Tests**: Shell injection payloads, path traversal attempts, oversized files, non-YouTube URLs.
- **Media Tests**: `ffprobe` against valid MP4, missing audio, corrupted media.

## 14. Dependency Analysis
- Requires `yt-dlp` Python package.
- Requires system `ffprobe` executable.
- Local Dev Setup: Developers must install `ffprobe` locally and `yt-dlp` via `requirements.txt`. Docker is optional.

## 15. Risk Analysis
- **yt-dlp Breakage**: YouTube frequently changes signatures. Mitigation: Update `yt-dlp` dependency regularly, handle extraction errors gracefully.
- **Long Downloads blocking API**: Since MS-003 explicitly avoids Taskiq/BackgroundTasks, synchronous YouTube downloads will block the request. This is acceptable for the MS-003 isolated scope and will be handled via the proper async architecture in the background-job milestone.

## 16. Rollback Strategy
- Changes are isolated to the `backend/app/services/source` layer and new API routes. Can be reverted via git if critical flaws are discovered.

## 17. Acceptance Criteria
- [ ] `yt-dlp` is used through a dedicated backend service abstraction.
- [ ] YouTube URLs are validated before acquisition.
- [ ] `yt-dlp` metadata extraction is performed safely.
- [ ] Downloads are constrained by size/time/storage limits.
- [ ] User-controlled paths cannot escape the source storage directory.
- [ ] `yt-dlp` exceptions are mapped to sanitized application errors.
- [ ] `ffprobe` independently validates acquired media.
- [ ] Incomplete downloads are cleaned up.
- [ ] No shell command injection is possible through YouTube URLs or filenames.
- [ ] `yt-dlp` unit tests do not require real network downloads.
- [ ] MS-003 does not implement transcription, AI processing, or clipping logic.

## 18. Verification Plan
- Run Pytest suite covering source ingestion unit/integration tests.
- Manually upload a valid and invalid file via frontend.
- Manually ingest a valid YouTube URL and an oversized/invalid YouTube URL.
- Inspect storage directory to confirm UUID filenames and cleanup of failed files.

## 19. File Matrix
- `backend/requirements.txt` (add `yt-dlp`, `python-multipart`)
- `backend/app/api/v1/sources.py`
- `backend/app/services/source/youtube.py`
- `backend/app/services/source/validator.py`
- `backend/app/services/source/media_probe.py`
- `backend/app/services/source/storage.py`
- `backend/app/models/source.py` (Pydantic schemas)
- `frontend/src/components/SourceInput.tsx` (or similar)
- `frontend/src/lib/api-client.ts` (add source routes)

## 20. Post-Approval Implementation Checklist
- [ ] Update `backend/requirements.txt`.
- [ ] Implement `storage.py` (UUID generation, safe paths).
- [ ] Implement `media_probe.py` (`ffprobe` wrapper).
- [ ] Implement `validator.py`.
- [ ] Implement `youtube.py` (`yt-dlp` integration).
- [ ] Implement API routes and Pydantic schemas.
- [ ] Implement frontend UI.
- [ ] Write tests and verify security boundaries.
