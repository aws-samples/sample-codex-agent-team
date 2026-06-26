---
name: team-documentation
description: Documentation patterns for the hybrid Codex team. Use when implementation work requires README, runbook, architecture, API, usage, config, inline documentation, or spec artifact updates tied to `.codex/specs` workflows.
---

# Team Documentation

Use this skill when code, infrastructure, configuration, APIs, or workflows change in a way users, developers, or operators need to understand.

## Scope

Update only documentation materially affected by the work:
- READMEs
- runbooks
- architecture notes
- API docs
- usage examples
- deployment docs
- configuration docs
- spec summaries
- inline function/class/module docs
- changelogs when the project tracks them

Do not duplicate large spec sections into product docs. Link to `.codex/specs/<slug>/` artifacts when useful.

## README Minimum

```md
# Project Name

One-line description.

## Quick Start
<install/run commands>

## Configuration
| Variable | Description | Default |

## Usage
<common operations and examples>

## Development
<setup, tests, lint/type-check>

## Deployment
<prereqs, deploy, rollback>
```

## Runbook Minimum

```md
# <Service> Runbook

## Overview
What this service does and who owns it.

## Architecture
Components, dependencies, and links to diagrams/specs.

## Health Checks
Signals and expected values.

## Common Issues
Symptoms, diagnosis, resolution.

## Escalation
Owners and escalation path.
```

## Architecture Decision Record

```md
# ADR-001: <Decision>

## Status
Accepted | Proposed | Superseded

## Context
Why a decision was needed.

## Decision
What was chosen.

## Consequences
Pros, cons, reversibility.
```

## Spec Artifact Ownership

- `spec.md`: lead-owned design decisions, requirements, constraints.
- `design.md`: lead-owned architecture, repo structure, infrastructure design, security considerations.
- `tasks.md`: lead-authored; agents update completion notes when directed.
- `review.md`: review-agent synthesizer-owned PASS/FAIL findings.
- `sa-review.md`: sa-agent-owned Well-Architected findings.
- `decisions.md`: append-only decision log.

## Team Flow

- `coding-agent` updates task-local docs and inline documentation.
- `devops-agent` updates deployment, CI/CD, config, resource maps, and runbooks.
- `sa-agent` writes architecture review documentation in Well-Architected pillar format.
- `fullstack-agent` reconciles top-level project documentation after all review gates pass.

## Accuracy Checks

- Verify command examples are runnable and non-interactive.
- Verify env vars, resource names, outputs, ARNs, ports, URLs, and paths match the implementation.
- For AWS docs, use AWS Core/Data Analytics skills, `aws-mcp`, or AWS IaC MCP as appropriate.
- For library/framework docs, use Context7 when current docs matter.
- Note staleness risks for version-sensitive docs.

## Writing Rules

- Lead with what and why.
- Prefer concrete examples.
- Keep docs scannable.
- Document inputs, outputs, prerequisites, verification commands, edge cases, and rollback where relevant.
- Avoid filler and marketing language.
