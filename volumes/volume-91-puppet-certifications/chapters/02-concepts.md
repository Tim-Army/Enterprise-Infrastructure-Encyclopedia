# Chapter 02: Concepts

## Learning Objectives

- Explain resource abstraction (types and providers).
- Explain idempotence and desired-state convergence.
- Explain facts and Facter.
- Explain catalog compilation and the agent run lifecycle.
- Complete a walkthrough for each concepts topic.

## Theory and Architecture

The **Concepts** domain covers how Puppet works. **Resource abstraction** is central: you declare a
**resource** (a `package`, `file`, `service`, `user`, …) by its desired state, and Puppet's **type**
translates it through a platform-specific **provider** (apt vs yum, systemd vs init) — so the same
manifest works across OSes. **Idempotence** means applying the same catalog repeatedly converges to the
same state and makes no change once compliant. **Facts** are system data (OS, IP, memory) gathered by
**Facter** and available as variables in manifests, so code can adapt to each node. The **agent run
lifecycle**: the agent collects **facts** → sends them to the **primary server** → the server **compiles
a catalog** (the node's desired state, from manifests + Hiera + facts) → the agent **applies** the
catalog (making changes) → sends a **report** back. Understanding abstraction, idempotence, facts, and
the catalog lifecycle is the foundation the language and administration build on. This chapter teaches
the concepts with hands-on `puppet` walkthroughs.

## Design Considerations

Declare **desired state**, not steps — let the **provider** handle the platform. Rely on **idempotence**:
safe to run on a schedule (every 30 minutes by default), correcting **drift**. Use **facts** to make code
portable across nodes rather than hardcoding values. Understand where **catalog compilation** happens
(the server) versus **application** (the agent). Keep manifests deterministic.

## Implementation and Automation

The labs show resource abstraction across providers, confirm idempotence and drift correction, read
facts, and inspect a compiled catalog — the concepts the domain validates.

## Validation and Troubleshooting

Confirm the concepts:

```text
Resource abstraction: type (package/file/service) -> provider (apt/yum, systemd/init) -> cross-OS
Idempotence: apply repeatedly -> converge to desired state; no change once compliant -> corrects drift
Facts (Facter): system data as variables -> code adapts per node
Lifecycle: agent facts -> primary server compiles catalog -> agent applies -> report
```

Common pitfalls: writing **provider-specific** commands (`exec { 'apt-get install' }`) instead of the
`package` type; and assuming Puppet runs commands **imperatively** — it converges to declared state.

## Security and Best Practices

Idempotent desired state prevents configuration drift and enforces a known-good baseline — defensive
standardization. Prefer typed resources over `exec`. All work is authorized administration of your own
systems.

## Hands-On Lab

Concepts walkthroughs. **Shared prerequisites** — open-source Puppet 8, sudo, and `puppet apply`.
**Cost:** none.

### Lab 2.1 — See resource abstraction

**Objective:** One declaration, platform-specific provider.

```bash
puppet resource package rsync
```

```text
package { 'rsync':
  ensure   => '3.2.7-1',
  provider => 'apt',           # on Debian; 'yum'/'dnf' on RHEL
}
```

**Expected result:** the `package` type reporting the state via the platform's **provider** — the same
resource works across OSes.

**Negative test:** manage packages with `exec { 'apt-get install rsync': }`; it breaks on RHEL — use the
**`package`** type.

**Cleanup:** none (read-only).

### Lab 2.2 — Confirm idempotence and drift correction

**Objective:** Converge to desired state.

```bash
cat > /tmp/svc.pp <<'PP'
file { '/tmp/motd':
  ensure  => file,
  content => "Authorized use only\n",
}
PP
sudo puppet apply /tmp/svc.pp
echo "tampered" | sudo tee -a /tmp/motd >/dev/null   # simulate drift
sudo puppet apply /tmp/svc.pp                        # Puppet corrects it
cat /tmp/motd
```

```text
Notice: /File[/tmp/motd]/content: content changed  # drift corrected back to desired state
Authorized use only
```

**Expected result:** Puppet detects the tampered content and restores the declared state — drift
correction via idempotence.

**Negative test:** rely on a one-time provisioning script; drift is never corrected — Puppet re-applies
desired state.

**Cleanup:**

```bash
sudo rm -f /tmp/motd /tmp/svc.pp
```

### Lab 2.3 — Read facts

**Objective:** Use system data in code.

```bash
facter os.name os.release.major networking.ip
```

```text
os.name => Ubuntu
os.release.major => 24
networking.ip => 10.0.0.15
```

**Expected result:** structured facts about the node — the variables manifests use to adapt per system.

**Negative test:** hardcode the OS/IP in a manifest; use **facts** (`$facts['os']['family']`) so the code
is portable.

**Cleanup:** none (read-only).

### Lab 2.4 — Inspect a compiled catalog

**Objective:** See the desired state Puppet builds.

```bash
cat > /tmp/cat.pp <<'PP'
package { 'htop': ensure => installed }
PP
sudo puppet apply --noop /tmp/cat.pp --detailed-exitcodes; echo "exit=$?"
```

```text
Notice: /Package[htop]/ensure: current_value 'purged', should be 'present' (noop)
exit=2      # 2 = changes would be made (noop)
```

**Expected result:** in `--noop` mode, Puppet compiles the catalog and reports the change it *would* make
(exit 2) without applying — the desired state versus current state.

**Negative test:** apply untested code straight to production; use **`--noop`** to preview the catalog's
changes first.

**Cleanup:**

```bash
sudo rm -f /tmp/cat.pp
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Puppet's concepts are resource abstraction (types translated by platform providers), idempotence (repeated
application converging to desired state and correcting drift), facts gathered by Facter for portable code,
and the agent lifecycle where the primary server compiles a catalog from manifests, Hiera, and facts that
the agent applies and reports on.

- [ ] I can explain resource abstraction (types/providers).
- [ ] I can demonstrate idempotence and drift correction.
- [ ] I can read facts with Facter.
- [ ] I can inspect a compiled catalog with --noop.
- [ ] I completed Labs 2.1–2.4 including each negative test.
