# Chapter 09: Keeping the Program Current and Career Paths

## Learning Objectives

- Explain Palo Alto Networks certification validity and recertification.
- Track program change, including the 2025 role-based restructure.
- Plan a certification path by role across the three tracks.
- Relate these credentials to Volume XVI and the encyclopedia's security volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Palo Alto Networks certifications are tied to the platform and carry a validity period —
**typically two years** — after which they are renewed by passing a current exam (or a
higher-level one). The program was **rebuilt in 2025** into the role-based framework, retiring
the legacy code-based exams (PCNSA/PCNSE/PCCSE and the rest), so anyone returning to certify
must confirm the **current** credential names and blueprints. Because the platform (PAN-OS,
Cortex XDR/XSIAM/XSOAR, Prisma/Cortex Cloud) evolves quickly, currency means tracking product
change as well as the certification cycle. Confirm the framework on paloaltonetworks.com before
you study or renew.

## Design Considerations

Plan by **role and track**: start with the shared **Foundational** credentials, take the track
**Professional**, then the **Specialist** credentials for your role, and the **Architect**
credential for design roles. Pair credentials across tracks where your job spans them (e.g.,
Network Security + Cloud Security). Keep skills current with platform releases.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.paloaltonetworks.com/services/education/certification" \
  | grep -oiE 'Foundational|Professional|Specialist|Architect|Network Security|Security Operations|Cloud Security' \
  | sort -u
```

## Validation and Troubleshooting

Confirm the currency and career facts:

```text
Validity: typically 2 years; renew by current (or higher) exam. Confirm on the portal.
2025 restructure: legacy code exams retired -> role-based framework (levels + tracks).
Path: Foundational -> track Professional -> Specialist (role) -> Architect.
```

Common pitfalls: studying a **retired** exam; and letting a certification **lapse** past its
window.

## Security and Best Practices

Keep knowledge current with the platform (PAN-OS, Cortex, Prisma/Cortex Cloud move fast). Track
the program on the official site, recertify on time, and combine credentials for your role. Keep
all practice **authorized and defensive**.

## References and Knowledge Checks

- paloaltonetworks.com/services/education/certification: the role-based framework and recert terms.
- Volume XVI (Palo Alto Networks Security): the product platform in depth.
- Related security volumes: Cisco Security (XXV), Fortinet (XIX), Zscaler (XXXV), CrowdStrike (L), Cybersecurity (X), ISC2 (XL).

**Knowledge checks**

1. What is the typical validity period, and how do you recertify?
2. What changed in the 2025 restructure?
3. What path suits a SOC analyst?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with
`curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current framework

**Objective:** Read the current levels and tracks.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.paloaltonetworks.com/services/education/certification" \
  | grep -oiE 'Foundational|Professional|Specialist|Architect|Network Security|Security Operations|Cloud Security' \
  | sort -u
```

**Expected result:** the current levels and tracks — confirming scope before study or renewal.

**Negative test:** rely on a pre-2025 PCNSE-era list; the program was **rebuilt** — verify on
paloaltonetworks.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a certification path

**Objective:** Map a role to a track and level sequence.

```python
python3 - <<'PY'
paths={"Firewall engineer":"Foundational -> Network Security Professional -> NGFW Engineer -> Architect",
       "SOC analyst":"Foundational -> SecOps Professional -> XDR/XSIAM Analyst",
       "Automation engineer":"Foundational -> SecOps Professional -> XSOAR Engineer",
       "Cloud security engineer":"Foundational -> Cloud Security Professional -> Cloud Security Engineer"}
for role,path in paths.items(): print(f"{role:22}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** target a Specialist exam with no Foundational base; climb the **levels** in
order.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Palo Alto Networks certifications are valid roughly two years and renewed by current exam; the
2025 restructure retired the legacy code-based exams for the role-based framework, and the
platform evolves quickly. Plan a path by role and track from Foundational upward, pair
credentials as your job spans tracks, and verify the current program on the official site.

- [ ] I can explain validity and recertification.
- [ ] I can explain the 2025 restructure.
- [ ] I can plan a role-based path across the tracks.
- [ ] I can verify the current program on paloaltonetworks.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
