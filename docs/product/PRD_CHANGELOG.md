# ClipForge AI — PRD Change Log

> **Document Location**: `/docs/product/PRD_CHANGELOG.md`  
> **Status**: ACTIVE  

---

## [0.1.0] — 2026-08-13
### Added
- Initial Product Requirements Document (PRD) Draft (`/docs/product/PRD.md`).
- Detailed product vision, core product principles, and target user personas (YouTubers, Podcasters, Social Creators, Agencies, Freelancers, Beginners, Viral Clip Hunters, Manual Control Enthusiasts).
- Complete 17-stage user workflow map from Dashboard to Export.
- Functional specifications for Manual Clipping (30/60/90s silence-aware target clipping) and AI Clipping (Hook, curiosity, emotional impact, standalone context, vitality scoring).
- Explainable Vitality Score calculation methodology and reasoning framework.
- Multilingual speech-to-text transcription engine specification using `faster-whisper` (Primary Local) and OpenAI Whisper (Cloud Fallback) with RTL support (Urdu, Arabic, Persian).
- Free-First AI Architecture specifications incorporating Ollama local models and dynamic OpenRouter free-model discovery with `FREE-ONLY` and `FREE-FIRST` zero-cost routing policies.
- Lightweight Clip Editor spec featuring independent clip state, timing adjustments (+/- 5s), visual framing modes (Face Track 9:16, Split Screen, Original), and dynamic caption preset library (60+ styles).
- Video processing pipeline blueprint using FFmpeg, MediaPipe/OpenCV face tracking, and Taskiq + Redis background job orchestration.
- Vizard AI competitive analysis breakdown (KEEP, IMPROVE, ADAPT, FUTURE, OUT OF SCOPE).
- Comprehensive acceptance criteria, edge case handling, telemetry observability, and testing requirements.
