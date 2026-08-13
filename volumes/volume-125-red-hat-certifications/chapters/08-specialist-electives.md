# Chapter 08: Specialist Electives (Level 4)

## Learning Objectives

- Map the Level-4 Specialist electives across the tracks — the RHCA building blocks.
- Understand what the flagship specialists test: security, identity, clustering, automation, and virtualization.
- Drill representative specialist concepts.

## The Specialist tier

Level-4 **Specialist** exams (Red Hat Certified Specialist, RHCS) have **no prerequisites** and each validates one high-value area. Three same-track Specialists (plus the track's Administrator and Engineer exams) assemble an **RHCA**. Representative electives, verified on redhat.com, 3 August 2026:

| Exam | Specialist in… | Track affinity |
|:---|:---|:---|
| EX415 | Security: Securing Red Hat Enterprise Linux | Enterprise Linux |
| EX362 | Identity Management (IdM/FreeIPA) | Enterprise Linux |
| EX436 | High Availability Clustering (Pacemaker) | Enterprise Linux |
| EX442 | Linux Performance Tuning | Enterprise Linux |
| EX210 | Cloud Infrastructure (OpenStack) | Cloud |
| EX358 | Services Management and Automation | Ansible/Enterprise Linux |
| EX480 | MultiCluster Management (ACM + ACS) | OpenShift |
| EX316 | OpenShift Virtualization | OpenShift |
| EX188/EX288 | Containers / Cloud-Native Developer | Cloud-Native |

(**EX318**, the old RHV virtualization specialist, is **retired** — use EX316.)

## Hands-On Lab

RHEL-family + container tooling. Each lab samples one specialist's core. **Cost:** none.

### Lab 8.1 — Security specialist (EX415)

**Objective:** Apply a hardening control the EX415 tests: SCAP compliance scanning.

```bash
sudo dnf install -y openscap-scanner scap-security-guide >/dev/null 2>&1
ls /usr/share/xml/scap/ssg/content/ 2>/dev/null | head -3 || echo "SCAP content ships with scap-security-guide"
sudo oscap xccdf eval --profile cis_server_l1 --report /tmp/report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel*-ds.xml 2>/dev/null | grep -E "Title|Result" | head -6 || echo "run against your RHEL datastream"
```

**Expected result:** OpenSCAP evaluating the system against a CIS profile and producing a report — EX415 covers SCAP compliance, auditd, AIDE, USBGuard, and SELinux hardening; automated compliance scanning is its signature skill.

**Negative test:** Claiming "compliant" from a passing scan of the wrong profile — profile selection (CIS L1 vs L2 vs STIG) determines what "compliant" means; the exam tests choosing correctly.

**Rollback:** `rm -f /tmp/report.html`.

### Lab 8.2 — Identity Management specialist (EX362)

**Objective:** State the IdM/FreeIPA architecture EX362 tests.

```text
IdM (FreeIPA) = 389 Directory Server (LDAP) + MIT Kerberos (SSO) + Dogtag (PKI/certs) + BIND (DNS) + SSSD (clients)
  server: ipa-server-install ; client: ipa-client-install (joins the domain, configures SSSD)
  manages: users, hosts, services, HBAC (host-based access control), sudo rules, RBAC — centrally
```

**Expected result:** IdM as the integrated identity stack (LDAP + Kerberos + PKI + DNS) with SSSD on clients — EX362 tests deploying the server, enrolling clients, and centrally managing users/hosts/HBAC/sudo. It is the Red Hat answer to Active Directory (and integrates with it via trusts).

**Negative test:** Managing users in local `/etc/passwd` on each host instead of IdM — defeats central identity; EX362 is precisely about eliminating that sprawl.

**Rollback:** None (design).

### Lab 8.3 — High Availability Clustering specialist (EX436)

**Objective:** Model the Pacemaker resource/constraint concepts EX436 tests.

```bash
python3 - <<'EOF'
# Pacemaker: a resource with a location constraint and colocation
cluster = {"nodes": ["n1","n2"], "resources": {}}
def add_resource(c, name, prefers):
    c["resources"][name] = {"prefers": prefers}
    return f"{name} started on {prefers} (location constraint)"
print(add_resource(cluster, "VirtualIP", "n1"))
print("colocation: WebServer runs wherever VirtualIP runs (grouped resources move together)")
print("fencing (STONITH) required so a failed node can't corrupt shared storage")
EOF
```

**Expected result:** A resource with a location preference and a colocation rule described — EX436 tests Pacemaker/Corosync clusters: resources, constraints (location/colocation/order), resource groups, fencing (STONITH), and shared storage (GFS2). Fencing is mandatory, not optional.

**Negative test:** A cluster without fencing — a partitioned node can corrupt shared storage; EX436 fails designs that skip STONITH.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Services Management and Automation (EX358)

**Objective:** Note what EX358 automates beyond core Ansible.

```text
EX358 scope: automate provisioning of network services with Ansible —
  configure/verify with modules for firewalld, storage, web (nginx/haproxy), DNS,
  database, NFS/Samba, and containers — the "automate the RHCSA services" exam
```

**Expected result:** EX358 as the bridge between RHCE Ansible ([Chapter 05](05-ansible-track-ex294.md)) and real service configuration — automating firewalld, storage, load balancing, DNS, databases, and file sharing via modules and System Roles.

**Negative test:** Hand-configuring each service (RHCSA-style) on an EX358 task — the exam wants the *automated*, idempotent, repeatable approach.

**Rollback:** None (design).

### Lab 8.5 — Choosing three for an RHCA

**Objective:** Assemble a valid RHCA elective set.

```text
Enterprise Linux RHCA example: RHCSA (EX200) + EX342 + { EX415 security, EX362 IdM, EX436 HA }
OpenShift RHCA example:        EX280 + EX380 + { EX480 multicluster, EX316 virt, EX288 dev }
Rule (2026): all three Specialists must be within the SAME track as the Admin+Engineer exams
```

**Expected result:** Two valid RHCA assemblies, each keeping all electives in-track — the 2026 rule this volume returns to. [Chapter 09](09-choosing-currency-and-career.md) turns this into a personal plan.

**Negative test:** An RHCA mixing EX415 (Enterprise Linux) with EX480 (OpenShift) — invalid post-2026; electives must match the track.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Specialist tier mapped, with EX318→EX316 retirement noted.
- [ ] Security (SCAP), IdM, HA (fencing), and automation specialists sampled.
- [ ] A valid in-track RHCA elective set assembled.
