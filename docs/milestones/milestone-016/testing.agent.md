# Testing Infrastructure Agent Specification

## Identity

* Milestone: MS-016
* Feature: Testing Infrastructure & Cross-Cutting Tests
* Status: PLANNING / AWAITING USER APPROVAL

## Objective

Establish cross-cutting testing infrastructure for the entire Clip Forge AI MVP, ensuring the reliability of unit, API, integration, and UI boundaries for MS-002 through MS-015.

## Allowed Scope

* `backend/tests/` (all subdirectories)
* `frontend/__tests__/` (all subdirectories)
* `e2e/` (new directory)
* `package.json`
* `playwright.config.ts`
* Minor test-specific configuration files (`pytest.ini`, `conftest.py`, etc.)

## Forbidden Scope

* Do NOT modify core application source code (`backend/app/`, `frontend/src/`) unless required to fix a verified bug discovered during testing.
* Do NOT add new product features.
* Do NOT implement MS-017+ features.

## Architecture Rules

* Tests must respect the existing modular monolith architecture.
* E2E tests must use Playwright.
* Backend tests must use Pytest.
* Frontend tests must use Jest / React Testing Library.

## Security Rules

* Tests must explicitly test MS-015 security constraints (unauthorized access, tenant isolation).
* Do not expose real secrets in test files. Use mocks or `.env.test`.

## Backend Rules

* All API routes must have basic unit/integration tests verifying 200, 401, 403, and 404 responses.
* Services must be tested with mocked database sessions.

## Frontend Rules

* Core contexts (`AuthContext`, `ProjectContext`) must be tested for state transitions.
* Complex views must be covered by component tests.

## Database Rules

* No schema changes allowed.
* Tests must use a clean, isolated database or transaction rollbacks for each test.

## Job Rules

* Taskiq workers must be tested using Taskiq's testing utilities.
* Redis must be mocked or managed via a local ephemeral instance during tests.

## Storage Rules

* Storage drivers must be mocked during unit tests to prevent disk pollution.
* E2E tests must clean up their own generated files.

## Error Handling Rules

* Ensure tests assert that correct error structures and HTTP status codes are returned on failure.

## Testing Requirements

* `pytest` must pass.
* `npm test` must pass.
* Playwright E2E tests must execute the happy path successfully.

## Verification Requirements

* Provide a test coverage report showing significant coverage of backend routers and services.
* Provide passing Playwright execution logs for the E2E happy path.

## Definition of Done

* Backend, Frontend, and E2E test scaffolding is established and passing.
* Tests run cleanly without hanging on background tasks.
* Ownership boundary tests are confirmed working.

## Change Control

Any requirement outside this agent specification requires user review and formal change control before implementation.
