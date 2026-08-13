# Chapter 01: The Cribl Certification Program

## Learning Objectives

- Describe Cribl and its observability-pipeline products.
- Identify the certification ladder and levels.
- Explain delivery, validity, and prerequisites.
- Access the Cribl REST API and expression syntax used in this volume.
- Verify program facts from the authoritative source.

## Theory and Architecture

**Cribl** builds an **observability data pipeline** that sits between your data sources and
your analytics/storage destinations, letting you **route, reduce, enrich, and replay**
telemetry (logs, metrics, traces) — controlling cost and getting the right data to the
right place. Its products: **Stream** (the core routing/processing engine), **Edge** (a
lightweight agent for collection at the source), **Search** (query data in place, without
moving it), and **Lake** (low-cost storage with replay). **Cribl University** runs a free
certification program that validates these skills.

This is a **certification-tracks** volume, like the other vendor volumes: it maps the
program — which credentials exist, their topic areas, and levels — and teaches each with a
hands-on walkthrough. The ladder:

- **Level 1 — CC User:** foundation across all products.
- **Level 2 — CC Admin - Stream** and **CC Admin - Edge:** product-deep administration.
- **Level 3 — CC Engineer:** solution design and optimization across products.
- **Level 4 — CCSC (Cribl Certified Service Consultant):** partner deployment readiness.

Every credential was **verified against cribl.io/university on 27 July 2026**. The
certifications are **free**, delivered as **online self-study** through Cribl University,
and **valid three years**.

## Design Considerations

Progress by level: **CC User** first (required for the Admin certs), then **Admin - Stream**
and/or **Admin - Edge**, then **CC Engineer** (requires the Admin certs), and **CCSC** for
partners. Practice on the **Cribl free tier / Cribl.Cloud** so labs are reproducible.

## Implementation and Automation

Labs use **Cribl Stream configuration** (pipelines/routes as specs), the **Cribl REST
API**, and Cribl's **expression syntax** (JavaScript-based). Confirm access:

```bash
# Cribl REST API (Bearer token from the UI/API):
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "https://<leader>/api/v1/system/info" | head
```

## Validation and Troubleshooting

Confirm the program facts:

```text
cribl.io/university:
  - ladder: CC User -> CC Admin (Stream / Edge) -> CC Engineer -> CCSC (partner)
  - products: Stream, Edge, Search, Lake
  - free; online self-study; valid 3 years; Admin certs require CC User
```

Common pitfalls: attempting an **Admin** cert before **CC User**; and confusing **Stream**
(processing) with **Edge** (collection).

## Security and Best Practices

Study the topic areas for your target level, practice on the **free tier**, treat Cribl
access as privileged (RBAC, API tokens over TLS), and progress **User → Admin → Engineer**.
Recertify within the three-year window.

## References and Knowledge Checks

- cribl.io/university and university.cribl.io: the certification catalog and courses.

**Knowledge checks**

1. What does a Cribl observability pipeline do?
2. Name the four products and the certification ladder.
3. What is the prerequisite for the Admin certifications?

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with
`curl`; a Cribl Stream instance (free tier/Cloud) with an API token for the API checks.
**Cost:** none.

### Lab 1.1 — Enumerate the certification ladder

**Objective:** State the program structure.

```bash
python3 - <<'PY'
ladder={"Level 1":"CC User","Level 2":"CC Admin - Stream / CC Admin - Edge",
        "Level 3":"CC Engineer","Level 4":"CCSC (partner)"}
for lvl,cert in ladder.items(): print(f"{lvl}: {cert}")
PY
```

**Expected result:** the four levels mapped to their certifications — the program ladder.

**Negative test:** rely on a stale cert list; Cribl revises the program — confirm on
cribl.io/university.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Authenticate to the Cribl API

**Objective:** Confirm API access to a Stream leader.

```bash
curl -sS -H "Authorization: Bearer $CRIBL_TOKEN" "https://<leader>/api/v1/system/info" \
  | python3 -c "import sys,json;print('cribl version:',json.load(sys.stdin).get('items',[{}])[0].get('version','?'))" 2>/dev/null \
  || echo "check token / leader URL"
```

**Expected result:** the Cribl **version** — proof API access works (the basis for later
labs).

**Negative test:** call the API with no token; Cribl returns **401** — authenticate first.

**Rollback:** none (read-only).

### Lab 1.3 — Identify the product each cert covers

**Objective:** Map certs to products.

```bash
python3 - <<'PY'
m={"CC User":"Stream/Edge/Search/Lake (foundation)","CC Admin - Stream":"Stream",
   "CC Admin - Edge":"Edge","CC Engineer":"all (design/optimize)","CCSC":"all (deploy)"}
for c,p in m.items(): print(f"{c:18}: {p}")
PY
```

**Expected result:** each cert mapped to its product focus — choosing the right path.

**Negative test:** assume one Admin cert covers both Stream and Edge; they are **separate**
— pick per product.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cribl builds an observability pipeline (Stream, Edge, Search, Lake), and Cribl University
runs a free, three-year-valid certification ladder — CC User → CC Admin (Stream/Edge) → CC
Engineer → CCSC. This volume teaches each with hands-on Cribl config and API work.

- [ ] I can describe Cribl's products and pipeline role.
- [ ] I can name the certification ladder and levels.
- [ ] I can authenticate to the Cribl API.
- [ ] I can map each certification to its product focus.
- [ ] I completed Labs 1.1–1.3 including each negative test.
