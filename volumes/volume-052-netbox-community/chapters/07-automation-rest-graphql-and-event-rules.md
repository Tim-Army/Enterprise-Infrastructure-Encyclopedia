# Chapter 07: Automation — REST, GraphQL, and Event Rules

## Learning Objectives

- Query and mutate NetBox through the REST API.
- Retrieve exactly the fields you need with GraphQL.
- Trigger outbound automation with webhooks and event rules.
- Bulk-load data efficiently.
- Complete a walkthrough for each automation surface.

## Theory and Architecture

NetBox's automation surfaces are the **REST API** (`/api/`, full CRUD, filtering,
pagination, bulk operations), the **GraphQL API** (`/graphql/`, fetch exactly the
fields/relations you want in one request), and **event-driven** outbound automation:
an **Event Rule** watches for object create/update/delete and fires an action — most
commonly a **webhook** (HTTP POST to an external system) or a script. Together they
make NetBox both the source of truth and a trigger for downstream automation.

## Design Considerations

Use **REST** for CRUD and bulk changes, **GraphQL** to avoid over-fetching in
read-heavy integrations, and **event rules + webhooks** to push changes outward
(e.g., trigger a pipeline when a device is created). Prefer **bulk** endpoints over
per-object loops for large loads.

## Implementation and Automation

The labs use `curl`/`pynetbox` for REST, a GraphQL query, a bulk create, and an event
rule + webhook.

## Validation and Troubleshooting

Confirm the surfaces:

```text
REST: /api/<app>/<model>/ CRUD + ?filters + bulk (list payloads).
GraphQL: POST /graphql/ { model { field relation { field } } }.
Event Rule -> Webhook: on create/update/delete -> HTTP POST to a URL.
```

Common pitfalls: N+1 REST calls where **GraphQL** or **bulk** fits; and webhooks with
no receiver (silent failures).

## Security and Best Practices

Scope **tokens** to least privilege, page/bulk large operations, use **GraphQL** to cut
payloads, and secure webhooks (secret/HMAC, TLS receiver). Log and monitor event-rule
deliveries.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — a running NetBox; `$NB`/`$TOKEN`;
`curl`, `python3`, `pynetbox`. **Cost:** none.

### Lab 7.1 — REST: filter and page

**Objective:** Query devices with a filter.

```bash
curl -sS -H "Authorization: Token $TOKEN" \
  "$NB/api/dcim/devices/?role=leaf&limit=5" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('count:',d['count'])"
```

**Expected result:** the **count** of leaf-role devices — REST filtering/pagination.

**Negative test:** fetch all devices and filter client-side; use **server-side
filters** (`?role=`) to cut payload.

**Rollback:** none (read-only).

### Lab 7.2 — GraphQL: fetch exact fields

**Objective:** Get device names and their site in one query.

```bash
curl -sS -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  -X POST "$NB/graphql/" \
  -d '{"query":"{ device_list { name site { name } } }"}'
```

**Expected result:** a JSON list of devices with `name` and nested `site.name` — one
round-trip, no over-fetch.

**Negative test:** call REST per device to get its site; **GraphQL** returns the graph
in one request.

**Rollback:** none (read-only).

### Lab 7.3 — REST bulk create

**Objective:** Create multiple objects in one request.

```bash
curl -sS -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  -X POST "$NB/api/ipam/vlans/" \
  -d '[{"vid":201,"name":"v201"},{"vid":202,"name":"v202"}]' \
  | python3 -c "import sys,json;print('created:',len(json.load(sys.stdin)))"
```

**Expected result:** **2** VLANs created in a single call — bulk efficiency.

**Negative test:** POST each VLAN separately in a loop; a **list payload** is one
transaction — bulk it.

**Rollback:** delete VLANs 201–202.

### Lab 7.4 — Event rule + webhook

**Objective:** Fire a webhook when a device is created.

```python
import pynetbox
nb = pynetbox.api("http://localhost:8000", token="TOKEN")
wh = nb.extras.webhooks.create(name="notify", payload_url="http://receiver.example/hook",
     http_method="POST")
er = nb.extras.event_rules.create(name="dev-created", object_types=["dcim.device"],
     event_types=["object_created"], action_type="webhook", action_object_id=wh.id,
     action_object_type="extras.webhook")
print("event rule:", er.name, "-> webhook:", wh.name)
```

**Expected result:** an **event rule** that POSTs to the webhook on device creation —
outbound automation.

**Negative test:** poll NetBox on a timer for new devices; an **event rule** pushes
instantly — prefer event-driven.

**Rollback:** `er.delete(); wh.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox automates through REST (CRUD, filtering, bulk), GraphQL (exact-field fetch), and
event rules with webhooks (push on change). This chapter queried, bulk-loaded, and
wired an event-driven webhook.

- [ ] I can filter and page the REST API.
- [ ] I can fetch exact fields with GraphQL.
- [ ] I can bulk-create objects.
- [ ] I can fire a webhook from an event rule.
- [ ] I completed Labs 7.1–7.4 including each negative test.
