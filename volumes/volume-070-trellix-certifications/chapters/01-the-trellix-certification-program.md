# Chapter 01: The Trellix Certification Program

## Learning Objectives

- Explain Trellix, its lineage (McAfee Enterprise + FireEye), and its platform.
- Describe the Trellix Education Services certification model (per-product specialists).
- Map the products to certifications (ePO, ENS, EDR, Network Security, DLP, Helix).
- Understand the Data Exchange Layer (DXL) that ties the platform together.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**Trellix** is the enterprise security company formed in 2022 from the merger of **McAfee
Enterprise** and **FireEye**, combining a broad **endpoint, network, data, and SecOps** portfolio
into an **XDR** platform. Its certification program is delivered by **Trellix Education Services**
(the successor to McAfee's education organization) and follows a **per-product Certified Product
Specialist** model — a certification validates that you can **install, configure, and administer** a
specific Trellix product. The core products and their certifications are: **ePolicy Orchestrator
(ePO)** — the central management console; **Endpoint Security (ENS)** — the endpoint protection
suite; **Endpoint Detection and Response (EDR)**; **Network Security (IPS)** and **Advanced Threat
Defense (ATD)**; **Data Loss Prevention (DLP)**; and **Helix** — the SecOps/SIEM/XDR platform.
Tying them together is the **Data Exchange Layer (DXL)** — a real-time messaging fabric (with the
open-source **OpenDXL**) that lets products share intelligence and orchestrate response.

Because the program carries a **McAfee → Trellix rebrand**, exam codes are in transition (the
legacy McAfee exams used **MA0-###** codes, e.g., MA0-100 for Endpoint Security, MA0-101 for ePO).
Verify current codes on trellix.com. This volume teaches each product-specialist track with
hands-on, **defensive** administration walkthroughs.

> **Scope.** Trellix's EDR, network security, and DLP are defensive platforms. Every lab is
> **authorized administration, detection, hunting, response, or automation** — never an
> operational attack technique.

## Design Considerations

Start with **ePO** — it is the management plane most Trellix products register to — then add the
product-specialist tracks your role needs (ENS for endpoint, EDR for detection/response, DLP for
data protection, Helix for SecOps). Use **DXL/OpenDXL** to integrate. Because of the rebrand,
**verify current course and exam details** on trellix.com.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.trellix.com/services/education/" \
  | grep -oiE 'Endpoint Security|ePolicy Orchestrator|EDR|Network Security|Data Loss|Helix|Certified' | sort -u
```

## Validation and Troubleshooting

The verified program facts (trellix.com and course descriptions, 28 July 2026):

```text
Trellix = McAfee Enterprise + FireEye (2022). Trellix Education Services: per-product Certified Product Specialist.
Products/certs: ePO (mgmt), ENS (endpoint), EDR, Network Security (IPS)/ATD, DLP, Helix (SecOps/XDR).
Fabric: Data Exchange Layer (DXL) + open-source OpenDXL. Legacy McAfee exam codes MA0-### in transition.
```

Common pitfalls: using **legacy McAfee (MA0-###)** codes as current without checking; and treating
Trellix as a single exam (it is **per-product**).

## Security and Best Practices

Center the deployment on **ePO**, integrate with **DXL**, and practice on **authorized** lab
instances only. Verify certifications and codes on trellix.com — third-party dumps are neither
authoritative nor permitted. All administration here is defensive.

## References and Knowledge Checks

- trellix.com/services/education: Trellix Education Services courses and certifications.
- OpenDXL (opendxl.com / github.com/opendxl): the open Data Exchange Layer SDK.

**Knowledge checks**

1. From which two companies was Trellix formed?
2. What does the Certified Product Specialist model validate?
3. What is DXL, and what is OpenDXL?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the product/certification set

**Objective:** Read the program from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.trellix.com/services/education/" \
  | grep -oiE 'Endpoint Security|ePolicy Orchestrator|EDR|Network Security|Data Loss Prevention|Helix' | sort -u
```

**Expected result:** the Trellix products with certification tracks — the program map.

**Negative test:** rely on old **McAfee** branding/codes; the program is **Trellix** now, with
codes in transition — confirm on trellix.com.

**Cleanup:** none.

### Lab 1.2 — Map products to certifications

**Objective:** Record the product-specialist tracks.

```python
python3 - <<'PY'
certs={"ePolicy Orchestrator (ePO)":"central management (legacy MA0-101)",
       "Endpoint Security (ENS)":"endpoint protection (legacy MA0-100)",
       "EDR":"detection and response","Network Security (IPS)":"network IPS (legacy MA0-104)",
       "Data Loss Prevention (DLP)":"data protection","Helix":"SecOps/SIEM/XDR"}
for p,f in certs.items(): print(f"{p:32}: {f}")
PY
```

**Expected result:** a product → certification map — your study reference (verify current codes).

**Negative test:** assume one Trellix exam; certifications are **per product** — pick the products
for your role.

**Cleanup:** none.

### Lab 1.3 — Plan a Trellix path

**Objective:** Sequence certifications for a role.

```python
python3 - <<'PY'
paths={"Endpoint admin":"ePO -> ENS","Detection/response":"ePO -> ENS -> EDR",
       "Data protection":"ePO -> DLP","SecOps analyst":"Helix (+ EDR)","Network security":"Network Security (IPS) + ATD"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences — the tracks this volume follows (ePO first for
endpoint-managed products).

**Negative test:** deploy ENS/EDR with no **ePO**; most Trellix endpoint products manage through
**ePO** — start there.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Trellix (McAfee Enterprise + FireEye) certifies per-product specialists through Trellix Education
Services across ePO, ENS, EDR, Network Security, DLP, and Helix, integrated by the DXL fabric.
Start with ePO, add product tracks by role, use DXL/OpenDXL, and verify current codes on
trellix.com.

- [ ] I can explain the Trellix lineage and platform.
- [ ] I can describe the per-product certification model.
- [ ] I can map products to certifications.
- [ ] I can plan a Trellix certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
