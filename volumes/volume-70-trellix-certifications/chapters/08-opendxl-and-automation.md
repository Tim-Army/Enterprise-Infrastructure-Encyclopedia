# Chapter 08: OpenDXL and Automation

## Learning Objectives

- Explain the Data Exchange Layer (DXL) and open-source OpenDXL.
- Publish and subscribe to messages on the DXL fabric.
- Share threat intelligence across the platform.
- Automate response through DXL and product APIs.
- Complete a walkthrough for each automation topic (defensive).

## Theory and Architecture

The **Data Exchange Layer (DXL)** is Trellix's real-time **messaging fabric** — a lightweight
publish/subscribe and request/response bus that lets security products (and third-party tools)
**share context and orchestrate action** instantly, without brittle point-to-point integrations.
When ATD sandboxes a file and finds it malicious, it **publishes** the verdict on DXL; ENS, EDR, and
the network subscribe and **block it everywhere** in seconds. Trellix open-sourced the client side
as **OpenDXL** (opendxl.com), with a real **Python SDK** — so integration and automation are genuine
code, not just console clicks. Beyond DXL, each product exposes a **REST API** (ePO, EDR, Helix) for
scripting. The pattern is **event-driven security automation**: an event on the fabric triggers
enrichment, decision, and response across integrated tools. This chapter's automation is
**defensive** — sharing intelligence and orchestrating protection.

## Design Considerations

Integrate through **DXL/OpenDXL** rather than point-to-point where possible — one fabric, many
producers/consumers. Use **pub/sub** for intelligence sharing and **request/response** for service
calls. Keep credentials/certificates secure (DXL uses mutual TLS). Put **human approval** on
consequential automated actions. Version automation in Git.

## Implementation and Automation

The labs use the OpenDXL Python SDK to connect, subscribe, and publish an indicator, and reason
about API automation — all **defensive**.

## Validation and Troubleshooting

Confirm the automation model:

```text
DXL: real-time pub/sub + request/response fabric (mutual TLS). OpenDXL: open-source client + Python SDK.
Pattern: ATD verdict -> publish on DXL -> ENS/EDR/network subscribe -> block everywhere.
Also: product REST APIs (ePO/EDR/Helix). Human approval on consequential actions.
```

Common pitfalls: **point-to-point** integrations where DXL's fabric fits; and automated response
with **no approval** on high-impact actions.

## Security and Best Practices

Use the **DXL fabric** for scalable integration, secure it with **mutual TLS/certificates**, and
gate consequential automation with **human approval**. Keep automation in **Git**, least-privilege
the service accounts, and audit actions. Defensive orchestration throughout.

## Hands-On Lab

Automation walkthroughs (defensive). **Shared prerequisites for Labs 8.1–8.3** — Python with
`pip install dxlclient` and access to a DXL broker (or the patterns), in an **authorized** lab.
**Cost:** none (OpenDXL is open source).

### Lab 8.1 — Connect and subscribe with OpenDXL

**Objective:** Join the DXL fabric and listen for events.

```python
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.callbacks import EventCallback

config = DxlClientConfig.create_dxl_config_from_file("dxlclient.config")
with DxlClient(config) as client:
    client.connect()
    class Handler(EventCallback):
        def on_event(self, event):
            print("DXL event:", event.payload.decode())
    client.add_event_callback("/threat/intel/indicator", Handler())
    print("subscribed to /threat/intel/indicator")
```

**Expected result:** an **OpenDXL** client connected and **subscribed** to a threat-intel topic —
listening on the fabric.

**Negative test:** poll each product's API on a timer for new intel; **DXL pub/sub** pushes it in
real time — subscribe.

**Cleanup:** disconnect (context manager handles it).

### Lab 8.2 — Publish an indicator

**Objective:** Share a malicious hash to the fabric.

```python
from dxlclient.message import Event
import json
# (within a connected DxlClient 'client')
event = Event("/threat/intel/indicator")
event.payload = json.dumps({"type":"md5","value":"<hash>","verdict":"malicious"}).encode()
client.send_event(event)
print("published malicious-hash indicator to DXL -> subscribers block it")
```

**Expected result:** a malicious indicator **published** on DXL — every subscriber can now block it
(estate-wide protection).

**Negative test:** email the hash to each product owner to block manually; **publish on DXL** for
instant, automated propagation.

**Cleanup:** none (event is transient).

### Lab 8.3 — Orchestrated response with approval

**Objective:** Automate a response with a human gate.

```python
python3 - <<'PY'
def orchestrate(indicator_malicious, analyst_approved):
    if not indicator_malicious: return "no action"
    if not analyst_approved: return "await analyst approval (contain proposed)"
    return "DXL: EDR isolate host + ENS block hash + Helix incident note"
print(orchestrate(True, False))
print(orchestrate(True, True))
PY
```

**Expected result:** response **proposed**, then **executed after approval** across EDR/ENS/Helix —
orchestrated, gated automation.

**Negative test:** auto-execute containment fleet-wide with no approval; gate **consequential**
actions on a human — then orchestrate.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

DXL is Trellix's real-time pub/sub fabric, open-sourced as OpenDXL with a Python SDK, enabling
event-driven security automation — an ATD verdict published on DXL blocks a threat across ENS, EDR,
and the network instantly. Integrate via the fabric, share intelligence, gate consequential actions
on approval, and secure it with mutual TLS. Defensive orchestration throughout.

- [ ] I can connect and subscribe with OpenDXL.
- [ ] I can publish a threat indicator to DXL.
- [ ] I can orchestrate a gated response.
- [ ] I can explain DXL vs point-to-point integration.
- [ ] I completed Labs 8.1–8.3 including each negative test.
