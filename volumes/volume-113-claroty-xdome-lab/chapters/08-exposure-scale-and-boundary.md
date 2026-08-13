# Chapter 08: Exposure, Scale, and the Boundary

## Learning Objectives

- Understand how discovery feeds exposure/risk management, not just segmentation.
- Understand scaling passive collection across sites and the Purdue model.
- Recognize the limits of a passive, integration-enforced approach.

## Hands-On Lab

### Exercise 8.1 — Exposure management from the same discovery (design + model)

**Objective.** See how the asset inventory drives risk prioritization.

**Track 1 — Walkthrough (design).** The passively-built inventory carries vendor, model, and firmware, which xDome maps to known vulnerabilities and exposures — so the same discovery that produced the segmentation baseline also produces a prioritized risk list, and segmentation can be tightened around the riskiest assets first.

**Track 2 — Walkthrough (model).** Tag an asset with a known-vulnerable firmware and prioritize it:

```bash
sudo tee /etc/xdome/assets > /dev/null <<'EOF'
10.70.4.40 plc  vendor=acme  firmware=1.2  cve=CVE-2023-0001  criticality=high
10.70.2.20 db   vendor=pg    firmware=15   cve=none          criticality=medium
EOF
awk '$5!="cve=none"{print "PRIORITIZE segmentation around " $1 " (" $5 ")"}' /etc/xdome/assets
```

**Expected result.** `PRIORITIZE segmentation around 10.70.4.40 (cve=CVE-2023-0001)` — the vulnerable PLC is the first asset to wrap tightly, because discovery told you it is both critical and exposed.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.2 — Scale: collectors, sites, and the Purdue model (design)

**Objective.** Understand multi-site passive collection.

**Design walkthrough.** Collectors are placed per site/cell (often at each Purdue level boundary) and feed one xDome tenant; zones map naturally to Purdue levels (L0–L1 devices, L2 supervisory, L3 site operations), and the derived policies enforce the **Purdue segmentation** every OT reference architecture calls for. Adding a site is adding a collector and enforcer integration, not re-architecting.

**Expected result (on paper).** A design note: collectors per cell, zones per Purdue level, policy pushed to the firewalls/NAC at each boundary, one tenant for estate-wide visibility.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify what a passive, integration-enforced model cannot do alone.

**Track 1 & 2 — Walkthrough.** Claroty's strengths — passive discovery and baselining — come with limits:

- **It does not enforce by itself.** Segmentation is only as good as the integrated firewall/NAC; without an enforcer, xDome detects but cannot block.
- **A collector only sees what is mirrored to it.** Traffic on an unmonitored path is invisible; SPAN coverage must be complete.
- **Same-subnet east-west** needs a distributed enforcer (a switch ACL/NAC or a host firewall) — a central firewall integration cannot filter intra-VLAN peers.
- **Deep protocol control** (which Modbus function codes are allowed) needs an OT-protocol IPS.

```bash
echo "xDome sees and decides; an enforcer blocks. No enforcer, no enforcement."
```

**Expected result.** A boundary note: pair xDome's visibility with a real enforcer (firewall/NAC/switch), complete SPAN coverage, an OT-protocol IPS for command-level control (TXOne volume), and host controls for same-subnet flows.

**Negative test.** Assume enabling xDome secures the plant. It secures nothing until an enforcer applies its policy — discovery and detection are necessary but not sufficient.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Discovery-driven exposure/risk prioritization understood.
- [ ] Multi-site collectors and Purdue-aligned zoning understood.
- [ ] The passive-only / needs-an-enforcer boundary recognized.
- [ ] Complementary controls identified.
