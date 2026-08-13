# Chapter 05: Network Security (IPS) and Advanced Threat Defense

## Learning Objectives

- Explain Trellix Network Security (IPS) and its FireEye heritage.
- Configure IPS policy and signatures.
- Describe Advanced Threat Defense (ATD) sandboxing.
- Integrate network detections with the wider platform.
- Complete a walkthrough for each network-security topic (defensive).

## Theory and Architecture

The **Network Security** track defends the wire. Trellix **Network Security (IPS)** — combining the
McAfee NSP and FireEye NX heritage — inspects network traffic inline to **detect and block**
exploits, malware, and command-and-control using **signatures**, protocol anomaly detection, and
behavioral analysis, managed by a **Manager** appliance/console with **Sensors** in the traffic
path. **Advanced Threat Defense (ATD)** adds **sandboxing** — detonating suspicious files in an
isolated analysis environment to produce a verdict on unknown/zero-day malware, and sharing that
verdict (via **DXL**) so endpoints and the network can block it everywhere. Together they provide
**network-based** detection that complements endpoint (ENS/EDR): IPS stops known and anomalous
traffic inline; ATD verdicts unknown files; and the platform **shares intelligence** so a detection
in one place protects the whole estate. All **defensive**.

## Design Considerations

Place **Sensors** at trust boundaries (perimeter, data-center edge, segments) inline for blocking or
on a tap for detection. Tune **IPS policy** to your environment (enable relevant signature sets,
tune false positives). Use **ATD** for unknown-file verdicts and **share** them via DXL. Correlate
network detections with endpoint in Helix/XDR.

## Implementation and Automation

The labs reason about IPS policy/signatures, ATD sandbox verdicts, and intelligence sharing — all
**defensive**.

## Validation and Troubleshooting

Confirm the network-security model:

```text
Network Security (IPS): Manager + Sensors inline/tap; signatures + anomaly + behavioral -> detect/block.
ATD: sandbox unknown files -> verdict -> share via DXL -> block everywhere.
Complements ENS/EDR (endpoint). Correlate in Helix/XDR. Defensive.
```

Common pitfalls: running IPS in **detect-only** at a perimeter that needs blocking; and not
**sharing ATD verdicts** so endpoints stay exposed.

## Security and Best Practices

Deploy Sensors **inline** where blocking is needed, tune **IPS policy** to reduce false positives,
sandbox unknowns with **ATD**, and **share verdicts via DXL** so one detection protects all.
Correlate network and endpoint. Authorized, defensive operation throughout.

## Hands-On Lab

Network-security walkthroughs (defensive). **Shared prerequisites for Labs 5.1–5.4** — a shell with
`python3`; concepts apply to a Trellix Network Security/ATD deployment in an **authorized** lab.
**Cost:** none.

### Lab 5.1 — IPS policy and signatures

**Objective:** Enable and tune detection for the environment.

```python
python3 - <<'PY'
policy={"signature_sets":["exploit","malware-c2","protocol-anomaly"],
        "mode":"inline-block at perimeter","tuning":"disable a signature only on proven false-positive path"}
for k,v in policy.items(): print(f"{k}: {v}")
PY
```

**Expected result:** an **IPS policy** with relevant signature sets, inline blocking, and scoped
tuning — network protection fit to the environment.

**Negative test:** enable every signature at max with no tuning; **false positives** flood the SOC —
tune to the environment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Sensor placement

**Objective:** Place sensors for detection vs blocking.

```python
python3 - <<'PY'
placements={"Perimeter":"inline (block inbound exploits/C2)","DC edge":"inline (protect servers)",
            "Internal span":"tap (detect lateral movement, no block)"}
for loc,mode in placements.items(): print(f"{loc:14}: {mode}")
PY
```

**Expected result:** sensor **placement/mode** per location — inline where blocking matters, tap
where visibility does.

**Negative test:** tap-only at the perimeter where you need to **block**; place inline for
enforcement.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — ATD sandbox verdict

**Objective:** Verdict an unknown file and share it.

```python
python3 - <<'PY'
def atd(file_static_clean, dynamic_malicious_behaviors):
    verdict = "malicious" if dynamic_malicious_behaviors>0 else "clean"
    return verdict, "share via DXL -> ENS/EDR/IPS block everywhere" if verdict=="malicious" else "no action"
v,action = atd(True, 3)
print("ATD verdict:", v, "->", action)
PY
```

**Expected result:** an unknown file **detonated**, ruled **malicious** by behavior, and its verdict
**shared** to block estate-wide — zero-day defense.

**Negative test:** trust a file because it's **statically** clean; **dynamic sandboxing** catches
behavior static analysis misses — detonate it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — Intelligence sharing

**Objective:** Propagate a detection across the platform.

```text
# A network/ATD detection publishes an indicator on DXL -> ENS blocks the hash, EDR hunts for it,
#   ePO tags exposed systems. One detection -> estate-wide protection.
"share: network/ATD verdict -> DXL -> endpoint + network block + hunt (defense in depth)"
```

**Expected result:** a detection **propagated** across endpoint and network via DXL — unified
defense.

**Negative test:** keep a network detection siloed; **share it** so endpoints block the same threat.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Trellix Network Security (IPS, from McAfee NSP + FireEye NX) detects and blocks on the wire with
signatures and behavioral analysis, and Advanced Threat Defense sandboxes unknown files for
verdicts shared via DXL. Place sensors by need, tune IPS, sandbox unknowns, and share intelligence
across endpoint and network. Defensive throughout.

- [ ] I can configure and tune an IPS policy.
- [ ] I can place sensors for detection vs blocking.
- [ ] I can explain ATD sandbox verdicts.
- [ ] I can propagate a detection via DXL.
- [ ] I completed Labs 5.1–5.4 including each negative test.
