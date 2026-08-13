# Chapter 08: TotalCloud and EDR

## Learning Objectives

- Assess cloud posture with TotalCloud (CSPM/CNAPP).
- Detect cloud misconfigurations and toxic combinations.
- Detect and respond to endpoint threats with Qualys EDR.
- Correlate the same-agent detection and response.
- Complete a walkthrough for each TotalCloud/EDR topic.

## Theory and Architecture

Two products extend Qualys into cloud and endpoint threats. **TotalCloud** is Qualys's **cloud
security** (CSPM/CNAPP) offering — it assesses **cloud posture** across AWS/Azure/GCP for
**misconfigurations** (public storage, over-permissive IAM, unencrypted data, open security groups),
scans **cloud workloads** for vulnerabilities, and identifies **toxic combinations** (attack paths
where a public workload, a critical vulnerability, and an over-privileged role together create real
risk). **Qualys EDR (Endpoint Detection and Response)** uses the **same Cloud Agent** to detect
malicious activity on endpoints — suspicious processes, persistence, lateral movement, known-bad
indicators — and to **respond** (isolate a host, kill a process, collect forensics), correlating with
the vulnerability and asset context Qualys already holds. The advantage of both is **unification**:
cloud posture and endpoint threats share the same platform, agent, and inventory as vulnerability and
compliance data, so risk is seen in one place. This chapter teaches each with a hands-on defensive
walkthrough (cloud misconfig, attack paths, and endpoint detection/response).

## Design Considerations

Assess cloud against **benchmarks** and hunt **toxic combinations**, not single misconfigs. Prioritize
**internet-exposed** cloud risk. For EDR, tune detections and define **response** actions (isolate/
kill/collect). Leverage the **same agent** so EDR detections carry vulnerability/asset context. Unify
the risk view.

## Implementation and Automation

The labs check cloud posture, find a toxic combination, and detect/respond on an endpoint.

## Validation and Troubleshooting

Confirm the TotalCloud/EDR model:

```text
TotalCloud = cloud CSPM/CNAPP: misconfig detection (public storage/over-permissive IAM/open SG) + workload vuln scan + toxic combinations (attack paths). Qualys EDR = same Cloud Agent detects endpoint threats (process/persistence/lateral/IOC) + responds (isolate/kill/collect), with vuln + asset context.
Advantage: unified platform/agent/inventory.
```

Common pitfalls: single cloud misconfigs in **isolation** (missing toxic combinations); and EDR
alerts with **no response** action.

## Security and Best Practices

Assess cloud against **CIS benchmarks**, prioritize **toxic combinations** and internet-exposed risk,
and give **EDR** tuned detections and **response** actions. Use the same-agent context. All work is
defensive.

## Hands-On Lab

TotalCloud/EDR walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 8.1 — Check cloud posture (CSPM)

**Objective:** Detect cloud misconfigurations.

```python
python3 - <<'PY'
resources=[{"type":"s3","public":True},{"type":"iam_key","age_days":500,"unused":True},
           {"type":"sg","open":"0.0.0.0/0:3389"}]
findings=[]
for r in resources:
    if r.get("public"): findings.append(f"{r['type']} public")
    if r.get("unused") and r.get("age_days",0)>90: findings.append(f"{r['type']} stale unused")
    if r.get("open"): findings.append(f"{r['type']} RDP open to world")
print("TotalCloud misconfigurations:", findings)
PY
```

**Expected result:** the cloud **misconfigurations** flagged — TotalCloud CSPM.

**Negative test:** assume the cloud provider secures your config; the **customer** owns it — assess
posture.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.2 — Find a toxic combination

**Objective:** Identify a cloud attack path.

```python
python3 - <<'PY'
workload={"public":True,"critical_vuln":True,"role":"admin","has_data":True}
toxic = workload["public"] and workload["critical_vuln"] and workload["role"]=="admin"
print("workload:", workload)
print("verdict:", "TOXIC COMBINATION -> public + critical vuln + admin role = attack path (top priority)" if toxic else "lower risk")
PY
```

**Expected result:** the **toxic combination** surfaced as top priority — TotalCloud attack-path
analysis.

**Negative test:** rank each misconfig alone; the dangerous **combination** is missed — analyze attack
paths.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.3 — Detect an endpoint threat (EDR)

**Objective:** Spot malicious activity.

```python
python3 - <<'PY'
event={"host":"pc-42","process":"powershell.exe","cmdline":"-enc <base64> downloadstring","parent":"winword.exe",
       "indicators":["office-spawns-powershell","encoded-command","network-download"]}
suspicious=len(event["indicators"])>=2
print("EDR event:", event["process"], "from", event["parent"])
print("verdict:", "MALICIOUS (office -> encoded PowerShell download) -> respond" if suspicious else "benign")
PY
```

**Expected result:** the Office-spawns-encoded-PowerShell chain flagged **malicious** — EDR detection.

**Negative test:** alert only on known malware hashes; **behavioral** chains (living-off-the-land) evade
that — detect behavior.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.4 — Respond to an endpoint threat

**Objective:** Contain and investigate.

```python
python3 - <<'PY'
response={"isolate host":"cut network except to Qualys","kill process":"powershell.exe (pid 4120)",
          "collect":"process tree + artifacts for forensics","context":"host has 3 critical vulns (same agent)"}
for action,detail in response.items(): print(f"{action:14}: {detail}")
print("Qualys EDR: same agent responds + carries vulnerability/asset context")
PY
```

**Expected result:** an EDR **response** (isolate/kill/collect) with vulnerability context — same-agent
response.

**Negative test:** detect but take **no action**; the threat continues — define automatic/analyst
response.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

TotalCloud assesses cloud posture and toxic combinations (CSPM/CNAPP), and Qualys EDR uses the same
Cloud Agent to detect and respond to endpoint threats with vulnerability/asset context — unifying
cloud and endpoint into the platform.

- [ ] I can check cloud posture (CSPM).
- [ ] I can find a toxic combination.
- [ ] I can detect an endpoint threat (EDR).
- [ ] I can respond to an endpoint threat.
- [ ] I completed Labs 8.1–8.4 including each negative test.
