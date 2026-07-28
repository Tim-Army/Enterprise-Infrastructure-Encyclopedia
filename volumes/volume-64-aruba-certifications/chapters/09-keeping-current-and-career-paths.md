# Chapter 09: Keeping the Aruba Program Current and Career Paths

## Learning Objectives

- Explain HPE Aruba Networking certification validity and recertification.
- Track program change, including the HPE Aruba rebrand and renumbering.
- Plan an Aruba certification path by role.
- Relate Aruba credentials to the encyclopedia's networking volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

HPE Aruba Networking certifications are tied to the platform (AOS-CX, Central, ClearPass) and
carry a validity period — **typically three years** under HPE's certification policy — after
which they are renewed by passing a current exam. The program itself changes: it was
**rebranded** from "Aruba Certified" to **HPE Aruba Networking Certified** and **renumbered**
(the HPE6-/HPE7- codes), and tracks and Advanced Product Certifications evolve with the
portfolio. Because of that, confirm the **current tracks, codes, and recertification terms** on
certification-learning.hpe.com before you study or renew.

## Design Considerations

Plan by **role**: campus, switching, security, wireless, or data center — start at **Associate**,
climb to **Professional**, then **Expert**, and add the **Network Architect** design credential
or **Advanced Product Certifications** (ClearPass, Central) as your role needs. Recertify before
expiry by taking a current exam.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://certification-learning.hpe.com/tr/certifications/aruba" \
  | grep -oiE 'Associate|Professional|Expert|Network Architect|Campus Access|Switching|Network Security|Data Center' \
  | sort -u
```

## Validation and Troubleshooting

Confirm the currency and career facts:

```text
Validity: typically 3 years (HPE policy); renew by current exam. Confirm on the portal.
Rebrand: "Aruba Certified" -> "HPE Aruba Networking Certified" (HPE6-/HPE7- codes).
Path: Associate -> Professional -> Expert (per track) + Network Architect / APC.
```

Common pitfalls: studying **legacy Aruba** codes/names; and letting a certification **lapse**
past its validity window.

## Security and Best Practices

Keep skills current with the platform (AOS-CX/Central/ClearPass releases move quickly). Track
the program on the HPE portal, recertify on time, and combine credentials for your role (e.g.,
Campus Access + Network Security for a segmentation-focused engineer).

## References and Knowledge Checks

- certification-learning.hpe.com and hpe.com/networkingtraining: the program, datasheets, and recert terms.
- Related encyclopedia volumes: Cisco (III, XXV, XXVII–XXX), Juniper (XXXI), Arista (LXII), NetBox (LII), Python for Network Engineers (LVIII), Ansible (LIX).

**Knowledge checks**

1. What is the typical validity period, and how do you recertify?
2. What changed in the rebrand from "Aruba Certified"?
3. What path suits a campus security engineer?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with
`curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current program

**Objective:** Read the current tiers and tracks.

```bash
curl -sSL -A "Mozilla/5.0" "https://certification-learning.hpe.com/tr/certifications/aruba" \
  | grep -oiE 'Associate|Professional|Expert|Campus Access|Switching|Network Security|Data Center|Mobility' \
  | sort -u
```

**Expected result:** the current tiers and tracks — confirming scope before study or renewal.

**Negative test:** rely on a cached legacy cert list; the program was **rebranded and
renumbered** — verify on certification-learning.hpe.com.

**Cleanup:** none.

### Lab 9.2 — Plan a path

**Objective:** Map a role to an Aruba certification sequence.

```python
python3 - <<'PY'
paths={"Campus engineer":"ACA/ACP Campus Access -> ACX (Switching/Mobility)",
       "Security engineer":"ACA/ACP/ACX Network Security + APC-ClearPass",
       "Wireless engineer":"Campus Access + ACX Campus Access Mobility (HPE7-A07)",
       "DC engineer":"ACP Data Center (HPE7-A05) -> Network Architect DC (HPE7-A04)",
       "Automation":"any track + Central/pyaoscx/Ansible aos_cx"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** target an Expert exam with no Associate/Professional base; climb the **tiers**
in order.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

HPE Aruba Networking certifications are valid roughly three years and renewed by current exam;
the program was rebranded from "Aruba Certified" and renumbered to HPE6-/HPE7- codes, and its
tracks and APCs evolve. Plan a path by role from Associate upward, add Network Architect or APCs,
and verify the current program on the HPE portal.

- [ ] I can explain validity and recertification.
- [ ] I can explain the rebrand and renumbering.
- [ ] I can plan a role-based Aruba path.
- [ ] I can verify the current program on the HPE portal.
- [ ] I completed Labs 9.1–9.2 including each negative test.
