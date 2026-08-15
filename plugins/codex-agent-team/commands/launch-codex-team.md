---
description: Plan or run a role-based Codex team workflow with explicit review gates.
---

Run the hybrid Codex team workflow for `$ARGUMENTS`.

Use `team-brainstorm` when requirements are not agreed, `team-spec-workflow` for
durable artifacts and task waves, `team-coordination` for delegation,
`team-review-cycle` for the independent verdict, and `team-documentation` for
close-out. Keep durable state under `.codex/specs/<kebab-slug>/`, keep writes
file-disjoint, wait for all requested agents, and close agents before
completion. Give every independently reviewable task group a durable group ID
and its own non-resetting three-cycle review budget: only group
cycles 1 and 2 may create fix waves, and cycle 3 is terminal for that group.
Do not reset a group by renaming or splitting it; independent groups may
continue while a blocked group awaits user disposition.
Report degraded capability before any single-threaded fallback.
