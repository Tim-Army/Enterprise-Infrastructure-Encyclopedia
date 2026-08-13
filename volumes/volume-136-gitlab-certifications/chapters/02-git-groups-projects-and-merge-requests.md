# Chapter 02: Git, Groups, Projects, and Merge Requests

## Learning Objectives

- Explain GitLab's group and project hierarchy and how permissions inherit.
- Use branching strategies and protected branches deliberately.
- Run code review through merge requests, approvals, and merge methods.
- Distinguish merge, squash, and rebase — and their effect on history.

## The hierarchy

GitLab organizes everything into **groups** containing **projects** (a project is a repository plus its issues, pipelines, registry, and settings). Groups nest, and **subgroups inherit** members and settings from their parents.

| Level | Holds | Why it matters |
|:---|:---|:---|
| **Group** | Projects, subgroups, shared runners, group-level settings and variables | Permissions and policy applied once, inherited everywhere below |
| **Subgroup** | Projects, further subgroups | Team or product boundaries within a larger organization |
| **Project** | Repository, issues, pipelines, registry, settings | The unit of work |

Inheritance is the design point: a member added at group level has that role in **every** project beneath it. This is efficient and it is also the commonest over-permissioning mistake — granting Maintainer at the top of the tree to solve one project's access problem hands that person Maintainer everywhere.

### Roles

GitLab's roles, in ascending order: **Guest**, **Reporter**, **Developer**, **Maintainer**, **Owner**. The two worth knowing precisely, because they appear in exam scenarios:

- **Developer** — push to unprotected branches, create merge requests, run pipelines. Cannot push to protected branches by default.
- **Maintainer** — manage project settings, protected branches, variables, and merge to protected branches.

## Protected branches

A **protected branch** restricts who may push and who may merge, and it is the mechanism behind every meaningful workflow control. Protecting `main` so that nobody pushes directly and only merge requests can merge is what makes code review actually enforced rather than merely encouraged.

Related controls: **push rules** (commit message patterns, file size limits, secret prevention), **approval rules** (Chapter 06), and **CODEOWNERS** files that require review from the people who own the touched paths.

## Merge requests

The **merge request (MR)** is GitLab's unit of code review and the center of its workflow. An MR bundles a source branch, a diff, discussion, approvals, and pipeline results, and it is where the platform's pieces converge — CI results and security findings surface in the MR rather than in a separate tool.

### Merge methods

| Method | Resulting history | Fits |
|:---|:---|:---|
| **Merge commit** | Preserves branch topology; adds a merge commit | Teams that want the full branching record |
| **Merge commit with semi-linear history** | Merge commit, but requires the source to be rebased first | A readable line of merges |
| **Fast-forward merge** | No merge commit; linear history; source must be rebased | Teams that want a strictly linear log |

**Squash** is orthogonal: it collapses an MR's commits into one on merge. Squashing gives a clean main-branch history at the cost of losing intermediate commits — good when branches contain messy work-in-progress commits, bad when the individual commits are meaningful and worth bisecting later.

## Hands-On Lab

Python models the workflow. **Cost:** none.

### Lab 2.1 — Role inheritance across the group tree

**Objective:** Show how a group-level grant propagates.

```bash
python3 - <<'EOF'
tree = {
  "acme":              {"parent": None,        "members": {"alice": "Owner"}},
  "acme/platform":     {"parent": "acme",      "members": {"bob": "Maintainer"}},
  "acme/platform/api": {"parent": "acme/platform", "members": {"carol": "Developer"}},
  "acme/platform/web": {"parent": "acme/platform", "members": {}},
  "acme/data":         {"parent": "acme",      "members": {"dan": "Reporter"}},
}
ORDER = ["Guest", "Reporter", "Developer", "Maintainer", "Owner"]

def effective(path, user):
    best, node = None, path
    while node:
        role = tree[node]["members"].get(user)
        if role and (best is None or ORDER.index(role) > ORDER.index(best)):
            best = role
        node = tree[node]["parent"]
    return best

for path in tree:
    roles = {u: effective(path, u) for u in ("alice","bob","carol","dan") if effective(path, u)}
    print(f"{path:22} {roles}")
print("\nbob is Maintainer on acme/platform, so he is Maintainer on api AND web — inheritance is")
print("the point AND the over-permissioning trap: grant at the LOWEST level that solves the problem.")
EOF
```

**Expected result:** Alice is Owner everywhere (granted at the root), Bob is Maintainer across both platform projects, Carol is Developer only on `api`, and Dan's Reporter role does not reach the platform tree at all. The closing line states the discipline: inheritance flows **down only**, so the fix for one project's access is a grant on that project, not at the top of the tree.

**Negative test:** Adding a contractor at the top-level group to give them access to one repository — they now hold that role across every project in the organization, including ones nobody intended them to see.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Protected branches and who can actually merge

**Objective:** Evaluate the push/merge decision the way GitLab does.

```bash
python3 - <<'EOF'
protection = {
  "main":    {"allowed_to_push": [],            "allowed_to_merge": ["Maintainer"], "require_mr": True},
  "release": {"allowed_to_push": ["Maintainer"],"allowed_to_merge": ["Maintainer"], "require_mr": True},
  "feature/*":{"allowed_to_push": ["Developer","Maintainer"], "allowed_to_merge": ["Developer","Maintainer"], "require_mr": False},
}
def can(action, branch, role):
    p = protection[branch]
    if action == "push":
        if not p["allowed_to_push"]:
            return f"DENIED — nobody may push directly to '{branch}'; changes must arrive via a merge request"
        return ("ALLOWED" if role in p["allowed_to_push"]
                else f"DENIED — push to '{branch}' requires {p['allowed_to_push']}")
    return ("ALLOWED" if role in p["allowed_to_merge"]
            else f"DENIED — merge to '{branch}' requires {p['allowed_to_merge']}")

for branch in protection:
    for role in ("Developer","Maintainer"):
        print(f"{role:11} push   -> {branch:10} : {can('push', branch, role)}")
        print(f"{role:11} merge  -> {branch:10} : {can('merge', branch, role)}")
    print()
print("Protecting main with NO direct push is what makes review mandatory rather than optional.")
EOF
```

**Expected result:** Nobody — not even a Maintainer — can push directly to `main`; merging there requires Maintainer; feature branches are open to Developers. The important structural insight is in the last line: a review policy that depends on people choosing to open merge requests is a convention, while an empty `allowed_to_push` list is a control.

**Negative test:** Leaving `main` unprotected and relying on team agreement — a rushed hotfix goes straight to `main` at 2 a.m., bypassing review, tests, and every security scan configured on merge requests.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Merge methods and what they do to history

**Objective:** Compare the resulting commit history.

```bash
python3 - <<'EOF'
main_before = ["A", "B"]
feature = ["C (wip)", "D (fix typo)", "E (address review)"]

def resulting_history(method, squash):
    commits = ["(squashed) feature: add search"] if squash else list(feature)
    if method == "merge commit":
        return main_before + commits + ["M (merge)"], "branch topology preserved"
    if method == "semi-linear":
        return main_before + commits + ["M (merge)"], "rebased first, then a merge commit — readable line of merges"
    return main_before + commits, "fast-forward: strictly linear, no merge commit"

for method in ("merge commit", "semi-linear", "fast-forward"):
    for squash in (False, True):
        hist, note = resulting_history(method, squash)
        print(f"{method:14} squash={str(squash):5} -> {hist}")
        print(f"{'':22} {note}")
    print()
print("Squash trades three honest commits for one clean one. Good when the branch is messy WIP;")
print("bad when each commit is a meaningful step you may want to bisect or revert independently.")
EOF
```

**Expected result:** Six combinations, showing squash collapsing three commits into one under every merge method. The trade in the closing lines is the judgment the exams probe: squashing is a history-quality decision, not a correctness one, and the right answer depends on whether your intermediate commits carry information worth keeping.

**Negative test:** Squashing every merge by policy on a repository where commits are carefully staged — you lose the ability to bisect to a precise change, and reverting a single logical step becomes reverting a large combined commit.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Group/subgroup/project hierarchy described, with role inheritance and its over-permissioning risk.
- [ ] GitLab roles ordered, with Developer and Maintainer boundaries understood.
- [ ] Protected branches used to make review enforceable rather than conventional.
- [ ] Merge methods and squash compared by their effect on history.
