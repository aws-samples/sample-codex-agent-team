---
name: team-documentation
description: Use when code, infrastructure, configuration, APIs, or workflows change what users, developers, or operators need to know.
---

# Team Documentation

## Outcome

Make affected user, developer, operator, and responder documentation accurately
describe the verified implementation. Preserve durable decisions without
copying the full spec, verify commands and implementation names, and expose
open validation or staleness risk.

Documentation is part of delivery. A review PASS does not excuse stale public
or operational contracts.

## Ownership

- `coding-agent`: task-local API, behavior, examples, migration notes, and
  inline function/class/module documentation
- `devops-agent`: deployment, CI/CD, configuration, environment contracts,
  resource maps, rollback, teardown, and runbooks
- `sa-agent`: architecture review, Well-Architected findings, cost/risk
  assumptions, and architecture handoffs
- lead: top-level README and cross-task reconciliation after review PASS
- review synthesizer: sole owner of `review.md`
- `sa-agent`: owner of `sa-review.md`

Assign one writer for each shared documentation file. Concurrent agents must
not edit the same README, runbook, ADR, or API document.

## Select The Documentation Surface

Update only material surfaces affected by the change:

- project, package, module, or service README
- quick start and developer setup
- API reference, OpenAPI, schemas, events, and examples
- configuration and environment-variable reference
- deployment, migration, rollback, and teardown procedures
- CI/CD overview and release process
- operator runbook and incident procedures
- architecture overview, diagram references, and ADRs
- contributor guide
- inline docs for public or non-obvious interfaces
- changelog/release notes when the project uses them

Link to `.codex/specs/<slug>/` for detailed requirements, design rationale,
review history, and decisions. Do not duplicate large spec sections into
product docs; duplicated details become stale.

## README Content

Include the smallest relevant set:

```markdown
# Project Name

One clear sentence describing purpose and scope.

## Prerequisites
Supported runtimes, tools, services, credentials, and environment assumptions.

## Quick Start
Verified install, configure, run, and smoke-check commands.

## Configuration
Variables/parameters, required status, safe default, format, source, and effect.

## Usage
Common user/developer flows with concrete examples and expected results.

## Development
Setup, tests, lint, type checks, build, and repository conventions.

## Deployment
Target selection, plan/deploy, smoke check, rollback, teardown, and open gates.

## Operations
Ownership, health, observability, runbook, and escalation links.
```

Do not claim support, deployment success, or runtime behavior beyond verified
evidence.

## API Documentation

For each changed endpoint, command, event, or public function, document:

- method/operation and path/name
- purpose and authorization
- request parameters, headers, body/schema, and validation
- response/event/output schema
- error status/types and retry behavior
- idempotency, pagination, rate limits, timeout, and compatibility
- one realistic request and response or usage example
- versioning/deprecation and migration when applicable

Generate or update OpenAPI/schema artifacts using the repository's existing
tooling. Verify generated docs match current implementation rather than editing
generated output by hand.

## Configuration Documentation

For each changed setting, include:

- exact implementation name
- source: file, environment, CLI, secret manager, parameter, or default
- required/optional status
- accepted format and safe example
- default and precedence
- secret/sensitive handling
- environment scope and restart/reload behavior
- failure behavior when missing or invalid

Explicit caller input versus sourced-default precedence must match scripts.
Never put real credentials or secret values in documentation.

## Deployment And Rollback

Document:

- prerequisites and required approvals
- target account, region, profile, stage, cluster/context, namespace,
  workspace, backend, and image selection
- plan/synth/diff and deployment commands
- expected outputs and health/smoke checks
- rollout order and blast-radius controls
- rollback trigger, command, and verification
- authoritative teardown and independent residue checks
- known open live-validation gates

Commands that mutate live systems must be clearly labeled with impact and
approval requirements. Do not present `destroy || true`, backend-disabled
teardown, or unverified cleanup as safe.

## Runbook

Use:

```markdown
# <Service> Runbook

## Overview
Purpose, user impact, owner, dependencies, and environments.

## Architecture
Components, data flow, critical resources, and links to diagrams/ADRs.

## Access And Safety
Required role, target checks, read-only starting point, and approval gates.

## Health And Observability
Endpoints, metrics, alarms, logs, dashboards, traces, and expected values.

## Common Failures
Symptoms, diagnosis, safe recovery, and verification.

## Deployment And Rollback
Commands, smoke checks, rollback triggers, rollback verification.

## Data Recovery Or Teardown
Backup/restore or authoritative cleanup with residue checks.

## Escalation
Primary ownership, secondary owner, incident channel/process, and vendor path.
```

Diagnosis should begin with read-only evidence. Separate safe investigation
from mutating recovery.

## Architecture Decisions

Use an ADR for a material decision that future maintainers may revisit:

```markdown
# ADR-NNN: <Decision>

## Status
Proposed | Accepted | Superseded

## Context
Forces, constraints, assumptions, and why a decision was needed.

## Decision
The selected option and scope.

## Alternatives
Options considered and why not selected.

## Consequences
Benefits, costs, risks, operations, security, and compatibility.

## Reversibility
Migration/rollback path and trigger to reconsider.
```

Link superseding ADRs instead of rewriting historical decisions.

## Writing Rules

- Lead with the operational or user-visible fact.
- Use concrete examples rather than generic prose.
- Keep headings and tables scannable.
- Explain why only when the reason affects correct use or future decisions.
- Use the repository's terminology and exact implementation names.
- Separate current behavior from proposed/future behavior.
- Avoid marketing claims and filler.
- Identify owner and escalation for operational responsibilities.

## Accuracy Gate

Before completion:

1. Re-read current implementation and config.
2. Compare every environment variable, API, resource, output, ARN, port, URL,
   path, command, flag, default, and example with current files.
3. Run command examples or the safest non-mutating validation that proves their
   syntax and scope.
4. Confirm setup/test commands use committed wrappers, lockfiles, and pinned
   tooling.
5. Confirm deploy/rollback/teardown docs identify targets and safety gates.
6. Check links and referenced files.
7. Use current AWS or library documentation for version-sensitive facts.
8. Search for old names and contradictory instructions.
9. Record unresolved runtime validation and staleness risk.

A command that could not run must be labeled unverified with the reason. Static
validation does not establish deploy/smoke/teardown behavior.

## Staleness Checks

Watch for:

- renamed environment variables or resource outputs
- examples using removed APIs or flags
- obsolete screenshots or architecture diagrams
- old model/service/library versions presented as current
- duplicated configuration tables
- stale owners or escalation paths
- rollback steps that no longer match deployment
- docs claiming a security control absent from IaC

Prefer generated reference from authoritative schemas where the repository
already supports it. Do not add a new documentation generator without a clear
maintenance benefit.

## Completion Handoff

Return:

- documentation files changed and audience
- implementation/spec sections used as source
- command examples verified and outcomes
- names/links checked
- open runtime validation or staleness risk
- documentation findings closed

Stop when every changed public, developer, and operator-facing contract is
accurate, owned, and consistent with the reviewed implementation.
