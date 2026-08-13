# Chapter 02: Administrator — TMOS and Data Plane Concepts

## Learning Objectives

- Explain the BIG-IP TMOS architecture (management vs data plane).
- Install, license, provision, and upgrade a BIG-IP (F5CAB1).
- Configure base networking: VLANs, self-IPs, and route domains.
- Reason about full-proxy data-plane concepts (F5CAB2).
- Complete a walkthrough for each Administrator foundation topic.

## Theory and Architecture

The **F5 Certified Administrator** exams **F5CAB1** (Install, Initial Configuration, and Upgrade)
and **F5CAB2** (Data Plane Concepts) establish the BIG-IP foundation. **TMOS** — the Traffic
Management Operating System — separates a **management plane** (the GUI, `tmsh` CLI, and iControl
REST API, on the management interface) from a **data plane** (the **TMM**, Traffic Management
Microkernel, that processes application traffic on the TMM interfaces). BIG-IP is a **full
proxy**: it terminates the client connection and originates a separate server-side connection, so
it can inspect and manipulate traffic in both directions. Base networking is built from **VLANs**,
**self-IPs** (the BIG-IP's own IP on each VLAN), **trunks**, and optional **route domains** for
overlapping-address multi-tenancy. Modules (LTM, DNS, ASM, APM) are **provisioned** on top of
TMOS. Understanding the full-proxy model and the management/data-plane split is the basis for
everything else.

## Design Considerations

Keep the **management plane** on an isolated network, separate from the **data plane**. Provision
only the modules you license and need (provisioning consumes memory/CPU). Plan VLANs and self-IPs
before deploying virtual servers. Use the full-proxy model deliberately — it is what enables SSL
offload, WAF, and traffic manipulation.

## Implementation and Automation

The labs provision a module, configure a VLAN and self-IP, verify the full-proxy model, and read
system state via tmsh/iControl. All actions are **authorized administration**.

## Validation and Troubleshooting

Confirm the TMOS model:

```text
TMOS: management plane (GUI/tmsh/iControl REST) | data plane (TMM on TMM interfaces).
Full proxy: terminate client side, originate server side -> inspect/modify both directions.
Base net: VLANs + self-IPs + trunks (+ route domains for overlapping addresses).
Modules: LTM/DNS/ASM/APM provisioned on TMOS. Exams F5CAB1 (install/config/upgrade), F5CAB2 (data plane concepts).
```

Common pitfalls: putting management on the **data-plane** network; and over-provisioning modules
(resource exhaustion).

## Security and Best Practices

Isolate and restrict **management access** (dedicated VLAN, RBAC, strong auth). Provision
conservatively. Keep software current with F5's guidance and back up the config (UCS) before
upgrades. These are defensive administration practices.

## Hands-On Lab

Administrator walkthroughs. **Shared prerequisites** — a BIG-IP (Virtual Edition in an authorized
lab) with `tmsh` and iControl REST access. **Cost:** none with BIG-IP VE.

### Lab 2.1 — Provision a module

**Objective:** Enable LTM on the BIG-IP.

```bash
tmsh modify sys provision ltm level nominal
tmsh show sys provision
```

**Expected result:** the **LTM** module provisioned at nominal level — the platform ready for
traffic management.

**Negative test:** provision every module at `dedicated`; that **exhausts** resources — provision
only what you need at an appropriate level.

**Rollback:** `tmsh modify sys provision ltm level none` (in a lab).

### Lab 2.2 — Configure a VLAN and self-IP

**Objective:** Build base data-plane networking.

```bash
tmsh create net vlan external interfaces add { 1.1 } tag 4093
tmsh create net self 10.10.20.5/24 vlan external
tmsh list net self 10.10.20.5
```

**Expected result:** an **external VLAN** and a **self-IP** on it — the BIG-IP's presence on the
data-plane network.

**Negative test:** assign a virtual server with no VLAN/self-IP path to the servers; base
**networking** must exist first — build the VLAN and self-IP.

**Rollback:** `tmsh delete net self 10.10.20.5; tmsh delete net vlan external`.

### Lab 2.3 — Verify the full-proxy model

**Objective:** Describe client-side vs server-side connections.

```text
# BIG-IP full proxy: CLIENT --(client-side conn)--> BIG-IP --(server-side conn)--> SERVER
#   Two independent connections -> BIG-IP can offload SSL, inspect (WAF), and steer traffic.
"full proxy: terminate client side + originate server side = inspect/modify both"
```

**Expected result:** the **full-proxy** two-connection model — the basis for offload and
inspection.

**Negative test:** treat BIG-IP as a simple packet forwarder; it is a **full proxy** — reason
about two connections.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Read system state via iControl REST

**Objective:** Query the BIG-IP over the API.

```bash
curl -sk -u "$BIGIP_CRED" "https://<bigip>/mgmt/tm/sys/version" 2>/dev/null \
  | python3 -c "import sys,json;print('TMOS version:', json.load(sys.stdin).get('selfLink','see nestedStats'))" 2>/dev/null \
  || echo "BIG-IP iControl REST at /mgmt/tm/... returns structured JSON (basic auth or token)"
```

**Expected result:** the TMOS version/state from the **iControl REST API** — the platform is
programmable.

**Negative test:** screen-scrape the GUI for state; **iControl REST** returns JSON — use it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The F5CAB1/F5CAB2 Administrator exams establish TMOS: a management/data-plane split, the
full-proxy model, base networking (VLANs, self-IPs, route domains), and module provisioning.
Isolate management, provision conservatively, and build base networking before virtual servers.

- [ ] I can provision a module with tmsh.
- [ ] I can configure a VLAN and self-IP.
- [ ] I can explain the full-proxy model.
- [ ] I can read system state via iControl REST.
- [ ] I completed Labs 2.1–2.4 including each negative test.
