# Chapter 05: Advanced CI/CD — Rules, DAGs, and Environments

## Learning Objectives

- Control job execution with `rules`, and understand why `rules` replaced `only/except`.
- Build directed-acyclic-graph pipelines with `needs` to break stage ordering.
- Split large pipelines with parent-child and multi-project triggers.
- Model environments, deployments, and manual approval gates.

## `rules`: deciding whether a job runs

`rules` is evaluated top to bottom, and **the first match wins** — later rules are not considered. Each rule can carry `if`, `changes`, `exists`, plus `when` and `allow_failure`.

```yaml
deploy-prod:
  script: ./deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: never
    - when: on_success
```

The legacy `only/except` keywords still work but are no longer recommended: `rules` is strictly more expressive, and mixing the two in one job is invalid. If you meet `only/except` in an existing repository, treat it as material to migrate.

`when: never` is the important escape hatch — it is how you *exclude* rather than include, and forgetting that first-match-wins means a broad early rule can shadow a specific later one.

## `needs` and the DAG

By default a job waits for its entire preceding stage. **`needs`** overrides that, letting a job start the moment its named dependencies finish — turning the pipeline from a sequence of stages into a **directed acyclic graph**.

The benefit is real: a fast unit-test job need not wait for a slow integration-test job in the same stage before its downstream deploy begins. The constraints are that `needs` cannot create a cycle, and that a job may only need jobs that run earlier in the graph.

## Parent-child and multi-project pipelines

| Pattern | Mechanism | Fits |
|:---|:---|:---|
| **Parent-child** | `trigger: include:` a separate YAML file | Monorepos — run only the sub-pipeline for the component that changed |
| **Multi-project** | `trigger: project:` another project | Cross-repository orchestration and downstream deployments |
| **`include:`** | Pull YAML from a file, template, or remote | Sharing configuration across many projects |

Parent-child pipelines exist mainly to keep monorepo pipelines comprehensible and fast: combined with `rules: changes:`, only the affected component's child pipeline runs.

## Environments and deployments

An **environment** is a named deployment target (`staging`, `production`) that GitLab tracks, giving you deployment history, the currently deployed commit, rollback, and — with **protected environments** — control over who may deploy there.

Common deployment gates:

- **`when: manual`** — a human presses the button.
- **Protected environments** — only specified roles can run the deployment job.
- **`environment: on_stop`** — a paired teardown job, essential for review apps.
- **Review apps** — an ephemeral environment per merge request, torn down on merge or close.

## Hands-On Lab

Python models advanced pipeline behavior. **Cost:** none.

### Lab 5.1 — First-match-wins rule evaluation

**Objective:** Evaluate `rules` the way GitLab does, and see rule shadowing.

```bash
python3 - <<'EOF'
def evaluate(rules, ctx):
    for i, r in enumerate(rules):
        cond = r.get("if")
        matched = True if cond is None else eval(cond, {}, ctx)
        if matched:
            return r.get("when", "on_success"), f"rule[{i}] matched ({cond or 'catch-all'})"
    return "never", "no rule matched — job does not run"

rules_good = [
  {"if": "branch == 'main'", "when": "manual"},
  {"if": "source == 'merge_request_event'", "when": "never"},
  {"when": "on_success"},
]
rules_shadowed = [
  {"when": "on_success"},                       # catch-all FIRST — shadows everything below
  {"if": "branch == 'main'", "when": "manual"},
]
for name, rules in (("correct", rules_good), ("shadowed", rules_shadowed)):
    print(f"\n=== {name} ===")
    for ctx in ({"branch":"main","source":"push"},
                {"branch":"feature/x","source":"merge_request_event"},
                {"branch":"feature/x","source":"push"}):
        when, why = evaluate(rules, ctx)
        print(f"  {ctx} -> when={when:10} [{why}]")
print("\nIn 'shadowed', the catch-all is FIRST so it always wins — the main-branch manual gate")
print("never applies, and production deploys run automatically. Order is not cosmetic.")
EOF
```

**Expected result:** The correct rule set gates `main` behind a manual step and skips merge-request pipelines; the shadowed set matches its catch-all every time, silently removing the manual production gate. This is a real and dangerous misconfiguration — the pipeline still works, so nothing looks broken, while the approval gate has quietly ceased to exist.

**Negative test:** Appending a new rule to the bottom of an existing list that already ends in a catch-all — the new rule is unreachable, and its author will swear it should be matching.

**Cleanup:** None.

### Lab 5.2 — DAG scheduling with `needs`

**Objective:** Compare stage-ordered and `needs`-driven execution.

```bash
python3 - <<'EOF'
jobs = {
  "build-api":  {"stage":"build","duration":60, "needs":[]},
  "build-web":  {"stage":"build","duration":90, "needs":[]},
  "test-api":   {"stage":"test", "duration":120,"needs":["build-api"]},
  "test-web":   {"stage":"test", "duration":45, "needs":["build-web"]},
  "deploy-web": {"stage":"deploy","duration":30,"needs":["test-web"]},
  "deploy-api": {"stage":"deploy","duration":30,"needs":["test-api"]},
}
stages = ["build","test","deploy"]

stage_total = sum(max(j["duration"] for j in jobs.values() if j["stage"]==s) for s in stages)

finish = {}
def finish_time(name):
    if name in finish: return finish[name]
    deps = jobs[name]["needs"]
    start = max((finish_time(d) for d in deps), default=0)
    finish[name] = start + jobs[name]["duration"]
    return finish[name]
dag_total = max(finish_time(n) for n in jobs)

print("stage-ordered (default):")
for s in stages:
    print(f"   {s:7} = {max(j['duration'] for j in jobs.values() if j['stage']==s)}s (slowest job)")
print(f"   TOTAL {stage_total}s\n")
print("with needs: (DAG):")
for n in sorted(jobs, key=lambda x: finish[x]):
    print(f"   {n:11} finishes at {finish[n]:>3}s")
print(f"   TOTAL {dag_total}s")
print(f"\nDAG saves {stage_total-dag_total}s: deploy-web starts as soon as test-web is done,")
print("instead of waiting for the slow test-api to finish its stage.")
EOF
```

**Expected result:** 240 seconds stage-ordered versus 210 with `needs` — `deploy-web` no longer waits on the unrelated `test-api`. The saving grows with pipeline size and asymmetry: the more independent the branches of your build, the more stage ordering costs you for nothing.

**Negative test:** Adding `needs` everywhere without thinking — you can accidentally drop a real dependency, and a deploy job starts before the artifact it requires has been produced.

**Cleanup:** None.

### Lab 5.3 — Environments, protection, and manual gates

**Objective:** Model who can deploy where.

```bash
python3 - <<'EOF'
environments = {
  "review/*":   {"protected":False,"allowed":[],                 "when":"on_success","auto_stop":True},
  "staging":    {"protected":False,"allowed":[],                 "when":"on_success","auto_stop":False},
  "production": {"protected":True, "allowed":["Maintainer","Owner"],"when":"manual",  "auto_stop":False},
}
def deploy(env, role, branch_protected):
    e = environments[env]
    if e["protected"]:
        if role not in e["allowed"]:
            return f"DENIED — '{env}' is protected; requires {e['allowed']}"
        if not branch_protected:
            return f"DENIED — protected environment deploys come from protected branches"
    if e["when"] == "manual":
        return f"ALLOWED — but requires a MANUAL action by {role} (human gate)"
    return "ALLOWED — automatic on success"

for env, role, bp in [("review/*","Developer",False), ("staging","Developer",False),
                      ("production","Developer",True), ("production","Maintainer",True)]:
    print(f"{role:11} -> {env:11} : {deploy(env, role, bp)}")
print("\nreview/* auto-stops when the MR closes — without on_stop, ephemeral environments")
print("accumulate forever and quietly consume infrastructure nobody remembers provisioning.")
EOF
```

**Expected result:** Developers deploy freely to review apps and staging, are denied production, and even a Maintainer's production deploy requires a manual action. The layering is the design: protection decides *who*, the manual gate decides *when*, and `auto_stop` handles cleanup. The closing note names a real cost — review apps without teardown are among the commonest sources of mystery cloud spend.

**Negative test:** Protecting the production *environment* but leaving production credentials as unprotected variables (Chapter 04) — the deployment job is gated while the credential remains readable from any branch pipeline.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] `rules` evaluated first-match-wins, with shadowing recognized as a silent gate failure.
- [ ] `only/except` identified as legacy, not to be mixed with `rules`.
- [ ] `needs` used to build a DAG and shorten the pipeline's critical path.
- [ ] Parent-child and multi-project pipelines matched to monorepo and cross-repo cases.
- [ ] Environments protected, manual gates applied, and review apps auto-stopped.
