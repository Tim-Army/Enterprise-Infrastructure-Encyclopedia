# Chapter 03: Foundations — Collaboration

## Learning Objectives

- Track work with issues and labels.
- Review and merge pull requests.
- Organize work with GitHub Projects.
- Reason about Discussions, Pages, and releases.
- Complete a walkthrough for each collaboration topic.

## Theory and Architecture

**GitHub Foundations** covers the collaboration features built around repositories. **Issues** track
work, bugs, and ideas — with **labels**, **assignees**, **milestones**, and cross-links to PRs.
**Pull requests** are where change is **reviewed**: reviewers comment, request changes, or approve, and
CI checks (Chapters 04–05) must pass before merge. **GitHub Projects** is a flexible planning board
(tables and boards with custom fields) that spans issues and PRs across repos. **Discussions** host
open-ended Q&A and community conversation; **Pages** publishes a static site from a repo; **releases**
package tagged versions with notes and assets; and the whole platform supports **@mentions**, **teams**,
and notifications. Understanding how issues, PRs, reviews, and Projects fit together is core to
collaborating on GitHub. This chapter teaches collaboration with hands-on `gh` walkthroughs.

## Design Considerations

Use **issues** to track work and **link** PRs to them (closing keywords auto-close issues on merge).
Require **PR review** (and passing checks) before merge via branch protection/rulesets (Chapter 07).
Plan with **Projects** across repositories. Use **Discussions** for questions (not issues) and **Pages**
for docs/sites. Tag **releases** for versioned deliverables.

## Implementation and Automation

The labs create and label an issue, review and merge a PR, and organize work in a Project — the
collaboration the Foundations exam validates.

## Validation and Troubleshooting

Confirm collaboration:

```text
Issues: track work (labels/assignees/milestones); link to PRs (closing keywords auto-close)
Pull requests: review (comment/request-changes/approve) + checks -> merge
Projects: planning boards/tables spanning issues + PRs across repos
Discussions (Q&A) | Pages (static site) | releases (tagged versions + notes/assets)
```

Common pitfalls: using **issues** for open-ended questions (use **Discussions**); and merging a PR
without **review** or passing checks — require both.

## Security and Best Practices

Require review and passing checks before merge, and use least-privilege team access (Chapter 07).
Collaboration controls protect code quality and integrity. All work is authorized.

## Hands-On Lab

Collaboration walkthroughs. **Shared prerequisites** — a GitHub repo (recreate `foundations-demo`), `gh`.
**Cost:** none.

### Lab 3.1 — Create and label an issue

**Objective:** Track a unit of work.

```bash
gh issue create --title "Add contributing guide" --body "We need CONTRIBUTING.md" --label "documentation"
gh issue list --json number,title,labels --jq '.[] | {number, title, labels: [.labels[].name]}'
```

```text
{ "number": 1, "title": "Add contributing guide", "labels": ["documentation"] }
```

**Expected result:** a labeled issue tracking the work — visible and triageable.

**Negative test:** open a vague issue with no title/label; write a clear title and label so it can be
triaged.

**Cleanup:** none yet.

### Lab 3.2 — Link a PR to an issue

**Objective:** Auto-close the issue on merge.

```bash
git switch -c docs/contributing
echo "# Contributing" > CONTRIBUTING.md
git add CONTRIBUTING.md && git commit -m "Add contributing guide

Closes #1"
git push -u origin docs/contributing
gh pr create --title "Add contributing guide" --body "Closes #1" --base main
```

```text
https://github.com/octocat/foundations-demo/pull/2
```

**Expected result:** a PR whose body `Closes #1` links it to the issue — merging will auto-close issue 1.

**Negative test:** open a PR unlinked to its issue; use a **closing keyword** (`Closes #1`) so the issue
resolves on merge.

**Cleanup:** none yet.

### Lab 3.3 — Review and merge a pull request

**Objective:** Approve and merge after review.

```bash
gh pr review 2 --approve --body "LGTM"
gh pr merge 2 --squash --delete-branch
gh issue view 1 --json state --jq '.state'
```

```text
✓ Approved pull request #2
✓ Squashed and merged pull request #2
✓ Deleted branch docs/contributing
CLOSED
```

**Expected result:** the PR reviewed, squash-merged, its branch deleted, and issue 1 auto-closed — the
review-and-merge flow.

**Negative test:** merge your own PR with no review on a shared repo; require **review** (enforced by
rulesets, Chapter 07).

**Cleanup:** none yet.

### Lab 3.4 — Organize work in a Project

**Objective:** Plan across issues and PRs.

```bash
gh project create --owner octocat --title "Roadmap"
gh project item-add 1 --owner octocat --url https://github.com/octocat/foundations-demo/issues/1
gh project item-list 1 --owner octocat --format json --jq '.items | length'
```

```text
1
```

**Expected result:** a Project board with the issue added — planning that spans repositories.

**Negative test:** track a cross-repo roadmap in a single repo's issues; use a **Project** to span repos.

**Cleanup:**

```bash
gh repo delete octocat/foundations-demo --yes
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub collaboration runs on issues (labeled, assigned, linked to PRs with closing keywords), pull
requests reviewed and merged after passing checks, and Projects planning across repositories — with
Discussions for Q&A, Pages for sites, and releases for versioned deliverables.

- [ ] I can create and label an issue.
- [ ] I can link a PR to an issue.
- [ ] I can review and merge a pull request.
- [ ] I can organize work in a Project.
- [ ] I completed Labs 3.1–3.4 including each negative test.
