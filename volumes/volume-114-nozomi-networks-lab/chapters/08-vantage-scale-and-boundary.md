# Chapter 08: Vantage, Scale, and the Boundary

## Learning Objectives

- Understand how Vantage aggregates many Guardians and manages assertions at scale.
- Extend the idea to more protocols and process assertions.
- Recognize the limits of passive, protocol-aware detection and where enforcement must come from.

## Hands-On Lab

### Exercise 8.1 — Vantage aggregation and assertions (design)

**Objective.** Understand fleet-scale management.

**Design walkthrough.** **Vantage** aggregates many Guardian sensors across sites into one console: assets, network graphs, process baselines, and alerts roll up centrally, and **assertions** (custom rules — "no writes to this PLC from that VLAN", "this variable must stay in range") are authored once and applied fleet-wide. Enforcement of the protocol-aware policy is delegated to integrated OT firewalls/IPS, the same split you built on Track 2.

**Expected result (on paper).** A design note: Guardians per site feeding one Vantage; assertions authored centrally; enforcement pushed to OT-aware firewalls/IPS at the cell boundaries.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.2 — More protocols, more assertions (model)

**Objective.** See the model generalize beyond Modbus.

**Track 2 — Walkthrough.** The same function-aware pattern applies to other OT protocols by parsing their command fields. Record additional assertions the enforcer would apply:

```bash
sudo tee -a /etc/nozomi/baseline > /dev/null <<'EOF'
protocol=dnp3 allowed=read deny=operate
protocol=s7   allowed=read deny=write,stop,program
assertion=no_write_from_it_vlan
EOF
tail -3 /etc/nozomi/baseline
```

**Expected result.** A short set of protocol-aware assertions — read-allowed, control-operations-denied — showing the model is protocol-general: parse the command, permit safe functions, deny control functions from the wrong source.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify what passive, protocol-aware detection cannot do alone.

**Track 1 & 2 — Walkthrough.** Nozomi's depth has limits:

- **It is passive; it must integrate to enforce.** Guardian sees and alerts; blocking a write needs an OT-aware firewall/IPS in the path (the proxy stood in for one here).
- **Encrypted OT protocols** hide the function code from a passive sensor; enforcement then needs a terminating proxy or endpoint agent (Arc).
- **A sensor only sees mirrored traffic.** Unmonitored links are blind spots.
- **Deep parsing must match the exact protocol/version** — an unknown or proprietary protocol may not be dissected.

```bash
echo "Guardian sees and asserts; an OT-aware enforcer blocks. No enforcer, detection only."
```

**Expected result.** A boundary note: pair Nozomi's protocol/process depth with an in-path OT-aware enforcer (an inline OT IPS such as the TXOne volume), endpoint sensors (Arc) for encrypted or host-level visibility, and complete SPAN coverage.

**Negative test.** Assume deploying Guardian secures the process. It detects superbly but blocks nothing itself — without an enforcer, the unauthorized write is alerted, not prevented.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Vantage fleet aggregation and central assertions understood.
- [ ] The function-aware pattern generalized to other OT protocols.
- [ ] The passive/needs-enforcer and encrypted-protocol boundaries recognized.
- [ ] Complementary controls (inline OT IPS, endpoint sensors) identified.
