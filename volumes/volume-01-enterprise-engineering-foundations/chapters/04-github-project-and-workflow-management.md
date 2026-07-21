# Chapter 04: GitHub Project and Workflow Management

![Lab flow for this chapter: an issue is linked to a GitHub Project board, and a pull request whose body uses the documented closing-keyword syntax auto-closes the issue on merge, while a pull request that only references the issue inside a code comment leaves it open.](../../../diagrams/volume-01-enterprise-engineering-foundations/chapter-04-linked-issue-pull-request-flow.svg)

*Figure 4-1. Flow used throughout this chapter's Hands-On Lab: an issue linked to a Project board and closed automatically only via the documented closing-keyword syntax, including the informal-reference negative test.*

## Learning Objectives

- Structure work using issues, labels, milestones, and GitHub Projects (v2)
  so status is derived from the repository rather than a separate tool.
- Design issue and pull request templates that enforce the information a
  reviewer or triager actually needs.
- Configure a review workflow — required reviewers, status checks, and a
  merge queue — that scales past a handful of contributors.
- Automate project board transitions with the GitHub CLI and GitHub Actions
  instead of manual board maintenance.
- Diagnose common failures in required-check and merge-queue configuration.

## Theory and Architecture

GitHub project and workflow management is the discipline of using a Git
hosting platform's native planning primitives — issues, labels, milestones,
Projects, pull requests, and their automation hooks — as the system of
record for work, instead of maintaining a parallel project-management tool
that inevitably drifts out of sync with what the repository actually
contains. This matters at enterprise scale because the alternative —
status tracked in a separate tool, disconnected from the commits and pull
requests that represent the actual work — creates a permanent
reconciliation burden and a single point where the two views disagree.

### The primitive hierarchy

GitHub's planning primitives form a hierarchy, from least to most
structured:

1. **Issues** — the atomic unit of trackable work: a bug, a feature
   request, a chapter to be written, a chore.
2. **Labels** — a flat, cross-cutting taxonomy applied to issues and pull
   requests (type, priority, area, status).
3. **Milestones** — a date- or release-bound grouping of issues, useful for
   answering "what ships in this cycle."
4. **Projects (v2)** — a spreadsheet/board view built from saved queries
   over issues and pull requests across one or more repositories, with
   custom fields (status, iteration, estimate) layered on top without
   modifying the underlying issue.

A key architectural property of Projects (v2) is that its custom fields
live on the *project item*, not on the issue itself — the same issue can
appear in multiple projects with different status values in each, and the
issue's own state (open/closed) remains the single ground truth that other
automation reads.

### Pull requests as the unit of review

A pull request is simultaneously a diff, a discussion thread, a CI
execution context, and — through "Closes #123" linking syntax — an edge in
the work graph connecting a change back to the issue that motivated it.
Enterprise workflow management treats this linkage as mandatory for
non-trivial changes specifically so that closing an issue and merging its
implementing change are auditable as the same event.

### Review workflow models

| Model | Mechanism | Best suited for |
| --- | --- | --- |
| Direct required review | Branch protection requires N approvals before merge | Small to mid-size teams, most enterprise repositories |
| CODEOWNERS-scoped review | Required reviewers vary by changed path ([Chapter 02](02-repository-architecture.md)) | Repositories with distinct ownership domains |
| Merge queue | PRs are serialized and re-tested against the latest `main` before merge | High-throughput repositories where parallel merges cause integration conflicts |

A merge queue solves a specific problem direct required review does not: on
a busy repository, two individually passing pull requests can still break
`main` when combined, because each was only tested against an earlier
version of `main`. The merge queue re-validates each PR against the
current `main` immediately before merging it, serializing integration
without requiring a human to manually re-run checks after every merge.

## Design Considerations

- **Labels as a controlled vocabulary, not free text.** Uncontrolled label
  creation produces near-duplicate labels (`bug`, `Bug`, `defect`) that
  fragment reporting. Define a small, documented label taxonomy (type,
  priority, area, status) and enforce it through a label-sync configuration
  file rather than ad hoc creation in the UI.
- **One project board or many.** A single cross-repository project
  simplifies portfolio-level status reporting but requires disciplined
  custom-field conventions across teams; per-repository or per-team
  projects reduce coordination overhead but fragment cross-cutting
  visibility. Choose based on who actually needs to see status across team
  boundaries and how often.
- **Issue templates vs. blank issues.** Structured issue-form templates
  (YAML-defined forms) capture consistent, machine-parseable fields at
  creation time; a blank issue is faster to file but pushes the burden of
  extracting the same information onto whoever triages it. Reserve blank
  issues for genuinely open-ended discussion.
- **When to require a merge queue vs. direct required review.** A merge
  queue adds latency (each PR waits for a fresh CI run in queue order) in
  exchange for integration safety; it earns its cost once concurrent PR
  volume makes post-merge breakage from combined changes a recurring
  problem, not before.
- **Draft pull requests.** Using draft PRs to signal "in progress, not
  ready for review" keeps CI and reviewer-assignment automation from firing
  prematurely, and is generally preferable to a `wip` label plus a
  ready-for-review label pair that requires manual maintenance.
- **Automation ownership.** Decide who owns the GitHub Actions workflows
  that move project items between states (see Implementation below) the
  same way you would decide ownership for any other automation — an
  unowned automation workflow is a workflow nobody notices has broken.

## Implementation and Automation

### 1. A structured issue form

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug report
description: Report a defect in a published chapter or the build tooling
labels: ["type:bug"]
body:
  - type: input
    id: location
    attributes:
      label: File or chapter path
      placeholder: volumes/volume-02-.../chapters/03-....md
    validations:
      required: true
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - "Blocking (build fails)"
        - "Major (technically incorrect)"
        - "Minor (typo, formatting)"
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: What is wrong, and what did you expect instead?
    validations:
      required: true
```

### 2. A pull request template

```markdown
<!-- .github/pull_request_template.md -->
## Summary

<!-- What does this change do, and why? -->

## Related issue

Closes #

## Validation

- [ ] `scripts/bash/validate.sh` passes locally
- [ ] Manually reviewed rendered Markdown for formatting issues

## Checklist

- [ ] Follows EDITORIAL_STANDARDS.md
- [ ] Updates INDEX.md/GLOSSARY.md if new terms were introduced
```

### 3. Label taxonomy as code

```yaml
# .github/labels.yml — synced with a label-sync GitHub Action
- name: "type:bug"
  color: "d73a4a"
  description: "Something is technically incorrect"
- name: "type:chore"
  color: "cfd3d7"
  description: "Maintenance work with no reader-visible change"
- name: "priority:high"
  color: "b60205"
- name: "status:blocked"
  color: "5319e7"
```

```yaml
# .github/workflows/label-sync.yml
name: Sync labels
on:
  push:
    branches: [main]
    paths: [".github/labels.yml"]
jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4
      - uses: crazy-max/ghaction-github-labeler@v5
        with:
          yaml-file: .github/labels.yml
```

### 4. Automating project board transitions with the GitHub CLI

```bash
# Add an issue to a project and set its Status field when it is assigned
gh project item-add 7 --owner example-org --url https://github.com/example-org/example-repo/issues/42

gh project item-edit \
  --project-id PVT_kwHOAbc123 \
  --id PVTI_lADOAbc123zM \
  --field-id PVTSSF_lADOAbc123zM \
  --single-select-option-id "in-progress-option-id"
```

### 5. Moving items automatically on pull request events

```yaml
# .github/workflows/project-automation.yml
name: Project automation
on:
  pull_request:
    types: [opened, ready_for_review, closed]

permissions:
  contents: read

jobs:
  update-status:
    runs-on: ubuntu-latest
    steps:
      - name: Move linked issue to In Review
        if: github.event.action == 'ready_for_review'
        env:
          GH_TOKEN: ${{ secrets.PROJECT_AUTOMATION_TOKEN }}
        run: |
          gh project item-edit \
            --project-id "${{ vars.PROJECT_ID }}" \
            --id "${{ github.event.pull_request.node_id }}" \
            --field-id "${{ vars.STATUS_FIELD_ID }}" \
            --single-select-option-id "${{ vars.IN_REVIEW_OPTION_ID }}"
```

### 6. Enabling a merge queue

```bash
gh api --method PATCH \
  repos/:owner/:repo/branches/main/protection \
  -f 'required_status_checks.contexts[]=validate' \
  -f required_status_checks.strict=true

gh api --method PUT \
  -H "Accept: application/vnd.github+json" \
  repos/:owner/:repo/merge_queue \
  -f merge_method=squash \
  -f 'grouping_strategy=ALLGREEN'
```

## Validation and Troubleshooting

- **Issue form validation ignored.** Structured issue forms only apply to
  issues created through the "New issue" template picker; issues filed via
  the API without going through the form schema bypass field validation
  entirely — do not assume every issue in the repository satisfies the
  form's `required` fields.
- **"Closes #123" not linking.** The closing keyword only auto-links and
  auto-closes when the pull request targets the repository's default
  branch and the keyword appears in the PR body (not just a commit
  message) or in the merge commit; verify by checking the issue's
  timeline for a "linked a pull request" event before relying on it.
- **Project automation token permission errors.** The default
  `GITHUB_TOKEN` cannot modify Projects (v2) items across organizations by
  default; a `403` from `gh project item-edit` inside a workflow usually
  means a fine-grained personal access token or GitHub App token with
  `project` write scope is required instead of the default token.
- **Merge queue stuck with no progress.** A merge queue entry that never
  completes usually indicates a required status check that never reports
  back for the queue's synthetic merge commit (common when a check is
  configured against `pull_request` events only, not `merge_group`
  events); add a `merge_group:` trigger to any workflow whose check is
  required by the queue.
- **Label sync deleting unexpected labels.** A label-sync action running
  in exact-sync mode removes any label not present in the source file,
  including ones created manually through the UI; audit `labels.yml`
  against the live label set before the first sync run in a repository
  with pre-existing labels.

## Security and Best Practices

- Scope the token used for project automation narrowly (a GitHub App
  installation token limited to `issues: write` and `projects: write` on
  the specific repositories that need it) rather than a broad personal
  access token stored as an organization-wide secret.
- Require status checks and reviews on the default branch even for
  small/trusted teams; the control matters most exactly when it is
  inconvenient, which is also when it is most likely to be skipped without
  enforcement.
- Treat issue templates as an input-validation boundary: a required
  severity/location field on a bug report reduces triage time and prevents
  low-signal reports from consuming reviewer attention disproportionately.
- Restrict who can convert a draft PR to ready-for-review versus who can
  approve it, so the "ready for review" signal reliably means CI and
  reviewer-assignment automation should fire.
- Audit project automation workflows (label sync, status transitions)
  periodically for stale references — a `single-select-option-id`
  referencing a since-renamed or deleted project field fails silently in
  many workflow configurations rather than producing an obvious error.
- Do not let a merge queue's `ALLGREEN` grouping strategy substitute for
  required review; the queue enforces integration testing, not human
  judgment, and both are required for a defensible review workflow.

## References and Knowledge Checks

**References**

- [GitHub documentation](https://docs.github.com/en) — Projects (v2), issue forms, and merge queue.
- [GitHub CLI (`gh`) manual](https://cli.github.com/manual/) — `gh project`, `gh issue`, `gh pr`.
- [templates/technical-review-checklist.md](../../../templates/technical-review-checklist.md)
  — this encyclopedia's own review gate, an example of a documented,
  enforceable workflow checklist.
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) — this repository's
  documented contribution workflow.

**Knowledge checks**

1. Why does a merge queue catch integration failures that direct required
   review, by itself, cannot?
2. What is the architectural reason a Projects (v2) custom field lives on
   the project item rather than on the issue?
3. Give an example of when per-team project boards are preferable to a
   single cross-repository project, and vice versa.
4. Why can an issue created through the GitHub API bypass an issue form's
   required fields?

## Hands-On Lab

**Objective:** Configure a structured issue template, a linked pull
request workflow, and a GitHub Project (v2) board with an automated status
transition, then prove the linkage and automation both work — and that a
malformed link fails to auto-close.

**Prerequisites**

- A GitHub repository you can configure (reuse the scratch repository from
  earlier chapters or create a new one) and `gh` CLI authenticated.
- Organization or personal account permission to create a Project (v2).

**Steps**

1. Add an issue template:

   ```bash
   mkdir -p .github/ISSUE_TEMPLATE
   cat > .github/ISSUE_TEMPLATE/task.yml <<'EOF'
   name: Task
   description: A trackable unit of work
   labels: ["type:task"]
   body:
     - type: textarea
       id: description
       attributes:
         label: Description
       validations:
         required: true
   EOF
   git add -A && git commit -m "feat: add task issue template"
   git push
   ```

2. Create an issue and a project, and link the issue to it:

   ```bash
   gh issue create --title "Lab task" --body "Demonstrates linked PR workflow" --label "type:task"
   gh project create --owner :owner --title "Workflow Lab"
   ```

   Note the issue number and the project number printed by each command.

3. Add the issue to the project:

   ```bash
   gh project item-add <project-number> --owner :owner \
     --url https://github.com/:owner/:repo/issues/<issue-number>
   ```

4. Create a branch and a pull request that correctly closes the issue:

   ```bash
   git checkout -b lab/close-issue
   echo "resolved" > lab-task.txt
   git add lab-task.txt
   git commit -m "feat: resolve lab task"
   git push -u origin lab/close-issue
   gh pr create --title "Resolve lab task" \
     --body "Closes #<issue-number>" --base main
   ```

5. **Expected result:** Open the issue in the GitHub UI (or run `gh issue
   view <issue-number>`) and confirm a "linked a pull request" reference
   appears in its timeline.

6. Merge the pull request:

   ```bash
   gh pr merge --squash --delete-branch
   ```

7. **Expected result:** Confirm the issue auto-closed:

   ```bash
   gh issue view <issue-number> --json state --jq .state
   ```

   Output must be `CLOSED`.

8. **Negative test:** Create a second issue and a pull request that
   references it only in a code comment, not in the PR body's closing
   keyword syntax:

   ```bash
   gh issue create --title "Lab task 2" --body "Should not auto-close" --label "type:task"
   git checkout -b lab/no-close
   echo "// relates to issue but does not close it" > lab-task-2.txt
   git add lab-task-2.txt
   git commit -m "feat: unrelated change referencing issue in a comment only"
   git push -u origin lab/no-close
   gh pr create --title "Does not close" --body "See lab-task-2.txt" --base main
   gh pr merge --squash --delete-branch
   gh issue view <second-issue-number> --json state --jq .state
   ```

   **Expected result:** Output is `OPEN` — confirming that only the
   documented closing-keyword syntax in the PR body triggers auto-close,
   not an informal reference elsewhere in the change.

9. **Cleanup:**

   ```bash
   gh issue close <second-issue-number>
   gh project delete <project-number> --owner :owner
   git checkout main && git pull
   git branch -D lab/close-issue lab/no-close
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub's native planning primitives — issues, labels, milestones, Projects
(v2), and pull requests — can serve as the sole system of record for work
when structured issue templates, closing-keyword linkage, and automated
status transitions are configured deliberately rather than left to manual
discipline. A merge queue adds integration safety that direct required
review alone cannot provide once PR throughput rises. Automation that moves
project items between states should run under a narrowly scoped
credential, not a broad personal token.

- [ ] Can design an issue template and label taxonomy that captures
      triage-relevant fields at creation time.
- [ ] Can explain why Projects (v2) custom fields are decoupled from the
      underlying issue.
- [ ] Can configure required reviews, required status checks, and a merge
      queue together.
- [ ] Can automate a project-item status transition from a GitHub Actions
      workflow with a correctly scoped token.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
