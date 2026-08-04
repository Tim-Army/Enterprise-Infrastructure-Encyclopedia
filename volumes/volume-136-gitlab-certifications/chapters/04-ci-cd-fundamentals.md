# Chapter 04: CI/CD Fundamentals

## Learning Objectives

- Write a `.gitlab-ci.yml` with stages, jobs, and scripts.
- Explain how runners pick up and execute jobs.
- Pass data between jobs with artifacts, and speed them up with cache.
- Use variables and their precedence correctly, including masked and protected values.

## What CI/CD is, in GitLab's terms

**Continuous Integration** merges and verifies changes automatically on every push. **Continuous Delivery/Deployment** carries verified changes onward to environments. In GitLab both live in one file at the repository root: **`.gitlab-ci.yml`**.

The object model is small, and the **Certified CI/CD Associate** exam is largely about knowing it precisely:

| Object | What it is |
|:---|:---|
| **Pipeline** | The whole run, triggered by a push, schedule, MR, or API |
| **Stage** | An ordered phase; stages run in sequence |
| **Job** | A unit of work inside a stage; jobs in the same stage run **in parallel** |
| **Runner** | The agent that executes a job |
| **Artifact** | Files a job produces, passed to later jobs and downloadable |
| **Cache** | Files reused between runs to save time (dependencies, not outputs) |

The rule that governs pipeline shape: **stages are sequential, jobs within a stage are parallel**, and a stage does not begin until every job in the previous stage has succeeded.

## Runners

A **runner** is the agent that runs jobs. Two things define one:

- **Scope** — *shared* (available across an instance), *group*, or *project*-specific.
- **Executor** — how it runs the job: `docker` (the common choice — each job in a fresh container), `shell` (directly on the host), `kubernetes`, `docker-machine` (autoscaling), and others.

Jobs and runners meet through **tags**: a job with `tags: [docker, linux]` will only run on a runner carrying those tags. A job whose tags match no runner does not fail — it **sits pending**, which is a distinctive and frequently misdiagnosed symptom.

## Artifacts versus cache

These are confused constantly, and the exams test the difference:

| | **Artifacts** | **Cache** |
|:---|:---|:---|
| Purpose | Pass **outputs** forward; make them downloadable | Reuse **dependencies** to save time |
| Guaranteed? | **Yes** — later jobs receive them | **No** — a cache miss is normal and must be survivable |
| Scope | Between jobs in a pipeline | Between pipelines, keyed |
| Example | Compiled binary, test report, scan result | `node_modules/`, `~/.m2`, pip wheels |

The rule of thumb: if the pipeline **breaks without it**, it is an artifact. If it merely runs **slower without it**, it is cache.

## Variables and precedence

Variables come from many places, and precedence decides which wins. From lowest to highest: instance → group → project → `.gitlab-ci.yml` (`variables:`) → job-level → trigger/manual-run variables.

Two protective flags:

- **Masked** — the value is redacted in job logs (it must meet format requirements to be maskable).
- **Protected** — the variable is exposed **only** to jobs running on protected branches or tags.

That second one is the security control that matters: production credentials marked protected simply do not exist in a pipeline running on someone's feature branch, so a malicious or careless `.gitlab-ci.yml` change on a branch cannot print them.

## Hands-On Lab

Python models pipeline execution. **Cost:** none.

### Lab 4.1 — Stages sequential, jobs parallel

**Objective:** Model execution order and total duration.

```bash
python3 - <<'EOF'
stages = ["build", "test", "deploy"]
jobs = [
  {"name":"compile",     "stage":"build",  "duration":120},
  {"name":"lint",        "stage":"build",  "duration":30},
  {"name":"unit-tests",  "stage":"test",   "duration":180},
  {"name":"integration", "stage":"test",   "duration":240},
  {"name":"sast",        "stage":"test",   "duration":90},
  {"name":"deploy-prod", "stage":"deploy", "duration":60},
]
total = 0
for stage in stages:
    in_stage = [j for j in jobs if j["stage"] == stage]
    slowest = max(j["duration"] for j in in_stage)
    total += slowest
    names = ", ".join(f"{j['name']}({j['duration']}s)" for j in in_stage)
    print(f"stage {stage:8} parallel: {names}")
    print(f"{'':14} stage takes {slowest}s — the SLOWEST job, not the sum\n")
serial = sum(j["duration"] for j in jobs)
print(f"pipeline duration: {total}s   (fully serial would be {serial}s)")
print(f"parallelism saves {serial-total}s. To speed this pipeline up, optimize 'integration' (240s)")
print("— the critical job in the slowest stage. Making 'sast' faster changes nothing.")
EOF
```

**Expected result:** 420 seconds against 720 if run serially, and the closing lines name the optimization target. This is the pipeline-tuning insight worth carrying: within a stage only the **slowest job** matters, so effort spent speeding up any other job in that stage is wasted. People routinely optimize the job that is easiest to optimize rather than the one on the critical path.

**Negative test:** Adding jobs to a stage assuming they are "free" because they run in parallel — they are free only while they finish faster than the current slowest job; the moment one overtakes it, it becomes the stage duration.

**Cleanup:** None.

### Lab 4.2 — Artifacts versus cache

**Objective:** Classify correctly, and see what breaks when you do not.

```bash
python3 - <<'EOF'
items = [
  {"path":"dist/app.bin",   "needed_by_later_job":True,  "can_rebuild":False},
  {"path":"node_modules/",  "needed_by_later_job":False, "can_rebuild":True},
  {"path":"coverage.xml",   "needed_by_later_job":True,  "can_rebuild":False},
  {"path":"~/.m2/",         "needed_by_later_job":False, "can_rebuild":True},
  {"path":"gl-sast-report.json","needed_by_later_job":True,"can_rebuild":False},
]
for i in items:
    kind = "ARTIFACT" if i["needed_by_later_job"] else "CACHE"
    why = ("later jobs REQUIRE it — guaranteed delivery"
           if kind == "ARTIFACT" else "just saves time — a miss is survivable")
    print(f"{i['path']:24} -> {kind:9} ({why})")

print("\n--- what happens if you get it wrong ---")
print("node_modules as an ARTIFACT : uploaded/downloaded every job, pipeline slows and storage bloats")
print("dist/app.bin as CACHE       : cache MISS is normal -> deploy job finds no binary -> PIPELINE FAILS")
print("\nRule: breaks without it = artifact. Merely slower without it = cache.")
EOF
```

**Expected result:** Build outputs and reports classify as artifacts, dependency directories as cache. The failure modes in the second half are asymmetric and that asymmetry is the point — misusing an artifact as cache produces an **intermittent** failure (only on cache miss), which is far harder to debug than the merely-slow failure of the reverse mistake.

**Negative test:** Caching build outputs to "speed up deploys" — it works until the first cache miss, at which point the deploy job fails with a missing file and the pipeline looks flaky rather than misconfigured.

**Cleanup:** None.

### Lab 4.3 — Variable precedence and protected values

**Objective:** Resolve a variable and check credential exposure.

```bash
python3 - <<'EOF'
LEVELS = ["instance", "group", "project", "yaml", "job", "manual"]
def resolve(defined):
    winner = None
    for lvl in LEVELS:                       # later levels override earlier
        if lvl in defined: winner = (lvl, defined[lvl])
    return winner

cases = [
  {"instance":"prod.example.com", "project":"stage.example.com"},
  {"group":"8080", "yaml":"3000", "job":"9000"},
  {"project":"v1", "manual":"v2-hotfix"},
]
for c in cases:
    lvl, val = resolve(c)
    print(f"defined at {list(c)} -> wins: {lvl} = '{val}'")

print("\n--- protected variables ---")
def exposed(var_protected, branch_protected):
    if var_protected and not branch_protected:
        return "NOT exposed — protected variable, unprotected branch (this is the security control)"
    return "exposed to the job"

for vp, bp, label in [(True, True,  "PROD_DEPLOY_KEY on main"),
                      (True, False, "PROD_DEPLOY_KEY on feature/xyz"),
                      (False, False,"BUILD_FLAG on feature/xyz")]:
    print(f"{label:34} -> {exposed(vp, bp)}")
print("\nMark production credentials PROTECTED: they then do not exist in pipelines on feature")
print("branches, so an edited .gitlab-ci.yml on a branch cannot echo them out.")
EOF
```

**Expected result:** Precedence resolves to the most specific level (manual run beats everything), and the protected-variable check shows the production key absent from a feature-branch pipeline. That absence is the control: without it, anyone able to push a branch can add `- echo $PROD_DEPLOY_KEY` to the CI file and read your production credential out of the job log.

**Negative test:** Storing production credentials as ordinary unprotected variables because "only our team can push" — every fork, branch, and merge-request pipeline can then read them, which is a much larger audience than intended.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] `.gitlab-ci.yml` object model learned: pipeline, stage, job, runner, artifact, cache.
- [ ] Stages-sequential / jobs-parallel modeled, with the slowest job identified as the tuning target.
- [ ] Runners, executors, and tag matching understood — including jobs that hang pending.
- [ ] Artifacts and cache classified by the breaks-without-it rule.
- [ ] Variable precedence resolved, and protected variables used to keep credentials off feature branches.
