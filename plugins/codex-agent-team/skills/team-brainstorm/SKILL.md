---
name: team-brainstorm
description: Use when team-style work starts from a rough project or feature idea rather than agreed requirements.
---

# Team Brainstorm

## Outcome

Produce user-approved requirements at
`.codex/specs/<kebab-slug>/requirements.md` that are ready for
`team-spec-workflow` to derive exact interfaces, architecture decisions,
file-disjoint task waves, role ownership, review scope, and verification.

This phase establishes product intent. It does not implement, choose
architecture prematurely, or spawn a build pool.

## Interaction

- Analyze the initial idea before asking questions.
- Ask one focused question at a time and wait for the answer.
- Adapt follow-up questions to previous answers; do not repeat settled topics
  or issue a long questionnaire.
- Ask only when an answer can materially change scope, behavior, architecture,
  risk, sequencing, staffing, or done criteria.
- Make assumptions and uncertainty explicit.
- Present the complete synthesis for user approval before writing the durable
  artifact.

Use up to ten questions as a normal bound, not a quota. Continue deeper only
when risk or ambiguity justifies it and the user wants further exploration.

## Discovery Checklist

Cover relevant topics and skip those already established.

Users and problem:

- target users, operators, administrators, and approvers
- current workflow and primary pain points
- desired outcome, value, and measurable success

Functional scope:

- core required behavior versus optional or nice-to-have behavior
- primary workflows, roles, permissions, inputs, outputs, and state changes
- MVP boundary, full vision, compatibility, and migration needs

Scale and data:

- users, traffic, concurrency, latency sensitivity, data volume, growth, and
  retention
- data sources, ownership, classification, tenancy, consistency, backup,
  restore, export, and deletion

Integrations:

- APIs, events, files, identity, databases, third-party services, and external
  systems
- existing schemas, rate limits, credentials, interface owners, and failure
  contracts

Non-functional requirements:

- availability, latency, throughput, durability, RTO, and RPO
- security, privacy, compliance, residency, and auditability
- accessibility, localization, supported platforms, maintainability, and
  observability

Delivery constraints:

- budget and cost sensitivity
- timeline, milestones, release constraints, and rollout expectations
- team capabilities, ownership, required/prohibited tools, and technology
  preferences
- deployment environment, environment separation, CI/CD, rollback, and
  operational support

Failure and completion:

- edge cases, abuse cases, partial failure, timeout, retry, degraded operation,
  and recovery
- production and external-system safety boundaries
- acceptance evidence and measurable done criteria
- explicit exclusions and decisions that may wait for design

## Scope Shaping

Prefer the smallest independently valuable slice that can be built, reviewed,
and verified. Preserve future vision in notes without converting it into the
current commitment.

If the idea contains independent systems, decompose it. Describe each boundary
and dependency, then complete requirements for the first valuable slice.
Examples include separating a backend API from a deployment platform, an
ingestion pipeline from analytics, or an operator console from its service.

The resulting slice should be coherent enough for one spec and one whole-run
review budget.

Classify every statement as:

- confirmed required behavior
- confirmed optional behavior
- proposed assumption requiring approval
- out-of-scope or deferred work
- open question that blocks planning

## Team-Ready Requirements

Requirements must expose information that later team artifacts need:

- interface candidates and integration boundaries
- application versus infrastructure ownership
- shared contracts that should be front-loaded before parallel work
- security or AWS surfaces requiring `sa-agent`
- deployment, smoke, teardown, and live-validation expectations
- independently testable acceptance criteria
- natural file/module or component boundaries for task waves
- documentation audiences: users, developers, operators, and responders

Do not invent file paths or final service choices during brainstorming unless
the user supplied them as constraints. Record the required behavior and tradeoff
boundary so design can choose correctly.

## Approval

Synthesize a concise draft with the final artifact sections. Use numbered,
testable requirements and explicit exclusions. Ask the user to approve or
correct it. Refine until approval is unambiguous.

After approval, infer a short kebab-case slug when obvious. Ask only when
several meaningful names remain. Write exactly the approved content; do not add
new requirements during file creation.

## Required Artifact

```markdown
# Requirements: <Title>

## Project Summary
Users, pain points, value, and agreed first slice.

## Functional Requirements
Numbered behavior grouped by capability.

## Non-Functional Requirements
Scale, data, availability, latency, security, compliance, operations, budget,
timeline, team/tool constraints, and deployment.

## Edge Cases
Boundary, failure scenarios, abuse, degraded mode, and recovery.

## Out of Scope
Explicit exclusions and deferred systems.

## Open Questions
Only unresolved items that planning must decide or track.

## Notes
Assumptions, terminology, references, dependencies, and future context.
```

Use stable requirement identifiers when `spec.md`, `tasks.md`, and `review.md`
will need to cite them.

## Quality Gate

Before writing, confirm:

- target users and pain points are clear
- required and optional behavior are separated
- data volume, integrations, availability, latency, security, compliance,
  budget, timeline, team constraints, and deployment were considered
- failure scenarios and done criteria are testable
- independent systems were decomposed where useful
- interface and ownership boundaries are visible enough for design
- user approval was obtained

After writing, report the artifact path and recommend `team-spec-workflow`.
Stop without implementation unless the user also requested the subsequent team
workflow.
