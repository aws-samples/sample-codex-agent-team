---
name: team-coordination
description: Coordinate the hybrid Codex team with explicit subagent prompts, file-disjoint task waves, worker pools, synthesizer-led review, and main-thread consolidation. Use when parallel work or role-based delegation is requested.
---

# Team Coordination

Use this skill when the user wants a lead/member workflow, role specialization, or parallel delegation.

## Core Constraint

Codex coordination is explicit. Do not assume Claude-style task-store tools exist.

Use:
- shared `.codex/specs/<slug>/` artifacts
- precise subagent prompts
- exact file scopes
- lead consolidation in the main thread

## Role Split

- `fullstack-agent`: planning, spec upkeep, task partitioning, review arbitration, documentation close-out.
- `coding-agent`: product code, tests, refactors, focused fixes.
- `devops-agent`: infrastructure, CI/CD, deployment, containers, environment wiring, runbooks.
- `review-agent`: correctness, security, regression, performance, missing-test review.
- `sa-agent`: architecture, reliability, cost, security posture, operations.

## Worker Pools

Size pools to the widest independent wave:

| Role | Cap | Names | Use |
| --- | ---: | --- | --- |
| `coding-agent` | 6 | `coding-1` ... `coding-6` | File-disjoint code/tests/refactors/fixes |
| `devops-agent` | 2 | `devops-1` ... `devops-2` | File-disjoint CI/CD/infra/env/runbook work |
| `review-agent` | 4 | `review-1` ... `review-4` | One synthesizer plus optional analysts |
| `sa-agent` | 1 | `sa-1` | Architecture/cost/reliability/security |

Caps are not quotas. Spawn fewer agents when there are fewer independent scopes.

## Prompt Requirements

Every subagent prompt must include:
- role agent to use
- instance name
- spec path
- wave/task reference
- exact file scope
- acceptance criteria
- verification command
- expected output
- warning not to edit outside listed files
- warning that peer agents may be editing nearby files
- whether the lead should wait for all agents before consolidation

Example:

```text
Use `coding-agent`.
You are `coding-2`, one of up to 6 parallel coding instances.
Context: `.codex/specs/orders-api/spec.md`, `design.md`, and Wave 2 in `tasks.md`.
Scope: implement only `src/orders/handler.ts` and `src/orders/handler.test.ts`.
Acceptance: handler validates input and returns the response shape from `spec.md#interfaces`.
Run: `npm test -- orders/handler`.
Do not edit files outside this scope; other coding/devops instances may be running concurrently.
Return files changed, verification result, blockers, and residual risks.
```

## Parallelism Rules

- Parallelize read-heavy exploration freely.
- Parallelize write-heavy work only when file scopes do not overlap.
- Author many small tasks instead of a few broad tasks.
- Keep waves wide and barriers few.
- Front-load shared interfaces.
- Keep coding and devops work file-disjoint.
- Use worktrees only for a documented overlap that cannot be decomposed.

## Review Coordination

Small review:
- Spawn one `review-agent`.
- It acts as synthesizer and owns the verdict.

Parallel review:
- Spawn `review-1` as Synthesizer.
- Spawn `review-2` through `review-4` as Analysts when there are independent slices.
- Analysts write no files. They return structured findings to the synthesizer.
- The synthesizer writes `review.md`, checks cross-slice consistency, and emits the single wave verdict.

Analyst prompt must include:
- `Role: Analyst`
- synthesizer name
- slice files
- cycle number
- advisory slice verdict only

Synthesizer prompt must include:
- `Role: Synthesizer`
- analyst names and expected slices
- instruction to wait for analysts or report missing analyst results
- instruction to author only `review.md`

## Consolidation

After each wave:
- Summarize subagent outcomes.
- Update `tasks.md` with `[x]`, `[!]`, or remaining work.
- Record decisions, blockers, deviations, and accepted risks in `decisions.md`.
- If review FAILs, create a fix wave.
- If review cannot run, report an open gate instead of fabricating PASS.

## Degraded Workflow

If required subagent capability is unavailable:
1. State the exact missing capability or failed call.
2. Explain what is lost: parallelism, adversarial review, or isolation.
3. Ask for explicit user approval before proceeding single-threaded.
4. If approved, mark any self-review as `SELF-REVIEW. Real review pending.`
