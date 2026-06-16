# Design: Codex Agent Team Sample

This repository packages a reusable Codex team workflow without copying personal Codex runtime state.

## System Overview

```text
User request
  -> main Codex thread or fullstack-agent
  -> .codex/specs/<slug>/ artifacts
  -> coding/devops/sa agents for scoped, file-disjoint work
  -> review-agent pool for PASS/FAIL review
  -> main thread consolidation
```

## Component Responsibilities

| Component | Responsibility |
| --- | --- |
| `.codex/agents` | Project-scoped custom agent definitions for Codex subagent workflows |
| `plugins/codex-agent-team` | Installable plugin containing reusable team skills and prompt shortcuts |
| `.agents/plugins/marketplace.json` | Repo marketplace so Codex can discover and install the plugin |
| `.codex/hooks` | Fail-open lifecycle logging for sessions and subagents |
| `.codex/rules` | Guardrails for commands that should remain explicit approvals |
| `docs/specs/templates` | Starter artifacts for spec-driven work |

## Agent Defaults

| Agent | Reasoning Effort | Primary Responsibility |
| --- | --- | --- |
| `fullstack-agent` | `xhigh` | Spawned lead for specs, work splitting, delegation, and review-loop consolidation |
| `coding-agent` | `high` | Scoped production code, tests, refactors, and fixes |
| `devops-agent` | `high` | CI/CD, containers, infrastructure, environment wiring, and runbooks |
| `review-agent` | `xhigh` | Independent PASS/FAIL review for bugs, regressions, security, and missing verification |
| `sa-agent` | `high` | Architecture, reliability, cost, and operational design guidance |

## Parallel Pool Model

The team supports multiple same-role instances when a wave has enough independent file scopes:

| Role | Cap | Naming | Coordination Rule |
| --- | ---: | --- | --- |
| `coding-agent` | 6 | `coding-1` ... `coding-6` | Each instance owns one implementation slice and must not edit outside it. |
| `devops-agent` | 2 | `devops-1`, `devops-2` | Each instance owns one delivery, CI/CD, infra, environment, or runbook slice. |
| `review-agent` | 4 | `review-1` ... `review-4`, or scope names | Each reviewer owns one changed file set and one review artifact if artifacts are requested. |
| `sa-agent` | 1 | `sa-1` or a scope name | Architecture advice is intentionally not pooled by default. |

The repo config uses `max_threads = 14` and `max_depth = 2`. The thread limit supports a spawned lead plus the maximum intended first-level role pool. The depth limit allows nested delegation, but the agent prompts instruct spawned agents not to spawn their own agents unless the user explicitly asks for recursive delegation.

Codex does not provide a shared queue for this workflow. `tasks.md` is the durable plan, and every subagent prompt must include an explicit instance name, file scope, expected output, verification expectation, and warning not to overwrite peer work.

## Smoke-Test Evidence

The max-pool shape was smoke-tested in a disposable project with six coding scopes, two devops scopes, four review scopes, one SA review, and one final lead consolidation. The final project check passed, all review scopes reported PASS, and the SA rerun reported PASS after ops guardrails were added. Details are recorded in `docs/agent-pool-smoke-test.md`.

The smoke run also showed intermittent subagent submission failures before execution with an engine routing 404. The recovery path was to close the failed agent and retry the same scope; explicit `openai.gpt-5.4` model overrides completed the final reruns. This is treated as an operational runtime observation rather than a prompt or repo-configuration defect.

## Design Decisions

| Decision | Rationale |
| --- | --- |
| Keep agents in `.codex/agents` | Codex custom agents are project/user configuration files rather than ordinary plugin contents. |
| Package workflow instructions as a plugin | Plugins are the shareable distribution unit for skills and prompt shortcuts. |
| Use a repo marketplace | A checked-in `.agents/plugins/marketplace.json` lets adopters install the plugin from the repo. |
| Exclude runtime specs and logs | Specs, session logs, SQLite state, caches, and shell snapshots are per-user runtime artifacts. |
| Keep hooks project-local | Adopters can inspect, trust, or disable them with Codex's normal hook review flow. |

## Security Considerations

- Custom agents and hooks run with the user's normal Codex permissions and sandbox settings.
- Subagents share the repository filesystem. File boundaries are enforced by instruction, review, and user oversight rather than by OS isolation.
- Hooks execute local Python code and must be reviewed before trust.
- Rules reduce accidental destructive operations but do not replace sandboxing, code review, or careful approval decisions.
- Ops smoke tasks should include non-production target preflight, bounded retry and timeout behavior, abort criteria, and evidence capture before checking external endpoints.
- No secrets, provider credentials, local auth files, or machine-specific model/provider settings are included.

## Extension Points

- Add domain agents as additional `.codex/agents/*.toml` files.
- Add workflow skills under `plugins/codex-agent-team/skills`.
- Add plugin assets only when the manifest references them.
- Add MCP configuration only after documenting required authentication, data access, and legal/security review.
