---
name: team-documentation
description: Documentation patterns for the hybrid Codex team. Use when implementation work requires README, runbook, architecture, API, or spec artifact updates tied to `.codex/specs` workflows.
---

# Team Documentation

Use this skill when code or infrastructure changes need documentation updates that stay aligned with `.codex/specs/<slug>/` artifacts.

## Scope

Update only the documentation that is materially affected:

- READMEs
- runbooks
- architecture notes
- API docs
- usage examples
- spec summaries

## Default Pattern

1. Link changes back to the relevant spec or decision file when one exists.
2. Explain what changed, why it matters, and how to verify or operate it.
3. Keep examples concrete and runnable.
4. Do not duplicate large spec sections into product docs.

## Minimum Checklist

- State the purpose of the changed component.
- Document inputs, outputs, or required configuration.
- Include the main verification or usage command when relevant.
- Note important edge cases, operational considerations, or rollout constraints.

## Team Flow Notes

- `coding-agent` should update task-local docs and inline documentation.
- `devops-agent` should update deployment, CI/CD, and runbook material.
- `fullstack-agent` should reconcile top-level project documentation at the end of a completed review cycle.
