---
name: team-brainstorm
description: Turn a rough project idea into `.codex/specs/<slug>/requirements.md` for the hybrid Codex team workflow. Use when work starts from an idea rather than an agreed spec.
---

# Team Brainstorm

Use this skill when the user has an idea but not a ready-to-build spec.

## Goal

Produce a repo-local requirements document at `.codex/specs/<slug>/requirements.md` that can feed `spec.md`, `design.md`, and `tasks.md`.

## Process

1. Analyze the idea: domain, users, value proposition, likely constraints.
2. Ask the minimum clarifying questions needed, one at a time. Use at most 10 unless the user wants deeper exploration.
3. Cover:
   - target users and pain points
   - core functionality versus nice-to-have
   - scale expectations
   - integrations and data sources
   - non-functional requirements
   - security/compliance
   - budget/timeline
   - deployment environment
   - edge cases and failure scenarios
   - what done means for MVP
4. Synthesize requirements.
5. Present them for user review and refine until accepted.
6. Ask for or infer a short kebab-case slug.
7. Save to `.codex/specs/<slug>/requirements.md`.

## Required Sections

- `## Project Summary`
- `## Functional Requirements`
- `## Non-Functional Requirements`
- `## Edge Cases`
- `## Out of Scope`
- `## Open Questions`
- `## Notes`

## Handoff

After requirements are agreed, the next step is usually:
- `team-spec-workflow` for `spec.md`, `design.md`, and `tasks.md`
- `fullstack-agent` or the main thread as coordinator for delegation and review

If the idea is too broad for one spec, decompose it into sub-projects and brainstorm the first buildable slice.
