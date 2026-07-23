# Chapter 20: VMware Telco Cloud, and Keeping the Certification Program Current

![Two halves. On the left, the three Telco Cloud specialist skills exams on the older 5V0 generation — Telco Cloud Platform Specialist (5V0-36.22), Telco Cloud NFV Specialist (5V0-37.22), and Telco Cloud Automation Specialist (5V0-44.21) — targeting service-provider network-functions virtualization outside the mainstream vSphere and VCF paths. On the right, a four-step currency check that repeats on a cadence: re-list the tiers and tracks from Broadcom's certification pages, re-confirm every exam code against its own page, flag retirements and new generations, and update this volume and its appendix. An arrow returns from step four to step one.](../../../diagrams/volume-05-vmware-virtualization/chapter-20-telco-and-program-currency-map.svg)

*Figure 20-1. A niche specialist track and the recurring check that keeps the whole VMware certification map in this volume honest — the program churns, so the check repeats.*

## Learning Objectives

- Identify the three VMware Telco Cloud specialist skills exams — Platform
  (5V0-36.22), NFV (5V0-37.22), and Automation (5V0-44.21) — and place them
  as a service-provider niche outside the mainstream vSphere/VCF and NSX
  paths.
- Explain what the `5V0` specialist-skills code family is and how it
  differs from the `2V0`/`6V0` professional and `3V0` advanced families in
  earlier chapters.
- Explain why the VMware certification program requires a recurring
  currency check, using the program's own recent churn (the Broadcom
  acquisition, VCF 9.0's new role series, generational code changes) as the
  evidence.
- Run a four-step currency check against Broadcom's primary sources that
  re-verifies the tiers, every exam code, retirements, and this volume's
  and appendix's accuracy — and know why third-party summaries are not
  acceptable sources for it.
- Feed the check's findings back into this volume, its Master Appendices
  course catalog, and the repository's certification blueprint, keeping the
  whole VMware map current rather than letting it drift silently.

## Theory and Architecture

Two things belong at the end of this volume's certification coverage: the
one remaining VMware track it has not addressed — **Telco Cloud** — and the
discipline that keeps everything the volume claims about the program *true*
over time. They are paired here deliberately: Telco Cloud is a small, older
niche whose exams are most likely to change availability quietly, which
makes it the natural example for why a recurring currency check matters.

As with every preparation chapter here, this is study and review material.
It names exam codes verified against Broadcom's certification pages; it does
not reproduce exam content. Confirm current codes, availability, and
blueprints directly before scheduling — this chapter's second half exists
precisely because that confirmation is not optional.

### The Telco Cloud specialist skills exams

VMware Telco Cloud targets communications service providers running
**network functions virtualization (NFV)** — the virtualized 4G/5G core and
RAN workloads that run on a telco-grade platform built from vSphere, NSX,
and VMware's Telco Cloud products. Three specialist skills exams cover it:

| Exam | Code | Scope |
| --- | --- | --- |
| Telco Cloud Platform Specialist | 5V0-36.22 | The CaaS/telco platform layer on vSphere + NSX |
| Telco Cloud NFV Specialist | 5V0-37.22 | NFV infrastructure — the virtualized network-functions layer |
| Telco Cloud Automation Specialist | 5V0-44.21 | Telco Cloud Automation (TCA) orchestration of network functions |

These are a **service-provider specialization**, not a step in the
vSphere/VCF/NSX progression the rest of this volume follows. A general
enterprise administrator does not need them; an engineer at a mobile
operator or NFV integrator does. They build on the vSphere and NSX
foundations this volume teaches (Chapters 1–11), but their subject matter —
telco platform, NFV infrastructure, TCA orchestration — sits outside it.

### The `5V0` code family, in context

This volume has now touched four VMware exam-code families, and the prefix
is a reliable signal of tier and scope:

- **`2V0`** — mainstream professional (VCP): broad, role-defining
  (Chapters 12–17).
- **`6V0`** — specialist professional: narrow single-product VCP (VCP-AVI,
  VCP-PCS, Chapter 17).
- **`3V0`** — advanced (VCAP): advanced depth, design or deploy
  (Chapter 18).
- **`5V0`** — **specialist skills**: focused skills exams for a specific
  solution area, this chapter's Telco Cloud exams among them. Their older
  `.21`/`.22` generation dates flag that they trail the current product
  releases, which is exactly the kind of fact a currency check must
  re-confirm.

### Why the program needs a recurring currency check

The rest of this chapter is not about an exam. It is about a maintenance
discipline, and it is here because the VMware certification program has
churned more than almost any other on this shelf:

- The **Broadcom acquisition** reorganized the entire program — renaming
  VCDX to Distinguished Expert, restructuring VCP around VVF/VCF, and
  moving training to Learning@Broadcom.
- **VCF 9.0** introduced an entirely new eight-exam advanced role series
  (Chapter 18) on `.25`/`.26` codes that did not exist a generation ago.
- Individual exams change generation — VCP-DCV sits on vSphere 8 while the
  VVF/VCF exams moved to 9.0 — and specialist exams like Telco Cloud's can
  be retired quietly as their products age.

A volume that states exam codes will drift out of true unless someone
re-verifies it. This volume's answer is a scheduled check, run on the same
cadence as the repository's other certification-currency checks, against
Broadcom's own pages — never third-party summaries, which drift worse than
the vendor and have been found wrong during exactly these checks elsewhere
in this encyclopedia.

## Design Considerations

- **Take a Telco Cloud exam only for a service-provider role.** These are a
  genuine specialization. For enterprise vSphere/VCF/NSX work they are off
  the path; pursue them when the job is NFV, a virtualized mobile core, or
  a telco platform integration, and skip them otherwise.
- **Confirm Telco Cloud availability before planning.** Because the `5V0`
  Telco exams are on an older generation, they are among the most likely in
  this volume to be retired or renumbered. Verify each still exists on
  Broadcom's page before investing study time — do not assume from this
  chapter that 5V0-36.22, 5V0-37.22, and 5V0-44.21 are all still live.
- **Run the currency check on a cadence, not on demand.** The value of the
  check is that it catches silent drift — an exam retired, a code bumped a
  generation, a new role added — before a reader relies on stale
  information. Schedule it; do not wait for a reader to hit a dead link.
- **Primary sources only.** The check is worthless if it trusts aggregator
  sites. Every code is confirmed against its own exam page on Broadcom, and
  the tier/track list against Broadcom's certification landing pages. A
  third-party "2026 VMware certification guide" is a lead to verify, never
  a source to cite.
- **Feed findings all the way through.** A currency check that updates only
  this chapter leaves the volume README, the study plans, the
  [Master Appendices course catalog](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md),
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  stale. Propagate every change to all of them in one pass.

## Implementation and Automation

### The four-step currency check

```text
# Run on the repository's certification-currency cadence. Each step's
# output feeds the next; step 4 closes the loop back to this volume.

1. Re-list tiers & tracks
   Source: Broadcom certification landing pages
   Output: current set of VCP / VCAP / Distinguished Expert / specialist
           credentials and their tracks (vSphere, VCF, NSX, Avi, PCS,
           Telco Cloud)

2. Re-confirm every exam code
   Source: each exam's own page (never a third-party summary)
   Output: verified code per exam; note any that no longer resolve

3. Flag retirements & new generations
   Output: exams retired or superseded (with any published end date),
           and new codes/roles that have appeared since last check

4. Update this volume + appendix
   Targets: Volume V chapters, README exam tables & study plans,
            Master Appendices Chapter 07 course catalog,
            CERTIFICATION_BLUEPRINTS.md
```

### Harvesting codes from Broadcom's own data source

```bash
# Broadcom's certification pages inject the exam code from a JSON API
# rather than in the raw HTML, so a plain fetch of the page misses it.
# Query the education-program JSON endpoint per certification slug and
# read the code out — the primary-source method used to verify this
# volume. Replace <slug> with the certification's URL slug.
curl -s 'https://www.broadcom.com/api/getjson?url=support/education/vmware/certification/<slug>&locale=en-us&type=education_program' \
  | grep -oE '[0-9]V0-[0-9]{2}\.[0-9]{2}'
```

### A drift log to make the check auditable

```text
# Record each check so drift is visible over time. One row per finding.

Date       | Exam / item          | Was          | Now / status      | Action
-----------|----------------------|--------------|-------------------|--------
2026-07-22 | VCF role series      | (absent)     | 3V0-11.26 … 25.25 | added ch18
2026-07-22 | VCDX                 | VCDX code    | Distinguished Exp | added ch19
2026-07-22 | Telco Cloud (5V0)    | —            | still live        | added ch20
```

## Validation and Troubleshooting

- **A resolving exam page is the pass signal.** For each code, the check
  passes when the exam's own Broadcom page resolves and shows that code. A
  page that 404s or shows a different code is the finding — record it in the
  drift log and trace it to a retirement or a generation bump.
- **Silence is the failure mode.** The risk this check addresses is not a
  wrong answer but an unnoticed change. If a check finds nothing, confirm it
  actually re-verified every code rather than skipping — a check that
  quietly no-ops is worse than none, because it manufactures false
  confidence.
- **Cross-check the appendix and blueprint.** After updating chapters,
  verify the [course catalog appendix](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md)
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  carry the same codes and the same retirements. A mismatch between them and
  this volume is itself a drift finding.
- **Telco Cloud is the canary.** Of everything this volume tracks, the
  `5V0` Telco exams are the likeliest to change first. If a check finds one
  retired, treat it as a prompt to re-verify the whole program more
  carefully, not as an isolated edit.

## Security and Best Practices

- Verify only against Broadcom's official domains; a currency check that
  follows a link from a search result to a look-alike site defeats its own
  purpose. Confirm you are on `broadcom.com` before trusting a code.
- Do not publish or circulate any exam content encountered while verifying —
  the check reads certification and exam-guide *metadata* (codes, names,
  tiers), never exam items, and must stay on that side of the line.
- Register for any Telco Cloud exam only through Broadcom's authorized
  testing partner, and confirm current identification and proctoring
  requirements from the official portal before exam day.
- Keep the drift log with the repository, not in a personal note — the
  point is that the next person to run the check inherits a verifiable
  history rather than re-deriving it from scratch.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative certification landing pages and per-exam guides for the
  Telco Cloud specialist exams (5V0-36.22, 5V0-37.22, 5V0-44.21) and for
  the whole program the currency check re-verifies.
- [VMware Telco Cloud documentation](https://techdocs.broadcom.com/us/en/vmware-sonp/telco-cloud.html) —
  product reference for the Telco Cloud Platform, NFV, and Automation
  exams.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  the repository's certification-to-volume mapping that the check keeps
  current.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  the course catalog the check updates alongside this volume.
- See [Chapters 17–19](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md)
  for the VCP, VCAP, and Distinguished Expert tiers this check verifies.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Name the three Telco Cloud specialist exams and explain why they are off
   the path for a general enterprise administrator.
2. Distinguish the `2V0`, `6V0`, `3V0`, and `5V0` code families by tier and
   scope, giving one exam in each.
3. Give three specific changes in the VMware program since the Broadcom
   acquisition that justify a recurring currency check.
4. Walk through the four-step currency check and explain why step 2 forbids
   third-party summaries as sources.
5. Why are the `5V0` Telco Cloud exams described as the "canary" for this
   volume's currency, and what should finding one retired trigger?

## Hands-On Lab

**Objective:** Run one complete currency check against Broadcom's primary
sources for a subset of this volume's exams, producing a drift log — the
maintenance skill this chapter teaches, exercised for real.

**Prerequisites**

- Web access to Broadcom's certification pages.
- The four-step check and the drift-log format from the Implementation
  section.
- This volume's current exam codes (Chapters 12–20) to check against.

**Steps**

1. **Re-list (target 15 minutes).** From Broadcom's certification landing
   pages, list the current VMware credential tiers and tracks. Compare
   against this volume's coverage (VCP, VCAP, Distinguished Expert, Avi,
   PCS, Telco Cloud).

   **Expected result:** a current tier/track list, with any credential this
   volume omits or names differently noted.

2. **Re-confirm codes (target 20 minutes).** For at least five exams across
   different families (one each of `2V0`, `6V0`, `3V0`, `5V0`, plus one
   more), open each exam's own Broadcom page and confirm the code matches
   this volume.

   **Expected result:** each code confirmed, or a mismatch recorded — do
   not accept a code from anything but the exam's own page.

3. **Flag changes (target 10 minutes).** Note any exam whose page does not
   resolve or shows a new code or generation, and any published retirement
   or end date.

   **Expected result:** a list of findings, empty or not, each traceable to
   a primary source.

4. **Log (target 10 minutes).** Record every finding in the drift-log
   format, with date, what it was, what it is now, and the action needed in
   this volume, the appendix, and the blueprint.

   **Expected result:** an auditable drift log a future checker can build
   on.

5. **Verify the loop closes.** For one finding (or, if none, one code you
   confirmed unchanged), confirm this volume, the appendix, and
   CERTIFICATION_BLUEPRINTS.md all agree. A disagreement is itself a
   finding.

   **Expected result:** the three sources are consistent, or the
   inconsistency is logged.

6. **Cleanup:** file the drift log with the repository; there is no
   infrastructure to tear down.

## Lab Verification

Complete this sign-off once a currency check has been run end to end and a
drift log produced. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VMware Telco Cloud is the service-provider specialization the rest of this
volume does not cover: three `5V0` specialist skills exams — Platform
(5V0-36.22), NFV (5V0-37.22), and Automation (5V0-44.21) — on an older
generation, relevant to NFV and virtualized-core work and off the path for
general enterprise administration. Their age makes them the canary for the
program's churn, which is why this chapter pairs them with a four-step
currency check: re-list the tiers, re-confirm every code against its own
Broadcom page, flag retirements and new generations, and propagate every
change through this volume, the Master Appendices course catalog, and the
repository blueprint. The program has changed enough since the Broadcom
acquisition that this check is maintenance, not optional — and its cardinal
rule is primary sources only.

- [ ] Can name the three Telco Cloud exams and who should take them.
- [ ] Can distinguish the `2V0`/`6V0`/`3V0`/`5V0` code families by tier and
      scope.
- [ ] Can justify a recurring currency check from the program's own churn.
- [ ] Can run the four-step check against Broadcom's primary sources.
- [ ] Understands why third-party summaries are never acceptable sources.
- [ ] Has produced a drift log and confirmed the volume, appendix, and
      blueprint agree.
- [ ] Completed the hands-on currency-check lab.
