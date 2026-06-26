---
name: team-spec-workflow
description: Spec-driven hybrid Codex team workflow using `.codex/specs/<slug>/` artifacts, wide file-disjoint task waves, explicit subagent handoffs, synthesizer-led review, and documentation close-out. Use for non-trivial work that needs planning, delegation, architecture decisions, or review loops.
---

# Team Spec Workflow

Use this workflow when a task spans multiple files, involves architecture decisions, affects production behavior, or benefits from role-based delegation.

## Artifact Layout

Store artifacts under `.codex/specs/<slug>/` using a short kebab-case slug.

```text
.codex/specs/<slug>/
  spec.md
  design.md
  tasks.md
  review.md
  review-summary.md
  sa-review.md
  decisions.md
  requirements.md
  security-exceptions.md
  prd/
```

Use only the files the task needs. For non-trivial team work, the normal minimum is `spec.md`, `tasks.md`, and a review artifact. Add `design.md` when architecture, data flow, infrastructure, or security details matter. Any production-impacting or AWS-heavy `design.md` must include Security Considerations.

Template sources, in order:
1. Repo-local `.codex/specs/templates/`
2. User-global `~/.codex/specs/templates/`
3. The section structures in this skill

## Spec Structure

`spec.md` should capture:
- problem and goal
- functional and non-functional requirements
- constraints and assumptions
- design decisions and alternatives
- exact interfaces and contracts
- edge cases and risks
- out of scope
- open questions

`design.md` should capture:
- architecture overview and component boundaries
- repository/module structure
- data model
- infrastructure design and outputs
- Security Considerations
- tradeoffs and alternatives
- open design questions

`decisions.md` is append-only. Use it for mid-flight ambiguity, accepted deviations, security exceptions, degraded workflows, or user-approved open gates.

## Task Format

Tasks are organized into parallel waves. Tasks in one wave can run simultaneously; waves run sequentially only when a real dependency forces a barrier.

Use this shape:

```md
## Wave 1: shared contracts
Spec ref: `spec.md#interfaces-and-contracts`
- [ ] [coding] Define API contracts | `src/api/types.ts` | Exports request/response types exactly as specified. Run: `npm test -- api-types`
- [ ] [devops] Define environment contract | `.github/workflows/ci.yml`, `docs/deploy.md` | CI and deploy docs agree on required env vars. Run: `npm run lint`
```

Task rules:
- Use `[coding]`, `[devops]`, or `[sa]` role tags.
- Include exact file paths.
- Include acceptance criteria.
- Include `Run: <command>` for verification.
- No two tasks in the same wave may write the same file.
- Keep each task self-contained and role-pure.
- Include interface contracts inline when producing or consuming shared interfaces.
- Use `[skip-verify]` only when no meaningful verification exists.
- Start a new wave only for real dependencies, not convenience.

## Parallelization

Author for a worker pool, not one worker:
- Make waves wide. Many small file-disjoint tasks beat one broad task.
- Make waves few. Pull independent work forward.
- Front-load shared contracts so consumers can run in parallel.
- Keep `[coding]` and `[devops]` scopes file-disjoint so both pools can run at once.
- Use worktrees only when overlap cannot be decomposed safely.

Pool caps:
- `coding-agent`: up to 6 instances
- `devops-agent`: up to 2 instances
- `review-agent`: up to 4 instances
- `sa-agent`: 1 instance

These are ceilings, not quotas. Spawn only enough agents for independent work.

## Delegation Model In Codex

Codex does not provide Claude-style `TeamCreate`, `TaskCreate`, `TaskUpdate`, `SendMessage`, or a shared task queue in this workflow. Coordination is explicit:

- The lead writes specs and tasks.
- The lead spawns role agents with narrow file scopes and concrete prompts.
- Each agent returns a concise summary, changed files, verification result, blockers, and residual risks.
- The lead consolidates outcomes into `tasks.md`, `decisions.md`, review artifacts, and the user-facing thread.

Each subagent prompt must include:
- role agent
- instance name
- spec path
- wave/task reference
- exact file scope
- acceptance criteria
- `Run:` command or verification expectation
- output expected
- instruction not to edit outside scope
- note that peers may be working concurrently
- whether to wait for all agents before consolidation

## Review Loop

Plan -> Build wave -> Review -> Fix if FAIL -> Documentation -> Cleanup.

For small cohesive changes, use one `review-agent` as synthesizer.

For broad changes, use parallel review:
- `review-1` is synthesizer and sole author of `review.md`.
- `review-2` through `review-4` are analysts.
- Analysts review disjoint slices and return structured findings; they write no review file.
- The synthesizer reviews cross-module consistency, deduplicates findings, writes `review.md`, and emits one PASS/FAIL verdict.

FAIL if any Critical or Warning remains, or required verification is absent. Suggestions do not block PASS.

Run at most three review cycles per wave before escalating with a concise summary of persistent issues.

## Security And AWS Acceptance

For AWS or production-impacting work, acceptance criteria should include applicable checks in priority order:

1. Encryption at rest verified.
2. Encryption in transit verified.
3. Access logging enabled.
4. Data classification tags present.
5. IAM least privilege checked.
6. Secrets stored in Secrets Manager, Parameter Store, or an approved project mechanism.

Use:
- `aws-security-guidelines` for security requirements.
- AWS Core/Data Analytics skills for service-specific workflow guidance.
- `aws-mcp` for current AWS facts and read-only checks.
- AWS IaC MCP server for CloudFormation/CDK validation, compliance, docs, and troubleshooting.

Security scan artifacts, when used, should live under `.codex/specs/<slug>/`. Accepted risks with compensating controls belong in `security-exceptions.md` or `decisions.md`.

## Completion Criteria

A wave is complete only when:
- all planned tasks are marked `[x]` in `tasks.md`
- verification commands are recorded
- review reports PASS
- docs affected by behavior/config/API/operations are updated
- blockers and deviations are recorded in `decisions.md`

The whole task is complete only after final documentation close-out and a concise user-facing summary.
