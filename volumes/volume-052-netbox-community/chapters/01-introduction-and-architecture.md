# Chapter 01: Introduction and Architecture

## Learning Objectives

- Explain what NetBox is and its role as a network source of truth.
- Distinguish NetBox Community from NetBox Cloud/Enterprise.
- Describe the architecture (Django, PostgreSQL, Redis) and data model.
- Stand up NetBox Community with `netbox-docker` and authenticate to the API.
- Verify the running version.

## Theory and Architecture

**NetBox** is the open-source **network source of truth (NSoT)** — a single,
authoritative data model for IP address management (**IPAM**), data-center
infrastructure (**DCIM**), circuits, virtualization, cabling, and tenancy, exposed
through a rich **REST** and **GraphQL** API to power automation. **NetBox Community**
is the free, Apache-2.0 edition (the same core as the paid **NetBox Cloud/Enterprise**
from NetBox Labs, without the managed hosting and proprietary add-ons). This volume
targets the **4.6.x** series.

Architecturally NetBox is a **Django** application backed by **PostgreSQL** (the data)
and **Redis** (caching and task queues), served by **gunicorn** behind a web server,
with background workers (`rq`) for jobs. Everything in the UI is also available through
the API — the API *is* the product for automation.

## Design Considerations

NetBox is a **source of truth**, not a monitoring or discovery tool: it holds the
**intended** state you drive automation from, not live telemetry. Model your network in
NetBox, then let automation reconcile devices to it. Run **Community** for self-hosted
control; choose Cloud/Enterprise for managed hosting and support.

## Implementation and Automation

Stand up NetBox with the community **`netbox-docker`** project, then talk to it via
`pynetbox` or `curl`:

```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker && docker compose pull && docker compose up -d
```

## Validation and Troubleshooting

Confirm the platform facts:

```text
NetBox Community:
  - open source (Apache 2.0); source of truth for IPAM + DCIM + more
  - stack: Django + PostgreSQL + Redis + gunicorn + rq workers
  - REST API (/api/) and GraphQL API (/graphql/); token auth
  - current series 4.6.x
```

Common pitfalls: treating NetBox as a discovery/monitoring tool (it is
intended-state); and forgetting Redis/worker containers (background jobs stall).

## Security and Best Practices

Protect the **API token** (least-privilege tokens, expiry), run behind TLS, back up
**PostgreSQL**, and keep the stack current. Model intended state and reconcile with
automation rather than hand-editing devices.

## References and Knowledge Checks

- docs.netbox.dev: installation, architecture, and the REST/GraphQL APIs.

**Knowledge checks**

1. Why is NetBox a "source of truth" rather than a monitoring tool?
2. What backs NetBox (data store and cache/queue)?
3. How does Community differ from Cloud/Enterprise?

## Hands-On Lab

Setup and orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** —
Docker + Docker Compose; `curl` and `python3` (`pip install pynetbox`). **Cost:** none.

### Lab 1.1 — Stand up NetBox Community

**Objective:** Run NetBox locally with `netbox-docker`.

```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker && docker compose up -d
docker compose ps --services --filter status=running | sort
```

**Expected result:** running services including **netbox**, **postgres**, and
**redis** — a working NetBox stack.

**Negative test:** start only the `netbox` container; without **postgres/redis** it
fails to serve — bring up the whole compose stack.

**Rollback:** `docker compose down` (add `-v` to drop volumes).

### Lab 1.2 — Verify the running version

**Objective:** Read the NetBox version from the API status endpoint.

```bash
curl -sS "http://localhost:8000/api/status/" | python3 -c "import sys,json;print('netbox-version:',json.load(sys.stdin)['netbox-version'])"
```

**Expected result:** a **4.6.x** version string — confirming the running release.

**Negative test:** assume the latest; **query `/api/status/`** — the running version
governs which features/fields exist.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Authenticate to the API

**Objective:** Create a token and make an authenticated call.

```bash
# Create a token in the UI (Admin > API Tokens) or via the API, then:
export NB=http://localhost:8000 TOKEN=<your-token>
curl -sS -H "Authorization: Token $TOKEN" "$NB/api/dcim/sites/" \
  | python3 -c "import sys,json;print('sites:',json.load(sys.stdin)['count'])"
```

**Expected result:** an authenticated response with a **site count** (0 on a fresh
install) — proof the token works.

**Negative test:** call `/api/dcim/sites/` with no token; NetBox returns **403** for
protected data — authenticate first.

**Rollback:** delete the token if it was only for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NetBox Community is the open-source network source of truth for IPAM, DCIM, and more —
a Django/PostgreSQL/Redis application whose REST and GraphQL APIs power automation
against intended state. This chapter stood up NetBox with `netbox-docker` and
authenticated to the API.

- [ ] I can explain NetBox as a source of truth.
- [ ] I can describe the architecture and Community vs Cloud/Enterprise.
- [ ] I can run NetBox with `netbox-docker`.
- [ ] I can verify the version and authenticate to the API.
- [ ] I completed Labs 1.1–1.3 including each negative test.
