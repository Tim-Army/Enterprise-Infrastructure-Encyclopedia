# Chapter 06: TrueFort

## Learning Objectives

- Explain TrueFort's application- and identity-centric segmentation.
- Explain how TrueFort leverages existing EDR agents.
- Reason about behavior baselining and service-account protection.
- State the pros, cons, compatibility, and requirements.
- Complete a walkthrough for each TrueFort topic.

## Theory and Architecture

**TrueFort** approaches microsegmentation from the **application and identity** side rather than the
network. Its distinguishing move is to **leverage existing EDR agents** — **CrowdStrike Falcon** and
**SentinelOne** — for telemetry and enforcement, so organizations that already run those agents can add
segmentation **without deploying a new agent** (TrueFort also offers its own agent). Policies are built
on **application intelligence**: TrueFort profiles each workload's **network, identity, process, and
application behavior**, uses **machine learning** to establish a trusted **baseline**, and enforces
against that profile — so a policy is "this application, run by this service account, may make these
process-and-network behaviors," not merely "this IP may reach that port." This makes it strong at
**service-account protection** and at catching **lateral movement and supply-chain** attacks that
IP/port-based segmentation misses.

## Pros, Cons, Compatibility, and Requirements

- **Pros:** can **reuse existing EDR agents** (CrowdStrike/SentinelOne) — no new agent to deploy where
  those exist; **application/identity/process-aware** (L7-ish behavior, not just IP/port); **service
  -account** protection; behavior baselining detects and blocks anomalous lateral movement and
  supply-chain activity; workload-portable.
- **Cons:** requires a **supported EDR** or the TrueFort agent to be present; **workload/server-focused**
  (not designed for network gear or agentless OT primarily); behavior modeling requires a baseline period
  and tuning.
- **Compatibility:** workloads with **CrowdStrike Falcon** or **SentinelOne** (telemetry/enforcement), or
  the TrueFort agent; Windows/Linux servers and cloud workloads.
- **Requirements:** a supported EDR deployment **or** the TrueFort agent; the TrueFort platform/console;
  a baseline period for behavior learning.

## Design Considerations

TrueFort is a strong fit where you **already run CrowdStrike or SentinelOne** and want to add
application/identity-aware segmentation and **service-account** control without another agent. Lean on
its **behavior baselining** for workloads where process/identity context matters (finance, PCI, service
accounts). Give it a **baseline window** and tune before enforcing. For network devices and agentless
OT/IoT, pair it with a network or appliance model (Chapters 03, 07).

## Implementation and Automation

The labs model EDR-leveraged deployment, an application/identity behavior policy, and service-account
protection — the TrueFort option in the rubric.

## Validation and Troubleshooting

Confirm the TrueFort model:

```text
Telemetry/enforcement: reuse existing EDR (CrowdStrike Falcon / SentinelOne) or TrueFort agent
Policy on application intelligence: network + identity + PROCESS + behavior (ML baseline), not just IP/port
Strengths: service-account protection; detect/block lateral movement + supply-chain
Requires: a supported EDR OR the TrueFort agent; baseline period; workload/server-focused
```

Common pitfalls: expecting TrueFort to segment hosts with **no EDR and no TrueFort agent** (nothing to
enforce with); and enforcing behavior policy before the **baseline** is representative.

## Security and Best Practices

Application/identity/behavior policy contains attacks that IP/port rules miss — especially service
-account abuse and living-off-the-land lateral movement. Protect the TrueFort console and the EDR
integration. Baseline, tune, then enforce. All work is authorized administration.

## Hands-On Lab

TrueFort walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 6.1 — Model EDR-leveraged deployment

**Objective:** Segment using an agent you already run.

```python
python3 - <<'PY'
fleet = {
  "srv-a": {"edr":"CrowdStrike"}, "srv-b": {"edr":"SentinelOne"},
  "srv-c": {"edr":None, "truefort_agent":True}, "srv-d": {"edr":None, "truefort_agent":False},
}
for host, cfg in fleet.items():
    if cfg.get("edr") in ("CrowdStrike","SentinelOne"):
        print(f"{host}: enforce via existing {cfg['edr']} (no new agent)")
    elif cfg.get("truefort_agent"):
        print(f"{host}: enforce via TrueFort agent")
    else:
        print(f"{host}: NO enforcement path -> add EDR or TrueFort agent")
PY
```

**Expected result:** hosts with CrowdStrike/SentinelOne segmented via the existing EDR; the bare host
flagged as needing an agent.

**Negative test:** assume every host is covered; `srv-d` has no EDR and no TrueFort agent — it needs one
to be enforced.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Model an application/identity behavior policy

**Objective:** Enforce on behavior, not just IP/port.

```python
python3 - <<'PY'
baseline = {"app":"payments","svc_account":"svc_pay","allowed_child":"java",
            "allowed_dst":[("db01","tcp/5432")]}
def check(app, account, child, dst):
    ok = (app==baseline["app"] and account==baseline["svc_account"]
          and child==baseline["allowed_child"] and dst in baseline["allowed_dst"])
    return "ALLOW" if ok else "BLOCK (deviates from baseline)"
print(check("payments","svc_pay","java",("db01","tcp/5432")))       # normal
print(check("payments","svc_pay","powershell",("db01","tcp/5432"))) # unexpected child process
print(check("payments","svc_pay","java",("evilhost","tcp/443")))    # unexpected destination
PY
```

```text
ALLOW
BLOCK (deviates from baseline)
BLOCK (deviates from baseline)
```

**Expected result:** the normal application behavior allowed; an unexpected child process or destination
blocked — behavior-aware segmentation.

**Negative test:** allow the payments service account to spawn any process to any host on tcp/443;
IP/port rules miss the malicious child process — enforce on **behavior**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Model service-account protection

**Objective:** Confine a service account to its purpose.

```python
python3 - <<'PY'
svc = {"account":"svc_backup","allowed":[("bkp01","tcp/445")], "should_never":[("dc01","tcp/3389")]}
attempts = [("bkp01","tcp/445"), ("dc01","tcp/3389")]
for dst in attempts:
    verdict = "ALLOW" if dst in svc["allowed"] else "BLOCK"
    flag = "  <- lateral-movement attempt" if dst in svc["should_never"] else ""
    print(f"svc_backup -> {dst}: {verdict}{flag}")
PY
```

**Expected result:** the backup service account allowed only to its backup target; an RDP-to-DC attempt
blocked — service-account containment.

**Negative test:** let a service account authenticate anywhere it has credentials; confine it to its
**intended** flows so stolen service creds cannot roam.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.4 — Score TrueFort against the rubric

**Objective:** Place it in the comparison.

```python
python3 - <<'PY'
weights = {"coverage":0.25,"visibility":0.15,"automation":0.15,"granularity":0.10,
           "scale":0.10,"failure_mode":0.05,"compliance":0.10,"tco":0.10}
scores  = {"coverage":3,"visibility":5,"automation":4,"granularity":5,   # process/identity granularity
           "scale":4,"failure_mode":3,"compliance":4,"tco":4}            # low TCO if EDR already present
total = sum(weights[k]*scores[k] for k in weights)
print(f"TrueFort weighted score: {total:.2f}/5 (strengths: visibility, process/identity granularity)")
PY
```

**Expected result:** a weighted score highlighting visibility and process/identity granularity — its
comparative strengths.

**Negative test:** score its **coverage** as if it segmented OT/network gear; weight it on
**application/identity** enforcement where it leads.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

TrueFort does application- and identity-centric microsegmentation by leveraging existing CrowdStrike or
SentinelOne EDR agents (or its own), enforcing on machine-learned behavior baselines of network,
identity, process, and application activity — strong at service-account protection and catching lateral
movement and supply-chain attacks that IP/port rules miss, provided a supported EDR or its agent is
present.

- [ ] I can explain TrueFort's EDR-leveraged, application/identity model.
- [ ] I can model a behavior-based policy and service-account protection.
- [ ] I can state the pros, cons, compatibility, and requirements.
- [ ] I completed Labs 6.1–6.4 including each negative test.
