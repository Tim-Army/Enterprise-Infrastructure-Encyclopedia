# Chapter 02: Cybersecurity and IT Essentials — GFACT, GISF, GSEC

## Learning Objectives

- Describe the GIAC Essentials focus area (GFACT, GISF, GSEC).
- Apply foundational technology, security, and hands-on defensive concepts.
- Use core command-line skills that underpin later focus areas.
- Verify security fundamentals with real tools.
- Complete a walkthrough for each essentials credential.

## Theory and Architecture

The **Cybersecurity & IT Essentials** focus area builds the foundation every other GIAC track
assumes. **GFACT (GIAC Foundational Cybersecurity Technologies)** covers the underlying technology —
computer hardware, operating systems, networking, programming/logic, and data representation — the
"how computers work" grounding for security. **GISF (GIAC Information Security Fundamentals)**, a
newer entry, covers security concepts, risk, and the CIA triad for those newer to the field.
**GSEC (GIAC Security Essentials)** is the flagship foundation — a broad, hands-on certification
spanning networking, cryptography, access control, defense-in-depth, Windows/Linux security,
incident handling basics, and more, with **CyberLive** practical testing. Together these validate
that a practitioner can read a hex dump, reason about a network capture, harden a host, and apply
core security principles — the prerequisites for the specialized focus areas. This chapter teaches
each with a hands-on defensive walkthrough.

## Design Considerations

Start with **GFACT/GISF** if you are new to IT/security; **GSEC** is the standard broad foundation
for practitioners and satisfies many baseline requirements. Practice the **command line** (Linux and
Windows), packet basics, and cryptography hands-on — GSEC's CyberLive rewards real skill, not
memorization. These foundations pay off across every later chapter.

## Implementation and Automation

The labs decode data (GFACT), reason about CIA/risk (GISF), and harden/verify a host (GSEC).

## Validation and Troubleshooting

Confirm the essentials map:

```text
GFACT = foundational tech (hardware/OS/networking/programming/data). GISF = security fundamentals (CIA/risk).
GSEC = broad hands-on security essentials (networking, crypto, access control, defense-in-depth) + CyberLive.
Foundation for all other focus areas.
```

Common pitfalls: skipping the foundation and stalling on later practical exams; and treating GSEC as
trivia (it is **hands-on**).

## Security and Best Practices

Build a real foundation: command-line fluency, packet and crypto basics, and host hardening.
Practice on authorized lab systems. Use GSEC's breadth as the springboard to a specialization. All
practice is defensive.

## Hands-On Lab

Essentials walkthroughs. **Shared prerequisites** — a Linux workstation with `python3`, `openssl`,
`xxd`, in a lab. **Cost:** none.

### Lab 2.1 — GFACT: decode data representations

**Objective:** Read hex, binary, and encodings.

```bash
printf 'GIAC' | xxd            # ASCII -> hex (47 49 41 43)
python3 -c "print(bin(0x47), chr(0x47))"   # hex 0x47 -> binary + 'G'
printf 'R0lBQw==' | base64 -d; echo        # base64 decode -> GIAC
```

**Expected result:** `GIAC` shown as **hex 47 49 41 43**, binary/char, and base64-decoded — data
representation, the GFACT foundation.

**Negative test:** assume base64 is encryption; it is **encoding** (reversible, no key) — GFACT
distinguishes them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.2 — GISF: apply the CIA triad to a risk

**Objective:** Reason about a security fundamental.

```python
python3 - <<'PY'
risk={"threat":"stolen laptop","asset":"customer database extract"}
controls={"Confidentiality":"full-disk encryption + access control",
          "Integrity":"signed backups + checksums",
          "Availability":"offsite backup + recovery plan"}
for pillar,ctrl in controls.items(): print(f"{pillar:15}: {ctrl}")
print("GISF: map each risk to CIA and choose proportionate controls")
PY
```

**Expected result:** the risk mapped to **Confidentiality/Integrity/Availability** controls — the
GISF fundamentals.

**Negative test:** address only Confidentiality (encryption) and ignore Availability; a lost laptop
with no backup still causes an outage — cover all three.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — GSEC: verify integrity with a hash and cipher

**Objective:** Apply crypto and defense-in-depth hands-on.

```bash
echo "config-baseline" > file.txt
sha256sum file.txt                                   # integrity baseline
openssl enc -aes-256-cbc -pbkdf2 -in file.txt -out file.enc -pass pass:LabPass  # confidentiality
openssl enc -d -aes-256-cbc -pbkdf2 -in file.enc -pass pass:LabPass             # decrypt -> original
sha256sum file.txt                                   # unchanged hash proves integrity
```

**Expected result:** a **SHA-256** integrity baseline plus **AES-256** encrypt/decrypt round-trip —
core GSEC crypto and defense-in-depth.

**Negative test:** detect tampering by eyeballing the file; a one-byte change alters the **hash** —
use checksums, not inspection.

**Rollback:** `rm -f file.txt file.enc`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Essentials focus area (GFACT foundational tech, GISF security fundamentals, GSEC broad hands-on
security) builds the foundation for every GIAC specialization, validated with CyberLive practical
testing.

- [ ] I can decode data representations (GFACT).
- [ ] I can apply the CIA triad to a risk (GISF).
- [ ] I can verify integrity and apply crypto (GSEC).
- [ ] I understand GSEC as the broad hands-on foundation.
- [ ] I completed Labs 2.1–2.3 including each negative test.
