# Chapter 02: CNAPP and the Wiz Security Graph

## Learning Objectives

- Explain what CNAPP consolidates and why the category exists.
- Understand the Wiz Security Graph as the unifying model beneath the pillars.
- Describe agentless scanning — how Wiz sees the cloud without agents.
- Recognize why a graph beats a list of findings.

*Cert relevance: the Security Graph and agentless model are foundational to **every** Wiz exam — Cloud Fundamentals assumes you understand them.*

## What CNAPP consolidates

Cloud security used to be a drawer of separate tools, each with its own console and its own list:

| Acronym | Tool | Answers |
|:---|:---|:---|
| **CSPM** | Cloud Security Posture Management | Are my cloud *configurations* secure? |
| **CWPP** | Cloud Workload Protection Platform | Are my *workloads* (VMs, containers) safe? |
| **CIEM** | Cloud Infrastructure Entitlement Management | Who can *do what* (identities and permissions)? |
| **DSPM** | Data Security Posture Management | Where is my *sensitive data* and is it exposed? |

**CNAPP** (Cloud-Native Application Protection Platform) is the consolidation of all of these into one platform. The reason the category exists is not just "fewer tools" — it is that **risk lives in the connections between these domains**, and separate tools cannot see the connections. A misconfiguration (CSPM) is not very interesting alone; a misconfiguration *on a workload with a critical vulnerability* (CWPP) *whose identity can reach a database of customer data* (CIEM + DSPM) is a breach waiting to happen. Only a platform that holds all four domains at once can see that.

## The Security Graph

Wiz's answer to "hold all four at once" is the **Wiz Security Graph**: a graph where the **nodes** are cloud resources (VMs, containers, buckets, identities, databases, functions) and the **edges** are their relationships (this VM *runs* that container; this role *can assume* that role; this identity *can read* that bucket; this workload *is exposed to* the internet).

Once the cloud is a graph, security questions become **graph queries**:

- "Show me every internet-exposed resource that can reach sensitive data" — a path query.
- "What can this compromised identity actually access?" — a reachability query.
- "Which vulnerabilities are on internet-facing workloads with high privilege?" — a filtered traversal.

This is the difference between a **list** and a **graph**. A list says "you have 8,000 vulnerabilities." A graph says "6 of those 8,000 are on a path from the internet to your crown jewels — fix these 6 first." The lab makes that difference concrete.

## Agentless scanning

The second Wiz foundation is **agentless scanning**. Traditional workload security requires deploying an **agent** on every VM and container — which means coverage gaps (the workloads without agents are invisible), deployment friction, and performance overhead. Wiz's original differentiator was to scan **agentlessly**: it takes point-in-time **snapshots** of workloads through the cloud provider's APIs and analyzes them out-of-band, needing no agent on the workload.

The consequence is **complete coverage on day one**: every workload in the account is visible because visibility comes from the cloud API, not from whether someone remembered to install an agent. (Wiz Defend adds an *optional* lightweight runtime sensor for real-time detection — Chapter 7 — but posture is agentless.) The lab models why agentless coverage beats agent-based coverage across a real fleet.

## Hands-On Lab

Python models the graph and agentless coverage. **Cost:** none.

### Lab 2.1 — A graph finds what a list cannot

**Objective:** See why relationships, not counts, surface real risk.

```bash
python3 - <<'EOF'
# a tiny cloud as a graph: nodes + edges (relationships)
edges = {
  "internet":   ["web-vm"],
  "web-vm":     ["app-role"],          # web-vm uses app-role
  "app-role":   ["data-bucket"],       # app-role can read data-bucket
  "data-bucket":["<CROWN JEWELS: PII>"],
  "batch-vm":   ["batch-role"],        # isolated, no path to data
  "batch-role": [],
}
# findings (the "list" a legacy tool emits)
findings = {
  "web-vm":   ["critical CVE (RCE)", "internet-exposed"],
  "batch-vm": ["critical CVE (RCE)"],
  "data-bucket": ["contains PII"],
  "old-vm-1": ["medium CVE"], "old-vm-2": ["low CVE"], "old-vm-3": ["low CVE"],
}
total = sum(len(v) for v in findings.values())
print(f"THE LIST (legacy tool): {total} findings across the estate. Where do you start?")
for n, fs in findings.items():
    print(f"   {n:12} {fs}")

def reaches_crown(node, seen=None):
    seen = seen or set()
    if node in seen: return False
    seen.add(node)
    for nxt in edges.get(node, []):
        if "CROWN JEWELS" in nxt or reaches_crown(nxt, seen): return True
    return False

print("\nTHE GRAPH (Wiz): which findings are on a PATH from the internet to PII?")
path_nodes = [n for n in edges if n != "internet" and reaches_crown(n)]
attack_path = [n for n in ["web-vm","app-role","data-bucket"] ]
print(f"   internet -> {' -> '.join(attack_path)} -> PII")
print("   the RCE on web-vm is internet-exposed AND its role reaches the PII bucket.")
print("   => 1 attack path. FIX web-vm's CVE first.")
print("\n   batch-vm has the SAME critical CVE — but its role reaches NOTHING sensitive.")
print("   same severity, RADICALLY different risk. The list can't tell them apart;")
print("   the graph can.")
print(f"\nList view: {total} findings, no priority. Graph view: 1 attack path, obvious")
print("first move. This is CNAPP's whole reason to exist — risk lives in the EDGES")
print("(exposure + vuln + privilege + data), and only a graph holds all four at once.")
EOF
```

**Expected result:** Two workloads with the identical critical CVE ranked completely differently because only one sits on a graph path from the internet to sensitive data. The list-versus-graph lesson is CNAPP's reason to exist — severity alone cannot prioritize, because risk lives in the relationships, and only a graph holding configuration, workload, identity, and data at once can find the exploitable path.

**Negative test:** Prioritizing by severity count alone. Both VMs show a "critical CVE," so a list treats them equally and you may fix the harmless one first — the graph shows only one is on a path to the crown jewels.

**Cleanup:** None.

### Lab 2.2 — Agentless coverage versus agent gaps

**Objective:** Quantify why agentless sees what agents miss.

```bash
python3 - <<'EOF'
import random
random.seed(14)
FLEET = 2000
# agent-based: coverage depends on whether an agent got installed
# reality: shadow IT, short-lived workloads, unsupported OSes, forgotten installs
agent_installed = [random.random() < 0.78 for _ in range(FLEET)]   # ~78% coverage typical
covered_agent = sum(agent_installed)
# agentless: visibility from the cloud API -> every workload the account knows about
covered_agentless = FLEET

print(f"cloud account: {FLEET} workloads (some short-lived, some shadow IT, mixed OS)\n")
print("AGENT-BASED workload security:")
print(f"   agents installed on {covered_agent}/{FLEET} = {100*covered_agent/FLEET:.0f}% coverage")
blind = FLEET - covered_agent
print(f"   {blind} workloads have NO agent -> INVISIBLE. A critical vuln on any of")
print(f"   those {blind} is simply not seen. And the blind ones are often the risky")
print("   ones (shadow IT, unmanaged, short-lived) that no one installed an agent on.\n")
print("AGENTLESS (Wiz snapshots via cloud API):")
print(f"   {covered_agentless}/{FLEET} = 100% coverage on DAY ONE — visibility comes from")
print("   the cloud API, not from whether someone installed an agent.")
print(f"\n   coverage gap closed: {blind} previously-invisible workloads")
print("\nWhy this matters: security coverage that depends on AGENT INSTALLATION has a")
print("hole exactly where you can't see it — the workloads without agents. Agentless")
print("scanning reads the cloud provider's APIs and snapshots workloads out-of-band,")
print("so EVERYTHING the account contains is in scope automatically. No deployment")
print("project, no per-workload friction, no 'we thought that was covered.'")
print("\n(Wiz Defend adds an OPTIONAL runtime sensor for real-time detection — Ch 7 —")
print("but POSTURE is agentless, which is why Wiz sees the whole estate from day one.)")
EOF
```

**Expected result:** Agent-based security covering roughly three-quarters of the fleet while agentless covers 100% from day one, closing the gap exactly where the unmanaged, riskier workloads live. The agentless lesson is coverage-by-default — visibility from the cloud API means every workload is in scope automatically, with no deployment project and no blind spots where an agent was never installed.

**Negative test:** Trusting agent-based coverage numbers. "78% covered" hides that the 22% without agents — often shadow IT and short-lived workloads — are invisible, and a critical vulnerability on any of them is simply never seen.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] CNAPP understood as the consolidation of CSPM, CWPP, CIEM, and DSPM — because risk lives in the connections between them.
- [ ] The Wiz Security Graph understood as nodes (resources) and edges (relationships) turning security questions into graph queries.
- [ ] Agentless scanning understood as snapshot-based, cloud-API visibility with complete day-one coverage.
- [ ] The graph-beats-a-list principle internalized — relationships surface real risk that severity counts cannot.
