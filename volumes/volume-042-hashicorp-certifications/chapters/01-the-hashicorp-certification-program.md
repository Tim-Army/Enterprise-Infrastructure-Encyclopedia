# Chapter 01: The HashiCorp Certification Program

## Learning Objectives

- Explain what HashiCorp certifies and where it sits in the infrastructure stack.
- Describe the current credential map: the Terraform and Vault Associate and Professional exams.
- Explain the Associate vs Professional tiers and the lab-based Professional format.
- Describe exam mechanics, two-year validity, and recertification.
- Track program change — the IBM acquisition, exam-version bumps, and the Consul Associate retirement.

## Theory and Architecture

**HashiCorp** (an **IBM company** since its 2025 acquisition) builds the tools
that define modern **infrastructure as code** and **secrets management** —
**Terraform** for provisioning and **Vault** for secrets — and certifies practical
mastery of them. These credentials sit alongside the encyclopedia's **automation
(IX)** and **cloud (XVII/XXXIII/XXXIV)** volumes: Terraform is the lingua franca
of multi-cloud provisioning, and Vault is a leading secrets and encryption
platform, so a HashiCorp credential validates skills that cut across every cloud
and platform track.

The current program has **two products and two tiers** — four exams:

| Product | Associate | Professional |
|---------|-----------|--------------|
| **Terraform** | Terraform Associate (**004**) | Terraform Authoring and Operations Professional |
| **Vault** | Vault Associate (**003**) | Vault Operations Professional |

The **Associate** exams are **one hour, online-proctored, multiple-choice** —
knowledge of the product's core workflow. The **Professional** exams are **four
hours, lab-based plus multiple-choice** — hands-on proof that you can author,
operate, and troubleshoot real configurations. Every credential is **valid two
years**; you recertify by passing an exam for the **same product at the same
level or higher**.

## Design Considerations

Plan a HashiCorp path by **product and depth**. Practitioners provisioning
infrastructure start with **Terraform Associate (004)**; those authoring reusable
modules and running Terraform at team scale continue to the **Authoring and
Operations Professional**. Security engineers managing secrets start with **Vault
Associate (003)** and advance to the **Vault Operations Professional** for
deployment, HA, and scaling. Because the **Professional** exams are lab-based,
prepare by **building and operating** real Terraform and Vault, not by reading.

Treat **currency** as a first-class concern — HashiCorp bumps exam versions and
prunes the lineup. Two recent changes: **Terraform Associate moved from 003 to
004**, **Vault Associate from 002 to 003**, and the **Consul Associate exam was
retired on 15 July 2026**. Confirm the current version and status before
studying.

## Implementation and Automation

Every objective in this volume can be practiced locally with the free CLIs —
`terraform`, `vault` (in `-dev` mode), and `consul` — no cloud account required:

```bash
# Confirm the tooling and versions the exams target
terraform version
vault version
# A throwaway Vault dev server for the Vault labs (foreground; use a second shell)
# vault server -dev
```

## Validation and Troubleshooting

Confirm a credential's objectives, format, and version on the official page:

```text
developer.hashicorp.com/certifications:
  - Infrastructure Automation -> Terraform Associate (004) + Authoring & Operations Professional
  - Security Automation -> Vault Associate (003) + Vault Operations Professional
  - the numbered exam objectives, duration, and format (MCQ vs lab-based)
  - two-year validity and recertification rules
```

Common pitfalls: studying the **retired version** (Terraform **003**, Vault
**002**) instead of the current **004/003**; expecting a **Consul Associate**
exam (retired 15 July 2026); and treating the **Professional** exams as
multiple-choice — they are **lab-based** and require hands-on skill.

## Security and Best Practices

Verify facts on **developer.hashicorp.com**, never a dump site. Practice with the
official **HashiCorp Learn** tutorials and the free CLIs. For Vault, never commit
tokens or unseal keys, use least-privilege **policies**, and prefer **dynamic
secrets** over static ones. For Terraform, protect **state** (it can contain
secrets) and use remote state with locking. Recertify before the two-year lapse.

## References and Knowledge Checks

- developer.hashicorp.com/certifications: the certification catalog, per-exam objectives, and tutorials.

**Knowledge checks**

1. What are the two products and two tiers in the current HashiCorp program?
2. How does the Professional exam format differ from the Associate format?
3. What recent version and lineup changes must you verify before studying?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and preparing the tools.

**Shared prerequisites for Labs 1.1–1.3** — a Linux shell with `curl`,
`terraform`, and `vault` installed. **Cost:** none.

### Lab 1.1 — Confirm current exam versions (Topic: Verify currency)

**Objective:** Read the current program from the authoritative source.

```bash
curl -sSL "https://developer.hashicorp.com/certifications" \
  | grep -oiE 'Terraform Associate \(00[0-9]\)|Vault Associate \(00[0-9]\)' | sort -u
```

**Expected result:** `Terraform Associate (004)` and `Vault Associate (003)` —
the current versions (003/002 are retired) from the authority.

**Negative test:** study a "Terraform Associate 003" course; it targets the
retired version — confirm the current code first.

**Cleanup:** none.

### Lab 1.2 — Verify the tooling (Topic: Prepare to practice)

**Objective:** Confirm the CLIs the exams exercise are installed.

```bash
terraform version | head -1
vault version
```

**Expected result:** a Terraform and a Vault version string — the two CLIs every
lab in this volume uses.

**Negative test:** study Terraform without the CLI installed; the exams are
hands-on in spirit — install and use the tools.

**Cleanup:** none.

### Lab 1.3 — Start a Vault dev server (Topic: Prepare the Vault labs)

**Objective:** Launch the throwaway Vault server the Vault chapters use.

```bash
vault server -dev -dev-root-token-id=root >/tmp/vault-dev.log 2>&1 &
export VAULT_ADDR='http://127.0.0.1:8200' VAULT_TOKEN='root'
sleep 2; vault status | grep -E 'Sealed|Version'
```

**Expected result:** `Sealed  false` and a version — a running, unsealed dev
Vault for the Vault Associate and Professional labs.

**Negative test:** use a dev server in production; it is in-memory and unsealed
for convenience — dev mode is for learning only.

**Cleanup:** `pkill -f 'vault server -dev'` when finished with the Vault chapters.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

HashiCorp (now an IBM company) certifies infrastructure as code (Terraform) and
secrets management (Vault) across two tiers: the one-hour multiple-choice
Associate exams (Terraform 004, Vault 003) and the four-hour lab-based
Professional exams (Terraform Authoring and Operations, Vault Operations).
Credentials are valid two years, and the program changes — the Consul Associate
exam retired 15 July 2026.

- [ ] I can name the four current HashiCorp exams and their tiers.
- [ ] I can explain Associate vs Professional format.
- [ ] I can confirm the current exam versions and the Consul retirement.
- [ ] I can start a Vault dev server and check the tooling.
- [ ] I completed Labs 1.1–1.3 including each negative test.
