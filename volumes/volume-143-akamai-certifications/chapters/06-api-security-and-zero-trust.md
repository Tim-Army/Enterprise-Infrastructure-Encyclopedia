# Chapter 06: API Security and Zero Trust

## Learning Objectives

- Explain API Security's discover → posture → runtime model (the Noname lineage).
- Distinguish API Security from the WAF's API protections — they are complementary layers.
- Map Akamai's Zero Trust portfolio: Enterprise Application Access, Secure Internet Access, MFA.
- Place Akamai's north-south zero trust beside Guardicore's east-west segmentation (Chapter 07).

*Course/cert relevance: **Akamai API Security – Architect** (Advanced-level credential), **Akamai Zero Trust Solutions** course, and the Enterprise Application Access / Secure Internet Access / MFA Certified Partner Solutions Architect specializations. **Defensive** throughout.*

## API Security: discover, posture, runtime

Akamai's dedicated **API Security** product (from the Noname acquisition) addresses what a WAF structurally cannot: the WAF inspects requests to APIs it is configured for; API Security **finds the APIs first**. Its model has three stages that build on each other:

| Stage | Question | Failure it prevents |
|:---|:---|:---|
| **Discovery** | What APIs actually exist, including undocumented ones? | The shadow/zombie API nobody protects because nobody knew it was there |
| **Posture** | Are they configured safely — auth, exposure, sensitive-data handling? | The API that works and leaks (weak auth, PII in responses) |
| **Runtime** | Is anything abusing them right now? | The business-logic attack that each request passes but the sequence does not |

The discovery stage is the same lesson as [Cloudflare's API Shield chapter](../../volume-142-cloudflare-certifications/chapters/04-ddos-bots-and-api-shield.md) and the shadow-endpoint audit, stated as a product's first stage: **you cannot secure, validate, or even inventory an API you do not know exists**, and discovery is therefore the precondition for everything after it.

### API Security is not the WAF

A common enterprise confusion the Architect credential exists to clear: **App & API Protector (Chapter 04) and API Security are different layers.** AAP applies request-level protections (injection, bots, rate limits) to traffic. API Security provides the *inventory, posture, and behavioral* layer — it knows your API estate as a set of specifications and normal behaviors, and catches the business-logic and posture problems that look like valid requests one at a time. You run both; they answer different questions.

## The Zero Trust portfolio

Akamai's north-south zero trust (user-to-application) is a portfolio, not a single product:

| Product | Role | Cloudflare/Zscaler analog |
|:---|:---|:---|
| **Enterprise Application Access (EAA)** | ZTNA — per-application access without network exposure | Cloudflare Access, Zscaler ZPA |
| **Secure Internet Access (SIA)** | SWG — egress filtering, formerly Enterprise Threat Protector | Cloudflare Gateway, Zscaler ZIA |
| **Akamai MFA** | Phishing-resistant multifactor | — |

The models map cleanly onto [Volume CXLII](../../volume-142-cloudflare-certifications/chapters/05-zero-trust-access.md) and [Volume XXXV (Zscaler)](../../volume-035-zscaler-zero-trust-exchange/README.md): EAA is per-application access replacing VPN, SIA is filtered egress, and the blast-radius arithmetic from those volumes transfers unchanged. What Akamai adds to the comparison is that this same vendor *also* sells the east-west half — Guardicore segmentation (Chapter 07) — so an Akamai estate can run both halves of zero trust under one roof, which is the volume's Chapter 07 hand-off.

## Hands-On Lab

Python models API security. **Cost:** none. Defensive throughout.

### Lab 6.1 — Discover, posture, runtime as a funnel

**Objective:** Show why the three stages must run in order.

```bash
python3 - <<'EOF'
DISCOVERED = {
  # api,                    documented, auth,        exposes_pii, behavior
  "/api/v2/orders":         (True,  "oauth",        False, "normal"),
  "/api/v2/users":          (True,  "oauth",        True,  "normal"),
  "/api/v1/orders":         (False, "api-key",      False, "normal"),       # zombie version
  "/internal/reports":      (False, "none",         True,  "normal"),       # shadow + no auth + PII
  "/api/v2/orders/export":  (True,  "oauth",        True,  "10x normal enumeration"),  # runtime abuse
}
print("STAGE 1 — DISCOVERY (what actually receives traffic):")
undocumented_apis = [a for a, m in DISCOVERED.items() if not m[0]]
print(f"   {len(DISCOVERED)} APIs live; {len(undocumented_apis)} undocumented: {', '.join(undocumented_apis)}")
print("   -> you cannot posture-check or monitor what you have not discovered.\n")

print("STAGE 2 — POSTURE (are the discovered APIs safe as configured?):")
for a, (doc, auth, pii, beh) in DISCOVERED.items():
    problems = []
    if auth == "none": problems.append("NO AUTH")
    if auth == "api-key": problems.append("weak auth (api-key)")
    if pii and auth != "oauth": problems.append("PII behind weak/no auth")
    if problems: print(f"   {a:26} {', '.join(problems)}")
print("   -> /internal/reports: no auth, exposes PII, undocumented. Fix before anything else.\n")

print("STAGE 3 — RUNTIME (is anything abusing the safe-looking ones?):")
for a, (doc, auth, pii, beh) in DISCOVERED.items():
    if beh != "normal":
        print(f"   {a:26} {beh} — each request is VALID; the SEQUENCE is exfiltration")
print("   -> /orders/export: correct auth, correct requests, 10x enumeration = data theft")
print("      by a legitimate client. No single request is an attack. Only runtime sees it.")
print("\nThe order is not optional: discover (or you protect a subset), posture (or you")
print("monitor known-bad configs), runtime (or you miss valid-but-abusive sequences).")
EOF
```

**Expected result:** Two undocumented APIs surface at discovery, an unauthenticated PII endpoint at posture, and a valid-but-abusive export at runtime — each stage catching what the others cannot. The strict ordering is the content: skipping discovery means posture and runtime cover only the known subset, which is exactly the subset that was never the problem.

**Negative test:** Buying runtime monitoring without discovery. It watches the documented APIs beautifully while `/internal/reports` leaks PII unmonitored.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — API Security versus the WAF, on one request stream

**Objective:** Show the two layers catching different things.

```bash
python3 - <<'EOF'
REQUESTS = [
  # description,                        waf_verdict,      api_sec
  ("SQLi payload in a query param",     "BLOCK (injection)", "pass (looks normal to behavior)"),
  ("valid login, 500/min from one key", "pass (each valid)", "FLAG (velocity anomaly)"),
  ("request to undocumented /api/v1",   "pass (no rule)",    "FLAG (shadow API)"),
  ("auth token for user A reads user B", "pass (valid token)","FLAG (BOLA — object-level auth)"),
  ("XSS in a form field",               "BLOCK (XSS)",       "pass (not its layer)"),
  ("normal order placement",            "pass",              "pass"),
]
print(f"{'request':38}{'WAF (AAP)':>22}{'API Security':>28}")
for desc, waf, api_sec in REQUESTS:
    print(f"{desc:38}{waf:>22}{api_sec:>28}")
print("\nNeither layer is a superset of the other:")
print("  WAF catches PAYLOAD attacks (injection, XSS) — API Security waves them through")
print("  API Security catches LOGIC/POSTURE attacks (BOLA, velocity, shadow APIs) that")
print("     are individually-valid requests the WAF has no rule for")
print("\nThe BOLA row is the canonical case: 'user A's token reads user B's object' is")
print("a perfectly-formed authenticated request. No injection, no bad input — the")
print("authorization logic is the vulnerability, and only a layer that MODELS the API")
print("(who should access what) can see it. That is why the Architect credential")
print("treats them as two products, not one with two names.")
EOF
```

**Expected result:** The WAF blocks payload attacks and passes logic attacks; API Security does the reverse; neither is a superset. The BOLA row is the sharpest — a valid authenticated request exploiting authorization logic — and it is the concrete reason enterprises run both layers rather than treating API Security as a fancier WAF.

**Negative test:** Deploying API Security and relaxing the WAF, or vice versa. Each move opens the class of attack the removed layer owned; the SQLi and the BOLA need different defenders.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — North-south and east-west under one vendor

**Objective:** Map the full zero-trust picture an Akamai estate can assemble.

```bash
python3 - <<'EOF'
LAYERS = {
  "north-south (user -> app)": [
    ("EAA",  "per-app access, no network exposure — replaces VPN"),
    ("SIA",  "filtered egress — blocks user -> bad-destination"),
    ("MFA",  "phishing-resistant identity proof"),
  ],
  "east-west (workload <-> workload)": [
    ("Guardicore", "microsegmentation — contains lateral movement (Chapter 07)"),
  ],
}
print("An Akamai estate can run BOTH halves of zero trust:\n")
for direction, prods in LAYERS.items():
    print(f"  {direction}:")
    for p, role in prods: print(f"     {p:12} {role}")
    print()
print("Why both halves matter, in one scenario:")
print("  a phished user (MFA reduces) reaches ONE app via EAA (north-south limits")
print("  the entry). From that app, GUARDICORE (east-west) decides whether they can")
print("  move laterally to the database. EAA bounded the front door; Guardicore")
print("  bounds the hallway. Neither substitutes for the other.")
print("\nMost vendors sell one half. Cloudflare/Zscaler (Vols CXLII/XXXV) are")
print("north-south-strong; the microseg vendors (Vol LXXXVII) are east-west.")
print("Akamai selling both is the estate-consolidation pitch — and the reason this")
print("volume's Chapter 07 is a Guardicore deep-dive rather than a footnote.")
EOF
```

**Expected result:** Akamai's north-south portfolio (EAA/SIA/MFA) and east-west product (Guardicore) mapped as complementary halves, with a scenario showing each bounding a different stage of an intrusion. The consolidation framing sets up Chapter 07 — this is the rare vendor selling both directions, so the segmentation half earns its own deep treatment.

**Negative test:** Calling an estate "zero trust" with EAA alone. The front door is bounded; a compromised app still has the run of the hallway until east-west segmentation exists.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] API Security's discover → posture → runtime model run in order, discovery first.
- [ ] API Security distinguished from the WAF, with BOLA as the layer-defining example.
- [ ] The Zero Trust portfolio (EAA/SIA/MFA) mapped onto the ZTNA/SWG pattern.
- [ ] North-south and east-west recognized as complementary, setting up the Guardicore chapter.
