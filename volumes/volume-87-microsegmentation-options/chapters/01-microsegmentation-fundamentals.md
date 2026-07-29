# Chapter 01: Microsegmentation Fundamentals

## Learning Objectives

- Define microsegmentation and how it differs from perimeter and VLAN segmentation.
- Explain east-west traffic and lateral movement.
- Explain the zero-trust and least-privilege basis for segmentation.
- Reason about segmentation granularity (network, host, process, identity).
- Complete a walkthrough for each fundamentals topic.

## Theory and Architecture

**Microsegmentation** is the practice of enforcing least-privilege network policy **between individual
workloads** — not just at the perimeter. Traditional security is **north-south** (a firewall between the
internet and the data center) and coarse **VLAN/subnet** segmentation groups many hosts into one zone.
Once an attacker lands inside a zone, they move **east-west** (host to host) — **lateral movement** — to
reach valuable systems. Microsegmentation shrinks the blast radius by giving each workload its own
policy: only the flows it legitimately needs are allowed; everything else is denied. This is the
network expression of **zero trust** — never trust, always verify — and **least privilege**. Segmentation
can be enforced and expressed at different **granularities**: **network** (subnet/VLAN/ACL), **host**
(per-workload firewall), **process/application** (which program may talk to which), and **identity**
(which user/service account or workload identity, independent of IP). Finer granularity contains attacks
better but costs more to model and operate. This chapter builds the mental model the rest of the volume
compares options against.

## Design Considerations

Start from the **flows that matter**: map what actually talks to what before writing policy. Prefer an
**allowlist** (default-deny) model for real containment, but roll it out in **monitor/observe** mode
first to avoid breaking production. Choose a **granularity** that matches the risk — L4 (port/protocol)
for broad segmentation, L7/process/identity for high-value assets. Segment the **crown jewels** and
**ringfence** flat, high-risk zones (domain controllers, jump hosts, OT) first.

## Implementation and Automation

The labs map east-west dependencies, model an allowlist policy, and reason about granularity — the
groundwork every microsegmentation project starts with.

## Validation and Troubleshooting

Confirm the fundamentals:

```text
Perimeter (north-south) + VLAN zones = coarse; attacker moves east-west (lateral) inside a zone
Microsegmentation = per-workload least-privilege policy (default-deny allowlist) = smaller blast radius
Zero trust / least privilege = allow only needed flows, deny the rest, verify identity
Granularity: network (subnet/ACL) -> host (per-workload FW) -> process/app -> identity (IP-independent)
```

Common pitfalls: enforcing default-deny before **mapping** the real flows (breaks apps); and stopping at
**VLAN** segmentation and assuming it contains lateral movement (it does not, within a zone).

## Security and Best Practices

Microsegmentation is a **defensive** control that contains lateral movement in your own network. Map
first, enforce in monitor mode, then default-deny. Protect the segmentation controller itself. All work
is authorized administration.

## Hands-On Lab

Fundamentals walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 1.1 — Map east-west dependencies

**Objective:** See the flows a policy must allow.

```python
python3 - <<'PY'
flows = [
  ("web01",  "app01", "tcp/8080"),
  ("app01",  "db01",  "tcp/5432"),
  ("admin",  "app01", "tcp/22"),
  ("web01",  "db01",  "tcp/5432"),   # unexpected — web talking straight to DB?
]
for src, dst, svc in flows:
    print(f"{src:8} -> {dst:6} {svc}")
print("Review: web01->db01 bypasses the app tier — candidate to DENY after verification")
PY
```

**Expected result:** the real dependency map, including a suspicious `web01→db01` flow — the input to
policy.

**Negative test:** write allow rules from an architecture diagram instead of observed flows; the diagram
misses shadow paths — map **actual** traffic.

**Cleanup:** none.

### Lab 1.2 — Model an allowlist (default-deny) policy

**Objective:** Turn flows into least-privilege rules.

```python
python3 - <<'PY'
allow = {("web01","app01","tcp/8080"), ("app01","db01","tcp/5432"), ("admin","app01","tcp/22")}
tests = [("web01","app01","tcp/8080"), ("web01","db01","tcp/5432"), ("app01","db01","tcp/5432")]
for f in tests:
    print(f"{f} -> {'ALLOW' if f in allow else 'DENY (default)'}")
PY
```

```text
('web01', 'app01', 'tcp/8080') -> ALLOW
('web01', 'db01', 'tcp/5432') -> DENY (default)
('app01', 'db01', 'tcp/5432') -> ALLOW
```

**Expected result:** only the mapped flows allowed; the suspicious web→db flow denied by default —
least privilege.

**Negative test:** use a default-allow model with a few deny rules; anything you forgot stays open —
default-**deny** is the containment model.

**Cleanup:** none.

### Lab 1.3 — Reason about granularity

**Objective:** Match enforcement granularity to risk.

```python
python3 - <<'PY'
levels = {
  "Network (subnet/ACL)":  "coarse; easy; contains between zones, not within",
  "Host (per-workload FW)": "each workload its own policy; contains within a zone",
  "Process/application":    "only allowed programs communicate; stops living-off-the-land",
  "Identity (IP-independent)":"policy follows user/service/workload identity, not IP",
}
for level, note in levels.items():
    print(f"{level:26}: {note}")
print("Rule: finer granularity = more containment + more modeling effort; match to asset value")
PY
```

**Expected result:** the granularity ladder with its trade-off — finer contains more but costs more.

**Negative test:** apply process/identity-level policy to every low-value host on day one; the modeling
cost stalls the project — start L4 broadly, go finer on crown jewels.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsegmentation replaces coarse perimeter and VLAN segmentation with per-workload, least-privilege
(default-deny) policy that contains east-west lateral movement — the network form of zero trust —
enforced at a granularity (network, host, process, or identity) matched to each asset's risk, and always
built from **mapped** flows rolled out in monitor mode first.

- [ ] I can define microsegmentation versus perimeter/VLAN segmentation.
- [ ] I can explain east-west traffic and lateral movement.
- [ ] I can model an allowlist (default-deny) policy from mapped flows.
- [ ] I can reason about enforcement granularity.
- [ ] I completed Labs 1.1–1.3 including each negative test.
