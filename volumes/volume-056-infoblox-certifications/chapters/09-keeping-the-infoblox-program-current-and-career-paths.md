# Chapter 09: Keeping the Infoblox Program Current and Career Paths

## Learning Objectives

- Explain Infoblox certification validity and digital badges.
- Track program change — Universal DDI and Threat Defense additions.
- Plan an Infoblox certification path by role.
- Relate Infoblox credentials to the encyclopedia's network and security volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Infoblox certifications are issued as **digital badges/credentials** through Infoblox
Education, with topic-area blueprints rather than published weightings. The program
tracks the platform: as Infoblox moved toward **cloud-native Universal DDI** and expanded
**Threat Defense**, it added microcredentials alongside the classic **NIOS DDI** exams,
and offers vendor-agnostic **Industry Learning** credentials. Confirm the current catalog
and any validity terms on the education site before you study.

## Design Considerations

Plan by **role and product**: DDI operators/admins follow **INO → INA → INE**; cloud-DDI
teams take **Universal DDI**; security teams take **Threat Defense** (plus vendor-agnostic
**DSA/DSP**); network-automation teams take **NetMRI (IMA)**. Vendor-agnostic **DDIA/
DDIP** build portable fundamentals.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.infoblox.com/infoblox-education/" \
  | grep -oiE 'NIOS DDI|Universal DDI|Threat Defense|NetMRI|DDI (Associate|Professional)|DNS Security' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
education.infoblox.com / launchpad.education.infoblox.com:
  - product: INO/INA/INE, IMA; Universal DDI + Threat Defense microcredentials
  - industry learning: DDIA/DDIP, DSA/DSP
  - digital badges; topic-area blueprints (no weightings)
```

Common pitfalls: studying stale NIOS-only material (Universal DDI is current); and
assuming published weightings.

## Security and Best Practices

Study the current **topic areas**, practice on NIOS/Universal DDI/Threat Defense lab
environments, and combine credentials for your role (e.g., INO → INA → INE, or Universal
DDI + Threat Defense). Track program additions so content changes don't surprise you.

## References and Knowledge Checks

- education.infoblox.com: the certification catalog, topic areas, and digital badges.

**Knowledge checks**

1. How are Infoblox certifications issued?
2. Which credentials reflect the move to cloud-native DDI and DNS security?
3. What path suits an on-prem DDI administrator?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell
with `curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current program

**Objective:** Read the current credential families.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.infoblox.com/infoblox-education/" \
  | grep -oiE 'NIOS DDI|Universal DDI|Threat Defense|NetMRI' | sort -u
```

**Expected result:** the current product families (**NIOS DDI, Universal DDI, Threat
Defense, NetMRI**) — confirming scope before you study.

**Negative test:** trust a cached NIOS-only list; **Universal DDI/Threat Defense** are
current — confirm on infoblox.com.

**Cleanup:** none.

### Lab 9.2 — Plan a path

**Objective:** Map a role to an Infoblox certification sequence.

```bash
python3 - <<'PY'
paths={"DDI Admin (on-prem)":"INO -> INA -> INE",
       "Cloud DDI":"Universal DDI",
       "DNS Security":"Threat Defense (+ DSA/DSP)",
       "Network Automation":"NetMRI (IMA)",
       "Fundamentals":"DDIA -> DDIP"}
for role,path in paths.items(): print(f"{role:22}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** collect credentials at random; **sequence by role/product** for a
coherent path.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Infoblox certifications are digital badges with topic-area blueprints, spanning on-prem
NIOS DDI (INO/INA/INE), cloud-native Universal DDI, Threat Defense, NetMRI (IMA), and
vendor-agnostic Industry Learning (DDIA/DDIP, DSA/DSP). Plan a path by role and verify
the current catalog before you study.

- [ ] I can explain how credentials are issued.
- [ ] I can name which credentials cover cloud DDI and DNS security.
- [ ] I can plan a role-based certification path.
- [ ] I can verify the current program on infoblox.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
