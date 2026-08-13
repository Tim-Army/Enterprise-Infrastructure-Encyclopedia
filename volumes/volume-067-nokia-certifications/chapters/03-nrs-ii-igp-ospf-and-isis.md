# Chapter 03: NRS II — IGP: OSPF and IS-IS

## Learning Objectives

- Explain the NRS II IGP scope and the OSPF/IS-IS composite variants.
- Configure OSPF on SR OS with areas.
- Configure IS-IS on SR OS with levels.
- Verify adjacencies and the link-state database.
- Complete a walkthrough for each IGP topic.

## Theory and Architecture

**NRS II** validates professional routing, and the **composite written** comes in two variants —
**4A0-C03 (IS-IS)** and **4A0-C04 (OSPF)** — reflecting the two interior gateway protocols a
Nokia SR OS network runs. **OSPF** is a link-state IGP organized into **areas** around a backbone
(area 0), flooding LSAs to build a synchronized link-state database and running SPF for shortest
paths. **IS-IS** is the link-state IGP favored in many large service-provider cores; it uses
**levels** (L1 intra-area, L2 backbone) instead of areas, runs directly over Layer 2, and is prized
for scalability and its clean support for **segment routing**. On SR OS both run under `configure
router`, enabled per interface, sourced from the **system** interface as router ID. The IGP
provides the internal reachability that BGP, MPLS, and services depend on.

## Design Considerations

Choose the IGP your network standardizes on (many SP cores use **IS-IS** for scale and SR
readiness). Keep the **backbone** clean (OSPF area 0 / IS-IS L2), summarize at boundaries, and
source the protocol from the **system** interface. Tune metrics deliberately; the IGP is the
foundation everything else rides on.

## Implementation and Automation

The labs configure OSPF and IS-IS, and verify adjacencies and the LSDB.

## Validation and Troubleshooting

Confirm the IGP model:

```text
OSPF: areas (backbone area 0), LSAs -> LSDB -> SPF. IS-IS: levels (L1/L2), runs over L2, SR-friendly.
Both under 'configure router', per-interface, router ID from system interface.
NRS II composite: 4A0-C03 (IS-IS variant) or 4A0-C04 (OSPF variant).
```

Common pitfalls: mismatched OSPF **area** or IS-IS **level** on a link (no adjacency); and sourcing
the router ID from an **unstable** interface.

## Security and Best Practices

Authenticate IGP adjacencies, keep the backbone clean, and source from the **system** interface.
Prefer **IS-IS** where segment routing and scale matter. Verify the **LSDB** is synchronized before
trusting paths.

## Hands-On Lab

IGP walkthroughs. **Shared prerequisites** — two SR OS nodes with a link and system interfaces, in
a lab. **Cost:** none.

### Lab 3.1 — Configure OSPF

**Objective:** Bring up an OSPF backbone adjacency.

```text
A:router>config# router ospf area 0.0.0.0 interface "system" no shutdown
A:router>config# router ospf area 0.0.0.0 interface "to-core" no shutdown
A:router# show router ospf neighbor
```

**Expected result:** an **OSPF** neighbor in **Full** state on the backbone — link-state
adjacency.

**Negative test:** put the two ends in **different areas**; the adjacency won't form across mixed
areas on a normal link — match the area.

**Rollback:** `configure router ospf shutdown`.

### Lab 3.2 — Verify the OSPF LSDB and routes

**Objective:** Confirm the database and SPF results.

```text
A:router# show router ospf database
A:router# show router route-table protocol ospf
```

**Expected result:** a synchronized **LSDB** and OSPF-learned routes — SPF working.

**Negative test:** trust reachability without checking the **LSDB**; verify it is synchronized.

**Rollback:** none (read-only).

### Lab 3.3 — Configure IS-IS

**Objective:** Bring up an IS-IS L2 adjacency.

```text
A:router>config# router isis interface "system" level-capability level-2
A:router>config# router isis interface "to-core" level-capability level-2
A:router>config# router isis area-id 49.0001
A:router# show router isis adjacency
```

**Expected result:** an **IS-IS** L2 adjacency **Up** — the SP-core IGP established.

**Negative test:** mismatch the **level** (L1 vs L2) across the link; align the level for the
adjacency.

**Rollback:** `configure router isis shutdown`.

### Lab 3.4 — Verify the IS-IS database

**Objective:** Confirm the IS-IS LSDB and routes.

```text
A:router# show router isis database
A:router# show router route-table protocol isis
```

**Expected result:** the **IS-IS LSDB** and learned routes — the core IGP converged.

**Negative test:** assume convergence without the **database**; check the LSDB is complete.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NRS II's IGP scope covers OSPF (areas) and IS-IS (levels), the two composite-written variants
(4A0-C04 OSPF, 4A0-C03 IS-IS). Configure each on SR OS, source from the system interface, keep the
backbone clean, and verify the synchronized link-state database.

- [ ] I can configure OSPF with areas.
- [ ] I can verify the OSPF LSDB and routes.
- [ ] I can configure IS-IS with levels.
- [ ] I can verify the IS-IS database.
- [ ] I completed Labs 3.1–3.4 including each negative test.
