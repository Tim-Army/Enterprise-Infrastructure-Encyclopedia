# Chapter 09: Open Technology Track, Choosing a Path, and Currency

## Learning Objectives

- Cover the LPI Open Technology track: DevOps Tools Engineer (701) and BSD Specialist (702).
- Choose and sequence certifications across both programs for your role.
- Keep certifications current: renewal windows, objective versions, and the LFCT lesson.

## The Open Technology track

Two single-exam LPI certifications outside the core Linux ladder (no prerequisites, 5-year validity):

| Certification | Exam | Scope |
|:---|:---|:---|
| **DevOps Tools Engineer** | 701 | Software engineering, container/machine deployment (Docker, Vagrant), config management (Ansible/Puppet/Chef awareness), CI/CD, monitoring/logging, IaC concepts |
| **BSD Specialist** | 702 | The BSD family (FreeBSD/OpenBSD/NetBSD): installation, users, network, storage, packages/ports — Unix skills applied off Linux |

DevOps Tools Engineer is vendor-neutral DevOps literacy (it complements the deep single-tool volumes: [Ansible LIX](../../volume-059-ansible/README.md), [Puppet XCI](../../volume-091-puppet-certifications/README.md), [Docker XCII](../../volume-092-docker-certifications/README.md)). BSD Specialist proves your Unix skills transfer beyond Linux.

## Hands-On Lab

### Lab 9.1 — DevOps Tools Engineer concepts (701)

**Objective:** Touch the four pillars 701 tests.

```bash
# Infrastructure as code (declarative desired state):
cat > compose.snippet <<'EOF'
services:
  web: { image: nginx, ports: ["8080:80"] }   # container deployment (Docker)
EOF
# Config management (idempotence — the DevOps core concept):
python3 - <<'EOF'
state = {"pkg_installed": False}
def ensure_installed(s):
    if not s["pkg_installed"]:
        s["pkg_installed"] = True; return "changed"
    return "ok (already installed)"
print(ensure_installed(state)); print(ensure_installed(state))
EOF
```

**Expected result:** A declarative service snippet and an idempotence demonstration (`changed` then `ok`) — 701's mental model: describe desired state, apply repeatedly, converge without re-doing work. CI/CD pipelines, monitoring, and container orchestration awareness complete the exam.

**Negative test:** A shell script that appends a line every run (not idempotent) vs the converging function above — non-idempotent automation is the anti-pattern 701 exists to correct.

**Rollback:** `rm compose.snippet`.

### Lab 9.2 — BSD Specialist orientation (702)

**Objective:** Note where BSD diverges from Linux, the heart of 702.

```bash
cat <<'EOF'
BSD vs Linux (exam 702 divergences):
  packages: pkg (binary) + ports tree (source)   vs apt/dnf
  init:     rc.d + /etc/rc.conf                    vs systemd
  firewall: pf (OpenBSD/FreeBSD)                   vs iptables/nftables
  storage:  ZFS first-class, UFS                   vs ext4/xfs + optional ZFS
  network:  ifconfig-centric, /etc/rc.conf         vs ip/NetworkManager
EOF
echo "same Unix concepts (users, permissions, shells, SSH) — different tooling and layout"
```

**Expected result:** The divergence table — 702 is your LPIC-1/2 Unix knowledge re-expressed in BSD's tooling (`pkg`/ports, `rc.conf`, `pf`, ZFS). The concepts transfer; the commands and file layout are the exam.

**Negative test:** Bringing `systemctl`/`apt` to a BSD exam — wrong OS family; recognizing the tooling swap is most of 702.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Your cross-program plan

**Objective:** Sequence both programs for your role.

```bash
cat > my-linux-cert-plan.md <<'EOF'
Background: new / junior admin / senior admin / devops / bsd
Program mix:
  entry:    Linux Essentials (010) or LFCA
  hands-on: LFCS (performance, 2yr)         <- do after LPIC-1 study as the practical capstone
  ladder:   LPIC-1 (101/102) -> LPIC-2 (201/202) -> LPIC-3 {300|303|305|306}
  breadth:  DevOps Tools Engineer (701) / BSD Specialist (702)
Renewal watch: LFCS 2yr ; LPIC 5yr (active-cert chaining!) ; Essentials lifetime
Verify objective versions before study: 101/102-500 v5.0 ; 201/202-450 v4.5
EOF
cat my-linux-cert-plan.md
```

**Expected result:** A plan that respects the two renewal cadences and the LPIC active-chaining rule (an expired LPIC-1 invalidates the LPIC-2/3 prerequisite) — the discipline both programs demand.

**Negative test:** Let LPIC-1 lapse while holding LPIC-2 — the ladder's prerequisite goes inactive; recertify the base to keep the chain valid.

**Rollback:** Keep the plan.

## Currency

- **Two renewal cadences.** LPI professional and Open Technology certifications are **5-year**; LFCS is **2-year**; LPI Essentials are **lifetime**. Track each.
- **Active-cert chaining (LPI).** LPIC-2 requires an active LPIC-1, LPIC-3 an active LPIC-2 — recertifying the base keeps the whole ladder valid.
- **Objective versions matter.** 101/102-500 are v5.0; 201/202-450 are v4.5. LPI revises objectives on its own cadence; study the current version, not a book's snapshot.
- **The LFCT lesson.** The Linux Foundation Certified Cloud Technician is **inactive** even though its LFS203 course still sells — verify a certification against the vendor's own status page before investing, not against course availability.

## Summary and Completion Checklist

- [ ] Open Technology track (701, 702) mapped.
- [ ] A cross-program path sequenced for your role.
- [ ] Renewal cadences, active-cert chaining, and objective-version discipline installed.
- [ ] The LFCT retirement understood as a currency lesson.
