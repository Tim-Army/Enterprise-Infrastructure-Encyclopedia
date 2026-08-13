# Chapter 09: Scaling, AWX, and Keeping Current

## Learning Objectives

- Tune execution strategy and performance.
- Explain AWX / Automation Platform for team-scale automation.
- Package dependencies as execution environments.
- Track ansible-core releases and the ecosystem.
- Complete a walkthrough for each scaling skill.

## Theory and Architecture

At team and fleet scale, Ansible adds control and performance. **Strategies** (`linear`
default, `free`, `host_pinned`) and **`forks`** control parallelism across hosts.
**AWX** (the open-source upstream of **Red Hat Ansible Automation Platform**) provides a
web UI/API, RBAC, job scheduling, credential management, and audit — turning ad-hoc runs
into governed automation. **Execution environments** are container images bundling
ansible-core plus the exact collections/Python deps, so runs are reproducible everywhere
(built with `ansible-builder`). The engine ships regular **ansible-core** releases
(current **2.21.x**) alongside the community `ansible` package; track both.

## Design Considerations

Raise **`forks`** and pick a **strategy** for throughput. Use **AWX/AAP** for RBAC,
scheduling, credentials, and audit rather than laptops. Package deps as **execution
environments** for reproducibility. Stay on **supported ansible-core** versions.

## Implementation and Automation

The labs tune forks/strategy, describe AWX and execution environments, and check the
version.

## Validation and Troubleshooting

Confirm the model:

```text
Parallelism: forks (ansible.cfg) + strategy (linear/free/host_pinned).
AWX/AAP: UI/API + RBAC + scheduling + credentials + audit. Execution environments (ansible-builder).
Releases: ansible-core 2.21.x + community 'ansible' package.
```

Common pitfalls: default `forks=5` throttling large fleets; and "works on my laptop" deps
(fixed by execution environments).

## Security and Best Practices

Tune **forks/strategy** for scale, run governed automation in **AWX/AAP** (RBAC, audit,
credential vaulting), reproduce deps with **execution environments**, and stay on
**supported** ansible-core. Track releases and deprecations.

## Hands-On Lab

Scaling walkthroughs. **Shared prerequisites** — ansible-core. **Cost:** none.

### Lab 9.1 — Tune parallelism

**Objective:** Raise forks for throughput.

```bash
cat > ansible.cfg <<'CFG'
[defaults]
forks = 50
CFG
ansible-config dump --only-changed | grep -i forks
```

**Expected result:** **`DEFAULT_FORKS = 50`** — higher parallelism across hosts.

**Negative test:** run a 500-host play at the default **forks=5**; raise forks to parallelize
appropriately.

**Rollback:** `rm -f ansible.cfg`.

### Lab 9.2 — Choose a strategy (describe)

**Objective:** Match strategy to the workload.

```text
# linear (default): all hosts complete a task before the next.
# free: each host runs as fast as it can (no lockstep).
# host_pinned: batch hosts to a worker.
"strategy: free for long, independent per-host work; linear for ordered rollouts"
```

**Expected result:** the strategy trade-offs — throughput vs ordering.

**Negative test:** use `linear` for long independent per-host jobs; **`free`** avoids the
slowest-host bottleneck.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Execution environments (describe)

**Objective:** Reproduce dependencies as an image.

```text
# ansible-builder: define ansible-core + collections + Python deps -> build a container image
#   (an execution environment) used by AWX/CLI so every run is identical.
"execution environment: pinned ansible-core + collections in one image"
```

**Expected result:** a reproducible **execution environment** image — no dependency drift.

**Negative test:** rely on each machine's local collections; **execution environments** pin
them for identical runs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.4 — Check the version

**Objective:** Confirm a supported ansible-core.

```bash
ansible --version | head -1
python -c "print('track ansible-core releases + the community ansible package')"
```

**Expected result:** an **ansible-core 2.21.x** line — a current, supported engine.

**Negative test:** run an end-of-life ansible-core; track **releases** and stay supported
for fixes/modules.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Ansible scales with forks/strategies for parallelism, AWX/Automation Platform for governed
team automation (RBAC, scheduling, audit), and execution environments for reproducible
dependencies — on supported ansible-core releases. This chapter tuned parallelism and
reviewed the scaling model.

- [ ] I can tune forks and choose a strategy.
- [ ] I can explain AWX/AAP's value.
- [ ] I can describe execution environments.
- [ ] I can confirm a supported ansible-core version.
- [ ] I completed Labs 9.1–9.4 including each negative test.
