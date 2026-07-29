# Chapter 04: SLES Networking, Security, and Monitoring

## Learning Objectives

- Configure networking on SLES.
- Secure the system (firewalld, users, permissions, SELinux/AppArmor).
- Manage processes and resources.
- Monitor system health and logs.
- Complete a walkthrough for each networking/security/monitoring topic.

## Theory and Architecture

The remaining SCA domains cover **networking, security, process management, and monitoring**.
**Networking** on SLES is configured with **wicked** (SUSE's network manager) or NetworkManager, plus
standard tools (`ip`), covering interfaces, addressing, routing, and DNS. **Security** spans the host
firewall (**firewalld**), user and permission management (users/groups, `sudo`, file permissions), and
**mandatory access control** — SLES uses **AppArmor** (profile-based confinement) by default, with
SELinux also available. **Process management** covers viewing and controlling processes (`ps`, `top`,
`systemctl`, signals) and resource limits. **Administration and monitoring** covers system health —
logs via **journalctl**, resource usage, and troubleshooting. Together these round out a SLES
administrator's daily toolkit: a networked, hardened, monitored system. This chapter teaches each with
a hands-on walkthrough (networking, firewalld/AppArmor, and monitoring).

## Design Considerations

Configure networking with **wicked**/NetworkManager consistently. Harden with **firewalld**
(default-deny), least-privilege **users/sudo**, correct **permissions**, and **AppArmor** confinement.
Monitor with **journalctl** and resource tools. Manage **processes** and limits. Keep the system
patched (Chapter 2) and configured (YaST).

## Implementation and Automation

The labs configure the firewall, check AppArmor, manage a process, and read logs.

## Validation and Troubleshooting

Confirm the networking/security/monitoring model:

```text
Networking: wicked / NetworkManager + ip (interfaces/routing/DNS). Security: firewalld (host firewall) + users/sudo/permissions + AppArmor (default MAC; SELinux optional).
Process: ps/top/systemctl/signals + limits. Monitoring: journalctl + resource tools. SCA domains: Network, Security, Process, Administration and Monitoring.
```

Common pitfalls: leaving the **firewall** open (default-deny inbound instead); and ignoring
**AppArmor** confinement.

## Security and Best Practices

Harden with **firewalld** (default-deny), least-privilege **users/sudo**, correct **permissions**, and
**AppArmor**; monitor with **journalctl**. Keep networking consistent. All work is authorized
administration.

## Hands-On Lab

Networking/security/monitoring walkthroughs. **Shared prerequisites** — a SLES/openSUSE VM (or read
commands), `python3`. **Cost:** none.

### Lab 4.1 — Configure the host firewall

**Objective:** Default-deny with needed services.

```bash
firewall-cmd --state 2>/dev/null || echo "firewalld: SLES host firewall"
firewall-cmd --list-services 2>/dev/null | head || echo "firewall-cmd --add-service=ssh --permanent; firewall-cmd --reload"
echo "SLES: default-deny inbound; allow only required services (ssh, http)"
```

**Expected result:** the **firewalld** service allow-list — host hardening.

**Negative test:** stop firewalld "to make it work"; that removes protection — **allow the service**
instead.

**Cleanup:** none.

### Lab 4.2 — Check AppArmor confinement

**Objective:** Mandatory access control.

```bash
aa-status 2>/dev/null | head || echo "aa-status: AppArmor profiles (enforce/complain) confining processes"
echo "SLES: AppArmor confines programs to declared file/capability access (default MAC)"
```

**Expected result:** **AppArmor** profiles confining processes — SLES mandatory access control.

**Negative test:** disable AppArmor for convenience; a compromised service is then unconfined — keep
profiles in **enforce**.

**Cleanup:** none (read-only).

### Lab 4.3 — Manage a process

**Objective:** Control running processes.

```bash
ps aux --sort=-%cpu 2>/dev/null | head -5 || ps aux | head -5
echo "top / systemctl / kill: inspect + control processes; systemd manages service processes"
```

**Expected result:** the top CPU **processes** and how to control them — process management.

**Negative test:** `kill -9` a systemd-managed service directly; systemd restarts it — use
**`systemctl stop`**.

**Cleanup:** none (read-only).

### Lab 4.4 — Monitor with journalctl

**Objective:** Read system health.

```bash
journalctl -p err -n 10 --no-pager 2>/dev/null || echo "journalctl -p err: recent errors across the system"
journalctl --disk-usage 2>/dev/null || echo "journalctl: unified systemd logs (filter by unit/priority/time)"
```

**Expected result:** recent **errors** from the unified journal — SLES monitoring.

**Negative test:** hunt through scattered `/var/log` files; **journalctl** is the unified, filterable
log — use it.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SLES networking, security, and monitoring cover wicked/NetworkManager networking, firewalld and
AppArmor hardening, process management, and journalctl monitoring — completing the SCA administrator's
daily toolkit.

- [ ] I can configure the host firewall.
- [ ] I can check AppArmor confinement.
- [ ] I can manage a process.
- [ ] I can monitor with journalctl.
- [ ] I completed Labs 4.1–4.4 including each negative test.
