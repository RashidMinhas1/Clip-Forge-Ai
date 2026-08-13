# ClipForge AI — Decision Log (Architecture Decision Records)

> **Status**: ACTIVE  
> **Format**: ADR (Architecture Decision Record) Standard  

---

## ADR-001: Selection of Python (FastAPI) as Core Backend Platform
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: ClipForge AI relies heavily on computer vision (face/speaker intelligence), audio processing (silence detection, Whisper speech-to-text), LLM structured output parsing, and FFmpeg filter manipulation.
- **Decision**: Select Python (FastAPI) as the backend framework over Node.js and Go.
- **Consequences**: Grants native access to top-tier AI/ML packages (PyTorch, OpenAI, MediaPipe, OpenCV, Whisper) while maintaining asynchronous web throughput via FastAPI and `asyncio`.

---

## ADR-002: Selection of PostgreSQL as Primary Database
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Transactional reliability, robust JSONB support for complex video/transcript metadata, and multi-tenant user project isolation are required.
- **Decision**: Select PostgreSQL with SQLAlchemy 2.0 Async ORM and Alembic migration management.
- **Consequences**: Provides reliable relational data modeling and native JSON querying capabilities.

---

## ADR-003: Selection of Taskiq + Redis for Background Jobs
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Heavy async operations (video downloading, audio extraction, speech recognition, AI clip analysis, FFmpeg rendering) must not block API HTTP worker threads.
- **Decision**: Select Taskiq + Redis as the primary background task processing system over Celery.
- **Consequences**: Provides a Python `asyncio`-native task queue with native FastAPI dependency injection, eliminating heavy Celery configuration overhead. Remains replaceable if future scale requires another queue driver.

---

## ADR-004: Selection of FFmpeg as Media Processing Engine
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: High-performance video crop framing, audio extraction, clip trimming, dynamic subtitle burning, and rendering compositing are essential core features.
- **Decision**: Adopt FFmpeg (CLI & Python wrapper) as the underlying media processing engine.
- **Consequences**: Provides industry-standard media manipulation capabilities with zero external cloud video rendering SaaS vendor lock-in.

---

## ADR-005: Selection of Modular Monolith Architecture
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Early-stage application requires low operational overhead, rapid development velocity, clean code isolation, and high maintainability without premature microservice complexity.
- **Decision**: Adopt a Modular Monolith architecture pattern (`Next.js + FastAPI + PostgreSQL + Redis + Taskiq + FFmpeg`).
- **Consequences**: Simplifies local development via Docker Compose and enables extracting heavy background workers into independent micro-services if extreme future scale requires it.

---

## ADR-006: Selection of Application-Level Tenant Authorization
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Multi-tenant user isolation is critical for user video privacy. Every database entity must strictly belong to an authenticated user.
- **Decision**: Implement Application-Level Tenant Authorization enforcing `WHERE user_id = authenticated_user.id` on all database operations and service handlers.
- **Consequences**: Ensures strict multi-tenant boundary checks in application code across Projects, Sources, Videos, Transcripts, Clips, Edits, Captions, Renders, Exports, and AI Jobs.

---

## ADR-007: Reservation of PostgreSQL Row-Level Security (RLS) for Future Evaluation
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Evaluating potential future defense-in-depth security layers without adding premature database setup friction during early development.
- **Decision**: Document PostgreSQL Row-Level Security (RLS) as a potential future defense-in-depth layer while relying on verified Application-Level Authorization as the active security boundary.
- **Consequences**: Keeps database migrations simple while preserving clear technical roadmap for future database-level security policy evaluation.

---

## ADR-008: Selection of shadcn/ui + Tailwind CSS for UI Foundation
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Need a modern, premium, highly responsive UI design system with accessible primitives and customizable dynamic aesthetics.
- **Decision**: Select shadcn/ui (Radix UI unstyled primitives) paired with Tailwind CSS styling tokens.
- **Consequences**: Eliminates bloated third-party UI framework restrictions while giving full control over video editing and preview components.

---

## ADR-009: MS-002 Docker Verification Environmental Exception
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: During MS-002 verification, Docker Desktop was unavailable on the verification host. All application-level tests (pytest 4/4, FastAPI runtime, health/readiness endpoints, frontend ESLint, Vitest, Next.js build, security audit, scope audit) passed. Only Docker container orchestration checks could not be executed.
- **Decision**: Classify the MS-002 verification result as `PASS WITH ENVIRONMENTAL EXCEPTION`. The application implementation is verified correct. Docker container verification is documented as BLOCKED — ENVIRONMENT and does not constitute an application defect.
- **Consequences**: Docker-specific runtime checks (container networking, Redis/PostgreSQL containers) remain unexecuted in the local environment. These may be verified in a CI environment (GitHub Actions) which provisions Docker automatically. No application code changes were made to compensate for Docker's absence.
