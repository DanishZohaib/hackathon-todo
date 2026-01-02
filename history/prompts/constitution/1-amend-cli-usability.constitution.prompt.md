---
id: 1
title: Amend CLI Usability
stage: constitution
date_iso: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution
labels: ["constitution", "usability", "cli"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

# Constitution Amendment: CLI Usability Improvements

## Prompt Text

```
Prompt

You are a Senior Software Architect issuing a Phase I constitutional amendment.

The system already follows spec-driven development.
This amendment improves usability without breaking architectural purity.

Amendment Scope

Applies ONLY to Phase I

Does NOT introduce persistence, users, APIs, or AI

New Constitutional Rules
8. Human-Friendly Identifiers

CLI-facing identifiers MUST be short and easy to type

Phase I identifiers MUST be sequential integers

IDs reset on application restart (in-memory rule preserved)

9. CLI Usability Is a First-Class Concern

CLI output MUST be readable without scrolling when possible

Visual separation improves correctness and reduces user error

ASCII tables are allowed in Phase I

10. Backward Simplicity

No command may accept ambiguous identifiers (e.g., description text)

All destructive actions MUST use explicit numeric IDs

11. Non-Breaking Evolution

ID changes must not alter business logic semantics

Service layer must remain UI-agnostic

Update CONSTITUTION.md to include these amendments.
```

## Response Text

Updated the constitution file to include new Phase I specific principles for CLI usability, including human-friendly identifiers, CLI usability as a first-class concern, backward simplicity, and non-breaking evolution. The version was incremented from 1.0.0 to 1.1.0 to reflect these additions.

## Outcome

The constitution was successfully updated with four new Phase I specific principles that improve CLI usability while maintaining architectural integrity. The changes focus on making the CLI more user-friendly with shorter identifiers, better output formatting, and clear requirements for command usage.

## Evaluation

The amendment was successfully applied to the constitution file, adding the new principles while preserving all existing ones. The version was properly incremented, and a sync impact report was included to document the changes made.