# Chapter 08: CCP-AppDS — Web App Firewall, nFactor, and NetScaler Console

## Learning Objectives

- Cover the 1Y0-342 exam's twelve modules: Web App Firewall, advanced security, AAA/nFactor, and NetScaler Console.
- Build WAF profiles/policies, an nFactor flow, and Console-driven management.
- Complete a walkthrough lab per module group (all twelve modules exercised).

## The exam in brief

**Certification:** Citrix Certified Professional — App Delivery and Security (CCP-AppDS). **Exam:** **1Y0-342** *NetScaler Advanced Topics — Security, Management and Optimization* — the one exam still carrying a legacy code. 60–70 questions, ~10% performance-based, English + Japanese. **Prerequisite:** either CCA-AppDS exam. **Recommended course:** NS-301 *NetScaler 14.x Advanced Administration (Security and Management)* — the exam corresponds to 100% of the course. Twelve modules in three arcs: WAF (1–5), AAA/nFactor (6–8), NetScaler Console (9–11), plus tuning (12).

## Hands-On Lab

Walkthroughs run against a lab VPX (WAF requires a premium/lab license; CPX Express covers the CLI shapes). **Cost:** eval licensing.

### Lab 8.1 — WAF profile and policy (modules 1–2)

**Objective:** Stand up the Web App Firewall in learning-then-blocking posture.

```bash
enable ns feature AppFW
add appfw profile prof_web -defaults advanced
set appfw profile prof_web -startURLAction LEARN LOG -SQLInjectionAction LEARN LOG STATS -crossSiteScriptingAction LEARN LOG STATS
add appfw policy pol_waf true prof_web
bind lb vserver lb_web -policyName pol_waf -priority 100 -type REQUEST
show appfw profile prof_web | head -20
```

**Expected result:** The advanced-defaults profile bound to the application, with Start URL, SQL injection, and XSS checks in **LEARN + LOG** — observe first, then flip learned relaxations into enforcement (`-SQLInjectionAction BLOCK LOG STATS`). Profiles hold the checks; policies decide which traffic hits which profile.

**Negative test:** Jump straight to BLOCK on a real app with no learning: legitimate requests trip Start URL closure — the module's core lesson is the learn-then-block sequence.

**Cleanup:** Keep for 8.2.

### Lab 8.2 — Protections in action (module 3)

**Objective:** Verify a security check actually blocks.

```bash
set appfw profile prof_web -SQLInjectionAction BLOCK LOG STATS
curl -s "http://10.150.9.100/search?q=1%27%20OR%20%271%27=%271" -o /dev/null -w "%{http_code}\n"
```

**Expected result:** The injection probe is blocked (WAF block page / reset per profile settings) and `stat appfw profile prof_web` counts the hit; a clean request still passes. Data flow: policy match → profile checks → block/transform/log.

**Negative test:** Send the same probe with the check back in LEARN — it passes and is logged as a candidate relaxation instead; action, not detection, is what changed.

**Cleanup:** Return the check to LEARN LOG in the lab.

### Lab 8.3 — Bot and API protection (modules 4–5)

**Objective:** Enable the advanced protections beyond the classic checks.

```bash
enable ns feature Bot
add bot profile prof_bot -signature BOT_SIGNATURES -deviceFingerprint ON
add bot policy pol_bot -rule true -profileName prof_bot
bind lb vserver lb_web -policyName pol_bot -priority 90 -type REQUEST
add ns limitIdentifier rate_login -threshold 10 -timeSlice 60000 -mode REQUEST_RATE
add responder policy pol_rate "SYS.CHECK_LIMIT(\"rate_login\")" RESET
```

**Expected result:** Bot signatures and device fingerprinting screen traffic before the WAF, and the rate identifier resets clients exceeding 10 requests/minute — bot management, API/rate protection, IP reputation, and AppQoE form the module 4–5 layer on top of the WAF.

**Negative test:** Loop 20 rapid requests at the protected vserver: the first ~10 succeed, the rest are reset — `show ns limitIdentifier rate_login` shows the counter doing it.

**Cleanup:** Remove the bot/rate lab objects.

### Lab 8.4 — nFactor authentication (modules 6–7)

**Objective:** Build a two-factor nFactor flow: LDAP then OTP.

```bash
add authentication vserver auth_vs SSL 10.150.9.230 443
bind ssl vserver auth_vs -certkeyName lab_cert
add authentication loginSchema ls_dual -authenticationSchema "/nsconfig/loginschema/LoginSchema/DualAuth.xml"
add authentication loginSchemaPolicy pol_ls -rule true -action ls_dual
add authentication policylabel pl_otp -loginSchema LSCHEMA_INT
add authentication policy pol_ldap2 -rule true -action lab_ldap
bind authentication policylabel pl_otp -policyName pol_ldap2 -priority 100
bind authentication vserver auth_vs -policy pol_ldap2 -priority 100 -nextFactor pl_otp
bind authentication vserver auth_vs -policy pol_ls -priority 100 -gotoPriorityExpression END
```

**Expected result:** A chained flow — login schema collects both credentials, factor one validates LDAP, `nextFactor` hands off to the OTP policy label — nFactor's grammar: **schemas** (what to collect), **policies** (how to validate), **policy labels** (the next factor). SAML, OAuth, and certificate factors slot into the same chain, which is how module 7's SSO use cases compose.

**Negative test:** Omit the `nextFactor`: authentication completes after LDAP alone — the chain is only as long as its links.

**Cleanup:** Keep the auth vserver for the lab; remove when done.

### Lab 8.5 — AAA customization (module 8)

**Objective:** Brand the logon and add a EULA.

```bash
add vpn portaltheme theme_lab -basetheme RfWebUI
bind authentication vserver auth_vs -portaltheme theme_lab
add authentication loginSchema ls_eula -authenticationSchema "/nsconfig/loginschema/LoginSchema/SingleAuthEula.xml"
```

**Expected result:** The logon page carries the custom theme and presents the EULA checkbox before credentials submit — portal themes and schema variants are module 8's surface; custom error pages round it out.

**Negative test:** Base a theme on a nonexistent one — the add fails; themes derive, they don't start blank.

**Cleanup:** Remove the lab theme.

### Lab 8.6 — NetScaler Console onboarding (modules 9–10)

**Objective:** Bring instances under central management and read the dashboards.

```text
console> Infrastructure > Instances > NetScaler > Add (NSIP + nsroot profile)
console> Security > Security Dashboard        # WAF/bot violations across the fleet
console> Infrastructure > Events > rules      # event management with severity filters
console> Infrastructure > SSL Dashboard       # expiring certificates, weak ciphers
```

**Expected result:** The lab instance inventoried; the unified security dashboard aggregates the WAF hits from Lab 8.2, the event rules classify instance events, and the SSL dashboard flags the lab cert's expiry — Console (formerly ADM) is the fleet's single pane, and modules 9–10 are its inventory/users/events/SSL surfaces.

**Negative test:** Add an instance with a wrong admin profile: discovery fails cleanly and the instance shows unreachable — credentials are per-profile, not global.

**Cleanup:** Remove the lab instance from Console.

### Lab 8.7 — Stylebooks and config management (module 11)

**Objective:** Deploy configuration as code from Console.

```text
console> Applications > Configuration > StyleBooks > HTTP/SSL Load Balancing
console>   fill parameters (vserver name/IP, services) > Target Instances > Deploy
console> Infrastructure > Configuration Audit > run audit against the template
```

**Expected result:** The Stylebook renders the same `add/bind` objects Lab 5.4 built by hand — now versioned, repeatable, and auditable; configuration audit diffs running config against the template and flags drift. Actionable tasks close the loop.

**Negative test:** Hand-edit the deployed vserver on the instance; the next audit reports the drift — the module's point is that the template, not the box, is the source of truth.

**Cleanup:** Delete the Stylebook deployment (Console removes the objects it created).

### Lab 8.8 — Tuning profiles (module 12)

**Objective:** Apply connection, SSL, and net profiles deliberately.

```bash
add ns tcpProfile tcp_lan -WS ENABLED -SACK ENABLED -mss 1460
add ssl profile ssl_strict -sslProfileType FrontEnd
set ssl profile ssl_strict -tls1 DISABLED -tls11 DISABLED -tls12 ENABLED -tls13 ENABLED
add netProfile np_snip -srcIP 10.150.9.6
set lb vserver lb_web -tcpProfileName tcp_lan -netProfile np_snip
set ssl vserver lb_web_ssl -sslProfile ssl_strict
```

**Expected result:** The vserver runs the tuned TCP profile, sources back-end traffic from the pinned SNIP, and the SSL vserver accepts only TLS 1.2/1.3 — profiles (TCP, SSL, net, HTTP) are module 12's mechanism for tuning per-vserver instead of globally; RPC nodes carry the same idea to inter-NetScaler communication.

**Negative test:** Disable TLS 1.2 as well and old clients fail the handshake — `show ssl vserver` plus `nstrace` prove it was the profile.

**Cleanup:** Remove the lab profiles.

## Summary and Completion Checklist

- [ ] WAF learn-then-block cycle built and proven (modules 1–3).
- [ ] Bot/API/rate protections layered (modules 4–5).
- [ ] nFactor chain, SSO composition, and AAA branding drilled (modules 6–8).
- [ ] NetScaler Console inventory, dashboards, Stylebooks, and audit exercised (modules 9–11).
- [ ] Per-vserver tuning profiles applied (module 12).
