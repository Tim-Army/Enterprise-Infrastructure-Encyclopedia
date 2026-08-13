# Chapter 06: Telemetry, ADM, and Auto-Generated Policy

## Learning Objectives

- Describe the cluster-and-agent architecture and decide where agents go.
- Collect comprehensive flow telemetry, or the native equivalent.
- Perform Application Dependency Mapping to discover tiers and dependencies.
- Auto-generate a least-privilege policy from the discovery.

This is the core of the lab. Each exercise carries both tracks. Secure Workload's method is **collect everything, discover the application, generate the policy, then analyze and enforce** — you do not hand-write the rules, you discover them.

## Hands-On Lab

### Lab 6.1 — Architecture and agent placement

**Objective.** State what the cluster and agents do and decide which hosts get an agent.

**Background.** The **Secure Workload cluster** (an on-premises appliance or a SaaS tenant) is the analytics brain: it ingests flow and process telemetry, performs ADM, holds the scope tree and policy, and runs policy analysis. The **agent** on each workload reports telemetry and enforces policy by programming the **native host firewall** — `iptables` with `ipset` on Linux, the **Windows Filtering Platform** on Windows. A device that can run no agent (the PLC) is not managed directly; it is protected by policy on its managed neighbors (Chapter 08).

**Walkthrough.**

**Step 1.** Decide agent placement:

| Host | Agent? | Scope (illustrative) |
|:---|:---|:---|
| cw-app01 | Yes | `Default:DC:ILLab:Web` |
| cw-db01 | Yes | `Default:DC:ILLab:Database` |
| cw-win01 | Yes | `Default:DC:OT:HMI` |
| cw-gw | Yes | `Default:DC:Infra` |
| cw-ot01 | **No** | represented; protected from neighbors |

**Step 2.** Note that a **scope** is a hierarchical grouping used to organize workloads and delegate policy — the tree above is one branch of it.

**Expected result.** A per-host agent-and-scope plan.

**Negative test.** Plan to install the agent on `cw-ot01`. It cannot run one; the PLC appears in telemetry only as the far end of the HMI's flows, and is protected from its neighbors in Chapter 08.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Collect comprehensive telemetry

**Objective.** Gather the flow telemetry ADM needs — for real via agents, or natively.

**Track 1 — Real Secure Workload.** Install the enforcement agent on each host; confirm the cluster shows each workload reporting flows and process inventory. Leave enforcement off while telemetry accrues.

**Track 2 — Native equivalent.** Collect every flow that crosses the estate into a log ADM can read. On `cw-gw` (which sees all cross-segment traffic) and on the endpoints:

```bash
sudo apt -y install conntrack
# generate the legitimate traffic first:
#   on cw-app01: run ~/checkdb.sh a few times
#   on cw-win01: poll the PLC a few times
# then harvest the flows into a telemetry log (src,dst,dport):
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/\1,\2,\3/p' \
  | sort -u | tee ~/telemetry.csv
```

**Expected result.** A `telemetry.csv` of observed flows, for example `10.10.20.11,10.10.20.12,5432` and `10.10.20.21,10.10.30.50,502`. This is the raw material for ADM.

**Negative test.** Collect telemetry while the Lab 5.3 attack runs, and the attack flow (`10.10.20.21,10.10.20.12,5432`) lands in the log. ADM faithfully learns whatever it sees, so the collection window must observe clean traffic — and the result must be reviewed against ground truth.

**Rollback.** Keep the telemetry log.

### Lab 6.3 — Application Dependency Mapping and auto-generated policy

**Objective.** Discover the application's tiers and dependencies from the telemetry, and generate a least-privilege policy.

**Track 1 — Real Secure Workload.** Create a workspace over the relevant scope and run **ADM**. The cluster analyzes the flows, proposes **clusters** (tiers) of similar workloads, and generates a candidate policy — allow rules for the discovered dependencies (Web→Database:5432, HMI→PLC:502) with a default deny.

**Track 2 — Native equivalent.** Perform ADM by hand: cluster the workloads by role and emit a policy from the observed dependencies.

**Step 1.** Assign each address to a discovered tier (in real ADM this clustering is automatic from flow similarity; here you name them), then generate allow rules from the telemetry:

```bash
cat > ~/adm.sh <<'EOF'
#!/usr/bin/env bash
# Map addresses to discovered tiers
declare -A TIER=( [10.10.20.11]=Web [10.10.20.12]=Database [10.10.20.21]=HMI [10.10.30.50]=PLC )
echo "# Auto-generated policy (ADM) — default deny, allow discovered dependencies:"
while IFS=, read -r s d p; do
  echo "allow ${TIER[$s]:-Unknown}(${s}) -> ${TIER[$d]:-Unknown}(${d}) :${p}"
done < ~/telemetry.csv | sort -u
EOF
chmod +x ~/adm.sh
~/adm.sh
```

**Expected result.** A generated policy that mirrors the real dependencies, for example:

```text
allow Web(10.10.20.11) -> Database(10.10.20.12) :5432
allow HMI(10.10.20.21) -> PLC(10.10.30.50) :502
```

Compare it to the Chapter 05 ground truth: the two legitimate flows, and nothing else. Discovery produced the policy; you did not write it.

**Negative test.** If `allow HMI -> Database :5432` appears, your telemetry window captured the attack. Delete that rule before it becomes policy — ADM proposes, a human disposes.

**Rollback.** Keep the generated policy; Chapter 07 analyzes and enforces it.

## Summary and Completion Checklist

- [ ] Architecture and scopes understood; agent placement decided.
- [ ] Comprehensive flow telemetry collected (agents or `telemetry.csv`).
- [ ] ADM performed and a least-privilege policy auto-generated.
- [ ] The generated policy reviewed against the Chapter 05 ground truth.
