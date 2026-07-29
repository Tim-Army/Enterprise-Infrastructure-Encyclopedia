# Volume LXI — Cribl Certification Tracks

> The whole Cribl certification ladder in one volume — CC User, CC Admin (Stream and
> Edge), CC Engineer, and the partner CCSC — across Stream, Edge, Search, and Lake, with
> hands-on Cribl config, REST API, and pipeline labs mapped to every topic area, verified
> against cribl.io/university.

## Overview

Volume LXI maps the **Cribl** certification program — the credentials for building and
operating the **observability data pipeline** (Stream, Edge, Search, Lake) that routes,
reduces, enriches, and replays telemetry to control cost and get the right data to the
right place. It sits with the encyclopedia's **observability** volumes (Observability XI,
Splunk XLV, OpenTelemetry LIV, Prometheus LV).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LVI): it
maps the program — which credentials exist, their topic areas, and levels — and teaches
each with a hands-on walkthrough. Every credential was **verified against cribl.io/university
on 27 July 2026**. The certifications are **free**, delivered as **online self-study**
through Cribl University, and **valid three years**.

Chapters are organized by credential:

- **Chapter 01** frames the program — the products, the ladder, and the API.
- **Chapter 02** takes the foundation **CC User** (all products).
- **Chapters 03–04** take **CC Admin - Stream** (sources/routes/pipelines, then functions/
  packs/optimization).
- **Chapter 05** takes **CC Admin - Edge** (nodes/fleets/collection).
- **Chapter 06** takes **CC Engineer** (solution design and optimization).
- **Chapter 07** covers **Cribl Search and Lake**.
- **Chapter 08** takes the partner **CCSC** with distributed deployment.
- **Chapter 09** covers keeping current and career paths.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on
labs and knowledge checks.

## Chapters

1. [The Cribl Certification Program](chapters/01-the-cribl-certification-program.md) — products, ladder, and the API.
2. [CC User — Foundation](chapters/02-cc-user-foundation.md) — deployment, the four products, the Stream flow.
3. [CC Admin - Stream — Sources, Routes, and Pipelines](chapters/03-cc-admin-stream-sources-routes-and-pipelines.md) — the data path.
4. [CC Admin - Stream — Functions, Packs, and Optimization](chapters/04-cc-admin-stream-functions-packs-and-optimization.md) — reduce, enrich, mask, reuse.
5. [CC Admin - Edge — Nodes, Fleets, and Collection](chapters/05-cc-admin-edge-nodes-fleets-and-collection.md) — source-side collection.
6. [CC Engineer — Solution Design and Optimization](chapters/06-cc-engineer-solution-design-and-optimization.md) — end-to-end architecture.
7. [Cribl Search and Lake](chapters/07-cribl-search-and-lake.md) — query-in-place and cheap storage/replay.
8. [CCSC and Distributed Deployment](chapters/08-ccsc-and-distributed-deployment.md) — leader/workers, commit/deploy, sizing.
9. [Keeping the Cribl Program Current and Career Paths](chapters/09-keeping-the-cribl-program-current-and-career-paths.md) — validity, change, and paths.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Cribl, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The full catalog with
credentials, topic areas, and the Cribl University training model is in the
[Cribl certification appendix](../volume-997-master-appendices/chapters/27-appendix-cribl-certifications-and-course-access.md)
(Master Appendices, Volume CMXCVII). Related practice lives in the observability (XI),
Splunk (XLV), OpenTelemetry (LIV), and Prometheus (LV) volumes.

## Lab coverage

The credential chapters go **per topic**: there is **one walkthrough lab for every topic
area** of each Cribl credential — **36 labs** across the ladder. Because Cribl is a
hands-on data platform, the walkthroughs use real tooling — **Cribl Stream configuration**
(sources/routes/pipelines/functions as specs), the **Cribl REST API**, Cribl **expressions**
and **Search queries**, and the **distributed** commit/deploy model — runnable on the
**Cribl free tier / Cribl.Cloud**. Each lab states an objective, commands/config, expected
results, a negative test, and cleanup, and ends with a **`**Lab verified by:** *pending*`**
sign-off.

## Software and platform baseline

This volume references **cribl.io/university** and **university.cribl.io** (catalog and
courses), **Cribl Stream / Edge / Search / Lake**, the **Cribl free tier / Cribl.Cloud** for
practice, and the Cribl REST API. Credentials were verified against cribl.io on 27 July
2026; Cribl revises the program as the portfolio evolves, so confirm the current ladder
before scheduling.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-061-cribl-certifications
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
