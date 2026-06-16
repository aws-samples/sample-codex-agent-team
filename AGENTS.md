# Codex Team Defaults

## Working Agreements

- Use repo-local `.codex/specs/<slug>/` for non-trivial specs, task plans, review files, and decision logs when a team workflow is in play.
- Keep the main thread as the coordinator for team-style work. Use explicit custom agents only when the user asks for parallel delegation, role specialization, or a lead/member workflow.
- Prefer file-disjoint parallel work. If two agents must edit the same file set, serialize that slice or add an explicit merge step.
- Keep durable project rules in project `AGENTS.md` files. Keep reusable workflow detail in skills rather than bloating global instructions.
- Treat review as a separate gate. A fix wave is not done until an explicit review pass reports PASS.

## Execution Hygiene

- Run commands non-interactively. Disable pagers with `--no-pager`, `--no-cli-pager`, or `GIT_PAGER=cat`; pass confirmation-suppression flags such as `--yes`, `--no-input`, or `-y` where appropriate.
- Do not rely on a command prompting for stdin, opening an editor, or attaching to a TTY. Provide required inputs through arguments, environment variables, or files.
- Use project-local dependency isolation. Do not install project dependencies globally; prefer existing `.venv`, local `node_modules`, package-manager lock files, committed wrappers, and language toolchain pins.
- Preserve lock files and isolation directories according to the repository convention. Do not introduce a new package manager or dependency workflow unless the task requires it.

## Production Safety

- Prefer read-only or least-privilege credentials for AWS or production-like investigation.
- Treat unknown environments as production until proven otherwise.
- Prefer `list`, `describe`, `get`, dry-run, plan, or diff operations before any mutating operation.
- Do not delete, terminate, modify production resources, or disable safety protections without explicit user direction and a clear impact statement.
- Never inline secrets in code, docs, configs, tests, or command examples.
