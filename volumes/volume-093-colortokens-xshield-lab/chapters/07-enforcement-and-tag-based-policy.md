# Chapter 07: Enforcement and Tag-Based Policy

## Learning Objectives

- Flip a validated policy from Observe to Enforce.
- Replace address-based rules with tag-based policy.
- Enforce on Windows through the Windows Filtering Platform.
- Reason about EDR-mediated enforcement where no new agent is wanted.

## Hands-On Lab

### Lab 7.1 — Flip from Observe to Enforce

**Objective.** Make the policy real. This is the moment Progressive
Segmentation has been de-risking — you enforce a policy you have already
watched behave correctly in simulation.

**Track 1 — Real Xshield**

**Step 1.** In the console, review the Observe-mode simulation one last
time. Confirm zero legitimate flows are in the would-deny set. This
review is the whole reason Observe exists.

**Step 2.** Move the `app-ctlab` group’s assets (or the specific policy)
from **Observe** to **Enforce**. In Xshield this is a state change on
the asset/policy, not a redeploy.

**Step 3.** Immediately validate both directions: legitimate app→db
still works; attacker win01→db is now denied. Watch the enforced denials
appear in the console.

**Track 2 — Native equivalent — the one-line flip**

The elegance of having built the structure in Observe is that
enforcement is a single change: the trailing `accept` in the
segmentation chain becomes `drop`.

**Step 1.** On `ct-db01`, change Observe to Enforce. Edit
`/etc/nftables.conf` and change the two Observe lines in the
`segmentation` chain:

```bash
sudo sed -i \
  -e 's/tcp dport \$DB_PORT log prefix "XSHIELD-WOULD-DENY db: " level warn accept/tcp dport $DB_PORT log prefix "XSHIELD-ENFORCE-DROP db: " level warn drop/' \
  -e 's/^        accept$/        ip saddr @app_tier accept\n        log prefix "XSHIELD-ENFORCE-DROP other: " level warn drop/' \
  /etc/nftables.conf

```

Review the result before loading — never enforce a rule you have not
read:

```bash
sudo cat /etc/nftables.conf

```

The `segmentation` chain should now read, in effect:

```bash
ip saddr @app_tier tcp dport 5432 accept                       # legit app -> db
tcp dport 5432 log prefix "XSHIELD-ENFORCE-DROP db: " drop     # anyone else -> db: DENIED
ip saddr @app_tier accept                                       # app tier otherwise ok
log prefix "XSHIELD-ENFORCE-DROP other: " drop                 # default-deny

```

**Step 2.** Load it:

```bash
sudo nft -f /etc/nftables.conf

```

**Step 3 — validate the legitimate flow survives.** From `ct-app01`:

```text
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab \
  -c "SELECT name FROM customers;"

```

Expected: the three rows, unchanged. The application is unaffected.

**Step 4 — validate the attack is now denied.** From `ct-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432

```

Expected — now blocked:

```text
TcpTestSucceeded : False

```

And on `ct-db01`, the enforced drop is logged:

```bash
sudo journalctl -k | grep "XSHIELD-ENFORCE-DROP db" | tail -2

```

**Step 5 — the whole-estate proof.** Re-run the reachability matrix from
`ct-app01`:

```text
~/reach.sh

```

The database line has flipped from D1’s `REACH` to `BLOCK` for
illegitimate sources while remaining reachable for the app. Re-run the
attacker’s version from `ct-win01` — the database is now unreachable
from the SCADA station.

**Expected result.** The exact lateral movement demonstrated in D3 is
now blocked, the legitimate application flow is untouched, and each
denial is logged. You moved from flat to segmented without an outage,
because you validated in Observe first.

**Negative test.** Skip the Observe review and enforce a policy that
omits the app→db allow. The application breaks instantly — `psql` from
`ct-app01` times out. Restore from your `C3-base-db` snapshot or reload
the correct ruleset. This is the outage Observe mode exists to prevent,
and feeling it once is the best argument for the discipline.

**Cleanup.** Keep enforcement on `ct-db01`. Optionally repeat E4–E5 for
`ct-app01` to ring-fence the web tier the same way.

### Lab 7.2 — Tag-based policy (Progressive Segmentation, phase 2: tighten)

**Objective.** Replace brittle IP-based rules with
**identity/label-based** policy — the property that makes Xshield policy
survive re-addressing, scaling, and cloud churn.

**Why tags matter**

An IP address is not identity. If `ct-app01` is rebuilt with a new
address, an IP rule silently fails open or closed. Xshield policy is
written against **tags** (labels like `role=app`, `env=prod`,
`tier=db`), and the platform resolves tags to current members
continuously. This is the single biggest operational advantage of a
microsegmentation platform over hand-written firewall rules.

**Track 1 — Real Xshield**

**Step 1.** In the console, apply tags to assets:
`ct-app01 → {role:app, env:lab}`, `ct-db01 → {role:db, env:lab}`,
`ct-win01 → {role:hmi, env:lab}`, `ct-ot01 → {role:plc, env:lab}`.

**Step 2.** Rewrite the ring-fence policy in tag terms: **allow**
`role:app → role:db` **on TCP 5432; deny all other ingress to**
`role:db`**.** Note there is no IP anywhere in the policy.

**Step 3.** Prove tag resolution: in the console, add a hypothetical
second app server, tag it `role:app`, and observe that it is
*immediately* authorized to reach the database with no policy edit.
Remove it afterward. This is the payoff — policy that scales with the
tag, not the address.

**Track 2 — Native equivalent — named sets as tags**

nftables named `set`s are exactly a tag: a named collection of members
that rules reference by name, and whose membership you change without
touching the rules.

**Step 1.** On `ct-db01`, refactor so the rule references the tag, and
membership is managed separately:

```bash
# The rule already says: ip saddr @app_tier tcp dport 5432 accept
# @app_tier IS the tag "role:app". To add a member, you touch the SET, not the RULE:
sudo nft add element inet xshield app_tier { 10.10.20.13 }   # a new 'role:app' host, authorized instantly
sudo nft list set inet xshield app_tier

```

Expected — the new member is authorized with no rule change:

```text
set app_tier {
    type ipv4_addr
    elements = { 10.10.20.11, 10.10.20.13 }
}

```

**Step 2.** Remove the hypothetical member again:

```bash
sudo nft delete element inet xshield app_tier { 10.10.20.13 }

```

**Step 3.** Persist the tag/rule split so it survives reboot — mirror
how Xshield stores policy and membership separately. Keep the *rules* in
`/etc/nftables.conf` and the *tag membership* somewhere the rules load
from. This is the conceptual structure; in production Xshield does it
for you.

**Step 4 — Windows tag equivalent.** On `ct-win01`, a firewall rule
scoped by `-RemoteAddress` is the same idea — the address list is the
tag membership, the rule is the policy:

```powershell
New-NetFirewallRule -DisplayName "XSHIELD role:hmi -> role:plc 502" `
  -Direction Outbound -Action Allow -Protocol TCP -RemotePort 502 `
  -RemoteAddress 10.10.30.50 -Profile Any

```

**Expected result.** Policy expressed against tags/sets, not raw
addresses; adding or removing a member changes authorization with no
rule edit — the operational model that separates a platform from a pile
of firewall rules.

**Negative test.** Write the policy with a hard-coded IP instead of a
tag, then “rebuild” `ct-app01` at a new address (change its netplan to
`.13` and reapply). The application breaks until you hand-edit the rule.
Tags eliminate exactly this failure class — which is why identity-based
policy is the reason to buy the platform.

**Cleanup.** Restore `ct-app01` to `.11` if you changed it, and reapply
its netplan.

### Lab 7.3 — Windows Filtering Platform enforcement (host-agent mode on Windows)

**Objective.** Enforce microsegmentation on the Windows workload the way
the Xshield Windows agent does — by programming the Windows Filtering
Platform — and see the native-firewall-controller prerequisite in
action.

**Background**

The Xshield Windows agent does not ship its own packet filter. It
programs the **Windows Filtering Platform**, the same subsystem the
Windows Defender Firewall uses. That is why Xshield’s documented Windows
prerequisite is that no *other* product — third-party firewall, or a GPO
— controls the native firewall: there can be only one authoritative
controller of WFP. In Track 2 you *are* that controller, using the
`NetSecurity` PowerShell module and `netsh advfirewall`.

**Track 1 — Real Xshield**

With the agent enrolled (Lab 6.2) and tags applied (Lab 7.2), author a policy for
`role:hmi` (ct-win01): **allow outbound TCP 502 to** `role:plc`**; deny
outbound to** `role:db` **and** `role:app`**.** Move it Observe →
Enforce as in E5. The agent translates this into WFP filters; you will
see them in the next Track-2 steps even on a real deployment, because
that is where they land.

**Track 2 — Native equivalent**

**Step 1.** On `ct-win01`, define the segmentation intent for the HMI:
it may reach the PLC on 502 and nothing else east-west. First, allow the
one legitimate flow explicitly:

```powershell
New-NetFirewallRule -DisplayName "XSHIELD allow hmi->plc 502" `
  -Direction Outbound -Action Allow -Protocol TCP -RemotePort 502 `
  -RemoteAddress 10.10.30.50 -Profile Any -Group "Xshield"

```

**Step 2.** Block the lateral movement the HMI should never perform —
reaching the database and the app tier:

```powershell
New-NetFirewallRule -DisplayName "XSHIELD deny hmi->datacenter" `
  -Direction Outbound -Action Block -Protocol TCP `
  -RemoteAddress 10.10.20.11,10.10.20.12 -Profile Any -Group "Xshield"

```

**Step 3.** Verify the rules exist and are enabled:

```powershell
Get-NetFirewallRule -Group "Xshield" |
    Format-Table DisplayName, Direction, Action, Enabled

```

**Step 4 — validate.** The legitimate flow to the PLC still works:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502

```

Expected: `TcpTestSucceeded : True` (subject to Part F, where `ct-gw`
also gets involved).

The lateral movement to the database is now blocked at the source host:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432

```

Expected: `TcpTestSucceeded : False` — blocked outbound by WFP on
`ct-win01` itself, in addition to the inbound block on `ct-db01` from
E5. Defense in depth: the source refuses to send and the destination
refuses to receive.

**Step 5 — inspect the WFP filters** the way you would to troubleshoot a
real agent:

```powershell
netsh advfirewall firewall show rule name="XSHIELD deny hmi->datacenter"

```

For the deep view of the Windows Filtering Platform layer itself:

```powershell
netsh wfp show filters file="C:\Temp\wfp.xml"
# then open C:\Temp\wfp.xml and search for the rule names

```

**Expected result.** The Windows host enforces egress microsegmentation
through WFP: PLC allowed, data-center lateral movement blocked,
verifiable both by connection test and by inspecting the filters —
exactly what the Xshield Windows agent produces.

**Negative test.** Enable a conflicting rule via Local Group Policy
(`gpedit.msc` → Computer Configuration → Windows Settings → Security
Settings → Windows Defender Firewall) that allows all outbound, then
refresh policy. Your `netsh` rules may be overridden or merged
unpredictably — demonstrating exactly why Xshield requires a single
controller of the native firewall. Remove the GPO rule.

**Cleanup.** Keep the rules; Part F builds on the hmi→plc flow. To
remove later:
`Get-NetFirewallRule -Group "Xshield" | Remove-NetFirewallRule`.

### Lab 7.4 — EDR-mediated enforcement **Design Exercise**

**Objective.** Reason correctly about Xshield’s EDR enforcement mode,
which cannot be reproduced in this lab because it requires a licensed
EDR and the Xshield integration. This is a written exercise with a model
answer — no simulation pretending to be the real thing.

**The scenario**

Your organization already runs **CrowdStrike Falcon** on all Windows and
Linux servers. Leadership is allergic to “yet another agent.” You are
evaluating Xshield. `ct-win01` and `ct-app01` already have Falcon;
`ct-db01` does too. The PLC (`ct-ot01`) has nothing and can take
nothing.

**Questions to answer (write your answers before reading the model)**

1. Which enforcement mode should you propose for the three servers, and

```text
why?

```

2. What does EDR-mediated enforcement give you that the host-agent mode

```text
does not, operationally?

```

3. What are the limits — where must you *still* use another mode?
4. How does the per-asset decision rule from E1 apply here?

**Model answer**

1. **EDR-mediated mode** for the three servers. Xshield enforces

```text
through **CrowdStrike, SentinelOne, or Microsoft Defender for
Endpoint** where those agents already run. Since Falcon is already
deployed, Xshield can drive enforcement through it — **no new
agent** to deploy, package, or get change-approved. This directly
answers the “no more agents” objection, which is often the real
blocker to a microsegmentation project.

```

2. Operationally: **no additional software footprint** on the servers

```text
(no new service, no new update stream, no new resource draw), a
**faster rollout** (you are configuring an integration, not
deploying to every host), and **one less agent** for the endpoint
team to maintain and for change control to worry about. The policy
model, tags, Observe→Enforce lifecycle, and flow map are identical
to host-agent mode — only the enforcement delivery differs.

```

3. Limits: EDR-mediated mode only covers assets **that run a supported

```text
EDR**. The PLC runs none and can run none, so it **still requires
the agentless Gatekeeper** (Part F). Any asset without a supported
EDR and without the ability to take the host agent falls back to
Gatekeeper or cloud-native. EDR mode does not extend coverage to
OT/IoT/legacy — that is exactly the gap the Gatekeeper fills, and
why Xshield ships both.

```

4. The E1 rule holds precisely: *can take an agent and you administer

```text
it → host agent; else EDR present → EDR-mediated; … else cannot take
an agent → Gatekeeper.* Here the “EDR present” branch wins for the
three servers because Falcon is already there, and the PLC falls all
the way through to Gatekeeper. One estate, two enforcement modes —
which is the entire Xshield value proposition: breadth of
enforcement under one console and one policy model.

```

**Expected result.** A defensible enforcement design for a mixed estate
that uses EDR mode where an EDR exists and Gatekeeper where no agent is
possible — and the ability to explain the trade-offs to a skeptical
endpoint team.

**Negative test (conceptual).** Propose EDR-mediated mode for the PLC
because “we like not deploying agents.” It has no EDR and can host none
— the mode simply does not apply. Recognizing which mode is
*inapplicable* to an asset is as important as knowing which is best.

## Summary and Completion Checklist

- [ ] Lab 7.1 complete, including its negative test.
- [ ] Lab 7.2 complete, including its negative test.
- [ ] Lab 7.3 complete, including its negative test.
- [ ] Lab 7.4 complete, including its negative test.
