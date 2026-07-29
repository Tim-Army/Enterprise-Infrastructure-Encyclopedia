# Chapter 09: Profiles and Keeping Current

## Learning Objectives

- Explain the profiles signal and its status.
- Track signal and component stability.
- Follow semantic-convention evolution safely.
- Track releases across the OTel components.
- Complete a walkthrough for each currency task.

## Theory and Architecture

OpenTelemetry adds **profiles** as a fourth signal — continuous CPU/memory profiling
carried through OTLP and the Collector, correlating resource usage with traces. Profiles
are newer than the stable traces/metrics/logs, so its API/SDK support varies by language
— check status before relying on it. OTel components **version independently**: the
**specification** (v1.59.0), the **Collector** (v0.157.0, still 0.x), per-language
**SDKs**, and **semantic conventions** (which reach stability per domain, sometimes with
migration from older names). Track each on its own GitHub releases.

## Design Considerations

Adopt **stable** signals first (traces/metrics/logs); treat **profiles** as emerging.
Watch **semantic-convention** changes — attribute renames ship with a migration period,
so pin conventions and migrate deliberately. Don't assume the Collector's 0.x versioning
means instability — it is production-used, but read release notes.

## Implementation and Automation

The labs check signal status, convention versions, and component releases.

## Validation and Troubleshooting

Confirm the currency model:

```text
Signals: traces/metrics/logs stable; profiles emerging (check per-language status).
Independent versions: spec (1.x), Collector (0.x), SDKs, semantic conventions.
Semantic conventions stabilize per domain; renames have migration windows.
```

Common pitfalls: relying on **profiles** where the SDK is experimental; and breaking
dashboards on a **convention rename**.

## Security and Best Practices

Build on **stable** signals, monitor **semantic-convention** changes and migrate on your
schedule, keep **SDK/Collector/instrumentation** versions aligned, and read release notes
before upgrading. Track the components you actually run.

## Hands-On Lab

Currency walkthroughs. **Shared prerequisites** — a shell with `curl`, `python3`.
**Cost:** none.

### Lab 9.1 — Check the Collector release

**Objective:** Read the latest Collector version.

```bash
curl -sS "https://api.github.com/repos/open-telemetry/opentelemetry-collector/releases/latest" \
  | python3 -c "import sys,json;print('collector:',json.load(sys.stdin)['tag_name'])"
```

**Expected result:** the latest Collector tag (a **0.15x.x** release) — the component to
track.

**Negative test:** assume the Collector shares the spec's 1.x version; components version
**independently** — check each.

**Cleanup:** none.

### Lab 9.2 — Check the specification release

**Objective:** Read the current spec version.

```bash
curl -sS "https://api.github.com/repos/open-telemetry/opentelemetry-specification/releases/latest" \
  | python3 -c "import sys,json;print('spec:',json.load(sys.stdin)['tag_name'])"
```

**Expected result:** the current spec tag (a **1.x** release) — the standard's version.

**Negative test:** treat the spec and Collector as one version; they differ — track both.

**Cleanup:** none.

### Lab 9.3 — Confirm signal stability

**Objective:** State which signals are stable.

```bash
python3 - <<'PY'
status={"traces":"stable","metrics":"stable","logs":"stable","profiles":"development/experimental"}
for sig,st in status.items(): print(f"{sig:9}: {st}")
PY
```

**Expected result:** traces/metrics/logs **stable**, profiles **emerging** — what to rely
on today.

**Negative test:** build a product hard-dependency on **profiles**; confirm the
per-language **status** first — it is newer.

**Cleanup:** none.

### Lab 9.4 — Plan a semantic-convention migration

**Objective:** Handle a convention rename safely.

```text
# Older http.method -> newer http.request.method (stabilized).
# During migration, emit both or gate on OTEL_SEMCONV_STABILITY_OPT_IN; update dashboards; then drop the old name.
"migration: dual-emit -> update consumers -> remove legacy attribute"
```

**Expected result:** a safe **dual-emit → migrate → drop** plan — no broken dashboards on
a rename.

**Negative test:** rename attributes in one step; **downstream dashboards/alerts break** —
migrate in phases.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OpenTelemetry keeps evolving: profiles join traces/metrics/logs as a fourth (emerging)
signal, components version independently (spec 1.x, Collector 0.x), and semantic
conventions stabilize per domain with migration windows. This chapter checked releases,
signal status, and a convention migration.

- [ ] I can explain the profiles signal and its status.
- [ ] I can track independent component versions.
- [ ] I can state which signals are stable.
- [ ] I can plan a semantic-convention migration.
- [ ] I completed Labs 9.1–9.4 including each negative test.
