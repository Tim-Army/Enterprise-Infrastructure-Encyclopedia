# Chapter 02: Delinea and the PAM Landscape

## Learning Objectives

- Recap PAM and why privileged access is the attack path.
- Explain the Thycotic + Centrify merger and what each side contributed.
- Describe the unified Delinea Platform.
- Place Delinea's extension from PAM into identity security.

*Cert relevance: this chapter frames the portfolio and platform every Delinea credential sits on.*

## PAM, briefly

**Privileged Access Management (PAM)** secures, controls, and monitors **privileged accounts** — the administrator, root, and service accounts that can change configurations, access all data, and disable controls. Because a compromised privileged credential lets an attacker do anything that account can, privileged access is the **primary path** in most breaches ([the full attack chain is covered in the BeyondTrust volume, CLVI](../../volume-156-beyondtrust-certifications/chapters/02-privileged-access-management.md)). PAM breaks that path with **vaulting, rotation, session control, least privilege, and just-in-time access** — and Delinea's portfolio implements all of it. The lab recaps the discipline.

## The Thycotic + Centrify merger

Delinea was formed in **2021** by merging **Thycotic** and **Centrify**, two established PAM vendors with complementary strengths:

- **Thycotic** brought **Secret Server** (a widely-adopted, fast-to-deploy **credential vault**) and **Privilege Manager** (**endpoint** least privilege) — strong on **secrets and endpoints**, known for ease of deployment.
- **Centrify** brought **server PAM** — privilege elevation on **Linux/Unix/Windows servers**, **Active Directory bridging**, and identity-centric access — strong on **server and infrastructure** privilege.

Together they cover privileged access **end to end**: secrets, endpoints, and servers. The merger is why the Delinea portfolio spans [Secret Server (Ch 3)](03-secret-server.md), [Privilege Manager (Ch 4)](04-privilege-manager.md), and [Server PAM (Ch 5)](05-server-pam.md) — and why a certification candidate encounters both heritages. The lab models the complementary coverage.

## The unified Delinea Platform

Post-merger, Delinea unified the portfolio under the **Delinea Platform** — a **cloud-native SaaS** control plane that ties the products together: one place for policy, vaulting, sessions, analytics, and identity security, rather than separate consoles. The platform direction reflects the industry shift to **SaaS-delivered, identity-centric** security: PAM delivered as a service, integrated with the rest of the identity stack, and extended with analytics and threat detection. Understanding that the products increasingly operate **through the platform** (not just as standalone installs) is part of the modern Delinea picture. The lab models the platform.

## From PAM to identity security

Delinea, like its peers, is **extending from PAM into broader identity security** — because privileged access is one part of a larger identity attack surface. This includes **Identity Threat Detection and Response (ITDR)** (detecting identity-based attacks), **Identity Security Posture Management (ISPM)** (finding and reducing identity risk), and **Privileged Behavior Analytics** (spotting anomalous privileged activity), covered in [Chapter 8](08-the-delinea-platform-and-identity-security.md). The thesis: securing privilege is necessary but not sufficient; you must also **detect** identity threats and **reduce** identity attack surface across the estate. This places Delinea in the wider identity-security landscape alongside [SailPoint (CXXXII)](../../volume-132-sailpoint-certifications/README.md) governance and [Ping (CL)](../../volume-150-ping-identity-certifications/README.md)/[Okta (LXXVI)](../../volume-076-okta-certifications/README.md) access management. The lab situates Delinea.

## Hands-On Lab

Python models the merged portfolio and platform. **Cost:** none.

### Lab 2.1 — The merger covers privileged access end to end

**Objective:** See how Thycotic + Centrify combine to cover the full privileged surface.

```bash
python3 - <<'EOF'
# the privileged-access surface, and which heritage/product covers each part
SURFACE = [
  ("human admin passwords / shared secrets", "Secret Server",     "Thycotic"),
  ("endpoint local admin rights",            "Privilege Manager", "Thycotic"),
  ("Linux/Unix/Windows SERVER privilege",    "Server PAM",        "Centrify"),
  ("Active Directory bridging (one identity)","Server PAM",       "Centrify"),
  ("DevOps / machine / CI-CD secrets",       "DevOps Secrets Vault","Delinea"),
  ("service-account governance",             "Account Lifecycle Manager","Delinea"),
  ("identity threat detection (ITDR)",       "Delinea Platform",  "Delinea"),
]
print("The privileged-access surface, covered end to end by the merged portfolio:\n")
print(f"   {'surface':42}{'product':26}heritage")
for surface, product, heritage in SURFACE:
    print(f"   {surface:42}{product:26}{heritage}")
print("\nThe 2021 THYCOTIC + CENTRIFY merger was COMPLEMENTARY:")
print("  THYCOTIC = secrets (Secret Server) + endpoints (Privilege Manager) — fast to deploy")
print("  CENTRIFY = SERVER privilege + AD bridging — infrastructure/identity-centric")
print("Together they cover privileged access END TO END — secrets, endpoints, AND servers —")
print("now unified under the DELINEA PLATFORM (one SaaS control plane), and extended into")
print("IDENTITY SECURITY (ITDR/ISPM/analytics). That breadth is why the certification spans")
print("multiple products + both heritages. PAM is necessary but not sufficient — you also")
print("DETECT identity threats and REDUCE identity attack surface across the estate.")
EOF
```

**Expected result:** The privileged-access surface mapped to products and heritage — Thycotic's Secret Server and Privilege Manager (secrets and endpoints), Centrify's Server PAM (servers and AD bridging), and Delinea's DevOps Secrets Vault, ALM, and Platform. The lesson is that the 2021 merger was complementary, covering privileged access end to end, now unified under the Delinea Platform and extended into identity security (ITDR/ISPM/analytics).

**Negative test:** Treating Delinea as a single-product vault vendor. The Thycotic + Centrify merger makes it an end-to-end portfolio (secrets, endpoints, servers, DevOps, service accounts, identity security); a candidate encounters both heritages and the unifying platform.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] PAM recapped — privileged access as the primary attack path, broken by vaulting/least-privilege/JIT.
- [ ] The 2021 Thycotic + Centrify merger understood — secrets/endpoints plus server privilege and AD bridging.
- [ ] The unified Delinea Platform understood — one SaaS control plane over the portfolio.
- [ ] Delinea's extension from PAM into identity security (ITDR, ISPM, analytics) recognized.
