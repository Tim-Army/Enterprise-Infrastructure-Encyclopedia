# Chapter 09: Choosing Your Track, Currency, and Career

## Learning Objectives

- Choose between (or sequence) the Virtualization and AppDS tracks for your role.
- Build a study plan per exam from the modules and courses.
- Keep the certifications current through the announced program overhaul.

## Choosing a track

| If your role is… | Start with | Then |
|:---|:---|:---|
| CVAD administrator / EUC engineer | CCA-V | CCP-V |
| Network / ADC engineer | CCA-AppDS (Traffic Management option) | CCP-AppDS |
| Remote-access / security engineer | CCA-AppDS (Gateway option) | CCP-AppDS |
| Full-stack Citrix engineer | CCA-V + CCA-AppDS-Gateway | CCP-V, CCP-AppDS |

The two CCA-AppDS options certify the same credential — choose by exposure: Gateway if you front CVAD with remote access, Traffic Management if you run the ADC estate. The Gateway exam's CVAD-integration module makes it the natural second certification for virtualization people.

## Study plans

| Exam | Course | Volume chapters | Suggested prep |
|:---|:---|:---|:---|
| CCA-V | CVAD-201 (2402 LTSR) | [02](02-cca-v-deploying-and-delivering.md)–[03](03-cca-v-security-monitoring-operations.md) | 4–6 weeks with a lab site |
| CCP-V | CVAD-301 (2402 LTSR) | [04](04-ccp-v-advanced-administration.md) | 4–6 weeks after CCA-V |
| CCA-AppDS-Gateway | CNS-225 / NS-232 | [05](05-appds-netscaler-platform-and-load-balancing.md)–[06](06-cca-appds-gateway-secure-remote-access.md) | 4–6 weeks with CPX/VPX |
| CCA-AppDS-TM | NS-201 | [05](05-appds-netscaler-platform-and-load-balancing.md), [07](07-cca-appds-traffic-management.md) | 4–6 weeks with CPX/VPX |
| CCP-AppDS (1Y0-342) | NS-301 | [08](08-ccp-appds-waf-nfactor-console.md) | 6–8 weeks; WAF lab time matters |

Course access: instructor-led through Authorized Training Providers; on-demand eLearning is delivered through the **Pluralsight partnership** (included for customers with an active Citrix or NetScaler subscription) — the CVAD Academy and NetScaler Administrator Academy paths. The full course catalog is in the [Citrix appendix](../../volume-997-master-appendices/README.md).

The AppDS exams include ~10% **performance-based items** (TM adds CLI simulations): budget lab hours at the NetScaler CLI, not just reading — the Chapter 05–08 walkthroughs are sized to be run, and CPX Express makes them free.

## Currency through the overhaul

- **Re-verify before every exam registration.** The program is explicitly mid-overhaul with "additional certifications planned"; exam names, options, and the platform can change. The authoritative surfaces are citrix.com/training-and-certifications, netscaler.com's training page, and Webassessor.
- **Watch for the Expert tier's replacement.** CCE-V/CCE-N are gone; if the overhaul reintroduces an expert level, current CCP holders will likely be its audience.
- **Historical credentials.** Legacy certifications (1Y0-era) surface on the new platform via the email-plus-password-reset recovery; badges live on Credly.
- **Government relevance.** Citrix certifications have appeared in DoD workforce-credential listings (COOL); with the CCE tier retired, verify which current credentials your program accepts before targeting one.

## Hands-On Lab

### Lab 9.1 — Personal certification plan

**Objective:** Commit a plan to paper.

```bash
cat > my-citrix-plan.md <<'EOF'
Role: ___                     Track: V / AppDS / both
Exam 1: ___                   Target date: ___
Course/lab: CVAD-201 / NS-201 / CNS-225 + CPX lab
Modules weak: ___             Lab hours/week: ___
Re-verify program on: (2 weeks before exam) ___
EOF
cat my-citrix-plan.md
```

**Expected result:** A dated plan with the re-verification step built in — the overhaul makes that step part of the plan, not paranoia.

**Negative test:** A plan without lab hours: the AppDS performance items will find you.

**Rollback:** Keep the plan.

### Lab 9.2 — Currency watch

**Objective:** Make the re-check cheap enough to actually do.

```bash
curl -s https://www.citrix.com/training-and-certifications/ | tr -s ' \n' ' ' | grep -o "Citrix Certified [A-Za-z– ]*" | sort -u > citrix-certs-$(date +%F).txt
diff citrix-certs-*.txt 2>/dev/null || echo "first snapshot taken"
```

**Expected result:** A dated snapshot of the official certification list; the next run diffs against it — a one-command overhaul detector.

**Negative test:** Relying on a training vendor's mirror for the same check — stale mirrors are how people register for retired exams.

**Rollback:** Keep the snapshots.

## Summary and Completion Checklist

- [ ] Track chosen and sequenced for your role.
- [ ] Study plan committed, with lab hours for the performance-based items.
- [ ] Currency habit installed: re-verify on the official surfaces before registering.
