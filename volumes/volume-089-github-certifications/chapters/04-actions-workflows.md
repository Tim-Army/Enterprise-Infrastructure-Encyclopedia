# Chapter 04: Actions — Workflows

## Learning Objectives

- Explain the GitHub Actions workflow model (events, jobs, steps, runners).
- Write a workflow triggered by an event.
- Use a matrix to run jobs in parallel.
- Use marketplace and composite actions.
- Complete a walkthrough for each workflow topic.

## Theory and Architecture

**GitHub Actions** automates work in response to repository **events**. A **workflow** is a YAML file in
`.github/workflows/`. It declares **`on`** (the triggering events — `push`, `pull_request`, `schedule`,
`workflow_dispatch`, and more), and one or more **jobs**. Each **job** runs on a **runner**
(GitHub-hosted like `ubuntu-latest`, or self-hosted) and contains ordered **steps** — each step either
**`run`s** a shell command or **`uses`** an **action** (a reusable unit, e.g., `actions/checkout`). Jobs
run in parallel by default and can depend on each other (`needs`) or fan out with a **matrix** (running
the same job across versions/OSes). Actions come from the workflow's own repo, the **Marketplace**, or
**composite** actions you author. Understanding events → jobs → steps → runners, and the YAML that
expresses them, is the core of the Actions certification. This chapter teaches workflows with hands-on
walkthroughs.

## Design Considerations

Trigger workflows on the **right events** (CI on `push`/`pull_request`; manual runs via
`workflow_dispatch`; scheduled jobs via `schedule`). Pin **actions** to a version/SHA for
reproducibility and security. Use a **matrix** to test across versions in parallel. Choose
**GitHub-hosted** runners for simplicity or **self-hosted** for special hardware/network — and harden
self-hosted runners. Keep workflows small and composable.

## Implementation and Automation

The labs write an event-triggered workflow, add a matrix, and use a marketplace action — the workflow
model the Actions exam validates.

## Validation and Troubleshooting

Confirm the workflow model:

```text
Workflow (.github/workflows/*.yml): on (events) -> jobs -> steps (run | uses action)
Runners: GitHub-hosted (ubuntu-latest) or self-hosted; jobs parallel by default, needs = dependency
Matrix: fan a job across versions/OSes; actions from repo / Marketplace / composite
Events: push, pull_request, schedule, workflow_dispatch, ...
```

Common pitfalls: pinning an action to a **mutable tag** (`@main`) — pin to a version/SHA; and running
everything in one giant job instead of parallel jobs/matrix.

## Security and Best Practices

Pin actions to a SHA/version, limit `GITHUB_TOKEN` permissions (Chapter 05), and harden self-hosted
runners. Workflows act on your own repositories with least privilege. All work is authorized.

## Hands-On Lab

Workflow walkthroughs. **Shared prerequisites** — a GitHub repo with `gh`, and the ability to add files
under `.github/workflows/`. **Cost:** none (GitHub-hosted runner minutes on the free tier).

### Lab 4.1 — Write an event-triggered workflow

**Objective:** Run a job on push.

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [ main ]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: echo "Building on ${{ runner.os }}"
```

```text
# after committing and pushing:
gh run list --workflow=ci.yml --json name,conclusion --jq '.[0]'
{ "name": "CI", "conclusion": "success" }
```

**Expected result:** a workflow that checks out the repo and runs a build step on every push to `main`
(and on manual dispatch).

**Negative test:** trigger on **every** branch's every event when you only need `main`; scope `on` to the
events you want.

**Cleanup:** none yet.

### Lab 4.2 — Fan out with a matrix

**Objective:** Run a job across versions in parallel.

```yaml
# add to ci.yml
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [ 18, 20, 22 ]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: node --version
```

```text
# three parallel jobs: test (18), test (20), test (22)
```

**Expected result:** the `test` job runs three times in parallel — once per Node version — via the
matrix.

**Negative test:** copy-paste three near-identical jobs for three versions; use a **matrix** instead.

**Cleanup:** none yet.

### Lab 4.3 — Use a marketplace action pinned to a version

**Objective:** Reuse a trusted action safely.

```yaml
# a step using a versioned marketplace action
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: ./dist
```

```text
# artifact 'build-output' uploaded and downloadable from the run
```

**Expected result:** a marketplace action reused at a pinned major version — reproducible and reviewable.

**Negative test:** reference `actions/upload-artifact@main`; a mutable ref can change under you — pin to
`@v4` (or a SHA).

**Cleanup:** none yet.

### Lab 4.4 — Inspect a run

**Objective:** Confirm the workflow executed.

```bash
gh run list --workflow=ci.yml --limit 1
gh run view --log | grep -m1 "Building on"
```

```text
completed  success  CI  main  push
Building on Linux
```

**Expected result:** the run listed as `success` with the expected step output — the workflow ran.

**Negative test:** assume a workflow ran because the file exists; check `gh run list`/`view` — a syntax
error or wrong trigger means it never ran.

**Cleanup:**

```bash
git rm .github/workflows/ci.yml && git commit -m "Remove demo workflow" && git push
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub Actions runs workflows (YAML in `.github/workflows/`) on events, composed of jobs on GitHub-hosted
or self-hosted runners, each with steps that `run` commands or `use` actions — parallel by default, fanned
out with a matrix, and built from marketplace or composite actions pinned to a version or SHA.

- [ ] I can explain events, jobs, steps, and runners.
- [ ] I can write an event-triggered workflow.
- [ ] I can fan out a job with a matrix.
- [ ] I can use a pinned marketplace action.
- [ ] I completed Labs 4.1–4.4 including each negative test.
