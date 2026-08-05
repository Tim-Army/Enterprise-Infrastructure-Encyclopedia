# Chapter 04: App & API Protector

## Learning Objectives

- Place App & API Protector in the Kona Site Defender lineage the course badges still reflect.
- Understand the Adaptive Security Engine's self-tuning claim and what it does not remove.
- Operate protections in the evaluate-then-enforce rhythm.
- Handle the WAF-behind-WAF and origin-exposure interactions specific to enterprise estates.

*Course relevance: **Akamai Web Application and API Protection** — "configuring and maintaining App & API Protector with Advanced Security Management using the new Adaptive Security Engine" — plus the legacy **Kona Site Defender Config & Maintain / Advanced** badges still in the catalog. **Defensive** throughout.*

## The lineage, because the badges show it

Akamai's WAF has generations, and the badge catalog preserves them: **Kona Site Defender (KSD)** badges sit beside the current **App & API Protector (AAP)** course. This matters practically — enterprise estates run mixed generations, documentation and muscle memory span both, and a "Kona rule" reference in a runbook is not an error but an era. The current course's scope line names the pieces: AAP with **Advanced Security Management**, the **Adaptive Security Engine (ASE)**, and **Bot Visibility & Mitigation**.

## The Adaptive Security Engine

ASE's pitch is self-tuning: rules that adjust sensitivity per traffic profile, reducing the manual rule-exception grind that consumed WAF operators for a decade. The honest operator reading, consistent with every precision chapter on this shelf:

- **Self-tuning moves work; it does not remove it.** The grind shifts from writing exceptions to *reviewing what the engine decided* — its sensitivity choices are now configuration you inherit and must audit.
- **The evaluate mode is still the contract.** AAP protections run in evaluation before enforcement; the [log → measure → enforce ladder](../../volume-142-cloudflare-certifications/chapters/03-waf-rules-and-rate-limiting.md) is identical in shape, and precision measured on your traffic remains the go-live evidence, ASE or no ASE.
- **Adaptive systems drift by design.** What the engine considers normal tracks your traffic; a traffic change (a new client, a bot wave, a product launch) changes the baseline. Periodic review of *what changed in the engine's decisions* is the new hygiene task.

## Enterprise interactions

Two estate-scale problems the course's "maintain" verb covers:

1. **Origin exposure, again.** The [gray-cloud audit](../../volume-142-cloudflare-certifications/chapters/02-the-edge-network-dns-and-caching.md) has an Akamai twin: the origin must accept traffic only from Akamai's edge (Site Shield / firewall by published ranges), or the WAF is a suggestion for anyone holding the origin's address. Same failure, same fix, different vendor vocabulary.
2. **Layered WAFs.** Enterprises often run AAP at the edge *and* a cloud provider's WAF at the origin. Two rule sets, two false-positive surfaces, two teams — and requests rejected by the inner layer look like origin errors to the outer one. The lab models the diagnosis pattern, because "the WAF blocked it — which WAF?" is a real Tuesday.

## Hands-On Lab

Python models WAF operations. **Cost:** none. Defensive throughout.

### Lab 4.1 — Reviewing what the adaptive engine decided

**Objective:** Audit self-tuning the way you audit a junior analyst.

```bash
python3 - <<'EOF'
DECISIONS = [
  # rule group,                engine sensitivity, last month, traffic driver,            verdict
  ("SQLi core",                "high",   "high",   "stable",                     "fine"),
  ("XSS core",                 "high",   "high",   "stable",                     "fine"),
  ("RFI/LFI",                  "medium", "high",   "new PDF-upload feature",     "REVIEW — lowered on legit uploads; confirm scope is the upload path ONLY"),
  ("command injection",        "high",   "high",   "stable",                     "fine"),
  ("protocol anomalies",       "low",    "medium", "new IoT client fleet",       "REVIEW — engine adapted to odd-but-legit clients; verify the fleet is yours"),
  ("scanner signatures",       "medium", "high",   "pen-test window last month", "RESTORE — it learned from your OWN pen test; that traffic was not 'normal'"),
]
print(f"{'rule group':22}{'now':>8}{'before':>8}   driver / verdict")
reviews = 0
for g, now, before, driver, verdict in DECISIONS:
    flag = "" if verdict == "fine" else "  <--"
    if verdict != "fine": reviews += 1
    print(f"{g:22}{now:>8}{before:>8}   {driver}")
    if verdict != "fine": print(f"{'':40}{verdict}")
print(f"\n{reviews} of {len(DECISIONS)} adaptations need a human decision. The engine did its")
print("job — it adapted to traffic. The REVIEW is the new job: every sensitivity")
print("change has a traffic story, and the operator's question is whether that")
print("story should have been learned from.")
print("\nThe pen-test row is the sharp case: the engine treated authorized attack")
print("traffic as environment and relaxed. Adaptive systems need to be told which")
print("traffic is EXEMPT from learning — schedule windows, then verify baselines.")
EOF
```

**Expected result:** Three of six adaptations warrant human decisions, including the engine having learned from the customer's own pen test. The framing carries: self-tuning converts rule-writing into decision-review, and the pen-test case shows the one instruction adaptive systems always need — what not to learn from.

**Negative test:** Treating "adaptive" as "unattended." Six months of unreviewed adaptations is a security posture nobody chose, assembled from whatever the traffic did.

**Cleanup:** None.

### Lab 4.2 — Which WAF blocked it?

**Objective:** Diagnose layered-WAF rejections systematically.

```bash
python3 - <<'EOF'
CASES = [
  # symptom at the edge,                 edge_waf_log, origin_status, origin_waf_log, culprit
  ("user reports 403 on checkout",       "deny: XSS rule 950004",  None,  None,       "EDGE — AAP denied; user never reached origin"),
  ("API client gets 403",                "pass",       403,   "deny: SQLi sig",        "ORIGIN WAF — passed edge, inner layer denied"),
  ("mobile app gets 403",                "pass",       403,   "pass",                  "ORIGIN APP — both WAFs passed; the app itself said 403"),
  ("partner batch gets 429",             "rate limit", None,  None,                    "EDGE — rate policy, not a WAF rule at all"),
  ("intermittent 5xx spikes",            "pass",       503,   "deny (under load)",     "ORIGIN WAF — failing closed under load; capacity, not rules"),
]
print("Diagnosis order: EDGE LOG first, ORIGIN STATUS second, ORIGIN LOG third.\n")
for symptom, edge, origin_status, origin_waf, culprit in CASES:
    print(f"  {symptom}")
    print(f"     edge log: {edge:26} origin: {origin_status if origin_status else '-':>4}  origin waf: {origin_waf if origin_waf else '-'}")
    print(f"     -> {culprit}\n")
print("The rule that prevents the two-team stalemate: a 403 the EDGE log shows as")
print("'pass' is NOT the edge's 403 — and a 403 with no origin-WAF deny is the")
print("APPLICATION's. Every blocked-request ticket resolves in three lookups, in")
print("order, or it circulates for a week as 'the WAF is blocking us' between")
print("teams that each checked only their own layer.")
print("\nPrecondition, as always: BOTH layers' logs must land somewhere queryable")
print("(Vol CXLII ch08's pipeline-health lesson applies to each independently).")
EOF
```

**Expected result:** Five symptoms resolved to five different culprits — edge WAF, origin WAF, the application itself, a rate policy, and origin capacity — by the same three-lookup order. The stalemate framing is the operational truth: layered estates turn every 403 into an inter-team ticket unless the diagnosis order is agreed and the logs from both layers actually arrive.

**Negative test:** Concluding "the WAF is fine" after checking one layer. Three of the five cases require the second or third lookup to attribute correctly.

**Cleanup:** None.

### Lab 4.3 — Origin lockdown, Akamai edition

**Objective:** Verify the origin accepts only edge traffic.

```bash
python3 - <<'EOF'
SOURCES = [
  # source,                       in_akamai_ranges, allowed_by_origin_fw, note
  ("Akamai edge (Site Shield range)", True,  True,  "the intended path"),
  ("Akamai edge (new range, unsynced)",True, False, "range list DRIFTED — legit traffic dropped"),
  ("office IP (debug exception)",     False, True,  "the 'temporary' hole, 14 months old"),
  ("random scanner",                  False, False, "correctly rejected"),
  ("attacker with origin IP",         False, False, "correctly rejected — lockdown working"),
]
print(f"{'source':36}{'edge range':>11}{'fw allows':>11}   assessment")
findings = 0
for s, in_range, allowed, note in SOURCES:
    ok = (in_range and allowed) or (not in_range and not allowed)
    mark = "" if ok else "  <-- FINDING"
    if not ok: findings += 1
    print(f"{s:36}{'yes' if in_range else 'no':>11}{'yes' if allowed else 'NO':>11}   {note}{mark}")
print(f"\n{findings} findings, and they are OPPOSITE failures:")
print("  1. the UNSYNCED RANGE drops legitimate edge traffic — Akamai's ranges")
print("     change; the firewall list is a feed to automate, not a file to paste.")
print("     (Site Shield exists precisely to give you a managed, stable set.)")
print("  2. the DEBUG EXCEPTION admits non-edge traffic — the WAF, bot manager,")
print("     and rate limits all evaluate NOTHING for whoever finds that path.")
print("\nThe audit is two assertions, run on schedule:")
print("  every allowed source is in the current edge ranges;")
print("  every current edge range is allowed. Drift in either direction is a page.")
EOF
```

**Expected result:** Two findings in opposite directions — a stale range list dropping legitimate traffic and a fossilized debug exception bypassing every protection. The two-assertion audit at the end is the whole control, and its "on schedule, both directions" framing is what distinguishes lockdown from a firewall rule someone once wrote.

**Negative test:** Pasting the range list once at go-live. It is correct until Akamai's next range change, and the failure mode (some users, some edges, sometimes) is miserable to diagnose from symptoms.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The KSD → AAP lineage read correctly in badges, runbooks, and estates.
- [ ] Adaptive Security Engine adaptations reviewed as decisions, with learning-exempt windows for tests.
- [ ] Layered-WAF rejections diagnosed in the three-lookup order.
- [ ] Origin lockdown audited in both directions on a schedule.
