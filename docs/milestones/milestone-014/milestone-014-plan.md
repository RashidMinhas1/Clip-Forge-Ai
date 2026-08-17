# MS-014 — Export & Gallery

## 1. Objective
Implement the Export & Download Gallery system. This includes a rendered clip gallery view on the frontend, endpoints to download the final MP4 artifact, generation and download of subtitles (SRT, VTT, TXT, JSON), and basic retry handling for failed renders.

## 2. Authoritative Scope
- **MILESTONE_REGISTRY.md**: "Rendered clip gallery, download endpoints, metadata persistence, retry handling, UI integration."
- **PRD.md**: "Stage 14: Export & Download Gallery" and "Export Formats: .srt, .vtt, .txt, .json".

## 3. Current Repository State
- Branch: `milestone/001-foundation`
- The MS-013 Rendering Pipeline has been successfully merged and locked.
- The `RenderJob` table stores the `output_path` and `status` of FFmpeg renders.

## 4. Dependencies on MS-013
- **RenderJob**: The gallery depends on `RenderJob` records where `status` is `completed` (or `failed` for retries).
- **Storage Driver**: MP4 artifacts are stored via the local storage mechanism initialized in earlier milestones and used by MS-013.

## 5. Architecture
- **Backend API**: A new router `/api/v1/exports` will provide gallery listing (fetching completed/failed `RenderJob` records for a project), file download capabilities, and dynamic generation of SRT/VTT/TXT files based on the clip's transcript segment.
- **Frontend UI**: A new `Exports` page in the project dashboard (`/projects/[projectId]/exports/page.tsx`) to display a grid of completed renders with download options, and to handle render retries.

## 6. Backend Plan
- `backend/app/api/v1/exports.py`: Endpoints for listing exports by project, downloading MP4, generating/downloading subtitles.
- `backend/app/services/export.py`: Service class responsible for formatting `TranscriptWord` data into valid SRT, VTT, TXT, and JSON formats for the specific boundaries of the `ClipCandidate`.
- `backend/app/models/export.py`: Pydantic models for the export gallery response.
- `backend/app/api/v1/render.py`: Add a `POST /api/v1/renders/{job_id}/retry` endpoint to reset status and re-queue a failed render.

## 7. Frontend Plan
- `frontend/src/app/projects/[projectId]/exports/page.tsx`: The Gallery page for the project.
- `frontend/src/components/exports/ExportCard.tsx`: UI component displaying the clip thumbnail, status, and download actions.
- `frontend/src/hooks/useExports.ts`: Hook to fetch the project's gallery and handle downloads.

## 8. Database Plan
**DATABASE CHANGES: NONE REQUIRED**
The existing `RenderJob` table sufficiently captures the export metadata (`output_path`, `status`, `clip_id`, `project_id`, `created_at`). Retry logic simply resets the `RenderJob` status to `queued` and re-dispatches the Taskiq job.

## 9. API Plan
- `GET /api/v1/projects/{project_id}/exports`: List `RenderJob` records for a project.
- `GET /api/v1/exports/{job_id}/download/video`: Serve the MP4 file (FileResponse).
- `GET /api/v1/exports/{job_id}/download/captions?format=srt`: Generate and serve the subtitle file.
- `POST /api/v1/renders/{job_id}/retry`: Retry a failed render job.

## 10. File Change Matrix

| File | Action | Layer | Purpose | Risk |
|------|--------|-------|---------|------|
| `backend/app/api/v1/exports.py` | CREATE | API | Gallery and download endpoints | Low |
| `backend/app/services/export.py` | CREATE | Service | SRT/VTT/TXT/JSON generator | Low |
| `backend/app/models/export.py` | CREATE | Model | Pydantic response schemas | Low |
| `backend/app/api/v1/render.py` | MODIFY | API | Add `/retry` endpoint | Low |
| `backend/app/main.py` | MODIFY | Core | Register `exports` router | Low |
| `frontend/src/app/projects/[projectId]/exports/page.tsx` | CREATE | Page | Gallery UI view | Low |
| `frontend/src/components/exports/ExportCard.tsx` | CREATE | Component | Individual export display | Low |
| `frontend/src/hooks/useExports.ts` | CREATE | Hook | Gallery state management | Low |
| `frontend/src/app/projects/page.tsx` | MODIFY | Page | Update navigation to include exports if applicable | Low |
| `backend/tests/api/v1/test_exports.py` | CREATE | Tests | API and format tests | Low |

## 11. Security Plan
- Verify project ownership and tenant isolation on all `/api/v1/exports` endpoints.
- Ensure `FileResponse` paths are securely sanitized and strictly bounded to the user's storage directory to prevent path traversal attacks.
- Ensure no secret leakage. `git grep -i -E "api_key\|apikey\|authorization\|bearer\|secret\|password"` will be run.

## 12. Testing Plan
- **Backend Unit**: Test `export.py` formatting logic to ensure SRT/VTT outputs are strictly compliant with standards.
- **Backend API**: Test download endpoints, ensuring 404s for missing files and 403s for unauthorized access. Test the retry endpoint.
- **Frontend**: Component tests for `ExportCard` download triggers and retry triggers.

## 13. Regression Protection
- Run existing MS-001 through MS-013 pytest suites.
- MS-014 must not modify `task_render_clip` (MS-013) or `ClipEditor` (MS-011) functionality.

## 14. Scope Boundaries
**IN SCOPE**:
- Render gallery view per project.
- MP4 download.
- SRT/VTT/TXT/JSON subtitle generation and download.
- Failed render retry.

**OUT OF SCOPE (MS-015+)**:
- Direct social media publishing APIs (TikTok/YouTube).
- Cloud storage syncing (S3, Dropbox).
- Bulk exporting as a single ZIP.

## 15. Acceptance Criteria
1. The user can navigate to the "Exports" tab of a project and see all rendered clips.
2. The user can download the final MP4 video artifact.
3. The user can download `.srt`, `.vtt`, `.txt`, and `.json` subtitle files for a specific rendered clip.
4. The user can click "Retry" on a failed render to re-queue the FFmpeg job.
5. The API enforces tenant isolation and prevents unauthorized file downloads.

## 16. Implementation Sequence
1. Backend Foundation: `export.py` service for subtitle generation.
2. API Layer: `/api/v1/exports.py` and `/retry` endpoint in `render.py`.
3. Frontend Integration: `useExports.ts` hook.
4. UI Layer: `ExportCard.tsx` and `exports/page.tsx`.
5. Testing & Security Verification.

## 17. Verification Gates
- Backend: `cd backend && .venv\Scripts\pytest -q`
- Frontend: `cd frontend && npm test -- --run && npm run lint && npm run build`
- Security: `git grep -i -E "api_key\|apikey\|authorization\|bearer\|secret\|password"`

## 18. Risks
- Standardizing caption formats (VTT vs SRT timecodes). Mitigation: Rely on established timestamp formatting utilities.
- Serving large video files efficiently. Mitigation: FastAPI `FileResponse` streams files efficiently.

## 19. Open Questions
- Should the Gallery be a separate page (`/projects/[projectId]/exports`) or embedded within the existing dashboard? (Plan assumes separate page or tab inside the project view).

## 20. Final Approval Gate
This plan requires explicit user approval before MS-014 implementation begins.
