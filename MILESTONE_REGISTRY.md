# ClipForge AI — Milestone Registry & Execution Roadmap

> **Status**: ACTIVE (Foundation Phase Verified)
> **Rule**: No milestone may proceed without explicit implementation plan approval and verification locking.

---

## Milestone Execution Matrix

| Milestone ID | Milestone Name | Goal & Scope Summary | Status | Git Branch |
| :--- | :--- | :--- | :--- | :--- |
| **MS-001** | Foundation & Architecture | Establish development rules, documentation system, architecture blueprint, security policy, git workflow, and templates. | **COMPLETED & LOCKED** | `milestone/001-foundation` |
| **MS-002** | Application Runtime & Infrastructure | Next.js & FastAPI runtimes, Docker integration, base configuration, health endpoints, logging, testing foundation, basic UI shell. | **VERIFICATION PASS — AWAITING MERGE & LOCK** | `milestone/002-application-runtime-infrastructure` |
| **MS-003** | Database & Project Persistence | PostgreSQL async engine, SQLAlchemy models, Alembic migrations, project/user ownership, auto‑save, resume capability. | **PLANNED** | `milestone/003-database-persistence` |
| **MS-004** | Source Ingestion & Validation | Local upload, YouTube URL ingestion, FFmpeg probing, metadata extraction, secure StorageDriver, background job handling. | **PLANNED** | `milestone/004-source-ingestion` |
| **MS-005** | Transcription Service | faster‑whisper integration (multi‑model strategy), multilingual support, word‑level timestamps, optional OpenAI Whisper fallback under FREE‑FIRST policy, UI transcript view. | **PLANNED** | `milestone/005-transcription` |
| **MS-006** | AI Provider Abstraction | Central AI Router, provider/interface contracts, request/response normalization, Pydantic schema validation, FREE‑ONLY & FREE‑FIRST policies, telemetry. | **PLANNED** | `milestone/006-ai-abstraction` |
| **MS-007** | Ollama Local AI Integration | Adapter for local Ollama models, health checks, model discovery, JSON response handling, graceful fallback per policy. | **PLANNED** | `milestone/007-ollama` |
| **MS-008** | OpenRouter Free Model Routing | Secure OpenRouter integration, dynamic free‑model discovery, capability matching, pricing validation, retry & fallback logic, telemetry. | **PLANNED** | `milestone/008-openrouter-free` |
| **MS-009** | Manual Clipping Engine | Silence‑aware target clipping (30 s / 60 s / 90 s) for local & YouTube sources, intelligent boundary selection, extensive test matrix. | **PLANNED** | `milestone/009-manual-clipping` |
| **MS-010** | AI Clip Discovery & Vitality Scoring | Prompt design, multi‑dimensional scoring, explainable VitalityScore, duplicate avoidance, confidence handling. | **PLANNED** | `milestone/010-ai-clipping` |
| **MS-011** | Clip Review & Selection UI | Functional preview of AI candidates, vitality display, justification, actions (Approve / Regenerate / Cancel), persistence of selection state. | **PLANNED** | `milestone/011-clip-review` |
| **MS-012** | Lightweight Editor & Framing Engine | Video preview, clip list, timing adjustments, undo/redo, framing modes (Face‑Track, Split‑Screen, Split + Gameplay, Split + Human Reaction, Original). | **PLANNED** | `milestone/012-editor-framing` |
| **MS-013** | Caption Engine | 60+ style presets, RTL support, live preview, per‑clip independent configuration, word‑highlight, visual emphasis. | **PLANNED** | `milestone/013-captions` |
| **MS-014** | Rendering Pipeline | Asynchronous FFmpeg render via Taskiq + Redis, state machine (QUEUED → PROCESSING → COMPLETED / FAILED / CANCELLED), output validation, temporary artifact cleanup. | **PLANNED** | `milestone/014-rendering` |
| **MS-015** | Export & Gallery | Rendered clip gallery, download endpoints, metadata persistence, retry handling, UI integration. | **PLANNED** | `milestone/015-export` |
| **MS-016** | Security Hardening & Audit | Full authentication/authorization, tenant isolation, rate limiting, CORS, security headers, secret management, file‑access safeguards, audit reporting. | **PLANNED** | `milestone/016-security` |
| **MS-017** | Testing Infrastructure & Cross‑Cutting Tests | Unit, API, integration, UI, E2E, media, AI, security, regression, performance suites; test scaffolding established early (MS‑002) and extended throughout. | **PLANNED** | `milestone/017-testing` |
| **MS-018** | End‑to‑End MVP Verification & Release | Complete real‑world workflow verification (dashboard → export) with functional, UI, backend, DB, AI, media, security, regression, performance checks; generate verification report. | **PLANNED** | `milestone/018-mvp-verification` |
| **MS-019** | Post‑MVP Planning (Future Extensions) | Placeholder for future multi‑track editor, overlays, social publishing, paid‑provider fallback, advanced media effects; planning only, no implementation. | **PLANNED** | `milestone/019-post-mvp` |

---

### Cross‑Cutting Concerns
- **Security**: Integrated security considerations are included in every milestone (authentication, authorization, secret handling, file access). The final hardening audit occurs in MS‑016.
- **Testing**: A test plan is defined for each milestone; the overarching testing framework is established in MS‑017 and continuously applied.
- **Feature Agents**: Each functional milestone will produce a corresponding `docs/features/FEATURE_NAME.agent.md` specification during the PLANNING stage.

*Prepared by Antigravity – your AI‑augmented software architect.*
