# Chapter 01: The Arista Certification Program

## Learning Objectives

- Describe Arista, EOS, and CloudVision.
- Identify the ACE learning tracks and certification tiers.
- Explain delivery, prerequisites, and recertification.
- Access EOS via CLI and eAPI for this volume.
- Verify program facts from the authoritative source.

## Theory and Architecture

**Arista Networks** builds high-performance data-center and campus networking, unified by
**EOS (Extensible Operating System)** — a Linux-based, single-image network OS with a
publish/subscribe state database (**SysDB**), programmability (**eAPI** JSON-RPC, Linux
shell, Python), and **CloudVision (CVP)** for fleet-wide telemetry, provisioning, and
change control. **Arista Academy** runs the **Arista Certified Engineer (ACE)** program,
which validates these skills.

This is a **certification-tracks** volume: it maps the program — which credentials exist,
their topic areas, and levels — and teaches each with a hands-on walkthrough. The program
was **revised on 1 June 2025** into a **Learning Track** model with a tiered system —
**Associate (Level 1) → Specialist (Level 3) → Professional (Level 4)** — across tracks:

- **Network Foundations** (Associate).
- **Data Center** (Specialist: DC Operations, DC Engineering).
- **Campus** (Specialist: Campus Operations, Campus Engineering).
- **WAN Routing** (Specialist: MPLS Core).
- **Automation** (Foundations + Advanced → Professional for Automation).

Every credential was **verified against training.arista.com on 27 July 2026**. A **new
recertification policy** also took effect 1 June 2025.

## Design Considerations

Start with **Network Foundations (Associate)**, then pursue a **Specialist** track (Data
Center, Campus, or WAN Routing) by operations or engineering focus, and the **Automation**
track toward the **Professional** accreditation. Practice on free **cEOS/vEOS** images
(containerlab) or **Arista Test Drive**.

## Implementation and Automation

Labs use the **EOS CLI**, **eAPI** (JSON-RPC), and **CloudVision** / automation tooling.
Confirm eAPI access:

```bash
curl -sS -k -u admin:admin https://<switch>/command-api \
  -d '{"jsonrpc":"2.0","method":"runCmds","params":{"version":1,"cmds":["show version"],"format":"json"},"id":1}'
```

## Validation and Troubleshooting

Confirm the program facts:

```text
training.arista.com (revised 1 Jun 2025):
  - tiers: Associate (L1) -> Specialist (L3) -> Professional (L4)
  - tracks: Network Foundations, Data Center, Campus, WAN Routing, Automation
  - built on EOS + CloudVision; blueprints published; recert policy 1 Jun 2025
```

Common pitfalls: studying the **pre-2025** ACE structure (it was revised); and confusing
**Operations** vs **Engineering** specializations within a track.

## Security and Best Practices

Study the current **track blueprints**, practice on **cEOS/vEOS**, treat EOS/eAPI/CloudVision
access as privileged (RBAC, TACACS+/RADIUS, API over TLS), and progress **Associate →
Specialist → Professional**. Recertify per the 2025 policy.

## References and Knowledge Checks

- training.arista.com and arista.com: the ACE program, track blueprints, and EOS/CloudVision docs.

**Knowledge checks**

1. What is EOS and what makes it extensible?
2. Name the ACE tiers and the learning tracks.
3. What does CloudVision provide?

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with
`curl`; a cEOS/vEOS switch (containerlab) with eAPI enabled for the API checks. **Cost:**
none (free images).

### Lab 1.1 — Enumerate the tracks and tiers

**Objective:** State the program structure.

```bash
python3 - <<'PY'
tracks={"Network Foundations":"Associate (L1)","Data Center":"Specialist (Ops/Eng)",
        "Campus":"Specialist (Ops/Eng)","WAN Routing":"Specialist (MPLS Core)",
        "Automation":"Foundations+Advanced -> Professional"}
for t,l in tracks.items(): print(f"{t:20}: {l}")
PY
```

**Expected result:** the tracks mapped to tiers — the ACE program map.

**Negative test:** rely on the pre-2025 ACE levels; the program was **revised 1 Jun 2025**
— confirm on training.arista.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Query EOS via eAPI

**Objective:** Confirm eAPI access with `show version`.

```bash
curl -sS -k -u admin:admin https://<switch>/command-api \
  -d '{"jsonrpc":"2.0","method":"runCmds","params":{"version":1,"cmds":["show version"],"format":"json"},"id":1}' \
  | python3 -c "import sys,json;print('EOS version:',json.load(sys.stdin)['result'][0].get('version','?'))"
```

**Expected result:** the **EOS version** in JSON — proof eAPI works (the basis for later
labs).

**Negative test:** call `/command-api` without eAPI enabled; enable it (`management api
http-commands`) first.

**Rollback:** none (read-only).

### Lab 1.3 — Confirm the management surfaces

**Objective:** State how EOS is managed/automated.

```text
# EOS surfaces: CLI (industry-standard), eAPI (JSON-RPC), bash/Linux shell, Python;
#   CloudVision (CVP) for fleet telemetry/provisioning/change control.
"surfaces: CLI, eAPI, Linux shell, Python; CloudVision for the fleet"
```

**Expected result:** the correct EOS/CloudVision management surfaces — where you operate
and automate Arista.

**Negative test:** assume CLI-only; **eAPI/Python/CloudVision** enable automation — use
them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Arista Certified Engineer program (revised June 2025) validates EOS and CloudVision
skills across a tiered Learning Track model — Associate → Specialist → Professional —
spanning Network Foundations, Data Center, Campus, WAN Routing, and Automation. This
volume teaches each with EOS CLI, eAPI, and CloudVision work.

- [ ] I can describe EOS and CloudVision.
- [ ] I can name the ACE tracks and tiers.
- [ ] I can query EOS via eAPI.
- [ ] I can identify the management/automation surfaces.
- [ ] I completed Labs 1.1–1.3 including each negative test.
