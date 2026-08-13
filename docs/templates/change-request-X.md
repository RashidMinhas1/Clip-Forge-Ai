# Change Request Analysis: [CHANGE_TITLE]

> **Change Request ID**: CR-XXX  
> **Target Milestone**: MS-XXX (Locked / Active)  
> **Document Location**: `/docs/decisions/change-request-XXX.md`  
> **Status**: PROPOSED / APPROVED / REJECTED  

---

## 1. Requested Change Overview
[Detailed summary of the user's requested modification or scope change to locked features.]

## 2. Current vs Proposed Behavior
- **Current Behavior**: [Description of existing locked feature behavior]
- **Proposed Behavior**: [Description of requested new behavior]

## 3. Comprehensive Technical Impact Analysis

### 3.1 Architecture & Codebase Impact
[List of backend, frontend, media, or AI services affected.]

### 3.2 Feature Agent (`.agent.md`) Specs Impact
[List of `.agent.md` files requiring update and spec revision.]

### 3.3 Database & Migration Impact
[Schema alterations, table migrations, index additions.]

### 3.4 API & Data Contract Impact
[Endpoint route modifications, breaking schema changes.]

### 3.5 Security & Data Privacy Impact
[Row-level isolation checks, secret validation.]

### 3.6 Regression Risk Assessment
- **Risk Level**: LOW / MEDIUM / HIGH
- **Mitigation Strategy**: [How potential regression will be tested and prevented]

## 4. Work Estimate & File Changes

#### Files to Modify
- [ ] [`path/to/file1.py`](file:///path/to/file1.py)
- [ ] [`path/to/file2.ts`](file:///path/to/file2.ts)

#### Feature Agent Files to Spec Update
- [ ] [`docs/features/FEATURE_NAME.agent.md`](file:///d:/Clip-Forge-Ai/docs/features/FEATURE_NAME.agent.md)

## 5. Approval Gate
- [ ] User review completed.
- [ ] User explicit authorization granted to proceed.
