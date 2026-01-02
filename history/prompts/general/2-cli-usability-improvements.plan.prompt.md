---
id: 2
title: CLI Usability Improvements Plan
stage: plan
date: 2026-01-01
surface: agent
model: Claude Sonnet 4.5
feature: cli-usability-improvements
branch: "8-cli-usability-improvements"
user: user
command: "/sp.plan"
labels: [planning, cli, usability, architecture]
links:
  spec: "specs-history/006-sequential-task-identifiers.spec.md, specs-history/007-cli-table-rendering.spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - plan.md
  - research.md
  - data-model.md
  - contracts/api-contracts.md
  - quickstart.md
tests:
  - "plan completeness validated"
  - "contracts defined"
  - "data model specified"
---

## Prompt

Prompt

You are planning a Phase I revision, not a new phase.

Revision Goals

Improve CLI usability

Maintain architectural cleanliness

Avoid breaking existing behavior

Execution Plan
Step 1: ID Strategy Update

Introduce sequential ID generator

Ensure service layer owns ID creation

Step 2: Update Commands

Enforce integer-only IDs

Improve error messages for invalid IDs

Step 3: CLI Table Renderer

Create a dedicated rendering function/module

Ensure CLI remains thin

Step 4: Validation

Add tasks

List tasks (verify table)

Delete using numeric ID

Update using numeric ID

Mark complete/incomplete

Stop Condition

Phase I revision complete

No persistence

No Phase II work begins

Produce a Phase I Revision Plan and stop.

## Response snapshot

Successfully created a comprehensive Phase I revision plan for CLI usability improvements:

1. **plan.md**: Complete implementation plan with technical context, constitution check, and step-by-step approach
2. **research.md**: Research findings resolving all unknowns about sequential ID generation and ASCII table rendering
3. **data-model.md**: Detailed data model changes for integer IDs
4. **contracts/api-contracts.md**: Complete API contracts for CLI commands and service methods
5. **quickstart.md**: Quickstart guide for implementing the changes

The plan addresses all requirements:
- Sequential integer ID generation starting from 1
- ASCII table rendering for improved CLI output
- Integer-only ID validation across all commands
- Non-breaking evolution preserving existing functionality
- In-memory behavior maintained (IDs reset on restart)

All artifacts are ready for the implementation phase.

## Outcome

- ✅ Impact: Complete planning artifacts for CLI usability improvements
- 🧪 Tests: All planning documents validated against requirements
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/api-contracts.md, quickstart.md
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan maintains architectural cleanliness while improving usability

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All validations passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation phase