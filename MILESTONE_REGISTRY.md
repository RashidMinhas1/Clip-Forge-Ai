# ClipForge AI — Milestone Registry & Execution Roadmap

> **Status**: ACTIVE (Foundation Phase Verified)
> **Rule**: No milestone may proceed without explicit implementation plan approval and verification locking.

---

## Milestone Execution Matrix

| Milestone ID | Milestone Name | Goal & Scope Summary | Status | Git Branch |
| :--- | :--- | :--- | :--- | :--- |
| **MS-001** | Foundation & Architecture | Establish development rules, documentation system, architecture blueprint, security policy, git workflow, and templates. | **COMPLETED & LOCKED** | `milestone/001-foundation` |
| **MS-002** | Application Runtime & Infrastructure | Next.js & FastAPI runtimes, Docker integration, base configuration, health endpoints, logging, testing foundation, basic UI shell. | **VERIFICATION PASS — AWAITING MERGE & LOCK** | `milestone/002-application-runtime-infrastructure` |
| **MS-003** | Source Ingestion & Validation | Local upload, YouTube URL ingestion, FFmpeg probing, metadata extraction, secure StorageDriver. | **COMPLETED & LOCKED** | `milestone/003-source-ingestion-validation` |
| **MS-004** | Database Schema & Persistence | PostgreSQL async engine, SQLAlchemy models, Alembic migrations, project/user ownership, auto‑save, resume capability. | **PLANNED** | `milestone/004-database-persistence` |
| **MS-005** | Transcription Service | faster‑whisper integration (multi‑model strategy), multilingual support, word‑level timestamps, optional OpenAI Whisper fallback under FREE‑FIRST policy, UI transcript view. | **COMPLETED &amp; LOCKED** | `milestone/005-transcription-service` |
| **MS-006** | AI Provider Abstraction | Central AI Router, provider/interface contracts, request/response normalization, Pydantic schema validation, FREE‑ONLY & FREE‑FIRST policies, telemetry. | **PLANNED** | `milestone/006-ai-abstraction` |
| **MS-007** | Ollama Local AI Integration | Adapter for local Ollama models, health checks, model discovery, JSON response handling, graceful fallback per policy. | **PLANNED** | `milestone/007-ollama` |
| **MS-008** | OpenRouter Free Model Routing | Secure OpenRouter integration, dynamic free‑model discovery, capability matching, pricing validation, retry & fallback logic, telemetry. | **PLANNED** | `milestone/008-openrouter-free` |
| **MS-009** | AI Clip Discovery & Vitality Scoring | Prompt design, multi‑dimensional scoring, explainable VitalityScore, duplicate avoidance, confidence handling. | **COMPLETED & LOCKED** | `milestone/009-ai-clip-discovery` |
| **MS-010** | Clip Review & Selection UI | Functional preview of AI candidates, vitality display, justification, actions (Approve / Regenerate / Cancel), persistence of selection state. | **COMPLETED & LOCKED** | `milestone/010-candidate-review-ui` |
| **MS-011** | Lightweight Editor & Framing Engine | Video preview, clip list, timing adjustments, undo/redo, framing modes (Face‑Track, Split‑Screen, Split + Gameplay, Split + Human Reaction, Original). | **COMPLETED & LOCKED** | `milestone/011-lightweight-clip-editor` |
| **MS-012** | Caption Engine | 60+ style presets, RTL support, live preview, per‑clip independent configuration, word‑highlight, visual emphasis. | **PLANNED** | `milestone/012-captions` |
| **MS-013** | Rendering Pipeline | Asynchronous FFmpeg render via Taskiq + Redis, state machine (QUEUED → PROCESSING → COMPLETED / FAILED / CANCELLED), output validation, temporary artifact cleanup. | **PLANNED** | `milestone/013-rendering` |
| **MS-014** | Export & Gallery | Rendered clip gallery, download endpoints, metadata persistence, retry handling, UI integration. | **PLANNED** | `milestone/014-export` |
| **MS-015** | Security Hardening & Audit | Full authentication/authorization, tenant isolation, rate limiting, CORS, security headers, secret management, file‑access safeguards, audit reporting. | **PLANNED** | `milestone/015-security` |
| **MS-016** | Testing Infrastructure & Cross‑Cutting Tests | Unit, API, integration, UI, E2E, media, AI, security, regression, performance suites; test scaffolding established early (MS‑002) and extended throughout. | **PLANNED** | `milestone/016-testing` |
| **MS-017** | End‑to‑End MVP Verification & Release | Complete real‑world workflow verification (dashboard → export) with functional, UI, backend, DB, AI, media, security, regression, performance checks; generate verification report. | **PLANNED** | `milestone/017-mvp-verification` |
| **MS-018** | Post‑MVP Planning (Future Extensions) | Placeholder for future multi‑track editor, overlays, social publishing, paid‑provider fallback, advanced media effects; planning only, no implementation. | **PLANNED** | `milestone/018-post-mvp` |

---

### Deferred/Skipped Features
- **Manual Clipping Engine**: Originally planned prior to AI Clip Discovery, but deferred/skipped. It does not alter the numbering of already-locked milestones.

### Cross‑Cutting Concerns
- **Security**: Integrated security considerations are included in every milestone (authentication, authorization, secret handling, file access). The final hardening audit occurs in MS‑016.
- **Testing**: A test plan is defined for each milestone; the overarching testing framework is established in MS‑017 and continuously applied.
- **Feature Agents**: Each functional milestone will produce a corresponding `docs/features/FEATURE_NAME.agent.md` specification during the PLANNING stage.

*Prepared by Antigravity – your AI‑augmented software architect.*
