# ClipForge AI — Decision Log (Architecture Decision Records)

> **Status**: ACTIVE  
> **Format**: ADR (Architecture Decision Record) Standard  

---

## ADR-001: Selection of Modular Monolith Architecture
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Early-stage application needs low operational complexity, fast iteration, high maintainability, and clean subsystem separation for media/AI workloads.
- **Decision**: Adopt a Modular Monolith structure. Keep FastAPI backend and Next.js frontend clean, well-isolated by modules, without deploying complex microservices micro-overhead initially.
- **Consequences**: Easy local development via Docker Compose; clear subsystem boundaries allow extracting heavy rendering workers later if high scaling requires it.

---

## ADR-002: Selection of Python (FastAPI) as Core Backend Platform
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: ClipForge AI relies heavily on computer vision (face/speaker intelligence), audio processing (silence detection, Whisper speech-to-text), LLM structured output parsing, and FFmpeg filter manipulation.
- **Decision**: Select Python (FastAPI) as the backend framework over Node.js and Go.
- **Consequences**: Grants native access to top-tier AI/ML packages (PyTorch, OpenAI, MediaPipe, OpenCV, Whisper) while maintaining asynchronous web throughput via FastAPI and asyncio.

---

## ADR-003: Multi-Provider AI Abstraction Layer
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Relying strictly on a single AI provider risks vendor lock-in, rate limiting outages, and price fluctuations.
- **Decision**: Architect an AI Router with provider adapters supporting OpenAI, Google Gemini, OpenRouter, and local LLM backends. Enforce server-side schema validation via Pydantic on all LLM responses.
- **Consequences**: Application code is decoupled from underlying AI models; credentials remain server-side; prompt templates are version-controlled.

---

## ADR-004: Mandatory Feature `.agent.md` Specification Architecture
- **Date**: 2026-08-13
- **Status**: APPROVED
- **Context**: Large complex AI video processing applications require strict behavioral specs for each feature to prevent hallucinated behaviors, broken API contracts, or silent regression.
- **Decision**: Enforce that every major technical feature MUST have a standalone spec file in `docs/features/FEATURE_NAME.agent.md` defining inputs, schemas, business logic, processing rules, error handling, forbidden behaviors, and acceptance criteria.
- **Consequences**: AI agents and developers have an unambiguous source of truth for feature implementations. Behavioral changes require explicit spec updates and re-approval.
