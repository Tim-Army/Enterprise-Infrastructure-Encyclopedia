# Chapter 09: Keeping the Arista Program Current and Career Paths

## Learning Objectives

- Explain Arista certification validity and recertification.
- Track program change since the June 2025 revision.
- Plan an ACE certification path by role.
- Relate Arista credentials to the encyclopedia's network volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

The Arista Certified Engineer program was **revised on 1 June 2025** into the Learning
Track model with a new **recertification policy**. Certifications track the platform (EOS
and CloudVision) and expand by **track** (Network Foundations, Data Center, Campus, WAN
Routing, Automation) and **tier** (Associate → Specialist → Professional). Because the
program is recent, confirm the current tracks, blueprints, and recert terms on
training.arista.com before you study.

## Design Considerations

Plan by **role**: everyone starts with **Network Foundations (Associate)**; data-center
engineers take the **Data Center** Specialist track, campus teams the **Campus** track,
service-provider/WAN engineers the **WAN Routing** track, and automation engineers the
**Automation** track toward **Professional**. Recertify per the 2025 policy.

## Implementation and Automation

Verify currency from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.training.arista.com/learning-pathways" \
  | grep -oiE 'Foundations|Data Center|Campus|WAN Routing|Automation|Associate|Specialist|Professional' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
training.arista.com (revised 1 Jun 2025):
  - tiers: Associate (L1) -> Specialist (L3) -> Professional (L4)
  - tracks: Network Foundations, Data Center, Campus, WAN Routing, Automation
  - blueprints published; recertification policy 1 Jun 2025
```

Common pitfalls: studying the **pre-2025** ACE structure; and mixing up **Operations** vs
**Engineering** specializations.

## Security and Best Practices

Study the current **track blueprints**, practice on **cEOS/vEOS** or Arista Test Drive, and
combine credentials for your role (e.g., Foundations → Data Center Eng, or → Automation
Professional). Recertify per the 2025 policy; track new tracks as they launch.

## References and Knowledge Checks

- training.arista.com and arista.com: the ACE program, track blueprints, and EOS/CloudVision docs.

**Knowledge checks**

1. When was the ACE program revised, and into what model?
2. Name the tiers and the learning tracks.
3. What path suits a data-center engineer?

## Hands-On Lab

Currency and career walkthroughs. **Shared prerequisites for Labs 9.1–9.2** — a shell with
`curl` and `python3`. **Cost:** none.

### Lab 9.1 — Verify the current tracks

**Objective:** Read the current learning tracks.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.training.arista.com/learning-pathways" \
  | grep -oiE 'Network Foundations|Data Center|Campus|WAN Routing|Automation' | sort -u
```

**Expected result:** the current tracks (**Network Foundations, Data Center, Campus, WAN
Routing, Automation**) — confirming scope.

**Negative test:** trust a pre-2025 cert list; the program was **revised** — confirm on
training.arista.com.

**Cleanup:** none.

### Lab 9.2 — Plan a path

**Objective:** Map a role to an ACE track sequence.

```bash
python3 - <<'PY'
paths={"Network generalist":"Network Foundations (Associate)",
       "Data Center Engineer":"Foundations -> Data Center Specialist (Eng)",
       "Campus Engineer":"Foundations -> Campus Specialist (Eng)",
       "SP/WAN":"Foundations -> WAN Routing (MPLS Core)",
       "Automation":"Foundations -> Automation (Found+Adv) -> Professional"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the career mapping this volume supports.

**Negative test:** attempt a Specialist track first; start with **Network Foundations
(Associate)** for the base.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Arista's ACE program (revised June 2025) is a tiered Learning Track model — Associate →
Specialist → Professional across Network Foundations, Data Center, Campus, WAN Routing, and
Automation — with a new recertification policy. Plan a path by role from Foundations upward
and verify the current tracks before you study.

- [ ] I can explain the June 2025 revision and recertification.
- [ ] I can name the tiers and tracks.
- [ ] I can plan a role-based ACE path.
- [ ] I can verify the current program on training.arista.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
