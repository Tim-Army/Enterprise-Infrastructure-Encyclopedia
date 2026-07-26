# Chapter 03: Systems Security Certified Practitioner (SSCP)

## Learning Objectives

- Explain who the SSCP is for and how it differs from CC and CISSP.
- List the seven SSCP domains and their exam weights.
- Describe the SSCP exam mechanics and the 2024–2025 refresh to CAT.
- Apply hands-on operations skills: access control, risk monitoring, IR, cryptography, and network defense.
- Complete a per-domain walkthrough for each SSCP domain.

## Theory and Architecture

The **Systems Security Certified Practitioner (SSCP)** is ISC2's credential for
**hands-on security operations** — the administrators, analysts, and engineers
who implement and monitor the controls that a CISSP designs. It requires **one
year** of experience in one or more of its domains (a one-year degree waiver
applies) and is often described as the "technician's CISSP": the same breadth of
concepts, focused on **doing** rather than governing.

Following the outline effective **September 2024** and a **new item format in
2025**, the exam moved to **Computer Adaptive Testing** with a **700/1000** pass
mark across seven weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Security Concepts and Practices | 16% |
| 2 | Access Controls | 15% |
| 3 | Risk Identification, Monitoring and Analysis | 15% |
| 4 | Incident Response and Recovery | 14% |
| 5 | Cryptography | 9% |
| 6 | Network and Communications Security | 16% |
| 7 | Systems and Application Security | 15% |

The weights are strikingly even — no domain dominates — reflecting SSCP's intent
that a practitioner be competent across the whole operations surface.

## Design Considerations

Position SSCP between **CC** and **CISSP**. It suits someone already working in a
SOC, on a systems team, or in network operations who wants a recognized security
operations credential without CISSP's five-year gate. Because the domains map
almost one-to-one onto daily operational tasks — provisioning access, watching
logs, responding to incidents, running crypto, hardening endpoints — the fastest
route to SSCP is to **document the work you already do** against the seven
domains and fill the gaps.

## Implementation and Automation

Every SSCP domain has a concrete shell analog, which is how the labs below make
the abstract concrete: `getfacl`/`setfacl` for **access control**, a CVSS-style
score for **risk analysis**, `journalctl`/`last` for **IR**, `openssl` for
**cryptography**, `nft`/`ss` for **network security**, and package/hardening
checks for **systems and application security**.

## Validation and Troubleshooting

Confirm the SSCP blueprint before studying:

```text
isc2.org > Certifications > SSCP > Exam Outline:
  - seven domains and weights (16/15/15/14/9/16/15, eff Sep 2024)
  - CAT format, 700/1000 to pass
  - one year of experience (or the degree waiver -> Associate of ISC2)
```

Common pitfalls: studying the retired **linear/125-item** format instead of the
current **CAT**; under-preparing **Cryptography** because it is only 9% (it is
still tested and conceptually dense); and confusing SSCP's **Access Controls**
(implementation) with CISSP's **IAM** (architecture).

## Security and Best Practices

Treat SSCP as validation of **operational discipline**: enforce least privilege
with ACLs, monitor with integrity and log analysis, respond with a rehearsed
playbook, and default to strong, current cryptography. Renew via CPE and AMF.
SSCP satisfies **DoD 8140/8570 IAT Level II** baselines — useful for defense and
regulated roles.

## References and Knowledge Checks

- isc2.org: *SSCP* page and Exam Outline; *SSCP Official Study Guide*.

**Knowledge checks**

1. How does SSCP's audience differ from CC's and CISSP's?
2. Which SSCP domain carries the lowest weight, and why is it still important?
3. What changed about the SSCP exam format in 2024–2025?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted SSCP domain**.

**Shared prerequisites** — a Linux shell with `python3`, `openssl`, `getfacl`/
`setfacl` (acl package), `ss`, and `journalctl`; a few labs use `sudo`.
**Cost:** none.

### Lab 3.1 — SSCP: Security Concepts and Practices (16%)

**Objective:** Model IAAA — the identity, authentication, authorization, and
accountability chain.

```bash
python3 - <<'PY'
event = {"identify":"alice", "authenticate":"MFA-ok",
         "authorize":"role=operator", "account":"logged to SIEM"}
for step,val in event.items():
    print(f"{step.title():14}: {val}")
PY
```

**Expected result:** the four IAAA steps in order — the conceptual backbone of
every access decision SSCP tests.

**Negative test:** treat authentication and authorization as one step; proving
*who* you are is separate from *what* you may do.

**Cleanup:** none.

### Lab 3.2 — SSCP: Access Controls (15%)

**Objective:** Implement fine-grained access with a POSIX ACL.

```bash
touch report.csv
setfacl -m u:nobody:r report.csv 2>/dev/null || sudo setfacl -m u:nobody:r report.csv
getfacl report.csv | grep -E 'user:'
```

**Expected result:** a `user:nobody:r--` entry alongside the owner — an explicit
access-control entry beyond the base permission bits (fine-grained DAC).

**Negative test:** rely on `chmod` alone for one extra user; base bits cannot
grant a single named user access — that is what ACLs are for.

**Cleanup:** `setfacl -b report.csv; rm -f report.csv`

### Lab 3.3 — SSCP: Risk Identification, Monitoring and Analysis (15%)

**Objective:** Compute a qualitative risk score from likelihood and impact.

```bash
python3 - <<'PY'
def risk(likelihood, impact):  # 1..5 scales
    score = likelihood*impact
    band = "LOW" if score<=6 else "MEDIUM" if score<=14 else "HIGH"
    return score, band
for name,l,i in [("Unpatched RCE",4,5),("Weak TLS cipher",3,3),("Stale account",2,2)]:
    s,b = risk(l,i); print(f"{name:16} L{l} x I{i} = {s:2}  -> {b}")
PY
```

**Expected result:** scores of 20 (HIGH), 9 (MEDIUM), 4 (LOW) — a risk register
ranked for treatment, the analysis SSCP expects.

**Negative test:** rank by likelihood alone; a low-likelihood, catastrophic-
impact risk still demands attention — risk is the product.

**Cleanup:** none.

### Lab 3.4 — SSCP: Incident Response and Recovery (14%)

**Objective:** Triage authentication events from system logs.

```bash
journalctl _COMM=sshd --no-pager 2>/dev/null | tail -20 \
  || last -n 20
```

**Expected result:** recent authentication/login records — the evidence a
responder reviews to scope an incident and confirm recovery.

**Negative test:** clear logs before investigating; you destroy the evidence and
the audit trail — preserve first.

**Cleanup:** none.

### Lab 3.5 — SSCP: Cryptography (9%)

**Objective:** Show a keyed HMAC detecting tampering that a plain hash cannot
attribute.

```bash
KEY="s3cr3t"
printf 'transfer $100' > msg.txt
openssl dgst -sha256 -hmac "$KEY" msg.txt
printf 'transfer $900' > msg.txt
openssl dgst -sha256 -hmac "$KEY" msg.txt   # different HMAC -> tamper evident
```

**Expected result:** two different HMAC-SHA256 values — a keyed MAC provides
integrity *and* authenticity, unlike an unkeyed hash an attacker could recompute.

**Negative test:** use a plain `sha256sum` for message authentication; anyone can
recompute it after tampering — a MAC needs a secret key.

**Cleanup:** `rm -f msg.txt`

### Lab 3.6 — SSCP: Network and Communications Security (16%)

**Objective:** Read the listening surface and reason about segmentation.

```bash
ss -tuln | awk 'NR==1 || /LISTEN|UNCONN/' | head
echo "Rule of thumb: each listening port is an entry point -> restrict by firewall/VLAN"
```

**Expected result:** the TCP/UDP listeners on the host — the surface a
practitioner reduces with firewalls, segmentation, and least-service hardening.

**Negative test:** assume an internal service needs no firewall; east-west
traffic is a primary lateral-movement path — segment internally too.

**Cleanup:** none.

### Lab 3.7 — SSCP: Systems and Application Security (15%)

**Objective:** Harden-check a host — find SUID binaries and world-writable files.

```bash
find /usr/bin -perm -4000 -type f 2>/dev/null | head -5      # SUID review
find /tmp -maxdepth 1 -perm -0002 -type f 2>/dev/null | head # world-writable
```

**Expected result:** a short list of SUID binaries (each a privilege-escalation
review item) and any world-writable files in `/tmp` — endpoint-hardening
findings SSCP covers.

**Negative test:** ignore SUID binaries as "normal"; each one runs as its owner
and is a hardening review item — enumerate and justify them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SSCP is ISC2's hands-on security-operations credential: seven evenly weighted
domains (16/15/15/14/9/16/15) on a CAT exam, one year of experience, DoD 8140
IAT-II recognized. It validates the practitioner who implements and monitors the
controls a CISSP designs — access control, risk monitoring, incident response,
cryptography, and network and endpoint defense.

- [ ] I can list the seven SSCP domains and their weights.
- [ ] I can implement an ACL and a keyed MAC at a shell.
- [ ] I can compute a likelihood × impact risk score.
- [ ] I can triage auth logs and enumerate SUID/world-writable files.
- [ ] I completed Labs 3.1–3.7 including each negative test.
