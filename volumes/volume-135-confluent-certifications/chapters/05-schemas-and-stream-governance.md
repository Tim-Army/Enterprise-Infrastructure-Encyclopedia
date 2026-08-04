# Chapter 05: Schemas and Stream Governance

## Learning Objectives

- Explain Schema Registry and how schema IDs travel with records.
- Choose between Avro, Protobuf, and JSON Schema.
- Apply compatibility modes and evolve schemas without breaking consumers.
- Describe Stream Governance beyond schemas: lineage, catalog, and quality.

## The problem schemas solve

Kafka stores bytes. Without a shared contract, every consumer must guess the producer's format, and any producer change silently breaks every downstream consumer — the failure mode that makes event streaming unmanageable at scale.

**Schema Registry** (a Confluent component, not part of Apache Kafka) holds versioned schemas centrally. Producers register a schema and prepend its **schema ID** to each record; consumers read the ID and fetch the schema to deserialize. The payload carries an ID, not the full schema, so the overhead is a few bytes.

The registry organizes schemas into **subjects**, conventionally `<topic>-value` and `<topic>-key`, each with its own version history and compatibility setting.

## Formats

| Format | Strengths | Trade-offs |
|:---|:---|:---|
| **Avro** | Compact binary; rich schema evolution; the Kafka-ecosystem default | Requires the registry to read data |
| **Protobuf** | Compact; strong cross-language tooling; familiar in gRPC shops | Different evolution rules from Avro |
| **JSON Schema** | Human-readable; easy debugging and adoption | Verbose on the wire; weaker typing |

## Compatibility modes

This is the exam-critical material, and the direction of each check is what people get wrong:

| Mode | Guarantees | Practical meaning |
|:---|:---|:---|
| **BACKWARD** (default) | New schema can read data written with the previous schema | **Upgrade consumers first** |
| **FORWARD** | Previous schema can read data written with the new schema | **Upgrade producers first** |
| **FULL** | Both directions | Upgrade in any order |
| **NONE** | No checking | You are on your own |
| **\*_TRANSITIVE** | The same check against **all** previous versions, not just the last | Stronger; needed when old data is replayed |

The transitive variants matter more in Kafka than in most systems, precisely because the log is **replayable**: a consumer reading from the beginning of a two-year retention encounters every historical version, so compatibility only with the immediately preceding version is not enough.

### The safe-change rules (BACKWARD)

- **Adding a field with a default** is safe: old data lacks it, the default fills in.
- **Adding a field without a default** breaks: the new schema cannot read old records.
- **Removing a field** that had no default breaks consumers still expecting it.
- **Renaming** is a remove plus an add — usually breaking; use aliases where the format supports them.
- **Changing a type** is generally breaking, except for defined promotions (`int` → `long`).

## Stream Governance

Confluent's **Stream Governance** (examined on CCAC) extends beyond schemas:

- **Schema Registry** — the contracts above.
- **Stream Catalog** — discovery and metadata: what topics exist, who owns them, what they contain.
- **Stream Lineage** — a visual graph of how data flows producer → topic → processor → sink, which is how you answer "if I change this topic, what breaks?"
- **Data quality rules** — validation on the stream itself.

## Hands-On Lab

Python models schema governance. **Cost:** none.

### Lab 5.1 — Schema Registry and the wire format

**Objective:** Model registration, ID embedding, and deserialization.

```bash
python3 - <<'EOF'
registry, next_id = {}, [1]
def register(subject, schema):
    for sid, (subj, sch) in registry.items():
        if subj == subject and sch == schema: return sid
    sid = next_id[0]; next_id[0] += 1
    registry[sid] = (subject, schema); return sid

schema_v1 = {"type":"record","name":"Order","fields":[{"name":"id","type":"string"},{"name":"total","type":"double"}]}
sid = register("orders-value", schema_v1)

def produce(payload, schema_id):   # magic byte + 4-byte schema id + payload
    return {"magic":0, "schema_id":schema_id, "payload":payload}
def consume(record):
    subj, sch = registry[record["schema_id"]]
    fields = [f["name"] for f in sch["fields"]]
    return f"decoded with {subj} v(id={record['schema_id']}) fields={fields} -> {record['payload']}"

rec = produce({"id":"o-1","total":42.5}, sid)
print(f"registered schema id: {sid}")
print(f"wire record: {rec}")
print(consume(rec))
print("\nThe record carries a 5-byte header (magic + schema id), not the schema itself.")
print("Consumers resolve the ID against the registry — which is why the registry is a")
print("hard runtime dependency for deserialization, and must be sized and monitored as one.")
EOF
```

**Expected result:** A schema registers once and returns an ID; records carry only that ID; consumers resolve it to deserialize. The closing point is operationally important and often missed: **Schema Registry is on the critical path for consumption**, so its availability matters as much as the brokers'.

**Negative test:** Embedding the full schema in every record — correctness is fine and the bandwidth cost is enormous, which is exactly the waste the registry exists to remove.

**Cleanup:** None.

### Lab 5.2 — Compatibility checking

**Objective:** Test schema evolution against BACKWARD compatibility.

```bash
python3 - <<'EOF'
def fields(schema): return {f["name"]: f for f in schema["fields"]}

def backward_compatible(old, new):
    """New schema must be able to read data written with the OLD schema."""
    problems = []
    o, n = fields(old), fields(new)
    for name, f in n.items():
        if name not in o and "default" not in f:
            problems.append(f"added field '{name}' WITHOUT a default — cannot read old records")
    for name, f in o.items():
        if name not in n:
            problems.append(f"removed field '{name}' — new schema drops data old records carry")
        elif o[name]["type"] != n[name]["type"]:
            promotion = (o[name]["type"], n[name]["type"]) in {("int","long"),("float","double")}
            problems.append(f"changed type of '{name}': {o[name]['type']} -> {n[name]['type']}"
                            + (" (allowed promotion)" if promotion else " — BREAKING"))
    return problems

v1 = {"fields":[{"name":"id","type":"string"},{"name":"total","type":"double"}]}
candidates = {
  "add field WITH default":    {"fields":[{"name":"id","type":"string"},{"name":"total","type":"double"},{"name":"currency","type":"string","default":"USD"}]},
  "add field WITHOUT default": {"fields":[{"name":"id","type":"string"},{"name":"total","type":"double"},{"name":"region","type":"string"}]},
  "remove a field":            {"fields":[{"name":"id","type":"string"}]},
  "change type string->int":   {"fields":[{"name":"id","type":"int"},{"name":"total","type":"double"}]},
}
for name, v2 in candidates.items():
    issues = backward_compatible(v1, v2)
    print(f"{name:28} -> {'COMPATIBLE' if not issues else 'REJECTED'}")
    for i in issues: print(f"{'':30} {i}")
EOF
```

**Expected result:** Only "add field with default" passes; the other three are rejected with specific reasons. The default is what makes an added field safe — it gives the new schema something to supply when reading old records that lack the field. Internalize that one rule and most evolution questions answer themselves.

**Negative test:** Setting compatibility to NONE to ship a breaking change quickly — the registry stops protecting you, and consumers fail at deserialization in production, usually at replay time rather than immediately.

**Cleanup:** None.

### Lab 5.3 — Choose a compatibility mode and upgrade order

**Objective:** Match the mode to who you can upgrade first.

```bash
python3 - <<'EOF'
MODES = {
  "BACKWARD":  ("new schema reads OLD data",   "upgrade CONSUMERS first", "default; most common"),
  "FORWARD":   ("old schema reads NEW data",   "upgrade PRODUCERS first", "when consumers are many/slow to change"),
  "FULL":      ("both directions",             "any order",               "safest, most restrictive"),
  "NONE":      ("no checks",                   "no guarantees",           "avoid"),
}
print(f"{'mode':10}{'guarantee':28}{'upgrade order':28}note")
for m,(g,o,n) in MODES.items():
    print(f"{m:10}{g:28}{o:28}{n}")

def recommend(can_upgrade_consumers_first, replays_old_data):
    base = "BACKWARD" if can_upgrade_consumers_first else "FORWARD"
    return base + ("_TRANSITIVE  (log is replayed, so ALL prior versions must stay readable)" if replays_old_data else "")

print()
for c, r in [(True, False), (True, True), (False, False), (False, True)]:
    print(f"consumers-first={str(c):5} replays-old-data={str(r):5} -> {recommend(c, r)}")
print("\nTRANSITIVE matters in Kafka specifically because the log is REPLAYABLE: a consumer")
print("reading from the earliest offset meets every historical schema version, not just the last.")
EOF
```

**Expected result:** The mode follows from which side you can upgrade first, and the transitive variant is recommended whenever old data gets replayed. That replay caveat is the Kafka-specific twist — in a request/response system, compatibility with the previous version suffices; in a replayable log with long retention, it does not.

**Negative test:** Using plain BACKWARD with two-year retention and then replaying from the beginning — consumers hit schema versions from eighteen months ago that were never checked against the current one, and deserialization fails mid-replay.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Schema Registry's wire format (schema ID, not schema) and runtime criticality understood.
- [ ] Avro, Protobuf, and JSON Schema compared.
- [ ] Compatibility modes applied, with defaults as the key to safe field addition.
- [ ] Transitive compatibility justified by the replayable log.
- [ ] Stream Governance placed: registry, catalog, lineage, and quality rules.
