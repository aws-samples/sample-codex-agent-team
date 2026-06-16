---
name: team-coordination
description: Coordinate the hybrid Codex team with explicit subagent prompts, file-disjoint task waves, and main-thread consolidation. Use when parallel work or role-based delegation is requested.
---

# Team Coordination

Use this skill when the user wants the Codex team to work in a lead/member pattern instead of a single thread doing everything.

## Key Constraint

Do not assume Claude-style task tools exist. Coordination is explicit:

- shared spec artifacts in `.codex/specs/<slug>/`
- narrow subagent prompts
- clear file boundaries
- lead consolidation in the main thread

## Recommended Role Split

- `fullstack-agent`: planning, spec upkeep, task partitioning, review arbitration
- `coding-agent`: product code and tests
- `devops-agent`: infrastructure, CI/CD, deployment, env wiring
- `review-agent`: correctness, security, regression, tests
- `sa-agent`: architecture, reliability, cost, operations

## Parallel Worker Pools

Use the same pool shape as the Claude Code sample, translated to Codex's explicit subagent prompts:

| Role | Cap | Naming | Use |
| --- | ---: | --- | --- |
| `coding-agent` | 6 | `coding-1` ... `coding-6` | File-disjoint product code, tests, refactors, and fixes |
| `devops-agent` | 2 | `devops-1` ... `devops-2` | File-disjoint CI/CD, infra, environment, and runbook work |
| `review-agent` | 4 | `review-1` ... `review-4` or scope names like `review-api` | Parallel per-scope review |
| `sa-agent` | 1 | `sa-1` or a scope name | Architecture, reliability, cost, operations |

These are ceilings, not quotas. Spawn fewer agents when the wave has fewer independent scopes. Do not spawn idle agents.

Codex does not provide Claude-style `TeamCreate`, `TaskCreate`, `TaskUpdate`, or a shared task queue in this workflow. The coordinator must assign each spawned Codex subagent an explicit instance name, file scope, expected output, and verification command. Use `.codex/specs/<slug>/tasks.md` as the durable plan and record consolidation notes there or in `decisions.md`.

## Prompt Shape For Spawned Agents

Every lead-authored subagent prompt should include:

- the role to use
- the instance name, such as `coding-2`, `devops-1`, or `review-api`
- the spec path
- the exact file scope
- the expected output
- the verification expectation
- a warning that peer instances may be editing nearby files concurrently
- whether the lead should wait for all agents before consolidating

Example structure:

```text
Use `coding-agent`.
You are `coding-2`, one of up to 6 parallel coding instances.
Scope: implement the parser changes in `src/parser.ts` and `src/parser.test.ts`.
Context: `.codex/specs/log-parser/spec.md` and Wave 2 in `tasks.md`.
Deliver: code changes plus a short summary of what changed, tests run, and residual risks.
Do not edit files outside the listed scope.
Other coding/devops instances may be running concurrently; do not overwrite their work.
```

## Parallelism Rules

- Parallelize read-heavy exploration freely.
- Parallelize write-heavy work only when file scopes do not overlap.
- Author wide waves: many small file-disjoint tasks in the same wave beat a few broad tasks.
- Use up to 6 coding instances and 2 devops instances only when there are enough independent implementation scopes.
- Keep one review agent per scope when the changed file sets are meaningfully separable.
- Use up to 4 review instances for disjoint review scopes; each reviewer owns exactly one scope and one review artifact if artifacts are requested.
- Ask the main thread to wait for all spawned agents before consolidating.

## Ops Smoke And Deploy Guardrails

For smoke, staging, deploy, or other environment-facing tasks, put these requirements into the task acceptance criteria and subagent prompt:

- disposable or explicitly non-production target validation
- required environment variables or parameters
- target allowlist or production denylist when endpoint checks are involved
- bounded retry count, timeout, delay, and abort criteria
- evidence capture: command output, target classification, candidate artifact or build identifier, and final PASS or FAIL

If review or SA finds missing guardrails, create a fix wave, rerun the affected review scope, and update the lead summary or review summary.

## Spawn Failure Handling

If subagent creation fails before execution with a model or engine routing error such as `404 Not Found: Engine not found`:

- close the failed agent
- retry the same bounded scope without changing file ownership
- if inherited-model retries keep failing, retry with a supported explicit model override
- record the operational note in the relevant spec artifact

## Consolidation Rules

- Summarize subagent outcomes rather than replaying raw transcripts.
- Update `.codex/specs/<slug>/tasks.md`, `decisions.md`, and review artifacts after each wave.
- Record blockers as explicit decisions or open questions so the next wave has stable context.
- If any review scope reports FAIL, the full wave fails. Convert findings into a fix wave and review again.
