---
name: team-review-cycle
description: Use when implemented work needs an independent correctness, security, regression, performance, or verification review before completion.
---

# Team Review Cycle

## Outcome

Produce evidence-backed findings and exactly one independent `PASS` or `FAIL`
verdict for the current integrated state. Preserve the review history, consume
one global cycle budget for the whole team run, and terminate automatic
review/fix work after cycle 3.

Review is adversarial validation, not a formality. An implementer, lead, or
self-authored PASS is a TODO marker rather than an independent verdict.

## Inputs

Every review handoff must contain:

- review role and unique instance name
- spec directory
- wave and whole-run cycle number
- exact modified files or assigned review slice
- acceptance criteria and interface contracts
- worker verification commands and outcomes
- prior unresolved findings for cycle 2 or 3
- open live-validation gates
- named analysts/synthesizer and expected results

The reviewer also reads current requirements, spec, design, tasks, decisions,
files, diff, and review history. Missing scope or evidence is itself a review
gap; do not infer it from an old summary.

## Roles

Synthesizer:

- Exactly one `review-agent`, normally `review-1`.
- Sole author of `review.md`.
- Reviews an assigned slice plus whole-wave cross-slice consistency.
- Waits for all requested analyst results or records missing evidence.
- Deduplicates and attributes analyst findings.
- Runs or evaluates cross-cutting verification.
- Issues the only authoritative group verdict.

Analyst:

- Optional `review-2` through `review-4`.
- Reviews one file-disjoint slice.
- Writes no files and never edits `review.md`.
- Returns structured findings to the named synthesizer.
- Gives an advisory slice result only.
- Identifies assumptions/interfaces requiring cross-slice confirmation.

Small cohesive changes use one synthesizer with no analysts. Parallel analysts
are useful only when there are independently reviewable slices.

## Analyst Format

```text
Slice: <module/files> | Wave N, Cycle M
Critical:
- [file:line] impact, current evidence, and specific correction
Warning:
- [file:line] impact, current evidence, and specific correction
Suggestion:
- [file:line] optional improvement
Cross-slice concerns: <interfaces/assumptions or none>
Verification:
- <exact command, exit code, result>
Open live validation: <gaps or none>
Advisory slice result: PASS | FAIL
```

An empty section says `None`; it is never omitted ambiguously. Analysts return
their evidence and stop. They do not ask implementers to fix findings directly;
the coordinator creates the fix wave after synthesis.

## Synthesizer Review File

Append one section per cycle to `.codex/specs/<slug>/review.md`. Preserve prior
cycles.

```markdown
## Cycle N - YYYY-MM-DD
Reviewing: Wave M - <integrated scope>
Analysts: <instances and slices, including missing results>

### Critical
- [`file:line`] Impact, evidence class, evidence, and specific correction.

### Warning
- [`file:line`] Impact, evidence class, evidence, and specific correction.

### Suggestion
- [`file:line`] Optional improvement.

### Spec Alignment
Requirements, acceptance criteria, exclusions, interface contracts.

### Cross-Task Consistency
Schemas, names, generated artifacts, config, outputs, and ownership.

### Security And Operations
Trust boundaries, IAM, secrets, network, encryption, logging, rollback.

### Verification And Test Adequacy
Exact commands, CI coverage, behavior proven, verifier gaps.

### Open Live Validation
Unrun runtime/cloud/deploy/smoke/teardown evidence.

### Verdict: PASS | FAIL
Reason: <one line when FAIL>
```

Tag analyst-sourced findings with the instance. Deduplicate equivalent issues
without losing evidence or affected files.

## Review Method

### Spec Alignment

- Map changes to requirements and acceptance criteria.
- Verify exact interfaces, payloads, schemas, errors, environment variables,
  outputs, names, ports, paths, and version contracts.
- Check exclusions, assumptions, and decisions.

### Correctness And Reliability

- Edge cases, invalid/empty input, boundary conditions, off-by-one behavior
- Error handling, retries, timeouts, cancellation, idempotency
- Race conditions, ordering, shared state, stale writes, deadlocks
- Cleanup, partial failure, rollback, teardown, leaked resources
- Compatibility, migration, serialization, timezone/platform behavior

### Security

- Trust-boundary validation, authentication, authorization, injection
- Secrets, logging, data exposure, unsafe defaults
- IAM least privilege and trust
- Network exposure and scoped egress
- Encryption/KMS, classified storage, retention, and auditability

### Performance

- N+1 work, hot paths, resource sizing, connection behavior
- Sequential uncached bulk external calls
- Unbounded concurrency, missing backpressure, retry storms, cached failures
- Data structures, pagination, batching, and lifecycle

### Maintainability And Documentation

- Project conventions, clarity, unnecessary complexity
- Ownership, observability, actionable failure messages
- README, API, config, deployment, rollback, runbook, and inline-doc accuracy

### Test Methodology

- Focused unit tests cover logic, errors, and boundaries.
- Integration tests cover service/framework/storage/process boundaries.
- Regression tests reproduce the fixed defect.
- Concurrency and cleanup tests are deterministic.
- Mocks do not replace the behavior the acceptance criteria require.
- CI-pinned checks and relevant suites ran.

## Evidence Discipline

Re-read the exact current file before citing `file:line`. Never report a
remembered snapshot, stale line number, or already-fixed issue.

Empirically test before rating a claim Critical when safe execution can confirm
or falsify it. If execution is unavailable, classify the finding as requiring
live validation and normally use Warning unless the severe defect is directly
provable.

For every finding, identify its evidence class:

- static-verifiable
- empirically reproduced
- requires live validation

Verify the verifier. A green command is not enough if it:

- checks the wrong scope
- omits a CI-pinned linter/type checker/test
- never exercises the acceptance criterion
- uses a broken assertion or inadequate script
- substitutes static validation for required runtime behavior

The finding should close the weak check or preserve the verification gap, not
only patch observed instances.

For long review/verification commands, return a concise heartbeat through the
available handoff channel. Quiet execution is not failure and does not justify
a replacement synthesizer.

## Delivery And AWS Evidence

Static lint, synth, validate, plan, and unit tests cannot prove runtime account,
region, profile, workspace, backend, kube-context, config precedence, provider
semantics, real pipeline status, smoke target, destroy behavior, or residue.

For IaC, deploy scripts, CI/CD, and shell tooling:

- inspect static checks
- require deploy/smoke/teardown or closest safe executable equivalent when the
  acceptance criteria require it
- check rollback and authoritative-state handling
- require independent residue evidence
- preserve an open live-validation gate when execution cannot run

Use `aws-security-guidelines`, relevant AWS skills, AWS IaC MCP validation, and
current read-only AWS facts when AWS behavior is material.

## Severity

Critical:

- likely runtime failure or broken required contract
- data loss/corruption
- severe/high security vulnerability
- destructive wrong-target or production-impacting infrastructure defect

Warning:

- meaningful correctness, security, reliability, performance, race, cleanup,
  or maintainability defect
- missing required test, CI check, analyst evidence, or live validation
- fragile behavior or unjustified spec deviation

Suggestion:

- non-blocking clarity, style, low-risk docs, or optional improvement

Severity reflects impact and evidence, not how easy the fix is.

## Verdict

FAIL when:

- any Critical or Warning remains
- required verification is absent or inadequate
- a requested analyst result is missing
- a required live-validation gate is open
- current files do not satisfy the accepted interfaces

PASS only when the integrated scope is acceptable as-is and all required
evidence is present. Suggestions do not block PASS.

## Global Cycle Budget

There is one non-resetting maximum of three review cycles for the entire user
objective/team run. A cycle is consumed when its synthesizer is spawned, before
the result is known. The same budget counts:

- initial review
- targeted re-review
- replacement synthesizer
- retry after interruption or failure

Derive the next number from durable review and orchestration evidence before
spawn. Do not reset for a new implementation wave, fix wave, reviewer, review
file, process, or resumed session.

- Cycle 1: full broad adversarial review.
- Cycle 2: verify cycle-1 fixes, targeted regressions, and new blockers.
- Cycle 3: terminal final verification of remaining fixes and gates.

Only cycle 1 or 2 FAIL may create one scoped fix wave. After the fix, all
affected and regression checks run before the next synthesizer spawn.

Cycle 3 is terminal. If it returns FAIL, is interrupted, or cannot complete:

1. Stop all automatic fix and review work.
2. Close active agents.
3. Preserve unresolved findings, partial results, and verification evidence.
4. Record affected tasks/docs and open live-validation gates.
5. Report the run blocked for user decision.

Never spawn cycle 4.

## Coordinator Handoff

The synthesizer returns one message with wave, cycle, verdict, counts by
severity, commands/outcomes, missing evidence, and review path. The coordinator
reads the verdict; it does not rewrite or aggregate an independent PASS.
