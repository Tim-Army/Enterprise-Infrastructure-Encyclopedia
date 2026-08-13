# Chapter 02: ESXi 8 and the Distributed Services Engine

## Learning Objectives

- Install and configure ESXi 8.
- Explain the vSphere Distributed Services Engine and DPUs.
- Understand how DPU offload changes host architecture.
- Manage an ESXi 8 host with esxcli.
- Complete a walkthrough for each ESXi 8 topic.

## Theory and Architecture

**ESXi 8** installs and is managed like ESXi 7 (ISO → DCUI → management network; esxcli/Host
Client), but adds support for the **vSphere Distributed Services Engine (DSE)** — vSphere 8's
marquee hardware feature. A **DPU (Data Processing Unit)**, also called a SmartNIC, is a small
computer on a network card with its own CPU, memory, and OS. With DSE, ESXi runs a **second,
lightweight ESXi instance on the DPU** and **offloads** network switching, storage services, and
security (NSX distributed firewall) **to the DPU** — freeing the host x86 CPU for VM workloads,
improving performance, and isolating infrastructure services from the workload domain (a security
benefit). The DPU is provisioned and lifecycle-managed by **vLCM** alongside the host. Not every
host has a DPU; DSE is opt-in on supported hardware. Beyond DSE, ESXi 8 raises configuration
maximums, supports the latest CPUs (via updates), and refines the host services you already know.

## Design Considerations

Deploy **DPUs** where **CPU offload** and **east-west isolation** matter (dense virtualization,
NSX security). Keep the same host-hardening discipline (NTP, syslog, controlled SSH, lockdown).
Manage DPU + host lifecycle together via **vLCM images**. Where no DPU exists, ESXi 8 operates like
7 with higher maximums.

## Implementation and Automation

The labs configure the host, inspect DPU/hardware, and reason about the offload model.

## Validation and Troubleshooting

Confirm the ESXi 8 / DSE model:

```text
ESXi 8: install/manage like 7 (DCUI, esxcli, Host Client) + higher maximums + latest CPUs.
Distributed Services Engine: DPU/SmartNIC runs a lightweight ESXi -> offload network/storage/NSX security.
Benefits: host CPU freed, better performance, infra services isolated from workload domain. vLCM manages the DPU.
```

Common pitfalls: expecting **DSE** on hosts without a DPU; and lifecycle-managing the DPU
separately from the host (use **vLCM** together).

## Security and Best Practices

Use the DPU to **isolate** network/security services from the workload domain, keep the same host
hardening (Chapter 8), and manage DPU+host with **vLCM**. Verify hardware compatibility for DSE.
Offload deliberately where it pays off.

## Hands-On Lab

ESXi 8 walkthroughs. **Shared prerequisites** — an ESXi 8 host (physical or nested), in a lab.
**Cost:** none.

### Lab 2.1 — Configure the management network

**Objective:** Verify the host's management adapter.

```bash
esxcli network ip interface ipv4 get
esxcli system ntp set --server=pool.ntp.org --enabled=true
esxcli system ntp get
```

**Expected result:** the **vmk0** management adapter and **NTP** synchronized — the ESXi 8 host on
the network with accurate time.

**Negative test:** run without NTP; time drift breaks certificates/vCenter — enable NTP (same as 7).

**Rollback:** `esxcli system ntp set --enabled=false` in a lab.

### Lab 2.2 — Inspect host hardware for DPU

**Objective:** Check for a Distributed Services Engine DPU.

```bash
esxcli hardware pci list | grep -iA2 -E "DPU|SmartNIC|Pensando|BlueField" | head \
  || echo "no DPU present; DSE requires a supported DPU/SmartNIC (e.g., NVIDIA BlueField, AMD Pensando)"
esxcli network nic list
```

**Expected result:** a **DPU** if present (or a note that none is) — DSE eligibility.

**Negative test:** enable DSE on a host with **no DPU**; DSE requires **supported DPU hardware** —
verify first.

**Rollback:** none (read-only).

### Lab 2.3 — Explain the offload model

**Objective:** Describe what the DPU does.

```text
# Without DSE: host x86 CPU runs the virtual switch, storage services, and NSX firewall.
# With DSE: the DPU runs those -> host CPU serves VMs; infra services isolated on the DPU.
"DSE: virtual switching + storage services + NSX security -> offloaded to DPU (host CPU freed)"
```

**Expected result:** the **offload** model — infrastructure services on the DPU, workloads on the
host CPU.

**Negative test:** expect DSE to speed up a host with no network/security offload need; it pays off
where **infra services** consume CPU — target those cases.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Maintenance mode

**Objective:** Prepare the host for changes.

```bash
esxcli system maintenanceMode set --enable=true
esxcli system maintenanceMode get
esxcli system maintenanceMode set --enable=false
```

**Expected result:** the host entering/exiting **maintenance mode** — the safe state for
patching/DPU updates (VMs evacuate via DRS).

**Negative test:** patch a host with running VMs and no maintenance mode; **enter maintenance mode**
first.

**Rollback:** ensure the host is out of maintenance mode.

### Lab 2.5 — Review host services and hardening

**Objective:** Confirm secure host configuration.

```bash
esxcli network firewall ruleset list --ruleset-id=sshServer
esxcli system syslog config get
```

**Expected result:** SSH controlled and **syslog** configured — a hardened ESXi 8 host (same
discipline as 7).

**Negative test:** leave SSH permanently enabled; control it and use lockdown mode (Chapter 8).

**Rollback:** ensure SSH is disabled after the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ESXi 8 installs and is managed like ESXi 7 with higher maximums, and adds the vSphere Distributed
Services Engine — offloading network, storage, and NSX security to a DPU/SmartNIC to free host CPU
and isolate infrastructure services, lifecycle-managed by vLCM. Use DPUs where offload pays off,
and keep the same host hardening.

- [ ] I can configure the management network and NTP.
- [ ] I can check a host for a DPU.
- [ ] I can explain the DSE offload model.
- [ ] I can use maintenance mode and review hardening.
- [ ] I completed Labs 2.1–2.5 including each negative test.
