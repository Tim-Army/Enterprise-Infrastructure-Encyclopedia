# Chapter 03: VMDR — Asset Management and CSAM

## Learning Objectives

- Build a complete asset inventory with CSAM.
- Categorize and enrich assets (hardware, software, business context).
- Manage the external attack surface.
- Detect unauthorized and end-of-life software.
- Complete a walkthrough for each asset-management topic.

## Theory and Architecture

**VMDR (Vulnerability Management, Detection and Response)** is Qualys's flagship workflow, and it
starts where all security starts: **knowing your assets**. **CyberSecurity Asset Management (CSAM)**
builds a **complete, continuously-updated inventory** of every device, its **hardware and software**,
and its **business context** — enriched with data like end-of-life/end-of-support status, installed
software, and open ports. CSAM also includes **External Attack Surface Management (EASM)** —
discovering internet-facing assets the organization may not know it owns. The inventory is the
foundation: you can only assess and remediate what you can see, and **unauthorized software**,
**end-of-life systems**, and **unknown internet-facing assets** are common risk sources CSAM surfaces.
Assets are organized with **dynamic tags** (by OS, location, criticality, exposure) so every downstream
activity — scanning, prioritization, reporting — can be scoped by business context. This chapter
teaches each with a hands-on defensive walkthrough (inventory enrichment, attack-surface discovery,
and EOL/unauthorized-software detection).

## Design Considerations

Achieve **complete inventory** (agents + scanners + passive + connectors). Enrich with **business
context** and **EOL/EOS** data. Run **EASM** to find shadow internet assets. Flag **unauthorized** and
**end-of-life** software. Use **dynamic tags** for scoping. Treat inventory as the living foundation,
not a one-time export.

## Implementation and Automation

The labs enrich inventory, discover attack surface, and flag EOL/unauthorized software.

## Validation and Troubleshooting

Confirm the CSAM model:

```text
VMDR starts with CSAM: complete inventory (hardware/software/business context) + EOL/EOS enrichment + External Attack Surface Management (find unknown internet assets).
Surfaces unauthorized software + end-of-life systems. Dynamic tags scope everything downstream. Foundation: can't secure what you can't see.
```

Common pitfalls: an **incomplete inventory** (blind spots); and ignoring **EOL software** (unpatchable
risk).

## Security and Best Practices

Build a **complete, enriched** inventory, run **EASM**, flag **EOL/unauthorized** software, and scope
with **dynamic tags**. Keep the inventory continuously current. All work is defensive.

## Hands-On Lab

CSAM walkthroughs. **Shared prerequisites** — `python3`, in a lab. **Cost:** none.

### Lab 3.1 — Enrich an asset inventory

**Objective:** Add context to raw assets.

```python
python3 - <<'PY'
asset={"host":"fin-db01","os":"Windows Server 2019","software":["SQL Server 2016","Java 8"]}
enrichment={"business_unit":"Finance","criticality":"high","eol_software":["Java 8 (EOL)"],
            "open_ports":[1433,3389]}
asset.update(enrichment)
print(asset)
print("CSAM: raw asset + business context + EOL data = actionable inventory")
PY
```

**Expected result:** an asset **enriched** with business unit, criticality, and EOL flags — CSAM
context.

**Negative test:** treat a bare hostname list as your inventory; without **context** you can't
prioritize — enrich it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Discover the external attack surface

**Objective:** Find unknown internet assets.

```python
python3 - <<'PY'
known={"www.example.com","mail.example.com"}
easm_discovered={"www.example.com","mail.example.com","legacy-portal.example.com","dev-api.example.com"}
shadow=easm_discovered - known
print("shadow internet-facing assets (EASM):", shadow)
print("CSAM EASM: assess these before an attacker finds them")
PY
```

**Expected result:** **shadow internet-facing assets** discovered — External Attack Surface
Management.

**Negative test:** scan only known assets; **unknown** internet-facing systems remain exposed — run
EASM.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Flag end-of-life software

**Objective:** Surface unpatchable risk.

```python
python3 - <<'PY'
software=[{"name":"Windows Server 2012","eol":True},{"name":"OpenSSL 1.0.2","eol":True},
          {"name":"Windows Server 2025","eol":False}]
eol=[s["name"] for s in software if s["eol"]]
print("end-of-life (no security updates):", eol)
print("CSAM: EOL software can't be patched -> replace/isolate/compensating controls")
PY
```

**Expected result:** the **EOL software** flagged — unpatchable-risk visibility.

**Negative test:** keep scanning EOL systems for patches that will never come; they need
**replacement/isolation** — flag and plan.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Detect unauthorized software

**Objective:** Enforce software policy.

```python
python3 - <<'PY'
authorized={"corporate browser","office suite","endpoint agent"}
installed={"corporate browser","office suite","p2p-sharing-tool","remote-access-tool"}
unauthorized=installed - authorized
print("unauthorized software:", unauthorized)
print("CSAM: flag unauthorized software (risk + policy violation) for removal")
PY
```

**Expected result:** the **unauthorized software** identified — software-policy enforcement.

**Negative test:** track only vulnerabilities and ignore **unauthorized apps**; risky tools persist —
flag them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VMDR begins with CSAM: a complete, enriched asset inventory with External Attack Surface Management,
end-of-life and unauthorized-software detection, and dynamic tagging — the visibility foundation that
everything else depends on.

- [ ] I can enrich an asset inventory.
- [ ] I can discover the external attack surface.
- [ ] I can flag end-of-life software.
- [ ] I can detect unauthorized software.
- [ ] I completed Labs 3.1–3.4 including each negative test.
