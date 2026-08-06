# Chapter 04: Designing APIs

## Learning Objectives

- Explain API-first / design-first development.
- Describe API specifications — RAML and OpenAPI (OAS).
- Understand Design Center and Anypoint Exchange.
- Recognize reuse and discoverability as the payoff.

*Cert relevance: API design (specs, Design Center, Exchange) is a core certification domain.*

## API-first / design-first

MuleSoft champions **API-first** (design-first) development: **design the API contract before implementing it.** Rather than building an integration and letting its interface emerge, you first define **what the API looks like** — its endpoints, request/response shapes, and behavior — as a formal **specification**, agree on it with consumers, and *then* implement it. The benefits are large: consumers can start building against the contract immediately (using **mocks**), the interface is stable and deliberate, and the specification becomes the single source of truth. API-first is the foundation of a well-designed application network. The lab models the approach.

## API specifications: RAML and OAS

An API **specification** is a machine-readable contract describing the API. MuleSoft supports two standards:

- **RAML (RESTful API Modeling Language)** — MuleSoft's originated, human-friendly YAML-based spec language, strong for **modular, reusable** API design (fragments, data types, traits).
- **OAS (OpenAPI Specification)** — the industry-standard spec (formerly Swagger), widely supported across tools.

A spec defines **resources** (endpoints), **methods** (GET/POST/...), **request/response schemas**, and **examples** — everything a consumer needs to understand and call the API without reading the implementation. From a spec, Anypoint can generate **mocks**, **documentation**, and **implementation skeletons**. The lab models a spec.

## Design Center and Anypoint Exchange

Two platform components support design and reuse:

- **Design Center** — the environment for **authoring** API specifications (RAML/OAS) and flows, with a built-in **mocking service** so a spec can be tested and consumed before any code exists.
- **Anypoint Exchange** — the **catalog/marketplace** where APIs, connectors, templates, and reusable **fragments** are **published and discovered**. Exchange is where the application network becomes **findable**: a team searching for "customer data" finds the existing System API and reuses it, rather than building a new one.

Together they close the loop from **designing** an API to **publishing** it for reuse. The lab models discovery.

## Reuse and discoverability

The payoff of good API design plus Exchange is **reuse** — the entire point of the [application network (Ch 2)](02-api-led-connectivity.md). When APIs are designed to a clear contract and published to a discoverable catalog, teams **find and compose** them instead of rebuilding, and each well-designed API accelerates future projects. Discoverability turns a collection of APIs into a **reusable asset library**; without it, APIs are built and forgotten, and the point-to-point problem creeps back. Designing for reuse and publishing for discovery is what makes the application network compound. The lab synthesizes.

## Hands-On Lab

Python models an API spec and reuse via Exchange. **Cost:** none.

### Lab 4.1 — Design-first specs and reuse through Exchange

**Objective:** See a spec-driven mock and discovery-driven reuse.

```bash
python3 - <<'EOF'
# an API specification (RAML/OAS-style) authored design-FIRST, before implementation
spec = {
  "api": "Customers System API", "spec_lang": "RAML",
  "resources": {
    "GET /customers/{id}": {"response": {"id": "int", "name": "string", "tier": "string"}},
    "GET /customers":      {"response": "[customer]"},
  },
}
print("DESIGN-FIRST: author the API spec BEFORE implementing:\n")
print(f"   {spec['api']} ({spec['spec_lang']}):")
for res, d in spec["resources"].items():
    print(f"      {res:22} -> {d['response']}")
# a spec enables a MOCK immediately (consumers build against it before code exists)
def mock(resource):
    return spec["resources"].get(resource, {}).get("response")
print(f"\n   MOCK (from spec, no code yet): GET /customers/42 -> {mock('GET /customers/{id}')}")
print("   -> consumers start building NOW against the stable contract\n")

# Anypoint Exchange: reuse via discovery instead of rebuild
EXCHANGE = {"Customers System API": "published, reused by 6 projects",
            "Orders System API": "published, reused by 4 projects"}
print("ANYPOINT EXCHANGE — discover + REUSE (vs rebuild):")
need = "customer data"
found = "Customers System API"
print(f"   team needs '{need}' -> searches Exchange -> finds '{found}' -> REUSES it")
print(f"   ({EXCHANGE[found]}) — no new integration built\n")
print("API-FIRST = design the CONTRACT (RAML/OAS spec) before code: consumers build against")
print("a MOCK immediately, the interface is stable + deliberate, the spec is the source of")
print("truth. DESIGN CENTER authors specs (+ mocking); ANYPOINT EXCHANGE publishes them so")
print("teams DISCOVER + REUSE instead of rebuilding. Reuse + discoverability = the payoff that")
print("makes the application network COMPOUND (Ch 2). Without it, point-to-point creeps back.")
EOF
```

**Expected result:** A design-first RAML spec for a Customers System API enabling an immediate mock (consumers build before code exists), and a team discovering and reusing that published API via Anypoint Exchange instead of rebuilding. The API-design lesson is that API-first defines a stable contract up front (mockable, the source of truth), Design Center authors specs, and Exchange makes them discoverable for reuse — the payoff that makes the application network compound.

**Negative test:** Building the integration first and letting the interface emerge, with no catalog. Consumers wait for code, the interface is accidental, and APIs are forgotten rather than reused; API-first specs plus Exchange discovery deliver a stable contract and genuine reuse.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] API-first / design-first understood — define the contract before implementing.
- [ ] API specifications understood — RAML and OAS (OpenAPI) as machine-readable contracts.
- [ ] Design Center and Anypoint Exchange understood — authoring specs (with mocks) and publishing for discovery.
- [ ] Reuse and discoverability recognized as the payoff that makes the application network compound.
