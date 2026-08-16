# MS-005 Implementation Plan: Transcription Service

## 1. Milestone Objective
Implement the Transcription Service to perform Speech-to-Text extraction on ingested video sources using a local-first strategy, supporting multilingual audio and word-level timestamps.

## 2. Problem Being Solved
Long-form video cannot be intelligently clipped by AI or properly captioned without a highly accurate, timestamped text transcript. The system must automatically extract audio and transcribe it into word-level segments without relying exclusively on paid cloud APIs.

## 3. Exact Scope
**IN SCOPE:**
- Audio extraction from ingested source videos (FFmpeg).
- Integration with `faster-whisper` for local, zero-cost transcription as the primary engine (configurable model size, compute type, device).
- Fallback integration with OpenAI Whisper API for cloud transcription (isolated adapter).
- Multilingual support with language detection.
- Generation of segment-level and word-level timestamps.
- Database persistence of `Transcript`, `TranscriptSegment`, and `TranscriptWord` models.
- Backend API endpoints structured for asynchronous task triggers and polling, utilizing a clean service contract.
- Frontend UI to view the transcript within a Project (Queued, Processing, Completed, Failed states).

**EXPLICITLY EXCLUDED (OUT OF SCOPE):**
- Background Job Infrastructure (Taskiq + Redis is deferred to later milestones).
- Universal AI Provider Manager (MS-006).
- AI Clip Discovery and Vitality Scoring (MS-010).
- Manual Clipping Engine (MS-009).
- Caption/Subtitle visual rendering and styling (MS-013).
- Direct use of FastAPI `BackgroundTasks` for production execution.
- Forced paid API usage or auto-upgrades.

## 4. Features Included
- **FEAT-004**: Speech-to-Text Transcription
- **FEAT-003**: Audio Extraction & Silence Detection (Audio extraction specifically for Whisper).

## 5. Backend Work
- **Audio Extraction**: Use FFmpeg to extract audio tracks from ingested video sources gracefully.
- **Transcription Engine**: Implement `faster-whisper` for local transcription (CPU-compatible, lazy-loaded). Implement an isolated OpenAI Whisper API adapter strictly for fallback.
- **Service Contract**: Define `TranscriptionService` with clean abstraction that allows future background job engines (Taskiq) to execute the long-running task. The API design will simulate an asynchronous pattern (returning a job ID/status) so clients do not hold HTTP connections open.
- **Resource Safety**: Enforce configuration limits on concurrent transcriptions, memory footprint, model sizes, and timeouts. Ensure cleanup of temporary files.

## 6. Frontend Work
- **Transcript View**: A UI component on the Project page to display the generated transcript.
- **Status Indicators**: Show transcription progress/status (`No transcript`, `Queued`, `Processing`, `Completed`, `Failed`).
- **Data Display**: Render detected language, text, segment timestamps, and word timestamps. Provide a retry action for failures.

## 7. Database Work
Create new SQLAlchemy models and Alembic migrations specifically for transcription:
- `Transcript` (belongs to `Source`)
- `TranscriptSegment` (belongs to `Transcript`)
- `TranscriptWord` (belongs to `TranscriptSegment`)

## 8. API Changes
- `POST /api/v1/projects/{project_id}/sources/{source_id}/transcribe` (Trigger transcription task, returns status/ID)
- `GET /api/v1/projects/{project_id}/sources/{source_id}/transcript` (Retrieve transcript and its status)

## 9. Dependencies
- `faster-whisper` (Python package)
- `openai` (Python package for Whisper fallback only)

## 10. Security Requirements
- Ensure OpenAI API keys are strictly read from environment variables and never exposed to the frontend.
- Validate `project_id` and `source_id` ownership (tenant isolation) before processing or returning transcripts.
- Prevent shell injection in FFmpeg commands (no `shell=True`).
- Clean up all temporary extracted audio files after transcription to prevent storage leaks.
- Sanitize error messages sent to the frontend.

## 11. Testing Strategy
- **Unit Tests**: Mock `faster-whisper` and OpenAI APIs to test parsing, language detection, and database storage logic. Verify resource cleanup and failure handling. Do not download real models during tests.
- **Integration Tests**: Test the API endpoints for triggering and fetching transcripts. Verify project/source relationship validation.
- **Frontend Tests**: Test empty state, queued, processing, completed, and failed states of the transcript UI. Mock API responses.

## 12. Regression Requirements
- MS-002 Health/Ready endpoints must remain intact.
- MS-003 Source Ingestion must continue functioning.
- MS-004 Project/Source persistence must not be broken by the new models.

## 13. Acceptance Criteria
- Given a valid ingested source, when the user requests transcription, the backend extracts audio and delegates to the transcription service.
- Local `faster-whisper` is attempted first. If configured and required, OpenAI Whisper is used as fallback.
- Transcript is saved to PostgreSQL with accurate timestamps.
- Frontend successfully displays the transcript and its status.
- Temporary audio files are rigorously deleted.

## 14. Verification Requirements
- Static verification (Lint, passing test suite) is mandatory.
- Environmental exceptions (Docker, PostgreSQL) are reported but static tests must mock behavior thoroughly to prove logical correctness.

## 15. Definition of Done
- Implementation matches this plan exactly.
- Background Job Infrastructure and Universal AI Provider Manager are NOT implemented.
- Automated backend and frontend tests pass.
- Code is clean, documented, and secure.
