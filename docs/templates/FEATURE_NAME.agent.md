# Feature Agent Specification: [FEATURE_NAME]

> **File Pattern**: `[feature-name].agent.md`  
> **Location**: `/docs/features/[feature-name].agent.md`  
> **Status**: PROPOSED / APPROVED / LOCKED  

---

## 1. Feature Identity
- **Feature ID**: FEAT-XXX
- **Feature Name**: [e.g., Speech-to-Text Transcription Engine]
- **Target Milestone**: MS-XXX
- **Owner Subsystem**: [e.g., Transcription Subsystem]

## 2. Feature Purpose
[Detailed description of what this feature accomplishes and why it exists in the system.]

## 3. User Role
[What the user does, inputs, or requests during this feature.]

## 4. System Role
[What the backend/frontend infrastructure does automatically.]

## 5. Assistant / AI Role
[Specific AI LLM or ML model responsibility, scoring, or reasoning logic.]

## 6. User Input
[Detailed listing of all form fields, file uploads, parameters, or intent instructions.]

## 7. Input Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "projectId": { "type": "string", "format": "uuid" },
    "userInstruction": { "type": "string" }
  },
  "required": ["projectId"]
}
```

## 8. Validation Rules
- [Rule 1: Boundary checks, range limits, MIME types, duration limits, etc.]
- [Rule 2: Authorization & ownership checks]

## 9. Processing Rules
- [Step-by-step internal business logic execution sequence]

## 10. Business Rules
- [Quota checks, multi-tenant restrictions, status transitions]

## 11. AI Rules
- [Prompt construction rules, temperature settings, provider router options, structured format constraints]

## 12. Output Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "status": { "type": "string" },
    "result": { "type": "object" }
  },
  "required": ["status", "result"]
}
```

## 13. UI Behavior
- [Loading indicators, progress bars, empty states, preview renders, toast alerts]

## 14. API Behavior
- [Endpoint routes, HTTP methods, status codes (200, 400, 401, 403, 422, 500)]

## 15. Database Behavior
- [Entities created/modified, transaction scope, indexing constraints]

## 16. Error Handling
- [Specific error codes, user-facing error messages, sanitize stack traces]

## 17. Edge Cases
- [Network disconnects, malformed media, missing audio track, empty transcript, LLM timeout]

## 18. Security Requirements
- [Row-level tenant validation, secret key isolation, pre-signed stream access]

## 19. Privacy Requirements
- [Local storage isolation, user video confidentiality, temporary file purging]

## 20. Performance Considerations
- [Async job delegation, FFmpeg hardware acceleration, LLM response caching]

## 21. Retry Behavior
- [Exponential backoff rules, max retry counts]

## 22. Failure Behavior
- [Graceful failure degradation, state transition to `FAILED`, alerting]

## 23. Example User Input
```json
{
  "projectId": "123e4567-e89b-12d3-a456-426614174000",
  "userInstruction": "Find controversial opinions about remote work."
}
```

## 24. Example System Processing
1. Validate user authorization for project `123e4567-e89b-12d3-a456-426614174000`.
2. Extract transcript segments and language metadata.
3. Construct AI Router prompt with schema constraints.
4. Dispatch background job.

## 25. Example Assistant / AI Output
```json
{
  "clipId": "clip-99",
  "startTime": 45.2,
  "endTime": 105.8,
  "duration": 60.6,
  "vitalityScore": 88,
  "whyThisClip": "Strong controversial hook debating workplace productivity.",
  "hookScore": 92,
  "standaloneContextScore": 85,
  "confidenceScore": 0.94
}
```

## 26. Example UI Output
Render clip card displaying:
- Video preview player (45.2s - 105.8s)
- Vitality Score badge: 88 / 100
- Reason: "Strong controversial hook debating workplace productivity."
- Actions: [ APPROVE ] [ REGENERATE ] [ CANCEL ]

## 27. Forbidden Behavior
- NEVER hardcode sample AI outputs in production handlers.
- NEVER return raw internal stack traces to the user.
- NEVER allow access to clips owned by another user ID.

## 28. Acceptance Criteria
- [ ] Schema validation enforces all required fields.
- [ ] System handles empty transcript segments gracefully without crashing.
- [ ] Verification report records 100% test pass rate.

## 29. Verification Requirements
- Functional unit test covering input schema parsing.
- Integration test simulating backend job failure and retry.
- Security test verifying row-level isolation.
