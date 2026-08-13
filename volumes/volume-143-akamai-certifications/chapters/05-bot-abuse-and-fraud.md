# Chapter 05: Bot, Abuse, and Fraud Protection

## Learning Objectives

- Distinguish Bot Manager, Account Protector, and Content Protector by the abuse each addresses.
- Score and act on bots by intent and consequence, not by a single threshold.
- Understand account-abuse detection: the signals beyond a valid password.
- Recognize client-side (Magecart-class) threats and the compliance angle.

*Course relevance: **Akamai Bot Manager Foundations / Advanced**, **Bot & Abuse Protection** (Bot Manager + Account Protector + Content Protector), **Fraud Management** (Bot Manager + Account Protector), **Client-Side Protection & Compliance**. **Defensive** throughout.*

## Three products, three abuses

| Product | Addresses | Core signal |
|:---|:---|:---|
| **Bot Manager** | Automated traffic — scraping, credential stuffing, inventory hoarding | Behavioral + fingerprint bot scoring |
| **Account Protector** | Account *takeover and abuse* — by traffic that may be human or bot | Per-account behavioral anomaly vs that account's history |
| **Content Protector** | Scraping of content/pricing specifically | Content-access pattern detection |

The Bot & Abuse Protection course bundles the first three because real abuse uses all of them: a credential-stuffing campaign is *bot traffic* (Bot Manager) attempting *account takeover* (Account Protector), and the defenses compose. The Fraud Management course narrows to the Bot-Manager-plus-Account-Protector pair that most directly touches money.

## Bots by intent, not threshold

[Volume CXLII's bot chapter](../../volume-142-cloudflare-certifications/chapters/04-ddos-bots-and-api-shield.md) established score-by-consequence; the Akamai courses add a **taxonomy of intent** that changes the *action*, not just the threshold:

| Bot intent | Right response |
|:---|:---|
| Search/SEO crawlers, monitors | Allow (verified) — blocking deindexes you |
| Partner integrations, price comparison you invited | Allow-list explicitly |
| Scrapers (competitive, unwanted) | Serve alternate/delayed content, or challenge |
| Credential stuffing | Aggressive challenge/deny — it is an attack |
| Inventory/scalping bots | Deny — the business impact is direct |

The insight the lab builds: **the same bot score demands different actions by intent**, and intent is inferred from *what the bot is doing* (which endpoints, what sequence) as much as from how bot-like it looks. A 95-percent-confident bot hitting `robots.txt` and the sitemap is probably Google; the same confidence hitting `/login` in a spray is an attack.

## Account abuse beyond the password

Account Protector's premise is the one [Volume CXL's DEM chapter](../../volume-140-dynatrace-certifications/README.md) and every IAM volume circle: **a valid password is not proof of a valid user.** Detection uses per-account behavioral baselines — usual devices, locations, times, velocities — and flags the login that is *credentialed but anomalous*: right password, wrong everything else. This is the same shape as [CyberArk (LXXVII)](../../volume-077-cyberark-certifications/README.md) and [Okta (LXXVI)](../../volume-076-okta-certifications/README.md) risk signals, applied at the edge before the request reaches the application.

## Client-side protection and compliance

**Content Protector & Compliance** addresses the threat class the other products cannot see: **malicious third-party scripts in the browser** — Magecart-style skimmers that steal card data client-side, where a server-side WAF has no visibility. The compliance angle is real and current: **PCI DSS v4** requirements for payment-page script integrity make this a checkbox with an auditor attached, not only a security control. The lab models script-inventory drift, because the failure is a script that *changed*, not one that was obviously malicious on day one.

## Hands-On Lab

Python models abuse detection. **Cost:** none. Defensive throughout.

### Lab 5.1 — Same score, different action by intent

**Objective:** Route bots by what they are doing.

```bash
python3 - <<'EOF'
BOTS = [
  # description,                       bot_score, endpoints,                 verified
  ("Googlebot crawling",                    96,  ["/", "/sitemap.xml"],     True),
  ("uptime monitor",                        92,  ["/health"],               True),
  ("price-comparison (partner)",            88,  ["/api/products"],         False),
  ("competitor scraper",                    90,  ["/api/products"]*40,      False),
  ("credential stuffing",                   85,  ["/login"]*500,            False),
  ("scalper on drop",                       97,  ["/checkout"]*200,         False),
]
def action(score, endpoints, verified):
    ep = endpoints[0]
    rate = len(endpoints)
    if verified:                              return "ALLOW (verified good bot)"
    if ep == "/login" and rate > 50:          return "DENY — credential stuffing"
    if ep == "/checkout" and rate > 20:       return "DENY — scalping, direct $ impact"
    if ep == "/api/products" and rate > 20:   return "CHALLENGE / alt content — scraping"
    if ep == "/api/products":                 return "ALLOW-LIST — invited partner"
    return "monitor"

print(f"{'bot':30}{'score':>7}{'req':>6}   action")
for desc, score, eps, verified in BOTS:
    print(f"{desc:30}{score:>7}{len(eps):>6}   {action(score, eps, verified)}")
print("\nScores span 85-97 and the actions span ALLOW to DENY — because INTENT, read")
print("from endpoint and rate, decides the action. The 96-score Googlebot is allowed;")
print("the 85-score credential-stuffer is denied. A threshold alone would have")
print("inverted that — blocking Google and, at a lower cutoff, waving the attack through.")
print("\nThe course's point: bot MANAGEMENT, not bot blocking. Some automation is")
print("your business (partners, search); the skill is telling invited automation")
print("from abuse by what it does, then acting per the business consequence.")
EOF
```

**Expected result:** Scores clustered in the high 80s–90s producing the full action range from allow to deny, driven by endpoint and rate rather than score. The inversion note is the argument against threshold-only bot control — the highest-scoring bot is the one you most want to allow.

**Negative test:** A single "block above 90" rule. It blocks Googlebot and the scalper alike, and misses the 85-score credential-stuffing attack entirely.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — Credentialed but anomalous

**Objective:** Detect account abuse the password check passes.

```bash
python3 - <<'EOF'
ACCOUNTS = {
  "alice": {"usual_countries": {"DE","AT"}, "usual_devices": {"d1","d2"}, "usual_hours": range(7,20)},
  "bob":   {"usual_countries": {"US"},      "usual_devices": {"d9"},      "usual_hours": range(6,23)},
}
LOGINS = [
  # user,   password_ok, country, device, hour, velocity_per_min
  ("alice", True,  "DE", "d1", 9,   1),
  ("alice", True,  "BR", "dX", 3,   1),     # right password, wrong everything
  ("bob",   True,  "US", "d9", 14,  1),
  ("bob",   True,  "US", "dY", 14,  40),    # right password, 40 logins/min = stuffing hit
  ("alice", False, "DE", "d1", 10,  1),     # wrong password — different problem
]
def risk(user, pw, country, device, hour, vel):
    if not pw: return "reject (bad password) — not Account Protector's job"
    p = ACCOUNTS[user]
    flags = []
    if country not in p["usual_countries"]: flags.append("new country")
    if device not in p["usual_devices"]:    flags.append("new device")
    if hour not in p["usual_hours"]:        flags.append("odd hour")
    if vel > 10:                            flags.append(f"velocity {vel}/min")
    if len(flags) >= 3: return f"HIGH RISK — step-up/deny: {', '.join(flags)}"
    if len(flags) >= 1: return f"elevated — challenge: {', '.join(flags)}"
    return "normal — allow"

for user, pw, country, device, hour, vel in LOGINS:
    print(f"  {user:6} pw={'ok ' if pw else 'BAD'} {country} {device} {hour:>2}h vel={vel:>2}  -> {risk(user, pw, country, device, hour, vel)}")
print("\nEvery 'ok' login above has the RIGHT PASSWORD. Account Protector's whole")
print("job starts AFTER the password check succeeds: alice's Brazil-3am-new-device")
print("login and bob's 40/min burst are both credentialed and both hostile.")
print("\nThe signal is DEVIATION FROM THAT ACCOUNT'S baseline — not a global rule.")
print("bob logging in from the US at 2pm is normal; alice doing the identical thing")
print("from Brazil at 3am is not. Per-account baselines, same discipline as Vol CXL's")
print("Davis and every IAM risk engine — moved to the edge, before the app is touched.")
EOF
```

**Expected result:** Two right-password logins flagged high-risk on behavioral deviation, one bad-password login correctly routed elsewhere, and the rest allowed. The post-authentication framing is the lesson — Account Protector's entire value is downstream of the password being correct, which is exactly where password-only defenses stop looking.

**Negative test:** Trusting any login with a valid password. Credential stuffing succeeds precisely because the passwords are valid — bought, breached, or reused.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Client-side script drift and PCI DSS v4

**Objective:** Catch the skimmer that a WAF cannot see.

```bash
python3 - <<'EOF'
BASELINE = {   # approved scripts on the payment page, with content hashes
  "checkout.js":        "sha:a1b2",
  "analytics.js":       "sha:c3d4",
  "payment-sdk.js":     "sha:e5f6",
  "tag-manager.js":     "sha:0000",
}
OBSERVED = {
  "checkout.js":        "sha:a1b2",
  "analytics.js":       "sha:c3d4",
  "payment-sdk.js":     "sha:9999",     # <- CHANGED. new version? or tampered?
  "tag-manager.js":     "sha:0000",
  "cdn-helper.js":      "sha:beef",     # <- NEW script nobody approved
}
print(f"{'script':20}{'baseline':>12}{'observed':>12}   status")
findings = 0
for s in sorted(set(BASELINE) | set(OBSERVED)):
    b, o = BASELINE.get(s), OBSERVED.get(s)
    if b == o: status = "unchanged"
    elif b is None: status = "*** NEW — unapproved script on the PAYMENT PAGE"; findings += 1
    elif o is None: status = "removed"
    else: status = "*** CHANGED — verify: new release, or a skimmer?"; findings += 1
    print(f"{s:20}{str(b):>12}{str(o):>12}   {status}")
print(f"\n{findings} findings on the payment page. Neither is visibly 'malicious' —")
print("that is the point. A Magecart skimmer is valid JavaScript that also exfiltrates")
print("card fields; a server-side WAF never sees it, because it runs in the USER's")
print("browser on data the user typed. Only client-side monitoring catches it.")
print("\nPCI DSS v4 turned this from good-practice into REQUIREMENT: payment-page")
print("scripts must be inventoried and their integrity assured. The control is")
print("exactly this diff — a maintained baseline vs what actually loads — run")
print("continuously, alerting on NEW and CHANGED. The failure is always a script")
print("that CHANGED, so a one-time approval list is worse than none (it feels done).")
EOF
```

**Expected result:** A changed payment SDK and an unapproved new script, neither obviously malicious, flagged by baseline diff. The PCI DSS v4 framing makes it concrete — this is now an audited requirement, not a nice-to-have — and the closing line names the trap: a static allow-list feels like compliance while missing the change-based attack it exists to catch.

**Negative test:** Approving the script list once and considering client-side protection "done." The skimmer arrives as a *change* to an already-approved script, weeks later.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Bot Manager, Account Protector, and Content Protector matched to their abuse classes.
- [ ] Bots acted on by intent (endpoint + rate), not by a single score threshold.
- [ ] Account abuse detected as credentialed-but-anomalous against per-account baselines.
- [ ] Client-side script integrity monitored continuously, meeting PCI DSS v4 by diff.
