# Chapter 09: Keeping the Program Current and Career Paths

## Learning Objectives

- Explain PSDGP validity and CPD recertification.
- Track program and legal change over time.
- Plan a data governance career path around PSDGP.
- Relate PSDGP to related ICCP credentials and encyclopedia volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

PSDGP is **valid for three years** and is renewed through **Continuing Professional
Development (CPD)** — documented professional-development activity — rather than continuing-
education units or a re-examination. Because the credential rests on **law and mandate**,
currency is not only about the certification cycle: FOIA practice, privacy rules, records
schedules, and open-data mandates evolve, so a certified professional must **track statutory
change** as part of keeping the program current. Confirm the credential's terms and the course
content on ther2c.com and iccp.org before you certify or recertify.

## Design Considerations

Plan a path: earn a **core** ICCP credential (e.g., DGSP) for the general body of knowledge,
then **PSDGP** for the public-sector specialization; pair it with security/privacy credentials
(e.g., ISACA CDPSE, ISC2 CGRC) for the compliance dimension. Keep a **CPD log** from day one so
recertification is routine.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.ther2c.com/psdg" \
  | grep -oiE 'certification|exam|governance|public sector' | sort -u | head
```

## Validation and Troubleshooting

Confirm the currency and career facts:

```text
Validity: 3 years, renewed via CPD (not CEU/re-exam).
Path: core ICCP (DGSP) -> PSDGP -> pair with CDPSE/CGRC for privacy/compliance.
Track: FOIA, Privacy Act, NARA schedules, FISMA/FedRAMP, OPEN Data Act changes.
```

Common pitfalls: assuming a **one-time** certification (it expires in 3 years); and letting
**legal knowledge** go stale between renewals.

## Security and Best Practices

Keep privacy, records, and security knowledge **current** — the legal environment changes more
often than the exam. Maintain a CPD log and revisit the program's mission drivers when mandates
or administration priorities shift.

## References and Knowledge Checks

- ther2c.com/psdg and iccp.org: the PSDGP course, ICCP certification, and recertification terms.
- Related encyclopedia volumes: ISC2 (XL), ISACA (XLIV), Enterprise Cybersecurity (X), NetBox (LII).

**Knowledge checks**

1. How long is PSDGP valid, and how is it renewed?
2. What core credential underpins PSDGP, and what pairs well with it?
3. Why must legal knowledge be tracked between renewals?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with
`curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify program currency

**Objective:** Confirm the credential from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.ther2c.com/psdg" \
  | grep -oiE 'Mission Drivers|Deliverables|Roles and Responsibilities|Legal and Regulatory|certification' \
  | sort -u
```

**Expected result:** the four content areas and the certification reference — confirming the
program is unchanged before you study or recertify.

**Negative test:** rely on a cached course outline from years ago; law and mandates change —
**verify on ther2c.com/iccp.org**.

**Cleanup:** none.

### Lab 9.2 — Plan a governance career path

**Objective:** Sequence credentials by role.

```python
python3 - <<'PY'
paths={
 "Public-sector data steward":"DGSP (core) -> PSDGP",
 "Agency CDO":"PSDGP -> pair with CDPSE (privacy) / CGRC (governance)",
 "Privacy-focused":"PSDGP + ISACA CDPSE",
}
for role,path in paths.items(): print(f"{role:26}: {path}")
PY
```

**Expected result:** role-to-credential sequences — PSDGP built on a core cert and paired with
privacy/governance credentials.

**Negative test:** target PSDGP with no core knowledge or experience; meet the **prerequisite**
(degree+experience or a core ICCP cert) first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

PSDGP is valid three years and renewed through CPD, and its legal foundation means currency
includes tracking statutory change, not just the certification cycle. Build it on a core ICCP
credential, pair it with privacy/governance certs, keep a CPD log, and verify the program on
the authoritative sources.

- [ ] I can explain the 3-year CPD recertification.
- [ ] I can plan a governance career path around PSDGP.
- [ ] I can explain why legal knowledge must stay current.
- [ ] I can verify the program on ther2c.com/iccp.org.
- [ ] I completed Labs 9.1–9.2 including each negative test.
