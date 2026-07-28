# Chapter 07: Technology Specialist — Advanced WAF (ASM)

## Learning Objectives

- Explain the CTS Advanced WAF / ASM specialization (exam 303).
- Build a web application firewall policy (positive and negative security).
- Apply attack signatures and tune false positives.
- Add bot defense and layered protections.
- Complete a walkthrough for each Advanced WAF topic (defensive).

## Theory and Architecture

The **F5 Certified Technology Specialist, ASM** (exam **303**) covers **BIG-IP Advanced WAF**
(Application Security Manager) — F5's web application firewall. A WAF protects applications by
inspecting HTTP(S) and enforcing a **security policy**. Advanced WAF combines **negative security**
(**attack signatures** matching known exploit patterns — SQL injection, XSS, command injection) and
**positive security** (a **learned/whitelisted** model of legitimate URLs, parameters, and their
allowed values, blocking anything else). It adds **bot defense** (distinguishing humans, good bots,
and malicious automation), **L7 DoS** protection, **credential-stuffing/brute-force** mitigation,
and **data guard** (masking sensitive responses). Policies run in **transparent** (log-only) or
**blocking** mode, and **learning** suggests refinements from real traffic. Everything here is
**defensive**: building and tuning protection, not attacking.

## Design Considerations

Start a policy in **transparent** mode and use **learning** to tune before **blocking**, so you
don't break the app. Combine **signatures** (negative) with a **positive** model for defense in
depth. Add **bot defense** for automation-heavy threats. Tune **false positives** with precision
(disable a signature only where proven benign), never by weakening the whole policy.

## Implementation and Automation

The labs create a WAF policy, enable signatures, tune a false positive, add bot defense, and
review events — all **defensive**.

## Validation and Troubleshooting

Confirm the WAF model:

```text
Advanced WAF (ASM): negative (attack signatures) + positive (learned URLs/params) security.
Bot defense, L7 DoS, brute-force/credential-stuffing, data guard.
Modes: transparent (log) -> learning -> blocking. Exam 303.
```

Common pitfalls: going straight to **blocking** with no learning (breaks the app); and fixing a
false positive by **disabling the whole policy** instead of a precise exception.

## Security and Best Practices

Deploy in **transparent → learning → blocking** order. Keep **signatures** updated. Tune false
positives **precisely**. Layer positive + negative security and bot defense. Review the **event
log** to improve the policy. This is defensive application protection.

## Hands-On Lab

Advanced WAF walkthroughs (defensive). **Shared prerequisites** — a BIG-IP VE with ASM/Advanced
WAF provisioned and the `web_vs` virtual server, in an authorized lab. **Cost:** none.

### Lab 7.1 — Create a WAF policy in transparent mode

**Objective:** Attach a log-only policy to the app.

```bash
tmsh create asm policy web_waf policy-builder { learning-mode automatic } enforcement-mode transparent
tmsh modify ltm virtual web_vs policies add { web_waf }
tmsh list asm policy web_waf enforcement-mode
```

**Expected result:** a WAF policy in **transparent** mode on `web_vs` — protection observing
without blocking yet.

**Negative test:** attach a new policy directly in **blocking** mode; it may block legitimate
traffic — start **transparent** and learn.

**Cleanup:** detach and delete the policy.

### Lab 7.2 — Enable attack signatures (negative security)

**Objective:** Match known exploit patterns.

```text
# Assign signature sets (e.g., "Generic Detection", SQLi, XSS, command injection) to the policy.
# Signatures = NEGATIVE security: block traffic matching known-bad patterns.
"signatures: SQLi/XSS/cmd-injection sets -> block known attacks"
```

**Expected result:** attack **signature sets** enabled — negative-security coverage of known
exploits.

**Negative test:** rely only on signatures; add a **positive** model too — defense in depth.

**Cleanup:** none (policy-level).

### Lab 7.3 — Tune a false positive

**Objective:** Allow a legitimate request the WAF flagged.

```text
# Learning shows a benign parameter value tripping a SQLi signature on /search.
# Fix precisely: add an allowed value / disable that ONE signature on that ONE parameter.
"tune: disable signature X on parameter 'q' of /search only; keep it enforced elsewhere"
```

**Expected result:** a **precise exception** clearing the false positive while keeping protection
elsewhere.

**Negative test:** disable the signature **globally** to stop the alert; scope the exception —
keep coverage on other endpoints.

**Cleanup:** none.

### Lab 7.4 — Add bot defense

**Objective:** Mitigate malicious automation.

```text
# Bot Defense classifies clients (human / good bot / malicious) and challenges/blocks bad bots;
#   protects against scraping, credential stuffing, and automated abuse.
"bot defense: classify -> allow humans/good bots, challenge/block malicious automation"
```

**Expected result:** **bot defense** distinguishing humans from malicious automation — a layer
beyond signatures.

**Negative test:** treat all automated traffic as either fully allowed or fully blocked; **bot
defense** classifies it — enable it.

**Cleanup:** none.

### Lab 7.5 — Review WAF events

**Objective:** Investigate what the policy saw.

```bash
tmsh show asm policy web_waf
# In production, review the ASM event log (requests, violations, signatures matched) to tune.
echo "review ASM event log: violations, matched signatures, suggested policy changes"
```

**Expected result:** the policy status and **violation/event** review — the feedback loop that
tunes protection.

**Negative test:** enable blocking and never review events; the **event log** drives tuning —
review it continuously.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CTS Advanced WAF/ASM specialization (303) covers building web application firewall policies —
negative (signatures) plus positive (learned) security, bot defense, and precise false-positive
tuning — deployed transparent → learning → blocking. Layer protections, tune precisely, and let
the event log drive improvement. Defensive throughout.

- [ ] I can create a WAF policy in transparent mode.
- [ ] I can enable attack signatures.
- [ ] I can tune a false positive precisely.
- [ ] I can add bot defense and review events.
- [ ] I completed Labs 7.1–7.5 including each negative test.
