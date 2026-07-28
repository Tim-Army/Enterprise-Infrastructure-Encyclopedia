# Chapter 05: Security Service Edge Engineer and Network Security Architect

## Learning Objectives

- Explain the Security Service Edge Engineer and Network Security Architect credentials.
- Describe Prisma Access and the SASE/SSE model.
- Enforce Zero Trust access to applications from the cloud edge.
- Design a Network Security architecture from requirements.
- Complete a walkthrough for each SSE and architecture topic.

## Theory and Architecture

The **Security Service Edge Engineer** (Specialist) credential covers **Prisma Access** —
Palo Alto's cloud-delivered **SSE**, the security half of **SASE**. Instead of backhauling
users to a data-center firewall, Prisma Access delivers firewall, **SWG**, **CASB**, **ZTNA**,
and DLP from the cloud, close to users and apps, enforcing the same App-ID/User-ID/Content-ID
policy everywhere. The **Network Security Architect** (Architect) credential is the design
capstone for the track: taking requirements — sites, remote users, applications, compliance,
and threat model — and producing an architecture that spans on-prem NGFW, Panorama, SD-WAN, and
Prisma Access, with Zero Trust segmentation, HA, and centralized policy, justifying each
trade-off. SSE brings the enforcement to the user; the architect ties the whole Network
Security stack together.

## Design Considerations

Deliver security from the **cloud edge** (Prisma Access) for remote users and branches so
policy follows the user, not the location. Enforce **ZTNA** (per-app access, not network
access). At the architecture level, design **requirement-first**, remove single points of
failure, and keep one **consistent policy** across on-prem and cloud edge.

## Implementation and Automation

The labs reason about SSE service chaining, ZTNA access, and an architecture design from
requirements.

## Validation and Troubleshooting

Confirm the SSE and architecture model:

```text
SSE (Prisma Access): cloud-delivered FWaaS + SWG + CASB + ZTNA + DLP; policy follows the user.
SASE = SD-WAN (network) + SSE (security), converged.
Architect: requirements -> NGFW + Panorama + SD-WAN + Prisma Access -> Zero Trust + HA + one policy.
```

Common pitfalls: backhauling remote users to a central firewall (latency; use **Prisma
Access**); and granting **network** access instead of **per-app ZTNA**.

## Security and Best Practices

Enforce **least-privilege ZTNA** — users reach only the apps their role permits. Keep **one
policy** across on-prem and cloud edge. Design with **no single point of failure** and map every
decision to a requirement. Zero Trust, delivered from the edge.

## Hands-On Lab

SSE and architecture walkthroughs. **Shared prerequisites for Labs 5.1–5.4** — a shell with
`python3`. **Cost:** none.

### Lab 5.1 — Model SSE service chaining

**Objective:** Describe cloud-delivered security for a remote user.

```python
python3 - <<'PY'
chain=["Prisma Access (nearest node)","FWaaS + App-ID","SWG (URL/threat)","CASB (SaaS)",
       "ZTNA (per-app)","DLP"]
print("remote user -> " + " -> ".join(chain) + " -> app")
print("policy follows the user (not the location)")
PY
```

**Expected result:** a remote user's traffic secured through the **Prisma Access** service
chain — SSE from the cloud edge.

**Negative test:** backhaul the user to HQ for inspection; **SSE** delivers it near the user —
avoid the hairpin.

**Cleanup:** none.

### Lab 5.2 — ZTNA access decision

**Objective:** Grant per-application, not network, access.

```python
python3 - <<'PY'
def ztna(user_authorized_for_app, device_healthy):
    return "grant access to THIS app only" if (user_authorized_for_app and device_healthy) else "deny"
print("authorized+healthy:", ztna(True,True))
print("authorized, unhealthy device:", ztna(True,False))
PY
```

**Expected result:** access to **one app** when authorized and healthy — ZTNA, not network
access.

**Negative test:** drop the user onto the corporate network (VPN-style); **ZTNA** grants
per-app access only — scope it.

**Cleanup:** none.

### Lab 5.3 — Architecture from requirements

**Objective:** Translate requirements into a Network Security design.

```python
python3 - <<'PY'
req={"sites":12,"remote_users":3000,"saas_heavy":True,"compliance":"PCI"}
design={"branches":"Prisma SD-WAN + local breakout",
        "remote_users":"Prisma Access (SSE/ZTNA)",
        "datacenter":"NGFW HA pair + Panorama",
        "policy":"one App-ID/User-ID policy across on-prem + edge",
        "segmentation":"Zero Trust; PCI zone isolated"}
print("requirements:",req)
for k,v in design.items(): print(f"  {k:12}: {v}")
PY
```

**Expected result:** a requirement-driven design spanning **SD-WAN, Prisma Access, NGFW/Panorama**
with one policy — the architect deliverable.

**Negative test:** design product-first with no requirements; architect **requirement-first** and
justify trade-offs.

**Cleanup:** none.

### Lab 5.4 — Failure and consistency check

**Objective:** Verify no SPOF and one policy.

```python
python3 - <<'PY'
design={"datacenter":"NGFW HA pair","edge":"Prisma Access (cloud, multi-node)",
        "policy":"single source in Panorama pushed everywhere"}
spof=[k for k,v in design.items() if "single" in v.lower() and "policy" not in k]
print("SPOF:", spof or "none"); print("policy consistency:", "one source" )
PY
```

**Expected result:** **no single point of failure** and **one policy source** — a resilient,
consistent architecture.

**Negative test:** run separate, divergent policies on-prem and in the cloud; keep **one policy
source** — consistency prevents gaps.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SSE Engineer credential covers Prisma Access — cloud-delivered FWaaS/SWG/CASB/ZTNA/DLP where
policy follows the user — and the Network Security Architect credential ties NGFW, Panorama,
SD-WAN, and Prisma Access into one requirement-driven, Zero-Trust, no-SPOF architecture with a
single policy source. Deliver security from the edge and design requirement-first.

- [ ] I can describe the Prisma Access SSE service chain.
- [ ] I can make a ZTNA per-app access decision.
- [ ] I can design a Network Security architecture from requirements.
- [ ] I can verify no SPOF and one policy source.
- [ ] I completed Labs 5.1–5.4 including each negative test.
