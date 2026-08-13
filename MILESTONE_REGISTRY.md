# ClipForge AI — Milestone Registry & Execution Roadmap

> **Status**: ACTIVE (Foundation Phase Verified)  
> **Rule**: No milestone may proceed without explicit implementation plan approval and verification locking.

---

## Milestone Execution Matrix

| Milestone ID | Milestone Name | Goal & Scope Summary | Status | Git Branch |
| :--- | :--- | :--- | :--- | :--- |
| **MS-001** | Foundation & Architecture | Establish development rules, documentation system, architecture blueprint, security policy, git workflow, and templates. | **COMPLETE & VERIFIED** | `milestone/001-foundation` |
| **MS-002** | Project Management & Source Ingestion | User project creation, dashboard setup, local video upload validation, YouTube URL ingestion pipeline. | **PLANNED** | `milestone/002-project-source` |
| **MS-003** | Audio Extraction & Transcription Engine | Background audio extraction, Whisper/AI speech-to-text, segment & word-level timestamp generation, transcript UI. | **PLANNED** | `milestone/003-transcription` |
| **MS-004** | AI Clip Discovery & Vitality Scoring | Intelligent hook analysis, silence detection, vitality scoring, candidate clip generation, review stage (Approve/Regenerate/Cancel). | **PLANNED** | `milestone/004-ai-clipping` |
| **MS-005** | Clip Editor & Visual Framing Engine | Lightweight video editor, trim adjustment controls (+/- 5s), face tracking/speaker intelligence, framing modes (9:16, Split-screen, Original). | **PLANNED** | `milestone/005-editor-framing` |
| **MS-006** | Caption Customization Engine | Caption preset engine (60+ styles), dynamic word-level highlighting, visual word emphasis, RTL support (Arabic/Urdu), per-clip styling preview. | **PLANNED** | `milestone/006-captions` |
| **MS-007** | Background FFmpeg Render Pipeline | Async render job queue, FFmpeg compositing (crop, captions, timing), progress telemetry, output stream integrity validation. | **PLANNED** | `milestone/007-rendering` |
| **MS-008** | Export, Delivery & Persistence | Rendered clip gallery, multi-format download management, project auto-save, end-to-end pipeline verification. | **PLANNED** | `milestone/008-export` |

---

> **Note**: Final product milestone allocation, granular features, and timelines are refined post-PRD approval. Additional milestones may be added as required by product requirements.

---

## Milestone Execution Lifecycle
- `PLANNING`: Creating milestone implementation plan (`/docs/milestones/milestone-XXX/milestone-XXX-plan.md`).
- `ANALYSIS`: Requirement & subsystem impact analysis.
- `FEATURE AGENT`: Creating/updating feature agent specs (`/docs/features/FEATURE_NAME.agent.md`).
- `USER APPROVAL`: Plan and feature specs approved by user.
- `MILESTONE BRANCH`: Creating isolated branch (`milestone/XXX-name`).
- `IMPLEMENTATION`: Writing code and unit tests.
- `TESTING & VERIFICATION`: Executing functional, security, media, and UI tests.
- `VERIFICATION REPORT`: Generating formal audit report (`milestone-XXX-verification-report.md`).
- `LOCKED`: User final sign-off, pushed to GitHub, merged to main, milestone closed.
