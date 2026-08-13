# ClipForge AI — Product Requirements Document (PRD)

> **Document Version**: 0.1.0 (DRAFT)  
> **Status**: PENDING USER REVIEW & APPROVAL  
> **Target Audience**: Product Managers, Software Architects, Engineering Lead, UX Architects, QA Leads  
> **Document Location**: `/docs/product/PRD.md`  

---

## 1. Executive Summary

**ClipForge AI** is a professional, AI-powered long-form to short-form video repurposing platform. It bridges advanced AI automation with granular human control, allowing creators to rapidly extract viral, high-engagement short video clips (TikTok, YouTube Shorts, Instagram Reels) from long-form content (podcasts, interviews, webinars, gaming, educational lectures).

The system operates on a **Free-First AI Architecture**, utilizing local zero-cost models (`faster-whisper`, `Ollama`, `FFmpeg`, `MediaPipe`, `Taskiq + Redis`) alongside dynamic free cloud models (`OpenRouter`) to eliminate mandatory paid API dependencies for MVP users.

---

## 2. Problem Statement

Creating short-form clips from long-form video content manually is an excruciating, time-consuming process requiring creators to:
1. Manually watch hours of video to identify high-hook moments.
2. Manually scrub timelines to set cut points without interrupting speech.
3. Manually crop horizontally framed videos into vertical 9:16 aspect ratios while tracking active speakers.
4. Manually transcribe, time-sync, style, and visually highlight dynamic subtitles word-by-word.

Existing commercial SaaS tools (e.g., Vizard AI, Opus Clip) are often expensive, lock users into strict monthly credit limits, depend exclusively on paid cloud APIs, leak user privacy, and offer weak manual control when AI clip boundaries require fine-tuning.

---

## 3. Product Vision

ClipForge AI provides a seamless, beginner-friendly yet highly professional workflow that turns long-form video into polished, caption-ready vertical short clips in minutes.

```
LONG-FORM VIDEO (Local Upload / YouTube URL)
        ↓
SOURCE PROCESSING & SILENCE DETECTION
        ↓
MULTILINGUAL TRANSCRIPTION (faster-whisper / Whisper Cloud)
        ↓
MANUAL (30/60/90s) OR AI CLIP DISCOVERY
        ↓
CANDIDATE CLIP REVIEW (Approve / Regenerate / Cancel)
        ↓
LIGHTWEIGHT EDITOR & VISUAL FRAMING (9:16 Face Track / Split)
        ↓
CAPTION ENGINE (60+ Presets, Word Highlights, RTL Support)
        ↓
BACKGROUND FFmpeg RENDERING (Taskiq + Redis)
        ↓
EXPORT & DOWNLOAD GALLERY
```

---

## 4. Goals

1. **AI Automation + Human Oversight**: Deliver automated AI clip discovery with explainable Vitality Scores, while giving users intuitive lightweight controls to tweak clip boundaries, framing, and subtitle styling.
2. **Free-First AI Cost Control**: Provide full end-to-end functionality using open-source, local, or free AI providers (`faster-whisper`, `Ollama`, `OpenRouter free models`) with zero mandatory credit card requirement for core MVP features.
3. **Multilingual & RTL Support**: Support global speech recognition and caption rendering across English, Urdu, Arabic, Persian, and major international languages with native Right-to-Left text handling.
4. **Project Persistence & Auto-Save**: Ensure users can leave the app and resume work seamlessly without losing transcript edits, framing choices, or approved clip configurations.
5. **Architectural Efficiency**: Maintain a lightweight modular monolith (`Next.js + FastAPI + PostgreSQL + Redis + Taskiq + FFmpeg`) providing instant UI responsiveness and background job telemetry without microservice overhead.

---

## 5. Non-Goals (Out of Scope for MVP)

- **Not a Premiere Pro / CapCut Replacement**: MVP will NOT feature multi-track NLE timelines, keyframe animation, scale/rotation transform controls, video masks, or complex color grading.
- **No Direct Social Publishing**: Direct API publishing to TikTok, YouTube, or Instagram is excluded from MVP; users export rendered MP4 artifacts directly.
- **No Automated Paid API Fallbacks**: The system will NEVER automatically route requests to paid AI providers without explicit user setup and consent.

---

## 6. Target Users & Personas

### Persona 1: YouTube Content Creator ("Alex", 100k Subscribers)
- **Goal**: Repurpose 45-minute YouTube video essays into 5 viral YouTube Shorts per week.
- **Pain Points**: Spending 6+ hours per video manually cutting, re-framing 9:16, and animating text.
- **Workflow**: Pastes YouTube URL → AI Clip Discovery → Approves Top 3 Clips → Applies Face Track → Exports MP4.

### Persona 2: Podcaster & Agency Editor ("Sarah", Podcast Network)
- **Goal**: Produce clips from multi-speaker video podcasts in English and Urdu.
- **Pain Points**: Existing tools mangle Urdu text ordering and cut off speakers mid-sentence.
- **Workflow**: Uploads local MP4 → Selects Manual Clipping (60s target) → Tweaks +/- 3s in lightweight editor → Selects Urdu caption preset with current-word highlight → Renders clips.

### Persona 3: Beginner Creator / Solopreneur ("David", Tech Reviewer)
- **Goal**: Create short-form video clips with zero budget and zero technical editing skills.
- **Pain Points**: Cannot afford $30/mo SaaS subscriptions or complex editing software.
- **Workflow**: Uses local Ollama + faster-whisper → Generates candidate clips → Applies pre-styled caption preset → Downloads ready-to-post short.

---

## 7. Complete User Workflow Stages

```
Stage 01: Dashboard
Stage 02: New Project Creation
Stage 03: Source Input (Local Upload / YouTube URL)
Stage 04: Video Information & Metadata Validation
Stage 05: Speech-to-Text Transcription (faster-whisper / Whisper)
Stage 06: Transcript Review & Export
Stage 07: Clipping Selection (Manual 30/60/90s OR AI Discovery)
Stage 08: Candidate Clip Review (Approve / Regenerate / Cancel)
Stage 09: Approved Clips Collection
Stage 10: Lightweight Clip Editor (Timing +/- 5s, Playback, Undo/Redo)
Stage 11: Visual Framing Engine (Face Track 9:16, Split-Screen, Original)
Stage 12: Caption Styling Engine (Presets, Word Highlights, RTL)
Stage 13: Background FFmpeg Render Execution (Taskiq + Redis)
Stage 14: Export & Download Gallery
```

---

## 8. Dashboard Specification

- **Header**: App Logo, User Profile, Quick Settings (AI Provider Status badge: Local Ollama / OpenRouter Free).
- **Primary CTA**: `[ + New Project ]` prominent action button.
- **Project Grid / List**:
  - Project Thumbnail & Title
  - Source Type Badge (Local / YouTube)
  - Duration & Detected Language
  - Status Indicator (`Draft`, `Transcribed`, `Clips Ready`, `Rendering`, `Completed`)
  - Last Updated Timestamp
  - Action Menu: `[ Open / Resume ]`, `[ Rename ]`, `[ Delete ]`
- **States**:
  - **Empty State**: Friendly illustration, "No projects yet. Click [+ New Project] to transform your first video!"
  - **Loading State**: Shimmer skeleton cards.
  - **Error State**: Safe alert banner with retry button.

---

## 9. Source Input (Local Upload & YouTube URL)

### 9.1 Local Upload
- **Supported Formats**: `.mp4`, `.mov`, `.webm`, `.mkv`
- **Max File Size**: 2 GB per source file for MVP.
- **Validation**: Server-side FFmpeg stream probe verifying valid video/audio streams, duration (> 10s, < 4h), and non-corrupted headers.

### 9.2 YouTube URL Ingestion
- **Supported Formats**: Standard YouTube links (`youtube.com/watch?v=...`, `youtu.be/...`).
- **Validation**: URL regex pattern check, availability probe, metadata extraction (Title, Channel, Duration, Thumbnail).
- **Backend Acquisition**: Non-blocking Taskiq task executing source retrieval and storing media in isolated user directory (`storage/{user_id}/{project_id}/source/raw.mp4`).

---

## 10. Manual Clipping Engine (30s / 60s / 90s Silence-Aware)

- **User Options**: `[ 30 Seconds ]`, `[ 60 Seconds ]`, `[ 90 Seconds ]` target durations.
- **Silence Boundary Detection**:
  - Backend runs FFmpeg `silencedetect` filter / PyDub silence analysis (`noise_floor = -30dB`, `min_silence_len = 0.4s`).
  - Target Window: Evaluates natural pause points within `±15%` of selected target duration.
  - **Rule**: Never slice in the middle of active speech if a silence point exists within the tolerance window.
- **Output**: Array of deterministic candidate clips with start/end timestamps and silence boundary confidence scores.

---

## 11. AI Clipping Engine & Vitality Scoring

### 11.1 AI Analysis Criteria
The AI engine evaluates the full timestamped transcript using multi-dimensional prompt scoring:
1. **Hook Strength (0-100)**: Opening 3-5 seconds curiosity or statement punchiness.
2. **Curiosity & Engagement (0-100)**: Piques audience interest or poses compelling questions.
3. **Emotional Impact (0-100)**: Humor, excitement, controversy, or empathy.
4. **Information Value (0-100)**: Actionable insights, educational tips, or strong takeaways.
5. **Standalone Context (0-100)**: Makes complete sense without watching the full video.
6. **Payoff / Ending (0-100)**: Satisfying conclusion or strong closing statement.

### 11.2 Vitality Score Formula & Reasoning
$$\text{VitalityScore} = 0.25(\text{Hook}) + 0.20(\text{Curiosity}) + 0.20(\text{Standalone}) + 0.15(\text{Value}) + 0.10(\text{Emotional}) + 0.10(\text{Payoff})$$

- **Output Object**:
```json
{
  "clipId": "clip-001",
  "startTime": 124.5,
  "endTime": 178.2,
  "duration": 53.7,
  "vitalityScore": 92,
  "whyThisClip": "Strong opening statement on AI productivity with high curiosity and complete standalone context.",
  "hookScore": 95,
  "standaloneContextScore": 90,
  "confidenceScore": 0.94
}
```

---

## 12. Candidate Clip Review Stage

Each discovered AI clip is presented as a candidate card featuring:
- **Video Preview Player**: Loops candidate timestamp segment (`startTime` to `endTime`).
- **Metadata Badges**: Duration (e.g., `53.7s`), Vitality Score (`92 / 100`).
- **Explanation Card**: "Why selected: Strong opening statement on AI productivity..."
- **Action Controls**:
  - `[ APPROVE ]`: Moves clip into the Approved Collection. Preserves AI reasoning.
  - `[ REGENERATE ]`: Requests AI Router to produce a new candidate for *only this candidate position* without re-processing the entire project.
  - `[ CANCEL ]`: Dismisses candidate clip card.

---

## 13. Multilingual Speech-to-Text Transcription

- **Primary Local Provider**: `faster-whisper` (`medium` or `large-v3` model running locally on CPU/GPU).
- **Cloud Fallback**: OpenAI Whisper API (`whisper-1`).
- **Capabilities**:
  - Auto-language detection with confidence rating.
  - Segment-level timestamps (`start`, `end`, `text`).
  - Word-level timestamps (`start`, `end`, `word`) for current-word subtitle highlighting.
  - Native RTL Unicode preservation for Urdu, Arabic, Persian.
- **Export Formats**: `.srt`, `.vtt`, `.txt`, `.json`.

---

## 14. Lightweight Clip Editor Specification

The clip editor provides focused pre-render preparation for individual approved clips:

```
+-----------------------------------------------------------------------+
|  [ Clip 01 (Approved) ]  [ Clip 02 (Approved) ]  [ Clip 03 ]          |
+-----------------------------------------------------------------------+
|                                                                       |
|                     [ Video Preview Player ]                          |
|                       (Real-time Overlays)                            |
|                                                                       |
+-----------------------------------------------------------------------+
|  Timing Adjustment:                                                   |
|  Add Start: [ -5s ] [ -2s ] [ -1s ]  |  Add End: [ +1s ] [ +2s ] [ +5s ]|
|  Current Duration: 00:54.2s (Original: 00:52.0s)                      |
+-----------------------------------------------------------------------+
|  Framing Mode:                                                        |
|  (o) Face Track 9:16   ( ) Split Screen   ( ) Original Size           |
+-----------------------------------------------------------------------+
|  Caption Style Preset:                                                |
|  [ Bold Yellow Glow  v ]  [ RTL: Enabled (Urdu) ]  [ Word Highlight ] |
+-----------------------------------------------------------------------+
|  [ Undo ]  [ Redo ]  [ Reset ]                     [ Save Changes ]   |
+-----------------------------------------------------------------------+
```

### Editor Rules:
- **Per-Clip Independent State**: Modifications to Clip 01 DO NOT affect Clip 02.
- **Timing Bounds**: Start/End adjustments cannot exceed raw source video limits or produce negative duration.
- **Auto-Save**: Changes persist via debounced backend API calls (`/api/v1/clips/{clip_id}/edit`).

---

## 15. Visual Framing Engine Modes

1. **Face Track (Vertical 9:16)**: Uses MediaPipe / OpenCV face detection to track active speaker center-of-mass and dynamically crop wide 16:9 video into vertical 9:16 short-form format.
2. **Split Screen (9:16)**: Crops speaker video into top half and secondary content into bottom half.
3. **Split + Gameplay (9:16)**: Combines primary content on top with pre-configured royalty-free gameplay footage on bottom.
4. **Split + Human Reaction (9:16)**: Top/bottom split featuring secondary reaction layer.
5. **Original Size**: Preserves original aspect ratio without cropping.

---

## 16. Dynamic Caption Preset Engine

- **Preset Library**: 60+ customizable subtitle presets (e.g., *Bold Yellow Glow*, *TikTok Modern*, *Minimalist Subtitle*, *Neon Punch*).
- **Typography & Styling**: Font family, font size, text color, line height, text position, container width, background color, background opacity, highlight color.
- **Word-Level Highlighting**: Visually highlights currently spoken word in real time matching speech timestamps.
- **RTL Language Engine**: Handles right-to-left alignment, word ordering, and character shaping for Urdu, Arabic, and Persian.

---

## 17. Free-First AI Architecture & OpenRouter Integration

```
                            +--------------------------+
                            |     AI Router Gateway    |
                            +--------------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
  +-------------------+        +-------------------+        +-------------------+
  |  Ollama Adapter   |        | OpenRouter        |        | OpenAI / Gemini   |
  | (Local Zero-Cost) |        | Provider Adapter  |        | Adapter (Cloud)   |
  +-------------------+        +-------------------+        +-------------------+
            |                            |                            |
            +----------------------------+----------------------------+
                                         |
                                         v
                            +--------------------------+
                            | Pydantic Schema Validation|
                            | (Strict JSON Enforcer)   |
                            +--------------------------+
```

### 17.1 AI Routing Policies
1. **`FREE-ONLY` (Default Policy)**:
   - Queries Ollama local instance or OpenRouter Free Model Catalogue (`:free` tagged models).
   - NEVER makes paid API calls. If no free provider is available, raises clear user alert.
2. **`FREE-FIRST`**:
   - Prefers free local/cloud models; falls back to user-configured paid key ONLY if explicitly enabled by user.
3. **`NORMAL`**: Follows configured priority list.

### 17.2 Dynamic OpenRouter Free Model Discovery
- Backend periodically queries OpenRouter `/api/v1/models` endpoint.
- Filters models with `pricing.prompt == "0"` and `pricing.completion == "0"`.
- Caches model catalog in Redis for 6 hours.
- Evaluates model capability match (context window size, structured output support) before dispatching prompt.

---

## 18. Background Job Queue Architecture (Taskiq + Redis)

- **Job Types**:
  - `task_ingest_source`: Ingests local video or fetches YouTube stream.
  - `task_transcribe_audio`: Executes `faster-whisper` audio extraction & transcription.
  - `task_ai_clip_discovery`: Invokes AI Router for clip intelligence and vitality scoring.
  - `task_render_clip`: Executes FFmpeg video framing, dynamic subtitle overlay burn, and clip rendering.
- **State Machine**: `QUEUED` → `PROCESSING` (`0%` to `100%` progress telemetry) → `COMPLETED` / `FAILED`.

---

## 19. Database Model Architecture (Entities & Relationships)

```
[User] (1) ------ (N) [Project] (1) ------ (1) [SourceVideo]
                          |
                          +------ (1) [Transcript] (1) ------ (N) [TranscriptSegment]
                          |                                             |
                          +------ (N) [ClipCandidate]                   +--- (N) [TranscriptWord]
                          |
                          +------ (N) [ApprovedClip] (1) ------ (1) [ClipEdit]
                                         |                   (1) ------ (1) [FramingConfig]
                                         |                   (1) ------ (1) [CaptionConfig]
                                         |
                                         +------ (N) [RenderJob] (1) ------ (1) [Export]
```

### Application-Level Tenant Isolation:
All database queries MUST enforce ownership validation: `WHERE user_id = authenticated_user.id`.

---

## 20. Vizard AI Competitive Analysis Matrix

| Capability / Feature | Vizard AI Reference | ClipForge AI Strategy | Classification |
| :--- | :--- | :--- | :--- |
| **YouTube Ingestion** | Supported | Supported via Taskiq background acquisition | **KEEP** |
| **AI Clip Discovery** | Supported | Supported with explainable Vitality Score breakdown | **IMPROVE** |
| **Paid API Dependency** | Mandatory SaaS subscription | **Free-First AI Architecture** (Ollama + OpenRouter Free) | **IMPROVE** |
| **RTL Language Support** | Weak / buggy text ordering | Native Unicode RTL engine (Urdu, Arabic, Persian) | **IMPROVE** |
| **Clip Boundary Control** | Basic timing sliders | Precise `+ / - seconds` silence-aware editor | **IMPROVE** |
| **Per-Clip Styling** | Global styles forced | Independent caption & framing per approved clip | **IMPROVE** |
| **User Data Privacy** | Cloud SaaS lock-in | Local-first processing option with zero media leaks | **IMPROVE** |
| **Social Auto-Publishing**| Supported | Omitted from MVP; direct MP4 export focus | **OUT OF SCOPE** |

---

## 21. Acceptance Criteria (Given / When / Then)

### Scenario A: Manual 60s Target Clipping
- **Given** a valid 30-minute uploaded video,
- **When** the user selects Manual Clipping with a 60-second target,
- **Then** the system detects natural silence pauses and outputs candidate clips with durations between 51s and 69s without severing spoken words mid-sentence.

### Scenario B: Free-Only AI Clip Discovery
- **Given** a transcribed video and `FREE-ONLY` AI routing policy,
- **When** the user clicks `[ Find AI Clips ]`,
- **Then** the AI Router queries Ollama or OpenRouter free models, validates returned JSON against Pydantic schema, and presents candidate cards with Vitality Scores without making any paid API calls.

### Scenario C: Independent Clip Caption Styling
- **Given** approved Clip 01 and Clip 02,
- **When** the user changes Clip 01's caption preset to "Bold Yellow Glow",
- **Then** Clip 01 updates its caption configuration while Clip 02 retains its original independent caption styling.

---

## 22. Edge Case Matrix & Handling

| Edge Case Event | Impact | System Remediation & User Feedback |
| :--- | :--- | :--- |
| **Video Has No Audio Track** | Ingestion failure | FFmpeg probe detects 0 audio channels; shows alert: *"No audio track detected in source video."* |
| **Video Has Zero Speech (Music Only)** | Transcription empty | `faster-whisper` returns 0 segments; shows alert: *"No spoken language detected in video."* |
| **Ollama Local Instance Offline** | AI processing failure | AI Router catches connection error, attempts OpenRouter Free fallback, or notifies user to launch Ollama. |
| **OpenRouter Free Model Deprecated** | Provider error | Dynamic discovery removes model from catalog and automatically routes request to next compatible free model. |
| **Malformed AI Timestamp Output** | Data corruption risk | Pydantic schema validation rejects response (`startTime >= endTime` or `endTime > videoDuration`); triggers auto-retry. |
| **User Closes Browser Mid-Render** | Orphaned job | Taskiq job continues processing on backend; state persists in PostgreSQL; progress restores when user re-opens project. |

---

## 23. Security, Privacy & Secret Protection

- **Server-Side Secret Isolation**: OpenAI/Gemini/OpenRouter API keys are stored exclusively in backend environment variables and NEVER exposed to frontend bundles or client logs.
- **Application-Level Tenant Boundary**: Every backend service handler validates `user_id` ownership before returning projects, transcripts, clips, or media streams.
- **Media File Security**: Media artifacts are stored in un-indexed user directories (`/storage/{user_id}/...`) and delivered exclusively via authenticated pre-signed URLs or streaming routes.
- **Automatic Storage Cleanup**: Temporary FFmpeg processing chunks and raw audio files are automatically purged 6 hours after job completion.

---

## 24. MVP vs Future Extensibility Scope

### MVP Scope (Target Release)
- Dashboard & Project Persistence
- Local Video Upload & YouTube URL Ingestion
- Multilingual Transcription (`faster-whisper` + Whisper Cloud)
- Manual Clipping (30/60/90s Silence-Aware)
- AI Clip Discovery with Explainable Vitality Score
- Candidate Clip Review (`Approve`, `Regenerate`, `Cancel`)
- Lightweight Clip Editor (Timing `+/- 5s`, Playback, Save, Undo/Redo)
- Visual Framing Engine (Face Track 9:16, Split-Screen, Original)
- Dynamic Caption Engine (60+ Presets, Current-Word Highlight, RTL Support)
- Background Taskiq + Redis FFmpeg Render Execution
- Export & Download Gallery
- Free-First AI Architecture (Ollama + OpenRouter Free Models)

### Future Scope (Post-MVP Extensions)
- Multi-track timeline editor (B-roll layers, overlay graphics, keyframes)
- Direct API publishing to TikTok, YouTube Shorts, Instagram Reels
- Advanced voice isolation and background noise suppression
- AI script translation into 30+ languages
- Team collaboration and multi-user workspace permissions

---

## 25. Open Questions & Recommendations

### Open Questions:
1. **Gameplay Asset Integration for Split-Screen**: Should MVP include a small bundle of pre-packaged royalty-free gameplay loops (e.g., Minecraft/Subway Surfers), or allow users to upload custom background video clips? *(Recommendation: Include 3 pre-packaged local loops for MVP).*

### Technical Recommendations:
1. **Pre-packaged `faster-whisper` Model**: Bundle `tiny` and `base` models with Docker container for offline development, while downloading `medium` on first boot.
2. **Debounced Auto-Save**: Implement 1000ms debounce on Editor timing and caption slider changes to prevent excessive API writes.
