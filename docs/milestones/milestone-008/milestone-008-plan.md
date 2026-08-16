# MS-008 PLANNING — OPENROUTER FREE MODEL DISCOVERY

## 1. Objective & Scope
The objective of MS-008 is to extend the existing `OpenRouterProvider` and `AIRouter` (MS-006) to dynamically discover and select **currently available free OpenRouter models**. This reinforces the "Free-First" project philosophy by automatically leveraging community/free LLMs available on OpenRouter when `FREE_ONLY` or `FREE_FIRST` routing policies are active.

**In Scope:**
- Fetching model metadata from the official OpenRouter API (`https://openrouter.ai/api/v1/models`).
- Normalizing and filtering models to identify genuinely free options (zero cost for prompt and completion).
- Integrating the discovery logic into the `OpenRouterProvider` or `AIRouter`.
- Fallback mechanisms for API failures, timeouts, or empty free-model lists.

**Out of Scope:**
- No MS-009 manual clipping engine or UI/frontend redesign.
- No AI clip discovery workflows.
- No new database schema or persistent storage for model metadata.
- No new routing policies.

## 2. Architecture & Design
The OpenRouter discovery feature will be encapsulated within the `OpenRouterProvider` to keep provider-specific logic isolated.

1. **Discovery API Endpoint**: `GET https://openrouter.ai/api/v1/models`
2. **Metadata Fetching**: The `OpenRouterProvider` will expose an async method (e.g., `_fetch_free_models()`) that queries this endpoint. 
3. **Caching**: Since model pricing does not change by the second, we will implement a lightweight in-memory cache with a TTL (Time-To-Live, e.g., 1 hour) using Python's `asyncio` or simple timestamp comparisons. No database schema is required.
4. **Free Model Filtering**: A model is classified as "free" if:
   - `pricing.prompt` == "0" (or 0.0)
   - `pricing.completion` == "0" (or 0.0)
5. **Router Integration**: When the `AIRouter` attempts to resolve a fallback using `OpenRouterProvider` under a `FREE_ONLY` or `FREE_FIRST` policy, the router will ask the provider for an available free model. If the configured `model` in `AIRequest` is not free, the provider will dynamically override it with a discovered free model (or fail safely).

## 3. File Change Matrix
- `[MODIFY] backend/app/services/ai/providers/openrouter.py`:
  - Responsibility: Add `_fetch_free_models` and in-memory TTL caching. Update `generate_text` and `generate_structured` to auto-resolve to a free model if the routing policy mandates it and the requested model is not free.
- `[MODIFY] backend/app/services/ai/router.py`:
  - Responsibility: Update fallback logic to seamlessly request free-model overrides from `OpenRouterProvider` during `FREE_ONLY` or `FREE_FIRST` resolution.
- `[NEW] backend/tests/services/ai/test_openrouter_discovery.py`:
  - Responsibility: Test the OpenRouter API parsing, caching, free-model filtering, and error handling.
- `[MODIFY] backend/app/core/config.py`:
  - Responsibility: Add `OPENROUTER_DISCOVERY_CACHE_TTL` (default 3600 seconds).

## 4. Database & Persistence
- **No changes**. The discovery cache will be strictly in-memory (singleton or TTL dict). If the server restarts, the cache is rebuilt on the next request.

## 5. Storage & Privacy
- Model metadata does not contain PII or user data. No external storage is required.

## 6. API Design
- **No public backend API required**. Model discovery is an internal backend service capability used by the `AIRouter` to fulfill application AI requests.

## 7. Security
- The `GET https://openrouter.ai/api/v1/models` endpoint will be called securely using HTTPS.
- While the endpoint does not strictly require the API key for public model lists, the existing `OPENROUTER_API_KEY` will be safely used in the Authorization header to prevent rate-limiting.
- **SSRF/Injection**: The base URL `https://openrouter.ai/api/v1` remains hardcoded or strictly validated in `OpenRouterProvider`; it is not user-configurable to avoid SSRF.
- Raw provider metadata will be parsed safely using `dict.get()` and validated to prevent application crashes from malformed upstream responses.

## 8. Testing Strategy
- **Provider Discovery Tests (`test_openrouter_discovery.py`)**:
  - *Success*: Mock the HTTP GET request to return a mix of paid and free models. Verify the filter returns only free models.
  - *API Unavailable/Timeout*: Mock an `httpx.TimeoutException` or `ConnectError`. Verify the provider raises an `AIProviderError` and the router falls back safely.
  - *Malformed Response*: Mock a response with missing `pricing` keys. Verify the model is safely excluded rather than crashing.
  - *Caching*: Call the discovery method twice. Verify the HTTP client is only invoked once.
- **Router Fallback Tests**:
  - Update existing MS-006 router tests to ensure `OpenRouterProvider` correctly selects a free model during `FREE_ONLY` policy enforcement when Ollama is unavailable.

## 9. Verification Strategy
- **Targeted AI Tests**: `cd backend; .venv\Scripts\pytest -q tests/services/ai`
- **Full Backend Pytest**: `cd backend; .venv\Scripts\pytest -q`
- **Security Check**: `git grep -i -E "api_key|apikey|authorization|bearer|secret|password"` to ensure no hardcoded secrets exist.
- **Environment Exceptions**: If Docker/Postgres is unavailable, full tests will report `BLOCKED — ENVIRONMENT`.

## 10. Risks & Rollback
- **Risk**: OpenRouter API structure changes (e.g., `pricing` fields move).
  - *Mitigation*: Defensive parsing (`.get("pricing", {}).get("prompt", "0")`). If parsing fails completely, the provider fails gracefully, and the router catches the `AIProviderError`.
- **Risk**: Rate limiting on the models endpoint.
  - *Mitigation*: In-memory TTL caching guarantees a maximum of 1 request per hour per worker.
- **Rollback**: Revert the modifications to `backend/app/services/ai/providers/openrouter.py` to restore the static, non-discovery MS-006 behavior.

## 11. Acceptance Criteria
- [ ] `OpenRouterProvider` can fetch and parse the official OpenRouter models API.
- [ ] Only genuinely free models (0 cost for prompt and completion) are cached.
- [ ] Paid models are strictly excluded from the free-model pool.
- [ ] API timeouts and malformed JSON responses do not crash the application.
- [ ] The `AIRouter` correctly uses discovered free models when `FREE_ONLY` or `FREE_FIRST` is active and fallback to OpenRouter is required.
- [ ] No database changes are introduced.
- [ ] All MS-001 through MS-007 regression tests continue to pass.
- [ ] No secrets are exposed or hardcoded.

## 12. Regression Protection
- The introduction of OpenRouter discovery must not break the `OllamaProvider` (MS-007) or the core `AIRouter` (MS-006).
- The existing mocked fallback tests will be run to ensure the fallback chain (Ollama -> OpenRouter -> Mock) remains intact.
- The `test_transcription_service.py` (MS-005) must remain green.
