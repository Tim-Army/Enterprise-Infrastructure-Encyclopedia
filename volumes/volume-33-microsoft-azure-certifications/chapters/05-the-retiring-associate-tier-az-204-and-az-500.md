# Chapter 05: The Retiring Associate Tier — AZ-204 and AZ-500

## Learning Objectives

- State exactly what is retiring, on what date, and what a retirement does
  and does not do to a credential you already hold
- Decide whether to sit AZ-204 or AZ-500 before their retirement dates, or
  redirect that study time
- Describe what each certification covered, since the subject matter
  remains professionally essential after the credential closes
- Identify where the retiring subject matter has moved within Microsoft's
  reorganized program
- Apply a general rule for evaluating any certification that carries a
  published end date

## Theory and Architecture

### The two closing certifications

Verified against Microsoft Learn on **23 July 2026**:

| Certification | Exam | Retires |
| --- | --- | --- |
| Azure Developer Associate | AZ-204 | **31 July 2026** |
| Azure Security Engineer Associate | AZ-500 | **31 August 2026** |

Microsoft's banner on both pages is explicit and worth quoting in
substance: the certification, its related exam, **and its renewal
assessments** all retire on the stated date, after which the certification
can no longer be earned **or renewed**.

That last clause is the consequential one, and it is unusual. For most
vendors — AWS's Advanced Networking specialty, for instance (Volume XVII,
Chapter 13) — a retirement stops new certifications while existing ones
run out their term normally. Here, because Azure role-based certifications
renew **annually** ([Chapter 01](01-the-azure-certification-program-levels-codes-and-renewal.md)),
withdrawing the renewal assessment means a held AZ-204 or AZ-500 will
lapse at its next annual renewal date and cannot be renewed.

A credential you hold today remains valid until its expiry. It simply has
no path forward after that.

### What this means for a study plan

The arithmetic is unforgiving and should be done before any further
reading:

- **AZ-204 retires 31 July 2026.** A study plan not already near
  completion cannot reach a test date. Redirect it.
- **AZ-500 retires 31 August 2026.** A candidate already strong on Azure
  security has a narrow window; anyone starting from scratch does not.
- **Neither will renew.** Even a successful pass buys one annual cycle,
  after which the credential lapses permanently. Weigh that against the
  effort.

For most readers the honest conclusion is to **not start either**, and to
treat the subject matter — which remains entirely current — as
professional development rather than certification preparation.

### AZ-204: what the developer certification covered

The Azure Developer certification spanned participation in all phases of
cloud application development: requirements, design, development,
deployment, security, maintenance, performance tuning, and monitoring.
Its technical surface included Azure compute solutions (App Service,
Functions, container hosting), storage and data access patterns, securing
solutions with Microsoft Entra ID and Key Vault, monitoring and
instrumentation, and integrating third-party services through API
Management, Event Grid, Event Hubs, and Service Bus.

None of that becomes less relevant. The credential is closing; the job is
not.

### AZ-500: what the security certification covered

The Azure Security Engineer implemented, managed, and monitored security
for Azure, multi-cloud, and hybrid environments as part of an end-to-end
infrastructure — identity and access with Entra ID, platform protection
and network security, security operations using Microsoft Defender for
Cloud and its tooling, and data and application security.

### Where the subject matter went

Microsoft has been reorganizing the associate tier around **roles as they
exist now**, and the developer and security content did not disappear so
much as redistribute:

- **Application development on Azure** is increasingly represented by the
  AI-centric developer certifications in
  [Chapter 06](06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md) —
  Azure AI Apps and Agents Developer (AI-103) and Azure AI Cloud Developer
  (AI-200) — which assume application-development competence and add AI
  workloads on top.
- **Security** is served by Microsoft's dedicated `SC` family, which sits
  outside the Azure-branded lineup: SC-100 (Cybersecurity Architect),
  SC-200 (Security Operations Analyst), and SC-300 (Identity and Access
  Administrator). A reader whose role is Azure security should look there
  rather than at a closing AZ-500.
- **Platform security fundamentals** remain examinable within AZ-104
  ([Chapter 03](03-azure-administrator-az-104.md)) and AZ-305
  ([Chapter 08](08-the-expert-tier-az-305-and-az-400.md)).

## Design Considerations

- **Do the date arithmetic first.** Before any study decision, compare
  your realistic test date against the retirement date. This is a
  five-minute calculation that saves months.
- **Weigh the no-renewal clause explicitly.** A certification that cannot
  be renewed is a depreciating asset. That may still be worth it if an
  employer or contract requires it now, and rarely otherwise.
- **Do not delete the knowledge with the credential.** Both syllabi remain
  accurate descriptions of real work. Keep studying the material; stop
  studying *for the exam*.
- **Redirect security readers to the `SC` family.** It is the durable home
  for Microsoft security certification and carries no equivalent closure.
- **Treat this as the general rule.** Any certification carrying a
  published end date should be evaluated on: can I reach a test date, will
  it renew, and does something durable cover the same ground?

## Implementation and Automation

### Confirming a retirement date yourself

```bash
# Never take a retirement date second-hand. Both certification pages
# state it in a banner rendered into the page HTML.
for c in azure-developer azure-security-engineer; do
  printf '%-26s ' "$c"
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$c/" \
    | sed 's/<[^>]*>/ /g' | tr -s ' ' \
    | grep -oE 'This certification[^.]{0,140}\.' | head -1
done
```

### Checking what you already hold and when it expires

```text
# Microsoft Learn profile → Certifications shows each credential's
# expiry date and its renewal window. For a retiring certification,
# confirm whether a renewal assessment is still offered:
#
#   https://learn.microsoft.com/en-us/users/me/credentials
#
# Record, per credential:
#   certification | earned | expires | renewal available? | action
```

### Finding the durable alternative

```bash
# List the SC-family security certifications, which are not part of the
# Azure-branded closure and are the redirect target for AZ-500 readers.
curl -s 'https://learn.microsoft.com/api/catalog/?locale=en-us&type=certifications' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin)
for c in d["certifications"]:
    t=c["title"]
    if "Security" in t or "Identity" in t or "Cybersecurity" in t:
        print(c["certification_type"], "|", t)'
```

## Validation and Troubleshooting

- **Read which nouns the banner covers.** These banners name the
  certification, the exam, *and* the renewal assessments. A banner
  covering only the exam would have different consequences — check rather
  than pattern-matching.
- **"Retired" and "will retire" are different states.** AI-102 and DP-100
  are already retired (Chapter 06); AZ-204 and AZ-500 have future dates
  and remain earnable until then.
- **Verify the no-renewal implication against your own credential.** If
  you hold one of these, confirm the expiry and whether a renewal
  assessment is still offered in your Microsoft Learn profile — that is
  the authoritative record for your account.
- **Do not infer a successor.** Microsoft's pages announce the retirement
  without naming a one-to-one replacement. The redistribution described
  above is an assessment of where the subject matter now lives, not a
  vendor-stated mapping — treat it as guidance and confirm current
  recommendations on Microsoft Learn.

## Security and Best Practices

- Continue applying AZ-500's material regardless of the credential:
  Defender for Cloud, Entra ID conditional access, network protection, and
  data security are operational requirements, not exam topics.
- Do not let a retiring certification justify unauthorized practice
  material to "get it done in time." A rushed pass on a closing credential
  is the weakest possible reason to violate the certification agreement.
- If an employer requires AZ-500 specifically, raise the retirement and
  the no-renewal clause with them early — the requirement itself will need
  updating, and that conversation is better had before the date than
  after.
- Keep the sandbox-subscription discipline from Chapter 01 for any
  security experimentation; Defender and policy changes are disruptive by
  design.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Developer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/) (AZ-204 — retires 31 July 2026)
- [Microsoft Certified: Azure Security Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-security-engineer/) (AZ-500 — retires 31 August 2026)
- [Certification renewal](https://learn.microsoft.com/en-us/credentials/support/renew-your-microsoft-certification) —
  the annual model whose withdrawal makes these closures permanent.
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 06](06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md)
  for the certifications that now occupy the developer space, and
  [Chapter 09](09-specialty-certifications-and-certification-operations.md)
  for the currency check that catches changes like these.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name both retiring certifications, their exam codes, and their dates.
2. What three things do the retirement banners cover, and why does the
   third matter more here than for most vendors?
3. Does a retirement invalidate a credential you already hold? What does
   it change?
4. Where should a reader whose role is Azure security direct their
   certification effort instead, and why?
5. State the general rule for evaluating any certification that carries a
   published end date.

## Hands-On Lab

**Objective:** Make a defensible, dated decision about both retiring
certifications rather than drifting into or away from them — and verify
every input to that decision from primary sources.

**Cost note:** Entirely free. No Azure resources are created.

**Prerequisites**

- Web access to Microsoft Learn.
- Your own certification record, if you hold any Azure credentials.

**Steps**

1. **Confirm both dates (10 minutes).** Run the retirement-date query from
   the Implementation section.

   **Expected result:** 31 July 2026 for AZ-204 and 31 August 2026 for
   AZ-500, read from Microsoft's own pages — not from this chapter.

2. **Do the arithmetic (10 minutes).** For each, write your earliest
   realistic test date given current preparation, and compare it to the
   retirement date.

   **Expected result:** an explicit go/no-go per certification, with the
   date gap stated.

3. **Apply the renewal clause (10 minutes).** For any go decision, write
   what happens at the first annual renewal after the retirement date.

   **Expected result:** the recognition that the credential lapses
   permanently, and a statement of why it is still worth it — or a
   reversal to no-go.

4. **Find the durable alternative (15 minutes).** Run the SC-family query
   and identify which certification best covers your actual role.

   **Expected result:** a named alternative with a one-sentence
   justification.

5. **Negative test (10 minutes).** Search a third-party certification
   listing for AZ-204 or AZ-500 and check whether it shows the retirement.

   **Expected result:** most will not — demonstrating why step 1 uses
   Microsoft's pages and why a study plan built on aggregator data would
   have walked into a closing exam.

6. **Record the decision.** Write the outcome, dated, with the primary
   sources you used. There is nothing to clean up.

## Lab Verification

Complete this sign-off once both dates have been confirmed from Microsoft
and a dated decision recorded. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Azure Developer Associate (**AZ-204**) retires **31 July 2026** and Azure
Security Engineer Associate (**AZ-500**) retires **31 August 2026**. Both
banners cover the certification, the exam, and the renewal assessments —
and because Azure role-based certifications renew annually, withdrawing
the renewal assessment means a held credential lapses at its next renewal
and cannot be restored. A credential you hold stays valid to its expiry; it
simply has no path forward. For most readers the correct decision is not to
start either, to keep studying the subject matter — which remains entirely
current — and to redirect certification effort to the AI-centric developer
certifications of Chapter 06 or the durable `SC` security family. The
general rule generalizes: can I reach a test date, will it renew, and does
something durable cover the same ground?

- [ ] Can state both retirement dates and their exam codes.
- [ ] Can explain why the withdrawal of renewal assessments matters more
      in Microsoft's annual model.
- [ ] Knows a retirement does not invalidate a held credential.
- [ ] Can name where developer and security subject matter now lives.
- [ ] Has made and recorded a dated go/no-go decision for both.
- [ ] Completed the hands-on lab, including the third-party-discrepancy
      negative test.
