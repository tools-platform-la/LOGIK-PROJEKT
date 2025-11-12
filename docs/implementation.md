# Implementation: Forking, Syncing, and Contributing

Last updated: 2025-11-12

This document describes how we work from the fork `tools-platform-la/LOGIK-PROJEKT` and contribute changes back to the upstream project `flamelogik/LOGIK-PROJEKT`.

## Remotes

- `origin`: https://github.com/tools-platform-la/LOGIK-PROJEKT.git
- `upstream`: https://github.com/flamelogik/LOGIK-PROJEKT.git

## Prerequisites

- Git 2.23+ and a GitHub account
- SSH key or HTTPS auth set up
- Identify yourself:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Optional but recommended:

```bash
git config --global pull.rebase false         # prefer explicit rebase commands
git config --global commit.gpgsign true       # sign commits if you use GPG/SSH signing
```

## One‑time setup

```bash
git clone https://github.com/tools-platform-la/LOGIK-PROJEKT.git
cd LOGIK-PROJEKT
git remote add upstream https://github.com/flamelogik/LOGIK-PROJEKT.git
git remote -v   # verify origin and upstream
```

## Keep `main` in sync with upstream (preferred: rebase)

We keep a linear history on our fork’s `main`. Only force‑push to your fork (`origin`), never to upstream.

```bash
git fetch upstream
git switch main    # or: git checkout main
git rebase upstream/main
# If history changed, update your fork:
git push origin main --force-with-lease
```

UI alternative: on GitHub, use “Sync fork → Update branch”.

## Day‑to‑day feature workflow

1) Start from an up‑to‑date `main` (steps above).
2) Create a topic branch:

```bash
git switch -c feature/<topic>
```

3) Make focused commits with clear messages.
4) Keep your branch fresh before pushing/PR:

```bash
git fetch origin
git rebase origin/main
```

5) Push the branch to your fork:

```bash
git push -u origin feature/<topic>
```

## Open a Pull Request to upstream

- Base repo: `flamelogik/LOGIK-PROJEKT`, base branch: `main`
- Head repo: `tools-platform-la/LOGIK-PROJEKT`, branch: `feature/<topic>`

Checklist for the PR description:

- Problem summary and solution approach
- Testing steps/results (screens, logs, or commands)
- Backward compatibility or migration notes (if any)
- Enable “Allow edits by maintainers” so upstream can help tweak your branch

## Keep your PR updated

When upstream moves, rebase your branch and update the PR:

```bash
git fetch upstream
git rebase upstream/main
# Resolve conflicts, then continue:
git push --force-with-lease
```

Prefer `rebase` over `merge` for cleaner history in your branch/PR.

## Conflict resolution quick guide

```bash
git status                              # see conflicted files
# edit files to resolve conflicts
git add <files>
git rebase --continue                   # or: git merge --continue

# if you need to start over during a rebase
git rebase --abort
```

## Optional: GitHub CLI helpers

```bash
# sync fork (fast‑forward) from upstream/main into your fork’s main
gh repo sync tools-platform-la/LOGIK-PROJEKT -b main

# open a PR from current branch to upstream
gh pr create --repo flamelogik/LOGIK-PROJEKT --base main --head tools-platform-la:$(git branch --show-current)
```

## Hygiene

- Do not commit directly to `main`; always use feature branches
- Keep PRs small and focused
- Avoid committing large binaries; update `.gitignore` when needed
- Branch naming: `feature/<topic>`, `fix/<issue-id>`, `docs/<area>`

## Quick reference

```bash
# Add upstream
git remote add upstream https://github.com/flamelogik/LOGIK-PROJEKT.git

# Sync main
git fetch upstream && git switch main && git rebase upstream/main && git push origin main --force-with-lease

# New branch
git switch -c feature/<topic>

# Update branch before PR
git fetch origin && git rebase origin/main

# Push branch
git push -u origin feature/<topic>
```

