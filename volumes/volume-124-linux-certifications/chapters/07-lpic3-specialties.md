# Chapter 07: LPIC-3 — The Four Specialties

## Learning Objectives

- Map the four LPIC-3 specialty certifications: 300, 303, 305, 306.
- Understand each specialty's scope and its flagship technologies.
- Complete a walkthrough lab per specialty.

## The specialty tier

LPIC-3 is LPI's expert level: four independent certifications, each a single exam, each requiring an **active LPIC-2**. You choose by role — they are siblings, not a sequence.

| Certification | Exam | Scope |
|:---|:---|:---|
| LPIC-3 Mixed Environments | 300 | Samba/Active Directory integration: domains, winbind, FreeIPA |
| LPIC-3 Security | 303 | Cryptography, access control (SELinux/AppArmor), hardening, intrusion detection |
| LPIC-3 Virtualization and Containerization | 305 | KVM/QEMU/libvirt, Xen awareness, containers (LXC/Docker), orchestration awareness |
| LPIC-3 High Availability and Storage Clusters | 306 | Pacemaker/Corosync, load balancing, DRBD, cluster storage (GFS2/Ceph awareness) |

## Hands-On Lab

A Linux VM with nested-virt where noted. **Cost:** none.

### Lab 7.1 — Mixed environments: Samba as more than a share (300)

**Objective:** See the domain-side Samba the 300 exam tests.

```bash
sudo apt-get install -y -qq samba winbind 2>/dev/null
testparm -s 2>/dev/null | head -5
wbinfo --ping-dc 2>&1 | tail -1 || echo "no domain joined (expected in a standalone lab)"
cat <<'EOF'
exam 300 scope: Samba as AD domain controller or member; winbind identity mapping;
FreeIPA; NT ACLs vs POSIX; SMB protocol versions and signing
EOF
```

**Expected result:** Samba validated and `wbinfo` demonstrating the domain-facing tooling (cleanly reporting no domain in a standalone lab) — exam 300 is Samba at domain scale: DC/member roles, winbind UID mapping, and FreeIPA integration, not just file shares.

**Negative test:** Treating exam 300 as "advanced Chapter 6 file sharing" — the share is the smallest part; identity integration is the exam.

**Rollback:** `sudo apt-get remove -y samba winbind`.

### Lab 7.2 — Security: MAC and integrity (303)

**Objective:** Exercise mandatory access control and file integrity — 303's pillars.

```bash
sudo aa-status 2>/dev/null | head -3 || sestatus 2>/dev/null | head -3 || echo "install apparmor-utils or run on an SELinux distro"
sudo apt-get install -y -qq aide 2>/dev/null && sudo aideinit -y -f 2>/dev/null | tail -1 || echo "aide init (can take minutes) — the integrity baseline"
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
echo "303 scope: X.509/PKI, disk crypto (LUKS), SELinux/AppArmor, scanning (nmap awareness, defensively on your own systems), IDS (AIDE/auditd)"
```

**Expected result:** The MAC framework's status (AppArmor profiles or SELinux mode), an AIDE integrity baseline initialized, and a host key fingerprint read — 303's spread: cryptography (PKI, LUKS), mandatory access control, hardening, and integrity/intrusion detection, all defensive.

**Negative test:** MAC in permissive/complain mode treated as protection — it only logs; enforcing mode is the control, and the distinction is a certain exam item.

**Rollback:** `sudo apt-get remove -y aide`.

### Lab 7.3 — Virtualization: a real VM via libvirt (305)

**Objective:** Drive KVM/QEMU through libvirt, 305's core stack.

```bash
sudo apt-get install -y -qq qemu-kvm libvirt-daemon-system virtinst 2>/dev/null
virsh version 2>/dev/null | head -3
virsh net-list --all 2>/dev/null
qemu-img create -f qcow2 lab.qcow2 1G && qemu-img info lab.qcow2 | head -4
echo "305 scope: KVM/QEMU/libvirt (domains, networks, storage pools), Xen awareness, LXC, Docker, image formats"
```

**Expected result:** libvirt answering (`virsh version`), the default NAT network listed, and a qcow2 image created and inspected — 305's stack from hypervisor (KVM) through management (libvirt/virsh) to image formats (qcow2 features: snapshots, thin provisioning), plus the container side already drilled in [Volume XCII](../../volume-092-docker-certifications/README.md).

**Negative test:** `qemu-img info` on a raw image reports no snapshot support — format choice is capability choice; qcow2 vs raw trade-offs are exam material.

**Rollback:** `rm lab.qcow2`.

### Lab 7.4 — High availability: the cluster shape (306)

**Objective:** Model quorum and failover, 306's constant themes.

```bash
python3 - <<'EOF'
# Quorum: a 3-node cluster surviving one failure
nodes = {"n1": True, "n2": True, "n3": False}   # n3 down
votes = sum(nodes.values()); quorum = len(nodes)//2 + 1
print(f"votes={votes} quorum={quorum} ->", "cluster RUNS (has quorum)" if votes >= quorum else "cluster STOPS")
nodes["n2"] = False
votes = sum(nodes.values())
print(f"votes={votes} quorum={quorum} ->", "cluster RUNS" if votes >= quorum else "cluster STOPS (split-brain protection)")
EOF
echo "306 stack: Pacemaker (resources/constraints) + Corosync (membership/quorum), fencing/STONITH, DRBD replication, HAProxy/keepalived, GFS2/Ceph awareness"
```

**Expected result:** `votes=2 quorum=2 → RUNS`, then `votes=1 → STOPS` — quorum arithmetic, the reason clusters have odd node counts and stop rather than split-brain. Around it: Pacemaker resources and constraints, Corosync membership, fencing (STONITH), DRBD block replication, and load balancing — exam 306's estate.

**Negative test:** A two-node cluster without special quorum handling — one failure kills the majority; why two-node clusters need qdevice/fencing tweaks is a guaranteed exam topic.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] All four LPIC-3 specialties mapped and sampled.
- [ ] Samba-at-domain-scale, MAC/integrity, libvirt/qcow2, and quorum/failover drilled.
- [ ] A specialty chosen (or none — LPIC-2 is a complete stopping point).
