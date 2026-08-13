# Chapter 04: Enterprise Admin and Cloud Admin

## Learning Objectives

- Explain the Admin credentials and their scope (Enterprise vs Cloud).
- Summarize the Enterprise Admin blueprint topic areas and weights.
- Apply administration: config files, indexes, users/auth, and getting data in.
- Manage forwarders and inputs at scale.
- Complete a per-topic walkthrough for each Admin topic area.

## Theory and Architecture

The **Enterprise Certified Admin** validates day-to-day administration of Splunk
Enterprise — components, licensing, **configuration files**, **indexes**, users
and authentication, **getting data in (GDI)**, distributed search, and
**forwarder management**. The **Cloud Certified Admin** covers the same operations
scoped to **Splunk Cloud** (where Splunk manages the infrastructure and the admin
manages data, inputs, and users). The Enterprise Admin blueprint weights ~17
topic areas, led by **Indexes**, **Distributed Search**, and **Forwarder
Management** at 10% each.

## Design Considerations

Admin is about **configuration and data flow**. Master the **configuration file**
model (directory structure, layering, precedence via `btool`), the **index**
lifecycle (buckets, retention), **roles and authentication** (LDAP/SAML), and the
**data pipeline** (input → parsing → indexing) with **forwarders** and the
**deployment server** managing them at scale. Know which duties differ on **Cloud**
(no OS/index-cluster management) vs **Enterprise**.

## Implementation and Automation

The labs below use Splunk **CLI/config** patterns for each Admin topic area —
components, config precedence, indexes, roles/auth, inputs, and forwarder
management — illustratively (adapt to your instance).

## Validation and Troubleshooting

Confirm the blueprint before studying:

```text
splunk.com > Enterprise Certified Admin > test blueprint:
  - ~17 topic areas; Indexes, Distributed Search, Forwarder Management 10% each
  - prerequisite: Power User; Cloud Admin covers the Splunk Cloud scope
```

Common pitfalls: editing the wrong **config layer** (use `btool` to see effective
settings); confusing **universal** vs **heavy** forwarders; and assuming Cloud
admins manage indexers (Splunk does, on Cloud).

## Security and Best Practices

Use **`btool`** to verify effective configuration before changing it; manage
forwarders centrally with the **deployment server**; scope **roles** to least
privilege; and monitor license usage and indexing. On Cloud, work within the
managed model (self-service inputs, roles, and apps).

## References and Knowledge Checks

- splunk.com: *Enterprise Admin* and *Cloud Admin* blueprints; Admin Manual; Distributed Deployment Manual.

**Knowledge checks**

1. Which three Enterprise Admin topics are weighted 10% each?
2. How do you determine the effective value of a configuration setting?
3. What administration duties differ between Splunk Cloud and Enterprise?

## Hands-On Lab

Per-topic walkthroughs — **one lab per Admin topic area** (consolidated). Commands
are illustrative Splunk CLI/config.

**Shared prerequisites** — a Splunk Enterprise instance (or trial) with CLI
access. **Cost:** none (trial).

### Lab 4.1 — Splunk components and license

**Objective:** Identify components and check licensing.

```bash
$SPLUNK_HOME/bin/splunk btool server list --debug 2>/dev/null | head
$SPLUNK_HOME/bin/splunk list licenser-pools 2>/dev/null || echo "(check License Manager in UI)"
```

**Expected result:** server settings and license pool info — the components and
license-management basics (blueprint topics 1–2).

**Negative test:** ignore license warnings; repeated violations restrict search —
monitor daily indexing volume.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Configuration files and precedence

**Objective:** Determine an effective setting with `btool`.

```bash
$SPLUNK_HOME/bin/splunk btool inputs list --debug 2>/dev/null | head
echo "Layering: system/default < app/default < app/local < system/local (local wins)."
```

**Expected result:** the effective `inputs.conf` settings with their source files —
config layering and precedence (a core Admin topic).

**Negative test:** edit `default/` files; edits belong in **`local/`** — `default/`
is overwritten on upgrade.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Indexes and buckets

**Objective:** Inspect an index and its bucket lifecycle.

```bash
$SPLUNK_HOME/bin/splunk list index 2>/dev/null | head
echo "Bucket lifecycle: hot -> warm -> cold -> frozen (deleted/archived) per retention."
```

**Expected result:** the indexes and the hot→warm→cold→frozen lifecycle — the
Indexes topic (10%, tied heaviest).

**Negative test:** set tiny retention and lose needed data; size **retention** to
requirements before ingesting.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Users, roles, and authentication

**Objective:** Create a least-privilege role and integrate auth.

```bash
$SPLUNK_HOME/bin/splunk add role analyst -srchIndexesAllowed _internal 2>/dev/null \
  || echo "(create role: limit indexes + capabilities)"
echo "Auth: integrate LDAP/SAML for enterprise identity; map groups to roles."
```

**Expected result:** a role limited to specific indexes and the auth-integration
concept — user and authentication management.

**Negative test:** give analysts the `admin` role; scope **roles** to least
privilege and map from directory groups.

**Rollback:** `$SPLUNK_HOME/bin/splunk remove role analyst 2>/dev/null || true`

### Lab 4.5 — Getting Data In and forwarders

**Objective:** Configure a monitor input and understand forwarder types.

```bash
cat <<'CONF'
# inputs.conf
[monitor:///var/log/app]
sourcetype = app_logs
index = app
CONF
echo "Universal Forwarder (lightweight, forwards) vs Heavy Forwarder (parses/routes)."
```

**Expected result:** a monitor input stanza and the forwarder-type distinction —
the GDI and forwarder basics.

**Negative test:** deploy heavy forwarders everywhere; the **universal forwarder**
is lightweight for most endpoints — use HF only where parsing/routing is needed.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — Forwarder management (deployment server)

**Objective:** Manage forwarders centrally with the deployment server.

```bash
echo "serverclass.conf maps deployment apps -> forwarder classes (by host/type)."
$SPLUNK_HOME/bin/splunk list deploy-clients 2>/dev/null | head || echo "(deployment server manages forwarder configs)"
```

**Expected result:** the deployment-server model (server classes distributing apps
to forwarders) — Forwarder Management (10%, tied heaviest).

**Negative test:** configure each forwarder by hand; the **deployment server**
manages them at scale — centralize.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.7 — Inputs: monitor, network, scripted, agentless

**Objective:** Distinguish input types.

```bash
cat <<'CONF'
[monitor:///var/log]          # file/dir
[tcp://514]                    # network (syslog)
[script://./bin/collect.sh]   # scripted
[http]                        # HTTP Event Collector (agentless)
CONF
```

**Expected result:** the input types (monitor, network, scripted, HEC/agentless) —
the several input topic areas consolidated.

**Negative test:** open a raw network port with no parsing plan; define
sourcetype/index and parsing for network inputs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.8 — Parsing phase and manipulating raw data

**Objective:** Configure line breaking and a transform.

```bash
cat <<'CONF'
# props.conf
[app_logs]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
# transforms.conf: route/mask via REGEX + DEST_KEY
CONF
```

**Expected result:** parsing configuration (line breaking, time extraction) and the
transform mechanism — the parsing/raw-data topics.

**Negative test:** rely on default line merging for multiline logs; set
`LINE_BREAKER`/`SHOULD_LINEMERGE` explicitly for correct event breaking.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Enterprise Admin certifies day-to-day Splunk administration — components,
licensing, config files and precedence, indexes and buckets, roles/auth, getting
data in, forwarders, the deployment server, inputs, and parsing — led by Indexes,
Distributed Search, and Forwarder Management (10% each). The Cloud Admin covers the
same in the managed Splunk Cloud scope.

- [ ] I can name the three 10% Enterprise Admin topics.
- [ ] I can use `btool` and edit the correct config layer.
- [ ] I can manage indexes, roles, inputs, and forwarders.
- [ ] I can configure parsing and central forwarder management.
- [ ] I completed Labs 4.1–4.8 including each negative test.
