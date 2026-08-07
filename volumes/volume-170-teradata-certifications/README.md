# Volume CLXX — Teradata Certification Tracks

> The Teradata Vantage Certification program — verified 6 August 2026 on `teradata.com/university/certification`.
> Teradata is the pioneer and leader of the enterprise **data warehouse**, built on **MPP (massively parallel
> processing)** — a **shared-nothing** engine that distributes data across **AMPs** and queries it in parallel.
> Today it is cloud: **Teradata Vantage / VantageCloud** (**Lake** = cloud-native, elastic, lakehouse;
> **Enterprise** = full data warehouse). Certifications are transitioning from the legacy **Vantage 2** track to
> the current **VantageCloud Lake** track — the flagship is the **Associate VantageCloud Lake 2.0** exam (**$149**,
> **75 min**, Pearson VUE, digital badge, **no prerequisites**, **no expiration**). Every lab runs **free** in
> Python. A cloud-data-warehouse / MPP-analytics volume.

## Overview

**Teradata** is the platform that defined the **enterprise data warehouse** — running analytics on enormous data
with a **shared-nothing MPP** architecture that scales linearly by distributing data across parallel processing
units (**AMPs**). Now cloud-native as **Teradata Vantage / VantageCloud**, it keeps that powerful engine while
adding elasticity, open formats, and in-database analytics. Teradata sits alongside the cloud data platforms this
shelf covers ([Snowflake XLIX](../volume-049-snowflake-certifications/README.md),
[Databricks XLVIII](../volume-048-databricks-certifications/README.md),
[Cloudera CLVIII](../volume-158-cloudera-certifications/README.md)) — its distinctive angle is MPP depth and the
**Primary Index** distribution model.

Chapter 02 covers **Vantage and VantageCloud** (Lake vs Enterprise). Chapters 03–08 take the discipline: **the MPP
architecture**, **data distribution and the Primary Index**, **SQL and querying at scale**, **physical database
design**, **workload management and administration**, and **ClearScape Analytics and the modern platform**.
Chapter 09 closes on choosing a path, with a capstone across the whole analytics lifecycle.

A theme runs through it: **distribute** (Primary Index), **design** (indexes/PPI), **query** (parallel SQL +
optimizer), **operate** (workload/space), and **analyze** (ClearScape in-database) — enterprise analytics on a
shared-nothing MPP engine.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Teradata Certification Program](chapters/01-the-teradata-program.md) | 1.1–1.2 |
| 02 | [Teradata Vantage and VantageCloud](chapters/02-vantage-and-vantagecloud.md) | 2.1 |
| 03 | [The MPP Architecture](chapters/03-the-mpp-architecture.md) | 3.1 |
| 04 | [Data Distribution and the Primary Index](chapters/04-data-distribution-and-primary-index.md) | 4.1 |
| 05 | [SQL and Querying at Scale](chapters/05-sql-and-querying.md) | 5.1 |
| 06 | [Physical Database Design](chapters/06-physical-database-design.md) | 6.1 |
| 07 | [Workload Management and Administration](chapters/07-workload-management-and-administration.md) | 7.1 |
| 08 | [ClearScape Analytics and the Modern Platform](chapters/08-clearscape-and-modern-platform.md) | 8.1 |
| 09 | [Choosing Your Teradata Path](chapters/09-choosing-your-teradata-path.md) | 9.1–9.2 |

## The certifications

Transitioning from legacy to current:

| Track | Certifications |
| --- | --- |
| **VantageCloud Lake (current)** | Associate VantageCloud Lake 2.0 ($149/75min) · Associate VantageCloud Lake |
| **Vantage 2 (legacy, winding down)** | Associate 2.4/2.3 · Data Engineering · Administration · (Analytics/Data Science/Architecture retired 31 Jul 2024) |

**Mechanics:** Pearson VUE · digital badges (Credly) · **no prerequisites** · **no expiration** · 74,000+ awarded.
Guidance: target the **VantageCloud Lake Associate** (current); verify retired legacy exams before planning.

## What you will be able to do

- Read the Teradata program — current VantageCloud Lake vs legacy Vantage 2, and the exam mechanics.
- Explain Vantage/VantageCloud — Lake (cloud-native, elastic, lakehouse) vs Enterprise (full data warehouse).
- Describe the MPP architecture — Parsing Engine, AMPs, BYNET, shared-nothing parallelism.
- Choose a Primary Index — even distribution vs skew, single-AMP access, and join co-location.
- Query at scale — Teradata SQL, the cost-based optimizer, joins, and statistics.
- Design for performance — types, secondary/join indexes, and PPI partition elimination.
- Administer — workload management (TASM), space (spool), users, and governance.
- Run modern analytics — ClearScape in-database ML, QueryGrid, and the open lakehouse.

## Prerequisites

- Familiarity with SQL and relational databases helps.
- A Linux or macOS host with `python3`. **Teradata certifications** are delivered via Pearson VUE (Associate
  VantageCloud Lake ~$149; no prerequisites; no expiration).

## See also

- [Volume XLIX — Snowflake](../volume-049-snowflake-certifications/README.md), [Volume XLVIII — Databricks](../volume-048-databricks-certifications/README.md), and [Volume CLVIII — Cloudera](../volume-158-cloudera-certifications/README.md) — cloud data-platform peers.
- [Volume CLXVIII — SAS](../volume-168-sas-certifications/README.md) — analytics and in-database ML.
- [Volume CLXV — Informatica](../volume-165-informatica-certifications/README.md) — data integration feeding the warehouse.
