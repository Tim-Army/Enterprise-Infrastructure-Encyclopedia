# Chapter 05: Sentry — Deployment and Architecture

## Learning Objectives

- Install and configure the CyberArk PAM components.
- Design a resilient, hardened Vault architecture.
- Plan high availability and disaster recovery.
- Harden and validate a deployment.
- Complete a walkthrough for each deployment topic.

## Theory and Architecture

The **Sentry** level (prerequisite: Defender) validates **deploying, installing, and configuring** the
CyberArk solution. It covers standing up the **Digital Vault** (the hardened core, on a dedicated,
locked-down server with its own firewall and encryption), then the satellite components — **CPM**,
**PVWA**, and **PSM** — and connecting them securely to the Vault. Architecture decisions include
**high availability** (Vault clustering / a Disaster Recovery Vault that replicates the primary),
**component redundancy** (multiple CPMs/PVWAs/PSMs for scale and resilience), **network placement**
(the Vault isolated, components in appropriate zones), and **hardening** (the Vault server is
security-hardened by design — minimal services, no domain membership, strict firewall). A Sentry
plans, installs, configures, and **validates** the deployment so it is resilient and secure. This
chapter teaches each with a hands-on defensive walkthrough (component topology, HA/DR planning, and
hardening checks).

## Design Considerations

Isolate and **harden the Vault** (dedicated server, minimal surface, strict firewall). Deploy
**redundant** components for HA and scale. Plan **DR** (Disaster Recovery Vault replication) and test
failover. Place components in the right **network zones**. Validate the deployment end to end before
go-live.

## Implementation and Automation

The labs plan component topology, design HA/DR, and check hardening.

## Validation and Troubleshooting

Confirm the deployment model:

```text
Install Vault (hardened, isolated) -> connect CPM/PVWA/PSM securely. HA: Vault cluster / DR Vault replication + redundant components.
Hardening: dedicated server, minimal services, no domain join, strict firewall. Validate end to end.
```

Common pitfalls: a **single** Vault with no DR (single point of failure); and a **non-hardened** Vault
server (defeats the purpose).

## Security and Best Practices

**Harden and isolate** the Vault, deploy **redundant** components, plan and **test DR**, place
components in correct zones, and **validate** before go-live. All work is defensive.

## Hands-On Lab

Deployment walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 5.1 — Plan the component topology

**Objective:** Place components correctly.

```python
python3 - <<'PY'
topology={"Vault (primary)":"isolated secure zone, hardened server",
          "DR Vault":"separate site, replicates primary",
          "CPM x2":"management zone (redundant)","PVWA x2":"app zone behind LB (redundant)",
          "PSM x2":"session zone (redundant, near targets)"}
for comp,place in topology.items(): print(f"{comp:16}: {place}")
PY
```

**Expected result:** a **redundant, zoned** topology with an isolated Vault and DR — the Sentry
architecture.

**Negative test:** put the Vault in the general server VLAN with everything else; it's exposed —
**isolate** it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Design high availability and DR

**Objective:** Survive a failure.

```python
python3 - <<'PY'
plan={"HA":"redundant CPM/PVWA/PSM + Vault cluster","DR":"DR Vault replicates primary to a second site",
      "failover_test":"quarterly: promote DR, validate, fail back","rpo":"near-zero (continuous replication)"}
for k,v in plan.items(): print(f"{k:13}: {v}")
print("Sentry: no single point of failure; test failover regularly")
PY
```

**Expected result:** an **HA + DR** plan with tested failover — resilient PAM.

**Negative test:** deploy one Vault and never test DR; an outage takes down all privileged access —
build and **test** HA/DR.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Check Vault hardening

**Objective:** Validate the secure baseline.

```python
python3 - <<'PY'
checks={"dedicated server":True,"domain-joined":False,"extra services":False,
        "firewall default-deny":True,"encryption at rest":True}
issues=[k for k,ok in checks.items() if (k in ("domain-joined","extra services") and ok) or (k not in ("domain-joined","extra services") and not ok)]
print("hardening issues:", issues or "none — Vault baseline OK")
PY
```

**Expected result:** a hardened Vault baseline with **no issues** — Sentry hardening validation.

**Negative test:** domain-join the Vault or run extra services on it; that widens attack surface —
keep it **minimal and standalone**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Validate the deployment end to end

**Objective:** Prove it works before go-live.

```python
python3 - <<'PY'
tests=["Vault reachable + healthy","CPM rotates a test account","PVWA login + retrieve works",
       "PSM launches + records a session","PTA receives events","DR replication current"]
for t in tests: print(f"[PASS] {t}")
print("Sentry: validate every component path before production cutover")
PY
```

**Expected result:** all component paths **validated** — a deployment ready for go-live.

**Negative test:** cut over without validating PSM/DR; a broken path surfaces in production — **validate
end to end** first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Sentry deployment domain installs and configures a hardened, isolated Vault with redundant CPM/
PVWA/PSM components, plans and tests HA/DR, and validates the deployment end to end — resilient,
secure PAM infrastructure.

- [ ] I can plan the component topology.
- [ ] I can design HA and DR.
- [ ] I can check Vault hardening.
- [ ] I can validate the deployment end to end.
- [ ] I completed Labs 5.1–5.4 including each negative test.
