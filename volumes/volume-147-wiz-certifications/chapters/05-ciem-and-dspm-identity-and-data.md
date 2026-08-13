# Chapter 05: CIEM and DSPM — Identity and Data

## Learning Objectives

- Explain CIEM — effective permissions and the privilege side of risk.
- Explain DSPM — finding, classifying, and protecting sensitive data.
- Understand why identity and data are the two ends of most attack paths.
- Recognize effective (not just assigned) permissions as the truth.

*Cert relevance: CIEM and DSPM are the identity and data pillars of Wiz Cloud — the two ends of the attack path that make exposure and vulnerability *matter*.*

## CIEM: who can actually do what

**Cloud Infrastructure Entitlement Management (CIEM)** answers "who can do what in my cloud?" — and the hard word is *actually*. Cloud permissions are a tangle: an identity's **effective permissions** are the accumulation of its directly-attached policies, its group memberships, the roles it can assume, and roles those roles can assume, minus explicit denies. What an identity is *assigned* and what it can *effectively do* are rarely the same, and the gap is where privilege-escalation risk hides.

Wiz computes **effective permissions** by resolving the whole chain in the graph, then surfaces the dangerous truths: this "read-only" user can, through an assumable role, actually delete production; this service account nobody audits can reach every bucket. CIEM is the **privilege** factor of the toxic combination (Chapter 3) — it is *what the attacker gains* once they land. The lab models assigned-versus-effective permissions.

## DSPM: where the sensitive data is

**Data Security Posture Management (DSPM)** answers "where is my sensitive data, and is it exposed?" You cannot protect data you do not know you have — and cloud sprawl means sensitive data ends up in forgotten buckets, dev copies of production, and mislabeled stores. DSPM **discovers and classifies** data across the estate (PII, PHI, PCI, secrets), then assesses its **exposure**: is this sensitive store public? reachable by an over-privileged identity? unencrypted?

DSPM is the **crown-jewel** end of the attack path — it is *what the attacker is after*. Together, CIEM (privilege) and DSPM (data) turn a generic "exposed vulnerable workload" into a specific "exposed vulnerable workload **whose role can read a bucket of customer PII**" — which is the difference between a finding and an emergency. The lab models data discovery and exposure.

## Two ends of the path

Return to the attack path from Chapter 3:

```text
internet → [exposed, vulnerable workload] → [CIEM: what its identity can reach] → [DSPM: the sensitive data at the end]
```

CSPM and vulnerability management (Chapter 4) find the *entry and the weakness*; **CIEM and DSPM define the two ends that make it worth attacking** — the privilege gained and the data reached. A CNAPP needs all four because an attack path needs all four; drop CIEM and you cannot tell an over-privileged path from a dead end, drop DSPM and you cannot tell a crown jewel from an empty bucket. This is why Wiz consolidates them onto one graph.

## Hands-On Lab

Python models entitlements and data exposure. **Cost:** none.

### Lab 5.1 — Assigned versus effective permissions

**Objective:** Resolve the permission chain to find hidden privilege.

```bash
python3 - <<'EOF'
# identities with directly-assigned policies + roles they can assume
ASSIGNED = {
  "analyst":     {"s3:GetObject"},               # looks read-only
  "ci-runner":   {"sts:AssumeRole:deploy-role"},  # can assume deploy-role
  "deploy-role": {"s3:*", "ec2:*"},               # powerful
  "intern":      {"s3:GetObject"},
}
ASSUMABLE = {                                     # who can assume what
  "analyst":   ["ci-runner"],                     # analyst -> ci-runner (misconfig!)
  "ci-runner": ["deploy-role"],
}
def effective(identity, seen=None):
    seen = seen or set()
    if identity in seen: return set()
    seen.add(identity)
    perms = set(ASSIGNED.get(identity, set()))
    # follow assumable chain
    for target in ASSUMABLE.get(identity, []):
        perms |= effective(target, seen)
    # a raw 'AssumeRole:X' token contributes X's perms too
    for p in list(perms):
        if p.startswith("sts:AssumeRole:"):
            perms |= effective(p.split(":")[-1], seen)
    return perms

for who in ["analyst", "intern", "ci-runner"]:
    asg = ASSIGNED.get(who, set())
    eff = effective(who)
    danger = "  <-- ESCALATION" if ("s3:*" in eff or "ec2:*" in eff) and "s3:*" not in asg else ""
    print(f"{who:12} assigned={sorted(asg)}")
    print(f"{'':12} EFFECTIVE={sorted(eff)}{danger}")
print("\nThe trap: 'analyst' is ASSIGNED only s3:GetObject — looks harmless, read-only.")
print("But analyst -> can assume ci-runner -> can assume deploy-role -> has s3:* + ec2:*.")
print("So analyst's EFFECTIVE permission is FULL S3 and EC2 control — including DELETE.")
print("'intern' has the same assigned policy but NO assume chain, so intern really is")
print("read-only. Same assignment, opposite risk — the difference is in the GRAPH.")
print("\nCIEM computes EFFECTIVE permissions by resolving the whole assume-role chain,")
print("not the assigned policy you see at a glance. That gap — assigned looks safe,")
print("effective is dangerous — is where privilege escalation hides, and it's the")
print("PRIVILEGE factor of the toxic combination: what the attacker gains on landing.")
EOF
```

**Expected result:** An identity assigned only read-only access shown to have full delete power through an assume-role chain, while another with the identical assigned policy is genuinely read-only. The effective-permissions lesson is that assigned policy is not the truth — CIEM resolves the whole chain in the graph, and the gap between assigned-looks-safe and effective-is-dangerous is exactly where privilege escalation hides.

**Negative test:** Auditing identities by their attached policies. "analyst" and "intern" have the same read-only policy, so a policy audit clears both — but analyst's assume-role chain grants full control, which only resolving effective permissions reveals.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Data discovery and exposure (DSPM)

**Objective:** Find sensitive data and rank stores by exposure.

```bash
python3 - <<'EOF'
# data stores discovered across the estate; DSPM classifies + assesses exposure
STORES = [
  # name,            classification,   public, encrypted, reachable_by_exposed_role
  ("prod-customers",  "PII",           False,  True,   True),   # role-reachable from exposed wl
  ("analytics-copy",  "PII (dev copy)",True,   False,  False),  # PUBLIC copy of prod PII!
  ("payments",        "PCI",           False,  True,   False),
  ("app-logs",        "none",          True,   False,  False),  # public but not sensitive
  ("backups",         "PII",           False,  False,  True),   # unencrypted + reachable
]
def exposure(s):
    _, cls, public, enc, reachable = s
    if cls == "none": return (0, "not sensitive")
    score = 0; why = []
    if public:        score += 5; why.append("PUBLIC")
    if not enc:       score += 2; why.append("unencrypted")
    if reachable:     score += 3; why.append("reachable by exposed role")
    return (score, ", ".join(why) if why else "well-protected")
print("DSPM: discovered data stores, ranked by EXPOSURE of SENSITIVE data:\n")
ranked = sorted(STORES, key=lambda s: -exposure(s)[0])
for s in ranked:
    name, cls, *_ = s
    score, why = exposure(s)
    tag = f"[{cls}]"
    print(f"   risk {score:>2}  {name:16}{tag:16} {why}")
print("\nTop finding: 'analytics-copy' — a PUBLIC, UNENCRYPTED dev copy of production")
print("PII. The prod store is locked down, but someone made a copy for analytics and")
print("left it public. DSPM finds it BECAUSE it classifies data wherever it lives, not")
print("just where you expect it. 'backups' is next: PII, unencrypted, reachable.")
print("\n'app-logs' is public too but classified 'none' — public alone isn't the issue,")
print("PUBLIC + SENSITIVE is. DSPM is the CROWN-JEWEL end of the attack path: it tells")
print("you WHICH exposure reaches real data. You can't protect data you didn't know")
print("you had — and the dangerous copies are always the ones you forgot about.")
EOF
```

**Expected result:** A public, unencrypted dev copy of production PII surfacing as the top data-exposure risk — found because DSPM classifies data wherever it lives, not only where expected — while a public but non-sensitive log store is correctly deprioritized. The DSPM lesson is that you cannot protect data you do not know you have, and public-plus-sensitive (not public alone) is the crown-jewel end of the attack path.

**Negative test:** Protecting only the known production data store. The locked-down prod store is fine; the risk is the forgotten public dev copy of the same PII — DSPM finds it precisely because it discovers and classifies data across the whole estate, not just the expected locations.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] CIEM understood as effective (chain-resolved) permissions — the privilege factor and what an attacker gains.
- [ ] DSPM understood as discovering and classifying sensitive data and assessing its exposure — the crown-jewel end.
- [ ] Identity and data recognized as the two ends of an attack path that make exposure and vulnerability matter.
- [ ] Effective-permission and data-exposure risk ranked by graph context, not by assigned policy or store name.
