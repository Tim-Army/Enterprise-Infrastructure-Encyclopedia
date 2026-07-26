# Chapter 16: Appendix — HashiCorp Certifications and Course Access

The **HashiCorp** (now an **IBM company**) certification program — the
infrastructure-automation and security-automation credentials — organized by
product and tier, with each exam's objectives, format, price, and validity. The
lineup and objectives were harvested on **26 July 2026** from
**developer.hashicorp.com/certifications** — the same source that anchors
[Volume XLII — HashiCorp Certification Tracks](../../volume-42-hashicorp-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works at HashiCorp.** Official preparation is free through
**HashiCorp Learn** (developer.hashicorp.com tutorials) and the product
documentation; the **CLIs are free** (`terraform`, `vault`, `consul`), so every
objective can be practiced locally with no cloud account. Exams are
**online-proctored** (PSI). Credentials are issued as verifiable badges under
**IBM Professional Certification** (Credly).

> **Currency.** HashiCorp bumps exam versions and prunes the lineup — the
> **version** is the currency signal. Recent changes captured here: **Terraform
> Associate 003 → 004**, **Vault Associate 002 → 003**, and the **Consul
> Associate (003) exam retired 15 July 2026** (leaving Terraform and Vault as the
> only certified products). Confirm the current version and status on
> developer.hashicorp.com before registering.

## Free training and entry points

- **[HashiCorp Certifications](https://developer.hashicorp.com/certifications)** —
  the authoritative catalog with per-exam objectives, format, and price
- **[HashiCorp Learn / Developer](https://developer.hashicorp.com/)** — free
  tutorials and documentation for Terraform, Vault, and Consul
- **Free CLIs** — `terraform`, `vault` (with `-dev` mode), and `consul` (with
  `-dev` mode) for local, no-cost practice
- **Exam review guides** — the objective lists per exam are the definitive study
  scope

## Fees, delivery, and renewal

- **Fee band (US pricing; confirm at registration):** the **Associate** exams
  (Terraform 004, Vault 003) are the low band (**~US$70.50**); the **Professional**
  exams (Terraform Authoring and Operations, Vault Operations) are the high band
  (**US$295** for Vault Operations). Confirm current pricing at registration.
- **Delivery:** **online-proctored (PSI)**. **Associate** exams are **one hour,
  multiple-choice**; **Professional** exams are **four hours (including a 15-minute
  break), lab-based plus multiple-choice** — you configure real Terraform/Vault.
- **Prerequisites:** none enforced, though the Professional exams assume real
  experience.
- **Validity and renewal:** every credential is **valid two years**; recertify by
  **passing an exam for the same product at the same level or higher** — there is
  **no continuing-education-credit model**.

## The certification map

Objectives verified against developer.hashicorp.com on 26 July 2026.

| Credential | Product | Tier | Format | Objectives |
| --- | --- | --- | --- | --- |
| Terraform Associate (004) | Terraform | Associate | 1 hr, multiple-choice | 8 |
| Terraform Authoring and Operations Professional | Terraform | Professional | 4 hr, lab-based + MCQ | 6 |
| Vault Associate (003) | Vault | Associate | 1 hr, multiple-choice | 9 |
| Vault Operations Professional | Vault | Professional | 4 hr, lab-based + MCQ | 8 |
| ~~Consul Associate (003)~~ | Consul | Associate | — | **Retired 15 July 2026** |

## Exam objectives

- **Terraform Associate (004):** IaC with Terraform · Terraform fundamentals ·
  Core Terraform workflow · Terraform configuration · Terraform modules ·
  Terraform state management · Maintain infrastructure with Terraform · HCP
  Terraform.
- **Terraform Authoring and Operations Professional:** Manage resource lifecycle ·
  Develop and troubleshoot dynamic configuration · Develop collaborative
  Terraform workflows · Create, maintain, and use Terraform modules · Configure
  and use Terraform providers · Collaborate on IaC using HCP Terraform.
- **Vault Associate (003):** Authentication methods · Vault policies · Vault
  tokens · Vault leases · Secrets engines · Encryption as a service · Vault
  architecture fundamentals · Vault deployment architecture · Access management
  architecture.
- **Vault Operations Professional:** Create a working Vault server configuration ·
  Monitor a Vault environment · Employ the Vault security model · Build
  fault-tolerant Vault environments · Understand HSM integration · Scale Vault
  for performance · Configure access control · Configure Vault Agent.

## Notes

- **HashiCorp is an IBM company** (acquired 2025); badges are administered under
  IBM Professional Certification.
- **The version is the currency signal.** Study **Terraform 004** and **Vault
  003**, not the retired 003/002; there is no active **Consul** exam.
- **Professional exams are lab-based** — prepare by building and operating real
  Terraform and Vault, not by reading alone.
- **Recertify by exam** within two years (a higher level renews the lower).
- **Hands-on practice** for these tools lives across the encyclopedia:
  Terraform/IaC and Vault in **Volume IX (Infrastructure Automation)**, and the
  cloud targets they provision in **Volumes XVII (AWS)**, **XXXIII (Azure)**, and
  **XXXIV (Google Cloud)**.
