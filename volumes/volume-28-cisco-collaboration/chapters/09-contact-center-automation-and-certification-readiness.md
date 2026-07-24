# Chapter 09: Contact Center, Automation, and Certification Readiness

## Learning Objectives

- Explain Webex Contact Center architecture: telephony, routing,
  tenant configuration, digital channels, and the AI features CLCCE
  weights
- Position the contact center against the call-queuing features of
  Chapter 04 — when a feature suffices and when a platform is
  needed
- Automate the collaboration estate with its APIs: AXL, the Webex
  APIs, and endpoint/xAPI programmability
- Operate deliberately: upgrades, backups, monitoring, and the
  change discipline collaboration outages punish
- Assemble a personal readiness plan for CLCOR and a chosen
  concentration from the verified blueprints

## Theory and Architecture

### Webex Contact Center: the cloud CX platform

CLCCE (300-830, new in 2026) certifies **Webex Contact Center**, and
its four domains outline the platform:

- **Telephony and Call Routing (30%)** — how calls enter (Cloud
  Connected PSTN, or a **Local Gateway** — a CUBE, Chapter 05
  verbatim — for bring-your-own-carrier), and how routing
  strategies, queues, teams, and skill-based assignment place a
  contact with an agent. This is the contact center's core, and it
  reuses every SIP and dial-plan instinct the volume built.
- **Tenant Configuration and Reporting (30%)** — Control Hub tenant
  setup, users and agent profiles, entry points and queues, and the
  analytics that make a contact center measurable (a contact center
  you cannot report on is not one).
- **Digital Channels (15%)** — chat, email, and social/messaging
  contacts unified with voice into one agent desktop.
- **Advanced Features and AI (25%)** — self-service (virtual agents,
  IVR flows in the flow designer), agent assist, transcription, and
  the AI features reshaping the tier.

### The queuing-versus-platform boundary

Chapter 04's Native Call Queuing and hunt pilots handle front-office
"ring the sales team, queue if busy." A **contact center** is
warranted when you need skills-based routing, agent states and wrap-up,
multichannel, real-time and historical analytics, and workforce
optimization. The exam and the design review both test the boundary:
reaching for UCCX/Webex CC where a hunt group suffices wastes money;
stretching hunt groups to fake a contact center wastes goodwill.
(UCCX/UCCE remain in many estates; the track's certification lens is
now the cloud platform, and this chapter follows it while naming the
on-premises heritage.)

### Automation across the estate

Collaboration is deeply programmable, and the retired CLAUTO exam's
domains map the surfaces:

- **AXL** (Chapter 03) — SOAP/XML provisioning of CUCM: bulk device,
  line, user, and dial-plan operations. The workhorse for
  on-premises lifecycle.
- **Webex APIs** — REST for Control Hub: users, licenses, devices,
  memberships, messaging (bots), and meetings. SCIM for identity
  from the IdP.
- **Endpoint xAPI** — room/desk devices scriptable over SSH/WebSocket
  for macros, in-room automation, and telemetry.
- **Serviceability/RIS/CDR** — operational data APIs feeding the
  monitoring of the next section.

The habits are Volume IX's and Volume XXVII's: idempotent operations,
identity/secrets in a vault not a script, post-condition asserts,
and change artifacts.

### Operations

Collaboration punishes careless change publicly. Upgrades: CUCM
cluster upgrades are rehearsed on the lab cluster, run in windows,
with the publisher and subscribers sequenced and replication
verified between steps; Expressway and CMS follow their own ordered
procedures; Webex updates arrive continuously and are *tracked*, not
controlled — read the release notes so a cloud change is not a
mystery outage. Backups: DRS (Disaster Recovery System) for the UC
apps on a schedule, tested by actual restore to the lab, plus
configuration exports. Monitoring: RTMT/Prime Collaboration or a
telemetry pipeline (CDR/CMR, SIP OPTIONS state, registration counts,
edge health) with alerting — because in collaboration, the users are
otherwise your monitoring, and they are not gentle.

## Design Considerations

- **Contact center sizing and licensing** from concurrent agents and
  channel mix, with PSTN via CCP or Local Gateway chosen on carrier
  and compliance constraints.
- **Automation as the provisioning path**, not a side project: if
  agents/users are added by hand, the estate drifts and the audit
  suffers — pipe AXL/Webex API from the source of truth.
- **Upgrade cadence as risk management**: the estate that fears
  upgrades accumulates security and support debt (the volume's
  recurring theme); a rehearsed pipeline makes currency routine.
- **Observability designed in**: CDR/CMR retention, dashboards, and
  synthetic test calls per site — day-2 in the design, not after
  the first outage.

## Implementation and Automation

AXL bulk pattern (the shape Chapters 03–08 anticipated):

```python
from zeep import Client                 # AXL is SOAP/WSDL
# Provision a batch of agents' phones + lines from a source-of-truth CSV,
# with a post-condition check that each registered.
for row in agents:                      # idempotent: get-then-add/update
    ensure_phone(client, row)           # addPhone or updatePhone
assert all(is_registered(client, r.device) for r in agents), \
    "post-condition: every provisioned device must register"
```

Webex API pattern (Control Hub side):

```bash
# Idempotent license/team assignment via the Webex API
curl -sS https://webexapis.com/v1/people?email=agent@example.lab \
  -H "Authorization: Bearer $TOKEN"            # get-then-patch
# xAPI on a room device (macro deploy over WebSocket) — telemetry + control
```

Upgrade wave (collaboration flavor of Volume XXVII's pattern):

```text
preflight: DRS backup verified, replication=2, cert validity > window,
           OPTIONS trunks up, no active P1
sequence:  publisher -> verify -> subscribers one by one -> verify
           replication + registration between each
edge:      Expressway C then E per Cisco order; CMS per its guide
soak:      test calls per site (synthetic), CMR quality nominal
rollback:  documented per component; DRS restore rehearsed on lab
```

## Validation and Troubleshooting

Contact-center validation is flow-first: a test contact through each
entry point reaching the right queue and agent, reporting rows
appearing, digital channels landing on the same desktop. Its
troubleshooting reuses the whole volume — a CC call that fails at
ingress is Chapter 05 (Local Gateway/CCP) or Chapter 02 (SIP); one
that reaches the queue but not the agent is routing-strategy and
agent-state logic. Automation troubleshooting: AXL faults name the
object and field; Webex API 4xx carry precise messages; the
idempotency test (run twice, second run no-ops) catches the
template-versus-default fights Chapter 03 warned about. Operations
troubleshooting is prevention audited: the backup you did not test
is not a backup, the monitor that never alerted in a drill is not a
monitor — validate both deliberately.

## Security and Best Practices

- Contact center handles customer PII and often recordings:
  encryption, retention policy, and access control are compliance
  obligations, not options — Volume X's controls aimed at CX data.
- API tokens scoped and vaulted, bot accounts least-privileged,
  SCIM as the identity path; no long-lived admin tokens in
  automation.
- Recording and transcription consent and storage handled per
  jurisdiction — the encyclopedia's editorial and privacy
  discipline applies to what you build as much as what you write.

## References and Knowledge Checks

- CLCCE 300-830 v1.0 exam topics (four domains: 30/30/15/25)
- CLAUTO 300-835 v1.1 exam topics (retired February 2026 — kept for
  the record)
- Cisco Webex Contact Center and DevNet collaboration API
  documentation

Knowledge checks:

1. Give two requirements that move a design from Chapter 04 hunt
   queuing to a contact center, and one that does not justify the
   jump.
2. Which chapter's skills configure Webex Contact Center PSTN via a
   Local Gateway, and why is that reuse exact?
3. Why is the twice-run idempotency test the entry bar for AXL and
   Webex automation alike?
4. Build a weight-ordered CLCOR study sequence from this volume's
   README tables and justify the ordering.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in the
CLCCE 300-830 v1.0 exam guide (Collaboration Cloud Customer Experience — Webex
Contact Center) and the CLAUTO 300-835 v1.1 exam guide (Automating Collaboration
Solutions)** — mapped in the volume README's coverage tables. **CLAUTO retired
in the February 2026 restructure**, but collaboration automation remains core to
the track and to CCIE Collaboration; its labs are kept as a complete automation
reference. Labs use the Webex Contact Center admin/APIs, AXL, Finesse, the Webex
REST APIs, device xAPI, and Python. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 9.1–9.45** — a Webex Contact Center tenant with
admin access, a Webex org and API token in `$WBX`, a Unified CM with AXL in
`$AXL`, a Finesse server, collaboration room devices with local xAPI, and a
Python 3 workstation with `git`. **Cost:** none beyond lab resources.

### Lab 9.1 — Describe Webex Contact Center telephony architecture options (CLCCE Objective 1.1)

**Objective:** Read the tenant's voice (telephony) connection option.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/entry-point" 2>/dev/null | jq -r '.data[]?.name'
```

**Expected result:** the entry points and their telephony type — Webex Contact
Center voice connects via **Cisco Bundled PSTN**, **Voice POP bridge (SIP trunk)**,
or a **customer local gateway/CUBE**; the architecture choice determines PSTN
ingress and CVA/IVR media.

**Negative test:** an entry point with no mapped telephony connection cannot
receive PSTN calls — the connection option must be provisioned to the entry point.

**Cleanup:** none (read-only).

### Lab 9.2 — Configure Webex Contact Center telephony integration (CLCCE Objective 1.2)

**Objective:** Map a dial number/entry point to a flow.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/dial-number" 2>/dev/null | jq -r '.data[]? | "\(.number) -> \(.entryPointId)"'
```

**Expected result:** dial numbers bound to entry points — telephony integration
maps a PSTN number to an entry point, which invokes a routing flow; this is the
join between the carrier/trunk and the contact-center logic.

**Negative test:** a dial number with no entry-point mapping rings but never enters
a flow — the number→entry-point→flow chain must be complete.

**Cleanup:** none (read-only).

### Lab 9.3 — Configure inbound and outdial telephony for agents (CLCCE Objective 1.3)

**Objective:** Verify inbound queues and the outdial entry point/ANI.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/outdial-ani" 2>/dev/null | jq -r '.data[]?.name'
```

**Expected result:** the outdial ANI and inbound queues — agents receive inbound
via queues/teams and place outdial calls through an outdial entry point with a
permitted ANI; both are provisioned per tenant/agent profile.

**Negative test:** an agent whose profile lacks outdial permission or a valid ANI
cannot place external calls — the outdial entry point and ANI are prerequisites.

**Cleanup:** none (read-only).

### Lab 9.4 — Configure components to route voice calls (CLCCE Objective 1.4)

**Objective:** Read the flow's queue/team routing components.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/queue" 2>/dev/null | jq -r '.data[]? | "\(.name) \(.channelType)"'
```

**Expected result:** the queues and their routing (skills/teams) — voice routing
uses a flow (Flow Designer) that plays prompts/menus, sets variables, and queues
the contact to a team or skill-based queue with a distribution policy.

**Negative test:** a flow that queues to a team with no available agents and no
overflow leaves callers waiting indefinitely — the routing needs overflow/RONA
handling.

**Cleanup:** none (read-only).

### Lab 9.5 — Troubleshoot voice channels (CLCCE Objective 1.5)

**Objective:** Diagnose a voice-channel failure (no ingress, no agent audio).

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/task?channelType=telephony&from=$FROM&to=$TO" 2>/dev/null | jq '.data[]? | {id, status, wrapUpReason}'
```

**Expected result:** the call tasks and their disposition — no ingress traces to
the dial-number/entry-point/telephony connection; no agent audio traces to the
agent's WebRTC/desktop or network; the task history shows where the contact
stopped.

**Negative test:** blame the flow for calls that never create a task — no task
means the problem is upstream at telephony ingress, not routing.

**Cleanup:** none (read-only).

### Lab 9.6 — Describe network requirements for Webex Contact Center (CLCCE Objective 2.1)

**Objective:** Verify agent-desktop reachability and media requirements.

```bash
curl -s -o /dev/null -w 'ttfb=%{time_starttransfer}\n' "https://desktop.wxcc-us1.cisco.com" 2>/dev/null
! Confirm required domains/ports and WebRTC media reachability for the agent desktop
```

**Expected result:** low latency to the desktop/media edge — agents need the
Webex CC domains/ports open, WebRTC media reachability, and adequate bandwidth per
concurrent agent; blocked media forces failures or poor audio.

**Negative test:** a proxy intercepting WebSocket/WebRTC breaks the agent desktop
state channel; agents drop to "not connected" — the real-time channels must be
allowed.

**Cleanup:** none (read-only).

### Lab 9.7 — Configure Webex Contact Center users (CLCCE Objective 2.2)

**Objective:** Provision an agent and assign profile/team.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/agent" 2>/dev/null | jq -r '.data[]? | "\(.name) \(.teamIds)"'
```

**Expected result:** agents with their multimedia profile and team — a CC user is
a Webex user granted an agent/supervisor role, an agent profile (queues, wrap-up,
outdial), and team membership.

**Negative test:** an agent with no team assignment cannot receive queued contacts
— team/queue mapping is required for routing to reach them.

**Cleanup:** none (read-only).

### Lab 9.8 — Configure the desktop experience (CLCCE Objective 2.3)

**Objective:** Read the desktop layout/profile applied to agents.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/desktop-layout" 2>/dev/null | jq -r '.data[]?.name'
```

**Expected result:** the desktop layouts and profiles — the agent desktop is
customized by a layout (widgets, tabs, custom pages) and desktop profile (which
layout, features, and permissions each team gets).

**Negative test:** a layout referencing a broken custom-widget URL shows an empty
panel — custom desktop widgets must resolve.

**Cleanup:** none (read-only).

### Lab 9.9 — Configure recording (CLCCE Objective 2.4)

**Objective:** Verify the recording schedule/policy.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/recording-schedule" 2>/dev/null | jq -r '.data[]? | "\(.name) \(.percentage)"'
```

**Expected result:** recording schedules and sampling percentage — Webex CC
records calls by schedule/percentage per queue/team, stored for QM/compliance and
retrievable in the Recording Management/Analyzer.

**Negative test:** a recording schedule scoped to a queue that no flow uses records
nothing — the schedule must target active queues.

**Cleanup:** none (read-only).

### Lab 9.10 — Configure visualizations and dashboards (CLCCE Objective 2.5)

**Objective:** Read an Analyzer visualization/dashboard definition.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/analyzer/visualization" 2>/dev/null | jq -r '.data[]?.title' | head
```

**Expected result:** the visualizations/dashboards — the Analyzer builds real-time
and historical reports (queue stats, agent state, CSAT) as visualizations placed
on dashboards, scoped by role.

**Negative test:** a real-time visualization built on a historical-only data source
shows no live data — the data source (real-time vs historical) must match the
report type.

**Cleanup:** none (read-only).

### Lab 9.11 — Configure components to route digital contacts (CLCCE Objective 3.1)

**Objective:** Read the digital (chat/email/social) routing entry points.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/entry-point" 2>/dev/null | jq -r '.data[]? | select(.channelType!="telephony") | "\(.name) \(.channelType)"'
```

**Expected result:** digital entry points and their channel — digital contacts
(chat, email, SMS, social) enter via channel-specific entry points and flows
(Connect/Flow Designer), queuing to digitally-capable agents.

**Negative test:** a digital contact routed to a queue whose agents lack the
digital channel capability never gets answered — agent multimedia profiles must
include the channel.

**Cleanup:** none (read-only).

### Lab 9.12 — Troubleshoot digital channels (CLCCE Objective 3.2)

**Objective:** Diagnose a chat/email/SMS/social channel failure.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/task?channelType=chat&from=$FROM&to=$TO" 2>/dev/null | jq '.data[]? | {id, status}'
```

**Expected result:** the digital tasks and status — a channel not delivering traces
to the channel asset/connector (e.g., the social/SMS integration credentials), the
entry-point/flow mapping, or agent capability; the task history shows where it
stopped.

**Negative test:** a social channel failing because the third-party connector token
expired is an integration problem, not a flow problem — check the channel asset
first.

**Cleanup:** none (read-only).

### Lab 9.13 — Configure advanced voice flow design (CLCCE Objective 4.1)

**Objective:** Add a callback / HTTP-request node to a voice flow.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/flow" 2>/dev/null | jq -r '.data[]?.name'
! In Flow Designer: add Courtesy Callback and an HTTP Request node to a CRM
```

**Expected result:** the flow with advanced nodes — advanced voice flows add
courtesy **callback** (hold the place in queue, call back), **HTTP Request** (query
a CRM/API for screen-pop or routing), and conditional branching for data-driven
routing.

**Negative test:** an HTTP Request node to an API that times out with no error
branch stalls the flow — advanced nodes need error handling.

**Cleanup:** none (read-only).

### Lab 9.14 — Configure advanced digital flow design (CLCCE Objective 4.2)

**Objective:** Add an HTTP request / post-call survey to a digital flow.

```bash
! In Flow Designer (digital): add an HTTP Request node and a post-call survey
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/flow?channelType=chat" 2>/dev/null | jq -r '.data[]?.name'
```

**Expected result:** the digital flow with the survey/HTTP nodes — advanced digital
flows integrate external data (HTTP) and append a **post-call survey** (CSAT) after
the interaction, feeding the Analyzer.

**Negative test:** a post-call survey attached but the channel not configured to
deliver it (e.g., no chat window persistence) yields no responses — the delivery
path must support the survey.

**Cleanup:** none (read-only).

### Lab 9.15 — Describe prebuilt and custom connectors (CLCCE Objective 4.3)

**Objective:** Read the connectors integrating external systems.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/connector" 2>/dev/null | jq -r '.data[]? | "\(.name) \(.type)"'
```

**Expected result:** the connectors — Webex CC ships **prebuilt** connectors (CRM
like Salesforce/ServiceNow, WhatsApp/social) and supports **custom** connectors
(HTTP/API) so flows and the desktop integrate with business systems.

**Negative test:** a prebuilt CRM connector with expired OAuth credentials fails
screen-pop; the desktop shows no customer record — the connector auth must be
current.

**Cleanup:** none (read-only).

### Lab 9.16 — Describe Webex Contact Center APIs (CLCCE Objective 4.4)

**Objective:** Read tasks/agents via the Webex CC APIs.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/v2/task?from=$FROM&to=$TO&pageSize=5" 2>/dev/null | jq '.data[]? | {id, channelType, status}'
```

**Expected result:** tasks returned — the Webex CC APIs expose configuration
(entry points, queues, agents), real-time and historical **tasks**, and
search/analytics, enabling automation and custom reporting/integration.

**Negative test:** a token without the contact-center scope returns `403` — the CC
APIs require the appropriate integration scope.

**Cleanup:** none (read-only).

### Lab 9.17 — Describe AI assistant features (CLCCE Objective 4.5)

**Objective:** Read the AI features enabled for the tenant.

```bash
! Control Hub / Webex CC: AI features — call/topic summarization, transcript topic analytics, agent wellness
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/ai/features" 2>/dev/null | jq '.' 2>/dev/null || echo "see Control Hub AI settings"
```

**Expected result:** the AI features enabled — Webex CC AI provides call
**summarization** (auto wrap-up notes), **topic analytics** across interactions,
and **agent wellness** (burnout signals), each org/policy controlled.

**Negative test:** AI summaries absent because transcription is disabled — the AI
features depend on transcription/recording being enabled.

**Cleanup:** none (read-only).

### Lab 9.18 — Describe the Webex AI Agent (CLCCE Objective 4.6)

**Objective:** Read the AI Agent (self-service bot) configuration.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://api.wxcc-us1.cisco.com/organization/$ORG/ai-agent" 2>/dev/null | jq -r '.data[]?.name' 2>/dev/null || echo "see AI Agent in the CC admin portal"
```

**Expected result:** the AI Agent(s) — the Webex **AI Agent** provides
conversational self-service (voice/digital) that resolves or triages contacts
before escalating to a human, with a handoff carrying context.

**Negative test:** an AI Agent with no escalation path traps callers when it cannot
resolve the query — a human handoff must be configured.

**Cleanup:** none (read-only).

### Lab 9.19 — Git version-control operations (CLAUTO Objective 1.1)

**Objective:** Exercise add, clone, commit, diff, branch, merge.

```bash
git init collab-auto && cd collab-auto
echo "print('axl')" > axl.py && git add axl.py && git commit -m "base"
git switch -c feature && echo "print('axl v2')" > axl.py && git commit -am "v2"
git switch main && git diff feature -- axl.py | head; cd .. && rm -rf collab-auto
```

**Expected result:** the diff between branches — Git tracks collaboration
automation as versioned code (add/commit/branch/merge/diff), the foundation for
reviewing and deploying scripts safely.

**Negative test:** `git push` with no remote configured fails — a remote must be
added before pushing.

**Cleanup:** `rm -rf collab-auto`.

### Lab 9.20 — Describe API styles: REST, RPC, SOAP (CLAUTO Objective 1.2)

**Objective:** Call the same estate three ways.

```bash
# REST (Webex): resource-oriented
curl -s -H "Authorization: Bearer $WBX" https://webexapis.com/v1/people/me | jq .displayName
# SOAP (AXL): XML envelope, method in the body
curl -sk -u $AXL_USER:$AXL_PW -H 'SOAPAction: CUCM:DB ver=14.0' https://$CUCM:8443/axl/ -d @axl-getccmversion.xml | xmllint --format - | head
```

**Expected result:** REST returns JSON resources (Webex); SOAP returns an XML
envelope (AXL); RPC-style APIs call a named method — collaboration mixes all three
(Webex REST, UCM AXL SOAP, Finesse REST), so knowing each style matters.

**Negative test:** send a REST body to the AXL SOAP endpoint; it rejects the payload
— the styles are not interchangeable.

**Cleanup:** none (read-only).

### Lab 9.21 — Describe sync vs async API patterns (CLAUTO Objective 1.3)

**Objective:** Contrast a synchronous AXL call with an async Webex job.

```bash
# synchronous AXL: blocks for the answer
curl -sk -u $AXL_USER:$AXL_PW -H 'SOAPAction: CUCM:DB ver=14.0 listPhone' https://$CUCM:8443/axl/ -d @list-phone.xml -o /dev/null -w '%{time_total}s\n'
# asynchronous Webex bulk job: returns a job id to poll
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings" 2>/dev/null | jq '.items[0] | {id, latestExecutionStatus}'
```

**Expected result:** AXL returns inline; the Webex bulk job returns a status to
poll — large collaboration operations (bulk provisioning) are async; small queries
are synchronous.

**Negative test:** assume a bulk job finished on submit; the devices are not updated
until the job completes — you must poll the job status.

**Cleanup:** none (read-only).

### Lab 9.22 — Interpret Python for collaboration automation (CLAUTO Objective 1.4)

**Objective:** Read a script exercising data types, functions, classes, loops.

```bash
python3 - <<'PY'
class Agent:
    def __init__(self, name, skills): self.name, self.skills = name, skills
    def has(self, s): return s in self.skills
team = [Agent("amy", {"sales"}), Agent("ben", {"support","sales"})]
for a in team:
    print(a.name, "sales" if a.has("sales") else "-")
PY
```

**Expected result:** `amy sales` / `ben sales` — the script uses a class, a method
with a condition, a set (data type), and a loop, the constructs the exam expects
you to interpret in automation scripts.

**Negative test:** reference an undefined attribute; Python raises `AttributeError`
— interpreting the traceback is part of the skill.

**Cleanup:** none.

### Lab 9.23 — Describe Python virtual environments (CLAUTO Objective 1.5)

**Objective:** Create an isolated venv for collaboration SDKs.

```bash
python3 -m venv wbxenv && source wbxenv/bin/activate
pip install -q webexteamssdk 2>/dev/null; which python; deactivate
```

**Expected result:** `which python` points inside `wbxenv/` — a venv isolates SDK
versions (webexteamssdk, zeep for AXL) per project, avoiding dependency conflicts.

**Negative test:** installing an SDK system-wide risks version clashes across
projects — the venv is the isolation that prevents it.

**Cleanup:** `rm -rf wbxenv`.

### Lab 9.24 — Describe infrastructure roles in collaboration (CLAUTO Objective 1.6)

**Objective:** Identify load balancer, firewall, DNS, and reverse-proxy roles.

```bash
nslookup -type=SRV _cisco-uds._tcp.example.com     # DNS service discovery
nslookup -type=SRV _collab-edge._tls.example.com    # reverse-proxy path (Expressway MRA)
```

**Expected result:** the SRV records and edge path — in collaboration, **DNS**
drives service discovery, the **reverse proxy** (Expressway) fronts MRA, the
**firewall** controls edge traversal, and a **load balancer** distributes across
UCM/Expressway nodes; each role is a dependency for automation reaching the right
endpoint.

**Negative test:** automation targeting a single node instead of the load-balanced
VIP fails when that node is down — target the service, not one host.

**Cleanup:** none (read-only).

### Lab 9.25 — Automate UCM MACs with the AXL API (CLAUTO Objective 2.1)

**Objective:** Add/modify a phone/user via AXL from Python (zeep).

```bash
python3 - <<'PY'
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
s=Session(); s.verify=False; s.auth=HTTPBasicAuth("AXLUSER","PW")
c=Client("AXLAPI.wsdl", transport=Transport(session=s))
svc=c.create_service("{http://www.cisco.com/AXL/API/14.0}AXLAPIBinding","https://CUCM:8443/axl/")
print(svc.listPhone({'name':'SEP%'}, returnedTags={'name':'','description':''})['return'] is not None)
PY
```

**Expected result:** the phones listed — AXL automates moves/adds/changes: add/
update/remove phones, lines, and users programmatically, the core of UCM
provisioning automation.

**Negative test:** an `addPhone` referencing a nonexistent device pool throws an
AXL fault — AXL validates referential integrity.

**Cleanup:** remove any test phone added.

### Lab 9.26 — Automate UCM dial plan/cluster with AXL (CLAUTO Objective 2.2)

**Objective:** Query/modify route patterns and cluster config via AXL.

```bash
curl -sk -u $AXL_USER:$AXL_PW -H 'SOAPAction: CUCM:DB ver=14.0 executeSQLQuery' https://$CUCM:8443/axl/ \
  -d '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/14.0"><soapenv:Body><ns:executeSQLQuery><sql>select dnorpattern from routepattern</sql></ns:executeSQLQuery></soapenv:Body></soapenv:Envelope>' | xmllint --format - | head
```

**Expected result:** the route patterns via AXL SQL — AXL automates dial-plan and
cluster configuration (route patterns, partitions, CSS, service parameters) and can
run read `executeSQLQuery`/thin SQL for reporting.

**Negative test:** an `executeSQLUpdate` on a production table without care can
corrupt the dial plan — prefer the typed AXL methods over raw SQL updates.

**Cleanup:** none (read-only query).

### Lab 9.27 — Describe UCM CTI APIs TAPI/JTAPI (CLAUTO Objective 2.3)

**Objective:** Read the CTI application-user association that TAPI/JTAPI needs.

```text
admin:show risdb query ctimgr
admin:run sql select name from applicationuser where name like '%jtapi%' or name like '%cti%'
```

**Expected result:** the CTI manager and CTI application user — **TAPI** (Windows)
and **JTAPI** (Java) let applications monitor and control calls (screen-pop, click-
to-dial, contact-center) via CTI; the app user must have CTI control of the
devices.

**Negative test:** a JTAPI app whose user lacks "Standard CTI Enabled" and device
control cannot observe/control calls — the CTI permissions are the gate.

**Cleanup:** none (read-only).

### Lab 9.28 — Describe the UCM Serviceability Perfmon API and RTMT (CLAUTO Objective 2.4)

**Objective:** Read a performance counter via the Perfmon (RIS/SOAP) API.

```bash
curl -sk -u $AXL_USER:$AXL_PW -H 'SOAPAction: perfmonCollectCounterData' \
  "https://$CUCM:8443/perfmonservice2/services/PerfmonService" \
  -d @perfmon-collect.xml 2>/dev/null | xmllint --format - | head
```

**Expected result:** counter samples (e.g., registered phones, CPU) — the
Serviceability Perfmon SOAP API exposes the same counters RTMT graphs, so scripts
can pull performance/health data for dashboards and alerting.

**Negative test:** collect a counter with a bad object/instance name; the service
returns a fault — counter names must match the Perfmon schema.

**Cleanup:** none (read-only).

### Lab 9.29 — Describe the IP Phone Services API (CLAUTO Objective 2.5)

**Objective:** Read/serve an IP Phone Services XML object to a phone.

```bash
curl -s "http://$PHONESVC/services/menu" 2>/dev/null | xmllint --format - | head
! Phone requests CiscoIPPhoneMenu/Text/Input XML objects over HTTP
```

**Expected result:** a `CiscoIPPhone*` XML object — the IP Phone Services API
serves XML (menus, text, input, directories, images) that phones render, enabling
custom on-phone applications and integrations.

**Negative test:** malformed `CiscoIPPhone` XML shows an "XML error" on the phone —
the phone strictly parses the schema.

**Cleanup:** none (read-only).

### Lab 9.30 — Describe Finesse REST APIs and gadgets (CLAUTO Objective 2.6)

**Objective:** Read agent/dialog state via the Finesse REST API.

```bash
curl -sk -u agent:PW "https://$FINESSE/finesse/api/User/agent" | xmllint --format - | head
```

**Expected result:** the agent's Finesse state — the Finesse REST API exposes user,
dialog, queue, and team resources; **gadgets** (OpenSocial) embed custom UI in the
agent desktop, both used to build contact-center integrations.

**Negative test:** a gadget calling a Finesse API without the agent's authenticated
session gets `401` — gadgets act within the agent's authenticated context.

**Cleanup:** none (read-only).

### Lab 9.31 — Describe Webex REST API capabilities and authentication (CLAUTO Objective 3.1)

**Objective:** Authenticate and read identity via the Webex REST API.

```bash
curl -s -H "Authorization: Bearer $WBX" https://webexapis.com/v1/people/me | jq '{displayName, emails}'
```

**Expected result:** the authenticated identity — the Webex REST API uses OAuth
bearer tokens (integration, bot, or personal), is resource-oriented (people, rooms,
messages, meetings, devices), and rate-limited; auth scope governs access.

**Negative test:** an expired/invalid token returns `401`; an out-of-scope call
returns `403` — the token and its scopes gate every call.

**Cleanup:** none (read-only).

### Lab 9.32 — Implement admin operations on Webex org/users/licenses (CLAUTO Objective 3.2)

**Objective:** Assign a license/role to a user via the API.

```bash
UID=$(curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/people?email=labuser@example.com" | jq -r '.items[0].id')
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/people/$UID" | jq '{licenses, roles}'
```

**Expected result:** the user's licenses/roles — admin automation provisions users,
assigns licenses (Calling/Meetings/Messaging) and roles, and manages org settings
programmatically for scale.

**Negative test:** an admin token lacking org-admin scope cannot modify other users
— administrative operations require an admin-scoped token.

**Cleanup:** revert any test license change.

### Lab 9.33 — Automate Webex spaces and memberships in Python (CLAUTO Objective 3.3)

**Objective:** Create a space and add members via the SDK.

```bash
python3 - <<'PY'
from webexteamssdk import WebexTeamsAPI
api=WebexTeamsAPI(access_token="TOKEN")
room=api.rooms.create("Automation Lab")
api.memberships.create(roomId=room.id, personEmail="teammate@example.com")
print("created", room.id)
PY
```

**Expected result:** the created space with a member — `webexteamssdk` wraps the
REST API so a few lines create spaces, add members, and post content, the core of
messaging automation.

**Negative test:** add a member the org's external policy blocks; the SDK raises an
API error — org policy still applies to automation.

**Cleanup:** `api.rooms.delete(room.id)`.

### Lab 9.34 — Implement notifications in Python (CLAUTO Objective 3.4)

**Objective:** Post an automated notification message to a space.

```bash
python3 - <<'PY'
from webexteamssdk import WebexTeamsAPI
api=WebexTeamsAPI(access_token="TOKEN")
api.messages.create(roomId="ROOMID", markdown="**Alert:** UCM CPU > 80% on pub")
print("sent")
PY
```

**Expected result:** the markdown notification posted — a common automation is
pushing alerts (from monitoring, CI, or scripts) into a Webex space via the
messages API for team visibility.

**Negative test:** post to a room the token's identity is not a member of; the API
returns `404` — the bot/user must be in the space.

**Cleanup:** delete the test message.

### Lab 9.35 — Implement interactive bots with buttons and cards (CLAUTO Objective 3.5)

**Objective:** Post an Adaptive Card with an action button.

```bash
curl -s -X POST -H "Authorization: Bearer $BOT" -H 'Content-Type: application/json' \
  https://webexapis.com/v1/messages -d '{"roomId":"ROOMID","markdown":"choose",
  "attachments":[{"contentType":"application/vnd.microsoft.card.adaptive","content":{"type":"AdaptiveCard","version":"1.2","body":[{"type":"TextBlock","text":"Approve?"}],"actions":[{"type":"Action.Submit","title":"Approve","data":{"a":"ok"}}]}}]}' | jq '{id}'
```

**Expected result:** the card posted with a button — interactive bots use Adaptive
Cards (buttons/inputs) and receive submissions via an `attachmentActions` webhook,
building approval/self-service workflows in Webex.

**Negative test:** an `Action.Submit` with no webhook to receive
`attachmentActions` does nothing on click — the bot must subscribe to the action
webhook.

**Cleanup:** delete the test message.

### Lab 9.36 — Describe Webex bots, embedded apps, guest issuer, integrations (CLAUTO Objective 3.6)

**Objective:** Distinguish the Webex app/identity types.

```bash
curl -s -H "Authorization: Bearer $BOT" https://webexapis.com/v1/people/me | jq '{type, displayName}'
```

**Expected result:** `type: bot` for a bot token — Webex has **bots** (own
identity, added to spaces), **integrations** (act as a user via OAuth),
**embedded apps** (run inside the Webex client), and **guest issuer** (JWT for
unauthenticated external users); each fits a different automation pattern.

**Negative test:** use a bot token expecting to act as a specific user; bots have
their own identity and cannot impersonate users — an integration (OAuth) is needed
for user-context actions.

**Cleanup:** none (read-only).

### Lab 9.37 — Embed Webex messaging with Widgets (CLAUTO Objective 3.7)

**Objective:** Read the Widgets embed configuration for a web app.

```bash
! The Webex Widgets (webex-widgets) embed a space/calling into a web page via a token
curl -s https://unpkg.com/@webex/widgets 2>/dev/null -o /dev/null -w '%{http_code}\n'
echo "embed: <webex-space accessToken=... spaceId=...></webex-space>"
```

**Expected result:** the Widgets library reachable and the embed element — Webex
**Widgets** embed messaging/calling/meetings UI into a custom web application with
a user access token, so developers add collaboration without building the UI.

**Negative test:** embed a widget with an expired token; it renders an auth error —
the widget needs a valid user token at load.

**Cleanup:** none (read-only).

### Lab 9.38 — Describe the Webex SDKs (CLAUTO Objective 3.8)

**Objective:** Identify the SDKs for each platform.

```bash
python3 -c "import webexteamssdk; print('python sdk', webexteamssdk.__version__)" 2>/dev/null || echo "pip install webexteamssdk"
```

**Expected result:** the Python SDK version — Webex offers SDKs across languages
(Python `webexteamssdk`, Node, browser/JS, iOS/Android calling SDKs) that wrap the
REST APIs and (for calling SDKs) media, so automation and apps use idiomatic
libraries.

**Negative test:** an SDK version predating an API feature lacks the method; upgrade
the SDK — the SDK must track the API.

**Cleanup:** none.

### Lab 9.39 — Automate room devices with xAPI (CLAUTO Objective 4.1)

**Objective:** Drive a collaboration room device directly via its local xAPI.

```bash
curl -sk -u admin:PW "https://$DEVICE/getxml?location=/Status/SystemUnit/Software/Version" | xmllint --format -
curl -sk -u admin:PW -H 'Content-Type: text/xml' "https://$DEVICE/putxml" \
  -d '<Command><Standby><Deactivate/></Standby></Command>'
```

**Expected result:** the device software version and a wake command accepted — the
on-device **xAPI** (over HTTP/SSH/WebSocket) reads Status, sets Configuration, and
runs Commands, so scripts control endpoints directly (or via the cloud xAPI).

**Negative test:** a `putxml` command the device does not support returns an error
element — the xAPI command schema is device/version specific.

**Cleanup:** none (Standby Deactivate is benign).

### Lab 9.40 — Monitor room device events with xAPI (CLAUTO Objective 4.2)

**Objective:** Subscribe to device events (call state, UI) via xAPI feedback.

```bash
curl -sk -u admin:PW "https://$DEVICE/getxml?location=/Status/Call" | xmllint --format - | head
! Register HttpFeedback (or WebSocket) to receive Event/Status change notifications
```

**Expected result:** the current call status and an event subscription — xAPI
**feedback** pushes events (incoming call, macro action, sensor) to a listener, so
automation reacts to the device in real time (e.g., logging, room automation).

**Negative test:** an HttpFeedback URL that is unreachable stops receiving events;
the device drops the registration — the listener must be reachable.

**Cleanup:** deregister the test feedback.

### Lab 9.41 — Deploy custom controls for room devices (CLAUTO Objective 4.3)

**Objective:** Read a UI-extension (custom control) and its macro.

```bash
curl -sk -u admin:PW "https://$DEVICE/getxml?location=/Status/UserInterface/Extensions" | xmllint --format - | head
```

**Expected result:** the deployed UI extensions (panels/buttons) — custom controls
add buttons/panels to the device touch UI, wired to **macros** (on-device
JavaScript) or xAPI, to trigger room automation (lights, blinds, presets).

**Negative test:** a UI extension whose macro was removed shows the button but does
nothing — the control and its macro must both be present.

**Cleanup:** none (read-only).

### Lab 9.42 — Describe room-device deployment (CLAUTO Objective 4.4)

**Objective:** Read the device's provisioning/registration mode.

```bash
curl -sk -u admin:PW "https://$DEVICE/getxml?location=/Status/Provisioning" | xmllint --format -
```

**Expected result:** the provisioning mode (Webex cloud, UCM, or Expressway/edge) —
room devices deploy registered to Webex (Control Hub), to on-prem UCM, or via
Expressway; deployment automation sets provisioning, config, and macros at scale.

**Negative test:** a device set to Webex provisioning but activated with a UCM
config mismatches; it fails to register — the provisioning mode and config must
agree.

**Cleanup:** none (read-only).

### Lab 9.43 — Describe the Webex Meetings REST API (CLAUTO Objective 5.1)

**Objective:** Read meetings/recordings via the API.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/meetings?max=3" | jq -r '.items[]? | "\(.title) \(.state)"'
```

**Expected result:** the meetings and state — the Webex Meetings REST API manages
meetings and webinars (create, update, list, invitees, recordings, transcripts) for
scheduling and reporting automation.

**Negative test:** list meetings for another host without delegate/admin scope
returns only your own — cross-user access needs the right scope.

**Cleanup:** none (read-only).

### Lab 9.44 — Implement meetings management via REST (CLAUTO Objective 5.2)

**Objective:** Create and update a meeting programmatically.

```bash
MID=$(curl -s -X POST -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' https://webexapis.com/v1/meetings -d '{"title":"Auto Mtg","start":"2026-08-02T17:00:00Z","end":"2026-08-02T17:30:00Z"}' | jq -r .id)
curl -s -X PUT -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' "https://webexapis.com/v1/meetings/$MID" -d '{"title":"Auto Mtg (updated)","start":"2026-08-02T18:00:00Z","end":"2026-08-02T18:30:00Z"}' | jq '{id,title}'
```

**Expected result:** the meeting created then updated — meetings-management
automation schedules, reschedules, and cancels meetings/webinars and manages
invitees and registration at scale.

**Negative test:** a PUT with an end time before the start returns a validation
error — the API enforces meeting-time sanity.

**Cleanup:** `DELETE /v1/meetings/$MID`.

### Lab 9.45 — Configure Cisco Meeting Server via REST (CLAUTO Objective 5.3)

**Objective:** Read/create a CMS coSpace via its REST API.

```bash
curl -sk -u admin:PW "https://$CMS:8443/api/v1/coSpaces" | xmllint --format - | head
curl -sk -u admin:PW -X POST "https://$CMS:8443/api/v1/coSpaces" --data "name=LabSpace&uri=labspace"
```

**Expected result:** the coSpaces list and a created space — the Cisco Meeting
Server REST API manages coSpaces, calls, participants, and call legs, so meeting
spaces and in-call control are automated (provisioning, dynamic conferences).

**Negative test:** create a coSpace with a `uri` already in use; CMS returns a
duplicate error — coSpace URIs must be unique.

**Cleanup:** `DELETE /api/v1/coSpaces/<id>` for the test space.

## Lab Verification

Verification means the contact routed and reported, the automation
was idempotent from vaulted secrets, the backup restored (or the
procedure is rehearsed and documented), monitoring alerted on
demand, and the study plan exists. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The contact center is the estate's most demanding tenant — routing,
tenancy, digital channels, and AI — built on every skill the volume
taught; automation through AXL and the Webex APIs makes the estate
provisionable and auditable; and operations rehearsed turns upgrades
and recovery from feared events into routine ones. With core and
five concentrations verified, mapped, and practiced, the CCNP
Collaboration track is yours to schedule.

- [ ] I can place the hunt-group-versus-contact-center boundary and
      defend it
- [ ] My automation is idempotent, vaulted, and assert-checked
- [ ] My backup restored and my monitor alerted in a drill
- [ ] My exam plan is weight-ordered against the verified blueprints
