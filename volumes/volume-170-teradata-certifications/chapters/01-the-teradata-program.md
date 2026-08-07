# Chapter 01: The Teradata Certification Program

## Learning Objectives

- Describe Teradata as the MPP data-warehouse leader and where certification fits.
- Distinguish the current VantageCloud Lake track from the legacy Vantage 2 track.
- Understand the exam mechanics — Pearson VUE, digital badges, no expiration.
- Recognize the Associate VantageCloud Lake 2.0 as the current flagship.

*Cert relevance: this chapter frames the program — the current vs legacy tracks and mechanics the rest of the volume develops.*

## Teradata and its certifications

**Teradata** is the pioneer and long-standing leader of the **enterprise data warehouse** — the platform built to run **analytics on huge volumes of data** with speed and reliability, using **MPP (massively parallel processing)**, [Ch 3](03-the-mpp-architecture.md). For decades, the world's largest banks, retailers, airlines, and telecoms have run their most demanding analytics on Teradata. Today Teradata is **cloud** — its platform is **Teradata Vantage / VantageCloud** ([Ch 2](02-vantage-and-vantagecloud.md)), a connected, multi-cloud data platform — while retaining the deep, scalable analytics engine that made it the standard for large-scale data warehousing.

**Teradata Vantage Certifications** validate skill with the platform — its architecture, SQL, database design, administration, and analytics. Teradata sits alongside the cloud data platforms this shelf covers ([Snowflake XLIX](../../volume-049-snowflake-certifications/README.md), [Databricks XLVIII](../../volume-048-databricks-certifications/README.md), [Cloudera CLVIII](../../volume-158-cloudera-certifications/README.md)) — its distinctive angle is a **shared-nothing MPP architecture** and decades of data-warehouse depth. The lab builds the program map.

## Current versus legacy tracks

The Teradata certification program is **in transition**, which you must understand to choose the right exam:

- **VantageCloud Lake track (current)** — the modern, cloud-focused certifications. The flagship is the **Associate VantageCloud Lake 2.0** exam (plus an earlier VantageCloud Lake Associate and a Japanese version). This is where **new certification** is directed, reflecting Teradata's cloud/lakehouse direction.
- **Vantage 2 track (legacy, winding down)** — the older certifications: **Associate 2.4/2.3**, **Data Engineering**, **Administration**, and role-based exams (**Analytics, Data Science, Architecture**) that **retired 31 July 2024**; the Associate 2.4 had its last delivery around mid-2025.

So the practical guidance is: **target the VantageCloud Lake Associate** as the current entry credential, and treat the Vantage 2 role-based exams as legacy (many already retired). Always **check the certification site** for the current lineup, because it is actively evolving. The lab maps current versus legacy.

## Exam mechanics

Teradata certifications share a consistent, accessible shape:

- **Delivery** — through **Pearson VUE** (test center or online proctoring).
- **Digital badges** — credentials are issued as **verifiable digital badges** (Credly).
- **No eligibility requirements** — you can take an exam without prerequisites.
- **No expiration** — notably, Teradata certifications **do not expire** (unlike many vendors' 2–3-year validity), so a credential remains valid — though the platform evolves, so staying current matters.
- **Cost/format** — the **Associate VantageCloud Lake 2.0** is **$149** for **75 minutes**; a 25% discount promotion has been offered. Over **74,000** Teradata certifications have been awarded.

The **no-expiration, no-prerequisite** model lowers barriers; the Associate is the accessible entry point. The lab records the mechanics.

## The Associate as the entry point

The **Associate VantageCloud Lake** certification is the **foundation** of the current program — it validates core knowledge of the Teradata platform (Vantage/VantageCloud), its architecture, and SQL, at a level suitable for anyone starting with Teradata: analysts, developers, administrators, and data engineers. From this foundation, deeper and role-based skills build (many of the former role-based exams are being refreshed under the VantageCloud direction). Because it has **no prerequisites** and is a single accessible exam, the Associate is the natural first target and the anchor of this volume. The lab confirms the entry path. *(A single accessible foundational credential mirrors the Associate-first pattern across many cloud-platform certification programs.)*

## Hands-On Lab

Python models the program: current/legacy tracks, mechanics, and the entry path. **Cost:** none.

### Lab 1.1 — Map the current and legacy tracks

**Objective:** Record the VantageCloud Lake (current) and Vantage 2 (legacy) tracks.

```bash
python3 - <<'EOF'
TRACKS = {
  "VantageCloud Lake (CURRENT)": {
    "certs": ["Associate VantageCloud Lake 2.0 (flagship, $149/75min)", "Associate VantageCloud Lake"],
    "status": "where new certification is directed (cloud/lakehouse)",
  },
  "Vantage 2 (LEGACY, winding down)": {
    "certs": ["Associate 2.4/2.3", "Data Engineering", "Administration",
              "Analytics / Data Science / Architecture (RETIRED 31 Jul 2024)"],
    "status": "older track; role-based exams retiring",
  },
}
print("TERADATA VANTAGE CERTIFICATIONS — current vs legacy:\n")
for track, d in TRACKS.items():
    print(f"   {track}  [{d['status']}]")
    for c in d["certs"]: print(f"      - {c}")
    print()
print("Guidance: target the VantageCloud Lake ASSOCIATE (current entry); treat Vantage 2")
print("role-based exams as legacy (many already retired). Check the cert site — it's evolving.")
EOF
```

**Expected result:** A map of the current VantageCloud Lake track (Associate 2.0 flagship) versus the legacy Vantage 2 track (with the Analytics/Data Science/Architecture exams retired in July 2024). The lesson is that Teradata's program is transitioning to a cloud/lakehouse focus: target the VantageCloud Lake Associate as the current entry credential, and treat the older role-based Vantage 2 exams as legacy.

**Cleanup:** None.

### Lab 1.2 — Record the mechanics and entry path

**Objective:** Capture the delivery, badges, no-expiration model, and the Associate entry.

```bash
python3 - <<'EOF'
MECHANICS = {
  "delivery":     "Pearson VUE (test center or online proctored)",
  "badges":       "verifiable digital badges (Credly)",
  "eligibility":  "no prerequisites",
  "expiration":   "none — Teradata certifications do NOT expire",
  "flagship":     "Associate VantageCloud Lake 2.0 — $149, 75 minutes",
  "awarded":      "74,000+ Teradata certifications to date",
}
print("TERADATA EXAM MECHANICS:\n")
for k, v in MECHANICS.items():
    print(f"   {k:11}: {v}")
print()
print("The ASSOCIATE VantageCloud Lake is the accessible entry point: no prerequisites, a")
print("single exam, foundational platform + architecture + SQL knowledge. Credentials don't")
print("expire (rare), but the platform evolves, so staying current still matters. Start here.")
EOF
```

**Expected result:** A record of the mechanics — Pearson VUE delivery, digital badges, no prerequisites, no expiration, and the Associate VantageCloud Lake 2.0 flagship ($149, 75 minutes). The lesson is that Teradata certification is accessible (no prerequisites, no expiration) and the Associate VantageCloud Lake is the foundational entry point validating platform, architecture, and SQL knowledge.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Teradata placed — the MPP enterprise data-warehouse leader, now cloud (Vantage/VantageCloud).
- [ ] Current vs legacy understood — VantageCloud Lake (current) vs Vantage 2 (legacy, role-based exams retiring).
- [ ] The exam mechanics recorded — Pearson VUE, digital badges, no prerequisites, no expiration.
- [ ] The Associate entry point understood — Associate VantageCloud Lake 2.0 ($149, 75 min), the foundation.

## See also

- [Volume XLIX — Snowflake](../../volume-049-snowflake-certifications/README.md), [Volume XLVIII — Databricks](../../volume-048-databricks-certifications/README.md), and [Volume CLVIII — Cloudera](../../volume-158-cloudera-certifications/README.md) — cloud data-platform peers.
- [Chapter 02 — Teradata Vantage and VantageCloud](02-vantage-and-vantagecloud.md).
