# Chapter 06: The API and Automation

## Learning Objectives

- Authenticate and navigate the LibreNMS REST API.
- Automate device lifecycle through the API.
- Bulk-query ports, alerts, and inventory.
- Drive LibreNMS from Ansible.
- Complete a walkthrough for each automation surface.

## Theory and Architecture

LibreNMS exposes a **REST API** under `/api/v0/` authenticated by an **`X-Auth-Token`**
header. It covers devices, ports, alerts, rules, device groups, bills, inventory, and
more — full lifecycle automation. Because onboarding and querying are scriptable,
LibreNMS integrates cleanly into pipelines: add devices from a source of truth
(NetBox), export inventory, or react to alerts. The **`nms`/`lnms`** CLI and community
Ansible content complement the API.

## Design Considerations

Drive **onboarding from a source of truth** rather than by hand — script `POST
/devices` from NetBox data. Use **scoped tokens**, page large queries, and prefer the
API over screen-scraping. Treat LibreNMS config (devices, groups, rules) as data you can
reconcile.

## Implementation and Automation

The labs use `curl`/Python and Ansible against the REST API.

## Validation and Troubleshooting

Confirm the surface:

```text
REST: /api/v0/<resource>; header X-Auth-Token: <token>.
Resources: devices, ports, alerts, rules, devicegroups, inventory, bills.
CLI: lnms device:add/list/poll/remove.
```

Common pitfalls: hard-coding a token in scripts (leak risk); and per-device loops where
a bulk query fits.

## Security and Best Practices

Use **least-privilege, rotatable tokens**, keep them out of source (env/secret store),
page large result sets, and drive onboarding from the **source of truth**. Log
automation actions.

## Hands-On Lab

Automation walkthroughs. **Shared prerequisites** — a running LibreNMS; `$LNMS`/`$TOKEN`;
`curl`, `python3`, `ansible`. **Cost:** none.

### Lab 6.1 — List devices with fields

**Objective:** Query devices and select fields.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/devices" \
  | python3 -c "import sys,json;[print(d['hostname'],d['os'],d['status']) for d in json.load(sys.stdin)['devices'][:5]]"
```

**Expected result:** hostname/OS/status for devices — the read path of the API.

**Negative test:** scrape the web UI for inventory; the **API** returns structured JSON —
use it.

**Cleanup:** none (read-only).

### Lab 6.2 — Add a device programmatically

**Objective:** Onboard from a script (as if sourced from NetBox).

```bash
curl -sS -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -X POST "$LNMS/api/v0/devices" \
  -d '{"hostname":"192.0.2.10","version":"v2c","community":"public"}' \
  | python3 -c "import sys,json;print('status:',json.load(sys.stdin).get('status'))"
```

**Expected result:** an **ok** status adding the device — scripted onboarding.

**Negative test:** add devices by hand in the UI at scale; **script from the source of
truth** for consistency.

**Cleanup:** `DELETE /api/v0/devices/192.0.2.10`.

### Lab 6.3 — Query active alerts

**Objective:** Pull current alerts for a pipeline.

```bash
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/alerts?state=1" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('active alerts:',d.get('count',0))"
```

**Expected result:** the count of **active alerts** — data to drive downstream
automation.

**Negative test:** poll the UI for alert state; the **API** exposes it for scripting.

**Cleanup:** none (read-only).

### Lab 6.4 — Ansible against the API

**Objective:** Add a device with an Ansible task.

```yaml
- hosts: localhost
  tasks:
    - name: add device to LibreNMS
      ansible.builtin.uri:
        url: "{{ lookup('env','LNMS') }}/api/v0/devices"
        method: POST
        headers: { X-Auth-Token: "{{ lookup('env','TOKEN') }}" }
        body_format: json
        body: { hostname: "192.0.2.20", version: "v2c", community: "public" }
        status_code: 200
```

**Expected result:** Ansible reporting the device added — LibreNMS in a playbook.

**Negative test:** manage monitoring by clicking; **codify** it in Ansible for
repeatability and review.

**Cleanup:** remove the device via the API.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The LibreNMS REST API (token-auth, `/api/v0/`) covers the full device/alert/inventory
lifecycle, so onboarding and querying are scriptable — from `curl` to Ansible, ideally
sourced from a source of truth. This chapter automated device lifecycle and alert
queries.

- [ ] I can authenticate and query the API.
- [ ] I can add and remove devices programmatically.
- [ ] I can pull active alerts for automation.
- [ ] I can drive LibreNMS from Ansible.
- [ ] I completed Labs 6.1–6.4 including each negative test.
