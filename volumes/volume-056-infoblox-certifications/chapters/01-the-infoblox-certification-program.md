# Chapter 01: The Infoblox Certification Program

## Learning Objectives

- Describe Infoblox and what its certifications validate.
- Identify the product and vendor-agnostic credential families.
- Explain delivery, digital badges, and the topic-based model.
- Access the WAPI and NIOS CLI used throughout this volume.
- Verify program facts from the authoritative source.

## Theory and Architecture

**Infoblox** is the market leader in **DDI** — the integration of **DNS**, **DHCP**, and
**IP address management (IPAM)** — plus **DNS-layer security** (Threat Defense) and
network automation (NetMRI). Its platform spans the on-premises **NIOS Grid**, the
cloud-native **Universal DDI** (NIOS-X and the Infoblox Portal), and **BloxOne Threat
Defense**. **Infoblox Education** runs the certification program, which validates the
skills to deploy and operate these products.

This is a **certification-tracks** volume, like the other vendor volumes: it maps the
program — which credentials exist, their **topic areas**, and levels — and teaches each
with a hands-on walkthrough. The program has two families:

- **Product certifications:** NIOS DDI **Operator (INO)**, **Administrator (INA)**, and
  **Expert (INE)**; **NetMRI Administrator (IMA)**; plus **Universal DDI** and **Threat
  Defense** microcredentials (knowledge checks).
- **Industry Learning (vendor-agnostic):** **DDI Associate (DDIA)** / **Professional
  (DDIP)** and **DNS Security Associate (DSA)** / **Professional (DSP)**.

Every credential was **verified against launchpad.education.infoblox.com on 27 July
2026**. Infoblox publishes **topic areas** but not question counts or weightings, so this
volume maps a lab to each topic area.

## Design Considerations

Choose by role and product. **NIOS DDI** (INO → INA → INE) is the on-prem Grid path;
**Universal DDI** covers the cloud-native platform; **Threat Defense** covers DNS
security; **NetMRI** covers network automation. The **Industry Learning** credentials are
vendor-neutral DDI/DNS-security fundamentals.

## Implementation and Automation

Labs use the **WAPI** (the NIOS REST API) and the **NIOS CLI**:

```bash
# WAPI: authenticated REST over HTTPS to the Grid Manager
curl -sS -k -u admin:infoblox "https://<grid-master>/wapi/v2.13/grid"
```

## Validation and Troubleshooting

Confirm the program facts:

```text
launchpad.education.infoblox.com:
  - product: INO, INA, INE (NIOS DDI); IMA (NetMRI); Universal DDI + Threat Defense (knowledge checks)
  - industry learning: DDIA/DDIP, DSA/DSP (vendor-agnostic)
  - topic areas published (no weightings); digital badges issued
```

Common pitfalls: confusing **NIOS** (on-prem Grid) with **Universal DDI** (cloud-native);
and assuming published weightings (topic areas only).

## Security and Best Practices

Study the **topic areas** for your target credential, practice on a NIOS/Universal DDI
lab environment, treat Grid and WAPI access as privileged (RBAC, API auth over TLS), and
follow the INO → INA → INE progression.

## References and Knowledge Checks

- education.infoblox.com: the certification catalog, topic areas, and digital badges.

**Knowledge checks**

1. What does DDI stand for?
2. Name the three NIOS DDI certification levels.
3. How do NIOS and Universal DDI differ?

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell
with `curl`; access to a NIOS Grid (or the WAPI docs) for the API checks. **Cost:** none
for the read-only checks.

### Lab 1.1 — Enumerate the credential families

**Objective:** State the program structure.

```bash
python3 - <<'PY'
fam={"NIOS DDI":"INO, INA, INE","NetMRI":"IMA",
     "Microcredentials":"Universal DDI, Threat Defense",
     "Industry Learning":"DDIA, DDIP, DSA, DSP"}
for k,v in fam.items(): print(f"{k:18}: {v}")
PY
```

**Expected result:** the credential families mapped to their codes — the program map.

**Negative test:** rely on an old cert list; Infoblox revises the program (Universal DDI
is newer) — confirm on education.infoblox.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Authenticate to the WAPI

**Objective:** Confirm REST access to a Grid.

```bash
curl -sS -k -u admin:infoblox "https://<grid-master>/wapi/v2.13/grid" \
  | python3 -c "import sys,json;print('grid objects:',len(json.load(sys.stdin)))"
```

**Expected result:** a JSON response describing the **Grid** — proof WAPI access works
(the basis for later labs).

**Negative test:** call the WAPI without credentials; NIOS returns **401** — authenticate
first.

**Rollback:** none (read-only).

### Lab 1.3 — Confirm the CLI/console path

**Objective:** State the management surfaces.

```text
# NIOS management: Grid Manager UI, WAPI (REST), and the CLI (console/SSH on members).
# Universal DDI: the Infoblox Portal + NIOS-X hosts.
"surfaces: Grid Manager UI, WAPI, CLI (NIOS); Infoblox Portal (Universal DDI)"
```

**Expected result:** the correct management surfaces per product — where you operate
Infoblox.

**Negative test:** assume one UI covers both; **NIOS** and **Universal DDI** have
distinct management planes — use the right one.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Infoblox certification program validates DDI and DNS-security skills across product
certifications (NIOS DDI INO/INA/INE, NetMRI IMA, Universal DDI and Threat Defense
microcredentials) and vendor-agnostic Industry Learning (DDIA/DDIP, DSA/DSP), delivered
by Infoblox Education with topic-area blueprints.

- [ ] I can name the credential families and codes.
- [ ] I can explain NIOS vs Universal DDI.
- [ ] I can authenticate to the WAPI.
- [ ] I can identify the management surfaces.
- [ ] I completed Labs 1.1–1.3 including each negative test.
