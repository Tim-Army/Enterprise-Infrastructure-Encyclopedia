# Chapter 02: Foundations — Git and Repositories

## Learning Objectives

- Explain Git basics (commits, branches, remotes).
- Create and clone a repository.
- Commit changes and push to GitHub.
- Create a branch and open a pull request.
- Complete a walkthrough for each Git-and-repositories topic.

## Theory and Architecture

**GitHub Foundations** begins with **Git** — the distributed version-control system underneath GitHub. A
**repository** holds the project and its full history. **Git** tracks changes as **commits** (snapshots
with a message and parent), grouped on **branches** (movable pointers; `main` is the default). Work flows
**working tree → staging area (`git add`) → commit (`git commit`) → remote (`git push`)**, and a
**remote** (`origin`) links the local repo to GitHub. GitHub adds collaboration on top: **forks** (your
copy of someone's repo), **branches** for parallel work, and **pull requests (PRs)** to propose merging a
branch — the unit of review and collaboration. Understanding the commit/branch/remote model and the
clone→commit→push→PR flow is the foundation the rest of the platform builds on. This chapter teaches Git
and repositories with hands-on `git`/`gh` walkthroughs.

## Design Considerations

Commit **small, logical** changes with clear messages. Work on **branches**, not directly on `main`.
Keep the local branch in sync with the remote (`pull`/`push`). Use a **`.gitignore`** to keep build
artifacts and secrets out of history. Open a **pull request** for every change so it can be reviewed
(Chapter 03) before merging to `main`.

## Implementation and Automation

The labs initialize a repository, commit and push, and create a branch and pull request — the Git and
GitHub foundation the Foundations exam validates.

## Validation and Troubleshooting

Confirm Git and repositories:

```text
Repo = project + full history; commit = snapshot (+message/parent); branch = movable pointer (main default)
Flow: working tree -> git add (stage) -> git commit -> git push (to remote origin)
GitHub: fork (your copy) + branch (parallel work) + pull request (propose + review a merge)
.gitignore keeps artifacts/secrets out of history
```

Common pitfalls: committing directly to **`main`** instead of a branch + PR; and committing secrets or
build output (use **`.gitignore`**).

## Security and Best Practices

Never commit secrets (use `.gitignore` and secret scanning, Chapter 06). Work on branches with PR review,
and sign commits where required. All work is authorized development of your own repositories.

## Hands-On Lab

Git-and-repositories walkthroughs. **Shared prerequisites** — a free GitHub account, local `git` and
`gh`. **Cost:** none.

### Lab 2.1 — Create and clone a repository

**Objective:** Start a project on GitHub.

```bash
gh repo create foundations-demo --private --clone --add-readme
cd foundations-demo
git log --oneline
```

```text
✓ Created repository octocat/foundations-demo on GitHub
✓ Cloned repository
a1b2c3d (HEAD -> main, origin/main) Initial commit
```

**Expected result:** a private repository created and cloned, with an initial commit on `main`.

**Negative test:** create a public repo for private code by omitting `--private`; specify visibility
deliberately.

**Cleanup:** (repo removed at the end of Lab 2.4).

### Lab 2.2 — Commit and push a change

**Objective:** Record and publish a change.

```bash
echo "build/" > .gitignore
git add .gitignore
git commit -m "Add .gitignore for build artifacts"
git push
git log --oneline -1
```

```text
[main e4f5g6h] Add .gitignore for build artifacts
a1b2c3d..e4f5g6h  main -> main
e4f5g6h (HEAD -> main, origin/main) Add .gitignore for build artifacts
```

**Expected result:** the change staged, committed with a clear message, and pushed to `origin/main`.

**Negative test:** `git commit -am` a huge mix of unrelated changes; commit **small, logical** changes
with focused messages.

**Cleanup:** none yet.

### Lab 2.3 — Branch for a change

**Objective:** Work on a branch, not `main`.

```bash
git switch -c feature/add-docs
echo "# Docs" > docs.md
git add docs.md && git commit -m "Add docs page"
git push -u origin feature/add-docs
```

```text
Switched to a new branch 'feature/add-docs'
[feature/add-docs 7h8i9j0] Add docs page
branch 'feature/add-docs' set up to track 'origin/feature/add-docs'.
```

**Expected result:** a feature branch with its own commit, pushed and tracking the remote.

**Negative test:** commit the docs change straight to `main`; branch first so the change can be reviewed
in a PR.

**Cleanup:** none yet.

### Lab 2.4 — Open a pull request

**Objective:** Propose the branch for merge.

```bash
gh pr create --title "Add docs page" --body "Adds a docs.md page" --base main --head feature/add-docs
gh pr view --json number,state,baseRefName --jq '{number, state, base: .baseRefName}'
```

```text
https://github.com/octocat/foundations-demo/pull/1
{ "number": 1, "state": "OPEN", "base": "main" }
```

**Expected result:** an open pull request from the feature branch to `main` — ready for review.

**Negative test:** merge the branch locally and push to `main` with no PR; open a **pull request** so the
change is reviewed.

**Cleanup:**

```bash
gh repo delete octocat/foundations-demo --yes
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Foundations rests on Git: repositories holding history, commits as snapshots on branches, and the
working-tree → add → commit → push flow to a remote — with GitHub adding forks, branches, and pull
requests as the unit of review, all worked on branches (never directly on `main`) with a `.gitignore`
keeping artifacts and secrets out.

- [ ] I can explain commits, branches, and remotes.
- [ ] I can create and clone a repository.
- [ ] I can commit and push a change.
- [ ] I can branch and open a pull request.
- [ ] I completed Labs 2.1–2.4 including each negative test.
