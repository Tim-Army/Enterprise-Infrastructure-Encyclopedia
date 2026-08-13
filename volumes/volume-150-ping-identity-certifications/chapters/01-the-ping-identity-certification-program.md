# Chapter 01: The Ping Identity Certification Program

![The Ping Identity certification program and the portfolio beneath it. The program is product-specific: proctored exams at the Certified Professional level, plus Advanced Administrator and Expert tiers, each tied to a product in the portfolio. Certified Professional exams include PingFederate for federation, PingAccess for access management, PingDirectory for the directory, PingOne for cloud SSO and MFA, PingOne DaVinci for identity orchestration, PingOne Advanced Identity Cloud, PingOne Identity Governance, and PingAM for access management. Each exam is remotely proctored, multiple choice, roughly seventy questions in ninety minutes, priced around three hundred ninety-five US dollars, with pass marks that vary by product from sixty-four to seventy-five percent, and a voucher valid for a single attempt. The PingFederate exam is seventy items with a sixty-four percent pass mark. Preparation is through Ping Identity Training with learning pathways and on-demand courses. The portfolio reflects the 2023 Ping Identity and ForgeRock merger, spanning Ping-origin products PingFederate, PingAccess, PingDirectory, PingOne, PingID, PingOne DaVinci, and PingOne Protect, and ForgeRock-origin products rebranded as PingOne Advanced Identity Cloud, PingAM, PingIDM, PingDS, PingGateway, and PingOne Identity Governance, covering workforce identity, customer identity, federation, access management, directory, governance, orchestration, and threat protection.](../../../diagrams/volume-150-ping-identity-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Product-specific certifications over the merged Ping + ForgeRock identity portfolio.*

## Learning Objectives

- Describe the Ping Identity certification program — product-specific, proctored, at Professional and Expert levels.
- Place the exams across the portfolio (federation, access, directory, cloud, orchestration, governance).
- Understand the Ping + ForgeRock merger that shaped the portfolio.
- Recognize Ping's position in the identity-and-access-management landscape.

## What Ping Identity is

Ping Identity is a leader in **identity and access management (IAM)** — the platform organizations use to authenticate users, authorize access, and federate identity across applications, for both **workforce** (employees) and **customer** (CIAM) identity. Where [Okta (LXXVI)](../../volume-076-okta-certifications/README.md) is the cloud-first IDaaS generalist and [SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md) owns identity governance, **Ping's depth is federation and access management** — the enterprise-grade **PingFederate** federation server and a broad portfolio spanning SSO, MFA, directory, orchestration, and governance.

## The Ping + ForgeRock merger

The single most important context is that Ping Identity **merged with ForgeRock in 2023**, combining two of the largest independent IAM vendors. The result is a portfolio with **two heritages**:

| Origin | Products |
|:---|:---|
| **Ping** | PingFederate, PingAccess, PingDirectory, PingOne, PingID, PingOne DaVinci, PingOne Protect |
| **ForgeRock** (rebranded) | PingOne Advanced Identity Cloud, PingAM, PingIDM, PingDS, PingGateway, PingOne Identity Governance |

The ForgeRock products were **rebranded** into the Ping naming (ForgeRock Identity Cloud → **PingOne Advanced Identity Cloud**; ForgeRock AM → **PingAM**), and the certification program now covers **both** heritages. This is why the program is broad and product-specific rather than a tidy ladder — it reflects a large, merged portfolio.

## The product-specific program

Ping's certifications are **product-specific**: each exam certifies you on **one product**, at a **Certified Professional** level (with **Advanced Administrator** and **Expert** tiers above for some products). The verified Certified Professional exams include:

| Exam | Code | Product area |
|:---|:---|:---|
| **Certified Professional – PingFederate** | PFP-001 | Federation / SSO |
| **Certified Professional – PingAccess** | PAP-001 | Access management |
| **Certified Professional – PingDirectory** | PDP-001 | Directory |
| **Certified Professional – PingOne** | POP-001 | Cloud SSO + MFA |
| **Certified Professional – PingOne DaVinci** | PODV-001 | Identity orchestration |
| **Certified Professional – PingOne Advanced Identity Cloud** | PAICP-001 | Full IAM SaaS (ex-ForgeRock) |
| **Certified Professional – PingOne Identity Governance** | IGAP-001 | Governance |
| **Certified Professional – PingAM** | PT-AM-CPE | Access management (ex-ForgeRock) |

## What is published

Ping publishes the exam mechanics clearly — a refreshing contrast to the portal-gated vendors:

- **Format:** remotely **proctored**, **multiple choice**, roughly **70 questions in 90 minutes** (PingOne is 60–70; PingAM is ~100).
- **Price:** **~$395** (€365 / £310); a voucher is valid for a **single attempt**.
- **Pass marks vary by product:** PingFederate and PingAccess **64%**, PingDirectory **67%**, PingOne DaVinci **68%**, PingOne Advanced Identity Cloud and Identity Governance **70%**, PingOne **75%**.

Preparation is via **Ping Identity Training** (learning pathways, on-demand courses, an Authorized Training Partner network). The lab reads the program by product and pass mark.

## Hands-On Lab

The labs in this volume model IAM concepts in Python at no cost — Ping is enterprise software, so the labs model the *decisions and disciplines* the certifications test (federation trust, token scopes, adaptive auth, orchestration). Ping offers **free trials** of PingOne.

### Lab 1.1 — Read the product-specific program

**Objective:** Place an exam by product, portfolio heritage, and pass mark.

```bash
python3 - <<'EOF'
EXAMS = [
  # exam,                          code,       origin,      area,               pass%
  ("PingFederate",                 "PFP-001",  "Ping",      "federation/SSO",   64),
  ("PingAccess",                   "PAP-001",  "Ping",      "access mgmt",      64),
  ("PingDirectory",                "PDP-001",  "Ping",      "directory",        67),
  ("PingOne",                      "POP-001",  "Ping",      "cloud SSO+MFA",    75),
  ("PingOne DaVinci",              "PODV-001", "Ping",      "orchestration",    68),
  ("PingOne Adv. Identity Cloud",  "PAICP-001","ForgeRock", "full IAM SaaS",    70),
  ("PingOne Identity Governance",  "IGAP-001", "ForgeRock", "governance",       70),
  ("PingAM",                       "PT-AM-CPE","ForgeRock", "access mgmt",      70),
]
print(f"{'exam (Certified Professional)':32}{'code':11}{'origin':11}{'pass%':>6}   area")
for name, code, origin, area, passpct in EXAMS:
    print(f"{name:32}{code:11}{origin:11}{passpct:>5}%   {area}")
print("\nHow to read it:")
print("  - PRODUCT-SPECIFIC: each exam certifies ONE product (unlike a general IAM")
print("    cert). Pick the products your org runs.")
print("  - TWO HERITAGES: Ping-origin (PingFederate/Access/Directory/One/DaVinci) +")
print("    ForgeRock-origin, rebranded (Advanced Identity Cloud, PingAM, Governance).")
print("    The 2023 merger is why the portfolio — and the program — is this broad.")
print("  - PASS MARKS VARY by product (64%-75%). PingOne is the strictest (75%).")
print("  - all ~$395, proctored, MC, ~70Q/90min — Ping PUBLISHES its mechanics")
print("    (refreshingly, vs the portal-gated vendors).")
print("\nCertify for the products you operate: a federation shop takes PingFederate; a")
print("ForgeRock-heritage shop takes PingAM / Advanced Identity Cloud; a cloud-first")
print("shop takes PingOne. The program mirrors the merged portfolio, product by product.")
EOF
```

**Expected result:** The Certified Professional exams placed by product, Ping-versus-ForgeRock heritage, and their varying pass marks (64–75%), all proctored MC at ~$395. The product-specific lesson is that Ping certifies you on individual products across a merged two-heritage portfolio — you certify for the products your organization runs, not on a single general IAM ladder.

**Negative test:** Expecting one general "Ping Identity certification." The program is product-specific — PingFederate, PingAccess, PingOne, and PingAM are separate exams, and you pick the ones matching the products you operate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map the merged portfolio to identity functions

**Objective:** See how the portfolio covers the IAM functions.

```bash
python3 - <<'EOF'
PORTFOLIO = [
  # function,               product(s),                       chapter
  ("federation / SSO",      "PingFederate, PingOne",          "03, 05"),
  ("access management",     "PingAccess, PingAM",             "04"),
  ("cloud IAM (IDaaS)",     "PingOne, Advanced Identity Cloud","05"),
  ("MFA / passwordless",    "PingID, PingOne MFA",            "06"),
  ("threat / fraud",        "PingOne Protect",                "06"),
  ("orchestration",         "PingOne DaVinci",                "07"),
  ("directory",             "PingDirectory, PingDS",          "08"),
  ("governance (IGA)",      "PingOne Identity Governance",    "08"),
]
print(f"{'IAM function':24}{'Ping product(s)':34}covered in")
for func, prod, ch in PORTFOLIO:
    print(f"{func:24}{prod:34}Ch. {ch}")
print("\nThe merged portfolio covers the WHOLE IAM stack:")
print("  AUTHENTICATE  — who are you? (PingOne, PingID, federation)")
print("  FEDERATE      — trust identities across domains (PingFederate)")
print("  AUTHORIZE     — what can you access? (PingAccess, PingAM)")
print("  ORCHESTRATE   — design the identity journey (DaVinci)")
print("  STORE         — the directory of identities (PingDirectory/DS)")
print("  GOVERN        — who SHOULD have access, certified (Identity Governance)")
print("  PROTECT       — detect account threats/fraud (PingOne Protect)")
print("\nThat breadth is Ping's post-merger pitch: one vendor across workforce AND")
print("customer identity, on-prem AND cloud, from authentication to governance. The")
print("certifications are product-specific BECAUSE the portfolio is this wide — you")
print("specialize in the pieces your identity architecture uses. This completes the")
print("identity shelf: Okta (IDaaS), SailPoint (IGA), CyberArk (PAM), Ping (federation).")
EOF
```

**Expected result:** The Ping products mapped to the IAM functions — authenticate, federate, authorize, orchestrate, store, govern, protect — across the merged portfolio. The portfolio lesson is that Ping covers the whole identity stack for both workforce and customer identity, on-prem and cloud, which is why the certifications are product-specific: you specialize in the pieces your architecture uses.

**Negative test:** Treating Ping as a single-product SSO vendor. Post-merger it spans federation, access management, directory, cloud IAM, orchestration, governance, and threat protection — the breadth is the point, and the certifications reflect it product by product.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Ping program understood as product-specific, proctored, at Professional (and Advanced/Expert) levels.
- [ ] The exams placed across the portfolio by product and Ping-versus-ForgeRock heritage.
- [ ] The 2023 Ping + ForgeRock merger recognized as the shaper of the broad portfolio and program.
- [ ] Published mechanics known (~$395, proctored, ~70Q/90min, pass marks 64–75%), and Ping placed in the IAM landscape.
