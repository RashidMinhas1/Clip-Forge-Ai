# MS-016 - Testing Infrastructure & Cross-Cutting Tests

## 1. Milestone Identity
**MS-016** - Testing Infrastructure & Cross-Cutting Tests.

## 2. Objective
Establish and complete the cross-cutting testing infrastructure for the entire Clip Forge AI MVP. This milestone focuses on comprehensive test coverage for all preceding milestones (MS-002 through MS-015), ensuring the reliability of unit, API, integration, and UI boundaries before final MVP verification.

## 3. Relationship to MS-015
MS-016 builds directly upon the locked security hardening and authentication mechanisms introduced in MS-015. Testing strategies must now incorporate valid JWT token injection, project ownership verification, and security middleware assertions to ensure tests accurately reflect the secured production state.

## 4. Scope
### In Scope
- Expanding Pytest backend unit and integration tests.
- Expanding Jest/React Testing Library frontend component tests.
- Implementing Playwright E2E testing scaffolding for critical user flows (upload, edit, export).
- Testing AI provider abstraction fallbacks (mocking OpenRouter/Ollama).
- Testing media ingestion and rendering pipeline (mocking FFmpeg).
- Securing existing endpoints within test client setups.

### Out of Scope
- Implementing new product features.
- Performance and load testing (unless part of MVP Verification).
- CI/CD pipeline automation (out of scope unless explicitly requested).
- Any MS-017+ feature (e.g. advanced AI models, overlays, social publishing).
- Changing MS-001 through MS-015 implementation logic unless fixing a verified test bug.

## 6. Architecture Impact
- **Backend:** No change required.
- **Frontend:** No change required.
- **Database:** No change required.
- **Storage:** No change required.
- **API:** No change required.
- **Authentication:** No change required.
- **Authorization:** No change required.
- **Background jobs:** No change required.
- **Taskiq / Redis:** No change required.
- **External providers:** No change required.

## 7. File-Level Implementation Matrix
| File | Change | Purpose | Reason |
| :--- | :--- | :--- | :--- |
| `backend/tests/` | MODIFIED | Expand unit/API test coverage | Achieve test reliability for MS-002 to MS-015 |
| `frontend/__tests__/` | MODIFIED | Expand component tests | Validate UI components and contexts |
| `e2e/` | NEW | Playwright test specifications | End-to-end integration tests across stack |
| `package.json` | MODIFIED | Add Playwright dependency | Required for E2E testing |
| `playwright.config.ts` | NEW | Playwright configuration | Establish E2E testing framework |

## 8. Database Changes
No database changes required.

## 9. API Contract
No new endpoints required. (Testing existing endpoints only).

## 10. Frontend UX
No change required to UX. (Testing existing components only).

## 11. Background Processing
No background job changes required. (Taskiq workers will be tested in isolation).

## 12. Security
Builds on MS-015. Tests must explicitly verify:
- Unauthenticated access returns HTTP 401.
- Unauthorized cross-project access returns HTTP 403.
- Rate limiting behaviors (if testable).
- Safe file access and isolation behaviors.

## 13. Testing Strategy
- **Backend:** Complete test suites for API routes (`tests/api/`), services (`tests/services/`), models, and tasks.
- **Frontend:** Complete rendering and state management tests for contexts (`AuthContext`, `ProjectContext`) and complex views (`Lightweight Editor`, `Caption Engine`).
- **Regression:** Ensure existing test scaffolding from MS-002 through MS-015 runs successfully without regressions.

## 14. Acceptance Criteria
- **AC-01:** `pytest` executes successfully for all backend modules with no failures.
- **AC-02:** `npm test` executes successfully for all frontend components with no failures.
- **AC-03:** Playwright E2E tests successfully execute the "happy path" project lifecycle (creation -> upload -> edit -> export) without failures.
- **AC-04:** Ownership boundary tests successfully verify MS-015 security constraints.

## 15. Environment Constraints
- PostgreSQL and Redis dependencies must be mocked or managed via testcontainers/in-memory SQLite for local testing if actual infrastructure is unavailable.
- External AI endpoints (OpenRouter/Ollama) MUST be mocked using `pytest-mock` or `respx` to prevent network dependency during tests.

## 16. Governance
- **Implementation:** NOT STARTED
- **Implementation Branch:** NOT CREATED
- **Planning:** ONLY