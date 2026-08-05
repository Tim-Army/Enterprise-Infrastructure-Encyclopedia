# Chapter 04: Agentless Posture — CSPM and Vulnerability Management

## Learning Objectives

- Explain cloud security posture management (CSPM) — misconfigurations against a baseline.
- Understand cloud vulnerability management without agents.
- Place configuration and vulnerability findings into the attack-path model.
- Recognize how compliance frameworks map onto posture.

*Cert relevance: CSPM and vulnerability management are core **Cloud Fundamentals** material — the posture half of Wiz Cloud.*

## CSPM: configuration posture

**Cloud Security Posture Management (CSPM)** answers "are my cloud configurations secure?" It continuously checks cloud resources against a **baseline** of secure-configuration rules — is this storage bucket public? is encryption enabled? is this security group open to `0.0.0.0/0`? is logging on? — and reports the ones that fail. The baseline draws from provider best practices and compliance frameworks (CIS benchmarks, PCI, SOC 2, HIPAA).

The important shift from legacy CSPM is that a Wiz misconfiguration is **a node in the graph, not a line in a list**. "This bucket is public" is a fact; "this public bucket contains PII and is reachable by an internet-exposed workload's role" is an *attack path* (Chapter 3). CSPM feeds the graph; the graph decides which misconfigurations are urgent. The lab models mapping raw misconfigurations to compliance and to path-risk.

## Vulnerability management, agentless

**Vulnerability management** answers "what known software flaws are in my workloads?" Wiz does this **agentlessly** (Chapter 2): it snapshots each workload's disk through the cloud API, inventories installed packages, and matches them against vulnerability databases — no agent, complete coverage. It finds the CVEs on every VM, container image, and function in the account.

But — the recurring theme — **a raw CVE list is noise until the graph contextualizes it.** Wiz enriches each vulnerability with: is the workload *running* (or a dormant image)? is it *internet-exposed*? does its identity have *privilege*? does it reach *sensitive data*? A CVE that is exploitable, on a running, exposed, privileged workload near data is urgent; the same CVE on a stopped image behind ten network hops is not. This is **validated, in-context prioritization** rather than raw CVSS. The lab models it.

## Compliance as a view of posture

Compliance frameworks (CIS, PCI DSS, SOC 2, HIPAA) are, to a CNAPP, **views of the same posture data**: each control maps to one or more configuration checks, and your "compliance score" is the fraction of controls passing across the estate. Because the checks are continuous, compliance becomes a **live posture** (like the CIS work in the [Jamf volume (CXLVI)](../../volume-146-jamf-certifications/chapters/08-jamf-school-and-compliance.md)) rather than an annual audit scramble — the same "compliance is a number you hold, not a report you run" discipline, applied to cloud.

## Hands-On Lab

Python models posture and vulnerability prioritization. **Cost:** none.

### Lab 4.1 — Misconfigurations to compliance, and to path-risk

**Objective:** Turn raw config findings into a compliance view and a risk view.

```bash
python3 - <<'EOF'
# raw CSPM findings across resources; each maps to compliance controls
FINDINGS = [
  # resource,        misconfig,                  controls,               on_attack_path
  ("bucket-public",  "public read enabled",      ["CIS-2.1","PCI-1.2"],  True),   # public + holds data
  ("sg-open-ssh",    "SSH open to 0.0.0.0/0",    ["CIS-4.1","PCI-1.3"],  True),   # exposure hop
  ("rds-no-encrypt", "encryption at rest off",   ["CIS-2.3","HIPAA-164"],False),
  ("no-flow-logs",   "VPC flow logs disabled",   ["CIS-3.9"],            False),
  ("iam-no-mfa",     "root without MFA",         ["CIS-1.5","SOC2-CC6"], False),
]
CONTROLS_TOTAL = 20  # pretend baseline has 20 controls
failing_controls = set()
for _, _, ctrls, _ in FINDINGS:
    failing_controls.update(ctrls)
print("RAW findings -> COMPLIANCE view (controls failing):")
for res, mis, ctrls, _ in FINDINGS:
    print(f"   {res:16} {mis:28} -> {', '.join(ctrls)}")
score = 100*(CONTROLS_TOTAL-len(failing_controls))/CONTROLS_TOTAL
print(f"   compliance score ~ {score:.0f}% ({len(failing_controls)}/{CONTROLS_TOTAL} controls failing)")

print("\nSAME findings -> RISK view (which are on an attack path?):")
on_path  = [f for f in FINDINGS if f[3]]
off_path = [f for f in FINDINGS if not f[3]]
for res, mis, _, _ in on_path:
    print(f"   URGENT (on path)   {res:16} {mis}")
for res, mis, _, _ in off_path:
    print(f"   fix in due course  {res:16} {mis}")
print("\nTwo lenses on ONE dataset:")
print("  COMPLIANCE view — every failing control matters for the AUDIT (fix them all")
print("     eventually); it's a live % across the estate, not a yearly scramble.")
print("  RISK view — bucket-public + sg-open-ssh are on an ACTIVE attack path")
print("     (exposure + reachable data), so they jump the queue over root-MFA and")
print("     flow-logs, which are real audit gaps but not part of a breach path today.")
print("\nCSPM feeds the graph; the graph decides urgency. A misconfiguration is a NODE,")
print("not just a checklist line — 'public bucket' becomes urgent when the graph shows")
print("it holds PII and an exposed role can reach it. Compliance AND risk, one posture.")
EOF
```

**Expected result:** The same misconfiguration findings viewed two ways — a compliance score across mapped controls, and a risk ranking by attack-path membership — with exposure-and-data findings jumping the queue over real-but-non-path audit gaps. The two-lens lesson is that CSPM feeds one posture that answers both the auditor (every failing control, as a live percentage) and the responder (which findings are on a breach path now).

**Negative test:** Working misconfigurations in compliance-ID order. Root-without-MFA is a serious audit finding but not on today's attack path, while the public bucket and open SSH form a live exposure — risk context, not control numbering, sets the order.

**Cleanup:** None.

### Lab 4.2 — In-context vulnerability prioritization

**Objective:** Rank CVEs by graph context, not raw CVSS.

```bash
python3 - <<'EOF'
# same CVE (CVSS 9.8 RCE) on different workloads; context decides urgency
WORKLOADS = [
  # name,          running, internet_exposed, high_priv, reaches_data
  ("web-api",       True,   True,   True,   True),    # every amplifier -> URGENT
  ("stopped-image", False,  False,  False,  False),   # dormant -> low
  ("internal-tool", True,   False,  True,   False),   # running+priv, not exposed
  ("dmz-proxy",     True,   True,   False,  False),   # exposed, but low priv/no data
]
def risk_score(w):
    _, running, exposed, priv, data = w
    s = 0
    if running:  s += 2      # a stopped image can't be exploited now
    if exposed:  s += 4      # internet reachability = an entry point
    if priv:     s += 2      # privilege = what the attacker gains
    if data:     s += 3      # reaches sensitive data = the prize
    return s
print("The SAME critical CVE (CVSS 9.8 RCE) on four workloads — context sets urgency:\n")
print(f"   {'workload':16}{'run':>5}{'exposed':>9}{'priv':>6}{'data':>6}{'risk':>7}")
for w in sorted(WORKLOADS, key=lambda x: -risk_score(x)):
    name, running, exposed, priv, data = w
    print(f"   {name:16}{str(running):>5}{str(exposed):>9}{str(priv):>6}{str(data):>6}{risk_score(w):>7}")
print("\n   raw CVSS says all four are 9.8 — IDENTICAL. Context says they're worlds apart:")
print("   web-api (running+exposed+priv+data) is a live breach path; stopped-image")
print("   (dormant, isolated) is barely a risk. Same CVE number, ~5x the real risk.")
print("\nAgentless scanning FINDS the CVE on every workload (complete coverage, no agent).")
print("The GRAPH then enriches it: is it running? exposed? privileged? near data? That")
print("in-context score — not raw CVSS — is what Wiz surfaces. You fix web-api's RCE")
print("today and schedule stopped-image's for the next maintenance window. Validated,")
print("contextual prioritization is why 'if Wiz says critical, it actually is.'")
EOF
```

**Expected result:** One identical critical CVE scored roughly five times higher on a running, exposed, privileged, data-adjacent workload than on a dormant isolated image. The in-context lesson is that agentless scanning finds the CVE everywhere but the graph's enrichment (running, exposed, privileged, near data) sets urgency — validated context, not raw CVSS, is what makes Wiz's "critical" trustworthy.

**Negative test:** Patching by CVSS score alone. All four workloads show 9.8, so a CVSS-ordered queue treats a dormant, isolated image as equal to a live internet-facing breach path — context is the difference between a real fix and busywork.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] CSPM understood as continuous configuration checks against a baseline, feeding the graph as nodes rather than a flat list.
- [ ] Agentless vulnerability management understood — complete coverage, then graph enrichment for in-context priority.
- [ ] Findings placed into the attack-path model so exposure-and-data issues outrank isolated ones.
- [ ] Compliance treated as a live view of the same posture data, not an annual audit event.
