Status: PLANNING COMPLETE
Implementation: NOT STARTED
Branch: milestone/001-foundation
MS-007: AWAITING USER APPROVAL

# MS-007 PLANNING — OLLAMA LOCAL LLM INTEGRATION

## 1. Executive Summary
The MS-007 milestone introduces Ollama as a local AI provider for Clip-Forge-Ai. By leveraging the existing AI Provider Abstraction Layer (MS-006), Ollama will seamlessly integrate into the `AIRouter` without altering the core routing mechanisms, enabling completely free and local AI operations as mandated by the "Free-First" product philosophy.

## 2. Current Architecture Analysis
The current architecture (MS-006) defines a clean abstraction layer for AI capabilities:
- **Base Interface**: `BaseAIProvider` enforces `generate_text` and `generate_structured`.
- **Existing Providers**: OpenAI, Gemini, OpenRouter, and Mock.
- **Routing**: `AIRouter` manages provider selection using `FREE_ONLY` or `FREE_FIRST` policies.
- **Data Models**: `AIRequest` and `AIResponse` standardizing communication.

## 3. MS-007 Scope
### IN SCOPE
- **Ollama Provider Adapter**: Implementing `OllamaProvider` extending `BaseAIProvider`.
- **Configuration Integration**: Adding `OLLAMA_BASE_URL` and `OLLAMA_MODEL` environment variables.
- **Router Integration**: Registering Ollama in the `AIRouter` as a primary free-tier provider.
- **Error Normalization**: Translating Ollama connection failures and timeouts into `AIProviderError` subclasses.
- **Unit and Integration Tests**: Validating Ollama adapter behaviors using mocked HTTP responses.
- **Documentation & Verification**: Updating `.env.example` and compiling the milestone verification report.

### OUT OF SCOPE
- No integration with LM Studio or vLLM.
- No UI redesign or database schema changes.
- No telemetry redesign or transcription workflow modifications.

## 4. Architecture & Data Flow
The data flow strictly adheres to the MS-006 abstraction:
```text
Application
    ↓
AIRouter (Policy evaluation)
    ↓
OllamaProvider (Adapter)
    ↓ (HTTP POST /api/generate)
Ollama Local Runtime
    ↓
Local Model
```
If the Ollama runtime is unavailable, the `OllamaProvider` catches the connection error, wraps it in an `AITimeoutError` or `AIProviderError`, and bubbles it to the `AIRouter`. The router then initiates its fallback mechanism (e.g., cascading to OpenRouter if `FREE_FIRST` is active).

## 5. Configuration
The following configuration properties will be added to `backend/app/core/config.py`:
- `OLLAMA_BASE_URL`: string (default: `"http://localhost:11434"`)
- `OLLAMA_MODEL`: string (default: `"llama3"`)
- `OLLAMA_TIMEOUT`: integer (default: `60`)

These variables are optional in production environments if Ollama is not the active provider. They will be included as placeholders in `backend/.env.example`.

## 6. File Matrix
- [NEW] `backend/app/services/ai/providers/ollama.py`: Implements the `OllamaProvider`.
- [MODIFY] `backend/app/services/ai/router.py`: Registers `OllamaProvider` in the router initialization.
- [MODIFY] `backend/app/core/config.py`: Adds Ollama configuration attributes.
- [MODIFY] `backend/.env.example`: Adds `OLLAMA_BASE_URL` and `OLLAMA_MODEL` templates.
- [NEW] `backend/tests/services/ai/test_ollama_provider.py`: Unit tests specifically for the Ollama adapter.

## 7. API / Provider Contract
The `OllamaProvider` will:
- Implement `generate_text(req: AIRequest) -> AIResponse`.
- Implement `generate_structured(req: AIRequest, schema: Dict[str, Any]) -> AIResponse`.
- Utilize standard REST endpoints (`/api/generate` or `/api/chat`) exposed by Ollama.
- Map Ollama's native responses to the unified `AIResponse` format.
- Translate `httpx.ConnectError` to `AIProviderError`.

## 8. Security
- **Local Network Boundary**: The `OLLAMA_BASE_URL` configuration ensures requests are bounded to a specific host (typically localhost).
- **Sanitization**: Any raw errors returned from the Ollama API are sanitized before being bubbled up into `AIProviderError` messages to avoid leaking local system topologies.
- **No Credentials**: Ollama runs locally without API keys; no secrets will be added or required for this provider.

## 9. Testing Strategy
### Unit
- `OllamaProvider` initialization and configuration parsing.
- Request payload construction matching Ollama's API signature.
- Response normalization back to `AIResponse`.
- Connection timeout handling mapping to `AITimeoutError`.
- Connection refused mapping to `AIProviderError`.

### Router
- Ensure `AIRouter` prioritizes `OllamaProvider` under `FREE_ONLY`.
- Ensure `AIRouter` successfully falls back to OpenRouter/Mock if Ollama is unavailable.

### Regression
- Execute the full test suite (`MS-001` through `MS-006`) to ensure the addition of the new provider adapter does not negatively impact existing logic.

## 10. Verification Strategy
**Backend AI Tests:**
```powershell
cd backend
.venv\Scripts\pytest -q tests/services/ai
```
**Full Regression Check:**
```powershell
cd backend
.venv\Scripts\pytest -q
```
**Frontend Check (Assurance):**
```powershell
cd frontend
npm test -- --run
npm run lint
npm run build
```
*Note: If Ollama is not running on the executing machine, real integration tests will fail. We will rely on Mock HTTP testing. For Postgres tests, `BLOCKED — ENVIRONMENT` will be explicitly reported as per governance rules.*

## 11. Risks & Rollback
- **CRITICAL: Ollama Runtime Unavailable.** The service is not running on the host machine.
  *Mitigation*: `OllamaProvider` handles `httpx.ConnectError` safely. Router falls back seamlessly.
- **HIGH: Incompatible Model.** The requested `OLLAMA_MODEL` does not exist locally.
  *Mitigation*: `OllamaProvider` intercepts HTTP 404/400 errors and routes them to `AIProviderError`. Router falls back seamlessly.
- **MEDIUM: Timeout.** Local LLM generation is slower than cloud APIs.
  *Mitigation*: `OLLAMA_TIMEOUT` configuration introduced to allow higher thresholds (e.g., 60-120s) before terminating the request.
- **Rollback Strategy**: Revert `backend/app/services/ai/router.py` to remove the Ollama registration block, rendering the adapter inert.

## 12. Acceptance Criteria
- [ ] `OllamaProvider` successfully implements the `BaseAIProvider` contract.
- [ ] `OllamaProvider` normalizes Ollama responses into `AIResponse` format.
- [ ] `AIRouter` selects Ollama based on routing configuration.
- [ ] Fallback routing works when Ollama is unreachable.
- [ ] Configuration is securely managed without exposing new secrets.
- [ ] Unit and mock integration tests pass for the new provider.
- [ ] All MS-001 through MS-006 regression tests remain intact and pass (or report expected environmental blocks).
- [ ] No unauthorized UI or database modifications occur.
