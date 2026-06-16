---
description: Plan or run a hybrid Codex team workflow with the lead agent, shared `.codex/specs` artifacts, and explicit role-based subagents.
---

Use the hybrid Codex team workflow for `$ARGUMENTS`.

If the work is not yet specified, start with `team-brainstorm` or create the initial `.codex/specs/<slug>/spec.md`.

For non-trivial work:

1. Use `fullstack-agent` as the coordinator.
2. Use `team-spec-workflow`, `team-coordination`, and `team-review-cycle` as needed.
3. Break the work into file-disjoint waves in `.codex/specs/<slug>/tasks.md`.
4. Spawn role agents explicitly when parallel work helps.
5. Wait for all requested subagents, then consolidate outcomes and review status in the main thread.
