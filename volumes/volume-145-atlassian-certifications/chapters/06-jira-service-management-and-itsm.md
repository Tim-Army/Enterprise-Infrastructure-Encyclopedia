# Chapter 06: Jira Service Management and ITSM

## Learning Objectives

- Explain how Jira Service Management (JSM) extends Jira for IT service management.
- Configure request types, queues, and SLAs.
- Understand the agent-versus-customer model and why it changes licensing and design.
- Place JSM against the dedicated ITSM platforms.

*Cert relevance: JSM administration appears in the Atlassian certification catalog and shares the Jira admin foundations from Chapters 02–03. This chapter is defensive/operational — service delivery, not attack.*

## What JSM is

**Jira Service Management** is Jira reshaped for **service delivery** — IT help desks, HR service, facilities, any team that receives *requests* from *customers* and works them to resolution against *service-level commitments*. It is built on the same Jira engine (issues, workflows, JQL from Chapters 02–03), which is its distinctive angle: **the same platform your developers plan work in also runs your service desk**, so an escalation flows from a support ticket to an engineering issue without leaving Atlassian.

That integration is JSM's pitch against dedicated ITSM platforms like [ServiceNow (LXXX)](../../volume-080-servicenow-certifications/README.md): ServiceNow is the deep, standalone ITSM incumbent; JSM is ITSM *unified with the development toolchain*. Neither is universally right — the lab's placement section returns to it.

## Request types, queues, SLAs

Three concepts do most of JSM's work:

| Concept | Is | The design question |
|:---|:---|:---|
| **Request type** | The customer-facing form for a kind of request ("reset my password," "request access") | What does the customer see and fill in? |
| **Queue** | An agent-facing filtered view of incoming work (a saved JQL) | How do agents find the work that is theirs? |
| **SLA** | A time commitment on a request (respond in 1h, resolve in 8h), with a clock | What did we promise, and are we meeting it? |

A **request type** presents a simple form to a non-technical customer while mapping, behind the scenes, to a Jira issue type with all its workflow and fields — the customer sees "reset my password," the agent sees a fully-configured issue. **Queues** are JQL (Chapter 03) in service-desk clothing: agents work from queues, and a badly-designed queue set means agents miss or fight over work. **SLAs** attach a clock to commitments, and the lab models the subtlety that trips people up: **SLA clocks pause and resume**, and getting the pause conditions wrong misreports your performance.

## Agents versus customers

JSM's licensing and design both turn on a distinction Jira does not have:

- **Agents** are licensed users who *work* requests — they have JSM agent seats (the expensive ones from Chapter 05's licensing lab).
- **Customers** are *unlicensed* — they raise requests through the portal and get updates, but do not consume a seat. There can be unlimited customers.

This changes design: the **customer portal** must be simple enough for anyone in the company (or the public) to use without training, while the **agent view** carries the full Jira power. Blurring them — exposing Jira complexity to customers, or dumbing down the agent view — breaks both. The lab models sizing an agent team against request volume and SLA, because that is the real capacity question a JSM admin answers.

## Hands-On Lab

Python models JSM. **Cost:** none.

### Lab 6.1 — SLA clocks pause and resume

**Objective:** Compute SLA attainment with correct pause handling.

```bash
python3 - <<'EOF'
from datetime import datetime, timedelta
# A ticket's timeline; the SLA clock should PAUSE while "Waiting for Customer"
EVENTS = [
  ("10:00", "created / clock STARTS"),
  ("10:30", "agent responds, sets Waiting for Customer -> clock PAUSES"),
  ("14:00", "customer replies -> clock RESUMES"),
  ("14:45", "resolved -> clock STOPS"),
]
SLA_TARGET_MIN = 120   # resolve within 2 hours of ACTIVE work
def t(s): return datetime.strptime(s, "%H:%M")
# active time = total elapsed minus the paused window
created, paused_at, resumed_at, resolved = t("10:00"), t("10:30"), t("14:00"), t("14:45")
total_elapsed = (resolved - created).seconds // 60
paused = (resumed_at - paused_at).seconds // 60
active = total_elapsed - paused
print("Ticket timeline:")
for tm, ev in EVENTS: print(f"   {tm}  {ev}")
print(f"\ntotal elapsed (wall clock): {total_elapsed} min")
print(f"paused (waiting on customer): {paused} min")
print(f"ACTIVE time (the SLA clock):  {active} min")
print(f"SLA target: {SLA_TARGET_MIN} min\n")
print(f"By WALL CLOCK: {total_elapsed} min -> SLA BREACHED (looks terrible)")
print(f"By ACTIVE clock: {active} min -> SLA MET (the truth: agent was fast, customer was slow)")
print("\nThe pause matters enormously: the 3.5 hours 'Waiting for Customer' were NOT")
print("the agent team's fault, and counting them would penalize agents for customer")
print("response time they do not control. The SLA clock PAUSES during customer-side")
print("waits and RESUMES when the ball is back with the agent.")
print("\nGetting pause conditions WRONG is the classic JSM misconfiguration:")
print("  - forget to pause on 'Waiting for Customer' -> agents look slow, SLAs breach")
print("    on tickets they handled instantly, and the metric becomes meaningless")
print("  - pause too eagerly (on statuses agents control) -> SLAs look great while")
print("    customers wait, hiding real problems")
print("The admin configures WHICH statuses pause the clock — and it must reflect who")
print("actually holds the ball at each step.")
EOF
```

**Expected result:** A ticket that breaches by wall clock but meets its SLA by active time, because the 3.5-hour customer-wait is correctly paused. The pause-configuration lesson is the JSM admin skill — the clock must pause exactly when the customer holds the ball, and getting it wrong penalizes agents for customer delays or hides real slowness.

**Negative test:** Measuring SLAs by wall-clock time. Agents get penalized for the hours customers take to reply, and the metric stops meaning "how fast is the team."

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Size the agent team

**Objective:** Compute agents needed for a request volume and SLA.

```bash
python3 - <<'EOF'
DAILY_REQUESTS = 340
AVG_HANDLE_MIN = 18            # active agent minutes per request
AGENT_PRODUCTIVE_HRS = 6       # of an 8-hr shift, realistically
PEAK_MULTIPLIER = 1.6          # mornings/Mondays spike
SLA_RESPONSE_MIN = 60          # must respond within an hour

work_min_per_day = DAILY_REQUESTS * AVG_HANDLE_MIN
agent_min_per_day = AGENT_PRODUCTIVE_HRS * 60
base_agents = work_min_per_day / agent_min_per_day
peak_agents = base_agents * PEAK_MULTIPLIER
print(f"daily requests: {DAILY_REQUESTS}, avg handle {AVG_HANDLE_MIN} min")
print(f"total agent-work: {work_min_per_day:,} min/day")
print(f"per agent: {agent_min_per_day} productive min/day\n")
print(f"base agents (average load):  {base_agents:.1f} -> staff {-(-int(base_agents*10)//10)+1 if base_agents%1 else int(base_agents)}")
print(f"peak agents (Monday morning): {peak_agents:.1f} -> need ~{round(peak_agents)} to hold the 60-min SLA")
print("\nThe capacity question a JSM admin actually answers: staff for the AVERAGE")
print("and the SLA breaches every Monday; staff for the PEAK and agents are idle")
print("mid-week. The usual answer is staff near peak with cross-trained overflow, OR")
print("use AUTOMATION (Chapter 03) + self-service (the portal + knowledge base) to")
print("shave the request volume that reaches an agent at all.")
print("\nThe highest-leverage move is often NOT more agents: a good customer portal")
print("with request types that DEFLECT common asks (password resets -> self-service,")
print("FAQs -> linked Confluence pages) reduces DAILY_REQUESTS itself. Every request")
print("a customer resolves without an agent is one you do not staff for.")
print("\nThis ties the volume together: JSM (this chapter) + automation (ch03) +")
print("Confluence knowledge base (ch04) + the org's licensing (ch05) are ONE system.")
EOF
```

**Expected result:** A base agent count that must scale toward the peak to hold the SLA, with deflection (portal, automation, knowledge base) as the higher-leverage alternative to adding agents. The one-system framing is the chapter's synthesis — JSM sizing connects to automation, the Confluence knowledge base, and licensing, all covered earlier.

**Negative test:** Staffing for average daily volume. Every Monday-morning peak breaches the response SLA, and the fix "hire more agents" ignores the cheaper deflection levers.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — JSM versus a dedicated ITSM platform

**Objective:** Place JSM against ServiceNow-class platforms.

```bash
python3 - <<'EOF'
CRITERIA = [
  # criterion,                              weight, JSM, dedicated_ITSM
  ("already on Atlassian (Jira/Confluence)",   5,    5,     2),
  ("dev-to-support ticket flow (one platform)", 5,    5,     2),
  ("deep ITIL process coverage (CMDB, etc.)",   4,    3,     5),
  ("enterprise ITSM breadth (asset, HR, etc.)", 4,    3,     5),
  ("time-to-value / simplicity",               3,    5,     3),
  ("cost at scale",                            3,    4,     2),
]
jsm = sum(w*j for _, w, j, _ in CRITERIA)
itsm = sum(w*i for _, w, _, i in CRITERIA)
print(f"{'criterion':40}{'wt':>4}{'JSM':>6}{'dedicated':>11}")
for c, w, j, i in CRITERIA:
    print(f"{c:40}{w:>4}{j:>6}{i:>11}")
print(f"\n{'WEIGHTED':40}{'':>4}{jsm:>6}{itsm:>11}")
print("\nNeither wins universally — the deciding factor is what you ALREADY run:")
print("  ALREADY ON ATLASSIAN + want dev-to-support flow -> JSM's unification wins.")
print("     The escalation from a support ticket to an engineering Jira issue never")
print("     leaves the platform, and the team already knows the tool.")
print("  NEED DEEP ITIL/enterprise breadth (full CMDB, asset mgmt, HR service, deep")
print("     process) -> a dedicated ITSM platform (ServiceNow, Vol LXXX) goes deeper.")
print("\nJSM's real pitch is INTEGRATION, not feature-depth: 'your service desk and")
print("your dev backlog on one platform' beats 'the deepest standalone ITSM' for")
print("orgs whose support and engineering work is tightly coupled — which is most")
print("software companies. The honest read: JSM for Atlassian-native shops with")
print("dev-coupled support; ServiceNow-class tools for ITSM-first enterprises.")
EOF
```

**Expected result:** JSM winning on Atlassian-native integration and ServiceNow-class platforms winning on ITIL depth, with the decision resting on what the organization already runs. The integration-not-depth framing is JSM's honest positioning — it competes on unifying support with the dev toolchain, not on out-featuring the dedicated ITSM incumbents.

**Negative test:** Choosing JSM for a deep ITIL, CMDB-heavy enterprise ITSM program on its own merits. It is capable but not as deep as the dedicated platforms; the reason to choose it is the Atlassian unification, and if that does not apply, the case weakens.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] JSM understood as Jira reshaped for service delivery, unified with the dev toolchain.
- [ ] Request types, queues, and SLAs configured, with SLA clocks pausing correctly.
- [ ] The agent/customer model understood, with deflection preferred over adding agents.
- [ ] JSM placed against dedicated ITSM by integration versus depth.
