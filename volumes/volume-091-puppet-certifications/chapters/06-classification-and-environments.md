# Chapter 06: Classification and Environments

## Learning Objectives

- Explain node classification strategies.
- Assign classes and parameters to nodes.
- Explain directory environments.
- Reason about code deployment (r10k / Code Manager).
- Complete a walkthrough for each classification-and-environments topic.

## Theory and Architecture

**Classification** decides *which* configuration a node gets, and **Environments** decides *which version*
of the code. **Classification** assigns **classes** (and parameters) to nodes. Strategies include the
**`site.pp`** manifest with `node` statements, an **External Node Classifier (ENC)**, the Puppet
Enterprise **console** (point-and-click node groups), and — the common modern approach — **Hiera-based
classification** using the roles-and-profiles pattern (each node gets one **role** via Hiera). **Directory
environments** are separate directories under `environments/` (e.g., `production`, `development`), each
with its own **modules** and **manifests** and its own **`environment.conf`**; an agent runs against a
named environment, so you can test code in `development` before promoting to `production`. Code reaches
those environment directories through **code deployment** — **r10k** or **Code Manager** — which reads a
**control repo** (a Git repo with a `Puppetfile` listing module versions and a branch **per environment**)
and deploys each Git branch as an environment. This chapter teaches classification and environments with
hands-on walkthroughs.

## Design Considerations

Prefer **Hiera/roles-and-profiles** classification (one role per node) over sprawling `site.pp` `node`
blocks. Use **directory environments** to test in `development`/feature branches before **production**.
Manage code with a **control repo** + **Puppetfile** deployed by **r10k/Code Manager** (a Git branch per
environment). Pin module versions in the **Puppetfile**. Promote code by merging branches, not editing
production directly.

## Implementation and Automation

The labs classify a node with a role, reason about directory environments, and model a control-repo
deployment — the classification and environments the domain validates.

## Validation and Troubleshooting

Confirm classification and environments:

```text
Classification: assign classes/params via site.pp node{} | ENC | PE console | Hiera (one role per node)
Directory environments: environments/<name>/ (modules + manifests + environment.conf); agent picks one
Code deployment: r10k / Code Manager reads a control repo (Puppetfile + branch-per-environment) -> deploys
Promote: dev/feature branch -> test -> merge to production branch
```

Common pitfalls: editing code directly in the **production** environment (no testing) — use branches and
r10k; and huge `site.pp` `node` blocks instead of **role**-based classification.

## Security and Best Practices

Test in a non-production **environment** first, deploy via a reviewed **control repo** (change control),
and pin module versions. Environments and code deployment give safe, auditable change. All work is
authorized administration.

## Hands-On Lab

Classification-and-environments walkthroughs. **Shared prerequisites** — open-source Puppet 8 and
`python3`. **Cost:** none.

### Lab 6.1 — Classify a node with a role (Hiera)

**Objective:** Assign one role per node.

```yaml
# data/nodes/web1.yaml  (Hiera-based classification)
classes:
  - role::webserver
```

```python
python3 - <<'PY'
classification = {"web1": ["role::webserver"], "db1": ["role::database"]}
for node, roles in classification.items():
    assert len(roles) == 1, "one role per node"
    print(f"{node}: {roles[0]}")
print("Hiera assigns exactly one role per node -> role composes profiles")
PY
```

**Expected result:** each node classified with exactly one **role** via Hiera — the modern strategy.

**Negative test:** classify `web1` with three roles; a node gets **one** role that composes profiles.

**Cleanup:** none.

### Lab 6.2 — Reason about directory environments

**Objective:** Separate code versions.

```python
python3 - <<'PY'
envs = {
  "production":  "stable code; live agents run here",
  "development": "test changes safely before promotion",
  "feature-x":   "a feature branch deployed as its own environment",
}
for env, use in envs.items(): print(f"{env:12}: {use}")
print("An agent runs against ONE named environment (puppet agent --environment development)")
PY
```

**Expected result:** environments as isolated code versions — test in development, run in production.

**Negative test:** develop directly in `production`; use a **development**/feature environment first.

**Cleanup:** none.

### Lab 6.3 — Model a control-repo deployment

**Objective:** Deploy code with r10k/Code Manager.

```python
python3 - <<'PY'
# control repo: a Puppetfile + a Git branch per environment
puppetfile = {
  "puppetlabs-ntp": "10.1.0",
  "puppetlabs-stdlib": "9.6.0",
}
branches = ["production", "development", "feature-x"]
print("Puppetfile (pinned module versions):")
for m, v in puppetfile.items(): print(f"  mod '{m}', '{v}'")
print("r10k/Code Manager deploys each Git branch ->", branches)
PY
```

**Expected result:** a Puppetfile pinning modules and a branch-per-environment deployed by r10k/Code
Manager — auditable code delivery.

**Negative test:** copy modules onto the server by hand; use a **control repo + r10k** so deployment is
versioned and reviewed.

**Cleanup:** none.

### Lab 6.4 — Promote code between environments

**Objective:** Move a change safely to production.

```python
python3 - <<'PY'
flow = [
  "1. Commit change on 'feature-x' branch -> r10k deploys 'feature-x' environment",
  "2. Test agents against --environment feature-x (--noop first)",
  "3. Open PR: feature-x -> development -> production",
  "4. Merge to production branch -> r10k deploys production",
]
for step in flow: print(step)
PY
```

**Expected result:** a branch-based promotion path from feature to production — reviewed, tested change.

**Negative test:** merge straight to production without testing; promote through **environments** with
review.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Classification assigns classes and parameters to nodes — best done with Hiera and one role per node —
while directory environments hold separate versions of the code (development, production), and r10k or
Code Manager deploys a control repo (a Puppetfile plus a Git branch per environment) so changes are
tested in a non-production environment and promoted by merge.

- [ ] I can classify a node with a role.
- [ ] I can reason about directory environments.
- [ ] I can model a control-repo deployment.
- [ ] I can promote code between environments.
- [ ] I completed Labs 6.1–6.4 including each negative test.
