# Chapter 07: Keeping the HashiCorp Program Current and Career Paths

## Learning Objectives

- Explain HashiCorp's two-year validity and recertification model.
- Track program change — the IBM acquisition, exam-version bumps, and retirements.
- Plan a HashiCorp career path across Terraform and Vault, Associate to Professional.
- Relate HashiCorp credentials to the encyclopedia's cloud and automation volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

A HashiCorp credential is **valid for two years**. You recertify by **passing an
exam for the same product at the same level or higher** — for example, retaking
the Terraform Associate, or earning the Terraform Authoring and Operations
Professional (a higher level renews the Associate). There is no
continuing-education-credit model as with CompTIA or ISC2; recertification is by
exam.

The program is small and changes deliberately, and recent changes are exactly the
kind a stale study plan gets wrong:

- **HashiCorp is now an IBM company** (acquired 2025); credentials are
  administered under **IBM Professional Certification** (badges via Credly).
- **Exam versions bump:** Terraform Associate **003 → 004**, Vault Associate
  **002 → 003**.
- **Retirements:** the **Consul Associate (003)** exam retired **15 July 2026**,
  leaving Terraform and Vault as the only certified products.

## Design Considerations

Plan the path by **product and depth**. The most common route is **Terraform
Associate (004) → Terraform Authoring and Operations Professional** for
infrastructure engineers, and **Vault Associate (003) → Vault Operations
Professional** for security/platform engineers. Many practitioners hold **both**
Associate exams, since Terraform and Vault are routinely used together (Terraform
provisions; Vault secures the secrets that provisioning needs). Because the
**Professional** exams are lab-based, schedule them after real operational
experience.

## Implementation and Automation

Verify currency from **developer.hashicorp.com** — the certification pages carry
the current version and status:

```bash
curl -sSL "https://developer.hashicorp.com/certifications" \
  | grep -oiE '(Terraform|Vault) Associate \(00[0-9]\)|Professional' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing study time:

```text
developer.hashicorp.com/certifications:
  - active exams and current versions (Terraform Associate 004, Vault Associate 003)
  - each exam's objectives, format (MCQ vs lab-based), and price
  - two-year validity and recertify-by-exam rule
  - retirements (Consul Associate, 15 July 2026)
```

Common pitfalls: buying a **003 Terraform** or **002 Vault** course; planning for
a **Consul** exam (retired); and expecting a CE-credit renewal — HashiCorp
recertifies **by exam**.

## Security and Best Practices

Recertify before the two-year lapse (or advance to the Professional level, which
renews the Associate). Keep practicing with the **current CLI versions**, since
the tools evolve (new Terraform language features, Vault secrets engines).
Combine credentials thoughtfully — a Terraform + Vault pairing covers both
provisioning and secrets, the two halves of secure infrastructure automation.

## References and Knowledge Checks

- developer.hashicorp.com/certifications: the certification catalog, per-exam objectives, and recertification policy; IBM/HashiCorp announcements.

**Knowledge checks**

1. How long is a HashiCorp credential valid, and how do you recertify?
2. What three recent changes (acquisition, versions, retirement) must you verify?
3. Why do many practitioners hold both the Terraform and Vault Associate exams?

## Hands-On Lab

Exam-preparation walkthroughs for tracking program change and planning a path.

**Shared prerequisites for Labs 7.1–7.2** — a Linux shell with `curl` and
`python3`. **Cost:** none.

### Lab 7.1 — Verify the current program (Topic: Verify currency)

**Objective:** Read the active exams and versions from the source.

```bash
curl -sSL "https://developer.hashicorp.com/certifications" \
  | grep -oiE '(Terraform|Vault) Associate \(00[0-9]\)' | sort -u
```

**Expected result:** `Terraform Associate (004)` and `Vault Associate (003)` —
the current versions, confirming the 003/002 courses are stale and that no Consul
exam is listed.

**Negative test:** trust a "2024 HashiCorp certs" blog; versions have bumped and
Consul retired — confirm against developer.hashicorp.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Plan a two-year recertification (Topic: Maintain the credential)

**Objective:** Model the recertify-by-exam-or-higher rule.

```bash
python3 - <<'PY'
from datetime import date
earned = date(2026, 7, 26)      # Terraform Associate 004
expires = earned.replace(year=earned.year + 2)
print(f"Earned {earned} -> expires {expires}")
print("Recertify by: retaking Terraform Associate, OR passing Terraform Professional (higher level).")
PY
```

**Expected result:** an expiry two years out and the recertification options
(same exam or a higher level) — HashiCorp's exam-based renewal.

**Negative test:** expect continuing-education credits to renew it; HashiCorp has
**no CE model** — recertify by exam.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

HashiCorp credentials are valid two years and renewed by exam (same product,
same level or higher) — there is no continuing-education model. The program is
now under IBM, exam versions have bumped (Terraform 004, Vault 003), and the
Consul Associate retired on 15 July 2026. The natural paths are Terraform
Associate → Professional and Vault Associate → Professional, often held together.

- [ ] I can explain two-year validity and recertify-by-exam.
- [ ] I can name the IBM acquisition, version bumps, and Consul retirement.
- [ ] I can plan Terraform and Vault career paths.
- [ ] I can verify the current program from developer.hashicorp.com.
- [ ] I completed Labs 7.1–7.2 including each negative test.
