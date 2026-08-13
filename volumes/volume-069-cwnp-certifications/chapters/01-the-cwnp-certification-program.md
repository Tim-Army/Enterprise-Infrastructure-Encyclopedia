# Chapter 01: The CWNP Certification Program

## Learning Objectives

- Explain the CWNP vendor-neutral wireless certification program and its six career levels.
- Identify CWNA as the foundation for the professional level.
- Distinguish the enterprise Wi-Fi track (CWNE) from the IoT track (CWISE).
- Understand exam delivery (Prometric since 2024) and the Wi-Fi 6/6E/7 focus.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**CWNP** (Certified Wireless Network Professional) is the **vendor-neutral** standard for
enterprise wireless certification — it teaches the **802.11 (Wi-Fi)** and wireless-IoT principles
that underlie every vendor's gear (Cisco, Aruba, MikroTik, and others). The program has **six
career levels**. **Entry:** **CWSS** (Sales Specialist) and **CWTS** (Technology Specialist).
**Administrator:** **CWNA** (Certified Wireless Network Administrator, exam **CWNA-109**) — the
**foundation** that covers RF fundamentals, 802.11, site surveying, and enterprise security, and
the gateway to the professional level. **Professional** splits into a **Wi-Fi track** — **CWSP**
(Security), **CWAP** (Analysis), **CWDP** (Design) — and an **IoT track** — **CWISA** (IoT
Solutions Administrator), **CWICP** (Connectivity), **CWIIP** (Integration), **CWIDP** (Design).
**Expert** likewise has two summits: **CWNE** (enterprise Wi-Fi, requiring CWNA + CWSP + CWAP +
CWDP + CWISA, a third-party certification, and a board application review) and **CWISE** (IoT).

Exams are delivered by **Prometric** (the program transitioned from Pearson VUE on 1 August 2024)
at testing centers and via remote proctoring, and certificates are **valid three years**. The
2026 exam updates emphasize **802.11ax (Wi-Fi 6/6E)** and introduce foundational **802.11be
(Wi-Fi 7)**. Because CWNP is vendor-neutral and RF/analysis-heavy, this volume teaches each level
with hands-on RF math and 802.11 protocol-analysis walkthroughs.

> **Scope.** Wireless analysis uses packet capture. Every lab is **authorized capture and
> analysis** of your own or a lab network — never interception of networks you don't control.

## Design Considerations

Start with **CWNA** — it is the foundation for both professional tracks. Choose the **Wi-Fi
track** (CWSP/CWAP/CWDP → CWNE) or the **IoT track** (CWISA/CWICP/CWIIP/CWIDP → CWISE) by role.
Study the **current RF and 802.11** (Wi-Fi 6E's 6 GHz band and Wi-Fi 7's features are now in
scope). Verify exam codes on cwnp.com; they revise on a cycle.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.cwnp.com/certifications/" \
  | grep -oiE 'CWNA|CWSP|CWAP|CWDP|CWISA|CWNE|CWISE|CWTS|CWSS' | sort -u
```

## Validation and Troubleshooting

The verified program facts (cwnp.com, 28 July 2026):

```text
6 levels. Entry: CWSS, CWTS. Administrator: CWNA (CWNA-109) = FOUNDATION.
Professional Wi-Fi: CWSP, CWAP, CWDP. Professional IoT: CWISA, CWICP, CWIIP, CWIDP.
Expert: CWNE (Wi-Fi; needs CWNA+CWSP+CWAP+CWDP+CWISA + 3rd-party + board review); CWISE (IoT).
Delivery: Prometric (from Pearson VUE, 1 Aug 2024). Validity 3 years. Focus: Wi-Fi 6/6E + Wi-Fi 7.
```

Common pitfalls: assuming **Pearson VUE** (it moved to **Prometric**); and thinking there is one
expert cert (there are **two** — CWNE and CWISE).

## Security and Best Practices

Build on the **CWNA** foundation, study **current RF/802.11** (Wi-Fi 6E/7), and practice analysis
**only on authorized networks**. Verify certifications on cwnp.com — third-party dumps are neither
authoritative nor permitted.

## References and Knowledge Checks

- cwnp.com/certifications: the program, career levels, and exams.
- CWNP learning resources and the CWNA study guide: RF and 802.11 fundamentals.

**Knowledge checks**

1. Which certification is the foundation for the professional level?
2. What are the two expert-level certifications?
3. Who delivers CWNP exams as of 2024?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the career levels

**Objective:** Read the program from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.cwnp.com/certifications/" \
  | grep -oiE 'CWNA|CWSP|CWAP|CWDP|CWISA|CWICP|CWIIP|CWIDP|CWNE|CWISE' | sort -u
```

**Expected result:** the CWNP certifications across the levels — the program map.

**Negative test:** assume one expert cert and Pearson VUE delivery; there are **two experts**
(CWNE/CWISE) and delivery is **Prometric** — confirm on cwnp.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map certifications to levels and tracks

**Objective:** Record the structure.

```python
python3 - <<'PY'
prog={"Entry":["CWSS","CWTS"],"Administrator":["CWNA (CWNA-109)"],
      "Professional Wi-Fi":["CWSP","CWAP","CWDP"],
      "Professional IoT":["CWISA","CWICP","CWIIP","CWIDP"],
      "Expert":["CWNE (Wi-Fi)","CWISE (IoT)"]}
for level,certs in prog.items(): print(f"{level:20}: {', '.join(certs)}")
PY
```

**Expected result:** the certifications by level and track — your study map.

**Negative test:** target a professional cert with no **CWNA**; CWNA is the **foundation** — earn
it first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a track

**Objective:** Sequence certifications for a role.

```python
python3 - <<'PY'
paths={"WLAN security":"CWNA -> CWSP","WLAN troubleshooting":"CWNA -> CWAP",
       "WLAN design":"CWNA -> CWDP","Wi-Fi expert":"CWNA+CWSP+CWAP+CWDP+CWISA -> CWNE",
       "IoT expert":"CWNA+CWIIP+CWICP+CWIDP -> CWISE"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the tracks this volume follows.

**Negative test:** attempt CWNE without the required professional certs and endorsement; **CWNE
needs CWNA+CWSP+CWAP+CWDP+CWISA + review** — complete them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CWNP is the vendor-neutral wireless standard with six career levels: entry (CWSS/CWTS), the CWNA
foundation, professional Wi-Fi (CWSP/CWAP/CWDP) and IoT (CWISA/CWICP/CWIIP/CWIDP) tracks, and two
experts (CWNE/CWISE). Exams are delivered by Prometric with three-year validity and a Wi-Fi 6/6E/7
focus. Start with CWNA and pick a track.

- [ ] I can name the six career levels.
- [ ] I can identify CWNA as the foundation.
- [ ] I can distinguish the CWNE and CWISE experts.
- [ ] I can plan a certification track.
- [ ] I completed Labs 1.1–1.3 including each negative test.
