---
name: optimize-my-codex
description: Use when auditing, modernizing, or migrating active Codex configuration under a user or agent home, especially models, effort, prompts, agents, hooks, rules, skills, plugins, or marketplaces.
---

# Optimize My Codex

## Outcome

Produce an effective, valid, safer, behavior-preserving Codex setup that uses
current supported capabilities while retaining intentional provider choices,
model routing, approval boundaries, learned safeguards, hooks, and local
workflow behavior.

Optimization is not unconditional minimization. Fewer lines or tokens are not
success when they remove a measured behavior fix, failure-mode guard, role
contract, validation requirement, or stop condition. Preserve useful
verbosity unless representative evidence proves a shorter replacement is
behaviorally non-inferior.

## Scope And Authorization

Honor the user's requested focus. For a full audit, inventory every active
configuration surface:

- global and repository `AGENTS.md`
- user and trusted-project `config.toml`, profiles, features, model provider,
  sandbox, approval, projects, notifications, and UI settings
- custom agents and their discovery/config references
- hooks, hook scripts, hook tests, and event wiring
- rules or requirements files and their path scope
- user skills, skill metadata, `agents/openai.yaml`, references, scripts, and
  assets
- plugin authoritative source, manifests, commands, skills, MCP/app wiring,
  marketplace declarations, enabled/installed state, and discovery metadata
- configured MCP servers and tool routing

Distinguish configured capabilities from present/discoverable capabilities.
Record broken references and optional components instead of assuming that a
configured path is active.

Safe local inspection is authorized for an audit. Before editing, present one
exact migration and obtain approval. External writes, installs from an
untrusted source, destructive cleanup, permissions broadening, deployment, and
live-resource mutation retain their normal approval boundaries.

## Active Source Versus Generated State

Classify every path before editing.

Active source includes maintained configuration, agent definitions, skill
source, plugin source, marketplace declarations, hook source/tests, and
repository guidance that Codex loads.

Generated or historical state includes:

- versioned plugin cache and install materializations
- sessions, transcripts, logs, rollouts, and shell snapshots
- SQLite databases, indexes, and temporary files
- downloaded packages and registries
- backups, fixtures, examples, evaluation baselines, and archived copies

Do not edit generated cache directly. Locate the authoritative plugin source,
modify and validate it, update its supported cachebuster/version metadata,
reinstall through the plugin command, then compare source with installed cache.
Generated cache is evidence of what is installed, not the maintenance target.

Do not rewrite historical examples, baselines, or fixtures merely to make a
search result look current. Change them only when the user explicitly includes
them or their active use is proven.

## Preserve Before Recommending

Before proposing changes, record:

- configured provider/backend and provider-specific model ID style
- exact main and agent model/effort matrix
- approval policy and sandbox settings
- agent limits, context/compaction, hooks, rules, MCP, plugins, marketplaces,
  project trust, and notifications
- current line and word measurements for prompt-bearing files
- hashes or byte snapshots of configuration that must remain unchanged
- installed plugin versions and authoritative source paths
- representative baseline behavior for prompts being materially rewritten

Never change the provider implicitly. Preserve exact model IDs when the user
specified them. A model migration request does not authorize changing auth,
backend, SDK, shell environment, tools, approvals, or unrelated provider
settings.

Use a deep comparison for structured configuration, not a loose text search.
Parse TOML, JSON, and YAML and compare nested keys, types, arrays, and exact
values. Use a byte comparison when the requirement is no config change.

## Current Documentation Route

Use current official Codex and model documentation when schema, supported
surfaces, discovery, model availability, prompting, or plugin behavior matters.
For broad Codex self-knowledge, use the `openai-docs` Codex manual helper and
targeted manual sections before relying on memory. Use official OpenAI docs for
remaining current gaps.

Explicit user targets override generic model recommendations. When public docs
do not establish a private/provider-specific slug, preserve the requested value
and report the live availability check as open rather than inventing support.

## GPT-5.6 Routing Policy

| Model | Appropriate workload |
| --- | --- |
| Sol | Ambiguous, high-value, architecture, security, deep review, polished frontend, or complex tool-driven work |
| Terra | Everyday implementation, DevOps, analysis, and efficient parallel workers |
| Luna | Clear, repeatable, structured, high-volume, extraction, transformation, or fixed test execution |

Use the configured provider's exact IDs. For Amazon Bedrock in this setup:

- `openai.gpt-5.6-sol`
- `openai.gpt-5.6-terra`
- `openai.gpt-5.6-luna`

Preserve an explicit effort matrix. When no matrix exists, start at medium and
raise effort only for a measured quality need. Reserve max for the hardest
quality-first roles. Before raising effort, check whether the prompt lacks a
success criterion, approval boundary, tool route, evidence requirement, output
contract, or validation loop.

Do not lower a user-approved effort merely to reduce token use. Model and
effort routing are independent decisions.

## Audit Method

1. Inventory active source and present/discoverable capabilities.
2. Capture before measurements and preserved fingerprints.
3. Identify conflicts, invalid schema, stale links, unsupported claims, unsafe
   broad permissions, broken discovery, duplicate ownership, context overhead,
   and model/workload mismatch.
4. Trace each prompt rule to its owning surface: global guidance, role prompt,
   triggered skill, hook, command wrapper, or repository instruction.
5. Run baseline evaluations before materially changing behavior.
6. Present findings by impact.

Use:

- High: safety, correctness, model/provider, approval, hook, discovery, or
  learned-behavior regression
- Medium: meaningful quality, maintainability, routing, context, or stale
  integration issue
- Low: cleanup or consistency with limited behavioral effect
- No Changes Needed: intentional, valid, or not proven beneficial to change

For each finding, give the exact file/key, current state, proposed value,
reason, preserved settings, validation, and rollback/restore path.

## Approval And Automatic Migration

Present one migration set containing:

- exact files and keys
- before and after values
- additions, removals, and preserved invariants
- source-versus-cache handling
- validation commands and open provider checks

Wait for exact migration approval before editing. After approval, migrate
approved configs automatically:

- re-read each target immediately before editing
- apply all approved in-scope changes without asking per file
- preserve unrelated user changes
- request renewed approval only if a target changed materially, a requested
  value is unsupported, or the necessary edit expands scope

Do not weaken `approval_policy`, sandboxing, developer instructions, hook
enforcement, or safety rules merely to make migration easier.

## Prompt And Skill Migration

For GPT-5.6 prompts:

- State role and user-visible outcome first.
- Define execution position, ownership, and approval boundaries.
- Preserve exact success criteria, evidence, output shape, and stop conditions.
- Preserve product requirements, incidents, measured failures, and learned
  behavior fixes.
- Keep role-specific failure prevention in agent prompts.
- Put reusable procedure in progressively loaded skills.
- Put durable cross-repository defaults in global `AGENTS.md`.
- Keep command wrappers thin: owning skill, `$ARGUMENTS`, durable output, and
  one load-bearing boundary.
- Translate unsupported mechanisms into real Codex spawn/wait/steer/close and
  durable-artifact behavior; do not claim unavailable capabilities.

Do not remove instructions solely because another file contains similar words.
Removal is allowed only when the replacement owner is active, reliably
triggered, semantically equivalent, and covered by regression evidence.

For every changed skill:

- validate YAML frontmatter, name, and description
- confirm the description states triggering conditions
- validate discovery metadata and `agents/openai.yaml` when present
- run a baseline pressure scenario before the edit and the matched scenario
  after the edit
- validate the skill immediately before editing another skill

For a coordinated rewrite, record baseline failures and preserved invariants
first. Compare before/after line and word counts as regression signals, not
quality targets.

## Validation Matrix

Run all applicable checks:

1. Parse changed TOML, JSON, and YAML.
2. Assert exact requested model, effort, provider, and agent-limit values.
3. Deep-compare preserved configuration against the before snapshot.
4. Validate each changed skill and plugin manifest.
5. Check cross-references, command-to-skill ownership, skill metadata, and
   discovery.
6. Test each changed hook against both success and failure cases, including
   race/lifecycle behavior when relevant.
7. Validate rules or requirements against representative allowed and denied
   cases.
8. Refresh plugins through supported commands and compare authoritative plugin
   source with installed generated cache.
9. Confirm strict Codex config loading, agent discovery, plugin enablement, and
   skill discovery.
10. Forward-test representative role and skill scenarios with the same
    provider, model, effort, permissions, and environment as the baseline.

Representative evaluations should cover normal success, ambiguity, dirty
worktrees, tool failure, missing verification, scope expansion, destructive or
external actions, liveness/recovery, review-cycle limits, and role-specific
learned failures. One successful response is not proof of non-regression.

If a live model/provider check or executable workflow cannot run, leave that
gate open. Static checks are not a substitute.

## Final Report

Return:

- changed files and exact changes
- before/after line and word measurements
- preserved provider/model/effort/configuration matrix
- parser, skill, plugin, hook, rule, discovery, and config-load evidence
- baseline versus final representative evaluation results
- source versus generated-cache comparison
- unsupported translations or live-model limitations
- unresolved risks and open gates
- required restart, reload, or new-thread action

Global guidance, agent definitions, skills, and newly installed plugin content
may be discovered only at process or thread start. State the exact restart or
new-thread requirement instead of implying the current context reloaded itself.
