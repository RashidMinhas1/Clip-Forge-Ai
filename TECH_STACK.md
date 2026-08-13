# ClipForge AI — Technology Stack & Infrastructure Architecture

> **Status**: LOCKED (Foundation Phase)  
> **Evaluation**: Comprehensive technical evaluation completed for high-performance AI video processing.

---

## 1. System Technology Matrix

| Layer | Selected Technology | Rationale & Trade-off Evaluation |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js (React 19+, TypeScript)** | App Router, Server Components, SSR/SSG capabilities, fast client navigation, robust TypeScript type safety. |
| **UI Components & Styling** | **Tailwind CSS + shadcn/ui** | Utility-first responsive styling, accessible unstyled primitives (Radix UI), customizable component foundation without unnecessary code bloat. |
| **Backend API Framework** | **Python (FastAPI)** | Asynchronous non-blocking I/O (`asyncio`), native integration with AI/ML ecosystems (PyTorch, Whisper, OpenCV, MediaPipe), Pydantic request/response schema validation, OpenAPI docs auto-generation. |
| **Database & ORM** | **PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic** | Enterprise-grade relational DB, JSONB support for complex video/transcript metadata, robust transactional security, schema versioning via Alembic. |
| **Background Processing** | **Redis + Taskiq / Celery** | Distributed asynchronous task queue for heavy long-running operations (video download, audio extraction, transcription, rendering, AI scoring). |
| **Media Processing Engine** | **FFmpeg (CLI & Python wrapper)** | Industry-standard high-performance video/audio demuxing, decoding, encoding, filter graph manipulation (framing, split-screen, captions rendering). |
| **AI Routing & Intelligence** | **Multi-Provider AI Router (OpenAI / Gemini / OpenRouter / Local LLMs)** | Vendor-agnostic provider abstraction layer with Pydantic structured output validation, token usage tracking, and automated retry mechanisms. |
| **Storage Abstraction** | **S3-Compatible Object Storage (MinIO local / AWS S3 prod)** | Unified storage driver interface supporting local filesystem for dev and cloud object storage for production. |
| **Containerization** | **Docker & Docker Compose** | Reproducible multi-container runtime environment for FastAPI, Next.js, PostgreSQL, Redis, and FFmpeg workers. |

---

## 2. Technical Evaluation & Architecture Validation

### 2.1 Backend Framework Decision (FastAPI vs Node.js vs Go)
- **Node.js/TypeScript**: Excellent for web APIs, but lacks native deep-learning ecosystem bindings for advanced clip intelligence, Whisper transcription processing, computer vision (face/speaker detection), and heavy media manipulations.
- **Go**: High throughput, but weak ecosystem for AI model integration and computer vision pipelines.
- **Python (FastAPI)**: Selected as the primary backend engine because AI/ML clip discovery, transcription segmenting, silence detection, visual subject tracking, and LLM structured prompt pipelines are central to ClipForge AI. FastAPI provides async web throughput comparable to Node.js while keeping AI/ML integration native.

### 2.2 UI Design System Strategy
- **shadcn/ui** provides standard accessible primitives (Dialogs, Dropdowns, Progress bars, Sliders, Tabs, Sheet sidebars).
- Custom video playback, transcript sync, caption style customization, and visual framing preview controls will be layered cleanly on top of Tailwind CSS design tokens.

---

## 3. Storage & Media Abstraction Layer Architecture

```
                 +-----------------------------------+
                 | Storage Service Interface (Driver)|
                 +-----------------------------------+
                                   |
                  +----------------+----------------+
                  |                                 |
       +--------------------+             +--------------------+
       | LocalStorageDriver |             |   S3StorageDriver  |
       | (Development Mode) |             | (Production AWS)   |
       +--------------------+             +--------------------+
```

All media operations (uploading raw video, storing extracted audio, storing generated thumbnails, saving rendered clips) MUST execute through a unified abstract storage class (`StorageDriver`), ensuring ZERO hardcoded cloud or filesystem paths in application business logic.
