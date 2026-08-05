# Chapter 03: Attack Paths and Toxic Combinations

## Learning Objectives

- Define a toxic combination and an attack path in Wiz terms.
- Understand why the *combination* is the risk, not the individual issue.
- Prioritize by attack path rather than by severity count.
- Recognize how attack-path thinking cuts alert fatigue.

*Cert relevance: attack paths are **the** Wiz concept — every exam tests whether you prioritize the path, not the pile. This is what "if Wiz says critical, it actually is" means.*

## The toxic combination

A **toxic combination** is a set of individually-manageable issues that, *together*, form a serious risk. Wiz's canonical example combines four factors:

1. **Public exposure** — the resource is reachable from the internet.
2. **A critical vulnerability** — it has an exploitable flaw (e.g. an RCE).
3. **High privilege** — its identity has powerful permissions.
4. **Access to sensitive data** — those permissions reach a crown jewel (PII, secrets).

Each factor *alone* is common and low-drama: plenty of workloads are public; plenty have some CVE; plenty of roles are over-privileged; plenty of data is sensitive. But a workload that is **public AND vulnerable AND high-privilege AND can reach PII** is a breach path — an attacker exploits the vuln from the internet, assumes the privilege, and reads the data. The **combination** is the risk.

## The attack path

An **attack path** is the concrete route through the Security Graph that a toxic combination describes:

```text
internet → [public web-vm: critical RCE] → [assumes app-role] → [reads customer-db: PII]
```

Wiz computes these by traversing the graph: it finds every path from an **entry point** (internet exposure, or a compromised identity) to a **crown jewel** (sensitive data, admin privilege), where each hop is enabled by a real relationship. The output is not "8,000 findings" but "**4 attack paths**, here is each one, here is the one node on each path whose fix breaks it."

That last part is the payoff: an attack path has **chokepoints** — a single node whose remediation severs the whole path. Fixing the one critical vuln on the public web-vm breaks the path even if the over-privileged role and the sensitive data remain. Attack-path thinking tells you not just *what is risky* but *the smallest fix that removes the risk*.

## Why this cuts alert fatigue

Legacy scanners produce thousands of findings and rank them by CVSS severity, which drowns teams: everything is "high" or "critical," so nothing is. Attack-path prioritization inverts it — **most findings are not on any path to anything that matters, and can wait; the few that complete a path to a crown jewel are urgent.** A critical CVE on an isolated internal batch box with no sensitive access is genuinely low-priority; a *medium* CVE that happens to be the chokepoint on a path from the internet to your customer database is urgent. Severity is a property of the flaw; **risk is a property of the path.** The labs make this operational.

## Hands-On Lab

Python models attack-path detection and prioritization. **Cost:** none.

### Lab 3.1 — Detect the toxic combination

**Objective:** Find the workloads where all four factors coincide.

```bash
python3 - <<'EOF'
# each workload scored on the four toxic factors
WORKLOADS = {
  # name        public  crit_vuln  high_priv  reaches_pii
  "web-frontend":  (True,  True,   True,   True),   # ALL FOUR -> toxic
  "public-cdn":    (True,  False,  False,  False),  # public but nothing else
  "internal-api":  (False, True,   True,   True),   # bad, but NOT public (no entry)
  "batch-worker":  (False, True,   True,   False),  # vuln+priv, no data, not public
  "marketing-vm":  (True,  True,   False,  False),  # public+vuln, low priv, no data
  "admin-jumpbox": (False, False,  True,   True),   # priv+data, not public, no vuln
}
FACTORS = ["public", "crit_vuln", "high_priv", "reaches_pii"]
print(f"{'workload':16}{'public':>8}{'critVuln':>10}{'highPriv':>10}{'PII':>6}   verdict")
toxic = []
for name, flags in WORKLOADS.items():
    allfour = all(flags)
    if allfour: toxic.append(name)
    mark = "  <-- TOXIC COMBINATION" if allfour else ""
    print(f"{name:16}{str(flags[0]):>8}{str(flags[1]):>10}{str(flags[2]):>10}{str(flags[3]):>6}{mark}")
print(f"\nTOXIC (all four factors): {toxic}")
print("\nNotice what is NOT toxic, and why:")
print("  public-cdn   — public, but no vuln/priv/data. Public alone is fine.")
print("  internal-api — vuln+priv+data, but NOT internet-exposed: no ENTRY point.")
print("  batch-worker — vuln+priv, but reaches no sensitive data: path leads nowhere.")
print("  marketing-vm — public+vuln, but low priv + no data: attacker gains little.")
print("\nEach factor ALONE is common and low-drama. The RISK is the COMBINATION —")
print("public + vulnerable + privileged + reaches-data = an attacker exploits from the")
print("internet, assumes the privilege, and reads the crown jewels. web-frontend is")
print("the one to fix, not because any single factor is worst, but because it's the")
print("only workload where all four MEET. This is the core Wiz judgment.")
EOF
```

**Expected result:** Only the workload with all four factors (public, vulnerable, high-privilege, reaches PII) flagged as toxic, while workloads with three of four are correctly not — each missing factor breaks the chain. The toxic-combination lesson is that individual factors are common and low-drama; the risk is the coincidence of all four, which is where an actual breach path exists.

**Negative test:** Flagging every workload with a critical vulnerability. Four of six here have a critical vuln, but only one is a toxic combination — treating the vuln alone as the risk floods the queue and misses that the others lack exposure, privilege, or data access.

**Cleanup:** None.

### Lab 3.2 — Prioritize by path, and find the chokepoint

**Objective:** Rank findings by whether they complete a path, and find the one fix that breaks it.

```bash
python3 - <<'EOF'
# graph of the toxic path + some noise findings elsewhere
edges = {
  "internet":    ["web-frontend"],
  "web-frontend":["app-role"],
  "app-role":    ["customer-db"],
  "customer-db": ["<PII>"],
}
# findings with CVSS severity; which are ON the internet->PII path?
findings = [
  # id,                 node,          severity(CVSS)
  ("RCE-2025-1",        "web-frontend", 9.8),   # chokepoint: entry of the path
  ("over-privilege",    "app-role",     6.5),   # on path (privilege hop)
  ("public-exposure",   "web-frontend", 7.0),   # on path (the exposure)
  ("crit-CVE-batch",    "batch-worker", 9.8),   # NOT on path (isolated)
  ("crit-CVE-devbox",   "dev-box",      9.9),   # NOT on path (isolated)
  ("medium-CVE-old",    "old-vm",       5.4),   # NOT on path
]
path_nodes = {"web-frontend", "app-role", "customer-db"}
print("Legacy ranking (by CVSS severity, highest first):")
for fid, node, sev in sorted(findings, key=lambda x: -x[2]):
    print(f"   CVSS {sev}  {fid:16} on {node}")
print("   -> you'd fix crit-CVE-devbox (9.9) and crit-CVE-batch (9.8) FIRST.")
print("      Both are isolated. You'd spend your morning on non-risks.\n")

print("Wiz ranking (on the internet->PII attack path first):")
on_path  = [f for f in findings if f[1] in path_nodes]
off_path = [f for f in findings if f[1] not in path_nodes]
for fid, node, sev in sorted(on_path, key=lambda x: -x[2]):
    print(f"   ON-PATH  CVSS {sev}  {fid:16} on {node}")
for fid, node, sev in sorted(off_path, key=lambda x: -x[2]):
    print(f"   off-path CVSS {sev}  {fid:16} on {node}  (can wait)")

print("\nCHOKEPOINT — the single fix that severs the path:")
print("   internet -> web-frontend -> app-role -> customer-db -> PII")
print("   fix RCE-2025-1 on web-frontend (the entry) and the internet can no longer")
print("   START down the path. ONE fix breaks it — even though app-role is still")
print("   over-privileged and customer-db still holds PII.")
print("\nSeverity is a property of the FLAW; risk is a property of the PATH. The 9.9 on")
print("dev-box is a bigger NUMBER and a smaller RISK than the 9.8 chokepoint on the")
print("path to PII. Wiz ranks by path, then points at the chokepoint: not just 'what's")
print("risky' but 'the smallest fix that removes the risk.' That's how it cuts fatigue.")
EOF
```

**Expected result:** Legacy CVSS ranking putting two isolated critical CVEs first, while Wiz's path-based ranking surfaces the on-path findings and identifies the single chokepoint fix that severs the internet-to-PII route. The prioritize-by-path lesson is that severity ranks the flaw but risk ranks the path — the highest CVSS number can be the lowest risk, and the chokepoint is the smallest fix that removes the whole path.

**Negative test:** Working the queue in CVSS order. The two highest-scored CVEs are on isolated boxes off any path to sensitive data; fixing them first spends effort on non-risks while the real chokepoint waits.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Toxic combination defined as the coincidence of exposure, vulnerability, privilege, and data access — the combination, not any single factor.
- [ ] Attack path understood as the concrete graph route a toxic combination describes, with identifiable chokepoints.
- [ ] Prioritization done by path (does it reach a crown jewel?) rather than by CVSS severity count.
- [ ] Attack-path thinking recognized as the cure for alert fatigue — most findings are off any path and can wait.
