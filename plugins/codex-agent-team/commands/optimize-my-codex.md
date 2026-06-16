---
description: Audit and improve a Codex setup under `~/.codex` and `~/.agents`.
---

Use the `optimize-my-codex` skill to audit and improve the Codex setup for `$ARGUMENTS`.

If `$ARGUMENTS` names a focus area, limit the audit to that area. Useful focus areas include `config`, `agents`, `hooks`, `rules`, `skills`, `plugins`, `marketplace`, and `commands`. If no focus area is provided, review the full Codex setup under `~/.codex` and `~/.agents`.

Start by inventorying the relevant files and presenting findings grouped by High Impact, Medium Impact, Low Impact, and No Changes Needed. Do not edit the Codex setup until the user approves specific proposed changes.

When changes are approved, make the smallest safe edits, preserve local customizations, validate changed JSON/TOML/YAML where applicable, and summarize what changed, why it changed, what was validated, and any follow-up improvements.
