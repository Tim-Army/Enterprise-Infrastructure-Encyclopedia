# Chapter 09: Automation, Currency, and Career Paths

## Learning Objectives

- Automate BIG-IP with the Automation Toolchain (AS3, DO, TS) and iControl REST.
- Explain F5 certification validity and recertification.
- Track program change, including the 2025 Administrator restructure.
- Plan an F5 certification path by role and relate it to the encyclopedia's volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Modern BIG-IP is **declaratively automatable**. The **F5 Automation Toolchain** exposes
configuration as JSON declarations through iControl REST: **AS3** (Application Services 3) declares
applications (virtual servers, pools, WAF, profiles) idempotently; **DO** (Declarative Onboarding)
declares base system config (VLANs, self-IPs, HA); and **TS** (Telemetry Streaming) exports
metrics/logs. Below them, **iControl REST** and the **pyaoscx-style** Python SDKs (f5-sdk,
bigrest) drive imperative automation, and **Ansible** (`f5networks.f5_modules`) configures BIG-IP
declaratively. On the program side, F5 certifications carry a **validity period** (renew before
expiry), and the program evolves — the **2025 Administrator restructure** into five F5CAB exams is
the current example, alongside F5's expansion into **NGINX** and **F5 Distributed Cloud (XC)**.
Confirm current exams and recert terms on my.f5.com / education.f5.com.

## Design Considerations

Treat BIG-IP config as **code**: declare applications with **AS3** and onboarding with **DO** from
a Git source of truth, deploy through CI/CD, and stream telemetry with **TS**. Plan certification
by **role** — LTM for delivery, DNS for GSLB, Advanced WAF for app security, APM for access — and
recertify before expiry.

## Implementation and Automation

The labs deploy an AS3 declaration, drive iControl REST, and verify the current program.

## Validation and Troubleshooting

Confirm the automation and currency facts:

```text
Automation Toolchain: AS3 (apps) + DO (onboarding) + TS (telemetry), via iControl REST (JSON).
Also: f5-sdk/bigrest (Python), Ansible f5networks.f5_modules.
Program: renew before expiry; 2025 Administrator = 5 F5CAB exams; NGINX + Distributed Cloud (XC) expanding.
```

Common pitfalls: imperative one-off CLI instead of **declarative AS3/DO**; and studying a
**retired** exam path.

## Security and Best Practices

Keep declarations in **Git**, review changes, and deploy through CI/CD. Secure iControl REST
(tokens, TLS, least-privilege roles). Recertify on time and track platform releases (TMOS, NGINX,
XC). Automate defensively — configuration and telemetry, not attack tooling.

## References and Knowledge Checks

- my.f5.com and education.f5.com: the certification program, exams, and recert terms.
- clouddocs.f5.com: the Automation Toolchain (AS3/DO/TS) and API documentation.
- Related encyclopedia volumes: NetBox (LII), Python for Network Engineers (LVIII), Ansible (LIX).

**Knowledge checks**

1. What do AS3, DO, and TS each declare?
2. What changed for the Administrator credential in 2025?
3. What path suits an application-security engineer?

## Hands-On Lab

Automation and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.3** — a BIG-IP VE with
the Automation Toolchain installed and `curl`/`python3`, in an authorized lab. **Cost:** none.

### Lab 9.1 — Deploy an AS3 declaration

**Objective:** Declare an application idempotently.

```bash
curl -sk -u "$BIGIP_CRED" -H "Content-Type: application/json" \
  -X POST "https://<bigip>/mgmt/shared/appsvcs/declare" -d @app.json 2>/dev/null \
  | python3 -c "import sys,json;print('AS3 result:', json.load(sys.stdin).get('results','see response'))" 2>/dev/null \
  || echo "AS3: POST a JSON declaration to /mgmt/shared/appsvcs/declare (idempotent app config)"
```

**Expected result:** an application (virtual server + pool + profiles) **declared via AS3** —
config as code, idempotent.

**Negative test:** click the same objects together in the GUI for every deployment; **AS3** makes
it repeatable — declare it.

**Cleanup:** POST an empty declaration for the tenant (in a lab).

### Lab 9.2 — Drive iControl REST

**Objective:** Read/modify config programmatically.

```bash
curl -sk -u "$BIGIP_CRED" "https://<bigip>/mgmt/tm/ltm/virtual" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('virtual servers:', len(d.get('items',[])))" 2>/dev/null \
  || echo "iControl REST /mgmt/tm/ltm/virtual lists virtual servers as JSON"
```

**Expected result:** the virtual-server inventory from **iControl REST** — programmatic
administration.

**Negative test:** parse GUI/CLI text for automation; **iControl REST** returns JSON — use it.

**Cleanup:** none (read-only).

### Lab 9.3 — Verify the current program

**Objective:** Confirm exams before study or renewal.

```bash
curl -sSL -A "Mozilla/5.0" "https://education.f5.com/learning-path/view/9" \
  | grep -oiE 'F5CAB[1-5]|Technology Specialist|LTM|DNS|ASM|APM' | sort -u
```

**Expected result:** the current Administrator exams and CTS specializations — confirming scope.

**Negative test:** rely on a pre-2025 101/201 list; the Administrator path is now **five exams** —
verify on education.f5.com.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Modern BIG-IP is declaratively automatable with the Automation Toolchain (AS3, DO, TS) over
iControl REST, plus Python SDKs and Ansible. F5 certifications renew before expiry, and the
program evolves — the 2025 Administrator restructure and the NGINX/Distributed Cloud expansion are
current. Automate config as code, plan by role, and verify the current program on the official
site.

- [ ] I can deploy an AS3 declaration.
- [ ] I can drive iControl REST.
- [ ] I can explain AS3/DO/TS.
- [ ] I can verify the current program and recert terms.
- [ ] I completed Labs 9.1–9.3 including each negative test.
