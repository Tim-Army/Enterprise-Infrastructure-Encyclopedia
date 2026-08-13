# Chapter 05: API Management

## Learning Objectives

- Explain what API Management adds on top of integration.
- Describe designing and publishing an API from a Boomi process.
- Apply API policies — security, rate limiting, and governance.
- Understand the API Control Plane and the API Management certifications.

*Cert relevance: this is the Professional API Design and Professional API Management track.*

## From integration to API

An integration **process** ([Ch 4](04-building-integrations.md)) moves data between systems. **API Management (APIM)** turns that capability **outward**: it lets you **publish** a process as a **managed API** that other applications, partners, or teams can call — with **security, control, and governance** around it. Instead of point-to-point integrations, you expose **reusable API endpoints** ("get customer", "create order") that many consumers use, and you **manage** who can call them, how often, and how securely.

APIM is the difference between "I wired system A to system B" and "I published a governed API that any consumer can use safely." As enterprises build dozens or hundreds of APIs, **managing** them — securing, versioning, monitoring, and governing — becomes essential. The **Professional API Design** and **Professional API Management** certifications validate this. The lab publishes and governs an API.

## Designing and publishing an API

In Boomi you **design an API** and **publish** it to a **gateway**:

- **Design** — define the API's **endpoints** (paths), **methods** (GET/POST), and the **process** that backs each one. A REST endpoint like `GET /customers/{id}` is wired to a process that fetches the customer.
- **Publish to a gateway** — deploy the API to an **API Gateway** (running on an Atom/Molecule, [Ch 3](03-atoms-molecules-atom-clouds.md)) that **receives external calls** and routes them to the backing process. The gateway is the **front door**.
- **Expose a contract** — consumers get a documented API (often OpenAPI/Swagger) they can call, without knowing the integration behind it.

So the flow is **process → API design → gateway → consumers**. The gateway is where management happens: every call passes through it, so it is the natural place to enforce policy. The lab designs an endpoint and routes it to a process.

## API policies

The gateway enforces **policies** on API traffic — this is the "management" in API Management:

- **Security / authentication** — require an **API key**, OAuth token, or basic auth; reject unauthenticated calls. Only authorized consumers get through.
- **Rate limiting / throttling** — cap calls per consumer per time window (e.g. 100/minute) to protect back-ends and enforce fair use.
- **Traffic management** — routing, caching, and versioning (serve `/v1` and `/v2` side by side).
- **Observability** — log and measure every call: who called, how often, latency, errors.

Policies are **configured, not coded**, and applied at the gateway so they protect **every** consumer uniformly. Designing good policies — enough security and control without blocking legitimate use — is core APIM skill. The lab applies auth and rate-limit policies.

## The API Control Plane and certifications

Boomi's **API Control Plane** addresses **API sprawl** — the problem of **too many APIs** across gateways and teams, including **"zombie APIs"** (undocumented, unmanaged, forgotten endpoints that are a security and maintenance risk). The Control Plane provides **federated** management and **governance** across all your APIs and gateways, so the whole estate is **discoverable, governed, and secure** — not a scattered mess.

The certifications reflect the two sides:

- **Professional API Design** — designing good APIs (endpoints, contracts, versioning, usability).
- **Professional API Management** — securing, governing, and operating APIs at scale (policies, gateways, the Control Plane).

Both are open-book/open-platform. The lab models the Control Plane governing an API estate. *(This is the same problem space as [MuleSoft's API-led approach and Anypoint (Vol CLX)](../../volume-160-mulesoft-certifications/README.md) — reusable, governed APIs as building blocks.)*

## Hands-On Lab

Python publishes a process as an API, applies policies, and governs the estate. **Cost:** none.

### Lab 5.1 — Publish and govern an API

**Objective:** Route an endpoint to a process, enforce auth + rate limit, and inventory the estate.

```bash
python3 - <<'EOF'
import time
# --- DESIGN + PUBLISH: map API endpoints to backing processes ---
API = {
  ("GET",  "/customers/{id}"): "p_get_customer",
  ("POST", "/orders"):         "p_create_order",
}
# --- POLICIES enforced at the GATEWAY ---
VALID_KEYS = {"key-acme", "key-globex"}
RATE_LIMIT = 3          # calls per consumer per window
calls = {}

def gateway(method, path, api_key):
    # policy 1: authentication
    if api_key not in VALID_KEYS:
        return "401 Unauthorized (bad API key)"
    # policy 2: rate limiting
    calls[api_key] = calls.get(api_key, 0) + 1
    if calls[api_key] > RATE_LIMIT:
        return f"429 Too Many Requests (> {RATE_LIMIT}/window)"
    # route to backing process
    proc = API.get((method, path))
    return f"200 OK -> {proc}" if proc else "404 No such API"

print("API MANAGEMENT — publish a process as a governed API:\n")
print("   Published endpoints (API -> backing process):")
for (m, p), proc in API.items():
    print(f"      {m:4} {p:18} -> {proc}")
print("\n   Gateway enforcing auth + rate-limit (limit=3/window):")
for i, (m, p, key) in enumerate([
    ("GET","/customers/{id}","key-acme"), ("GET","/customers/{id}","key-acme"),
    ("POST","/orders","key-acme"), ("GET","/customers/{id}","key-acme"),   # 4th acme -> 429
    ("GET","/customers/{id}","key-bad")], 1):                              # bad key -> 401
    print(f"      call {i}: {m:4} {p:18} key={key:9} -> {gateway(m,p,key)}")

# --- API CONTROL PLANE: govern the estate, find zombie APIs ---
ESTATE = [
  {"api": "customers", "documented": True,  "last_call_days": 2},
  {"api": "orders",    "documented": True,  "last_call_days": 1},
  {"api": "legacy-v0", "documented": False, "last_call_days": 400},   # zombie
]
print("\n   API CONTROL PLANE — govern the estate:")
for a in ESTATE:
    zombie = (not a["documented"]) or a["last_call_days"] > 365
    print(f"      {a['api']:12} documented={a['documented']!s:5} -> {'ZOMBIE (retire/govern)' if zombie else 'healthy'}")
print()
print("APIM publishes a PROCESS as a managed API behind a GATEWAY that enforces POLICIES")
print("(auth rejects the bad key -> 401; rate-limit caps calls -> 429) uniformly for every")
print("consumer. The API CONTROL PLANE governs the whole estate and flags ZOMBIE APIs")
print("(undocumented/unused) to fight API sprawl. Design + management = the two APIM certs.")
EOF
```

**Expected result:** An API that maps endpoints to backing processes, a gateway that rejects a bad key (401) and throttles a consumer over its limit (429) while routing valid calls, and an API Control Plane that flags an undocumented, long-unused API as a zombie. The lesson is what API Management adds over raw integration — publishing processes as governed APIs behind a policy-enforcing gateway, with the Control Plane governing the estate against sprawl — the substance of the Professional API Design and API Management certifications.

**Negative test:** Exposing back-end processes directly with no gateway. There is no authentication, no rate limiting, and no inventory, so any caller can hammer the back-end and undocumented endpoints accumulate as zombie APIs; the gateway and Control Plane are what make APIs safe and governed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The step from integration to API understood — publishing reusable, governed API endpoints.
- [ ] Designing and publishing understood — endpoints and methods routed through a gateway to processes.
- [ ] API policies understood — authentication, rate limiting, traffic management, and observability.
- [ ] The API Control Plane and certifications placed — federated governance against sprawl; Design and Management.

## See also

- [Chapter 04 — Building Integrations](04-building-integrations.md) — the processes that back APIs.
- [Volume CLX — MuleSoft](../../volume-160-mulesoft-certifications/README.md) — API-led connectivity in the same problem space.
- [Chapter 09 — Choosing Your Boomi Path](09-choosing-your-boomi-path.md) — where APIM fits a career path.
