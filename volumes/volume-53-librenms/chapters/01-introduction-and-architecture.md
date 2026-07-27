# Chapter 01: Introduction and Architecture

## Learning Objectives

- Explain what LibreNMS is and where it fits in network operations.
- Describe the architecture: web, discovery, poller, database, and RRD.
- Stand up LibreNMS and validate the install.
- Authenticate to the REST API.
- Verify the running version.

## Theory and Architecture

**LibreNMS** is an open-source (GPL) **network monitoring system** — an
auto-discovering, **SNMP**-based platform that polls devices for metrics and state,
stores time-series data, graphs it, and alerts on it. It descends from Observium and is
community-driven with a **rolling (CalVer) release** (e.g., **26.7.0**). Where NetBox
(Volume LII) holds *intended* state, LibreNMS observes *actual* state — the two are
complementary.

Architecturally LibreNMS is a **PHP (Laravel)** application with several moving parts:
the **web UI/API**, the **discovery** process (finds devices and what they expose), the
**poller** (collects metrics on a schedule), a **MariaDB/MySQL** database (config and
state), **RRDtool/rrdcached** (time-series storage), and background services (alerting,
`snmptrapd`/syslog). At scale the poller distributes across nodes.

## Design Considerations

LibreNMS is **agentless** — it relies on **SNMP** (v2c/v3) and other standard protocols
on the devices, so device SNMP configuration is prerequisite. Run it as the operational
monitor alongside a source of truth; feed device lists from NetBox where possible.

## Implementation and Automation

Stand up LibreNMS with the community **`docker-librenms`** compose project, then use the
**`lnms`** CLI and the REST API:

```bash
git clone https://github.com/librenms/docker.git librenms-docker
cd librenms-docker/examples/compose && docker compose up -d
```

## Validation and Troubleshooting

Confirm the platform facts:

```text
LibreNMS:
  - open source (GPL); agentless SNMP-based monitoring
  - components: web/API, discovery, poller, MariaDB, RRDtool/rrdcached, trap/syslog
  - REST API under /api/v0/; X-Auth-Token header
  - rolling CalVer releases (e.g., 26.7.0)
  - validate.php checks install health
```

Common pitfalls: expecting agent installs (it is **SNMP**-based); and a stalled
**poller** (metrics stop) — check the poller/cron.

## Security and Best Practices

Use **SNMPv3** (auth + privacy) over v2c where possible, restrict SNMP by ACL, protect
**API tokens**, run behind TLS, and keep the poller healthy. Run `validate.php` after
changes.

## References and Knowledge Checks

- docs.librenms.org: installation, architecture, and the API.

**Knowledge checks**

1. How does LibreNMS collect data (agent vs agentless)?
2. Name the discovery and poller roles.
3. How does LibreNMS complement a source of truth like NetBox?

## Hands-On Lab

Setup and orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — Docker
with Compose; `curl`, `python3`. **Cost:** none.

### Lab 1.1 — Stand up LibreNMS

**Objective:** Run LibreNMS with the community Docker compose.

```bash
git clone https://github.com/librenms/docker.git librenms-docker
cd librenms-docker/examples/compose && docker compose up -d
docker compose ps --services --filter status=running | sort
```

**Expected result:** running services including **librenms**, **db** (MariaDB), and
**redis/dispatcher** — a working stack.

**Negative test:** start only the web container; without **db** and the **dispatcher/
poller** no metrics are collected — bring up the whole stack.

**Cleanup:** `docker compose down` (add `-v` to drop data).

### Lab 1.2 — Validate the install

**Objective:** Run the built-in health check.

```bash
docker compose exec librenms php validate.php | tail -20
```

**Expected result:** validation output ending in **OK** (or actionable warnings) — the
install-health check.

**Negative test:** skip `validate.php` and debug blind; it flags DB schema, cron, and
permission issues — run it first.

**Cleanup:** none.

### Lab 1.3 — Authenticate to the API

**Objective:** Create an API token and call the API.

```bash
# Create a token in the UI (Settings > API > API Settings), then:
export LNMS=http://localhost:8000 TOKEN=<your-token>
curl -sS -H "X-Auth-Token: $TOKEN" "$LNMS/api/v0/devices" \
  | python3 -c "import sys,json;print('devices:',json.load(sys.stdin).get('count',0))"
```

**Expected result:** an authenticated response with a **device count** (0 on a fresh
install) — proof the token works.

**Negative test:** call `/api/v0/devices` with no token; LibreNMS returns **401** —
authenticate first.

**Cleanup:** delete the token if it was only for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

LibreNMS is the open-source, agentless, SNMP-based network monitor — a Laravel app with
discovery, poller, MariaDB, and RRDtool components, plus a REST API. This chapter stood
it up, validated it, and authenticated to the API.

- [ ] I can explain agentless SNMP monitoring.
- [ ] I can name the discovery, poller, and storage components.
- [ ] I can run LibreNMS with Docker.
- [ ] I can validate the install and authenticate to the API.
- [ ] I completed Labs 1.1–1.3 including each negative test.
