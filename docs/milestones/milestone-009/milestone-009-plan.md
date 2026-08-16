# MS-009 Plan — AI Clip Discovery

## 1. Goal & Scope
**Objective:** Enable the system to take an ingested video and its generated transcript, analyze the content using the existing AI Provider Manager (`AIRouter`), and generate a list of high-quality candidate clips for the user to review.

**In Scope:**
- Database schema for `ClipDiscoveryRun` and `ClipCandidate`.
- AI analysis service integrating with the existing `AIRouter`.
- Structured AI candidate generation (using Pydantic schema validation).
- Taskiq worker implementation for async processing.
- Candidate scoring (hook strength, emotional impact, standalone value, etc.).
- Candidate boundary calculation based on transcript word timestamps.
- API endpoints to trigger discovery, check status, and list candidates.
- Minimal frontend UI on the Source page to trigger discovery and display the generated candidate cards.

## 2. Authoritative Constraints
- **Architecture:** Must build heavily on MS-005 (Transcription) and MS-006–MS-008 (Universal AI Provider Manager). No new core frameworks.
- **Tenant Isolation:** All database queries must enforce Project/User ownership limits.
- **Database:** SQLAlchemy 2.0 Async ORM with PostgreSQL.
- **Background Jobs:** Taskiq with Redis must be used for clip discovery.
- **Security:** Strict validation of AI structured outputs.

## 3. Existing Architecture Integration
- The system will query the existing `Transcript`, `TranscriptSegment`, and `TranscriptWord` models.
- The clipping service will construct an `AIRequest` and use `BaseAIProvider.generate_structured()` via the existing `AIRouter`.
- A background worker (`@broker.task`) will be added to `backend/app/tasks/clipping.py`.

## 4. File Matrix
### Backend
#### [NEW] `backend/app/db/models/clipping.py`
Defines `ClipDiscoveryRun` and `ClipCandidate` SQLAlchemy models.

#### [NEW] `backend/app/models/clipping.py`
Pydantic schemas for clipping API (e.g., `ClipCandidateCreate`, `ClipCandidateResponse`).

#### [NEW] `backend/app/repositories/clipping.py`
`ClippingRepository` for creating discovery runs and saving candidate lists.

#### [NEW] `backend/app/services/clipping/discovery.py`
`ClipDiscoveryService`. Constructs the AI prompt containing transcript context, calls `AIRouter.generate_structured()`, maps words to timestamps, and validates boundaries.

#### [NEW] `backend/app/tasks/clipping.py`
Taskiq task for executing the long-running discovery asynchronously.

#### [NEW] `backend/app/api/v1/clipping.py`
FastAPI router containing discovery endpoints.

#### [MODIFY] `backend/app/api/v1/__init__.py`
Include the new clipping router.

#### [MODIFY] `backend/app/db/migrations/env.py` (or Alembic rev)
Generate new migration for clipping tables.

### Frontend
#### [MODIFY] `frontend/src/app/projects/[projectId]/sources/[sourceId]/page.tsx`
Add a UI section to start clip discovery, poll for status, and display the resulting `ClipCandidate` cards.

## 5. Database & Persistence
- `ClipDiscoveryRun`
  - `id` (PK, UUID)
  - `project_id` (FK to projects)
  - `source_id` (FK to sources)
  - `status` (queued, processing, completed, failed)
  - `error_message`
  - `created_at`, `updated_at`
- `ClipCandidate`
  - `id` (PK, UUID)
  - `run_id` (FK to clip_discovery_runs)
  - `project_id` (FK to projects)
  - `title`, `hook`, `reason`
  - `start_time`, `end_time`, `duration`
  - `score`, `confidence`
  - `transcript_excerpt`
  - `status` (pending_review, approved, rejected)

*Both tables will include strict indexing and ON DELETE CASCADE for project/source cleanup.*

## 6. AI Architecture
- **Request Flow:** `ClipDiscoveryService` -> `AIRouter` -> Selected AI Provider.
- **Provider Fallback:** Standard routing behavior (respecting free-first/free-only).
- **Structured Output:** The provider's `generate_structured` method will be utilized with a strict Pydantic model (`AIClipCandidateList`).
- **Context Handling:** Transcripts will be passed directly. (Chunking logic deferred unless testing proves it necessary for extremely long inputs, based on current model context windows).

## 7. Clip Discovery Algorithm
1. **Input:** Fetch all transcript words/segments.
2. **AI Analysis:** Provide AI with text and segment metadata. Request a specific number of standalone clips.
3. **Structured Response:** AI returns candidate bounds (e.g., matching start/end segment indices or specific text bounds).
4. **Timestamp Mapping:** Service matches the AI's selected text to the exact DB timestamps using `TranscriptWord` bounds.
5. **Validation:** Reject negative durations, bounds exceeding source length, or AI hallucinated quotes.
6. **Persistence:** Save valid candidates to the DB and update run status to `completed`.

## 8. API Design
- `POST /api/v1/projects/{project_id}/sources/{source_id}/clip-discovery` (Triggers async job, returns Run ID)
- `GET /api/v1/projects/{project_id}/sources/{source_id}/clip-discovery/{run_id}` (Returns status & candidates if complete)
- `GET /api/v1/projects/{project_id}/clip-candidates` (List all candidates for project)

## 9. Frontend Integration
- **Component:** `ClipDiscoveryPanel` added to the Source detail view.
- **Flow:** Button "Discover Clips" -> Displays loading spinner -> Polls API -> Renders a list of `CandidateCard` components.
- **CandidateCard:** Displays title, hook, excerpt, score, and start/end times.

## 10. Security
- API Endpoints strictly enforce that the `authenticated_user.id` is the owner of the `project_id`.
- Foreign Keys naturally restrict cross-project contamination.
- AI Provider API keys remain strictly backend-only. No leak via HTTP responses.

## 11. Testing & Regression
- **Unit Tests:** `backend/tests/services/clipping/test_discovery.py` (Mock AIRouter, test timestamp validation, handling of hallucinated quotes).
- **API Tests:** Test auth boundaries, job queuing, and status retrieval.
- **Frontend:** Test rendering of valid candidate cards and error handling.
- **Regression:** Ensure `MS-005` (transcription) and `MS-006` (routing) tests continue to pass.

## 12. Verification
- `pytest`
- `npm run test -- --run`
- `npm run build`
- `alembic upgrade head`
*(No SQLite workarounds permitted. ConnectionRefusedError is expected if Postgres is missing, which will be logged as BLOCKED - ENVIRONMENT).*

## 13. Risks & Rollback
- **Risk:** AI Model hallucinating text not in the transcript.
  - **Mitigation:** Strict boundary mapping algorithm that matches text to exact `TranscriptWord` entries. Rejects candidate if match fails.
- **Risk:** Large transcripts exceeding AI context.
  - **Mitigation:** Modern models (Ollama, Gemini, gpt-4o) have >100k context, which covers most reasonable videos.
- **Rollback:** `git reset --hard milestone/001-foundation`, drop the clipping tables.

## 14. Acceptance Criteria
- [ ] New `ClipDiscoveryRun` and `ClipCandidate` tables are queryable.
- [ ] Taskiq worker processes the discovery async.
- [ ] API accurately validates ownership of Project and Source.
- [ ] Service maps AI-selected text to real transcript timestamps.
- [ ] UI allows triggering and viewing results.
- [ ] Backend and Frontend build cleanly.

## 15. Explicit Out-of-Scope Items
- Manual clipping engine.
- Clip editor (Timeline, Video Cropping).
- Captions, styling, export, rendering.
- Any direct API calls bypassing `AIRouter`.
- Social publishing.

## 16. Implementation Order
1. Database Models & Migrations
2. Repositories & Schemas
3. Clip Discovery Service & AI integration
4. Taskiq Worker
5. FastAPI Endpoints
6. Tests
7. Frontend Integration

## 17. Final Approval Gate
**USER REVIEW & EXPLICIT APPROVAL REQUIRED.**
