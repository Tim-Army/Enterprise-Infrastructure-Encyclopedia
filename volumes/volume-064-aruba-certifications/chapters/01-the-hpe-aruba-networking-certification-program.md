# Chapter 01: The HPE Aruba Networking Certification Program

## Learning Objectives

- Explain what the HPE Aruba Networking certification program certifies.
- Identify the tiers (Associate, Professional, Expert), the Network Architect design tier, and Advanced Product Certifications.
- Map the certification tracks (Campus Access, Switching, Network Security, Mobility, Data Center) to exam codes.
- Describe the platform the exams test: AOS-CX, Aruba Central, ClearPass, and gateways.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**HPE Aruba Networking** is HPE's enterprise networking business — campus and data-center
switching, wireless LAN, SD-WAN, and network security — and its certification program is the
successor to the "Aruba Certified" scheme, rebranded **HPE Aruba Networking Certified**. The
program is structured as **tiers** and **tracks**. The tiers are **Associate (ACA)**,
**Professional (ACP)**, and **Expert (ACX)**, with a separate **Network Architect** design tier
and a set of **Advanced Product Certifications (APC)** for specific products. The tracks are the
technology domains: **Campus Access**, **Switching**, **Network Security**, **Mobility (WLAN)**,
and **Data Center**. Exams are delivered by **Pearson VUE**.

The exams test HPE Aruba's platform: **AOS-CX** (the modern, programmable switch operating
system with a built-in REST API and database-driven architecture), **Aruba Central** (the
cloud management and AIOps plane), **ClearPass** (network access control and policy), and the
**gateways/AOS-10** that terminate WLAN and enforce policy. Because AOS-CX and Central are
API-first, the program spans CLI, REST, and automation (pyaoscx and Ansible).

## Design Considerations

Choose a **track** by role — campus, switching, security, wireless, or data center — and climb
the **tiers** within it. Everyone benefits from the **Associate** foundation before Professional
and Expert. Add **Advanced Product Certifications** (e.g., ClearPass, Central) for depth on a
specific product. Confirm the current codes before scheduling; HPE revises the program.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://certification-learning.hpe.com/tr/certifications/aruba" \
  | grep -oiE 'Associate|Professional|Expert|Campus Access|Switching|Network Security|Data Center|Mobility' \
  | sort -u
```

## Validation and Troubleshooting

The verified program facts (certification-learning.hpe.com and hpepress.hpe.com, 28 July 2026):

```text
Tiers : Associate (ACA) -> Professional (ACP) -> Expert (ACX); + Network Architect; + APC.
Tracks: Campus Access, Switching, Network Security, Mobility (WLAN), Data Center.
Codes : ACA Campus Access HPE6-A85; ACA Switching HPE6-A86; ACA Network Security HPE6-A78;
        ACP Campus Access HPE7-A01; ACP Switching HPE7-A08; ACP Data Center HPE7-A05;
        ACX Campus Access Switching HPE7-A06; ACX Campus Access Mobility HPE7-A07;
        ACX Network Security HPE7-A10; Network Architect Campus HPE7-A03 / Data Center HPE7-A04.
APC   : Comware, CX 10000, AOS-10, ClearPass, Central.
Deliver: Pearson VUE. Validity typically 3 years (confirm on the portal).
```

Common pitfalls: studying the **legacy "Aruba Certified"** names/codes (the program was
rebranded and renumbered); and mixing up **Campus Access** (solution) with **Switching**
(platform) tracks.

## Security and Best Practices

Match the track to your production platform (AOS-CX, Central, ClearPass) and practice on real
or virtual gear. Verify exam codes on **certification-learning.hpe.com** — third-party dump
sites are neither authoritative nor permitted study material.

## References and Knowledge Checks

- certification-learning.hpe.com and hpe.com/networkingtraining: the certification catalog, datasheets, and training.
- hpepress.hpe.com: official certification study guides (with exam codes).

**Knowledge checks**

1. Name the three tiers and the Network Architect and APC additions.
2. Name the certification tracks.
3. Which exam code is the Campus Access Associate?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the tiers and tracks

**Objective:** Read the program structure from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://certification-learning.hpe.com/tr/certifications/aruba" \
  | grep -oiE 'Associate|Professional|Expert|Campus Access|Switching|Network Security|Data Center|Mobility' \
  | sort -u
```

**Expected result:** the tiers (**Associate/Professional/Expert**) and tracks (**Campus Access,
Switching, Network Security, Data Center, Mobility**) — the program map.

**Negative test:** study a years-old "Aruba Certified" list; the program was **rebranded and
renumbered** — confirm on certification-learning.hpe.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map codes to tracks and tiers

**Objective:** Record the verified exam codes.

```python
python3 - <<'PY'
codes={
 ("Campus Access","Associate"):"HPE6-A85", ("Switching","Associate"):"HPE6-A86",
 ("Network Security","Associate"):"HPE6-A78", ("Campus Access","Professional"):"HPE7-A01",
 ("Switching","Professional"):"HPE7-A08", ("Data Center","Professional"):"HPE7-A05",
 ("Campus Access Switching","Expert"):"HPE7-A06", ("Campus Access Mobility","Expert"):"HPE7-A07",
 ("Network Security","Expert"):"HPE7-A10",
}
for (track,tier),code in codes.items(): print(f"{tier:12} {track:24} {code}")
PY
```

**Expected result:** a track/tier → code table — your scheduling reference.

**Negative test:** register for a legacy code (e.g., an old HPE6-A4x); confirm the **current**
code on the portal before booking Pearson VUE.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a track and tier path

**Objective:** Sequence certifications for a role.

```python
python3 - <<'PY'
paths={"Campus engineer":"ACA Campus Access -> ACP Campus Access -> ACX (Switching/Mobility)",
       "Switching specialist":"ACA Switching -> ACP Switching -> ACX Switching",
       "Security engineer":"ACA Network Security -> ACP Network Security -> ACX Network Security",
       "Architect":"Professional -> HPE Aruba Certified Network Architect (HPE7-A03/A04)"}
for role,path in paths.items(): print(f"{role:22}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** attempt an Expert exam first; start at the **Associate** foundation for the
track.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The HPE Aruba Networking program certifies its campus, switching, security, wireless, and
data-center platform (AOS-CX, Central, ClearPass, gateways) across Associate, Professional, and
Expert tiers, a Network Architect design tier, and Advanced Product Certifications, delivered by
Pearson VUE. Pick a track, climb the tiers, and verify codes on the portal.

- [ ] I can name the tiers, the Network Architect tier, and APC.
- [ ] I can name the certification tracks.
- [ ] I can map the Associate/Professional/Expert exam codes.
- [ ] I can plan a track-and-tier path for a role.
- [ ] I completed Labs 1.1–1.3 including each negative test.
