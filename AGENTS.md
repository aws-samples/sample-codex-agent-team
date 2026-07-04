# Codex Team Defaults

## Working Agreements

- Use repo-local `.codex/specs/<slug>/` for non-trivial specs, task plans, review files, SA reviews, decision logs, and security exceptions when a team workflow is in play.
- Treat the main thread as the top-level team lead by default. Use `fullstack-agent` only when the user explicitly asks for a lead profile or spawn-plan generation.
- When a team workflow is in play, the lead coordinates and delegates. It may research, write specs, write tasks, update decisions, and consolidate outcomes, but it should not implement non-trivial production code, tests, IaC, or deployment changes itself.
- Prefer wide, file-disjoint task waves. No two parallel tasks may write the same file. If overlap is unavoidable, serialize that slice or document an explicit merge step.
- Under-provision before over-provisioning. A pool wider than the actual file-disjoint task width creates coordination churn, stale handoffs, and same-file races; spawn only when there is independent work to keep the agent busy.
- Treat review as a separate adversarial gate. A wave is not done until the assigned `review-agent` pass reports PASS. A self-review is a TODO marker, not a verdict.

## Team Protocol

- Task artifacts use this shape: `- [ ] [coding|devops|sa] <verb> <what> | <file paths> | <acceptance criteria>. Run: <command>`.
- Every task needs exact files, acceptance criteria, and a concrete verification command. Use `[skip-verify]` only for genuinely non-runnable coordination or analysis work.
- The lead should spawn role agents only when the user asks for parallel delegation, role specialization, a lead/member workflow, or team-style work.
- Spawn pools to match the widest independent wave, capped at 6 `coding-agent`, 2 `devops-agent`, 4 `review-agent`, and 1 `sa-agent`.
- Use `sa-agent` for AWS work touching IAM, KMS/encryption, security groups, network exposure, EKS access, stateful resources, or Terraform/CloudFormation state backends. If the lead consciously skips SA review for one of those surfaces, record the reason in `decisions.md`.
- Every spawned prompt must include instance name, role, spec path, task or wave reference, exact file scope, expected output, verification command, and an instruction not to edit outside scope.
- Review waves use one synthesizer reviewer when multiple reviewers are active. The synthesizer owns `review.md`; analyst reviewers send structured findings and write no review file.
- Record blockers in `tasks.md` and `decisions.md`. If the same blocker persists after two attempts, escalate to the user instead of silently degrading the workflow.
- Ground truth is disk artifacts first: `tasks.md`, `review.md`, `sa-review.md`, `decisions.md`, verification outputs, `git diff`, and current files. Messages, stale summaries, and subagent silence are not authoritative.
- Do not infer a teammate is dead from silence. For a quiet subagent, inspect artifacts and wait for its result; if recovery is genuinely needed, respawn or reassign with explicit scope rather than taking over broad work in the lead thread.

## Execution Hygiene

- Run commands non-interactively. Disable pagers with `--no-pager`, `--no-cli-pager`, or `GIT_PAGER=cat`; pass confirmation-suppression flags such as `--yes`, `--no-input`, or `-y` where appropriate.
- Do not rely on a command prompting for stdin, opening an editor, or attaching to a TTY. Provide required inputs through arguments, environment variables, or files.
- Use project-local dependency isolation. Do not install project dependencies globally; prefer existing `.venv`, local `node_modules`, package-manager lock files, committed wrappers, and language toolchain pins.
- Preserve lock files and isolation directories according to the repository convention. Do not introduce a new package manager or dependency workflow unless the task requires it.
- If code performs bulk independent external calls, use `concurrent-cached-fetch` before writing the loop. Bounded concurrency and a content-keyed disk cache are the default.

## Plugin Routing

- For AWS work, prefer AWS Core plugin skills for service, SDK, IaC, IAM, observability, Bedrock, serverless, containers, messaging, streaming, secrets, and cost tasks.
- Use AWS Data Analytics plugin skills for Glue, Athena, S3 Tables, S3 Vectors, OpenSearch, data lake, ETL, catalog, vector, search, and analytics workflows.
- For CloudFormation/CDK validation, compliance checks, deployment troubleshooting, and CDK reference lookups, use the configured AWS IaC MCP server.
- For current AWS service facts, prefer `aws-mcp` from the AWS plugins. Use only configured plugin-backed AWS MCP surfaces; do not add legacy standalone AWS MCP endpoints.
- Use Context7 for current library/framework documentation when relevant.
- Use Superpowers skills when their process matches the task: brainstorming, planning, TDD, systematic debugging, parallel-agent execution, code review, and verification before completion.
- If a Claude sample plugin is not installed in Codex, use the closest installed equivalent and state the gap instead of pretending the plugin exists.

## Production Safety

- Prefer read-only or least-privilege credentials for AWS or production-like investigation.
- Treat unknown environments as production until proven otherwise.
- Prefer `list`, `describe`, `get`, dry-run, plan, synth, or diff operations before any mutating operation.
- Use `aws-security-guidelines` for AWS resource, IaC, deployment, and security review work; pair it with AWS Core/Data Analytics skills for service-specific workflows and verify current facts with `aws-mcp` or the AWS IaC MCP server where applicable.
- Do not delete, terminate, modify production resources, deploy, or disable safety protections without explicit user direction and a clear impact statement.
- Never inline secrets in code, docs, configs, tests, prompts, or command examples.
- For IaC, deploy scripts, CI/CD, and shell tooling, static checks are necessary but not sufficient. Require executable validation such as deploy/smoke/teardown or the closest safe equivalent; if it cannot run, record that the live-validation gate remains open.
