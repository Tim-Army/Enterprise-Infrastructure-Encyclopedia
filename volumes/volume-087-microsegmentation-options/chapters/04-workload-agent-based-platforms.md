# Chapter 04: Workload and Agent-Based Platforms

## Learning Objectives

- Explain label-based, agent-first segmentation (Illumio).
- Explain telemetry-rich agent segmentation (Cisco Secure Workload).
- Explain agent-based segmentation with threat hunting (Akamai Guardicore).
- State the pros, cons, compatibility, and requirements of each.
- Complete a walkthrough for each agent-based topic.

## Theory and Architecture

**Workload/agent-based** platforms install a lightweight agent on each workload that programs the host
firewall and reports flows to a central controller — enforcement travels with the workload across
on-prem, cloud, and (sometimes) containers. Three leaders:

- **Illumio Core / Zero Trust Segmentation** — a **label-based, agent-first** model. The **VEN** agent
  on each workload reports flows to the **PCE** controller; policy is written against **labels** (role,
  application, environment, location), not IP or topology, and rendered into host-firewall rules. Strong
  process-level visibility and a real-time **traffic map (Illumination)**.
- **Cisco Secure Workload** (formerly **Tetration**) — agents plus rich **network telemetry** feed deep
  **application dependency mapping** and behavior baselining, then generate allowlist policy. The most
  telemetry-heavy option; correspondingly resource-intensive and complex.
- **Akamai Guardicore Segmentation** — agent-based with its own enforcement, known for strong
  data-center **east-west visibility**, an intuitive map, and integrated **threat hunting/deception** and
  AI-assisted policy.

All three give fine-grained, workload-portable policy; all three require deploying and operating agents.

## Pros, Cons, Compatibility, and Requirements

**Illumio Core / ZTS**

- **Pros:** label-based (policy independent of IP/topology); excellent traffic map; process-level;
  hybrid cloud; largest market mindshare; scales.
- **Cons:** requires the VEN agent on every workload; cost at scale; primarily workload-focused.
- **Compatibility:** Windows/Linux servers, cloud VMs, some container/Kubernetes; not network gear/OT
  natively.
- **Requirements:** PCE controller (SaaS or self-hosted) + VEN agents; label taxonomy design.

**Cisco Secure Workload (Tetration)**

- **Pros:** deepest visibility and application dependency mapping; behavior baselining; enforcement +
  analytics; scales to very large data centers.
- **Cons:** heavy and complex; resource-intensive; higher cost and operational burden.
- **Compatibility:** Windows/Linux agents; network telemetry from Cisco fabric; cloud workloads.
- **Requirements:** Secure Workload platform (SaaS or on-prem appliance) + agents; telemetry sources.

**Akamai Guardicore Segmentation**

- **Pros:** strong east-west visibility and map; integrated threat hunting/deception; hybrid; AI-assisted
  policy; relatively quick to value.
- **Cons:** proprietary agent (heavier than OS-firewall-only approaches); workload-focused.
- **Compatibility:** Windows/Linux (incl. legacy versions), cloud, some containers; agentless reach
  limited.
- **Requirements:** Guardicore management (SaaS/on-prem) + agents.

## Design Considerations

Choose **Illumio** for label-driven, workload-portable policy with a clear map; **Cisco Secure Workload**
when you need the deepest dependency mapping and already invest in Cisco; **Guardicore** for fast
east-west visibility with threat hunting. All three assume you can **deploy agents** — plan the agent
lifecycle (rollout, upgrades, coverage gaps). For assets that cannot take an agent (OT/IoT/legacy), pair
with an appliance or network model.

## Implementation and Automation

The labs model an Illumio label-based policy, reason about Secure Workload dependency mapping, and
compare the three agent platforms — the agent-based options in the rubric.

## Validation and Troubleshooting

Confirm agent-based enforcement:

```text
Illumio: VEN agent -> PCE; policy on LABELS (role/app/env/loc); host-firewall rendered; traffic map
Cisco Secure Workload: agents + network telemetry -> dependency map + behavior -> allowlist (heavy)
Guardicore: agent + own enforcement; east-west visibility + threat hunting
All: workload-portable, fine-grained; ALL require agents (lifecycle + coverage)
```

Common pitfalls: partial **agent coverage** leaving unsegmented hosts (the map has blind spots); and
enforcing before the **dependency map** is complete (breaks apps).

## Security and Best Practices

Agent-based policy is portable and fine-grained — protect the controller (PCE/Secure Workload/Guardicore
console) and the agents' integrity. Roll out in monitor mode, reach high **coverage**, then enforce. All
work is authorized administration.

## Hands-On Lab

Agent-based walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 4.1 — Model an Illumio label-based policy

**Objective:** Write policy on labels, not IPs.

```python
python3 - <<'PY'
# workloads carry labels: (role, app, env, loc)
workloads = {
  "web-1": ("web","shop","prod","us"),
  "app-1": ("app","shop","prod","us"),
  "db-1":  ("db","shop","prod","us"),
}
rules = [
  ("role=web,app=shop","role=app,app=shop","tcp/8080"),
  ("role=app,app=shop","role=db,app=shop","tcp/5432"),
]
for w,l in workloads.items(): print(f"{w}: role={l[0]} app={l[1]} env={l[2]} loc={l[3]}")
for s,d,svc in rules: print(f"Rule: {s}  ->  {d}  {svc}")
print("Illumio renders these label rules into host-firewall rules on each VEN")
PY
```

**Expected result:** tier rules expressed by label (role/app), independent of IP — new prod-shop
workloads inherit policy by label.

**Negative test:** write Illumio rules per-IP; you lose the label portability that is the point — use
labels.

**Cleanup:** none.

### Lab 4.2 — Reason about dependency mapping (Secure Workload)

**Objective:** Value deep telemetry before policy.

```python
python3 - <<'PY'
observed = [
  ("app-1","db-1","tcp/5432", 5000),
  ("app-1","cache-1","tcp/6379", 800),
  ("app-1","smtp-1","tcp/25", 3),     # rare — batch job? verify before allow/deny
]
for s,d,svc,flows in observed:
    tag = "core dependency" if flows > 100 else "rare — verify"
    print(f"{s}->{d} {svc}: {flows} flows/day ({tag})")
print("Secure Workload maps app dependencies + baselines behavior -> generated allowlist")
PY
```

**Expected result:** frequent dependencies vs rare flows surfaced — the map that drives a correct
allowlist.

**Negative test:** auto-enforce every observed flow including one-off noise; review **rare** flows
before allowing them.

**Cleanup:** none.

### Lab 4.3 — Compare the three agent platforms

**Objective:** Match each to a fit.

```python
python3 - <<'PY'
compare = {
  "Illumio":        "label-based, best map/UX, hybrid; needs VEN agents",
  "Cisco Secure WL":"deepest telemetry + dependency map; heavy/complex/costly",
  "Guardicore":     "east-west visibility + threat hunting; proprietary agent",
}
for tool, note in compare.items(): print(f"{tool:16}: {note}")
print("All agent-based: portable + fine-grained, but agent lifecycle + coverage required")
PY
```

**Expected result:** the three platforms contrasted with their shared agent requirement.

**Negative test:** assume any of the three segments OT devices they cannot install on; pair with an
appliance/network model for those.

**Cleanup:** none.

### Lab 4.4 — Reason about agent coverage risk

**Objective:** Quantify the blind-spot risk.

```python
python3 - <<'PY'
total, with_agent = 1000, 910
uncovered = total - with_agent
print(f"Workloads: {total}; with agent: {with_agent}; UNCOVERED: {uncovered} ({uncovered/total:.0%})")
print("Those 90 hosts are unsegmented blind spots -> reach coverage before enforcing default-deny")
PY
```

**Expected result:** the uncovered fraction quantified — the coverage gap to close before enforcement.

**Negative test:** enforce default-deny with 9% of hosts lacking agents; those hosts are either exposed
or broken — reach coverage first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Workload/agent-based platforms — Illumio (label-based, best-in-class map), Cisco Secure Workload (deepest
telemetry, heavy), and Akamai Guardicore (east-west visibility with threat hunting) — give portable,
fine-grained policy that travels with the workload, at the cost of deploying and operating agents and
reaching full coverage before enforcing.

- [ ] I can explain Illumio label-based segmentation.
- [ ] I can explain Secure Workload dependency mapping.
- [ ] I can state the pros, cons, compatibility, and requirements of each.
- [ ] I can quantify agent-coverage risk.
- [ ] I completed Labs 4.1–4.4 including each negative test.
