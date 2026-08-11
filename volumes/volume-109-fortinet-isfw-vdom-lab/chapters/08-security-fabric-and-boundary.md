# Chapter 08: Security Fabric, Automation, and the Boundary

## Learning Objectives

- Understand how the Security Fabric and FortiManager scale this policy across many FortiGates — a design exercise.
- Use an automation stitch to contain a host reactively.
- Recognize what the ISFW cannot segment and pair it with a complementary control.

## Hands-On Lab

### Exercise 8.1 — Central management and the Security Fabric (design exercise)

**Objective.** Understand how the hand-authored policy scales to an estate.

**Design walkthrough.** Editing one FortiGate does not scale. **FortiManager** centralizes policy across many FortiGates with policy packages and templates; the **Security Fabric** links FortiGates (and FortiSwitch/FortiAP) so segmentation and telemetry span the estate, and an upstream FortiGate can see and act on downstream segments. In a production ISFW deployment:

```text
FortiManager  --(policy package)-->  every ISFW FortiGate
Security Fabric  --(shared objects, topology, telemetry)-->  fabric members
FortiAnalyzer  <--(logs)--  fabric members  (central visibility)
```

**Expected result (on paper).** A design note: author zone/VDOM policy once in FortiManager, template it across sites, and use the Security Fabric for estate-wide visibility and coordinated enforcement — the same mechanics you built by hand, automated.

**Negative test (reasoning).** Assume the Security Fabric segments by itself. It does not — the fabric shares objects and visibility; the *policies* (Chapter 05) and *VDOMs* (Chapter 07) are what enforce. The fabric scales and coordinates them.

**Cleanup.** None (design).

### Exercise 8.2 — Reactive containment with an automation stitch

**Objective.** Contain a compromised host automatically on a trigger.

**Track 1 — Walkthrough.** FortiOS **automation stitches** run an action when a trigger fires. Build a stitch that, on a compromised-host or IOC trigger, adds the host to a **quarantine** address group a policy denies:

```text
FGT # config firewall address
FGT (address) # edit quarantine
FGT (quarantine) # set type dynamic
FGT (quarantine) # end
FGT # config system automation-stitch
FGT (stitch) # edit contain-host
FGT (contain-host) # set trigger compromised-host
FGT (contain-host) # set action quarantine-fortigate
FGT (contain-host) # end
```

A top-of-list deny policy referencing `quarantine` then contains any member.

**Evaluation FortiGate.** Two eval realities change how you do this. First, the eval VM license **caps the firewall policy table** — you cannot add the dedicated top-of-list quarantine-deny policy (a fourth rule fails with `reached the maximum number of entries`). Second, `diagnose user quarantine` is not a command on FortiOS 8.0. Drive the same reactive containment through the **banned-IP list**, which the FortiGate enforces on transit traffic without consuming a policy — exactly what an `IP Ban` automation action does:

```text
FGT # diagnose user banned-ip add src4 10.30.3.10 600 administrative
FGT # diagnose user banned-ip list src4
    src-ip-addr   created   expires   cause
    10.30.3.10    ...       ...       DLP
FGT # diagnose user banned-ip delete src4 10.30.3.10
```

The host's permitted flows drop the instant it is banned and return when it clears (`hmi → plc:502` goes OPEN → CONTAINED → OPEN). The `cause` argument is a cosmetic enum — an arbitrary string is relabeled (here `administrative` displays as `DLP`).

**Expected result (concept).** When the trigger fires for a host, the stitch quarantines it and the standing deny drops its traffic — reactive containment without a manual rule edit, analogous to the dynamic address groups of Volume CVIII.

**Track 2 — Walkthrough.** Model the stitch with a dynamic set consulted first:

```bash
sudo nft add set inet fgt quarantine '{ type ipv4_addr ; flags dynamic ; }'
sudo nft insert rule inet fgt forward ip saddr @quarantine drop
sudo nft add element inet fgt quarantine '{ 10.30.3.10 }'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.30.4.10 502 && echo OPEN || echo CONTAINED'
sudo nft delete element inet fgt quarantine '{ 10.30.3.10 }'
```

**Expected result.** `CONTAINED` while the host is in the set; access returns after removal — reactive, reversible containment.

**Negative test.** Placing the quarantine deny below a permit lets a contained host keep an allowed flow; the reactive deny must be first.

**Cleanup.** Remove the test member.

### Exercise 8.3 — The boundary

**Objective.** Identify traffic the ISFW cannot see, and cover it.

**Track 1 & 2 — Walkthrough.** An ISFW segments what **transits** it. It does not help with:

- **Intra-zone / same-subnet east-west** — two hosts on the same segment behind the same switch port never reach the FortiGate. Separate them into zones/VLANs or add access-layer/host controls.
- **Traffic on links that bypass the ISFW** — anything not routed through it.
- **Encrypted payloads** without inspection.

```bash
sudo ip netns exec db bash -c 'nc -z -w2 10.30.2.11 5432 2>/dev/null || echo "intra-zone flow not seen by ISFW"'
```

**Expected result.** A boundary note: use VLAN/zone design and VDOMs to force sensitive flows through the ISFW, enforce at the access edge for intra-zone traffic, and pair with host-based microsegmentation (Volumes XCIII–CVI) where the firewall has no path.

**Negative test.** Assume one flat segment with an intra-zone deny suffices — same-subnet traffic never reaches the ISFW, so the deny never applies. Segmentation design decides what the firewall can enforce.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] FortiManager / Security Fabric scaling understood as automation of what you built.
- [ ] An automation stitch practiced for reactive containment.
- [ ] Intra-zone and bypassed traffic recognized as the boundary.
- [ ] The boundary paired with a complementary control.
