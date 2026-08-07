# Chapter 05: Cloud Application Integration — Real Time

## Learning Objectives

- Distinguish Cloud Application Integration (CAI) from Cloud Data Integration (batch vs real time).
- Describe processes, service connectors, and app connections.
- Explain event-driven and API-triggered integration.
- Recognize where CAI fits alongside the rest of IDMC.

*Cert relevance: CAI is the Cloud Application Integration Developer, Professional exam — the real-time counterpart to CDI.*

## Batch versus real time

**Cloud Data Integration** ([Ch 3](03-cloud-data-integration.md)) moves data in **batches** — load millions of rows on a schedule. **Cloud Application Integration (CAI)** is its **real-time** counterpart: it connects **applications and services** so they exchange data **as events happen**, not on a nightly schedule. When a new order is created in one system and must **immediately** update inventory, notify shipping, and post to finance, that is CAI's job. Where CDI thinks in **rows and mappings**, CAI thinks in **messages, requests, and processes**.

The two are complementary and share the IDMC platform: many real solutions use **both** — CAI handles the real-time, event-driven flows while CDI handles the bulk loads. The **Cloud Application Integration Developer, Professional** certification is the real-time counterpart to the CDI Developer credential. The lab contrasts batch and real-time integration.

## Processes

The central abstraction in CAI is the **process** — an **orchestration** that runs in **real time** in response to a trigger. A process is a **flow of steps**: receive a request or event, call services, transform and route data, apply logic, and return a response. Unlike a batch mapping, a process:

- Runs **on demand** — triggered by an **API call**, an **event**, or a **schedule**.
- Handles **one transaction (or a few)** at a time, **quickly** — request/response latency matters.
- **Orchestrates services** — it calls out to applications, APIs, and other processes, waits for responses, and composes them.

A process can be **synchronous** (caller waits for a response — request/reply) or **asynchronous** (fire-and-forget or event-driven). This is classic **application/API integration and orchestration** — the same problem space as an integration/iPaaS platform. The lab builds a request/response process.

## Service connectors and app connections

CAI connects to the outside world through **connectors** and **connections**:

- **App connections** — configured links to **applications and systems** (Salesforce, SAP, databases, messaging systems), holding endpoints and credentials so processes can call them.
- **Service connectors** — definitions of **REST/SOAP services** a process can invoke: the URL, method, request/response structure, and authentication. A service connector turns an external API into a callable step inside a process.
- **Process objects** — reusable **data structures** passed between steps (the shape of an "order" moving through the flow).

Together these let a process **call any application or API** as a step — read from one system, transform, and write to another, in real time. Building and reusing these connectors well is core CAI skill. The lab models a service-connector call.

## Event-driven and API-triggered integration

CAI shines at **event-driven** and **API-first** patterns:

- **Expose a process as an API** — publish a process as a **REST endpoint** so other systems (or a web/mobile app) can invoke it. CAI becomes an **API layer** over your back-end systems.
- **React to events** — trigger a process when a **message arrives** (a queue/topic) or a **system emits an event**, propagating changes across applications immediately.
- **Guaranteed, orchestrated delivery** — with error handling, retries, and branching, so a real-time flow is **reliable**, not best-effort.

This is where CAI overlaps conceptually with dedicated integration platforms like **MuleSoft** ([Vol CLX](../../volume-160-mulesoft-certifications/README.md)) and **Boomi** — the difference is that CAI lives **inside IDMC**, sharing metadata and connectivity with data integration, quality, and governance. The lab exposes a process as an API and triggers it by event.

## Hands-On Lab

Python simulates a CAI process — request/response, a service-connector call, and an event trigger. **Cost:** none.

### Lab 5.1 — Build a real-time process with a service connector

**Objective:** Orchestrate a synchronous process that calls services and reacts to an event.

```bash
python3 - <<'EOF'
# a SERVICE CONNECTOR = a callable definition of an external API
def svc_inventory(sku):        # pretend REST call to an inventory service
    stock = {"SKU-1": 12, "SKU-2": 0}.get(sku, 0)
    return {"sku": sku, "in_stock": stock > 0, "qty": stock}
def svc_shipping(order_id):     # pretend REST call to a shipping service
    return {"order_id": order_id, "carrier": "ACME", "eta_days": 3}

# a CAI PROCESS = a real-time orchestration triggered by a request or event
def process_new_order(order):   # synchronous: caller waits for a response
    print(f"   [trigger] process invoked for order {order['order_id']} (real time)")
    inv = svc_inventory(order["sku"])                 # call service connector 1
    print(f"   step call svc_inventory -> {inv}")
    if not inv["in_stock"]:
        return {"order_id": order["order_id"], "status": "BACKORDERED"}
    ship = svc_shipping(order["order_id"])            # call service connector 2
    print(f"   step call svc_shipping  -> {ship}")
    return {"order_id": order["order_id"], "status": "CONFIRMED", "eta_days": ship["eta_days"]}

print("CAI — REAL-TIME application integration (vs CDI batch):\n")
print("Synchronous process (request -> orchestrate services -> response):")
resp = process_new_order({"order_id": 5001, "sku": "SKU-1"})
print(f"   RESPONSE: {resp}\n")

print("Event-driven trigger (a message arrives -> react immediately):")
for evt in [{"order_id": 5002, "sku": "SKU-2"}]:
    print(f"   [event] order.created {evt}")
    print(f"   -> {process_new_order(evt)}")
print()
print("A CAI PROCESS orchestrates SERVICE CONNECTORS (callable external APIs) in REAL")
print("TIME. Synchronous processes are request/response (expose as a REST API); event")
print("triggers react the moment a message arrives. Where CDI moves ROWS in batches, CAI")
print("moves MESSAGES as events happen. This real-time orchestration is the CAI Developer,")
print("Professional certification — the real-time counterpart to CDI.")
EOF
```

**Expected result:** A synchronous process that receives an order, calls an inventory service connector, calls a shipping service connector, and returns a confirmation — plus an event-triggered invocation that back-orders an out-of-stock item. The lesson is CAI's real-time model: a process orchestrates service connectors in response to API calls or events, the request/response counterpart to CDI's batch mappings, and the substance of the CAI Developer Professional certification.

**Negative test:** Using a nightly CDI batch to propagate order events. The inventory and shipping systems would be hours stale; real-time application integration requires event/API-triggered processes (CAI), not scheduled bulk loads (CDI).

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] CAI distinguished from CDI — real-time application/API integration versus batch data integration.
- [ ] Processes understood — real-time orchestrations triggered by API calls, events, or schedules.
- [ ] Service connectors and app connections understood — the callable links to external systems and APIs.
- [ ] Event-driven and API-first patterns recognized — expose processes as APIs and react to events.

## See also

- [Chapter 03 — Cloud Data Integration](03-cloud-data-integration.md) — the batch counterpart CAI complements.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — a dedicated API/integration platform in the same problem space.
- [Chapter 08 — Data Governance and Catalog](08-governance-and-catalog.md) — the shared metadata CAI contributes to.
