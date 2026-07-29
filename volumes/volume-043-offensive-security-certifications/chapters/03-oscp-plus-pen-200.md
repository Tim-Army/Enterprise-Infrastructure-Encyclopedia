# Chapter 03: OSCP+ (PEN-200)

## Learning Objectives

- Explain what the OSCP/OSCP+ certifies and its practical exam format.
- Describe the PEN-200 methodology across the penetration-testing kill chain.
- Practice the enumeration-first methodology on authorized targets only.
- Understand each phase well enough to detect and defend against it.
- Complete a per-topic walkthrough for each major PEN-200 area.

## Theory and Architecture

The **OSCP** (from course **PEN-200**) is the industry's benchmark hands-on
penetration-testing certification. Passing PEN-200 grants both the **OSCP**
(lifetime) and the renewable **OSCP+** (three years). The exam is a **~24-hour
practical**: three standalone machines (60% of the grade, initial access plus
privilege escalation) and one **Active Directory** set of three machines (40%),
followed by **24 hours to write a professional report**; **70/100** points pass.

PEN-200 teaches a repeatable **methodology** rather than a bag of exploits, across
the kill chain: **reconnaissance and enumeration**, **web and application
attacks**, **password attacks**, **privilege escalation** (Windows and Linux),
**lateral movement and pivoting**, **Active Directory** attacks, and an
introduction to **cloud (AWS)**. The consistent lesson is that **thorough
enumeration** — not clever exploitation — produces most footholds.

## Design Considerations

Prepare for OSCP+ by **building enumeration reflexes** and **note-taking
discipline** (the report is half the skill). Work only in **authorized labs** —
OffSec's PEN-200 lab, intentionally vulnerable VMs you own, or authorized CTFs.
Practice a consistent flow per target: enumerate services → research each service
→ find a foothold → escalate privileges → pivot → document. The AD portion is now
central, so drill AD enumeration and the standard authentication-attack concepts.

## Implementation and Automation

The labs below practice the **methodology and enumeration** for each PEN-200 area
against **your own host or an authorized lab**, and pair each offensive concept
with its **defensive** counterpart. They deliberately stop at enumeration and
concept — the exam skill is the repeatable method, and the defensive mapping is
what makes the knowledge legitimate.

## Validation and Troubleshooting

Confirm the PEN-200 course and exam on offsec.com:

```text
offsec.com/courses/pen-200:
  - earns OSCP (lifetime) + OSCP+ (3-year, renewable)
  - ~24h practical (3 standalone 60% + 1 AD set 40%) + 24h report, 70/100 to pass
  - syllabus: recon, web, password attacks, privesc, lateral movement, AD, cloud
```

Common pitfalls: **under-enumerating** (the #1 cause of getting stuck); poor
**note-taking** (you cannot write the report from memory); and practicing on
**unauthorized systems** — always stay in an authorized lab.

## Security and Best Practices

**Authorization and scope first, always.** Enumerate exhaustively, document every
step and finding as you go, and understand the **defensive control** for each
technique (patching, least privilege, network segmentation, monitoring). The
same knowledge that finds a foothold tells a defender how to close it.

## References and Knowledge Checks

- offsec.com: *PEN-200 (OSCP/OSCP+)* course and exam guide; the OffSec code of conduct.

**Knowledge checks**

1. What is the OSCP+ exam structure and passing score?
2. Why is enumeration the highest-leverage skill in PEN-200?
3. For one PEN-200 phase, what is the corresponding defensive control?

## Hands-On Lab

Per-topic walkthroughs — **one lab per major PEN-200 area**. **All commands
target your own host or an authorized lab only; each pairs offense with defense.**

**Shared prerequisites** — a Kali shell with `nmap`, `gobuster`/`ffuf`, `hydra`,
`john`; a local authorized target (e.g., a vulnerable VM you own) or `localhost`.
**Cost:** none.

### Lab 3.1 — Reconnaissance and enumeration

**Objective:** Run a thorough service enumeration pass (the foundation of PEN-200).

```bash
nmap -sC -sV -p- --min-rate 1000 127.0.0.1 -oN scan.txt 2>/dev/null | grep -E 'open|Service'
echo "Next: research each open service's version for known issues (enumeration -> foothold)."
```

**Expected result:** open services with versions on your **own** host, saved to
`scan.txt` — the enumeration-and-documentation habit the exam rewards.
**Defense:** minimize exposed services and keep versions patched.

**Negative test:** scan only common ports (`-F`) and stop; full-port, service, and
script enumeration finds what a quick scan misses.

**Cleanup:** `rm -f scan.txt`

### Lab 3.2 — Web and application attacks (content discovery)

**Objective:** Enumerate web content on your own lab web server.

```bash
python3 -m http.server 8080 --directory /tmp >/tmp/web.log 2>&1 &
sleep 1
gobuster dir -u http://127.0.0.1:8080 -w /usr/share/wordlists/dirb/common.txt -q 2>/dev/null | head \
  || curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/
kill %1 2>/dev/null
```

**Expected result:** discovered paths (or a `200` from your local server) — web
content discovery, a core web-attack starting point. **Defense:** remove
sensitive files, disable directory listing, and monitor for enumeration.

**Negative test:** assume the app has no hidden content; **enumerate directories
and files** — hidden endpoints are common footholds.

**Cleanup:** `pkill -f 'http.server 8080' 2>/dev/null || true`

### Lab 3.3 — Password attacks (on your own hashes)

**Objective:** Demonstrate offline password cracking against a hash you create.

```bash
HASH=$(python3 -c "import crypt; print(crypt.crypt('password123','\$6\$abc'))")
echo "user:$HASH" > mine.hash
echo "password123" > mywords.txt; john --wordlist=mywords.txt --format=crypt mine.hash 2>/dev/null | head
```

**Expected result:** John recovering the weak password from **your own** hash —
why weak passwords fall to offline cracking. **Defense:** long passphrases, MFA,
and slow hashing (Argon2/bcrypt) with lockout.

**Negative test:** crack a hash you do not own; only ever attack **your own** or
authorized-lab credentials.

**Cleanup:** `rm -f mine.hash mywords.txt; rm -f ~/.john/john.pot 2>/dev/null || true`

### Lab 3.4 — Privilege escalation enumeration (Linux)

**Objective:** Enumerate local privilege-escalation vectors on your own host.

```bash
find / -perm -4000 -type f 2>/dev/null | head -5      # SUID binaries
sudo -l 2>/dev/null | head                            # sudo rights
```

**Expected result:** SUID binaries and your sudo rights — the local-privesc
enumeration PEN-200 teaches. **Defense:** remove unnecessary SUID bits and audit
sudoers regularly.

**Negative test:** attempt escalation before enumerating; you escalate *through*
a specific misconfiguration you must first find — enumerate.

**Cleanup:** none.

### Lab 3.5 — Lateral movement and pivoting (concept + local proof)

**Objective:** Understand pivoting with a local port-forward proof.

```bash
ssh -f -N -L 9000:127.0.0.1:22 "$USER@127.0.0.1" 2>/dev/null && \
  { ss -tlnp | grep 9000; pkill -f 'ssh -f -N -L 9000'; } \
  || echo "Pivot concept: forward a port through a compromised host to reach an internal network."
```

**Expected result:** a local forwarded port (9000 → 22) or the pivot concept —
how an attacker reaches internal hosts through a foothold. **Defense:** segment
networks and monitor for unexpected tunnels.

**Negative test:** assume a flat network is fine; **segmentation** limits lateral
movement — pivoting exploits its absence.

**Cleanup:** `pkill -f 'ssh -f -N -L 9000' 2>/dev/null || true`

### Lab 3.6 — Active Directory enumeration (concept)

**Objective:** Understand the AD enumeration that drives the exam's AD set.

```bash
python3 - <<'PY'
steps = ["Enumerate domain: users, groups, computers (LDAP/BloodHound concepts)",
         "Find attack paths: misconfig, delegation, ACLs",
         "Authentication attacks: password spraying (authorized), Kerberos (Kerberoasting) concepts",
         "Move laterally to Domain Admin along the shortest path"]
for s in steps: print("-", s)
PY
```

**Expected result:** the AD enumeration-to-lateral-movement methodology (concept
only) — the 40% AD portion of the exam. **Defense:** tiered admin model, strong
service-account passwords, and monitoring (e.g., for spraying/Kerberoasting).

**Negative test:** brute-force AD accounts blindly; that triggers lockouts and
alerts — enumerate paths and use targeted, authorized techniques.

**Cleanup:** none.

### Lab 3.7 — Cloud (AWS) enumeration (concept)

**Objective:** Understand cloud enumeration introduced in PEN-200.

```bash
python3 - <<'PY'
print("Cloud enum (authorized): identity (IAM users/roles/policies), storage (public buckets),")
print("metadata endpoints, and over-permissive roles that enable privilege escalation.")
print("Tools: awscli, cloud enum scripts — only against accounts you own/are authorized to test.")
PY
```

**Expected result:** the cloud-enumeration concepts (IAM, storage, metadata,
over-permissioned roles) — the AWS introduction in PEN-200. **Defense:**
least-privilege IAM, block public storage, and restrict metadata access.

**Negative test:** enumerate a cloud account you do not own; cloud testing needs
explicit authorization — never touch another tenant.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OSCP/OSCP+ (PEN-200) is OffSec's benchmark practical penetration-testing
credential: a ~24-hour hands-on exam (three standalone machines plus an Active
Directory set) and a professional report. It teaches a repeatable, enumeration-
first methodology across recon, web, password attacks, privilege escalation,
lateral movement, Active Directory, and cloud — every phase paired here with its
defensive control and practiced only in authorized labs.

- [ ] I can describe the OSCP+ exam structure and passing score.
- [ ] I can run a thorough enumeration pass and document it.
- [ ] I can enumerate privesc, web content, and AD attack paths (concept).
- [ ] I can state the defensive control for each phase.
- [ ] I completed Labs 3.1–3.7 including each negative test.
