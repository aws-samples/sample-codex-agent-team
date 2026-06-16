# Tasks: <slug>

> Tasks are coordination artifacts for the main thread and spawned agents. They are not a live task store.

## Wave 1: <name>

- [ ] [coding] <verb> <what> | `<file path>`, `<file path>` | <acceptance>. Verify: `<command>`
- [ ] [devops] <verb> <what> | `<file path>` | <acceptance>. Verify: `<command>`

## Wave 2: <name>

- [ ] [review] Review <scope> | `<review-scope files>` | PASS/FAIL verdict recorded in `review-<scope>.md`. Verify: inspect diff and run relevant checks.

## Task Rules

- Tasks in the same wave must be file-disjoint.
- Each task must include exact file scope and a verification step.
- Devops or environment-facing smoke tasks must include non-production target validation, bounded retry/timeout behavior, abort criteria, and evidence capture.
- Add a new wave only for real dependencies.
- If a task needs files outside its scope, stop and update this plan before editing.
