# Chapter 08: Runners, Scaling, and Administration

## Learning Objectives

- Choose a runner executor and scope for a given workload.
- Size runner capacity against pipeline demand and queue time.
- Design cache strategy that actually hits.
- Compare GitLab.com, self-managed, and GitLab Dedicated deployment models.

## Runner architecture

A **GitLab Runner** is an agent that polls GitLab for jobs, runs them, and reports back. Two decisions define it.

**Scope** — who can use it:

| Scope | Available to | Fits |
|:---|:---|:---|
| **Shared** | All projects on the instance | General-purpose capacity |
| **Group** | Projects in one group | Team-specific tooling or hardware |
| **Project** | One project | Special requirements, isolated environments |

**Executor** — how the job runs:

| Executor | Isolation | Notes |
|:---|:---|:---|
| **Docker** | Fresh container per job | The usual choice; clean environment every run |
| **Shell** | None — runs on the host | Simple, but jobs share and can pollute state |
| **Kubernetes** | Pod per job | Scales with the cluster; the common cloud-native answer |
| **Docker Machine** | VM per job | Autoscaling on cloud VMs |
| **Custom / SSH** | Varies | Specialized targets |

The `shell` executor deserves a warning: jobs run directly on the host with the runner's privileges and leave state behind. It is convenient for a quick self-managed setup and it means an untrusted merge request's CI file executes commands on your machine.

## Concurrency and queueing

Two settings govern throughput: **`concurrent`** (total jobs a runner process runs at once, globally) and **`limit`** per runner. When demand exceeds capacity, jobs **queue** — and queue time, not job duration, is usually what developers experience as "CI is slow."

The sizing question is therefore not "how fast is a job?" but "how long does a job wait before starting at peak?"

## Cache strategy

A cache that never hits is pure overhead — you pay upload and download cost for nothing. Hit rate is governed by the **cache key**:

| Key strategy | Behavior |
|:---|:---|
| Static key (`key: build-cache`) | Everything shares one cache; frequent invalidation, cross-contamination |
| **`key: files: [package-lock.json]`** | Cache changes only when dependencies change — usually correct |
| `key: $CI_COMMIT_REF_SLUG` | Per-branch cache; good isolation, poor reuse for new branches |

`policy: pull` on jobs that only consume the cache avoids needless re-uploads, and `untracked`/`paths` should be scoped tightly — caching an entire workspace is a common way to make pipelines slower than no cache at all.

## Deployment models

| Model | You operate | Fits |
|:---|:---|:---|
| **GitLab.com (SaaS)** | Nothing; optionally your own runners | Most teams; fastest start |
| **Self-managed** | The whole instance: upgrades, backups, scaling, availability | Data residency, air-gapped, deep customization |
| **GitLab Dedicated** | Nothing; single-tenant SaaS | Isolation and compliance without operating it |

A frequent hybrid: GitLab.com for the platform with **self-hosted runners** — you keep source and pipelines on SaaS while jobs execute inside your network, which is how teams reach internal systems without exposing them.

## Hands-On Lab

Python models runner operations. **Cost:** none.

### Lab 8.1 — Choose the executor

**Objective:** Match executor to requirement, and see where `shell` is dangerous.

```bash
python3 - <<'EOF'
def choose(untrusted_contributors, needs_clean_env, has_k8s, needs_gpu_host):
    if needs_gpu_host and not has_k8s:
        return "shell or custom on dedicated hardware", "specialized hardware access; ISOLATE the runner"
    if has_k8s:
        return "kubernetes", "pod per job — clean isolation and cluster autoscaling"
    if untrusted_contributors or needs_clean_env:
        return "docker", "fresh container per job — required when CI config comes from contributors"
    return "shell", "simplest, but jobs share host state"

cases = [
  ("public repo, outside MRs", True,  True,  False, False),
  ("internal repo on k8s",     False, True,  True,  False),
  ("ML training on GPU box",   False, False, False, True),
  ("tiny internal tool",       False, False, False, False),
]
for label, *args in cases:
    ex, why = choose(*args)
    print(f"{label:26} -> {ex:38} ({why})")

print("\nWARNING on `shell`: the job runs on the HOST with the runner's privileges and leaves")
print("state behind. A merge request from an outside contributor edits .gitlab-ci.yml —")
print("so an untrusted CI file would execute arbitrary commands on your machine.")
EOF
```

**Expected result:** Public repositories and clean-environment needs route to `docker`, Kubernetes clusters to `kubernetes`, specialized hardware to an isolated `shell`/custom runner, and only a trivial internal case to plain `shell`. The warning is the security lesson: **the CI file is code from whoever opened the merge request**, so executor choice is an isolation decision, not a convenience one.

**Negative test:** Using a `shell` runner on a public repository — an outside contributor's merge request can run arbitrary commands on the runner host with its privileges.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Size runners against queue time

**Objective:** Size for peak wait, not average utilization.

```bash
python3 - <<'EOF'
def simulate(runners, concurrent_per_runner, jobs_at_peak, avg_job_min):
    capacity = runners * concurrent_per_runner
    waves = -(-jobs_at_peak // capacity)          # ceiling
    worst_wait = (waves - 1) * avg_job_min
    util = min(jobs_at_peak / capacity, 1.0) * 100
    verdict = ("healthy" if worst_wait <= 2 else
               "tolerable" if worst_wait <= 10 else
               "DEVELOPERS WILL CALL CI 'SLOW'")
    print(f"{runners} runner(s) x {concurrent_per_runner} concurrent = {capacity} slots | "
          f"{jobs_at_peak} jobs at peak")
    print(f"   {waves} wave(s), worst wait {worst_wait} min, utilization {util:.0f}% -> {verdict}\n")

simulate(1, 4, 40, 5)
simulate(3, 4, 40, 5)
simulate(5, 8, 40, 5)
print("Note the trap: the 1-runner case shows 100% UTILIZATION, which looks efficient on a")
print("dashboard while developers wait 45 minutes. Size on QUEUE TIME, not utilization.")
EOF
```

**Expected result:** One runner gives 100% utilization and a 45-minute worst-case wait; five runners with eight slots clear the peak in one wave. The closing observation is the operational insight — **high utilization and good service are opposites here**. A capacity dashboard showing runners fully busy is showing you a queue, and the metric that matches developer experience is time-to-start.

**Negative test:** Sizing runners to keep utilization near 100% for cost efficiency — you have deliberately built a permanent queue, and the cost you saved reappears as engineering time spent waiting.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Cache keys and hit rate

**Objective:** Compare key strategies by hit rate and net benefit.

```bash
python3 - <<'EOF'
# 20 pipelines; deps changed on 2 of them; work spread across 4 branches
PIPELINES, DEPS_CHANGED, BRANCHES = 20, 2, 4
RESTORE_SAVES_MIN, CACHE_OVERHEAD_MIN = 4.0, 0.5

def evaluate(name, hits):
    misses = PIPELINES - hits
    saved = hits * RESTORE_SAVES_MIN
    overhead = PIPELINES * CACHE_OVERHEAD_MIN
    net = saved - overhead
    print(f"{name:34} hits {hits:>2}/{PIPELINES} ({hits/PIPELINES*100:3.0f}%)  "
          f"net {net:+.1f} min  {'WORTH IT' if net > 0 else 'COSTS MORE THAN IT SAVES'}")

evaluate("key: files: [package-lock.json]", PIPELINES - DEPS_CHANGED)     # invalidates only on dep change
evaluate("key: $CI_COMMIT_REF_SLUG",        PIPELINES - BRANCHES)         # cold on each new branch
evaluate("key: $CI_COMMIT_SHA",             0)                            # unique per commit: never hits
evaluate("static key: build-cache",          PIPELINES - DEPS_CHANGED - 3) # contention/contamination
print("\n`key: $CI_COMMIT_SHA` is unique per commit, so the cache NEVER hits — you pay upload")
print("and download every pipeline for zero benefit. Key on the DEPENDENCY MANIFEST.")
EOF
```

**Expected result:** Keying on the lock file yields an 90% hit rate and a clear net saving; keying on commit SHA hits **zero** times while still paying overhead on every pipeline. That last configuration appears in real repositories surprisingly often, because it looks like a sensible cache key until you notice the key changes on every single commit by definition.

**Negative test:** Adding cache to every job without measuring hit rate — the pipeline gets slower, and because the cache "is configured" nobody suspects it as the cause.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Runner scope and executor chosen deliberately, with `shell` recognized as an isolation risk.
- [ ] Capacity sized on peak queue time rather than utilization.
- [ ] Cache keyed on the dependency manifest, with hit rate treated as the measure of value.
- [ ] GitLab.com, self-managed, and Dedicated compared, including the SaaS-plus-self-hosted-runners hybrid.
