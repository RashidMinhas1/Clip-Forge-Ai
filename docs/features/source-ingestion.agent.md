# Feature Agent Specification: Source Ingestion & Validation

**Feature ID**: FEAT-001 (Local Video Upload) & FEAT-002 (YouTube Video Source)
**Target Milestone**: MS-003
**Status**: PROPOSED / REVIEW

## 1. Feature Overview
The Source Ingestion & Validation feature is responsible for safely acquiring, validating, and temporarily storing video media from both local uploads and YouTube URLs. This forms the foundational media perimeter for ClipForge AI; no media can proceed to transcription, clipping, or rendering without successfully passing this stage. It utilizes `yt-dlp` for YouTube extraction and `ffprobe` for independent media validation.

## 2. Dependencies & Infrastructure
- **yt-dlp**: Used strictly for YouTube URL validation, metadata extraction, and controlled downloading.
- **ffprobe**: Used strictly for media inspection (duration, resolution, fps, codecs).
- **FastAPI / python-multipart**: Used for chunked local file uploads.
- **Local Storage**: Temporary directory for processing source files (`storage/tmp/`).

## 3. Scope & Boundary
### In-Scope
- Receiving local video uploads (MP4, MOV, WEBM, MKV).
- Accepting YouTube URLs.
- Validating file size (up to 2GB) and duration constraints.
- Using `yt-dlp` to fetch metadata and safely download YouTube video files.
- Independent media validation using `ffprobe`.
- Standardized error mapping for network and validation failures.
- Secure path generation (UUIDs) and file cleanup.

### Out-of-Scope
- Video transcoding or remuxing (via FFmpeg).
- Audio transcription.
- AI processing or clipping.
- Persistent database mapping (unless specifically requested by MS-003 boundary limits).

## 4. Technical Architecture
The feature is implemented within the backend service layer, enforcing separation of concerns. MS-003 strictly avoids Taskiq and background-job coupling, ensuring the service boundary is purely synchronous and independently testable.
- **API Boundary**: `backend/app/api/v1/sources.py` handles HTTP request parsing and response formatting. API routes remain completely thin.
- **Service Layer**: 
  - `backend/app/services/source/ingestion.py`: `SourceIngestionService` coordinating the workflow.
  - `backend/app/services/source/youtube.py`: `YouTubeSourceProvider` wrapping `yt-dlp` execution securely.
  - `backend/app/services/source/validator.py`: Enforces rules (size, duration, format).
  - `backend/app/services/source/media_probe.py`: Wraps `ffprobe` execution.
  - `backend/app/services/source/storage.py`: Manages safe file paths and temporary storage.

## 5. yt-dlp & FFprobe Strategy
### YouTube Acquisition (yt-dlp)
1. **Validation**: Normalize URL and verify against allowed YouTube domains.
2. **Metadata Extraction**: Run `yt-dlp --dump-json` to retrieve video metadata without downloading.
3. **Limit Check**: Verify metadata duration/size against application limits.
4. **Download**: Run `yt-dlp` with constraints to download media to the designated temporary storage path (using a UUID filename).

### Media Validation (FFprobe)
Regardless of the source (local or YouTube), `ffprobe` runs on the local file to extract:
- `video_codec`, `audio_codec`, `width`, `height`, `fps`, `duration`.
If `ffprobe` fails or indicates corruption, the source is marked `invalid` and deleted.

## 6. Security Constraints
- **Subprocess Safety**: All `yt-dlp` and `ffprobe` executions must use list-based arguments with `shell=False`. No string concatenation for commands.
- **Path Traversal Prevention**: Storage paths are generated using UUIDs. Original filenames are strictly discarded for filesystem operations.
- **URL Sanitization**: User-provided URLs are strictly checked to ensure they match YouTube regex before being passed to `yt-dlp`.
- **DoS Prevention**: Hard limits on file sizes (2GB) and upload constraints to prevent storage/memory exhaustion.

## 7. Error Mapping
`yt-dlp` and `ffprobe` errors are caught and sanitized before returning to the user:
- `INVALID_SOURCE_URL`
- `SOURCE_UNAVAILABLE`
- `SOURCE_RESTRICTED`
- `SOURCE_DOWNLOAD_FAILED`
- `SOURCE_TIMEOUT`
- `UNSUPPORTED_MEDIA`
- `SOURCE_SIZE_LIMIT_EXCEEDED`
- `MEDIA_VALIDATION_FAILED`

## 8. Source Metadata Contract
All successfully ingested sources must produce a normalized metadata object:
```json
{
  "source_id": "uuid-string",
  "source_type": "local | youtube",
  "original_url": "...",
  "normalized_url": "...",
  "provider": "youtube",
  "provider_video_id": "...",
  "title": "Video Title",
  "duration": 120.5,
  "width": 1920,
  "height": 1080,
  "fps": 30.0,
  "video_codec": "h264",
  "audio_codec": "aac",
  "has_audio": true,
  "container": "mp4",
  "file_size": 150450,
  "local_storage_reference": "/safe/path/uuid.mp4",
  "ingestion_status": "accepted",
  "validation_status": "valid",
  "created_at": "timestamp"
}
```

## 9. Testing Requirements
- **Unit**: Execute `yt-dlp` synchronously via the service abstraction. Mock `yt-dlp` and `ffprobe` responses. Ensure errors map to correct application exceptions. Validate URL regex and filename sanitization. Unit tests MUST NOT require real YouTube downloads.
- **Integration**: Test local file upload flow. Ensure YouTube ingestion logic handles network timeouts properly. Optional real-YouTube integration tests must be explicitly opt-in and environment-controlled.
- **Security**: Provide malformed URLs, shell injection attempts, and path traversal payloads to ensure they are blocked.

> [!IMPORTANT]
> Awaiting User Approval to begin execution.
