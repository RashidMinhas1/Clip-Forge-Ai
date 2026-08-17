# MS-012 — Caption Engine

## 1. Objective
To introduce the Caption Engine, responsible for translating pre-existing word-level transcript data into dynamic, styled, clip-relative subtitles for approved short-form clips. This milestone bridges the gap between text transcripts and visually engaging, ready-to-render captions.

## 2. Authoritative References
- **PRD**: Stage 12 (Caption Styling Engine), Section 16 (Dynamic Caption Preset Engine).
- **MILESTONE_REGISTRY.md**: MS-012 (Caption Engine).
- **ARCHITECTURE.md**: Subsystem boundaries for framing and rendering.

## 3. Existing System Dependencies
- **Transcription Subsystem (MS-005)**: Provides `TranscriptSegment` and `TranscriptWord` models.
- **Project/Source Subsystem (MS-003/MS-004)**: Ownership and relationship mappings.
- **Lightweight Editor (MS-011)**: The base UI environment where the caption overlay and styling panel will be integrated.

## 4. Scope
### INCLUDED
- Transcript-to-caption conversion using deterministic slicing.
- Word and segment timing translation (relative to clip).
- Caption styling configuration (presets, colors, typography).
- Live UI preview of captions overlaid on the MS-011 video player.
- Persistence of per-clip caption configurations.
- Multilingual and native RTL (Right-to-Left) rendering support for the UI preview.

## 5. Non-Goals
### EXCLUDED
- Final video rendering / FFmpeg subtitle burn-in (Reserved for MS-013 Rendering Pipeline).
- Export formats / SRT or VTT file generation (Reserved for MS-014 Export & Gallery).
- Direct text editing or AI-rewriting of the transcript.
- Advanced keyframe animation, scale, rotation, audio mixing, or masks.

## 6. User Flow
1. User opens an approved clip in the MS-011 Editor.
2. The UI fetches dynamically sliced captions for the clip's duration.
3. The video player displays a `CaptionOverlay` rendering the text in sync with playback.
4. User opens the "Captions" side panel to choose a preset (e.g., "Bold Yellow Glow") and adjusts colors/fonts.
5. The UI updates instantly, and changes are debounced and saved to the backend via `PATCH`.

## 7. Backend Design
The backend extracts captions on-the-fly without copying transcript data. 
- A service queries the existing `TranscriptWord` table filtering by `source_id` and the clip's `start_time` and `end_time`.
- Words are grouped into logical presentation chunks (e.g., 5-7 words) or by punctuation.
- Timestamps are normalized so `t=0` corresponds to the start of the clip.
- Configurations are saved independently in a new `ClipCaptionConfig` table.

## 8. Caption Data Model
**DATABASE CHANGES: REQUIRED**

New Table: `clip_caption_configs`
- `id`: UUID (Primary Key)
- `clip_id`: UUID (Foreign Key to `clip_candidates.id`, ON DELETE CASCADE)
- `preset_name`: String (Default: "tiktok_modern")
- `font_family`: String (Nullable)
- `font_size`: Integer (Nullable)
- `text_color`: String (Nullable)
- `highlight_color`: String (Nullable)
- `bg_color`: String (Nullable)
- `is_rtl`: Boolean (Default: False)

## 9. API Contract
**GET `/api/v1/projects/{project_id}/clips/{clip_id}/captions`**
- Purpose: Retrieve dynamic, clip-relative caption chunks and the current configuration.
- Validation: Validates `project_id` ownership. Ensures `clip_id` exists.
- Response: Array of caption chunks with relative start/end times and word-level timings, plus the config object.

**PATCH `/api/v1/projects/{project_id}/clips/{clip_id}/caption-config`**
- Purpose: Update the styling configuration for a clip.
- Validation: Pydantic schemas reject malicious input (e.g., HTML/JS in font strings).
- Request: Partial updates to `preset_name`, `text_color`, etc.
- Response: Updated configuration object.

## 10. Caption Processing Pipeline
- Query: `SELECT * FROM transcript_words WHERE source_id = ? AND start_time >= ? AND end_time <= ? ORDER BY word_index ASC`
- Boundary overlapping: Words spanning the `start_time` or `end_time` by >30% overlap are included and their relative times are clamped.
- No AI provider dependencies are invoked in this pipeline.

## 11. Frontend Design
- **Entry Point**: `frontend/src/app/projects/[id]/clips/[clip_id]/edit/page.tsx`
- **CaptionStylePanel**: A new tab in the editor controls area for applying presets and modifying colors.
- **CaptionOverlay**: An absolute-positioned transparent layer inside `ClipPlayer.tsx`. Subscribes to the HTML5 video `currentTime` ref to highlight the active word without triggering heavy React component re-renders.
- **Responsiveness**: Captions scale relative to the container width.

## 12. Transcript Integration
- Strictly reads from MS-005 tables (`transcripts`, `transcript_segments`, `transcript_words`).
- Does NOT duplicate transcripts.
- Does NOT introduce another speech-to-text provider.

## 13. Multilingual & RTL Support
- Directionality is detected server-side by checking characters against Unicode RTL blocks (Arabic, Urdu, Persian).
- If detected, `is_rtl = True` is sent to the frontend.
- Frontend applies `dir="rtl"` to the caption container, allowing browser text-shaping engines to handle ligatures and ordering correctly.

## 14. Persistence
- Caption configs persist instantly via debounced API calls.
- Configurations are bound to `clip_candidates`. If a candidate is rejected or regenerated, its `clip_caption_configs` record is purged via cascade delete.

## 15. Testing Strategy
### Backend
- Slicing service tests verifying correct chunking and relative timestamp math.
- API tests asserting 403 on tenant isolation violations.
### Frontend
- Component tests verifying overlay displays active words correctly at mock `currentTime`s.
- RTL rendering verification.
### Regression
- Verify MS-005 transcript ingestion remains unaffected.
- Verify MS-011 manual timing adjustments correctly propagate to the new caption boundaries.

## 16. Security
- Application-level tenant isolation enforced on all endpoints: `WHERE user_id = current_user.id`.
- Pydantic validation strictly typed to prevent injection attacks via color strings or font families.
- Verification command `git grep -i -E "api_key|apikey|authorization|bearer|secret|password"` will be run before lock to ensure no credentials leaked.

## 17. Performance
- Slicing is highly performant via database indices on `source_id` and `start_time`.
- Frontend utilizes `requestAnimationFrame` or ref-polling to sync captions to video playback, avoiding React state thrashing and stutter.

## 18. Regression Protection
- The MS-011 Editor UI will be extended, NOT rewritten. Existing framing modes and timeline controls will remain intact.
- The MS-005 Transcript system will not be modified.

## 19. File Change Matrix
| File | Action | Reason | MS-012 Scope |
|------|--------|--------|--------------|
| `backend/app/db/models.py` | Modify | Add `ClipCaptionConfig` model | Yes |
| `backend/alembic/versions/..._captions.py` | Create | DB migration | Yes |
| `backend/app/models/captions.py` | Create | Pydantic schemas | Yes |
| `backend/app/services/captions.py` | Create | Slicing logic | Yes |
| `backend/app/api/v1/captions.py` | Create | API endpoints | Yes |
| `frontend/src/components/editor/CaptionOverlay.tsx` | Create | Live UI preview | Yes |
| `frontend/src/components/editor/CaptionStylePanel.tsx` | Create | Styling UI | Yes |
| `frontend/src/app/projects/[projectId]/clips/[clipId]/edit/page.tsx` | Modify | Add panel to layout | Yes |
| `frontend/src/components/editor/ClipPlayer.tsx` | Modify | Mount overlay | Yes |
| `backend/app/api/v1/clipping.py` | Forbidden | Do not rewrite clipping | No |
| `backend/app/services/transcription.py` | Forbidden | Transcription is locked | No |

## 20. Acceptance Criteria
1. Clip-relative captions are dynamically derived without duplicating transcript data.
2. The UI correctly previews captions synchronized with video playback.
3. The UI highlights the active spoken word.
4. Users can select and save caption styling presets.
5. Urdu/Arabic clips automatically render with proper RTL Unicode handling.
6. Security checks confirm tenant isolation and absence of leaked credentials.

## 21. Implementation Order
1. DB Model & Alembic Migration.
2. Pydantic Schemas & Backend Slicing Service.
3. FastAPI Endpoints + API Tests.
4. Frontend `CaptionStylePanel` + API Hooks.
5. Frontend `CaptionOverlay` + Video Synchronization.

## 22. Explicit Scope Lock
### INCLUDED
- Caption extraction, timing translation, styling persistence, live UI preview, RTL handling.
### EXCLUDED
- MS-011 editor rewrites, timeline redesign, audio editing.
- MS-013 FFmpeg rendering pipeline.
- MS-014 Export system.
- Deferred Manual Clipping Engine.

## 23. Risks & Mitigations
- **Risk**: Caption rendering lags behind the video causing desynchronization.
- **Mitigation**: Bind overlay updates to HTML5 `timeupdate` events or `requestAnimationFrame` instead of global React context state.

## 24. Final Governance Gate
READY FOR USER APPROVAL
