# Chapter 02: CCSA — Gaia and Deployment

## Learning Objectives

- Explain the Check Point three-tier architecture.
- Configure Gaia with clish and the Gaia Portal.
- Deploy a Security Gateway and Management Server, and establish SIC.
- Navigate SmartConsole.
- Complete a walkthrough for each deployment topic.

## Theory and Architecture

Check Point uses a **three-tier architecture**: the **SmartConsole** (the administrator's GUI
client), the **Security Management Server** (stores the policy, objects, and logs, and pushes
policy), and one or more **Security Gateways** (enforce the policy on traffic). All run on
**Gaia**, Check Point's hardened OS, managed by **clish** (the structured CLI — `set`, `show`,
`save config`), the **Gaia Portal** (web UI), and **expert mode** (a bash shell for advanced
tasks). Deployment installs Gaia, runs the **First Time Configuration Wizard** to choose the role
(gateway, management, or standalone), and then establishes **SIC (Secure Internal Communication)** —
the certificate-based trust between the management server and each gateway that lets them
communicate securely. Once SIC is up and the gateway is added as an object in SmartConsole, the
management server can push policy to it. This deployment foundation underlies everything in CCSA.

## Design Considerations

Separate **management** from **gateway** roles in production (distributed deployment) for scale and
resilience; use **standalone** only for small/lab setups. Establish **SIC** with a strong one-time
password. Configure Gaia base settings (hostname, interfaces, DNS, NTP, routing) via **clish** for
repeatability. Keep SmartConsole and Gaia current with the release.

## Implementation and Automation

The labs configure Gaia networking with clish, verify SIC, and inspect the gateway.

## Validation and Troubleshooting

Confirm the deployment model:

```text
Three tiers: SmartConsole (GUI) -> Security Management Server (policy/logs) -> Security Gateway (enforcement).
Gaia OS: clish (set/show/save config) + Gaia Portal + expert mode. Deploy: First Time Wizard -> role -> SIC (cert trust).
Distributed (mgmt + gateway) preferred; standalone for small/lab.
```

Common pitfalls: broken **SIC** (gateway can't get policy); and configuring in expert mode where
**clish** (persistent, structured) belongs.

## Security and Best Practices

Use a **distributed** deployment, establish **SIC** securely, configure Gaia via **clish** (saved
config), and restrict management access. Keep NTP accurate (certificates/logs depend on it). Update
to the current release. Defensive administration throughout.

## Hands-On Lab

Deployment walkthroughs. **Shared prerequisites** — Check Point Quantum management + gateway (VM/
eval) with Gaia, in a lab. **Cost:** none.

### Lab 2.1 — Configure Gaia networking with clish

**Objective:** Set base network configuration.

```bash
clish
set interface eth0 ipv4-address 10.0.0.10 mask-length 24
set static-route 0.0.0.0/0 nexthop gateway address 10.0.0.1 on
set dns primary 10.0.0.53
save config
show interface eth0
```

**Expected result:** eth0 addressed with a default route and DNS, **saved** — Gaia base networking.

**Negative test:** configure the interface without **`save config`**; changes are lost on reboot —
save them.

**Rollback:** revert in a lab as needed.

### Lab 2.2 — Verify SIC

**Objective:** Confirm management-to-gateway trust.

```bash
# On the gateway (expert mode):
cpconfig    # option to reset/initialize SIC with a one-time password
# On management (SmartConsole/mgmt): the gateway object's SIC status shows "Trust established".
cp_conf sic state 2>/dev/null || echo "SIC = certificate trust between mgmt and gateway; must be 'Trust established'"
```

**Expected result:** **SIC trust established** — the management server can push policy to the
gateway.

**Negative test:** add a gateway object with **no SIC**; policy install fails — establish SIC
first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Inspect the gateway

**Objective:** Review gateway status and blades.

```bash
clish -c "show version all"
cpstat fw    2>/dev/null | head || echo "cpstat fw shows firewall status/policy; enabled blades listed in SmartConsole"
```

**Expected result:** the gateway version and **firewall status** — a deployed, enforcing gateway.

**Negative test:** assume the gateway is enforcing without checking; **cpstat/SmartConsole** confirm
policy is installed — verify.

**Rollback:** none (read-only).

### Lab 2.4 — Navigate SmartConsole objects

**Objective:** Understand the object model.

```text
# SmartConsole: define network objects (hosts, networks, gateways, services), then reference them
#   in the policy. Objects are reusable and central to Check Point policy.
"objects: hosts/networks/services/gateways -> reused across policy rules"
```

**Expected result:** the **object model** — reusable objects referenced by policy (the CCSA
foundation for Chapter 3).

**Negative test:** hard-code IPs in every rule; **objects** make policy readable and maintainable —
use them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.5 — Save and back up the configuration

**Objective:** Protect the configuration.

```bash
clish -c "save config"
# Management database: take a management backup / migrate export for disaster recovery.
echo "save config (Gaia) + management backup (database) -> recoverable deployment"
```

**Expected result:** Gaia config **saved** and the management database backed up — a recoverable
deployment.

**Negative test:** change policy/config with no backup; a failure is then hard to recover — back up
first.

**Rollback:** none (keep the backup).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Check Point's three-tier architecture (SmartConsole → Management Server → Security Gateway) runs on
Gaia, deployed via the First Time Wizard and secured with SIC. Configure Gaia with clish, establish
SIC, use the object model, and back up. Distributed deployments scale; standalone suits labs.

- [ ] I can configure Gaia networking with clish.
- [ ] I can verify SIC trust.
- [ ] I can inspect gateway status.
- [ ] I can navigate the SmartConsole object model and back up.
- [ ] I completed Labs 2.1–2.5 including each negative test.
