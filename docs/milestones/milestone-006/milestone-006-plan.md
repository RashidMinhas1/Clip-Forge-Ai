# MS-006 Implementation Plan: Universal AI Provider Manager

## 1. Goal & Scope
**Objective:** Establish a clean, universal AI provider abstraction layer ("Central AI Router") to isolate the application from provider-specific logic. 

**Scope:**
- Define the canonical AI provider interface and base abstractions.
- Implement the AI Router capable of executing configured routing policies (FREE-ONLY, FREE-FIRST, NORMAL).
- Implement normalized request/response models.
- Support structured Pydantic schema generation (`generate_structured`).
- Integrate basic provider telemetry and error normalization.
- Configuration loading for AI models and provider endpoints.
- Provide a robust mock provider for deterministic testing.

## 2. Authoritative Architecture & Decisions
- **Free-First AI Architecture:** Enforce policies preventing accidental paid API usage unless explicitly authorized. (Per PRD)
- **Modular Monolith & Background Jobs:** The AI router will be invoked synchronously for lightweight tasks or from within `Taskiq` for heavy tasks (e.g., clip discovery).
- **Security:** Secrets must remain strictly server-side and never leak to the frontend. (Per SECURITY_RULES.md)

## 3. Current Repository State
- **State:** The foundation (MS-001 through MS-004) and transcription service (MS-005) are locked and merged.
- **Existing AI Code:** Contains Whisper and `faster-whisper` implementations in `backend/app/services/transcription/`. There are currently no implementations for LLM orchestration.
- **Settings:** Pydantic `BaseSettings` handles current config in `backend/app/core/config.py`.

## 4. Proposed Architecture

### AI Provider Interface
```python
class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_text(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    async def generate_structured(self, request: AIRequest, response_model: Type[BaseModel]) -> AIResponse:
        pass
        
    @abstractmethod
    async def check_health(self) -> bool:
        pass
```

### Normalized Models
- **AIRequest:** Contains `messages`, `model`, `temperature`, `max_tokens`, `timeout`.
- **AIResponse:** Contains `content` (string or parsed JSON), `provider_name`, `model_used`, `usage` (prompt_tokens, completion_tokens), `latency_ms`.

### AI Router & Routing Strategy
The `AIRouter` class will manage provider registration and execution.
- **Routing Policies:** 
  - `FREE_ONLY` (default)
  - `FREE_FIRST`
  - `NORMAL`
- **Fallback:** On `ProviderError` or timeout, the router moves to the next eligible provider in the chain according to the routing policy.

### Error Handling & Telemetry
- Expose a normalized `AIProviderError` hierarchy (`AITimeoutError`, `AIAuthenticationError`, etc.).
- The Router emits standard python `logging` telemetry recording latency, model used, and token usage, avoiding any direct DB persistence in MS-006.

## 5. File Matrix

| Action | File | Purpose | Reason |
| ------ | ---- | ------- | ------ |
| NEW | `backend/app/services/ai/__init__.py` | Package init | Module setup |
| NEW | `backend/app/services/ai/models.py` | Normalized request/response Pydantic schemas | Decouple from provider SDKs |
| NEW | `backend/app/services/ai/providers/base.py` | Abstract `BaseAIProvider` class | Enforce uniform API |
| NEW | `backend/app/services/ai/router.py` | Orchestration and policy enforcement | Handle fallback & FREE-ONLY rules |
| NEW | `backend/app/services/ai/exceptions.py` | Normalized error classes | Unified error handling |
| NEW | `backend/app/services/ai/providers/mock.py` | Mock provider | Testing and local dev without keys |
| MODIFY | `backend/app/core/config.py` | Add AI routing settings | Enforce routing policy configuration |
| MODIFY | `backend/.env.example` | Add placeholders for OpenAI, OpenRouter | Configure provider API keys |
| NEW | `backend/tests/services/ai/test_router.py` | Test routing policies | Verify fallback and free-first |
| NEW | `backend/tests/services/ai/test_models.py` | Test normalization | Verify schemas |

*(Note: Locked files from MS-002 to MS-005 remain untouched except for config integration.)*

## 6. Database / API / Frontend Impact
- **Database changes:** NO. Provider abstraction is a runtime service layer. Telemetry is handled via structured logging at this stage; DB logging of AI telemetry is deferred to a future milestone if needed.
- **API Impact:** NO. MS-006 establishes backend internal infrastructure.
- **Frontend Impact:** NO. No frontend implementation is required for MS-006.

## 7. Security & Resource Safety
- **Secrets Management:** `OPENAI_API_KEY`, `OPENROUTER_API_KEY` are read strictly via Pydantic `Settings` and are never exposed via API endpoints.
- **Resource Constraints:** `AIRequest` enforces strict `timeout` (e.g., 60s default) to prevent worker locking. 
- **SSRF Prevention:** If configuring custom endpoints for local models, URLs are validated against allowed schemas (e.g., `http://localhost:*`, `http://127.0.0.1:*`) using Pydantic `HttpUrl`.

## 8. Dependencies & Configuration
- **Dependencies:** NO new runtime dependencies are strictly required for the abstraction layer itself.
- **Configuration:** Added to `config.py`:
  - `AI_ROUTING_POLICY` (default: "FREE_ONLY")
  - `OLLAMA_BASE_URL`
  - `OPENROUTER_API_KEY`

## 9. Testing & Regression Strategy
- **Unit Tests:** High coverage on `AIRouter` logic using `MockAIProvider` to simulate timeouts and failures.
- **Regression:** Run the full existing `pytest` suite to ensure `Settings` additions didn't break MS-002, MS-003, or MS-005.

## 10. Verification Strategy
**Backend Unit Testing**
```powershell
cd backend
.venv\Scripts\pytest tests/services/ai/ -v
```
*PASS condition:* 100% of AI router tests pass.

**Full Regression**
```powershell
.venv\Scripts\pytest -q
```
*PASS condition:* Pre-existing tests pass (or hit known Environmental blocks).

## 11. Risks & Rollback

| Risk | Severity | Impact | Mitigation |
| ---- | -------- | ------ | ---------- |
| Schema mismatch across providers | Medium | Parsing errors on structured generation | Centralized Pydantic normalization |
| Timeout blocking workers | High | Taskiq worker exhaustion | Strict timeout passed to `asyncio.wait_for` |
| Accidental paid API use | High | Financial cost to users | Default policy locked to `FREE_ONLY` |

**Rollback Strategy:** Delete the `backend/app/services/ai` directory and revert `config.py`.

## 12. Acceptance Criteria
- **AC-001:** `BaseAIProvider` interface exists with `generate_text` and `generate_structured`.
- **AC-002:** `AIRouter` correctly routes requests based on the `AI_ROUTING_POLICY` configuration.
- **AC-003:** `AIRouter` successfully falls back to a secondary provider upon primary provider failure or timeout.
- **AC-004:** Configuration system loads provider API keys securely without exposing them in logs.
- **AC-005:** `AIProviderError` hierarchy normalizes provider-specific exceptions.
- **AC-006:** A mock provider is available for deterministic testing.

---

### Milestone Boundary
MS-006 STRICTLY focuses on the abstraction, configuration, and routing architecture.

### Deferred Work
- **MS-007:** Implementation of the Ollama concrete adapter.
- **MS-008:** Implementation of the OpenRouter concrete adapter.
- **MS-010/MS-011:** AI Vitality Scoring logic and Prompt Engineering.
- **MS-012/MS-014:** Editing and rendering.

### Open Questions
Open Questions: None
