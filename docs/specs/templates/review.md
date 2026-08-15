# Review: <slug>

> Authored by the `review-agent` synthesizer. The lead does not author PASS/FAIL verdicts. Analysts return findings to the synthesizer and write no review file. Every section carries the durable task group identifier and that group's independent cycle count.

## Task Group <group-id> - Cycle N - YYYY-MM-DD

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

Cycle focus: Cycle 1 is full review. Cycle 2 verifies fixes and regressions. Cycle 3 is terminal final verification for this task group.

Each task group gets at most three cycles. A cycle is consumed when that
group's synthesizer is spawned, including targeted re-reviews, replacement
reviewers, and interrupted retries. Do not reset the group for a new
implementation/fix wave, reviewer, session, or file, and do not rename or split
it to evade exhaustion. After a group cycle 3 non-PASS result, stop that
group's automatic fix/review work, preserve its evidence, close agents no
longer needed for it, and report the group BLOCKED. Other independent groups
may continue. Never spawn cycle 4 for a group automatically.
