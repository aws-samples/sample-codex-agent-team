---
description: Plan or run a hybrid Codex team workflow with `.codex/specs` artifacts, file-disjoint waves, role-agent pools, and explicit review gates.
---

Use the hybrid Codex team workflow for `$ARGUMENTS`.

If the work starts as an idea, use `team-brainstorm` first. If it is already concrete, create or update `.codex/specs/<slug>/spec.md`, `design.md` when needed, and `tasks.md`.

For non-trivial work:

1. Use the main thread or `fullstack-agent` as the lead coordinator.
2. Use `team-spec-workflow`, `team-coordination`, and `team-review-cycle`.
3. Author wide, file-disjoint task waves in `.codex/specs/<slug>/tasks.md`.
4. Spawn role agents only when parallel work helps.
5. Use one review synthesizer, plus analysts when review slices are independent.
6. Treat review FAIL as a fix wave.
7. Use `team-documentation` before close-out when docs changed or should change.

If Codex cannot provide the requested subagent workflow, state the exact degraded capability and ask for explicit approval before proceeding single-threaded.
