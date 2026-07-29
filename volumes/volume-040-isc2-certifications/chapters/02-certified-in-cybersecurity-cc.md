# Chapter 02: Certified in Cybersecurity (CC)

## Learning Objectives

- Explain who the CC is for and why the exam is free and requires no experience.
- List the five CC domains and their exam weights.
- Describe the CC exam mechanics and the September 2026 outline refresh.
- Relate CC concepts to the CIA triad, access-control models, and basic network defense.
- Complete a per-domain walkthrough for each CC domain.

## Theory and Architecture

**Certified in Cybersecurity (CC)** is ISC2's **entry-level** credential, aimed
at career-changers, students, and IT staff moving into security. It requires
**no prior experience**, and ISC2 offers the exam and self-paced training free
under its **One Million Certified in Cybersecurity** pledge. CC proves a
candidate understands the foundational vocabulary and concepts that every later
ISC2 credential assumes.

The exam is **100 multiple-choice items in 2 hours**, pass mark **700/1000**,
across five weighted domains. The outline effective **1 October 2025** — current
through 31 August 2026 — weights them:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Security Principles | 26% |
| 2 | Business Continuity (BC), Disaster Recovery (DR) & Incident Response Concepts | 10% |
| 3 | Access Controls Concepts | 22% |
| 4 | Network Security | 24% |
| 5 | Security Operations | 18% |

> **Currency note:** ISC2 has announced a **new CC exam outline effective 1
> September 2026**. Confirm the domains and weights on the official CC exam
> outline before scheduling on or after that date.

## Design Considerations

CC is the **on-ramp**, not a destination. Use it to enter the field and to
decide a direction: candidates who enjoy the **Access Controls** and **Network
Security** material (nearly half the exam combined) often continue to **SSCP**;
those drawn to **Security Principles** and **Security Operations** are on the
path toward **CISSP**. Because CC assumes no background, its value is breadth —
a shared vocabulary (CIA triad, risk, least privilege, defense in depth) that
makes the heavier credentials approachable.

## Implementation and Automation

CC concepts map cleanly onto everyday Linux tooling, which is how this chapter's
labs make them concrete: hashing and encryption for **confidentiality and
integrity**, file permissions for **access control**, and packet and port
inspection for **network security**. None of it requires special hardware — a
single Linux shell demonstrates every domain.

## Validation and Troubleshooting

Confirm the CC blueprint and mechanics before studying:

```text
isc2.org > Certifications > Certified in Cybersecurity (CC) > Exam Outline:
  - five domains and weights (26/10/22/24/18 on the 1 Oct 2025 outline)
  - 100 items, 2 hours, 700/1000 to pass
  - free exam and self-paced training (One Million initiative)
  - the new outline effective 1 September 2026
```

Common pitfalls: paying for a third-party CC voucher when ISC2's is free;
studying a pre-2025 outline; and treating CC as equivalent to Security+ — they
overlap but CC is shorter and broader, and it is an ISC2 (endorsed, ethics-bound,
CPE-renewed) credential.

## Security and Best Practices

Keep the fundamentals rigorous even at entry level: know the **CIA triad**,
**least privilege**, **defense in depth**, and the difference between
**identification, authentication, authorization, and accountability (IAAA)** —
these recur on every ISC2 exam. Renew CC like any ISC2 credential (CPE + AMF);
because it is entry-level the CPE requirement is modest, but the habit matters.

## References and Knowledge Checks

- isc2.org: *Certified in Cybersecurity* page and Exam Outline; *One Million Certified in Cybersecurity*.

**Knowledge checks**

1. Which two CC domains together make up nearly half the exam?
2. What does the CIA triad stand for, and how does each lab in this chapter touch it?
3. What changes on 1 September 2026 for the CC exam?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CC domain**.

**Shared prerequisites** — a Linux shell with `python3`, `openssl`, `sha256sum`,
`ip`, and `ss`. **Cost:** none.

### Lab 2.1 — CC: Security Principles (26%)

**Objective:** Demonstrate the CIA triad with a hash (integrity) and a cipher
(confidentiality).

```bash
echo "patient records" > data.txt
sha256sum data.txt                                   # integrity baseline
openssl enc -aes-256-cbc -pbkdf2 -in data.txt -out data.enc -pass pass:Demo123
file data.enc                                        # confidentiality: now opaque
```

**Expected result:** a 64-hex SHA-256 digest (integrity) and `data.enc` reported
as `data` / OpenSSL-encrypted, not readable text (confidentiality) — two legs of
the CIA triad on one file.

**Negative test:** `cat data.enc` expecting the plaintext; it is ciphertext —
confidentiality is enforced.

**Cleanup:** `rm -f data.txt data.enc`

### Lab 2.2 — CC: BC, DR & Incident Response Concepts (10%)

**Objective:** Compute the recovery objectives (RPO/RTO) that BC/DR planning sets.

```bash
python3 - <<'PY'
last_backup_min_ago = 45     # data age at failure
restore_time_min    = 90     # time to bring service back
print(f"RPO (max tolerable data loss) must be >= {last_backup_min_ago} min")
print(f"RTO (max tolerable downtime)  must be >= {restore_time_min} min")
print("Incident response order: Preparation -> Detection -> Response -> Recovery -> Lessons Learned")
PY
```

**Expected result:** an RPO of 45 min and RTO of 90 min, plus the incident-
response lifecycle — the vocabulary CC tests.

**Negative test:** conflate RPO (data loss) with RTO (downtime); they measure
different things.

**Cleanup:** none.

### Lab 2.3 — CC: Access Controls Concepts (22%)

**Objective:** Enforce least privilege with Unix permissions.

```bash
echo "secret" > vault.txt
chmod 600 vault.txt                       # owner-only
ls -l vault.txt | awk '{print $1}'        # -rw-------
chmod 640 vault.txt; ls -l vault.txt | awk '{print $1}'   # add group read
```

**Expected result:** `-rw-------` then `-rw-r-----` — a direct demonstration of
least privilege and discretionary access control (DAC) via permission bits.

**Negative test:** `chmod 777 vault.txt` "to make it work"; world-writable
secrets violate least privilege — never do this.

**Cleanup:** `rm -f vault.txt`

### Lab 2.4 — CC: Network Security (24%)

**Objective:** Inspect listening services and identify the attack surface.

```bash
ss -tlnp 2>/dev/null | awk 'NR==1 || /LISTEN/' | head
ip -brief addr
```

**Expected result:** the TCP ports in `LISTEN` state and the host's addresses —
the exposed network surface a defender inventories and a firewall then reduces.

**Negative test:** assume "no output means secure"; it may mean `ss` needs
privileges — re-run with `sudo` before concluding.

**Cleanup:** none.

### Lab 2.5 — CC: Security Operations (18%)

**Objective:** Practice data handling and monitoring — hash-verify a file's
integrity over time.

```bash
echo "config v1" > app.conf; sha256sum app.conf | tee app.conf.sha256
echo "tampered" >> app.conf
sha256sum -c app.conf.sha256 || echo "INTEGRITY FAILURE detected"
```

**Expected result:** the second check fails and prints `INTEGRITY FAILURE
detected` — file-integrity monitoring, a core security-operations control.

**Negative test:** skip the baseline hash; without it you cannot detect the
change — monitoring needs a known-good reference.

**Cleanup:** `rm -f app.conf app.conf.sha256`

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CC is ISC2's free, no-experience entry credential: 100 items over five domains
weighted 26/10/22/24/18, with a new outline arriving 1 September 2026. Its value
is a rigorous shared vocabulary — CIA, IAAA, least privilege, defense in depth,
BC/DR, and basic network defense — that every heavier ISC2 credential builds on.

- [ ] I can list the five CC domains and their weights.
- [ ] I can demonstrate confidentiality, integrity, and access control at a shell.
- [ ] I can distinguish RPO from RTO and name the IR lifecycle.
- [ ] I know the CC outline changes on 1 September 2026.
- [ ] I completed Labs 2.1–2.5 including each negative test.
