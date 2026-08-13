# Chapter 09: Automation, Currency, and Career Paths

## Learning Objectives

- Automate SR OS with MD-CLI, NETCONF, gRPC, and pySROS.
- Explain Nokia certification validity and recertification.
- Track program change across the SRC program.
- Plan a Nokia certification path and relate it to the encyclopedia's volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Modern SR OS is **model-driven and automatable**. The **MD-CLI** exposes the same **YANG** data
model as the programmatic interfaces, so configuration is consistent across CLI and code:
**NETCONF** and **gRPC/gNMI** provide programmatic config and telemetry, and **pySROS** is Nokia's
official Python library for scripting SR OS (on-box and off-box) against that model. This makes SR
OS networks manageable as **code**: declare intent, push via NETCONF/pySROS from a Git source of
truth, and stream telemetry via gNMI. On the program side, Nokia's **SRC** certifications carry a
validity period and evolve as the platform and technologies (Segment Routing, SRv6, EVPN) advance —
so confirm the current exams and recert terms on nokia.com. Plan a path by role from NRS I upward.

## Design Considerations

Prefer the **MD-CLI** and the **model** for new work so CLI and automation align. Drive config from
**Git** via **pySROS/NETCONF**, and stream **telemetry** with gNMI instead of screen-scraping. Plan
certification by role — **NRS I → NRS II → SRA** — and recertify before expiry.

## Implementation and Automation

The labs script SR OS with pySROS, use NETCONF, and verify the current program.

## Validation and Troubleshooting

Confirm the automation and currency facts:

```text
Model-driven: MD-CLI + YANG model exposed via NETCONF + gRPC/gNMI; pySROS (Python) for scripting.
Manage as code: declare intent -> push via pySROS/NETCONF from Git -> telemetry via gNMI.
Program: SRC evolves (SR/SRv6/EVPN); renew before expiry. Path: NRS I -> NRS II -> SRA.
```

Common pitfalls: screen-scraping the CLI instead of using the **model/pySROS**; and studying a
**superseded** exam variant.

## Security and Best Practices

Keep intent in **Git**, push through **pySROS/NETCONF** with review, and secure programmatic access
(TLS, AAA, least privilege). Recertify on time and track platform/technology change (SR, SRv6,
EVPN). Automate configuration and telemetry — defensively.

## References and Knowledge Checks

- nokia.com/networks/training/src: the SRC program, exams, and recert terms.
- Nokia SR OS documentation and pySROS: the model, MD-CLI, and Python automation.
- Related encyclopedia volumes: Cisco Service Provider (XXIX), Juniper (XXXI), NetBox (LII), Python for Network Engineers (LVIII).

**Knowledge checks**

1. What interfaces expose the SR OS YANG model?
2. What is pySROS?
3. What path suits a service-provider network architect?

## Hands-On Lab

Automation and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.3** — an SR OS node
with NETCONF/gNMI enabled, Python with `pysros`, and `curl`, in a lab. **Cost:** none.

### Lab 9.1 — Script SR OS with pySROS

**Objective:** Read state from Python via the model.

```python
from pysros.management import connect
c = connect(host="10.0.0.1", username="admin", password="admin")
state = c.running.get("/nokia-state:state/router[router-name='Base']/interface")
print("interfaces via pySROS:", len(state))
```

**Expected result:** the router interfaces read through **pySROS** against the YANG model —
model-driven automation.

**Negative test:** parse `show router interface` text; **pySROS/the model** returns structured data
— use it.

**Rollback:** none (read-only).

### Lab 9.2 — Use NETCONF

**Objective:** Retrieve configuration programmatically.

```bash
# NETCONF <get-config> over SSH (port 830) returns the model-based config as XML.
ssh -p 830 admin@10.0.0.1 -s netconf <<'XML' 2>/dev/null | head || echo "NETCONF get-config returns SR OS config per the YANG model"
<rpc message-id="1"><get-config><source><running/></source></get-config></rpc>
XML
```

**Expected result:** the running configuration via **NETCONF** — programmatic, model-based access.

**Negative test:** automate via scraped CLI over telnet; use **NETCONF/gNMI** on the model — it is
structured and secure.

**Rollback:** none (read-only).

### Lab 9.3 — Verify the current program

**Objective:** Confirm exams before study or renewal.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nokia.com/networks/training/src/exams/" \
  | grep -oiE '4A0-[0-9CN]+|NRS|Service Routing Architect' | sort -u
```

**Expected result:** the current SRC exams and credentials — confirming scope.

**Negative test:** rely on a years-old exam list; the **SRC program evolves** — verify on
nokia.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Modern SR OS is model-driven: the MD-CLI and YANG model are exposed via NETCONF, gRPC/gNMI, and
pySROS, making networks manageable as code. Nokia SRC certifications renew before expiry and evolve
with SR/SRv6/EVPN. Automate against the model, plan by role from NRS I upward, and verify the
current program on nokia.com.

- [ ] I can script SR OS with pySROS.
- [ ] I can use NETCONF against the model.
- [ ] I can explain the MD-CLI/model/automation alignment.
- [ ] I can verify the current program and recert terms.
- [ ] I completed Labs 9.1–9.3 including each negative test.
