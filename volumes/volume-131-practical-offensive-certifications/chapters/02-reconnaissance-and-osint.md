# Chapter 02: Reconnaissance and OSINT

## Learning Objectives

- Cover the reconnaissance phase these certifications test (TCM PORP; the recon stage of CPTS/PNPT/eJPT).
- Understand OSINT and passive footprinting — and apply it defensively to reduce your own exposure.
- Model an attack-surface self-assessment.

## Recon, seen from the defender's chair

Every engagement begins with **reconnaissance** — mapping the target's exposed footprint. TCM's **PORP** (Practical OSINT Research Professional) certifies this discipline; it's also the first phase of network/web pentest certs (CPTS, PNPT, eJPT). The defensive value is direct: **the footprint an attacker enumerates is the footprint you should be shrinking.** This chapter's lab does recon *on your own organization's public exposure* — attack-surface management — the authorized, defensive use of the same skill.

| Recon type | What it finds | Defensive response |
|:---|:---|:---|
| **Passive OSINT** | Public data: domains, subdomains, emails, leaked creds, tech stack, employees | Reduce public exposure; monitor for leaks |
| **Active** (authorized) | Live hosts, open ports, service versions | Close/patch; minimize the attack surface |

## Hands-On Lab

Python models attack-surface self-assessment. **Cost:** none.

### Lab 2.1 — Map your own external attack surface

**Objective:** Enumerate what a public search would reveal about *your* org — to reduce it.

```bash
python3 - <<'EOF'
# Attack-surface self-assessment: catalog exposed assets you should minimize
exposed = [
  {"asset":"vpn.example.com",      "type":"remote access", "risk":"brute force / CVE", "action":"MFA + patch + geo-restrict"},
  {"asset":"old-portal.example.com","type":"forgotten web app","risk":"unpatched", "action":"decommission (shadow IT)"},
  {"asset":"admin@example.com in a breach dump","type":"leaked cred","risk":"credential stuffing","action":"force reset + MFA"},
  {"asset":"job posting listing exact tech stack","type":"info leak","risk":"targeted attack","action":"generalize postings"},
]
print(f"{'exposed asset':<40}{'defensive action'}")
for e in exposed:
    print(f"{e['asset']:<40}{e['action']}")
print("\nRecon done ON YOURSELF = attack-surface management: find what an attacker would, then shrink it.")
EOF
```

**Expected result:** A catalog of exposed assets — a VPN, a forgotten web app, a leaked credential, an over-detailed job posting — each with the defensive action to reduce it. This is OSINT turned inward: **the recon skill PORP certifies is, for a defender, continuous attack-surface reduction.** The forgotten app and the leaked credential are the findings that matter most.

**Negative test:** Running recon against an organization you have no authorization to assess — that's the offensive use, and it's out of bounds; the authorized, defensive application is assessing your *own* exposure (or a client's, under signed scope).

**Cleanup:** None.

### Lab 2.2 — The information a job posting leaks

**Objective:** See how much recon a public source gives away — and tighten it.

```bash
python3 - <<'EOF'
# A too-detailed job posting is free recon for an attacker; generalize it.
posting = "Seeking admin for our Windows Server 2019 AD, Fortinet FW, unpatched legacy SAP, Exchange 2016 on-prem"
leaks = {
  "Windows Server 2019 AD": "exact OS/version -> targeted AD attacks",
  "Fortinet FW":            "vendor -> look up FortiOS CVEs",
  "unpatched legacy SAP":   "advertises a known weak point",
  "Exchange 2016 on-prem":  "high-value target with known exploit chains",
}
print("Job posting leaks:")
for item, why in leaks.items(): print(f"  '{item}' -> {why}")
print("\nDefensive rewrite: 'Seeking a Windows/AD administrator with firewall and ERP experience.' (no versions/vendors)")
EOF
```

**Expected result:** The detailed posting hands an attacker the exact tech stack and a named weak point (unpatched SAP); the generalized rewrite gives none of it. Recon-awareness (a PORP/pentest skill) applied defensively means **not publishing your attack surface** in job postings, conference talks, or metadata. Small hygiene, real risk reduction.

**Negative test:** Assuming recon only matters to attackers — every detail you publish is enumerated; the defensive lesson is to control what leaks, informed by knowing what recon collects.

**Cleanup:** None.

### Lab 2.3 — Leaked-credential monitoring

**Objective:** Model the breach-dump exposure recon finds — and the response.

```bash
python3 - <<'EOF'
# OSINT includes checking breach corpora for your domain's credentials
your_domain = "example.com"
breach_hits = [
  {"email":"admin@example.com", "source":"2024 dump", "password_reused":True},
  {"email":"jdoe@example.com",  "source":"2023 dump", "password_reused":False},
]
for h in breach_hits:
    urgency = "URGENT (reused password + admin)" if h["password_reused"] and h["email"].startswith("admin") else "reset + monitor"
    print(f"{h['email']} in {h['source']} -> {urgency}")
print("\nDefensive OSINT: monitor breach corpora for your domain; force resets; enforce MFA; ban reused passwords.")
EOF
```

**Expected result:** A leaked admin credential with a reused password flagged URGENT. Attackers mine breach dumps for exactly this (credential stuffing); the defender does the same OSINT **first** — monitoring for their domain's exposed credentials and forcing resets/MFA before the credentials are used. This is recon as an early-warning system.

**Negative test:** Ignoring breach-dump exposure — attackers won't; credential stuffing from old dumps is a top initial-access vector, and defensive OSINT monitoring is the counter.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Reconnaissance/OSINT (PORP + the recon phase) and its defensive inversion understood.
- [ ] Attack-surface self-assessment (find and shrink your exposure) drilled.
- [ ] Information leakage (postings, metadata) and leaked-credential monitoring modeled.
