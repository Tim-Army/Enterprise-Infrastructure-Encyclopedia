# Chapter 09: Specialty Certifications and Certification Operations

## Learning Objectives

- Identify the surviving Azure specialty certifications and the three that
  have been retired
- Explain the adjacent certification families — `SC` security and the
  Windows Server hybrid track — and when an Azure engineer should look at
  them
- Run a four-step, primary-source currency check across the whole Azure
  program
- Distinguish the four notice types Microsoft publishes: retirement,
  renumbering, certification update, and language changes
- Operate a personal certification portfolio: renewal windows, lapses, and
  what to do when a held certification's exam closes

## Theory and Architecture

### What is left of the specialty tier

Verified against Microsoft Learn on **23 July 2026**:

| Specialty certification | Exam | Status |
| --- | --- | --- |
| Azure Virtual Desktop | AZ-140 | Current |
| Azure Cosmos DB Developer | DP-420 | Current (see [Chapter 07](07-data-on-azure-dp-300-dp-420-and-dp-750.md)) |
| Azure for SAP Workloads | AZ-120 | Current |
| Azure IoT Developer | AZ-220 | **Retired** |
| Azure Support Engineer for Connectivity | AZ-720 | **Retired** |
| Azure Stack Hub Operator | AZ-600 | **Retired** |

Half the specialty tier has closed. The pattern matches AWS's
([Volume XVII](../../volume-17-aws-architecture-security/README.md),
Chapter 13), where four of six specialties retired: **specialty
certifications are the least durable investment in any vendor program**,
because they depend on a single product area remaining strategically
important.

- **AZ-140 (Azure Virtual Desktop)** covers planning, delivering, and
  managing virtual desktop experiences — a durable operational need with a
  clear role behind it.
- **AZ-120 (Azure for SAP Workloads)** targets architects and engineers
  running SAP on Azure, including RISE with SAP. Microsoft strongly
  recommends Azure Administrator (AZ-104) first.

### Adjacent families worth knowing

Two families sit outside the Azure-branded lineup but matter to Azure
engineers:

- **`SC` — security, compliance, and identity.** SC-100 (Cybersecurity
  Architect), SC-200 (Security Operations Analyst), and SC-300 (Identity
  and Access Administrator). With AZ-500 retiring
  ([Chapter 05](05-the-retiring-associate-tier-az-204-and-az-500.md)),
  this family is where Microsoft security certification durably lives.
- **Windows Server hybrid administration** — AZ-800, AZ-801, and AZ-802,
  covering Windows Server as a workload across on-premises and hybrid
  environments. Despite the `AZ` prefix, the subject is Windows Server in
  a hybrid estate rather than Azure platform administration.

### Why this program needs a recurring check

Within roughly one year, verified from Microsoft's own pages: AI-900 was
renumbered to AI-901; AI-102 and DP-100 retired; AZ-204 and AZ-500 were
scheduled for retirement; three AI-centric associate certifications
arrived, one on an entirely new `AB` code family; DP-750 was added; three
specialties retired; and AZ-305 and AZ-400 were both updated.

No volume that states exam codes survives that rate of change unattended.

### Four notice types, easily confused

A currency check fails if it cannot tell these apart:

- **Retirement** — the certification, its exam, and (in Microsoft's case,
  significantly) its renewal assessment close. Example: AZ-204 on
  31 July 2026.
- **Renumbering** — the certification continues under a new exam code.
  Example: AI-900 → AI-901.
- **Certification update** — content is revised, the code is unchanged.
  Example: AZ-305 updated 17 April 2026.
- **Language or delivery change** — a localized version or delivery option
  changes while the exam continues. This is the trap AWS's Cloud
  Practitioner page demonstrates (Volume XVII, Chapter 13); read which
  noun the notice attaches to.

## Design Considerations

- **Prefer role-based over specialty for durable value.** Half of Azure's
  specialty tier closed in a year. Where a role-based certification covers
  the same ground, it is the safer multi-year investment.
- **Redirect security effort to the `SC` family.** It has no equivalent
  closure and is Microsoft's stated home for security certification.
- **Do not read `AZ-8xx` as Azure platform.** The Windows Server hybrid
  exams carry the prefix but certify a different subject.
- **Schedule the check; do not wait for a broken link.** The value is
  catching silent drift before a reader relies on it.
- **Primary sources only.** Microsoft Learn's catalog API and the
  certification pages. A third-party listing is a lead to verify, never a
  source to cite — Chapters 05 and 06 both include negative tests proving
  why.
- **Propagate findings completely.** A check that updates only this
  chapter leaves the volume README, the
  [appendix](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md),
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  stale.

## Implementation and Automation

### The four-step currency check

```text
1. Re-list the lineup
   Source: Microsoft Learn catalog API, filtered to Azure
   Output: current certifications by level

2. Re-confirm every exam code
   Source: each certification's own page (the code is in the page HTML)
   Output: verified code per certification

3. Classify every notice
   retirement | renumbering | certification update | language/delivery
   Output: dated findings, each traced to a primary page

4. Update volume + appendix + blueprint
   Targets: Volume XXXIII Chapters 01-09 and README,
            Master Appendices Chapter 09,
            CERTIFICATION_BLUEPRINTS.md
```

### Harvesting the lineup and every code

```bash
# Step 1 — the current Azure lineup, by level
curl -s 'https://learn.microsoft.com/api/catalog/?locale=en-us&type=certifications' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin)
for c in sorted([c for c in d["certifications"] if "azure" in (c["title"]+c["uid"]).lower()],
                key=lambda x: x["certification_type"]):
    print(c["certification_type"].ljust(12), c["uid"].replace("certification.",""))'
```

```bash
# Step 2 — the exam code and any retirement sentence, per certification
for c in azure-fundamentals azure-ai-fundamentals azure-data-fundamentals \
         azure-administrator azure-network-engineer-associate azure-developer \
         azure-security-engineer azure-database-administrator-associate \
         azure-ai-apps-and-agents-developer-associate azure-ai-cloud-developer-associate \
         ai-agent-builder-associate azure-solutions-architect devops-engineer \
         azure-virtual-desktop-specialty azure-cosmos-db-developer-specialty \
         azure-for-sap-workloads-specialty; do
  page=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$c/")
  code=$(printf '%s' "$page" | grep -oE '\b(AZ|AI|DP|SC|AB)-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  note=$(printf '%s' "$page" | sed 's/<[^>]*>/ /g' | tr -s ' ' \
         | grep -oE 'This certification[^.]{0,110}\.' | head -1)
  printf '%-46s %-12s %s\n' "$c" "${code:-NONE}" "$note"
done
```

### A drift log

```text
Date       | Item                    | Was       | Now                    | Action
-----------|-------------------------|-----------|------------------------|--------
2026-07-23 | Azure AI Fundamentals   | AI-900    | AI-901 (AI-900 retired |
           |                         |           | 30 Jun 2026)           | ch02
2026-07-23 | Azure AI Engineer       | AI-102    | retired                | ch06
2026-07-23 | Azure Data Scientist    | DP-100    | retired                | ch06
2026-07-23 | Azure Developer         | AZ-204    | retires 31 Jul 2026    | ch05
2026-07-23 | Azure Security Engineer | AZ-500    | retires 31 Aug 2026    | ch05
2026-07-23 | AI Agent Builder        | (absent)  | AB-620 (new family)    | ch06
```

## Validation and Troubleshooting

- **A resolving page with a matching code is the pass signal.** Anything
  else is a finding to trace and log.
- **Silence is the failure mode.** A check that finds nothing must be
  confirmed to have actually re-verified every certification; a quiet
  no-op manufactures false confidence.
- **Classify before recording.** A renumbering logged as a retirement, or
  an update logged as a renumbering, corrupts the log for whoever runs the
  next check.
- **Cross-check the three artifacts.** Volume, appendix, and blueprint
  must agree; disagreement is itself a finding.
- **The specialty tier and the AI tier are the canaries.** Both have moved
  most. Movement there should prompt a full re-verification rather than a
  local edit.

## Security and Best Practices

- Verify only against `learn.microsoft.com`. A check that follows a search
  result to a look-alike domain defeats its purpose.
- The check reads certification metadata — names, codes, levels, dates.
  It never touches exam content and must stay on that side of the line.
- Keep the drift log in the repository so the next checker inherits a
  verifiable history.
- Guard your own certification record: the Microsoft Learn transcript is
  the authoritative statement of what you hold and when it expires. Share
  transcript links deliberately, since they identify you.
- Register only through Microsoft's official scheduling flow.

## References and Knowledge Checks

**References**

- [Microsoft Learn — Browse Credentials](https://learn.microsoft.com/en-us/credentials/browse/?products=azure)
- [Microsoft Learn Catalog API](https://learn.microsoft.com/api/catalog/)
- [Microsoft Certified: Azure Virtual Desktop Specialty](https://learn.microsoft.com/en-us/credentials/certifications/azure-virtual-desktop-specialty/) (AZ-140)
- [Microsoft Certified: Azure for SAP Workloads Specialty](https://learn.microsoft.com/en-us/credentials/certifications/azure-for-sap-workloads-specialty/) (AZ-120)
- [Certification renewal](https://learn.microsoft.com/en-us/credentials/support/renew-your-microsoft-certification)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name the surviving Azure specialty certifications and the three that
   retired.
2. Why are specialty certifications a less durable investment than
   role-based ones, in this program and in AWS's?
3. Where should Microsoft security certification effort go now, and why?
4. Distinguish the four notice types, giving a current example of each.
5. A currency check reports no findings. What must you confirm before
   accepting it?

## Hands-On Lab

**Objective:** Run one complete, primary-source currency check across the
Azure program and produce an auditable drift log — and audit your own
certification portfolio while you are at it.

**Cost note:** Free. No Azure resources are created.

**Prerequisites**

- Web access to Microsoft Learn.
- This volume's stated codes (Chapters 01–08) to check against.
- Your Microsoft Learn certification record, if you hold any.

**Steps**

1. **Re-list (10 minutes).** Run the catalog query and compare against
   Chapter 01's table.

   **Expected result:** a match, or a documented difference.

2. **Re-confirm codes (20 minutes).** Run the per-certification loop.

   **Expected result:** every code confirmed from a Microsoft page. Any
   `NONE` is a finding to chase manually, not to ignore.

3. **Classify notices (10 minutes).** For each notice found, classify it
   as retirement, renumbering, update, or language/delivery, and record
   which noun it attached to.

   **Expected result:** each correctly classified, including at least one
   that is *not* a retirement.

4. **Log (10 minutes).** Record findings in the drift-log format with
   date, previous state, current state, and the action needed.

   **Expected result:** an auditable log.

5. **Audit your own portfolio (15 minutes).** For each certification you
   hold, record its expiry, whether a renewal assessment is still offered,
   and your renewal window.

   **Expected result:** a dated plan — particularly for any credential
   whose exam is closing, where no renewal path will exist.

6. **Negative test (10 minutes).** Compare a third-party Azure
   certification listing against your harvest.

   **Expected result:** at least one discrepancy — AI-900 still shown,
   AI-102 still listed as current, or the new `AB` certification absent.

7. **Close the loop.** Confirm this volume, the appendix, and
   CERTIFICATION_BLUEPRINTS.md agree with your harvest, and file the drift
   log. Nothing to tear down.

## Lab Verification

Complete this sign-off once a full currency check has been run, a drift log
produced, and your own portfolio audited. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Half the Azure specialty tier has closed: **AZ-140**, **DP-420**, and
**AZ-120** survive while **AZ-220**, **AZ-720**, and **AZ-600** are
retired — the same pattern AWS's specialty tier shows, and the reason
role-based certifications are the more durable investment. Security
certification lives durably in the **`SC` family** now that AZ-500 is
closing, and the `AZ-8xx` Windows Server hybrid exams certify a different
subject despite the prefix. Because this program renumbered, retired,
added, and updated certifications across a single year, this chapter
defines the four-step currency check: re-list from the catalog API,
re-confirm every code from its certification page, classify each notice as
retirement, renumbering, update, or language change, and propagate findings
through this volume, the appendix, and the blueprint. Primary sources only.

- [ ] Can name the surviving and retired Azure specialties.
- [ ] Can explain why specialty certifications are less durable.
- [ ] Knows the `SC` family is the durable home for security.
- [ ] Can distinguish the four notice types with current examples.
- [ ] Has produced a drift log and audited a personal portfolio.
- [ ] Completed the hands-on currency-check lab, including the negative
      test.
