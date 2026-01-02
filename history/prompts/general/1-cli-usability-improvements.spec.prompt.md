---
id: 1
title: CLI Usability Improvements Specifications
stage: spec
date: 2026-01-01
surface: agent
model: Claude Sonnet 4.5
feature: cli-usability-improvements
branch: "8-cli-usability-improvements"
user: user
command: "/sp.specify"
labels: [specification, cli, usability]
links:
  spec: "specs-history/006-sequential-task-identifiers.spec.md, specs-history/007-cli-table-rendering.spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - specs-history/006-sequential-task-identifiers.spec.md
  - specs-history/007-cli-table-rendering.spec.md
  - specs-history/checklists/requirements.md
tests:
  - "specs validated against requirements"
  - "quality checklist created"
---

## Prompt

### Prompt

You are operating in **Spec-Kit Plus revision mode**.

A usability issue has been identified in Phase I:
- UUIDs are hard to use in CLI
- CLI output lacks visual clarity

You must create **new specifications** (do NOT modify existing ones).

## New Required Specs (Phase I – Revision A)

### Spec 006: Sequential Task Identifiers
### Spec 007: CLI Table Rendering

## Rules
- Existing specs (001–005) remain valid
- New behavior MUST be additive
- Specs must clearly state what is replaced or overridden

## Spec Requirements
Each spec MUST include:
- Purpose
- Functional Requirements
- Acceptance Criteria
- Explicit Non-Goals

## Constraints
- IDs must be integers
- No third-party UI libraries
- Tables must use plain text characters only

Create the new specs and store them in `specs-history/`.
📄 Spec 006 — Sequential Task Identifiers
006_sequential_task_ids.md
Purpose
Replace UUID-based task identification with human-friendly sequential integers.

Functional Requirements

Each task receives an integer ID starting from 1

IDs increment by +1 for each new task

IDs are unique during runtime

IDs reset when application restarts

Acceptance Criteria

User can type IDs without copy/paste

Delete/update commands accept only integers

Listing tasks shows numeric IDs clearly

Non-Goals

Persistence of IDs

Global uniqueness

Reuse of deleted IDs

📄 Spec 007 — CLI Table Rendering
007_cli_table_rendering.md
Purpose
Improve CLI readability by rendering tasks in a structured table.

Functional Requirements

Task list must be displayed as an ASCII table

Columns:

ID

Title

Description

Status

Header and row separators must be visible

Example (Illustrative Only)

sql
Copy code
+----+-------------+----------------------+-----------+
| ID | Title       | Description          | Status    |
+----+-------------+----------------------+-----------+
| 1  | Buy Milk    | From grocery store   | ❌ Open   |
| 2  | Pay Bills   | Electricity + Gas    | ✅ Done   |
+----+-------------+----------------------+-----

## Response snapshot

Successfully created two specifications to address CLI usability issues:
1. Spec 006: Sequential Task Identifiers - Replaces UUID-based task identification with human-friendly sequential integers
2. Spec 007: CLI Table Rendering - Improves CLI readability by rendering tasks in a structured ASCII table

Both specifications meet all requirements with proper Purpose, Functional Requirements, Acceptance Criteria, and Non-Goals sections. Created quality checklist to validate specification completeness.

## Outcome

- ✅ Impact: Created specifications that address usability issues with UUIDs and CLI output clarity
- 🧪 Tests: Validated specs against requirements and created quality checklist
- 📁 Files: Created 006-sequential-task-identifiers.spec.md, 007-cli-table-rendering.spec.md, and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specifications successfully address the identified usability issues while maintaining simplicity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All validations passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase