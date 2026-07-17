# Codex Agent Team Sample

A shareable sample configuration for a hybrid Codex development team. It combines project-scoped custom agents, a repo-local plugin, prompt shortcuts, lifecycle hooks, command rules, and spec templates for a plan-build-review workflow.

Jump to [Quick Start](#quick-start).

> This repository is a sample configuration, not a production-ready control plane. Review every agent instruction, hook, rule, plugin file, and security note before using it on real projects.

## Overview

![Architecture Diagram](docs/architecture-diagram.png)

The sample is built around a main-thread coordinator and five optional role agents:

| Agent | Role | Model | Reasoning Effort | Primary Use |
| --- | --- | --- | --- | --- |
| `fullstack-agent` | Lead coordinator | `openai.gpt-5.6-sol` | xhigh | Specs, work splitting, delegation, spawn-plan generation, and review consolidation |
| `coding-agent` | Implementation engineer | `openai.gpt-5.6-terra` | xhigh | Scoped production code, tests, refactors, and fixes |
| `devops-agent` | Infrastructure and delivery specialist | `openai.gpt-5.6-terra` | high | CI/CD, containers, IaC, environment wiring, and runbooks |
| `review-agent` | Independent reviewer | `openai.gpt-5.6-sol` | max | PASS/FAIL review for bugs, regressions, security, and missing verification |
| `sa-agent` | AWS Solutions Architect teammate | `openai.gpt-5.6-terra` | max | Architecture, reliability, cost, security, and operational design |

These explicit IDs preserve the approved setup. The public repo intentionally
does not copy the private `model_provider`, credentials, region, profile, or
project-trust configuration; adopters must configure a provider that exposes
these model IDs. `.codex/config.toml` also defaults the main thread to
`openai.gpt-5.6-sol` at `xhigh`.

The public repository intentionally excludes `test-suite-runner`; use each
project's native test commands or add a local report-only role when that
specialization is needed. This keeps the published team focused on planning,
implementation, delivery, architecture, and independent review.

The reusable workflow lives in the `codex-agent-team` plugin under `plugins/codex-agent-team`. The custom agents live in `.codex/agents` because Codex custom agents are project or user configuration files rather than ordinary plugin contents. The sample also includes AWS security review guidance, concurrent external-fetch guidance, git workflow guidance, AWS Core/AWS Data Analytics/Superpowers plugin routing, and project-scoped MCP entries for AWS IaC help, Context7, and DeepWiki.

## Mental Model

Codex does not need a large team for every request. The default coordinator is still the main Codex thread. Use role agents when the work benefits from parallelism, role specialization, or a dedicated review gate.

The workflow has three practical rules:

1. Put durable planning artifacts in `.codex/specs/<slug>/`.
2. Split parallel work by files or ownership boundaries.
3. Treat review as a separate gate with one non-resetting three-cycle budget for the entire run.

This sample does not provide a shared task database. Coordination happens through explicit prompts, repo-local spec files, and main-thread consolidation.

## Parallel Worker Pools

The installed team can run multiple instances of the same role when the work is genuinely file-disjoint. The public sample config sets `.codex/config.toml` to `max_threads = 14` and `max_depth = 2`, which leaves room for the largest intended first-level worker pool and explicit recursive delegation. The main Codex thread is the preferred lead; `fullstack-agent` can also produce a spawn plan when the user explicitly asks for a lead profile.

| Role | Maximum Parallel Instances | Naming Pattern | Use |
| --- | ---: | --- | --- |
| `coding-agent` | 6 | `coding-1` through `coding-6` | Product code, tests, refactors, and fixes split by file or module ownership |
| `devops-agent` | 2 | `devops-1`, `devops-2` | Independent CI/CD, infra, environment, container, or runbook scopes |
| `review-agent` | 4 | `review-1` through `review-4`, or scope names like `review-api` | Parallel review of separate modules, layers, or changed file sets |
| `sa-agent` | 1 | `sa-1` or a scope name | Architecture, reliability, cost, operations, and AWS design advice |

These are ceilings, not quotas. Use fewer agents when there are fewer independent scopes, and serialize any work that must touch the same files. Codex does not provide Claude-style shared task tools in this workflow, so the coordinator assigns each spawned instance an explicit name, file scope, expected output, and verification command.

The earlier disposable smoke project has been removed. The current GPT-5.6
matrix, global review budget, and hook locking must be validated in the
adopter's own sandbox before production use.

## How The Workflow Runs

For non-trivial work, the flow is:

1. Capture requirements in `.codex/specs/<slug>/requirements.md` or create an initial `spec.md`.
2. Create or refine `spec.md`, `design.md`, and `tasks.md`.
3. Partition tasks into small, file-disjoint waves.
4. Spawn role agents only for slices that can proceed independently.
5. Give each spawned agent an explicit prompt with its role, spec path, file scope, expected output, and verification command.
6. Wait for all requested agents, then consolidate their results in the main thread or `fullstack-agent`.
7. Run a dedicated `review-agent` pass and consume the next whole-run cycle when its synthesizer is spawned.
8. A FAIL in cycle 1 or 2 may create a scoped fix wave. Cycle 3 is terminal; preserve evidence and report BLOCKED rather than spawning cycle 4.

Specs created during real work are ignored by `.gitignore`; they are runtime project artifacts, not part of this reusable sample.

## When To Use Each Agent or Skill

| Situation | Agent or Skill | Notes |
| --- | --- | --- |
| Starting from a rough idea | `team-brainstorm` | Produces `.codex/specs/<slug>/requirements.md` before deeper planning. |
| Planning a substantial feature | `fullstack-agent` with `team-spec-workflow` | Use when task splitting, artifacts, or review loops matter. |
| Implementing scoped app behavior | `coding-agent` | Give exact files, acceptance criteria, and verification commands. |
| Updating CI/CD, IaC, deployment config, or runbooks | `devops-agent` | Prefer plan, synth, diff, lint, dry-run, or non-mutating validation. |
| Reviewing a change | `review-agent` | Must lead with findings and return PASS or FAIL. |
| Evaluating architecture, reliability, cost, or operations | `sa-agent` | Useful before large build waves or production-impacting design choices. |
| Reviewing AWS resource security | `aws-security-guidelines` | Use for AWS IaC, deployment handoffs, data security controls, and production readiness. |
| Implementing many independent external calls | `concurrent-cached-fetch` | Adds bounded concurrency and content-keyed disk caching guidance. |
| Preparing branches, commits, or PR handoffs | `git-workflow` | Keeps git usage non-interactive and aligned with Conventional Commits. |

## Prerequisites

- Codex installed and authenticated.
- Python 3.11+ on `PATH` for the complete validation suite. The hooks themselves
  use only the Python standard library and remain compatible with Python 3.8+.
- A git repository root. Hook commands resolve repo-local paths with `git rev-parse --show-toplevel`.
- A trusted Codex project. Project `.codex` config, agents, hooks, and rules load only after you trust the project.
- For the AWS-optimized path, install and enable `aws-core@agent-toolkit-for-aws`, `aws-data-analytics@agent-toolkit-for-aws`, and `superpowers@openai-curated`. The sample `.codex/config.toml` reflects those enabled plugins.
- Optional: organization approval for Codex, OpenAI usage, plugin distribution, hooks, and any future MCP/server integrations.

## Quick Start

1. Clone or copy this repository.

2. Open Codex from the repository root and mark the project trusted when prompted.

3. Register the repo marketplace:

```bash
codex plugin marketplace add /absolute/path/to/sample_codex_agent_team
```

4. Open `/plugins`, switch to the `Sample Codex Agent Team` marketplace, and install `Codex Agent Team`.

5. Install or enable the companion plugins if your environment has access to their marketplaces:

```text
aws-core@agent-toolkit-for-aws
aws-data-analytics@agent-toolkit-for-aws
superpowers@openai-curated
```

6. Start a new Codex thread so plugin skills, commands, and custom agents are discoverable.

7. Start with an explicit workflow prompt:

```text
Use the Codex hybrid team to plan this feature. Create a .codex/specs plan, split implementation into file-disjoint scopes, spawn role agents where useful, and run an independent review wave.
```

For a rough idea, use the brainstorm command or skill:

```text
Use $team-brainstorm for: <idea>
```

For an existing spec, use:

```text
Use $team-spec-workflow for .codex/specs/<slug>. Build the next file-disjoint wave, then run review.
```

### Personal Marketplace Install

If you want this sample to load from your default personal Codex marketplace instead of registering the repo marketplace, use the installer script:

```bash
python3 scripts/install_personal_plugin.py --refresh-cache
```

The script updates `~/.agents/plugins/marketplace.json`, creates the canonical `~/plugins/codex-agent-team` symlink to this repo's `plugins/codex-agent-team`, and refreshes the installed plugin cache with `codex plugin add codex-agent-team@personal`.

This path matters: in the default personal marketplace, `./plugins/codex-agent-team` resolves to `~/plugins/codex-agent-team`, not to `~/.codex/plugins/codex-agent-team` and not to `~/.agents/plugins/plugins/codex-agent-team`. Do not also symlink the plugin skills into `~/.agents/skills`; duplicate discovery can surface duplicate skill selectors. If skills or role agents are present on disk but missing in a new Codex thread, verify the canonical symlink and rerun the installer.

If `~/plugins/codex-agent-team` already points to an older or private copy that you intentionally want to replace with this public sample, rerun with:

```bash
python3 scripts/install_personal_plugin.py --force --refresh-cache
```

## Common Usage Prompts

Create requirements from an idea:

```text
Use $team-brainstorm for a small internal dashboard that tracks service deployment health, owners, and stale alarms.
```

Plan a feature before coding:

```text
Use the Codex hybrid team for this feature. Create .codex/specs/deployment-health/, write spec.md, design.md, and tasks.md, then propose the first implementation wave before editing code.
```

Run parallel implementation:

```text
Use fullstack-agent as the coordinator. Split the work in .codex/specs/deployment-health/tasks.md into file-disjoint coding and devops scopes. Spawn up to 6 coding-agent instances and up to 2 devops-agent instances only where the files do not overlap, wait for all of them, and consolidate.
```

Run a focused review:

```text
Use review-agent to review the changes against .codex/specs/deployment-health/. If the changed files are separable, split review across up to 4 review-agent instances. Return Critical, Warning, Suggestion, Tests, and Verdict.
```

Request architecture advice:

```text
Use sa-agent to review the proposed design in .codex/specs/deployment-health/design.md for reliability, operational risk, cost, and security. Write findings to sa-review.md.
```

Audit your Codex setup:

```text
/optimize-my-codex
```

Scope the audit to one area:

```text
/optimize-my-codex agents
/optimize-my-codex hooks
/optimize-my-codex plugins
```

## Repository Layout

```text
.
|-- .agents/plugins/marketplace.json     # Repo marketplace exposing the plugin
|-- .codex/
|   |-- agents/                          # Custom Codex subagent roles
|   |-- config.toml                      # Shared subagent thread/depth defaults
|   |-- hooks.json                       # Repo-relative lifecycle hook wiring
|   |-- hooks/                           # Fail-open session/subagent loggers
|   `-- rules/                           # Command approval rules for risky operations
|-- plugins/codex-agent-team/
|   |-- .codex-plugin/plugin.json        # Plugin manifest
|   |-- commands/                        # Prompt shortcuts
|   `-- skills/                          # Team workflow skills
|-- docs/design.md                       # Architecture and design notes for this sample
|-- docs/specs/templates/                # Starting templates for .codex/specs work
|-- scripts/install_personal_plugin.py   # Optional personal-marketplace installer
|-- scripts/test_prompt_invariants.py    # Five-agent prompt and matrix regressions
`-- SECURITY.md                          # Threat model and user responsibilities
```

## Key Concepts

### Agents

Agents are `.toml` files in `.codex/agents`. Each file defines a `name`,
`description`, explicit `model`, `model_reasoning_effort`, optional nickname
candidates, and detailed GPT-5.6-oriented developer instructions. The
descriptions tell Codex when a role is appropriate; the full prompts preserve
role ownership, approval boundaries, learned failure modes, required evidence,
output contracts, and stop conditions.

The prompts intentionally constrain agents to their assigned scope:

- `fullstack-agent` owns requirements, contracts, file-disjoint waves, worker
  liveness, consolidation, closure, and the whole-run three-cycle review budget;
  it returns a Spawn Plan when nested delegation is unavailable.
- `coding-agent` may run as `coding-1` through `coding-6`; each instance follows
  exact-file ownership, TDD/debugging routes, interface contracts, CI-blocking
  verification, and task-local documentation close-out.
- `devops-agent` may run as `devops-1` or `devops-2`; each instance checks
  caller-input precedence, pipeline status, parsed-output isolation,
  authoritative state backends, teardown residue, rollback, and open live
  validation.
- `review-agent` may run as one synthesizer plus up to three analysts; analysts
  return evidence-backed slice findings, while only the synthesizer owns
  `review.md` and the PASS/FAIL verdict.
- `sa-agent` covers all six Well-Architected pillars and produces concrete
  current-source, ownership, rollout, rollback, cost, and residual-risk
  handoffs rather than generic advice.

Prompt optimization in this repository is behavior-preserving, not a line-count
minimization exercise. Shorter text is not considered an improvement when it
removes a measured safeguard, role contract, verification requirement, or stop
condition. Reusable procedure stays in progressively loaded skills so detailed
role prompts remain focused on role-specific failure prevention.

### Plugin

The repo-local plugin lives at `plugins/codex-agent-team`. Its manifest points Codex at the `skills/` directory and exposes prompt shortcuts under `commands/`.

Install it from the repo marketplace when you want the reusable workflow in a Codex session. Keep the plugin small and reviewable: the plugin itself does not bundle executable MCP servers, app integrations, dependency installers, or network scripts. Project-scoped MCP server configuration lives separately in `.codex/config.toml`.

### Skills

Skills are reusable instructions that the main thread or agents load on demand.

| Skill | Purpose |
| --- | --- |
| `team-brainstorm` | Convert a rough idea into `.codex/specs/<slug>/requirements.md`. |
| `team-spec-workflow` | Drive spec artifacts, task waves, delegation, and review loops. |
| `team-coordination` | Write explicit subagent prompts with file boundaries and verification expectations. |
| `team-review-cycle` | Maintain one synthesizer-owned review history and a global three-cycle PASS/FAIL gate. |
| `team-documentation` | Keep README, runbook, architecture, API, and spec docs aligned. |
| `aws-security-guidelines` | Review AWS services for encryption, TLS, logging, tagging, IAM, and production data controls. |
| `concurrent-cached-fetch` | Add bounded concurrency and disk caching for independent external fan-out calls. |
| `git-workflow` | Use non-interactive git commands, Conventional Commits, branch naming, pre-push checks, and conflict handling. |
| `optimize-my-codex` | Audit active Codex configuration, preserve provider choices, and automatically apply an approved GPT-5.6 migration. |

The AWS security guidance strengthens AWS-facing planning and review by making data controls explicit: KMS encryption, TLS enforcement, S3 Block Public Access, access logging, data-classification tags, least-privilege IAM, production-readiness checks, and `.codex/specs/<slug>/` security evidence for durable review notes.

### Plugins And MCP Servers

The sample expects current AWS facts to come from installed AWS plugins, not from legacy standalone AWS MCP endpoints. Project-scoped MCP servers are configured in `.codex/config.toml`; plugin-provided MCP tools are supplied by the installed plugins themselves. Review these entries before use because some servers start local `uvx` or `npx` processes and may download packages or access remote documentation services.

Companion plugin routing:

| Plugin | Purpose |
| --- | --- |
| `aws-core@agent-toolkit-for-aws` | AWS service, SDK, IAM, Bedrock, serverless, containers, observability, cost, messaging, secrets, and plugin-backed current AWS facts. |
| `aws-data-analytics@agent-toolkit-for-aws` | Glue, Athena, S3 Tables, S3 Vectors, OpenSearch, data lake, ETL, catalog, analytics, and vector/search workflows. |
| `superpowers@openai-curated` | Process skills for brainstorming, planning, debugging, TDD, parallel agents, review, and verification-before-completion. |

Configured project MCP servers:

| Server | Transport | Purpose |
| --- | --- | --- |
| `awslabs_aws_iac_mcp_server` | `uvx` stdio | AWS infrastructure-as-code assistance, using `AWS_PROFILE=default`. |
| `context7` | `npx` stdio | Up-to-date library and framework documentation. |
| `deepwiki` | Streamable HTTP | Repository and documentation research through DeepWiki. |

### Commands

Prompt shortcuts live under `plugins/codex-agent-team/commands`.

| Command | Purpose |
| --- | --- |
| `/brainstorm` | Calls `team-brainstorm` to turn an idea into requirements. |
| `/launch-codex-team` | Starts the hybrid team workflow for a specified task or existing spec. |
| `/optimize-my-codex` | Audits `~/.codex` and `~/.agents` for stale config, unclear agents, hook/rule issues, skill/plugin drift, and missing current best practices. |

Commands are convenience wrappers. The same workflows can be invoked by naming the skills directly in a prompt.

Use `/optimize-my-codex` after Codex updates, model changes, plugin changes, or when a local setup feels slow, noisy, stale, or inconsistent. Pass an optional focus area such as `config`, `agents`, `hooks`, `rules`, `skills`, `plugins`, `marketplace`, or `commands` to limit the audit:

```text
/optimize-my-codex rules
```

The command presents findings and one exact migration set first, then waits for approval. Once approved, it applies the complete migration automatically without per-file confirmation and validates changed JSON, TOML, YAML, skills, plugins, hooks, and model assignments as applicable.

### Specs

Runtime specs live under `.codex/specs/<slug>/`. The sample includes templates in `docs/specs/templates/`.

Common artifacts:

| File | Purpose |
| --- | --- |
| `requirements.md` | User problem, MVP scope, constraints, and open questions. |
| `spec.md` | Requirements, assumptions, interfaces, risks, and out-of-scope boundaries. |
| `design.md` | Architecture, components, data model, infrastructure, and tradeoffs. |
| `tasks.md` | File-disjoint waves with clear acceptance and verification. |
| `review.md` | Synthesizer-owned review history, one whole-run cycle counter, and the authoritative PASS/FAIL verdict. |
| `sa-review.md` | Architecture and Well-Architected style findings. |
| `decisions.md` | Durable decision log. |
| `prd.md` | Product requirements and rollout notes when product framing is needed. |

### Hooks

Hooks are configured in `.codex/hooks.json` and implemented in `.codex/hooks`.

| Event | Script | Purpose |
| --- | --- | --- |
| `SessionStart` | `.codex/hooks/session_start.py` | Records a filtered session-start event. |
| `SubagentStart` | `.codex/hooks/subagent_lifecycle.py start` | Records a filtered subagent-start event. |
| `SubagentStop` | `.codex/hooks/subagent_lifecycle.py stop` | Records a filtered subagent-stop event. |

The hooks are intentionally lightweight:

- They use only Python standard-library modules.
- They fail open so logging problems do not trap Codex.
- They filter incoming payloads to an allowlist.
- Session events write under `~/.codex/team-logs`; subagent lifecycle events honor `$CODEX_HOME/team-logs` and otherwise use `~/.codex/team-logs`.
- They rotate each log at 1 MiB with three backups.
- Subagent lifecycle writes and rotation are serialized with a file lock so parallel start/stop events do not race.

Review and trust hooks with `/hooks` before relying on them. Disable them in stricter environments if local metadata logging is not acceptable.

### Rules

Rules in `.codex/rules/codex-agent-team.rules` keep selected high-risk commands explicit. They prompt or block operations such as:

- `git push`
- `git push --force` and `git push --force-with-lease`
- `git reset --hard`
- `git clean`
- `gh pr create`
- `python3 -m pip install`
- `cdk deploy` and `cdk destroy`
- `terraform apply` and `terraform destroy`
- `sam deploy` and `sam delete`
- `aws cloudformation deploy` and `aws cloudformation delete-stack`
- `aws s3 rm` and `aws s3 rb`
- `kubectl delete`
- `docker system prune`

Rules reduce accidental risky operations and keep dependency installs explicit. They do not replace sandboxing, code review, least-privilege credentials, project-local dependency isolation, or careful approval decisions.

## Writing Good Subagent Prompts

Subagent prompts should be concrete enough that the agent can finish without inventing scope.

Include:

- Role agent to use.
- Instance name when using a pool, such as `coding-3`, `devops-1`, or `review-api`.
- Spec path and task or wave reference.
- Exact file scope.
- Expected output artifact or summary.
- Verification command or concrete evidence expected.
- Instruction not to edit outside the listed scope.
- Reminder that peer instances may be editing nearby files concurrently.
- Whether the coordinator should wait for all agents before consolidating.

Example:

```text
Use coding-agent.
You are coding-3, one of up to 6 parallel coding instances.

Spec: .codex/specs/deployment-health/
Scope: implement the API response types in src/api/types.ts and tests in src/api/types.test.ts.
Do not edit files outside that scope. Other coding/devops instances may be running concurrently; do not overwrite their work.

Acceptance:
- Exports match the contract in spec.md.
- Invalid state names are rejected.
- Existing callers keep compiling.

Verify:
- npm test -- src/api/types.test.ts
- npm run typecheck

Return:
- Summary of changes
- Commands run and outcomes
- Any required scope expansion
```

## Operating Safely

Use this sample with normal production safeguards:

- Treat unknown accounts, stages, clusters, and workspaces as production.
- Prefer read-only, list, describe, get, plan, synth, diff, and dry-run operations before mutating commands.
- Do not inline secrets in prompts, code, docs, config, tests, or command examples.
- Keep runtime specs, logs, local state, `.env` files, and provider credentials out of git.
- Use least-privilege credentials for investigation.
- Require explicit user direction and an impact statement before destructive operations.
- For ops smoke tests, require a disposable or non-production target, bounded retries and timeouts, abort criteria, and evidence capture before any external endpoint checks.

## Troubleshooting

If a subagent fails before doing work with an engine routing error such as `404 Not Found: Engine not found`, close that failed agent and retry the same bounded scope. If retries keep failing, use a currently supported role-appropriate model only after confirming availability, and record the override in the relevant spec or review artifact.

## Customization

- Add or edit custom agents in `.codex/agents/*.toml`.
- Add workflow skills under `plugins/codex-agent-team/skills/<skill>/SKILL.md`.
- Add prompt shortcuts under `plugins/codex-agent-team/commands/`.
- Add more marketplace entries in `.agents/plugins/marketplace.json`.
- Adjust subagent concurrency and recursion defaults in `.codex/config.toml`.
- Keep machine-specific provider settings, secrets, model providers, local paths, installed plugin caches, and runtime artifacts out of this repo.

When adding a new role agent, update:

1. `.codex/agents/<name>.toml`
2. This README's role tables
3. `docs/design.md`
4. Relevant skills or prompt shortcuts

## Validation

Useful checks after editing:

```bash
python3 scripts/test_prompt_invariants.py -v
python3 .codex/hooks/test_subagent_lifecycle.py -v
python3 -m py_compile .codex/hooks/session_start.py .codex/hooks/subagent_lifecycle.py
python3 -m json.tool .codex/hooks.json
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/codex-agent-team/.codex-plugin/plugin.json
python3 scripts/install_personal_plugin.py --dry-run
python3 -c "import pathlib, tomllib; files=[pathlib.Path('.codex/config.toml'), *pathlib.Path('.codex/agents').glob('*.toml')]; [tomllib.loads(p.read_text()) for p in files]"
ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f) }; puts "yaml ok"' plugins/codex-agent-team/skills/*/agents/openai.yaml
```

The prompt invariant suite asserts the five-agent public model/effort matrix,
confirms that `test-suite-runner` remains absent, and protects the lifecycle,
review, role, skill, command, and README contracts restored for GPT-5.6. The
hook regression covers malformed payloads, allowlist filtering, fail-open
behavior, and race-safe rotation through the persistent sidecar lock.

For plugin manifest validation, use Codex's bundled `plugin-creator` validator if available:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-agent-team
```

To check that Codex can load the project prompt/config context:

```bash
codex debug prompt-input "validate repo config"
```

If this command fails under a strict sandbox, rerun it in a normal shell or through your approved local Codex execution path.

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| Skills or commands are not visible | Session started before plugin install or enablement | Restart the Codex thread after installing the plugin. |
| Personal marketplace install shows the plugin but skills/agents are missing | `~/.agents/plugins/marketplace.json` points at `./plugins/codex-agent-team`, but `~/plugins/codex-agent-team` does not resolve to this repo's plugin | Run `python3 scripts/install_personal_plugin.py --refresh-cache`, then start a new Codex thread. |
| Duplicate team skills appear in selectors | Plugin skills were also exposed through direct `~/.agents/skills` symlinks or a direct `~/.agents/plugins/plugins/codex-agent-team` symlink | Remove the direct symlinks, keep `~/plugins/codex-agent-team` as the personal-marketplace source, refresh the plugin cache, and start a new Codex thread. |
| Custom agents are missing | Project is not trusted or Codex was not opened at repo root | Trust the project and restart from the repository root. |
| Hooks do not run | Hooks are not trusted, project is not a git repo, or hook path resolution failed | Review `/hooks`, ensure the repo has a git root, and inspect `.codex/hooks.json`. |
| Subagents edit overlapping files | Task scopes were not file-disjoint | Stop the wave, reconcile changes in the main thread, then create narrower tasks. |
| Review keeps failing | Findings are real or acceptance criteria are ambiguous | Convert findings into a fix wave and clarify the spec before more edits. |
| Plugin validation fails | Manifest schema or path issue | Check `plugins/codex-agent-team/.codex-plugin/plugin.json` and rerun the validator. |

## Legal And Security Review

Before adopting this sample for organization use, complete your own approvals:

| Area | Status |
| --- | --- |
| Codex/OpenAI usage approval | To be completed by adopter |
| Plugin distribution approval | To be completed by adopter |
| Hook execution review | To be completed by adopter |
| Local metadata logging approval | To be completed by adopter |
| MCP/server integrations | Review project-scoped entries in `.codex/config.toml` before trusting or enabling |
| Production or cloud-resource access | To be completed by adopter |

See `SECURITY.md` for the threat model.

## License

This sample is licensed under the MIT-0 License. See `LICENSE`.
