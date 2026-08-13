# Chapter 04: Network and Active Directory Attack Paths — Defended

## Learning Objectives

- Cover the network and Active Directory attack paths these certifications assess (CPTS, PNPT, HTB CAPE, PJPT).
- Understand *how* AD attack paths work — so you can detect, harden, and break them.
- Model an attack-path graph and its defensive controls.

## Understand the path to cut it

Internal network and **Active Directory** compromise is the core of the flagship pentest certs (HTB CPTS, TCM PNPT/PJPT, and the expert HTB CAPE). AD attacks chain small misconfigurations into domain compromise. The defender's job is to **understand each link so as to break it** — every technique in this chapter is presented as a *detection and hardening* lesson, modeled abstractly (no operational tooling).

| Common AD attack-path link | Defensive control that breaks it |
|:---|:---|
| Weak/kerberoastable service accounts | Long/managed passwords (gMSA); monitor for TGS requests |
| LLMNR/NBT-NS poisoning for hashes | Disable LLMNR/NBT-NS; SMB signing |
| Over-privileged accounts / paths to DA | Tiered admin model; least privilege; prune ACLs |
| ADCS misconfigurations | Fix vulnerable certificate templates; monitor issuance |
| Lateral movement (pass-the-hash) | Credential Guard; LAPS (unique local admin passwords) |
| Domain trust abuse | Review/limit trusts; SID filtering |

## Hands-On Lab

Python models attack paths as graphs — to defend them. **Cost:** none.

### Lab 4.1 — Model an attack-path graph

**Objective:** Represent the chain from foothold to domain admin — to find where to cut it.

```bash
python3 - <<'EOF'
# An AD attack path = a graph of privilege escalations. Defenders cut the cheapest edge.
edges = [
  ("workstation-user", "kerberoastable-svc", "weak SPN password"),
  ("kerberoastable-svc", "server-admin", "svc is local admin on a server"),
  ("server-admin", "domain-admin", "DA session to steal on that server"),
]
print("Attack path (foothold -> DA):")
for src, dst, why in edges:
    print(f"  {src}  --[{why}]-->  {dst}")
# Defensive analysis: which single control breaks the whole chain earliest?
print("\nCut the FIRST edge: give the service account a long/managed password (gMSA) -> kerberoast fails -> path broken.")
print("Defense-in-depth: also remove svc's local-admin rights (2nd edge) and avoid DA sessions on member servers (3rd).")
EOF
```

**Expected result:** A three-hop path from a workstation user to domain admin, with the defensive insight: **breaking the earliest edge (a weak service-account password) collapses the whole chain.** Understanding the path as a graph — the way tools like BloodHound help defenders visualize it — lets you find the cheapest, highest-impact control. This graph-thinking is exactly what CAPE-level material teaches, applied to defense.

**Negative test:** Patching only the last hop (avoid DA sessions on that one server) while leaving the weak service account — the attacker just finds another server; cutting the earliest/cheapest edge is more effective than chasing the final one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Kerberoasting, understood to detect it

**Objective:** Model the kerberoasting technique's *signature* — for detection.

```bash
python3 - <<'EOF'
# Kerberoasting: request service tickets (TGS) for accounts with SPNs, then crack offline.
# Defender's view: the DETECTION signal is anomalous TGS requests, esp. for many SPNs / weak encryption.
events = [
  {"user":"jdoe", "tgs_requests":2,  "enc":"AES",  "spn_count":2},
  {"user":"jdoe", "tgs_requests":40, "enc":"RC4",  "spn_count":38},   # <-- kerberoasting signature
]
baseline = 5
for e in events:
    flag = e["tgs_requests"] > baseline*3 and e["enc"] == "RC4"
    note = "  <-- DETECT: mass TGS + RC4 (downgrade) = likely kerberoasting" if flag else ""
    print(f"{e['user']}: {e['tgs_requests']} TGS reqs, enc={e['enc']}, {e['spn_count']} SPNs{note}")
print("\nDetections: alert on bulk TGS (Event 4769) + RC4 downgrade; harden: AES-only, gMSA, long passwords.")
EOF
```

**Expected result:** The burst of 40 TGS requests with RC4 encryption is flagged as the kerberoasting signature. Knowing *how* the attack works (request TGS tickets, crack offline) tells the defender *what to detect* (mass TGS / Event 4769, RC4 downgrade) and *how to prevent* (AES-only, gMSA). This is the defensive payoff of offensive knowledge — the entire premise of studying these techniques.

**Negative test:** A SOC that doesn't understand kerberoasting won't alert on the TGS burst — the technique hides in normal Kerberos traffic unless you know its shape; offensive understanding is what makes the detection possible.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Tiered admin: designing the path out

**Objective:** Model the tiered-administration control that structurally prevents escalation.

```bash
python3 - <<'EOF'
# Tiered admin: Tier 0 (DCs/identity), Tier 1 (servers), Tier 2 (workstations). Credentials never cross DOWN-to-UP.
def violates_tiering(admin_tier, logs_into_tier):
    # a Tier-0 admin logging into a Tier-2 workstation exposes DA creds to workstation compromise
    return admin_tier < logs_into_tier  # lower number = higher privilege
scenarios = [
  ("Tier0 DA", 0, 2),   # DA logs into a workstation -> VIOLATION (creds exposed)
  ("Tier2 helpdesk", 2, 2),
  ("Tier1 server admin", 1, 1),
]
for name, admin_tier, login_tier in scenarios:
    v = violates_tiering(admin_tier, login_tier)
    print(f"{name}: admin-tier {admin_tier} -> logs into tier {login_tier}: {'VIOLATION (credential exposure)' if v else 'OK'}")
print("\nTiering breaks lateral movement structurally: high-priv creds never touch lower-trust machines.")
EOF
```

**Expected result:** The Tier-0 domain admin logging into a Tier-2 workstation is a **violation** — it exposes DA credentials where an attacker on that workstation can steal them. Tiered administration is the architectural control that **structurally prevents** the credential-theft-and-lateral-movement paths the pentest certs exploit: high-privilege credentials never touch lower-trust systems. Understanding the attack path is what justifies this design.

**Negative test:** Domain admins logging into ordinary workstations "for convenience" — one compromised workstation then yields domain admin; tiering exists precisely to prevent that, and the attack-path knowledge is why.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] AD attack paths modeled as graphs, with the cut-the-earliest-edge defensive principle.
- [ ] Kerberoasting understood to *detect* (TGS/RC4 signature) and *prevent* (AES/gMSA).
- [ ] Tiered administration as the structural control against lateral movement drilled.
