# Chapter 09: Keeping the Microsoft Program Current

## Learning Objectives

- Explain the free annual renewal model and how to never let a credential lapse.
- Recognize how betas, retirements, and renumbers move through the program.
- Use the Microsoft Learn Catalog API to detect change programmatically.
- Interpret the Fundamentals tier as a durable, non-expiring foundation where applicable.
- Build an organizational process for keeping a certification map current.

## Theory and Architecture

Microsoft's program is a **moving target**, and keeping current is a skill in
itself. Three mechanisms drive change, and one mechanism keeps you covered.

**Renewal.** Microsoft **role-based** certifications are valid for **one
year** and renew through a **free, unproctored online assessment** on
Microsoft Learn, available in the **six months before expiry**. Pass it and
the credential extends another year — no re-exam, no fee. This is the single
most important operational fact: a Microsoft credential is cheap to *earn*
relative to its competitors and effectively free to *keep*, but only if you
renew in the window. (Fundamentals credentials have historically not expired,
though Microsoft has adjusted this over time — confirm on the credential's
page.)

**Betas.** New exams often launch in **beta**: discounted, with results
delivered only after the beta period closes and the passing bar is set. Betas
are how the newest content — the 2026 AI and agent wave, GH-600, SC-500 —
enters the program. Taking a beta is a way to certify early, at the cost of
delayed scoring.

**Retirements and renumbers.** Exams **retire** when their technology is
superseded (DP-203 → DP-700 for Fabric; SC-400 → SC-401; AI-900 → AI-901;
MS-100/101 → MS-102), and Microsoft posts **retirement notices** on the exam
page and in the certification's change log. A renumber is not cosmetic — the
blueprint usually changes with it.

**The Catalog API** is how you detect all of this without manual page-checking.
`learn.microsoft.com/api/catalog` returns every credential and exam as JSON
with `certification_type`, title (flagging `(beta)`/`(legacy)`), and links —
the reliable source for a scripted currency check.

## Design Considerations

Build a **renewal discipline**: track every held credential's expiry, and
diarize the renewal window (six months before). For teams, centralize this —
a lapsed credential is wasted investment. Treat the **free renewal
assessment** as lightweight but real; it reflects the current blueprint, so a
credential that renews also stays current on content.

Plan for **change**. Before starting study, verify the target exam's **code,
name, and status** on Learn; a study guide older than a few months may target
a retired exam. Re-verify **fast-moving families** (AI, data/Fabric, security)
more often than stable ones. Decide a policy on **betas** — they are good for
early adopters and for shaping a training program, less good when you need a
guaranteed near-term pass.

Maintain a **certification map** as living data. Re-run a Catalog API check on
a cadence, diff it against your last snapshot, and surface new betas, renames,
and retirements to the people who plan training.

## Implementation and Automation

A scripted currency check diffs the catalog against a saved snapshot:

```bash
# Snapshot today's current credentials
curl -s "https://learn.microsoft.com/api/catalog/?type=certifications&locale=en-us" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin);
print("\n".join(sorted(c["title"] for c in d["certifications"]
  if c["certification_type"] in ("fundamentals","role-based","specialty","business")
  and "(legacy" not in c["title"].lower())))' > certs-today.txt

# Compare with last month'\''s snapshot to see additions/removals
diff certs-lastmonth.txt certs-today.txt   # '<' removed, '>' added (new betas, renames)
```

Check a single exam's retirement status before studying:

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/<slug>/" \
  | grep -iE "retir|will no longer|replaced by" | head
```

## Validation and Troubleshooting

Confirm renewal availability and change status:

```text
Microsoft Learn > your profile > Certifications:
  each credential shows an expiry date and, in the last 6 months, a
  "Renew" button linking to the free assessment.
Certification page: a banner announces a pending retirement or a superseding exam.
```

Common pitfalls: **missing the renewal window** (it opens six months out and
closes at expiry — a lapse means re-earning by exam); studying a **retired or
renumbered** exam because a blog or dump was stale; assuming **betas** score
immediately (they do not); and treating the **Fundamentals** expiry policy as
fixed (confirm on the page). The Catalog API and the credential's change log
are the authoritative signals.

## Security and Best Practices

**Renew on time** — set reminders at the six-month mark for every held
credential. **Verify on Microsoft Learn**, never a dump site, and re-check
fast-moving families often. Use the **Catalog API** for scripted, auditable
currency checks and keep a **snapshot history** so change is visible. For
organizations, own the certification map centrally, feed it into training
plans, and treat the program's volatility (especially AI/agents) as a
standing operational item rather than a one-time survey.

## References and Knowledge Checks

- Microsoft Learn: *Renew your Microsoft Certification*; *Exam retirement policy*; *Beta exams*; *Microsoft Learn Catalog API*.

**Knowledge checks**

1. When does the free renewal window open, and what happens if you miss it?
2. How do beta exams differ from generally available exams in scoring?
3. How can the Catalog API make currency-checking auditable?

## Hands-On Lab

Exam-preparation walkthroughs for keeping current.

**Shared prerequisites for Labs 9.1–9.2** — a browser, `curl`, and `python3`.
**Cost:** none.

### Lab 9.1 — Script a currency snapshot (Topic: Detect change)

**Objective:** Capture today's current credentials for later diffing.

```bash
curl -s "https://learn.microsoft.com/api/catalog/?type=certifications&locale=en-us" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin);
print("\n".join(sorted(c["title"] for c in d["certifications"]
  if c["certification_type"] in ("fundamentals","role-based","specialty","business")
  and "(legacy" not in c["title"].lower())))' | tee certs-today.txt | wc -l
```

**Expected result:** a sorted list of current credentials and a count — the
snapshot you diff next month to see betas, renames, and retirements.

**Negative test:** try to enumerate from the rendered browse page with
`curl | grep`; you get the SPA shell, not the list — use the API.

**Cleanup:** keep `certs-today.txt` as the baseline; remove if not needed.

### Lab 9.2 — Check an exam for retirement (Topic: Verify before studying)

**Objective:** Confirm a target exam is current before investing study time.

```bash
curl -s "https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/" \
  | grep -oE '\bAI-[0-9]{3}\b' | sort -u
# -> AI-901 (AI-900 retired). If your guide says AI-900, it is stale.
```

**Expected result:** the current exam code (AI-901), letting you catch a stale
study plan (AI-900) before wasting effort.

**Negative test:** trust a six-month-old blog's exam code without checking;
you may study a renumbered or retired exam — always verify on Learn.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Microsoft credentials renew for free every year through an online assessment
in the six months before expiry — cheap to hold if you renew on time. The
program changes through betas, retirements, and renumbers, announced on
Microsoft Learn and detectable via the Catalog API. Keeping a scripted,
snapshotted certification map is the durable way to stay current, especially
for the fast-moving AI, data, and security families.

- [ ] I can explain the free annual renewal and its window.
- [ ] I can recognize betas, retirements, and renumbers.
- [ ] I can script a Catalog API currency check and diff snapshots.
- [ ] I can build an organizational process to stay current.
- [ ] I completed Labs 9.1–9.2 including each negative test.
