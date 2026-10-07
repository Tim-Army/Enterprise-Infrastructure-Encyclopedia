# Volume CLXXIII — Integrated Master Schedule (IMS)

> A practitioner's guide to building and running an **integrated master
> schedule (IMS)**: the integrated master plan and work breakdown structure
> under it, network logic, durations and resources, the critical path, schedule
> quality checks, baselining and earned value, statusing and change control,
> schedule risk analysis, and contract reporting, with every lab worked in
> **Microsoft Project**, **Primavera P6**, and **ProjectLibre**.

## Overview

Volume CLXXIII is a **vendor-neutral program management volume** on the
integrated master schedule, the single networked schedule of all the work needed
to deliver a program. It follows the approach used on U.S. Department of Defense
and other government programs, where the IMS is a contract deliverable and is
judged against the DoD IMP/IMS guide, the GAO Schedule Assessment Guide, the DCMA
14-point assessment, and EIA-748 earned value guidelines. The same practices make
any large program's schedule more trustworthy.

The volume follows one **sample program**, a branch network modernization that
replaces firewalls and adds SD-WAN at four sites, from an empty project file to
a baselined, statused, risk-analyzed, and reported IMS. Every lab gives steps
for all three tools: **Microsoft Project**, the tool most DoD contractors use;
**Primavera P6**, Oracle's enterprise scheduler; and **ProjectLibre**, a free,
open-source tool anyone can use to follow along.

Chapters follow the life of an IMS:

- **Chapter 01** defines the IMS and its integration with the IMP, WBS, and
  earned value, introduces the governing guidance, and sets up the project in all
  three tools.
- **Chapter 02** builds the work breakdown structure and integrated master plan,
  and codes tasks for vertical traceability.
- **Chapter 03** builds the network: activities, relationship types, leads, lags,
  constraints, and the sample program's full logic.
- **Chapter 04** adds durations, calendars, and resources, and resolves
  over-allocation.
- **Chapter 05** computes the critical path by hand and in each tool, and adds
  schedule margin.
- **Chapter 06** checks schedule quality against the DCMA 14-point assessment
  and GAO best practices, with a checking script.
- **Chapter 07** baselines the IMS and integrates it with earned value: PV, EV,
  AC, SPI, CPI, BEI, CPLI, and earned schedule.
- **Chapter 08** runs the status cycle, handles out-of-sequence progress, and
  controls change, including rolling wave planning.
- **Chapter 09** runs a Monte Carlo schedule risk analysis and sizes margin from
  it.
- **Chapter 10** produces reports and contract deliverables, including the
  IPMDAR, and exchanges schedules between tools.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic
hands-on labs and knowledge checks.

## Chapters

1. [IMS Fundamentals — What an Integrated Master Schedule Is](chapters/01-ims-fundamentals-what-an-integrated-master-schedule-is.md) — the IMS, its integration with the IMP, WBS, and EVM, governing guidance, and the three tools.
2. [The Integrated Master Plan and the Work Breakdown Structure](chapters/02-the-integrated-master-plan-and-the-work-breakdown-structure.md) — product-oriented WBS, control accounts, IMP events and criteria, and coding for traceability.
3. [Building the Network — Activities, Logic, and Relationships](chapters/03-building-the-network-activities-logic-and-relationships.md) — well-formed activities, FS/SS/FF/SF, leads, lags, constraints, deadlines, and open ends.
4. [Durations, Calendars, and Resource Loading](chapters/04-durations-calendars-and-resource-loading.md) — estimating methods, work and units, calendars, resources, cost, and leveling.
5. [The Critical Path, Float, and Schedule Margin](chapters/05-the-critical-path-float-and-schedule-margin.md) — forward and backward passes, total and free float, longest path, and margin.
6. [Schedule Quality — The DCMA 14-Point Assessment and GAO Best Practices](chapters/06-schedule-quality-the-dcma-14-point-assessment-and-gao-best-practices.md) — the 14 metrics, the ten best practices, and a checking script.
7. [Baselining and Integrating with Earned Value](chapters/07-baselining-and-integrating-with-earned-value.md) — baselines, the PMB, earned value measures, BEI, CPLI, and earned schedule.
8. [Statusing and Maintaining the IMS](chapters/08-statusing-and-maintaining-the-ims.md) — the status cycle, invalid dates, out-of-sequence progress, change control, and rolling wave planning.
9. [Schedule Risk Analysis](chapters/09-schedule-risk-analysis.md) — three-point estimates, risk events, Monte Carlo simulation, merge bias, and margin sizing.
10. [Reporting and Contract Deliverables](chapters/10-reporting-and-contract-deliverables.md) — the IPMDAR, schedule narratives, visuals, and exchanging schedules between tools.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all ten chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Related volumes

This is a vendor-neutral program management volume, not a certification-tracks
volume, and it is not mapped to a single exam blueprint. The sample program it
schedules draws on the network work covered in
[Fortinet Network Security (XIX)](../volume-019-fortinet-network-security/README.md)
and [Microsegmentation Options (LXXXVII)](../volume-087-microsegmentation-options/README.md).
For the security compliance work that often runs alongside a government program's
IMS, see [DISA SRGs and STIGs (CLXXII)](../volume-172-disa-srgs-and-stigs/README.md),
whose Chapter 09 covers the POA&Ms and milestones of a STIG compliance program.

## Lab coverage

There is **one lab set for every chapter**, all built around the same sample
program, so each lab starts from the result of the previous chapter. Every lab
gives steps for Microsoft Project, Primavera P6, and ProjectLibre; ProjectLibre
is free, so the whole volume can be completed without a commercial license.
Chapters 06 and 09 include Python scripts (a DCMA build-quality checker and a
Monte Carlo risk simulation) that work with any of the three tools. Each lab
states an objective, prerequisites, numbered steps with expected results, a
negative test, and rollback, and ends with a `**Lab verified by:** *pending*`
sign-off.

## Software and platform baseline

This volume references the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): the current desktop release
of **Microsoft Project**, the current release of **Primavera P6 Professional**,
and **ProjectLibre 1.9.x**, as of 2026-10. Menu locations change between
releases, especially in ProjectLibre and Primavera P6; check your version's help
if a command is not where a lab says. Government guidance (the IPMDAR data item,
MIL-STD-881, and EIA-748) is revised periodically; confirm the current revision
your contract cites.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-173-integrated-master-schedule
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
