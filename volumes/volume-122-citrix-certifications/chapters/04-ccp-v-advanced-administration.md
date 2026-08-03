# Chapter 04: CCP-V — Advanced Administration

## Learning Objectives

- Map all seven CCP-V modules: advanced administration, access, policies/profiles, WEM, security, troubleshooting, and cloud.
- Drill the high-availability and hybrid designs the professional exam centers on.
- Complete a walkthrough lab per module.

## The exam in brief

**Certification:** Citrix Certified Professional — Virtualization (CCP-V). **Exam:** *Citrix Virtual Apps and Desktops 7 Advanced Administration*, 60–70 questions, 64% minimum passing. **Prerequisite:** CCA-V. **Recommended course:** CVAD-301 *Citrix Virtual Apps and Desktops Advanced Administration (2402 LTSR)*; on-demand via Pluralsight. Seven modules, one lab each below.

## Hands-On Lab

Walkthroughs assume the Chapter 02 lab site plus StoreFront and, for module 4, a WEM lab. **Cost:** none beyond the eval.

### Lab 4.1 — Component redundancy (module 1: advanced administration)

**Objective:** Verify no single point of failure across the delivery chain.

```powershell
Get-BrokerController | Measure-Object | Select-Object Count       # >= 2
Get-ConfigZone | Select-Object Name, ControllerNames               # zones and membership
# SQL HA: AlwaysOn/mirroring at the database layer; StoreFront: server group of >= 2 behind a load balancer
```

**Expected result:** At least two controllers (per zone where zoned), database HA in place, StoreFront as a server group — the redundancy checklist module 1 walks component by component, including Local Host Cache as the brokering fallback when the site database is unreachable.

**Negative test:** Stop SQL in the lab: with Local Host Cache, existing brokering continues on the elected controller; without it, new launches fail — the exam's favorite DR distinction.

**Cleanup:** Restart SQL.

### Lab 4.2 — Advanced access with Gateway and StoreFront (module 2)

**Objective:** Configure the external path: Gateway ICA proxy in front of StoreFront.

```text
storefront> Manage Citrix Gateways > add gateway (public FQDN, STA = controllers)
storefront> Stores > enable Remote Access (Gateway ICA proxy)
netscaler> show vpn vserver        # gateway vserver UP, STA bound
```

**Expected result:** External launches traverse the Gateway (ICA over 443) with Secure Ticket Authority tickets from the controllers; internal launches keep going direct. Beacons decide which path a client takes.

**Negative test:** Remove the STA binding on the gateway; external enumeration still works but launches fail with a ticketing error — STA is the piece candidates forget.

**Cleanup:** Rebind the STA.

### Lab 4.3 — Policies and profiles (module 3)

**Objective:** Layer Citrix policies and Profile Management deliberately.

```powershell
Get-BrokerAssignmentPolicyRule | Select-Object -First 3 Name
# Studio > Policies: filter a policy to a delivery group; priority decides conflicts (lower number wins)
# Profile Management: enable, set the user store path \\fs\profiles\#SAMAccountName#
```

**Expected result:** A policy filtered to the lab group wins over unfiltered lower-priority policies; Profile Management writes the roaming profile to the user store on logoff — the module's two levers: policy precedence and profile consolidation.

**Negative test:** Set two conflicting policies with inverted priorities; the resultant set (Studio > Policies > Modeling) shows which won and why — model before you deploy.

**Cleanup:** Remove lab policies.

### Lab 4.4 — Workspace Environment Management (module 4)

**Objective:** Offload logon work to WEM, the performance module.

```text
wem> Actions: map a network drive + printer via Actions, assigned to the lab group
wem> System Optimization: enable CPU spike protection + memory management on the lab VDA set
```

**Expected result:** Drive and printer arrive via WEM agent at logon (not GPO), and the optimization counters engage under load — WEM replaces logon-script weight with agent-side actions, and the exam tests which layer (WEM action vs Citrix policy vs GPO) does what.

**Negative test:** Assign the same drive letter by GPO and WEM; the collision demonstrates why module 4 insists on one owner per setting.

**Cleanup:** Remove the lab WEM actions.

### Lab 4.5 — Advanced security (module 5)

**Objective:** Enable transport security plus session protection.

```powershell
# TLS on the VDA/broker XML traffic; then App Protection on the delivery group:
Set-BrokerDesktopGroup LabGroup -AppProtectionKeyLoggingRequired $true -AppProtectionScreenCaptureRequired $true
Get-BrokerDesktopGroup LabGroup | Select-Object Name, AppProtection*
```

**Expected result:** The group requires App Protection — anti-keylogging and anti-screen-capture enforced by capable clients; combined with TLS to the VDA and session recording where mandated, that is module 5's checklist.

**Negative test:** Launch from a client without App Protection support; the launch is refused for the protected group — protection is enforced at brokering, not best-effort.

**Cleanup:** Set both flags back to `$false`.

### Lab 4.6 — Advanced troubleshooting (module 6)

**Objective:** Work a launch failure with the professional toolset.

```powershell
Get-BrokerConnectionLog -MaxRecordCount 5 | Select-Object BrokeringTime, MachineName, ConnectionFailureReason
# CDF tracing / Scout for deep dives; Director > Trends > Failures for the pattern
```

**Expected result:** Failure reasons named by the broker (`None` on a healthy site) — the methodology: Director for the pattern, connection log for the reason, CDF/Scout for the deep dive. Exam scenarios give symptoms and ask for the next tool.

**Negative test:** Put the whole catalog in maintenance mode and launch: the connection log names the refusal cause — a *controlled* failure to practice reading.

**Cleanup:** Exit maintenance mode.

### Lab 4.7 — Hybrid and cloud concepts (module 7)

**Objective:** State the split of responsibilities in a hybrid deployment.

```text
citrix cloud> control plane: brokering, Studio/Director (Web), licensing  — Citrix-managed
resource location> Cloud Connectors x2, VDAs, StoreFront (optional local), Gateway or Gateway Service
```

**Expected result:** A correct division: Citrix operates the control plane; you operate connectors, images, and access. Module 7 scenarios test which failures are yours (connector down, VDA unregistered) versus the platform's, and when local StoreFront/Gateway are kept (sovereignty, HDX routing).

**Negative test:** Assume Gateway Service and lose the direct-HDX requirement your design had — hairpinning session traffic through the cloud POP; the module wants you to catch that trade-off.

**Cleanup:** None (design).

## Summary and Completion Checklist

- [ ] All seven CCP-V modules exercised.
- [ ] HA chain (controllers, LHC, SQL, StoreFront) and the Gateway/STA path drilled.
- [ ] Policy/profile/WEM layering and App Protection configured and reverted.
