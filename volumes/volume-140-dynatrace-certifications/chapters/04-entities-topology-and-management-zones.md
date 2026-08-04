# Chapter 04: Entities, Topology, and Management Zones

## Learning Objectives

- Explain the entity model and how Smartscape topology is built and maintained.
- Use tags and management zones to divide a shared environment.
- Distinguish access control from view filtering — and know why confusing them is dangerous.
- Design a tagging scheme that survives growth.

*Exam relevance: **Components And Architecture** and **Reporting And Analysis** (Associate); **Permissions and Policies** (Advanced Observability Specialist).*

## Entities and topology

Dynatrace models a monitored estate as **entities** — hosts, processes, services, applications, containers, cloud resources — with typed relationships between them: *runs on*, *calls*, *depends on*. The live graph of those relationships is **Smartscape**.

The graph is built automatically from observed behavior rather than declared in configuration, and that is the crucial property. A dependency appears because a call was seen, not because someone documented it. Consequently, Smartscape is usually more accurate than the architecture diagram, and it is accurate about **what happened recently**, which is a subtly different claim.

Each entity carries a stable identifier — `HOST-1A2B3C`, `SERVICE-9F8E7D` — that persists across restarts and re-IPs. Those IDs are what DQL joins on and what alerts reference, which makes them the durable handle for automation.

The dependency graph is not decoration. It is the input to Davis AI's causal analysis (Chapter 06): **root cause determination is only as good as the topology it reasons over.** A missing dependency does not merely leave a gap in a diagram — it removes a causal path, and the analysis then attributes a problem to the wrong place with full confidence.

## Tags

Tags attach meaning that the platform cannot infer. Dynatrace produces them three ways:

| Source | How | Best for |
|:---|:---|:---|
| **Automatically applied** | From cloud metadata, Kubernetes labels, process detection | Cloud/K8s estates where the truth already exists |
| **Rule-based** | Rules matching entity properties | Consistent, self-maintaining classification |
| **Manual** | Applied directly to an entity | Exceptions — and a maintenance liability |

The strong preference is rule-based. A rule such as *"tag any host whose name starts with `pci-` as `zone:pci`"* applies itself to hosts created next year by people who never read the rule. A manual tag applies to exactly the entity it was placed on, and rots the moment the estate changes.

## Management zones

A **management zone** is a rule-defined slice of the environment — "everything belonging to the payments team," "everything in the PCI scope." Zones drive both what a user sees and what they may access.

Here is the distinction that matters and that gets people into trouble:

| Mechanism | Effect | Security relevance |
|:---|:---|:---|
| **Filtering** in the UI | Changes what *you* are currently looking at | **None** — you can remove the filter |
| **Management zone permissions** | Constrains what a user is *allowed* to see | **Yes** — this is access control |

Treating a UI filter as a boundary is the error. If a user can clear the filter, it was never a control. Only permissions bound to management zones restrict access — and this matters most in exactly the environments where it is most tempting to hand-wave: regulated scopes, multi-tenant platforms, and estates shared with contractors.

## Hands-On Lab

Python models entities and zones. **Cost:** none.

### Lab 4.1 — Topology gaps break root cause

**Objective:** Show what a missing dependency costs the causal analysis.

```bash
python3 - <<'EOF'
# Observed dependency graph (what Smartscape built from real calls)
FULL = {
  "frontend":    ["checkout-api"],
  "checkout-api":["payments-api", "inventory-api", "postgres"],
  "payments-api":["vendor-gateway"],
  "inventory-api":["postgres", "redis"],
  "vendor-gateway":[],
  "postgres":[], "redis":[],
}
# The real fault
FAULTY = "vendor-gateway"

def root_cause(graph, degraded, faulty):
    """Walk down from degraded services; deepest reachable faulty node wins."""
    seen, stack, found = set(), list(degraded), []
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n)
        if n == faulty: found.append(n)
        stack.extend(graph.get(n, []))
    return found[0] if found else "UNKNOWN — blamed the topmost degraded service"

degraded = ["frontend", "checkout-api", "payments-api"]
print("Symptom: frontend, checkout-api and payments-api all degraded.\n")
print("--- complete topology ---")
print(f"  root cause: {root_cause(FULL, degraded, FAULTY)}   (correct)")

# Now: vendor-gateway was never instrumented, so the edge does not exist
PARTIAL = {k: [d for d in v if d != "vendor-gateway"] for k, v in FULL.items()}
del PARTIAL["vendor-gateway"]
print("\n--- topology missing vendor-gateway (never instrumented) ---")
print(f"  root cause: {root_cause(PARTIAL, degraded, FAULTY)}")
print("  -> the analysis blames payments-api: the deepest node it CAN see.")

print("\nThis is the failure mode that matters about causal AI:")
print("  it does not report low confidence when the topology is incomplete.")
print("  it reasons correctly over the graph it has, and returns a confident,")
print("  well-argued, WRONG answer — pointing a team at code that is fine.")
print("\nTopology completeness is therefore a precondition for trusting root cause,")
print("which is why Chapter 02's inventory reconciliation is not optional hygiene.")
EOF
```

**Expected result:** With the full graph the root cause is `vendor-gateway`; with the uninstrumented gateway missing, the analysis confidently blames `payments-api`. The insight is about the *shape* of the failure — causal analysis degrades into a confident wrong answer rather than an admission of uncertainty, so an incomplete topology is more dangerous than no topology at all.

**Negative test:** Trusting root-cause attribution in an estate you have not reconciled. The answer will look authoritative either way.

**Cleanup:** None.

### Lab 4.2 — Rule-based tags versus manual tags

**Objective:** Model how each behaves as the estate grows.

```bash
python3 - <<'EOF'
import random
random.seed(11)
RULES = [
  ("zone:pci",     lambda h: h["name"].startswith("pci-")),
  ("env:prod",     lambda h: "-prod-" in h["name"]),
  ("env:staging",  lambda h: "-stg-" in h["name"]),
  ("team:payments",lambda h: h.get("k8s_ns") == "payments"),
]
def gen(n, start=0):
    out = []
    for i in range(start, start + n):
        kind = random.choice(["pci-app-prod", "web-prod", "api-stg", "job-prod"])
        ns   = random.choice(["payments", "search", "core"])
        out.append({"name": f"{kind}-{i:03d}", "k8s_ns": ns})
    return out

hosts = gen(40)
manual = {h["name"]: {"env:prod"} for h in hosts if "-prod-" in h["name"]}   # applied by hand, today

def rule_tags(h): return {t for t, f in RULES if f(h)}

print(f"day 1: {len(hosts)} hosts")
r_cov = sum(1 for h in hosts if rule_tags(h)) / len(hosts) * 100
m_cov = sum(1 for h in hosts if manual.get(h['name'])) / len(hosts) * 100
print(f"   rule-based coverage : {r_cov:5.1f}%")
print(f"   manual coverage     : {m_cov:5.1f}%")

new = gen(60, start=40)                     # the estate grows; nobody revisits the manual tags
hosts += new
print(f"\nday 90: {len(hosts)} hosts ({len(new)} new, tagged by nobody)")
r_cov = sum(1 for h in hosts if rule_tags(h)) / len(hosts) * 100
m_cov = sum(1 for h in hosts if manual.get(h['name'])) / len(hosts) * 100
print(f"   rule-based coverage : {r_cov:5.1f}%   (rules applied themselves)")
print(f"   manual coverage     : {m_cov:5.1f}%   (decayed — no one tagged the new hosts)")

untagged_pci = [h["name"] for h in new if h["name"].startswith("pci-") and not manual.get(h["name"])]
print(f"\n{len(untagged_pci)} new PCI hosts carry NO manual tag.")
print("If the PCI management zone were built on manual tags, those hosts would sit")
print("OUTSIDE the compliance scope — invisible to the zone, and invisible in the")
print("audit that asks 'is everything in scope covered?'. The zone would look complete.")
print("\nRule-based tagging is not tidiness. It is the difference between a control")
print("that holds as the estate changes and one that silently stops holding.")
EOF
```

**Expected result:** Rule coverage holds as the estate grows from 40 to 100 hosts while manual coverage decays sharply, stranding new PCI hosts outside the zone. The compliance framing is the real lesson — a manually-tagged scope does not report itself as incomplete, so the audit sees a zone that looks fully populated.

**Negative test:** Bootstrapping a management zone with manual tags "just to get started." The zone will be wrong within a quarter, and nothing will announce it.

**Cleanup:** None.

### Lab 4.3 — Filtering is not access control

**Objective:** Separate what a user sees from what a user may see.

```bash
python3 - <<'EOF'
ENTITIES = [
  ("pci-db-prod-01",  "zone:pci"),
  ("pci-app-prod-02", "zone:pci"),
  ("web-prod-11",     "zone:general"),
  ("search-prod-04",  "zone:general"),
  ("hr-payroll-01",   "zone:restricted-hr"),
]
USERS = {
  "alice (platform)": {"zones": {"zone:pci","zone:general","zone:restricted-hr"}},
  "bob (app team)":   {"zones": {"zone:general"}},
  "carol (auditor)":  {"zones": {"zone:pci"}},
}
def visible(user, ui_filter=None):
    allowed = [e for e, z in ENTITIES if z in USERS[user]["zones"]]
    return [e for e in allowed if not ui_filter or dict(ENTITIES)[e] == ui_filter]

print("PERMISSIONS (management zones) — a real boundary:")
for u in USERS:
    print(f"   {u:20} can access {len(visible(u))}/{len(ENTITIES)}: {', '.join(visible(u))}")

print("\nUI FILTER — cosmetic. Alice filters to zone:general:")
f = visible("alice (platform)", "zone:general")
print(f"   alice now SEES  {len(f)}: {', '.join(f)}")
print(f"   alice can still ACCESS {len(visible('alice (platform)'))} — she clears the filter and they return.")

print("\nBob attempts the same filter trick in reverse (tries to view PCI):")
b = visible("bob (app team)", "zone:pci")
print(f"   bob sees {len(b)} entities: {b if b else '(nothing — permission, not preference)'}")

print("\nThe distinction, stated plainly:")
print("   FILTER      changes what you are LOOKING AT      -> convenience")
print("   PERMISSION  changes what you are ALLOWED to see  -> control")
print("\nAnyone who can remove a filter was never restricted by it. Scoping an auditor,")
print("a contractor, or a regulated environment with UI filters produces a screenshot")
print("that looks compliant and a system that is not.")
EOF
```

**Expected result:** Alice's filter hides entities she can still reach, while Bob's attempt returns nothing because permissions — not preference — bound him. The closing contrast is the one to carry into design reviews: a control that the controlled party can switch off is not a control.

**Negative test:** Demonstrating "restricted access" by showing a filtered dashboard. The demonstration proves nothing about what the account can reach.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Entities, stable entity IDs, and observed-not-declared Smartscape topology explained.
- [ ] Topology completeness understood as a precondition for trustworthy root cause.
- [ ] Rule-based tagging preferred over manual, with the compliance consequence stated.
- [ ] Management-zone permissions distinguished from UI filtering.
