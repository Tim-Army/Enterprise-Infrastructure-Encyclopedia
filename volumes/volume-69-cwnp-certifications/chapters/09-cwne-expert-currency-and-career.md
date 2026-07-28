# Chapter 09: The Expert Level, Currency, and Career Paths

## Learning Objectives

- Explain the CWNE and CWISE expert requirements.
- Understand CWNP validity and recertification.
- Track program change (Prometric delivery, Wi-Fi 6E/7).
- Plan a CWNP path and relate it to the encyclopedia's wireless volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

The two **expert** credentials are the summit of each track. **CWNE** (Certified Wireless Network
Expert) requires the enterprise Wi-Fi professionals — **CWNA, CWSP, CWAP, CWDP, and CWISA** — plus
a recognized **third-party Wi-Fi certification**, documented **experience**, professional
**endorsements**, and a **board application review**; it is earned, not merely tested. **CWISE**
(Certified Wireless IoT Solutions Expert) is the IoT summit, requiring **CWNA, CWIIP, CWICP, and
CWIDP** plus a third-party IoT/wireless certification and review. CWNP certifications are **valid
three years** and renewed by re-examination or earning higher credentials. The program evolves:
exams moved to **Prometric** (1 August 2024), and content now emphasizes **Wi-Fi 6/6E (802.11ax)**
and introduces **Wi-Fi 7 (802.11be)**. Because CWNP is **vendor-neutral**, it complements the
vendor wireless certifications (Aruba, Cisco, MikroTik) — the theory here applies to all of them.

## Design Considerations

Plan the **expert path** early — CWNE/CWISE require multiple professional certs, experience, and
endorsements, so map them out. Keep skills current with **Wi-Fi 6E/7**. Pair CWNP's vendor-neutral
theory with a **vendor certification** (Aruba/Cisco/MikroTik) for both breadth and depth.
Recertify before the three-year expiry.

## Implementation and Automation

The labs assess CWNE readiness, plan a path, and verify the current program.

## Validation and Troubleshooting

Confirm the expert and currency facts:

```text
CWNE: CWNA+CWSP+CWAP+CWDP+CWISA + 3rd-party Wi-Fi cert + experience + endorsements + board review.
CWISE: CWNA+CWIIP+CWICP+CWIDP + 3rd-party IoT/wireless cert + review.
Validity 3 years. Delivery: Prometric (from 1 Aug 2024). Focus: Wi-Fi 6/6E + Wi-Fi 7.
```

Common pitfalls: expecting CWNE from a **single exam** (it needs multiple certs + review); and
assuming **Pearson VUE** delivery (now **Prometric**).

## Security and Best Practices

Build the **professional certs** and real **experience** toward CWNE/CWISE, keep current with
**Wi-Fi 6E/7**, and pair vendor-neutral theory with **vendor certification**. Recertify on time.
Keep all wireless analysis **authorized and defensive**.

## References and Knowledge Checks

- cwnp.com/certifications: the program, expert requirements, and recertification.
- Related encyclopedia volumes: HPE Aruba (LXIV), MikroTik (LXVIII), Cisco (XXV), Wireshark (XX), Network Foundations (II).

**Knowledge checks**

1. What does CWNE require beyond passing exams?
2. Who delivers CWNP exams since August 2024?
3. What Wi-Fi generations does the current exam content emphasize?

## Hands-On Lab

Expert and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with `curl`
and `python3`. **Cost:** none.

### Lab 9.1 — Assess CWNE readiness

**Objective:** Check the CWNE prerequisites.

```python
python3 - <<'PY'
have={"CWNA":True,"CWSP":True,"CWAP":True,"CWDP":False,"CWISA":False,"third_party":True,"endorsements":False}
missing=[k for k,v in have.items() if not v]
print("CWNE ready:", not missing)
print("still needed:", missing)
PY
```

**Expected result:** CWNE readiness with the **missing requirements** listed (CWDP, CWISA,
endorsements) — a concrete plan.

**Negative test:** apply for CWNE with only CWNA/CWSP; it needs **all five certs + review** —
complete them first.

**Cleanup:** none.

### Lab 9.2 — Plan a CWNP + vendor path

**Objective:** Combine vendor-neutral and vendor certs.

```python
python3 - <<'PY'
plan={"Foundation":"CWNA (vendor-neutral RF/802.11)",
      "Vendor depth":"Aruba (LXIV) / MikroTik wireless (LXVIII) / Cisco",
      "Professional":"CWSP + CWAP + CWDP","Expert":"CWNE (with 3rd-party cert + review)"}
for stage,step in plan.items(): print(f"{stage:14}: {step}")
PY
```

**Expected result:** a path pairing **CWNP theory** with a **vendor certification** toward CWNE —
breadth plus depth.

**Negative test:** rely on vendor certs alone with no RF theory; **CWNA/CWNP** gives the
vendor-neutral foundation — combine them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CWNE and CWISE experts are earned through multiple professional certs, experience, third-party
certification, and board review. CWNP certifications are valid three years, delivered by Prometric
since 2024, with content on Wi-Fi 6/6E and Wi-Fi 7. Plan the expert path early and pair
vendor-neutral theory with vendor certification.

- [ ] I can state the CWNE/CWISE requirements.
- [ ] I can assess CWNE readiness.
- [ ] I can plan a CWNP-plus-vendor path.
- [ ] I can verify the current program on cwnp.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
