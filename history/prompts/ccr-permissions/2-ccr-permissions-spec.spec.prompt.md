---
id: 2
title: Claude Code Router Permissions Spec
stage: spec
date_iso: 2026-01-05
surface: agent
model: Claude Sonnet 4.5
feature: ccr-permissions
branch: 002-ccr-permissions
user: Claude
command: /sp.specify
labels: ["specification", "permissions", "ccr", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/002-ccr-permissions/spec.md
  - specs/002-ccr-permissions/checklists/requirements.md
  - specs-history/002_ccr_permissions_spec.md
tests_yaml: |
  - Specification created and validated
  - Checklist completed
  - Files copied to specs-history/
prompt_text: |
  Prompt

  A configuration failure has been identified in Phase II related to Claude Code Router permissions.

  The failure prevents agent execution due to invalid permission patterns.

  Create a new specification to govern:

  Tool permission syntax

  Safe Bash command access

  CCR compatibility

  This specification MUST:

  Apply to Phase II and beyond

  Not modify application logic

  Ensure CCR settings are valid and minimal

  Create a new spec and store it in specs-history/.


  ---

  ## 📄 **Spec 014 — Claude Code Router Permissions**

  ### `014_ccr_permissions_spec.md`

  ### Purpose
  Define valid, secure, and CCR-compatible tool permissions to enable agent execution without configuration errors.

  ---

  ### Functional Requirements

  1. **Permission Pattern Rules**
     - Bash permissions MUST use prefix matching via `:*`
     - Wildcards like `*` are NOT allowed alone

  2. **Quoting Rules**
     - No nested quotes inside permission strings
     - Paths must be unquoted or escaped properly

  3. **Minimal Permission Principle**
     - O
response_text: |
  Created specification for Claude Code Router permissions (specs/002-ccr-permissions/spec.md) that defines tool permission syntax, safe Bash command access, and CCR compatibility requirements. The specification includes functional requirements for permission pattern rules, quoting rules, minimal permission principles, CCR compatibility, tool permission syntax, and safe Bash access. A validation checklist was created and the specification was copied to specs-history/ as requested.
outcome: |
  Successfully created CCR permissions specification addressing configuration failures in Phase II related to invalid permission patterns. The specification defines clear rules for tool permissions, Bash access safety, and CCR compatibility while ensuring minimal and valid settings.
evaluation: |
  The specification meets all requirements: applies to Phase II and beyond, doesn't modify application logic, ensures CCR settings are valid and minimal, and has been stored in specs-history/. All functional requirements are testable and clearly defined.
---

## User Input

```text
Prompt

A configuration failure has been identified in Phase II related to Claude Code Router permissions.

The failure prevents agent execution due to invalid permission patterns.

Create a new specification to govern:

Tool permission syntax

Safe Bash command access

CCR compatibility

This specification MUST:

Apply to Phase II and beyond

Not modify application logic

Ensure CCR settings are valid and minimal

Create a new spec and store it in specs-history/.


---

## 📄 **Spec 014 — Claude Code Router Permissions**

### `014_ccr_permissions_spec.md`

### Purpose
Define valid, secure, and CCR-compatible tool permissions to enable agent execution without configuration errors.

---

### Functional Requirements

1. **Permission Pattern Rules**
   - Bash permissions MUST use prefix matching via `:*`
   - Wildcards like `*` are NOT allowed alone

2. **Quoting Rules**
   - No nested quotes inside permission strings
   - Paths must be unquoted or escaped properly

3. **Minimal Permission Principle**
   - O
```