---
name: team-review-cycle
description: Review-loop guidance for the hybrid Codex team with PASS or FAIL verdicts, scoped review files, and fix-wave handoffs. Use when a dedicated review pass is needed after implementation.
---

# Team Review Cycle

Use this skill when implementation is complete enough for an explicit review pass.

## Review Goals

Prioritize:

- correctness
- security
- regressions
- interface mismatches
- missing or weak verification
- missing smoke, staging, deploy, or environment guardrails such as non-production target validation, retry/timeout/abort behavior, and evidence capture

## Review File Options

- `review.md` for one cohesive review pass
- `review-<scope>.md` for split reviews by subsystem or file set
- `review-summary.md` for lead consolidation when multiple scope reviews exist

## Suggested Review Format

```md
## Cycle 1
Reviewing: Wave 2 API and validation scope

### Critical
- [src/api.ts:88] Contract mismatch can return malformed payloads.

### Warning
- [src/api.test.ts:14] No test for invalid token handling.

### Suggestion
- [docs/api.md:10] Clarify default timeout.

### Verdict
FAIL
Reason: Critical contract mismatch in request validation.
```

## Verdict Rules

- `FAIL` if there is any material bug, regression risk, security problem, or missing verification that blocks confidence.
- `PASS` only when the scoped change is acceptable as-is.

## Coordinator Rules

- Any FAIL becomes a new fix wave.
- Preserve review history by adding a new cycle section instead of deleting old findings.
- If multiple review scopes run in parallel, the lead should treat any single FAIL as a wave-level FAIL.
- After a fix wave, rerun the affected review scope and update `review-summary.md` or `lead-summary.md` with the final outcome.
