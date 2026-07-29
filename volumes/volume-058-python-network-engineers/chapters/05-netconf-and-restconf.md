# Chapter 05: NETCONF and RESTCONF

## Learning Objectives

- Explain model-driven management and YANG.
- Use ncclient for NETCONF get/edit operations.
- Use RESTCONF over HTTP with `requests`.
- Contrast NETCONF and RESTCONF.
- Complete a walkthrough for each model-driven skill.

## Theory and Architecture

**Model-driven** management replaces CLI scraping with structured, validated interfaces
defined by **YANG** data models. **NETCONF** runs over SSH (port 830) with XML payloads
and explicit datastores (running/candidate) and operations (`get-config`, `edit-config`,
`commit`); **ncclient** is the Python client. **RESTCONF** exposes the same YANG models
over **HTTP** (port 443) with JSON or XML, so you use plain **`requests`** with URLs like
`/restconf/data/<model>`. Both return structured data and validate config against the
model — no fragile text parsing.

## Design Considerations

Prefer **NETCONF** for transactional changes (candidate datastore + commit/rollback) and
**RESTCONF** for simple REST-style reads/writes and easy integration. Both need the
feature **enabled** on the device. Target the right **YANG model** (native vs OpenConfig).

## Implementation and Automation

The labs use ncclient for NETCONF and `requests` for RESTCONF.

## Validation and Troubleshooting

Confirm the model:

```text
NETCONF (ssh :830): ncclient manager.connect -> get_config / edit_config / commit. XML + YANG.
RESTCONF (https :443): requests GET/PUT/PATCH /restconf/data/<model>. JSON/XML + YANG.
```

Common pitfalls: NETCONF/RESTCONF **not enabled** on the device; and wrong **YANG model**
path.

## Security and Best Practices

Enable NETCONF/RESTCONF over **TLS/SSH**, use the **candidate datastore + commit** for
transactional safety (NETCONF), target the correct **YANG model**, and keep credentials
in a vault. Validate against the model before pushing.

## Hands-On Lab

Model-driven walkthroughs. **Shared prerequisites** — Python 3.12+ (`pip install ncclient
requests`); a NETCONF/RESTCONF-enabled lab device (or the patterns shown). **Cost:** none.

### Lab 5.1 — NETCONF get-config

**Objective:** Retrieve config over NETCONF.

```python
from ncclient import manager
with manager.connect(host="10.0.0.11", port=830, username="admin", password="admin",
                     hostkey_verify=False) as m:
    cfg = m.get_config(source="running")
    print("got", len(str(cfg)), "bytes of XML config")
```

**Expected result:** the running config as **XML** — a model-driven read.

**Negative test:** connect to :830 when NETCONF is **disabled**; enable it (`netconf-yang`)
first.

**Cleanup:** the `with` closes the session.

### Lab 5.2 — NETCONF edit-config

**Objective:** Change config transactionally.

```python
edit = """<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface><name>Loopback102</name><enabled>true</enabled></interface>
</interfaces></config>"""
with manager.connect(host="10.0.0.11", port=830, username="admin", password="admin", hostkey_verify=False) as m:
    m.edit_config(target="candidate", config=edit)
    m.commit()
```

**Expected result:** the candidate edited and **committed** — a transactional change.

**Negative test:** edit `running` directly without candidate/commit; use the
**candidate + commit** model for safe transactions.

**Cleanup:** delete Loopback102 via another edit-config.

### Lab 5.3 — RESTCONF GET

**Objective:** Read config over RESTCONF.

```python
import requests
r = requests.get("https://10.0.0.11/restconf/data/ietf-interfaces:interfaces",
                 auth=("admin","admin"), headers={"Accept":"application/yang-data+json"},
                 verify=False, timeout=10)
print(r.status_code, "->", list(r.json().keys()))
```

**Expected result:** **200** and a JSON body keyed by the YANG model — a RESTCONF read.

**Negative test:** omit the `Accept: application/yang-data+json` header; set the correct
**media type** for RESTCONF.

**Cleanup:** none (read-only).

### Lab 5.4 — Contrast NETCONF and RESTCONF

**Objective:** Choose the right protocol.

```python
print("NETCONF: ssh:830, XML, candidate+commit (transactional).")
print("RESTCONF: https:443, JSON/XML, REST verbs (simple integration).")
```

**Expected result:** the trade-offs — transactional NETCONF vs REST-friendly RESTCONF.

**Negative test:** force RESTCONF for a multi-step transactional change; **NETCONF's
candidate/commit** is safer there — pick per need.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Model-driven management uses YANG models over NETCONF (ncclient, SSH, candidate/commit)
and RESTCONF (requests, HTTP/JSON) — returning structured, validated data instead of CLI
text. This chapter read and edited config over both.

- [ ] I can explain YANG and model-driven management.
- [ ] I can get/edit config over NETCONF with ncclient.
- [ ] I can read config over RESTCONF with requests.
- [ ] I can choose NETCONF vs RESTCONF per need.
- [ ] I completed Labs 5.1–5.4 including each negative test.
