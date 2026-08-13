# Chapter 01: The Nokia Service Routing Certification Program

## Learning Objectives

- Explain the Nokia Service Routing Certification (SRC) program and its levels.
- Map the credentials (NRS I, NRS II, SRA) to their exams.
- Describe the SR OS platform and the classic and MD-CLI interfaces.
- Understand the written-plus-practical-lab structure of NRS II.
- Verify current program facts from the authoritative source.

## Theory and Architecture

The **Nokia Service Routing Certification (SRC)** program certifies engineers who design and
operate IP/MPLS service-provider networks on Nokia's **SR OS** (Service Router Operating System),
which runs the **7750 SR**, **7450 ESS**, and **7950 XRS** platforms. The program has three
levels. **Network Routing Specialist I (NRS I)** is the entry credential — a single exam,
**4A0-100** ("Nokia IP Networks and Services Fundamentals") covering the TCP/IP model, IPv4
addressing, Ethernet, packet forwarding, routing protocols, MPLS tunneling, and VPN-services
fundamentals. **Network Routing Specialist II (NRS II)** is the professional credential, earned by
**two** components: a **Composite Written** exam (**4A0-C03**, IS-IS variant, or **4A0-C04**, OSPF
variant) delivered at Pearson VUE, and a separate **3.5-hour practical lab** (**4A0-N01**) — so
NRS II proves both knowledge and hands-on skill across OSPF/IS-IS, BGP, MPLS, and services.
**Service Routing Architect (SRA)** is the expert design credential (**4A0-112**), requiring NRS
II, focused on end-to-end solution design.

SR OS offers two management interfaces: the **classic CLI** and the newer **MD-CLI** (model-driven
CLI, aligned to YANG models and the same data model exposed via NETCONF/gRPC). This volume teaches
each level with hands-on SR OS walkthroughs, one lab per exam domain.

## Design Considerations

Climb the levels in order: **NRS I** for fundamentals, **NRS II** (written + lab) for professional
routing and services, **SRA** for design. Because NRS II includes a **practical lab**, study on
real or virtual SR OS, not just theory. Prefer the **MD-CLI** for new work (it maps to the
automation model) while knowing the classic CLI.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nokia.com/networks/training/src/exams/" \
  | grep -oiE '4A0-[0-9CN]+|NRS|Service Routing Architect|Fundamentals' | sort -u
```

## Validation and Troubleshooting

The verified program facts (nokia.com SRC pages, 28 July 2026):

```text
NRS I: exam 4A0-100 (IP Networks and Services Fundamentals), 40 Q / 90 min / $125.
NRS II: Composite Written 4A0-C03 (IS-IS) or 4A0-C04 (OSPF), 60 Q / 90 min / 70% + Practical Lab 4A0-N01 (3.5 h).
SRA: exam 4A0-112 (requires NRS II).
Platform: SR OS (7750 SR / 7450 ESS / 7950 XRS); classic CLI + MD-CLI. Delivery: Pearson VUE + lab.
```

Common pitfalls: treating **NRS II** as written-only (it also has a **practical lab**); and mixing
up the **IS-IS (4A0-C03)** and **OSPF (4A0-C04)** composite variants.

## Security and Best Practices

Match the NRS II composite **variant** (IS-IS or OSPF) to your network, practice on **SR OS VSR**
in a lab, and verify exams on nokia.com — third-party dumps are neither authoritative nor
permitted. Secure SR OS management (AAA, SSH, MD-CLI over NETCONF/TLS).

## References and Knowledge Checks

- nokia.com/networks/training/src: the SRC program, exams, and courses.
- Nokia SR OS documentation: the platform, classic CLI, and MD-CLI.

**Knowledge checks**

1. Name the three SRC levels and their exams.
2. What two components make up NRS II?
3. What are the two NRS II composite-written variants?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the SRC levels

**Objective:** Read the program structure from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nokia.com/networks/training/src/exams/" \
  | grep -oiE '4A0-[0-9CN]+|NRS I|NRS II|Service Routing Architect' | sort -u
```

**Expected result:** the NRS I/II and SRA credentials with their 4A0 exam codes — the program map.

**Negative test:** assume NRS II is a single written exam; it also requires the **4A0-N01 lab** —
confirm on nokia.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map credentials to exams

**Objective:** Record the verified exam structure.

```python
python3 - <<'PY'
program={
 "NRS I":["4A0-100 (IP Networks & Services Fundamentals)"],
 "NRS II":["4A0-C03 (IS-IS) or 4A0-C04 (OSPF) composite written","4A0-N01 (3.5h practical lab)"],
 "SRA":["4A0-112 (requires NRS II)"],
}
for cred,exams in program.items():
    print(f"{cred}:")
    for e in exams: print("  -",e)
PY
```

**Expected result:** a credential → exam map — your scheduling reference.

**Negative test:** book only the composite written for NRS II; you also need the **practical lab**
— schedule both.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"SP routing engineer":"NRS I -> NRS II (written + lab)",
       "Network architect":"NRS I -> NRS II -> SRA (4A0-112)",
       "IS-IS network":"NRS II via 4A0-C03 (IS-IS variant)",
       "OSPF network":"NRS II via 4A0-C04 (OSPF variant)"}
for role,path in paths.items(): print(f"{role:22}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** target SRA without NRS II; **NRS II is the prerequisite** — earn it first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Nokia SRC program certifies SR OS service-provider routing across NRS I (4A0-100), NRS II
(composite written 4A0-C03/C04 plus the 4A0-N01 practical lab), and SRA (4A0-112). Climb in order,
practice on SR OS for the lab, and verify the current exams on nokia.com.

- [ ] I can name the three levels and their exams.
- [ ] I can explain the NRS II written-plus-lab structure.
- [ ] I can choose the IS-IS or OSPF composite variant.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
