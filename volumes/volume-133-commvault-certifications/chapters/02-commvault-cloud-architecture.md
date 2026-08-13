# Chapter 02: Commvault Cloud Architecture

## Learning Objectives

- Describe the CommCell architecture: CommServe, MediaAgent, agents, and Command Center.
- Compare SaaS, self-managed software, and hybrid deployment models.
- Explain the control plane / data plane split and why it matters for resilience.
- Size and place MediaAgents for throughput and availability.

## The CommCell

Commvault's architecture has been stable in shape for a long time, which is why its vocabulary persists across the modern **Commvault Cloud** branding. A **CommCell** is one managed environment, comprising:

| Component | Role |
|:---|:---|
| **CommServe** | The **control plane**: the brain holding configuration, schedules, job history, and the index of what was protected. One per CommCell. |
| **MediaAgent** | The **data plane**: moves data from source to storage, owns the deduplication database, and mounts storage libraries. |
| **Agent (iDataAgent)** | The client-side component that understands a specific workload (SQL, VMware, file system, M365). |
| **Command Center** | The web console — the administrative interface for policies, jobs, restores, and reporting. |
| **Storage library** | Where the data lands: disk, cloud object storage, or tape. |

The critical architectural property is the **control plane / data plane split**. The CommServe knows *what* was protected and *where it is*; the MediaAgents actually move and store it. This matters enormously for resilience: **losing the CommServe means losing the catalog**, and without the catalog you have backup data you cannot efficiently find or restore. Protecting the CommServe database is therefore not routine housekeeping — it is the precondition for every recovery.

## Deployment models

| Model | Who runs the control plane | Typical driver |
|:---|:---|:---|
| **SaaS** (Commvault Cloud) | Commvault | Speed to deploy; no infrastructure to maintain; SaaS workloads |
| **Software (self-managed)** | You | Data sovereignty, existing investment, air-gapped or regulated environments |
| **Hybrid** | Both | On-premises estate plus cloud/SaaS workloads under one strategy |

The certifications span all three — the Readiverse workload courses are explicitly labeled "Commvault Cloud SaaS," while the Cloud Administrator and Cloud Engineer material covers the platform generally.

## Placement and sizing

MediaAgent placement is where architecture becomes performance:

- Put the MediaAgent **close to the data** — moving backup data across a WAN to a distant MediaAgent is the classic cause of missed backup windows.
- Size for **concurrent streams** and the deduplication database's I/O profile (the DDB wants fast, low-latency storage — Chapter 04).
- Deploy **more than one MediaAgent** for any workload that cannot tolerate a single point of failure, and remember that the DDB is tied to its MediaAgent.

## Hands-On Lab

Python models the architecture. **Cost:** none.

### Lab 2.1 — Model the control plane / data plane split

**Objective:** Show why the catalog is the critical dependency.

```bash
python3 - <<'EOF'
commcell = {
  "CommServe": {"role":"control plane", "holds":["configuration","schedules","job history","index/catalog"]},
  "MediaAgent-01": {"role":"data plane", "holds":["dedup database","storage mounts"], "streams":50},
  "MediaAgent-02": {"role":"data plane", "holds":["dedup database","storage mounts"], "streams":50},
}
def impact(component_down):
    if component_down == "CommServe":
        return ("CRITICAL: no catalog -> no scheduling, no job control, and restores cannot be located "
                "efficiently. Backup DATA survives, but findability does not.")
    return (f"DEGRADED: {component_down} offline -> its streams and its dedup database are unavailable; "
            "other MediaAgents continue. Jobs bound to it fail until it returns.")

for c in ["CommServe","MediaAgent-01"]:
    print(f"{c} down -> {impact(c)}\n")
print("Design rule: protect the CommServe database like production data — it IS the recovery capability.")
EOF
```

**Expected result:** Losing a MediaAgent is degradation; losing the CommServe is a categorically different failure, because the catalog is what makes backup data *recoverable* rather than merely *stored*. This is the reason CommServe protection (and CommServe disaster recovery backups) is a first-order design task rather than an afterthought.

**Negative test:** Treating the CommServe as "just another server" with ordinary backups — in a site-loss scenario you restore the data but cannot efficiently identify or index it, which turns a recovery into an archaeology project.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — Choose a deployment model

**Objective:** Match the model to the constraint.

```bash
python3 - <<'EOF'
def choose(data_sovereignty, has_infra_team, workloads, speed_priority):
    if data_sovereignty and not speed_priority:
        return "SOFTWARE (self-managed) — you keep the control plane and the data in your jurisdiction"
    if workloads == "saas-only" and speed_priority:
        return "SaaS (Commvault Cloud) — fastest to protect M365/Salesforce-type workloads"
    if workloads == "mixed":
        return "HYBRID — SaaS for cloud/SaaS workloads, self-managed for the on-prem estate"
    return "SaaS — least operational burden"

cases = [
  ("Regulated bank, EU data residency", True,  True,  "mixed",     False),
  ("Startup, M365 + Salesforce only",   False, False, "saas-only", True),
  ("Enterprise, DC + cloud",            False, True,  "mixed",     False),
]
for name, *args in cases:
    print(f"{name:36} -> {choose(*args)}")
EOF
```

**Expected result:** Sovereignty pushes toward self-managed software, SaaS-only estates toward Commvault Cloud SaaS, and mixed estates toward hybrid. The decision is driven by **where the data must live and who operates the control plane**, not by feature lists — the protection capabilities are broadly common across models.

**Negative test:** Choosing SaaS for a workload whose data cannot legally leave a jurisdiction — a compliance failure that no amount of encryption configuration retroactively fixes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Place and size MediaAgents

**Objective:** Avoid the classic WAN-backup mistake.

```bash
python3 - <<'EOF'
sites = [
  {"site":"DC-1","data_tb":40,"mediaagent_local":True, "link_mbps":10000},
  {"site":"Branch-A","data_tb":5,"mediaagent_local":False,"link_mbps":100},
  {"site":"Cloud-AWS","data_tb":20,"mediaagent_local":True,"link_mbps":10000},
]
WINDOW_HOURS = 8
for s in sites:
    # crude throughput model: TB over the link within the backup window
    capable_tb = (s["link_mbps"]/8) * 3600 * WINDOW_HOURS / 1_000_000
    ok = s["mediaagent_local"] or capable_tb >= s["data_tb"]
    print(f"{s['site']:10} {s['data_tb']:>3} TB  local MA={str(s['mediaagent_local']):5} "
          f"link={s['link_mbps']:>5} Mbps  window-capacity={capable_tb:6.1f} TB  -> {'OK' if ok else 'MISSES WINDOW'}")
print("\nFix for Branch-A: put a MediaAgent local to the data, then replicate deduplicated copies over the WAN.")
EOF
```

**Expected result:** The two sites with local MediaAgents are fine, while Branch-A — 5 TB over a 100 Mbps link in an 8-hour window — **misses the window**, because the link can carry only about 0.36 TB in that time. The remedy is architectural: back up locally, then send the *deduplicated, incremental* copy over the WAN. Moving full backup data across a thin link is the most common capacity mistake in distributed deployments.

**Negative test:** Solving a missed window by extending it — the window exists because the business needs the systems back; a 20-hour backup on an 8-hour window is not a scheduling problem, it is a placement problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CommCell components (CommServe, MediaAgent, agents, Command Center, libraries) described.
- [ ] Control plane / data plane split understood, and the CommServe catalog identified as critical.
- [ ] SaaS, software, and hybrid deployment models matched to their drivers.
- [ ] MediaAgent placement sized against the backup window.
