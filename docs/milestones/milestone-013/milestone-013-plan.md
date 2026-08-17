# MS-013 — Rendering Pipeline

## 1. Objective
Implement the asynchronous video rendering pipeline to transform an approved AI clip (with its framing and caption configuration) into a final MP4 video artifact. The system must use Taskiq and Redis for background job management, track state (`QUEUED` → `PROCESSING` → `COMPLETED` / `FAILED`), and clean up temporary FFmpeg artifacts.

## 2. Authoritative Source Evidence
- **MILESTONE_REGISTRY.md**: "MS-013 | Rendering Pipeline | Asynchronous FFmpeg render via Taskiq + Redis, state machine..."
- **PRD.md**: "Stage 13: Background FFmpeg Render Execution (Taskiq + Redis)" and "task_render_clip: Executes FFmpeg video framing, dynamic subtitle overlay burn, and clip rendering."

## 3. Current Repository State
- Branch: `milestone/001-foundation`
- The MS-012 Caption Engine has been successfully merged and locked.
- The repository contains clip generation, framing metadata, and caption metadata.
- No MS-013 implementation branch exists. Working tree is clean.

## 4. Dependencies
- **Taskiq + Redis**: Established in MS-002, used in MS-003/MS-005. MS-013 relies on this for asynchronous execution.
- **Database Models**: MS-011 and MS-012 established `ClipCandidate` and `ClipCaptionConfig`. MS-013 will read from these to determine render instructions.
- **Storage Driver**: MS-003 established the local storage hierarchy. Rendered output will be saved here.

## 5. Scope
**IN SCOPE**:
- `RenderJob` database table and SQLAlchemy model.
- Taskiq background job (`task_render_clip`) for FFmpeg video processing.
- FFmpeg command generation mapping Framing and Caption configurations to video filters.
- API endpoints for triggering and polling render jobs.
- Frontend UI integration (Render button and progress indicator) in the Editor.

## 6. Out of Scope
- Rendered clip gallery UI (Reserved for MS-014).
- Direct API publishing to social media.
- Cloud rendering (AWS MediaConvert, etc.). FFmpeg is executed locally.

## 7. Architecture
A lightweight asynchronous job architecture. The user requests a render via the API. The API creates a `RenderJob` record in the database with status `queued` and dispatches a Taskiq job. The Taskiq worker executes FFmpeg using `subprocess.run()`, periodically updating the `progress` field in the database. The frontend polls the status endpoint to update the UI.

## 8. Database Plan
**Table**: `render_jobs`
- `id` (UUID, PK)
- `clip_id` (UUID, FK `clip_candidates.id`)
- `project_id` (UUID, FK `projects.id`)
- `status` (String: `queued`, `processing`, `completed`, `failed`, `cancelled`)
- `progress` (Float, 0.0 to 100.0)
- `output_path` (String, nullable)
- `error_message` (String, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `completed_at` (DateTime, nullable)

## 9. Backend Plan
- **`backend/app/db/models.py`**: Add `RenderJob` model.
- **`backend/app/models/render.py`**: Add Pydantic schemas (`RenderJobCreate`, `RenderJobResponse`).
- **`backend/app/services/render.py`**: FFmpeg command builder converting clip boundaries, framing mode, and caption styles into complex filter graphs.
- **`backend/app/tasks/render.py`**: Taskiq worker function `task_render_clip` that invokes the FFmpeg subprocess and updates job state.
- **`backend/alembic/versions/`**: Migration script for the `render_jobs` table.

## 10. API Plan
- **`POST /api/v1/clips/{clip_id}/render`**: Creates a RenderJob and queues the task. Returns `RenderJobResponse`.
- **`GET /api/v1/renders/{job_id}`**: Retrieves the current status and progress of the render job.

## 11. Frontend Plan
- **`frontend/src/hooks/useRender.ts`**: Hook to trigger the render and poll for progress.
- **`frontend/src/components/editor/RenderButton.tsx`**: A button in the editor interface that initiates rendering and transforms into a progress bar/spinner while processing.
- **`frontend/src/app/projects/[projectId]/clips/[clipId]/edit/page.tsx`**: Integrate the `RenderButton`.

## 12. Testing Plan
- **Backend**: Unit tests for the FFmpeg command builder (ensuring correct filter arguments). API tests for job creation and polling.
- **Taskiq**: Integration tests mocking `subprocess.run` to verify state transitions (`queued` -> `processing` -> `completed`/`failed`).
- **Frontend**: Component tests for `RenderButton` state transitions (Idle -> Processing -> Done).

## 13. Security Plan
- Render endpoints must validate `user_id` authorization (Tenant Isolation) to ensure users can only render clips they own.
- Input validation: Prevent command injection in FFmpeg by strictly sanitizing and typing all framing/caption variables.
- Secrets: No new secrets introduced.

## 14. File-Level Implementation Matrix

| File | Action | Purpose | Scope |
| ---- | ------ | ------- | ----- |
| `backend/app/db/models.py` | MODIFY | Add `RenderJob` model | IN |
| `backend/alembic/versions/*_render_jobs.py` | CREATE | DB Migration | IN |
| `backend/app/models/render.py` | CREATE | Pydantic schemas | IN |
| `backend/app/services/render.py` | CREATE | FFmpeg logic | IN |
| `backend/app/tasks/render.py` | CREATE | Taskiq background job | IN |
| `backend/app/api/v1/render.py` | CREATE | API endpoints | IN |
| `backend/app/main.py` | MODIFY | Register router | IN |
| `frontend/src/hooks/useRender.ts` | CREATE | Render polling hook | IN |
| `frontend/src/components/editor/RenderButton.tsx` | CREATE | UI for rendering | IN |
| `frontend/src/app/projects/[projectId]/clips/[clipId]/edit/page.tsx` | MODIFY | Mount button | IN |
| `backend/tests/api/v1/test_render.py` | CREATE | Tests | IN |

## 15. Implementation Sequence
1. **Phase 1 — Database**: Create `RenderJob` model and Alembic migration.
2. **Phase 2 — Backend Foundation**: Implement Pydantic models and FFmpeg command builder service.
3. **Phase 3 — Tasks**: Implement `task_render_clip` in Taskiq.
4. **Phase 4 — API**: Implement and register the render endpoints.
5. **Phase 5 — Frontend**: Create `useRender` hook and `RenderButton` component.
6. **Phase 6 — Integration**: Verify full loop from UI to FFmpeg execution.
7. **Phase 7 — Security & Tests**: Add authorization checks and unit tests.

## 16. Acceptance Criteria
- **Given** an approved clip with framing and caption settings, **When** the user clicks "Render", **Then** the UI shows a progress indicator and the backend queues a Taskiq job.
- **Given** an active render job, **When** the FFmpeg subprocess runs, **Then** the job progress updates in the database and is reflected in the frontend.
- **Given** a successful FFmpeg run, **Then** the job status changes to `completed` and the final MP4 artifact is saved in the correct storage directory.

## 17. Risk Register
- **Risk**: FFmpeg command injection vulnerabilities.
  - **Mitigation**: Strictly validate and type-cast all inputs; never pass user-provided strings directly to shell without shell-escaping or using array arguments.
- **Risk**: High CPU/Memory usage during render locking up the server.
  - **Mitigation**: Taskiq concurrency limits; `nice` value usage if necessary.

## 18. Regression Protection
- Run existing MS-001 through MS-012 pytest suites to ensure no existing clip or project flows are broken.

## 19. Verification Gates
- Full test pass required.
- Successful end-to-end render generation with valid MP4 output.
- No credentials leaked.

## 20. Governance Rules
1. MS-001 through MS-012 are locked and must not be modified directly.
2. MS-013 must be implemented on its own branch.
3. No MS-014+ functionality may be introduced.
4. No unauthorized dependencies may be installed.
5. No real credentials may be committed.
6. No database changes outside MS-013 scope.
7. No frontend redesign outside MS-013 scope.
8. No architectural changes without an authoritative decision.
9. Environmental failures must be documented, not bypassed through unauthorized substitutes.
10. Implementation requires explicit user approval after planning.

## 21. Definition of Done
- MS-013 branch is fully implemented and tested.
- Verification report is generated.
- Zero secrets committed.
- Ready for PR and merge.
