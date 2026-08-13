# Chapter 01: The MikroTik Certification Program

## Learning Objectives

- Explain the MikroTik certification program built on RouterOS.
- Identify MTCNA as the prerequisite for all other certificates.
- Map the specialist certificates (MTCRE, MTCTCE, MTCWE, MTCUME, MTCINE, and more) to their focus.
- Describe RouterOS (v6 and v7), the CLI, WinBox, and the API.
- Verify current program facts from the authoritative source.

## Theory and Architecture

MikroTik's certification program certifies engineers who deploy **RouterOS** — MikroTik's routing,
switching, wireless, and security operating system that runs on **RouterBOARD** hardware, the
**CHR** (Cloud Hosted Router) virtual machine, and x86. The program is a **hub-and-spoke** of
certificates. **MTCNA** (MikroTik Certified Network Associate) is the **foundation and the
prerequisite for every other certificate** — it covers RouterOS basics: configuration, addressing,
DHCP, NAT, basic firewall, wireless basics, bridging, and troubleshooting. From MTCNA, specialist
certificates branch by domain: **MTCRE** (Routing), **MTCTCE** (Traffic Control), **MTCWE/MTCEWE**
(Wireless), **MTCUME** (User Management), **MTCSE** (Security), **MTCSWE** (Switching), **MTCIPv6E**
(IPv6), and **MTCINE** (Inter-networking — BGP/MPLS, which additionally requires MTCRE).

Training is delivered by **MikroTik Certified Trainers** (instructor-led and online), with the
**exam taken online** at mikrotik.com after the course; certificates are **valid three years**.
RouterOS is managed by **CLI**, the **WinBox** and WebFig GUIs, and a **REST API** (RouterOS v7);
**v7** is the current major version, with syntax changes from v6 (notably routing). This volume
teaches each certificate track with hands-on RouterOS walkthroughs.

## Design Considerations

Earn **MTCNA first** — it gates everything else — then add the specialist certificates your role
needs (MTCRE→MTCINE for ISP/BGP, MTCTCE for firewall/QoS, MTCWE for wireless). Practice on **CHR**
(free) or RouterBOARD. Use **RouterOS v7** for new work and note its changed routing syntax.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://mikrotik.com/training/about" \
  | grep -oiE 'MTC[A-Z0-9]+|RouterOS|MTCNA' | sort -u
```

## Validation and Troubleshooting

The verified program facts (mikrotik.com, 28 July 2026):

```text
MTCNA = prerequisite for ALL other certificates. MTCINE additionally requires MTCRE.
Tracks: MTCRE (routing), MTCTCE (traffic control), MTCWE/MTCEWE (wireless), MTCUME (user mgmt),
        MTCINE (BGP/MPLS), MTCSE (security), MTCSWE (switching), MTCIPv6E (IPv6).
Platform: RouterOS v6/v7 on RouterBOARD/CHR/x86; CLI + WinBox/WebFig + REST API (v7).
Delivery: MikroTik Certified Trainers + online exam. Validity: 3 years.
```

Common pitfalls: attempting a specialist exam **without MTCNA**; and using **v6 routing syntax**
on RouterOS v7 (it changed).

## Security and Best Practices

Start with **MTCNA**, practice on **CHR** in a lab, and verify certificates on mikrotik.com —
third-party dumps are neither authoritative nor permitted. Secure RouterOS management (strong
passwords, restrict WinBox/API services, firewall the router itself).

## References and Knowledge Checks

- mikrotik.com/training: the certificate program, schedule, and trainers.
- MikroTik documentation (help.mikrotik.com): RouterOS v7, CLI, and the REST API.

**Knowledge checks**

1. Which certificate is the prerequisite for all others?
2. Which certificate additionally requires MTCRE?
3. What is the certificate validity period?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the program structure

**Objective:** Read the certificates from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://mikrotik.com/training/about" \
  | grep -oiE 'MTC[A-Z0-9]+|RouterOS' | sort -u
```

**Expected result:** the MTC* certificates and RouterOS — the program map.

**Negative test:** assume any exam can be taken first; **MTCNA is the prerequisite** — confirm on
mikrotik.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map certificates to focus

**Objective:** Record the certificate tracks.

```python
python3 - <<'PY'
certs={"MTCNA":"RouterOS basics (prereq for all)","MTCRE":"routing (static/OSPF/tunnels)",
       "MTCTCE":"firewall/NAT/QoS/proxy","MTCWE":"wireless/CAPsMAN","MTCUME":"PPP/hotspot/RADIUS",
       "MTCINE":"BGP/MPLS/VPLS (needs MTCRE)","MTCSE":"security/IPsec","MTCSWE":"switching/VLANs",
       "MTCIPv6E":"IPv6"}
for c,f in certs.items(): print(f"{c:9}: {f}")
PY
```

**Expected result:** a certificate → focus map — your study reference.

**Negative test:** target MTCINE directly; it needs **MTCNA and MTCRE** first — sequence them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a certificate path

**Objective:** Sequence certificates for a role.

```python
python3 - <<'PY'
paths={"ISP engineer":"MTCNA -> MTCRE -> MTCINE (BGP/MPLS)",
       "Firewall/QoS":"MTCNA -> MTCTCE","Wireless":"MTCNA -> MTCWE/MTCEWE",
       "ISP user services":"MTCNA -> MTCUME (hotspot/RADIUS)"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences — the tracks this volume follows.

**Negative test:** skip MTCNA for a specialist track; **MTCNA gates all** — earn it first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MikroTik's program certifies RouterOS engineers, with MTCNA as the prerequisite foundation and
specialist certificates (MTCRE, MTCTCE, MTCWE, MTCUME, MTCINE, MTCSE, MTCSWE, MTCIPv6E) branching
by domain. Training is trainer-led with an online exam and three-year validity. Earn MTCNA first,
practice on CHR, and use RouterOS v7.

- [ ] I can explain the MTCNA-first structure.
- [ ] I can map certificates to their focus.
- [ ] I can identify MTCINE's MTCRE prerequisite.
- [ ] I can plan a certificate path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
