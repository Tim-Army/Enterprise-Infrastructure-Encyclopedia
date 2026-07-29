# Chapter 08: Tenable One — Exposure Management

## Learning Objectives

- Explain exposure management and the Tenable One platform.
- Unify vulnerability, web, cloud, OT, and identity exposure.
- Use the Cyber Exposure Score and attack path analysis.
- Manage the external attack surface.
- Complete a walkthrough for each exposure-management topic.

## Theory and Architecture

**Tenable One** is Tenable's **exposure-management platform** — it unifies the signals from
**Vulnerability Management, Web App Scanning, Cloud Security, OT Security, and identity exposure**
into a single view of an organization's **cyber exposure**. The shift from vulnerability management to
**exposure management** is conceptual: instead of counting vulnerabilities per silo, you ask "where is
the organization actually exposed, and what would an attacker reach?" Tenable One provides a **Cyber
Exposure Score (CES)** (an organization-wide exposure metric), **Attack Path Analysis** (mapping how
an attacker could chain a misconfiguration, a vulnerability, and an over-permissive identity to reach
a critical asset), and **Attack Surface Management (ASM)** (discovering internet-facing assets you may
not know you own). The value is **context and prioritization across domains** — a medium vulnerability
on an internet-facing asset with a path to the crown jewels matters more than a critical one on an
isolated box. This chapter teaches each with a hands-on defensive walkthrough (exposure scoring,
attack path analysis, and attack surface discovery).

## Design Considerations

Think in **exposure and attack paths**, not siloed findings. Track the **Cyber Exposure Score** trend
as the top-line metric. Use **Attack Path Analysis** to prioritize choke points (fix one node to break
many paths). Run **ASM** to find shadow internet-facing assets. Communicate exposure to leadership in
**business terms**.

## Implementation and Automation

The labs unify exposure, compute a Cyber Exposure Score, analyze an attack path, and discover the
attack surface.

## Validation and Troubleshooting

Confirm the exposure-management model:

```text
Tenable One = unify VM + WAS + Cloud + OT + identity into one exposure view. Cyber Exposure Score (CES) = org-wide exposure metric.
Attack Path Analysis = how an attacker chains misconfig + vuln + identity to reach crown jewels. Attack Surface Management (ASM) = discover unknown internet-facing assets.
```

Common pitfalls: managing each product's findings in a **silo** (missing cross-domain attack paths);
and unknown **internet-facing assets** (shadow IT) never scanned.

## Security and Best Practices

Manage **exposure and attack paths** across domains, track the **CES** trend, fix **choke points**,
discover the **attack surface**, and report in business terms. All work is defensive. Discover and
scan only assets you own.

## Hands-On Lab

Exposure-management walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 8.1 — Unify exposure across domains

**Objective:** One view of exposure.

```python
python3 - <<'PY'
domains={"VM (hosts)":"1200 findings","Web (WAS)":"85 findings","Cloud":"40 misconfigs",
         "OT":"15 device vulns","Identity":"22 over-permissive roles"}
for d,f in domains.items(): print(f"{d:14}: {f}")
print("Tenable One: unify all domains -> single exposure picture (not five silos)")
PY
```

**Expected result:** exposure **unified across domains** — the Tenable One view.

**Negative test:** manage each domain in its own tool; cross-domain attack paths are invisible —
**unify** them.

**Cleanup:** none.

### Lab 8.2 — Compute a Cyber Exposure Score

**Objective:** One top-line metric.

```python
python3 - <<'PY'
def ces(critical_exposed, total_assets):   # illustrative 0-1000 exposure metric
    return round(1000 * critical_exposed / max(total_assets,1))
print("CES:", ces(48, 800), "(lower is better)")
print("Trend last quarter: 640 -> 540 -> 480 (improving) — the board-level metric")
PY
```

**Expected result:** a **Cyber Exposure Score** and its trend — the exposure-management KPI.

**Negative test:** report raw counts to the board; a single **CES trend** communicates risk reduction —
use it.

**Cleanup:** none.

### Lab 8.3 — Analyze an attack path

**Objective:** Find and break the chain.

```python
python3 - <<'PY'
path=["Internet-facing web app (medium vuln)","-> lateral to app server (cached creds)",
      "-> over-permissive service account","-> crown-jewel database"]
print(" ".join(path))
choke="revoke the over-permissive service account (breaks the path to the database)"
print("\nAttack Path Analysis -> choke point:", choke)
PY
```

**Expected result:** an **attack path** and the **choke point** that breaks it — attack-path
prioritization.

**Negative test:** fix the medium web vuln in isolation and ignore the path; the account still
bridges to the crown jewels — fix the **choke point**.

**Cleanup:** none.

### Lab 8.4 — Discover the external attack surface

**Objective:** Find unknown exposed assets.

```python
python3 - <<'PY'
known={"www.example.com","api.example.com"}
discovered={"www.example.com","api.example.com","old-vpn.example.com","test-portal.example.com"}
shadow=discovered - known
print("newly-discovered internet-facing assets (shadow):", shadow)
print("ASM: scan/assess these before an attacker does")
PY
```

**Expected result:** **shadow internet-facing assets** discovered — Attack Surface Management.

**Negative test:** scan only the assets you already track; **unknown** exposed assets remain
unassessed — run **ASM**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Tenable One unifies vulnerability, web, cloud, OT, and identity exposure into one view, with a Cyber
Exposure Score, Attack Path Analysis, and Attack Surface Management — shifting from counting
vulnerabilities to managing real, cross-domain exposure.

- [ ] I can unify exposure across domains.
- [ ] I can compute a Cyber Exposure Score.
- [ ] I can analyze an attack path and find the choke point.
- [ ] I can discover the external attack surface.
- [ ] I completed Labs 8.1–8.4 including each negative test.
