# Chapter 05: CC Admin - Edge — Nodes, Fleets, and Collection

## Learning Objectives

- Explain what the CC Admin - Edge certifies and its prerequisite.
- Deploy and manage Edge nodes.
- Organize nodes into fleets with hierarchical config.
- Collect data at the source and forward it.
- Complete a walkthrough for each Edge-admin topic.

## Theory and Architecture

The **Cribl Certified Admin - Edge (CC Admin - Edge)** validates implementing, managing,
and optimizing **Cribl Edge** — it requires **CC User**. **Edge** is a lightweight agent
deployed **at the data source** (hosts, containers, Kubernetes) to **collect** logs,
metrics, and host telemetry and forward them (often to Stream). Edge nodes are organized
into **Fleets** managed by a Leader, with **hierarchical configuration** (a subfleet
inherits and overrides parent config) so you manage thousands of nodes centrally.
Edge does light local processing and forwards; heavy processing happens in Stream.

## Design Considerations

Deploy **Edge** where the data is born (reducing the need for other agents), group nodes
into **Fleets** by role/environment, and use **hierarchical config** to set defaults at the
top and override per subfleet. Collect at the source and forward to **Stream** for heavy
processing.

## Implementation and Automation

The labs use Edge/fleet concepts and the API for nodes, fleets, and collection.

## Validation and Troubleshooting

Confirm the model:

```text
Edge: lightweight agent at the source -> collect (logs/metrics/host) -> forward (to Stream).
Fleets (Leader-managed) with hierarchical config (subfleet inherits/overrides). Light local processing.
```

Common pitfalls: heavy processing on Edge nodes (resource pressure); and flat fleets that
can't override per environment.

## Security and Best Practices

Collect **at the source** with Edge, organize into **Fleets** with **hierarchical config**,
keep node-side processing **light** (forward to Stream), and secure node↔Leader with TLS.
Monitor node health centrally.

## Hands-On Lab

Edge-admin walkthroughs. **Shared prerequisites** — a Cribl Edge/Leader (free tier);
`$CRIBL`/`$CRIBL_TOKEN`. **Cost:** none.

### Lab 5.1 — List Edge nodes

**Objective:** Enumerate managed Edge nodes.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "$CRIBL/api/v1/master/workers" \
  | python3 -c "import sys,json;print('edge nodes:',len(json.load(sys.stdin).get('items',[])))" 2>/dev/null \
  || echo "list nodes via the Leader / Manage Edge Nodes"
```

**Expected result:** the count of **Edge nodes** reporting to the Leader — the managed
fleet.

**Negative test:** manage nodes individually by hand; the **Leader** manages them centrally
— use it.

**Rollback:** none (read-only).

### Lab 5.2 — Organize a fleet

**Objective:** Group nodes into a fleet.

```text
# Fleets group Edge nodes; a subfleet inherits parent config and can override.
# Assign nodes to 'prod-linux' fleet; set defaults at parent, override at subfleet.
"fleet: prod-linux (inherits defaults) -> subfleet prod-linux-web (overrides)"
```

**Expected result:** a fleet with **hierarchical config** — centralized management with
per-group overrides.

**Negative test:** configure each node separately; **fleets + hierarchy** scale to
thousands.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Configure collection

**Objective:** Collect host logs/metrics at the source.

```json
{ "type": "file", "id": "app_logs", "path": "/var/log/app/*.log" }
```

**Expected result:** an Edge **file source** collecting app logs at the node — source-side
collection.

**Negative test:** ship raw files off-host to be parsed centrally; **collect + light-process
on Edge**, then forward.

**Rollback:** remove the source.

### Lab 5.4 — Forward to Stream

**Objective:** Send collected data to Stream.

```json
{ "type": "cribl_http", "id": "to_stream", "url": "https://stream-leader:10200" }
```

**Expected result:** an Edge **destination forwarding to Stream** — the collect-then-process
pattern.

**Negative test:** do heavy processing on the Edge node; **forward to Stream** for the heavy
lifting — keep Edge light.

**Rollback:** remove the destination.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CC Admin - Edge certifies managing Cribl Edge: lightweight source-side agents organized
into Leader-managed fleets with hierarchical config, collecting logs/metrics/host telemetry
and forwarding to Stream for heavy processing. This chapter listed nodes, organized a
fleet, and configured collection/forwarding.

- [ ] I can list and manage Edge nodes via the Leader.
- [ ] I can organize fleets with hierarchical config.
- [ ] I can configure source-side collection.
- [ ] I can forward collected data to Stream.
- [ ] I completed Labs 5.1–5.4 including each negative test.
