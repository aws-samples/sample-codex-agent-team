---
name: git-workflow
description: Conventional commit style, branch naming, non-interactive git usage, pull request flow, and merge-conflict handling. Use when working with version control, creating branches, writing commits, pushing, opening PRs, or resolving conflicts.
---

# Git Workflow

Use these conventions when working with version control.

## Non-Interactive Git

All git commands must be non-interactive:

```bash
git --no-pager log -10
git --no-pager diff
GIT_PAGER=cat git show HEAD
git commit -m "feat(auth): add login endpoint"
git merge --no-edit feature-branch
git rebase --no-edit main
```

Never rely on an editor opening for commit, merge, rebase, or PR text. Provide messages through flags or files.

## Commit Messages

Use Conventional Commits:

```text
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Good: `feat(auth): add OAuth2 callback handling`
Bad: `fixed stuff`

## Branch Naming

```text
<type>/<ticket-or-slug>-<description>
```

Examples:
- `feature/auth-api-login`
- `fix/null-pointer-crash`
- `docs/deploy-runbook`

## Common Operations

```bash
git status --short
git --no-pager diff
git --no-pager diff --staged
git stash push -m "WIP: auth middleware"
git stash pop
git cherry-pick <sha>
git reset --soft HEAD~1
```

Avoid destructive operations such as `git reset --hard`, force pushes, and broad cleans unless the user explicitly asks and the impact is clear.

## Merge Conflict Resolution

1. Run `git status --short`.
2. Inspect both sides of each conflict.
3. Remove conflict markers.
4. Run relevant tests or checks.
5. Continue with `git rebase --continue` or `git merge --continue`.

When resolving conflicts, assume the other side may contain user or peer work. Do not discard it without understanding it.

## Pre-Push Checks

Before pushing or opening a PR, run the repository's relevant verification:
- lint
- formatting check
- unit tests
- type checks
- build or package validation when appropriate

## Worktrees

Use worktrees when parallel work needs isolation beyond file-disjoint task scopes, or when an implementation plan explicitly calls for isolated branches.

```bash
git worktree add ../project-feature feature/my-feature
git worktree list
git worktree remove ../project-feature
```

## Team Integration

- The lead creates or recommends branches for spec-driven work.
- Coding and devops agents keep changes within assigned file scopes.
- Review agents use `git diff` or provided changed-file lists to understand the review surface.
- After review PASS, use the repository's established PR flow. If no flow exists, use `gh` CLI non-interactively when available and approved.
