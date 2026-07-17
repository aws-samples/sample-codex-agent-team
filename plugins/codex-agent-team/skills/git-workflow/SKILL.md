---
name: git-workflow
description: Use when creating branches or commits, inspecting history or diffs, resolving conflicts, pushing changes, opening pull requests, or using worktrees.
---

# Git Workflow

## Core Principle

Treat the working tree as shared user state. Inspect before acting, preserve
unrelated changes, use non-interactive commands, verify the exact changes being
recorded, and distinguish local Git operations from external writes such as a
push or pull request.

Preserve user and peer work even when it is unstaged, unfamiliar, or outside
the current task.

Follow repository-local guidance, naming, signing, branch protection, and PR
conventions when they differ from these defaults.

## Inspect First

Before staging, committing, resolving conflicts, switching branches, rebasing,
cleaning, or changing history, run:

```bash
git status --short
git --no-pager diff
git --no-pager diff --staged
git branch --show-current
```

Use `git --no-pager log`, `git show`, `git diff <base>...HEAD`, and
`git blame` as needed to understand history. Do not infer that an unfamiliar
change is disposable. Assume it belongs to the user or a peer.

If files you need contain unrelated edits, read the combined state carefully
and make a scoped patch. Never revert unrelated work merely to simplify your
diff.

## Non-Interactive Operation

Never depend on an editor, pager, prompt, or attached TTY. Provide messages and
content through arguments or files:

```bash
git --no-pager log -10 --oneline
GIT_PAGER=cat git show HEAD
git commit -m "feat(auth): add login endpoint"
git commit -F /tmp/commit-message.txt
git merge --no-edit feature-branch
git rebase --continue
```

For commands that may open an editor, set an appropriate non-interactive
editor only when the operation is understood. Do not automate an interactive
rebase blindly.

## Branches

Use the repository's established branch pattern. Otherwise prefer concise,
descriptive names:

```text
feature/auth-api-login
fix/null-pointer-crash
docs/deploy-runbook
refactor/order-validation
```

Before creating or switching a branch, inspect the dirty tree and determine
whether existing changes belong on the current branch. Do not stash, move, or
discard user work without understanding the consequence.

Create a branch from the intended base:

```bash
git fetch --prune
git switch main
git pull --ff-only
git switch -c feature/auth-api-login
```

`fetch`, `pull`, and remote operations may require network approval. Do not
assume the remote default branch or rewrite local work to match it.

## Commits

Use Conventional Commits when the repository has no stronger convention:

```text
<type>(<optional-scope>): <imperative subject>

<optional body explaining why and material tradeoffs>

<optional footer>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`,
`chore`.

Examples:

```text
feat(auth): add OAuth callback validation
fix(deploy): preserve terraform failure status
docs(runbook): document rollback verification
```

Before committing:

1. Re-run `git status --short`.
2. Inspect unstaged and staged diffs.
3. Stage only intended paths or hunks.
4. Confirm no secrets, generated residue, temporary logs, or unrelated files
   are included.
5. Run relevant verification.
6. Write a message that describes the actual change and why it exists.

Do not use broad staging such as `git add -A` when the tree includes unrelated
work. After committing, inspect `git show --stat --oneline HEAD` and the final
status.

## Merge Conflict Resolution

Resolve conflicts by understanding both sides:

1. Run `git status --short` and identify the operation in progress.
2. Read the base/current/incoming intent and nearby history.
3. Remove `<<<<<<<`, `=======`, and `>>>>>>>` markers after producing a
   coherent result.
4. Search for remaining conflict markers.
5. Stage only resolved files.
6. Run affected tests, lint, type checks, and builds.
7. Continue the merge, cherry-pick, or rebase non-interactively.

Do not choose `ours` or `theirs` across a file merely to end the conflict.
Generated files may need regeneration from the merged sources rather than
manual line selection.

If conflict resolution changes an interface used by peer work, report that
before continuing dependent work.

## Safety Boundaries

- Do not run `git reset --hard`, destructive checkout/restore, a broad clean
  with `git clean`, history rewriting, branch deletion, or force push unless the
  user explicitly requests the exact action and its impact is clear.
- Prefer `--force-with-lease` over an unqualified force push only when a
  history rewrite has been explicitly approved.
- Do not delete stashes, branches, tags, or worktrees merely because they look
  stale.
- Do not bypass hooks, signing, required checks, or branch protection to make a
  commit or push succeed.
- Never commit secrets or credentials. Stop and report suspected secret
  material.

These boundaries apply even when an operation appears recoverable through the
reflog. Recovery possibility is not authorization.

## Worktrees

Use worktrees when implementation needs branch isolation, an approved plan
requires it, or parallel work cannot remain file-disjoint in one tree.

```bash
git worktree list
git worktree add ../project-feature -b feature/my-feature main
git -C ../project-feature status --short
```

Choose a path outside the current repository's tracked tree. Verify the
worktree's branch and baseline before editing. Do not remove a worktree until
its changes are committed, transferred, or explicitly discarded.

Before removal, inspect:

```bash
git -C ../project-feature status --short
git worktree list
```

Removing a dirty worktree or deleting its branch is destructive and requires
clear direction.

## Pre-Push Verification

Run the repository checks that would block CI for the changed files:

- formatting check
- lint
- type checking
- focused and relevant full tests
- build/package verification
- generated-file, security, or policy checks when required

Use pinned local tools and committed wrappers. Inspect the complete branch diff
against its intended base. A successful local subset does not justify skipping
documented CI gates.

## GitHub And Remote Handoff

Pushing, creating or editing a GitHub issue/PR, posting comments, adding
reviewers, changing labels, and merging are external writes. Obtain the
required approval before performing them.

Use `gh` CLI non-interactively when available:

```bash
git push -u origin feature/auth-api-login
gh pr create --title "feat(auth): add login endpoint" --body-file /tmp/pr.md
gh pr view --web=false
gh pr checks
```

Write PR content from the actual diff and verification evidence. Include
purpose, important design choices, tests, rollout/rollback when relevant, and
open risks. Do not claim checks passed when they did not run.

## Completion Report

Report:

- branch and base
- files or commits affected
- exact verification commands and outcomes
- commit SHA and subject when a commit was requested
- remote/PR/issue action when approved and performed
- dirty-tree state, conflicts, blockers, and open risks

Do not create a commit, push, or PR unless the user asked for that action. A
code-edit request alone does not imply a Git history or GitHub write.
