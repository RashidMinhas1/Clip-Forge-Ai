# MS-011: Lightweight Clip Editor & Framing Engine — Implementation Plan

## 1. Executive Summary
This milestone introduces the **Lightweight Clip Editor & Framing Engine** to Clip Forge AI. It transitions users from the Candidate Clip Review stage (MS-010) into a focused pre-render preparation workspace for individual approved clips. The editor provides intuitive timing adjustments (start/end) and visual framing mode selection (e.g., Face Track 9:16) without the complexity of a full non-linear editor. All changes are persisted securely to the backend.

## 2. Scope

**IN SCOPE:**
- Opening a selected clip/candidate from the project.
- Lightweight clip editing workspace UI.
- Clip preview/player using HTML5 video.
- Timeline representation for the clip.
- Clip start/end adjustment (+/- seconds).
- Playback controls (play, pause, seek).
- Basic clip metadata display.
- Framing/canvas mode selection (Face Track 9:16, Split-Screen, Original).
- Aspect ratio handling in the UI preview.
- Persistence/autosave via debounced API calls.
- Integration with MS-010 candidate review output (Approved Clips).
- Preservation of original source media.

**OUT OF SCOPE:**
- Advanced captions and styling (Reserved for MS-013 Caption Engine).
- Keyframe animation, scale, rotation, and transform controls (Explicitly excluded in PRD for MVP).
- Full rendering pipeline and FFmpeg background execution (Reserved for MS-014).
- Final export system and gallery (Reserved for MS-015).
- Sophisticated effects, transitions, audio mixing, advanced masking.
- AI clip discovery or provider changes.
- Social publishing.
- Unrelated frontend redesign.

## 3. Architecture & Integration
MS-011 integrates directly into the existing Next.js frontend and FastAPI backend.

- **Frontend Routing:** A new route `/projects/[id]/clips/[clip_id]/edit` will serve the editor workspace.
- **Backend APIs:** Existing clipping/project routers will be extended to support patching the `ClipEdit` state.
- **Database:** Reuses the existing `ApprovedClip` and `ClipEdit` models (defined in MS-004/MS-009). No new migrations are anticipated if the schema already supports `start_time`, `end_time`, and `framing_mode`.
- **Background Jobs:** None required. The editor purely modifies database state.
- **Media Playback:** Uses standard HTML5 `<video>` elements streaming the raw source video, utilizing CSS/JS to simulate framing and playback constraints (start/end bounds).

## 4. File Matrix

### Frontend
- **[NEW]** `frontend/src/app/projects/[id]/clips/[clip_id]/edit/page.tsx`: The main editor workspace view.
- **[NEW]** `frontend/src/components/editor/ClipPlayer.tsx`: HTML5 video player restricted to clip bounds.
- **[NEW]** `frontend/src/components/editor/TimelineControls.tsx`: UI for adjusting start/end times.
- **[NEW]** `frontend/src/components/editor/FramingSelector.tsx`: UI for selecting framing modes.
- **[NEW]** `frontend/src/hooks/useClipEditor.ts`: State management and autosave debouncing.
- **[MODIFY]** `frontend/src/lib/api-client.ts`: Add endpoints for fetching/updating single clips.

### Backend
- **[MODIFY]** `backend/app/api/v1/clipping.py`: Add `GET` and `PATCH` endpoints for individual clip edits.
- **[MODIFY]** `backend/app/services/clipping.py`: Add business logic for validating timing adjustments (e.g., start < end, bounds within source duration).
- **[MODIFY]** `backend/app/models/clipping.py` (Schemas): Add `ClipEditUpdate` Pydantic schema for validation.
- **[NEW]** `backend/tests/api/v1/test_editor.py`: Test coverage for the new editor API endpoints.

### Documentation
- **[NEW]** `docs/milestones/milestone-011/milestone-011-plan.md`: This document.

## 5. Data & State Design

**LOCAL UI STATE (React State / Context):**
- `isPlaying`: boolean (Playback state).
- `currentTime`: number (Current playback position).
- `isDirty`: boolean (Tracks un-saved changes for debouncing).
- `isSaving`: boolean (UI indicator for autosave).

**PERSISTED PROJECT STATE (Database):**
- `start_time`: float (Adjusted start time in seconds).
- `end_time`: float (Adjusted end time in seconds).
- `framing_mode`: enum/string (`FACE_TRACK_9_16`, `SPLIT_SCREEN`, `ORIGINAL`).

*Note: No keyframe state or transform scale/rotation state is needed as per the PRD MVP constraints.*

## 6. API Design

**Endpoint:** `GET /api/v1/projects/{project_id}/clips/{clip_id}`
- **Authentication:** Bearer Token.
- **Ownership Check:** Validate that `project_id` belongs to the authenticated user.
- **Response:** `ClipResponse` schema including `start_time`, `end_time`, `framing_mode`, and source video URL.

**Endpoint:** `PATCH /api/v1/projects/{project_id}/clips/{clip_id}/edit`
- **Authentication:** Bearer Token.
- **Ownership Check:** Validate ownership.
- **Request Schema (`ClipEditUpdate`):**
  ```json
  {
    "start_time": 12.5,
    "end_time": 45.0,
    "framing_mode": "FACE_TRACK_9_16"
  }
  ```
- **Validation:** `start_time` must be < `end_time`. `end_time` must not exceed original video duration. `framing_mode` must be a valid enum.
- **Response:** `200 OK` with updated clip schema.

## 7. UI/UX Design
The UI will feature a dark-mode optimized or neutral workspace to focus on the video content:
- **Center:** The video preview player, constrained by the selected aspect ratio (e.g., 9:16).
- **Bottom:** A lightweight timeline showing the relative clip bounds within the source video. Buttons to +/- seconds.
- **Right Panel:** Framing mode selection radio buttons or cards.
- **Top Bar:** Breadcrumb navigation, Auto-save indicator, and "Done" button.

*Note on Local Application UI Verification (Phase 1 Finding):*
During the previous UI integration phase, the local application entry flow was corrected. The root URL (`/`) and `/projects` now serve the actual Clip Forge application UI instead of the generic developer verification screen. The MS-011 Editor will be directly accessible from the candidate list within this established application UI.

## 8. Security
- **Tenant Isolation:** All backend queries for updating clip data MUST include `user_id = current_user.id`.
- **Validation:** Strict Pydantic validation on timing adjustments to prevent negative durations, overlapping boundaries, or exceeding the source video length.
- **Media Access:** The frontend video player will stream media using authenticated pre-signed URLs or secure streaming routes, preventing unauthorized arbitrary filesystem access.
- **No shell execution:** This milestone only modifies database state; no FFmpeg shell commands are executed here.

## 9. Testing Strategy

### Frontend
- **Unit/Component:** Test that timeline boundaries correctly constrain user input.
- **Integration:** Mock API responses to verify debounced autosave behavior triggers correctly when timing changes.

### Backend
- **API Tests:**
  - Verify `PATCH` fails with `403 Forbidden` for a clip owned by another user.
  - Verify `PATCH` fails with `422 Unprocessable Entity` if `start_time` > `end_time`.
  - Verify successful state update and persistence.

### Integration
- **E2E Flow:** Verify navigation from MS-010 Candidate Review -> click "Edit" -> loads MS-011 Editor -> changes persist.

## 10. Verification Strategy
- **Manual Verification:** Open a local video project, select an approved clip, enter the editor, change framing to 9:16, add +2s to start time, refresh the page, and ensure changes persisted.

## 11. Risks & Rollback

- **Risk:** Complex state synchronization between the HTML5 video player and React state leading to infinite loops or jittery playback.
  - *Mitigation:* Use standard React ref patterns for `<video>` control instead of deeply linking video `currentTime` to React state on every frame.
- **Risk:** Excessive API calls from slider scrubbing.
  - *Mitigation:* Implement strict 1000ms debouncing on the autosave function.
- **Risk:** Accidental introduction of scale/rotation/keyframe UI.
  - *Mitigation:* Strict adherence to the PRD which explicitly excludes these from the MVP.
- **Rollback:** Revert the Git branch `milestone/011-lightweight-editor` if major integration issues arise with MS-010.

## 12. Acceptance Criteria
- [ ] Application UI is locally reachable (verified in Phase 1).
- [ ] Selected candidate clip can enter the editor workspace.
- [ ] Clip preview player successfully loads and plays the source video segment.
- [ ] Timeline controls correctly adjust `start_time` and `end_time`.
- [ ] Invalid inputs (negative duration, out of bounds) are rejected by both frontend and backend.
- [ ] Framing mode controls update the UI layout and persist the choice.
- [ ] State remains consistent upon page refresh (autosave works).
- [ ] Authorization and tenant isolation are enforced on all API endpoints.
- [ ] No locked milestone functionality (MS-001 through MS-010) is negatively impacted.
- [ ] Backend tests pass and validate ownership and boundaries.

---

## MS-011 PLANNING STATUS

**Planning:**
COMPLETE

**MS-010:**
LOCKED

**Implementation:**
NOT STARTED

**Implementation Branch:**
NOT CREATED

**Files Created:**
- `docs/milestones/milestone-011/milestone-011-plan.md`
- `implementation_plan.md`

**Files Modified:**
NONE

**Source Code Modified:**
NONE

**Dependencies Installed:**
NONE

**Database Changes:**
NONE

**Frontend Implementation:**
NONE

**UI Entry-Point Finding:**
The frontend entry point was previously corrected during the UI Integration phase. The generic "Developer / Infrastructure Verification UI" was replaced/bypassed. The root (`/`) serves the landing page, and `/projects` serves the redesigned Application Dashboard. The MS-011 editor will naturally extend from `/projects/[id]` without requiring entry-point redirection fixes.

**Architecture Conflicts:**
NONE identified. The editor strictly relies on updating existing database models via standard REST endpoints.

**Scope Risks:**
Risk of over-engineering the HTML5 video player to support complex timelines. Must strictly adhere to "Lightweight Editor" bounds (+/- seconds, framing mode only).

**Open Questions:**
NONE

**Final Verdict:**
READY FOR USER APPROVAL

**NEXT STEP:**
USER REVIEW & EXPLICIT APPROVAL
