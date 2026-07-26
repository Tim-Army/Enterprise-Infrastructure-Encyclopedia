# Chapter 08: GitHub Certifications

## Learning Objectives

- Enumerate the GitHub certifications and their GH-code exams.
- Distinguish the Foundations, Actions, Administration, Advanced Security, and Copilot credentials.
- Explain how GitHub certifications fit Microsoft's broader program.
- Recognize the new Agentic AI Developer credential.
- Build a study path for a DevOps or platform engineer using GitHub.

## Theory and Architecture

GitHub is a Microsoft company, and its certifications are part of the wider
Microsoft credential catalog, now using **GH-** exam codes and delivered
through the same Pearson VUE and Credly infrastructure. As verified on
Microsoft Learn (26 July 2026), the GitHub credentials are:

- **GitHub Foundations** — exam **GH-900** (Fundamentals). Git and GitHub
  basics — repositories, collaboration, issues, pull requests, and GitHub
  fundamentals. The gateway.
- **GitHub Actions** — the CI/CD credential for building, testing, and
  deploying with GitHub Actions workflows.
- **GitHub Administration** — exam **GH-100** (Associate-level). Administer
  GitHub organizations and enterprises — access, policies, and integrations.
- **GitHub Advanced Security** — exam **GH-500**. Code scanning, secret
  scanning, and dependency review with GitHub Advanced Security (GHAS).
- **GitHub Copilot** — exam **GH-300**. Use and administer GitHub Copilot
  effectively and responsibly.
- **GitHub Certified: Agentic AI Developer** — exam **GH-600**. A new
  credential for building agentic AI developer workflows on GitHub — part of
  the same 2026 agent wave seen across the AI family (Chapter 07).

These map directly to the automation, source-control, and DevOps skills in
**Volume IX — Infrastructure Automation** and the CI/CD and platform-
engineering content across the encyclopedia.

## Design Considerations

Start with **GH-900 (Foundations)** for anyone using GitHub seriously, then
choose by role. **DevOps/platform engineers** target **GitHub Actions** for
CI/CD; **GitHub administrators** take **GH-100**; **security engineers**
enabling GHAS take **GH-500**; and teams adopting **Copilot** take **GH-300**
(useful for both developers and the admins governing Copilot rollout — a
natural companion to the Microsoft 365 Copilot administration credential in
Chapter 07). The new **GH-600 Agentic AI Developer** suits engineers building
agent-driven developer workflows.

GitHub credentials complement the Azure **DevOps Engineer Expert (AZ-400)**
and the automation content of Volume IX — a modern platform engineer often
holds GitHub Actions plus AZ-400.

## Implementation and Automation

Verify the GitHub exam codes from Microsoft Learn:

```bash
for slug in github-foundations github-administration github-advanced-security github-copilot agentic-ai-developer; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bGH-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# github-foundations -> GH-900
# github-administration -> GH-100
# github-advanced-security -> GH-500
# github-copilot -> GH-300
# agentic-ai-developer -> GH-600
```

## Validation and Troubleshooting

Map the credentials:

| Credential | Exam | Focus |
| --- | --- | --- |
| GitHub Foundations | GH-900 | Git/GitHub basics |
| GitHub Actions | (GH-series) | CI/CD workflows |
| GitHub Administration | GH-100 | Org/enterprise administration |
| GitHub Advanced Security | GH-500 | Code/secret scanning (GHAS) |
| GitHub Copilot | GH-300 | Copilot use and administration |
| Agentic AI Developer | GH-600 | Agentic developer workflows |

Common pitfalls: assuming GitHub certifications are separate from the
Microsoft catalog (they are integrated, with **GH-** codes on Microsoft
Learn); confusing **GitHub Copilot (GH-300)** with the Microsoft 365 Copilot
and Agent Administration credential (Chapter 07) — the first is developer/tool
focused, the second is M365 governance; and overlooking the new **GH-600**
agentic credential.

## Security and Best Practices

Prepare with **Microsoft Learn** and **GitHub Skills** free interactive
courses, and practice in a **free GitHub account** and organization. Pair
**GitHub Actions** with the Azure **AZ-400** DevOps credential and the
automation practice in **Volume IX**. For security teams, **GH-500 (Advanced
Security)** pairs with the SC family (Chapter 03). Renew per the credential's
stated validity on Microsoft Learn.

## References and Knowledge Checks

- Microsoft Learn: certification pages for GitHub Foundations (GH-900), Administration (GH-100), Advanced Security (GH-500), Copilot (GH-300), Agentic AI Developer (GH-600).
- Cross-reference: [Volume IX — Infrastructure Automation](../volume-09-infrastructure-automation/README.md).

**Knowledge checks**

1. What exam code prefix do GitHub certifications use, and where are they catalogued?
2. How does GitHub Copilot (GH-300) differ from the M365 Copilot administration credential?
3. Which GitHub credential pairs naturally with the Azure AZ-400 DevOps Expert?

## Hands-On Lab

Exam-preparation walkthroughs for the GitHub family.

**Shared prerequisites for Labs 8.1–8.2** — a browser and a free GitHub
account; `curl` for Lab 8.1. **Cost:** none.

### Lab 8.1 — Confirm the GitHub GH-codes (Topic: Verify the family)

**Objective:** Prove GitHub uses GH-series codes on Microsoft Learn.

```bash
for slug in github-foundations github-administration github-advanced-security; do
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bGH-[0-9]{3}\b' | sort -u | tr '\n' ' '; echo " <- $slug"
done
```

**Expected result:** GH-900, GH-100, and GH-500 — GitHub certifications are
part of the Microsoft catalog with GH- codes.

**Negative test:** assume GitHub certs are hosted only on github.com with no
Microsoft Learn presence; they are catalogued on Microsoft Learn — verify
there.

**Cleanup:** none.

### Lab 8.2 — Plan a platform-engineer GitHub path (Topic: Study plan)

**Objective:** Sequence GitHub credentials for a DevOps role.

```text
GH-900 (Foundations)
  -> GitHub Actions (CI/CD) + GH-100 (Administration)
  -> GH-500 (Advanced Security) for supply-chain security
  -> GH-300 (Copilot); pair with Azure AZ-400 (DevOps Expert) and Volume IX.
```

**Expected result:** a Foundations→role path that complements Azure DevOps and
the automation volume.

**Negative test:** treat GitHub certs in isolation from Azure DevOps; a modern
platform engineer benefits from GitHub Actions **and** AZ-400 together.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

GitHub certifications are part of the Microsoft catalog with **GH-** codes:
Foundations (GH-900), Actions, Administration (GH-100), Advanced Security
(GH-500), Copilot (GH-300), and the new Agentic AI Developer (GH-600). They
complement Azure DevOps (AZ-400) and the automation practice in Volume IX.

- [ ] I can list the GitHub credentials and GH-codes.
- [ ] I can distinguish GH-300 from M365 Copilot administration.
- [ ] I can pair GitHub credentials with Azure DevOps and Volume IX.
- [ ] I recognize the new GH-600 agentic credential.
- [ ] I completed Labs 8.1–8.2 including each negative test.
