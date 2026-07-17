# Security

This repository is a sample Codex configuration. It contains agent definitions, plugin skills, hooks, rules, and documentation. It does not contain production application code or datasets.

## Threat Model

### Shared Filesystem Access

Codex subagents operate in the same repository and inherit the active sandbox and approval policy. File boundaries in this workflow are enforced by task prompts, spec artifacts, review, and human oversight.

Mitigations:

- Keep tasks file-disjoint within a wave.
- Require agents to report before editing outside their assigned scope.
- Run independent `review-agent` passes before accepting a wave.
- Limit the entire team run to three review synthesizer spawns. Replacements and interrupted retries consume the same budget; cycle 3 is terminal.
- Inspect `git diff --name-only` before committing or shipping changes.

### Hook Execution

The hooks in `.codex/hooks` are local Python subprocesses invoked by Codex lifecycle events. They run with the user's privileges and outside normal tool-call prompts once trusted.

Mitigations:

- Review the hook source before trusting it with `/hooks`.
- Hooks use only the Python standard library.
- Hooks are fail-open; hook failures should not trap a session.
- Logged payloads are filtered to a small allowlist. Session events use `~/.codex/team-logs`; subagent lifecycle events honor `$CODEX_HOME/team-logs` and otherwise use `~/.codex/team-logs`.
- Parallel subagent start/stop events use a file lock around log rotation and append operations to prevent writer races.

### Command Risk

Rules in `.codex/rules/codex-agent-team.rules` gate selected high-risk commands, including force pushes, hard resets, infrastructure deploys, and destroys.

Mitigations:

- Keep Codex sandboxing and approvals enabled.
- Prefer read-only, dry-run, plan, synth, diff, and describe commands before mutating commands.
- Do not use blanket approval modes for unknown repositories or production-like environments.

### Plugin Trust

The repo-scoped plugin packages skills and prompt shortcuts. Installing a plugin makes those workflows available to Codex.

Mitigations:

- Inspect `plugins/codex-agent-team/.codex-plugin/plugin.json` and every `SKILL.md`.
- Install from the checked-in repo marketplace only after review.
- Do not add MCP servers, app integrations, or executable scripts without separate review.

### Unbounded Review Loops

Repeated review and fix waves can consume resources indefinitely or leave
teammates running after useful work has stopped.

Mitigations:

- Count a review cycle when its synthesizer is spawned.
- Share one maximum three-cycle budget across all waves, reviewers,
  replacements, retries, sessions, and review files.
- Permit fix waves only after cycles 1 and 2.
- Treat a cycle 3 non-PASS result as terminal: stop automatic fixes and reviews,
  close active agents, preserve evidence, and report BLOCKED.

### Credentials And Production Resources

This sample intentionally excludes local provider config, auth files, secrets, and cloud credentials.

Mitigations:

- Never commit `~/.codex/auth.json`, provider credentials, API keys, tokens, or machine-specific paths.
- Treat unknown accounts, stages, clusters, and workspaces as production.
- Use least-privilege credentials and prefer read-only investigation.
- Require explicit user direction and an impact statement before destructive operations.

## User Responsibilities

- Review and adapt all agent instructions before use.
- Keep project and global Codex config scoped to the environment.
- Review all plugin, hook, and rule changes before trusting them.
- Maintain legal, privacy, and security approvals for Codex and any added integrations.
- Validate generated code and infrastructure with normal engineering review.

## Reporting Security Issues

Do not file public issues for sensitive vulnerabilities. Report issues through the maintainer's preferred private security channel for the public repository where this sample is published.
