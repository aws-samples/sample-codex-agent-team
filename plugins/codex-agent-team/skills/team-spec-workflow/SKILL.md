---
name: team-spec-workflow
description: Use when non-trivial work needs durable requirements, architecture decisions, delegated task waves, independent review, or coordinated documentation.
---

# Team Spec Workflow

## Outcome

Turn an agreed objective into durable, executable team artifacts, then carry
implementation through file-disjoint task waves, independent review,
documentation, worker closure, and one evidence-backed final decision.

Use this workflow for work spanning multiple files, meaningful architecture,
production behavior, infrastructure, security, delegated implementation, or a
review/fix loop. Small direct edits do not need artificial ceremony.

## Artifact Directory

Use `.codex/specs/<kebab-slug>/`. Prefer:

1. repository-local `.codex/specs/templates/`
2. user-global `~/.codex/specs/templates/`
3. the structures below

Create only the artifacts the task needs:

- `requirements.md`: approved users, product behavior, constraints, and
  exclusions
- `spec.md`: executable requirements, assumptions, exact interfaces, edge
  cases, risks, and acceptance
- `design.md`: architecture, boundaries, data flow, storage, infrastructure,
  tradeoffs, rollout, and Security Considerations
- `tasks.md`: task waves, ownership, task status, dependencies, acceptance,
  commands, and completion evidence
- `decisions.md`: append-only decisions, blockers, deviations, accepted risks,
  and open gates
- `review.md`: synthesizer-owned cycle history and verdicts
- `sa-review.md`: solution-architecture findings and handoffs
- optional `prd/` or security evidence required by repository conventions

Do not create parallel copies of the same decision. Link between artifacts and
name the authoritative section.

## Requirements And Spec

`requirements.md` records approved intent. Do not silently redesign it during
planning. If research reveals a material product conflict, return to the user
or record the open question.

`spec.md` should include:

- goal, users, success measures, and traceable requirement identifiers
- functional and non-functional requirements
- constraints, assumptions, dependencies, and exclusions
- exact interfaces and contracts
- data ownership, schemas, lifecycle, migration, and compatibility
- errors, edge cases, partial failure, retries, timeouts, and recovery
- observability and operational behavior
- acceptance criteria and required verification
- material unresolved questions

Exact interfaces include signatures, request/response payloads, events,
schemas, error forms, environment variables, resource outputs, names, ports,
paths, protocols, and version expectations. Define shared contracts before
dependent tasks.

## Design

Create `design.md` when component boundaries, repository structure, data flow,
infrastructure, migration, or tradeoffs matter. Include:

- context and selected architecture
- components and ownership
- sequence/data flow
- repository/module/file placement
- storage and consistency
- external integrations
- deployment and environment model
- observability and failure handling
- alternatives considered and why rejected
- rollout, rollback, and reversibility
- open design decisions

For AWS or production-impacting work, include `## Security Considerations` with
identity, trust boundaries, secrets, encryption/KMS, network exposure,
classified data, logging/retention, state backend, backups, threat/abuse cases,
and evidence needed for closure.

Engage `sa-agent` for IAM, KMS/encryption, network exposure, security groups,
EKS access, stateful resources, classified storage, logging/retention, or
Terraform/CloudFormation state backends.

## Task Contract

Use:

```md
## Wave 1: <outcome>
Spec refs: `spec.md#interfaces`, `requirements.md#FR-1`

- [ ] [coding] Implement order validation | `src/orders/validate.ts`, `src/orders/validate.test.ts` | Match `OrderInput` and error contracts; cover empty and duplicate IDs. Run: `npm test -- orders/validate`
- [ ] [devops] Add order table outputs | `infra/orders.tf`, `docs/config.md` | Export `orders_table_name`; KMS, PITR, tags, and docs match design. Run: `terraform -chdir=infra validate`
```

Every task must contain:

- task status marker
- role: `[coding]`, `[devops]`, or `[sa]`
- action and user/system outcome
- exact writable files and no-edit boundary
- acceptance criteria linked to the spec
- produced and consumed interfaces
- dependencies
- `Run: <command>` or a precise evidence query
- expected completion handoff

Use `[skip-verify]` only when no meaningful executable check exists. Analysis
tasks should still name the artifact and evidence they produce.

Task status semantics:

- `[ ]`: ready or waiting on an explicit dependency
- `[-]`: in progress, with owner noted
- `[x]`: completed with exact verification evidence
- `[!]`: blocked, with cause, attempts, owner, and needed decision

Do not mark `[x]` from a worker's claim alone. Reconcile returned results,
current files, and fresh command output. Preserve failure evidence in the task
note.

## Wave Construction

Build the fewest waves with the widest safe file-disjoint work:

- Put tasks with no unmet dependency in the same wave.
- Front-load shared interface contracts so consumers can fan out.
- Split broad tasks by module, endpoint, package, stack, workflow, or doc when
  each slice is independently testable.
- Run coding and DevOps work together when their files and contracts are
  independent.
- No two parallel tasks may write the same file.
- Serialize overlapping writers or name one explicit merge owner.
- Add a new wave only for a real data, contract, generation, or ordering
  dependency.

Pool caps are ceilings, not a reason to invent tasks. Use
`team-coordination` to size the pool to file-disjoint width and write exact
handoffs.

## Decisions And Blockers

`decisions.md` is append-only. Record:

- date and decision
- context and alternatives
- owner/approver
- affected requirements, interfaces, tasks, and docs
- consequences and reversibility
- validation or follow-up

Record blockers with the exact command/error, attempts, affected task, and
smallest needed decision. Do not hide a blocker by changing acceptance
criteria. If a blocker forces degraded single-threaded work, open review, or
missing live validation, obtain the required user approval and preserve the
lost assurance.

## Security And Verification

Task acceptance must cover applicable controls:

- IAM least privilege and trust
- encryption at rest and in transit
- KMS claims matching configuration
- secret handling
- network exposure and scoped egress
- logging, retention, metrics, alarms, and auditability
- backups/recovery and deletion protection
- state backend encryption/locking/recovery
- data-classification tags and classified-storage controls

Use `aws-security-guidelines`, relevant AWS skills, AWS IaC MCP validation, and
configured read-only AWS tools. Store scan/evidence artifacts under the spec
directory when the repository requires them. Accepted risks require owner,
reason, compensating control, expiration/revisit, and reversibility.

Each task runs focused verification and applicable CI-blocking checks. Verify
the verifier: the command must exercise the claimed behavior with pinned
repository tooling.

## Live-Validation Gate

Static checks are necessary but not sufficient for IaC, deploy scripts, CI/CD,
containers with delivery behavior, or shell tooling. Lint, validate, synth,
plan, and unit tests cannot prove target selection, cloud semantics, config
precedence, real exit status, smoke target, or teardown residue.

Require deploy/smoke/teardown or the closest safe executable equivalent when
approved and available. If it cannot run:

- mark affected criteria static-validated only
- identify the exact unproven behavior
- record the open live-validation gate in `decisions.md` and `review.md`
- do not imply runtime PASS

## Review And Fix Flow

After implementation evidence is consolidated:

1. Count every prior review synthesizer spawn for the entire team run.
2. Record the next cycle before spawning review.
3. Use `team-review-cycle` with exactly one synthesizer and optional
   file-disjoint analysts.
4. Wait for requested analyst evidence and the synthesizer verdict.
5. On cycle 1 or 2 FAIL, convert unresolved Critical/Warning findings into one
   scoped, file-disjoint fix wave.
6. Re-run affected and regression verification, then consume the next review
   cycle.
7. Cycle 3 is terminal. On non-PASS, stop automatic fixes/reviews, close active
   agents, preserve evidence, and report blocked.

One maximum three-cycle budget applies to the whole run. It does not reset for
a new wave, fix, reviewer, review file, retry, interruption, or resumed
session. A cycle is consumed when its synthesizer is spawned.

## Documentation

After independent PASS, use `team-documentation` to reconcile affected README,
API, configuration, deployment, rollback, runbook, architecture, and usage
surfaces. Task-local docs may be updated during implementation; final
reconciliation checks cross-task consistency and current names.

## Whole-Run Completion

Complete only when:

- requirements and interfaces are satisfied
- all required task status entries are `[x]`
- exact verification and CI evidence is recorded
- one independent synthesizer reports PASS within the three-cycle budget
- required live-validation gates are closed
- blockers, decisions, deviations, and accepted risks are durable
- affected documentation is accurate
- all requested worker results are harvested
- agents no longer needed are closed
- no required worker remains active
- no billable or temporary verification resource lacks an explicit handoff

If cycle 3 ends without PASS, completion is blocked rather than partial
success. Preserve the same artifact set so the user can decide the next action.
