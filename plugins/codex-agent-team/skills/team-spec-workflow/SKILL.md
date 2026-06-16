---
name: team-spec-workflow
description: Spec-driven hybrid Codex team workflow using `.codex/specs/<slug>/` artifacts, file-disjoint task waves, and explicit subagent handoffs. Use for non-trivial work that needs planning, delegation, or review loops.
---

# Team Spec Workflow

Use this workflow when the task spans multiple files, needs architectural decisions, or benefits from explicit parallel role handoffs.

## Artifact Layout

Store team artifacts under `.codex/specs/<slug>/` using a short kebab-case slug.

```text
.codex/specs/<slug>/
  spec.md
  design.md
  tasks.md
  review.md
  review-<scope>.md
  review-summary.md
  sa-review.md
  decisions.md
  requirements.md
```

Use only the files that the task needs. `spec.md`, `tasks.md`, and at least one review file are the normal minimum.

## Core Loop

1. Capture requirements and constraints in `spec.md`.
2. Add architecture and integration detail in `design.md` when the work is not obvious from the spec.
3. Write `tasks.md` in parallel waves.
4. Delegate file-disjoint work explicitly to custom agents.
5. Run a dedicated review wave and record PASS or FAIL.
6. Convert any FAIL into a fix wave, then repeat review.

## Task Format

`tasks.md` is a plain coordination artifact, not a live task-store. Use this shape:

```md
## Wave 1: shared contracts
- [ ] [coding] Define API contracts | `src/api/types.ts` | Exports the agreed request and response types. Verify: `npm test -- api-types`
- [ ] [devops] Define environment contract | `.github/workflows/ci.yml`, `docs/deploy.md` | CI and deploy docs agree on required env vars. Verify: `npm run lint`
```

Rules:

- Keep each task self-contained.
- Tasks in the same wave must not write the same files.
- Put the exact file paths in the task.
- Include a concrete verification step.
- For devops, smoke, staging, deploy, or environment-facing tasks, include target classification, non-production preflight, retry/timeout/abort behavior, and evidence capture.
- Start a new wave only when there is a real dependency barrier.

## Delegation Model

This workflow does not rely on a shared task-store. Use explicit delegation instead:

- The lead agent writes or updates the spec artifacts.
- The lead explicitly spawns role agents with a narrow scope and file list.
- Each agent returns a concise implementation or review summary.
- The lead consolidates outcomes back into the spec artifacts and the user-facing thread.

## Review Files

Use `review.md` for a single cohesive review pass. Use `review-<scope>.md` when review is split by subsystem or file set.

Suggested structure:

```md
## Cycle 1
Scope: API surface and request validation

### Findings
- [path:line] Risk or bug

### Tests
- Verification command and result

### Verdict
FAIL
```

## Coordination Guidelines

- Prefer many small file-disjoint scopes over a few large ones.
- Keep the main thread focused on decisions and consolidated outcomes.
- Use worktrees only when file overlap cannot be avoided and the repo supports them.
- Store key architecture or scope changes in `decisions.md` so later waves do not relitigate them.
- After any review or SA finding, create a fix wave, rerun the affected review scope, and record the outcome in `review-summary.md`, `lead-summary.md`, or `decisions.md`.
