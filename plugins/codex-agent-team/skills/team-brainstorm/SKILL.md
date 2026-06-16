---
name: team-brainstorm
description: Turn a project idea into `.codex/specs/<slug>/requirements.md` for the hybrid Codex team workflow. Use when work starts from a rough concept instead of an agreed spec.
---

# Team Brainstorm

Use this skill when the user has an idea but not a ready-to-build spec.

## Goal

Produce a repo-local requirements document at `.codex/specs/<slug>/requirements.md` that the team can turn into `spec.md`, `design.md`, and `tasks.md`.

## Process

1. Restate the project idea in concrete terms.
2. Ask only the clarifying questions needed to define MVP scope, constraints, integrations, and success criteria.
3. Synthesize the answer into a requirements document with explicit in-scope and out-of-scope boundaries.
4. Ask for or infer a short kebab-case slug.
5. Save the requirements document under `.codex/specs/<slug>/requirements.md`.

## Required Sections

- `## Project Summary`
- `## Functional Requirements`
- `## Non-Functional Requirements`
- `## Edge Cases`
- `## Out of Scope`
- `## Open Questions`
- `## Notes`

## Handoff

After the requirements document is agreed, the next step is usually:

- `team-spec-workflow` for the detailed plan
- `fullstack-agent` for coordination and delegation
