---
name: team-review-cycle
description: Review-loop guidance for the hybrid Codex team with synthesizer/analyst roles, PASS or FAIL verdicts, scoped findings, and fix-wave handoffs. Use when a dedicated review pass is needed after implementation.
---

# Team Review Cycle

Use this skill when implementation is ready for an explicit review wave.

## Review Goals

Prioritize:
- correctness
- security
- behavioral regressions
- interface mismatches
- performance risks
- missing or weak verification
- AWS/IaC safety where applicable

## Authority

The lead does not author a PASS/FAIL verdict for its own work. A self-review is a TODO marker, not a completed review gate.

Small changes can use one reviewer. Broad changes use parallel review:
- Synthesizer: exactly one reviewer, usually `review-1`; sole author of `review.md` and final verdict.
- Analyst: `review-2` through `review-4`; reviews one slice, writes no files, returns structured findings to the synthesizer.

## Analyst Findings Format

```text
Slice: <module/files reviewed> | Wave N, Cycle M
Critical:
- [file:line] Issue and recommended fix
Warning:
- [file:line] Issue and recommended fix
Suggestion:
- [file:line] Improvement
Cross-slice concerns: <interfaces/assumptions the synthesizer should re-check, or "none">
Slice verdict (advisory): PASS | FAIL
```

## Review File Format

`review.md` is written by the synthesizer only.

```md
## Cycle N - YYYY-MM-DD
Reviewing: Wave M - <description>

### Spec Alignment
Does each task satisfy acceptance criteria and interface contracts?

### Critical
- [file:line] Issue and recommended fix

### Warning
- [file:line] Issue and recommended fix

### Suggestion
- [file:line] Improvement

### Cross-Task Consistency
Interfaces match across tasks? Naming consistent? Conflicting assumptions?

### Security And Compliance
- [ ] Encryption at rest verified where applicable
- [ ] Encryption in transit verified where applicable
- [ ] Access logging enabled where applicable
- [ ] Data classification tags present where applicable
- [ ] Secret handling reviewed

### Tests
- [ ] Required verification passed
- [ ] Test coverage adequate

### Verdict: PASS | FAIL
Reason: <one-line if FAIL>
```

## Severity

- Critical: likely runtime failure, data loss, broken contract, severe/high security issue, or production-impacting infra defect.
- Warning: medium security risk, missing error handling, missing required verification, meaningful performance risk, fragile behavior, or unjustified spec deviation.
- Suggestion: maintainability, clarity, low-risk documentation, style, or optional improvement.

## Verdict Rules

- FAIL if any Critical or Warning remains.
- FAIL if required verification is absent.
- PASS only when the scoped change is acceptable as-is.
- Suggestions do not block PASS.

## Cycle Focus

- Cycle 1: full review, broad and adversarial.
- Cycle 2: verify prior Critical/Warning fixes, check regressions, flag only new Critical/Warning.
- Cycle 3: final verification. If issues persist, summarize for user escalation.

Maximum three cycles per wave before escalation.

## Coordinator Rules

- Any FAIL becomes a fix wave.
- Preserve review history by appending cycles rather than deleting old findings.
- If multiple review scopes run in parallel, the synthesizer owns the single verdict.
- If review cannot run, the gate is open. Do not fabricate PASS.
