# ClipForge AI — Security Architecture & Data Privacy Rules

> **Status**: LOCKED (Foundation Phase Verified)  
> **Scope**: Mandatory System-wide Security & Isolation Controls  

---

## 1. Secrets & Credentials Policy

- **Zero Hardcoding**: NEVER commit or hardcode API keys, database connection strings, JWT secret keys, storage credentials, or private access tokens into source code, comments, documentation, or frontend assets.
- **Environment Variable Enforcer**: All configuration values must be loaded from process environment variables and parsed through `pydantic-settings` on backend boot. If a required secret is missing, the backend service MUST immediately fail to launch.
- **Pre-Push Inspection**: Before committing code or pushing branches to GitHub, developers/agents must perform secret detection scans (`git status`, `git diff`) to verify `.env` or sensitive variables are not staged.

---

## 2. Application-Level Tenant Isolation & Data Privacy

- **Application-Level Tenant Authorization**: Security boundaries are governed by explicit application-level ownership checks (`WHERE user_id = authenticated_user.id`) enforced across all backend service handlers and queries for all user-owned entities (Projects, Sources, Videos, Transcripts, Clips, Edits, Caption configurations, Render Jobs, Exports, AI Jobs).
- **PostgreSQL Row-Level Security (RLS) Policy**: PostgreSQL Row-Level Security (RLS) may be evaluated as a future defense-in-depth layer. It is not currently active, and security reliance rests strictly on verified application-level authorization boundaries.
- **File System Isolation**: Video files, audio clips, thumbnails, and transcripts MUST be written to directory structures segmented by `user_id`. Direct path traversal (`../`) is strictly prevented by enforcing UUID validation on file request parameters.
- **Pre-Signed / Authorized Media Streaming**: Media files MUST NOT be stored in publicly accessible web server roots. Access is provided exclusively through authenticated API endpoints verifying ownership or short-lived signed tokens.

---

## 3. Input Validation & API Protection

- **Schema Strictness**: All incoming API requests must be validated using Pydantic schemas. Unrecognized or extra payload fields must be rejected.
- **File Upload Protection**: Video upload endpoints must enforce:
  - Allowed MIME types (`video/mp4`, `video/quicktime`, `video/webm`, `video/x-matroska`).
  - Max upload size limits (e.g., 2GB per video source).
  - FFmpeg stream sanity probe (verify valid video/audio headers before processing).
- **Sanitized Log Output**: Log files MUST filter out authorization headers, passwords, JWT tokens, AI API keys, and sensitive user transcripts.

---

## 4. Temporary Media Cleanup & Storage Retention

- Intermediate media artifacts created during audio extraction, speech recognition, silence detection, or FFmpeg rendering MUST be automatically deleted upon task completion or task failure.
- Storage cleanup cron background jobs will inspect orphaned processing directories (`/storage/tmp/`) every 24 hours and purge assets older than 6 hours.
