# Review: <slug>

> Authored by the `review-agent` synthesizer. The lead does not author PASS/FAIL verdicts. Analysts return findings to the synthesizer and write no review file. This file records the single whole-run cycle counter.

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
- [ ] Scan findings triaged where applicable

### Tests

- [ ] Required verification passed
- [ ] Test coverage adequate

### Verdict: PASS | FAIL

Reason: <one-line if FAIL>

---

Cycle focus: Cycle 1 is full review. Cycle 2 verifies fixes and regressions. Cycle 3 is terminal final verification.

The entire user objective or team run gets at most three cycles. A cycle is
consumed when its synthesizer is spawned, including targeted re-reviews,
replacement reviewers, and interrupted retries. Do not reset for a new wave,
reviewer, session, or file. After a cycle 3 non-PASS result, stop automatic fix
and review work, preserve the evidence, close active agents, and report BLOCKED.
Never spawn cycle 4 automatically.
