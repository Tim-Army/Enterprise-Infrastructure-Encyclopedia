# Chapter 02: The Automation Success Platform

## Learning Objectives

- Describe the Automation Success Platform and Automation 360.
- Explain the cloud-native, web-based architecture — Control Room, Bot Creators, Bot Runners.
- Distinguish the roles a bot plays — creator, runner, and the devices it drives.
- Understand where AI fits across the platform.

*Cert relevance: every certification sits on this platform; this chapter is the shared architecture they build on.*

## One cloud-native platform

The **Automation Success Platform**, built on **Automation 360**, is Automation Anywhere's unified environment for building, running, and governing automation. Its defining trait is that it is **cloud-native and fully web-based**: you build bots in a **browser**, not a thick desktop client, and the platform is delivered as SaaS (or a private cloud). This matters — it means automations, credentials, and analytics live in one managed place, teams collaborate without installing IDEs, and the vendor updates the platform continuously.

Automation 360 is the successor to Automation Anywhere's earlier desktop-based products, and the pivot to the browser is what enabled the platform to scale across large enterprises and to layer in **AI** ([Ch 5](05-attended-unattended-and-copilot.md), [Ch 7](07-agentic-process-automation.md)). Every certification tier assumes fluency with this platform. The lab models the platform's pieces.

## The core architecture

Automation 360 has three architectural pieces you must know:

- **Control Room** — the **central, web-based brain** ([Ch 4](04-the-control-room.md)). It stores bots, manages users and roles, schedules and deploys automations, holds credentials in a **Credential Vault**, and provides audit and analytics. Everything is orchestrated from here.
- **Bot Creator** — the **development** interface where a developer **builds** a bot (a browser-based visual builder, [Ch 3](03-building-bots.md)). Creators author automations and check them into the Control Room.
- **Bot Runner** — the **execution** agent that **runs** a bot on a machine. A Bot Runner is a licensed device (a VM or desktop) where automations actually execute — driving applications, moving data, clicking through systems.

The flow is **build in a Bot Creator → store/manage in the Control Room → execute on a Bot Runner**. The Control Room is the hub; Creators and Runners connect to it. The lab models the build→manage→run flow.

## Bots and the work they do

The unit of automation is the **bot** — historically a **Task Bot**, the automation logic that performs a process. A bot is a sequence of **actions** (open an app, read a cell, type text, click a button, call an API) operating on **variables** (the data flowing through). Automation 360 also introduced reusable building blocks and packages so bots are modular rather than monolithic scripts.

Bots automate work across the applications a human would use — a **web** app, a **desktop** app, a **terminal**, a **database**, a **spreadsheet**, an **API**. The platform provides **recorders** and pre-built **actions/packages** so you configure interactions instead of coding low-level integrations. Crucially, in Automation 360 the whole thing is version-controlled and centrally governed, not a pile of scripts on someone's laptop. The lab models a bot as actions over variables.

## Where AI fits

The platform is not just RPA plumbing; **AI is layered across it**:

- **Automation Co-Pilot** ([Ch 5](05-attended-unattended-and-copilot.md)) — an AI assistant that helps **developers** build bots faster and helps **business users** run automations in the flow of work.
- **Document Automation** ([Ch 6](06-document-automation.md)) — AI/ML that reads **unstructured documents** (invoices, forms) so bots can process them.
- **AI Agent Studio** ([Ch 7](07-agentic-process-automation.md)) — build **AI agents** and connect **generative AI** models into automations.
- **Process Discovery / Bot Insight** ([Ch 8](08-process-discovery-and-coe.md)) — AI to **find** automation opportunities and **measure** impact.

Because the platform is cloud-native, these AI services plug in centrally and are available to every automation. The result is a platform that spans **deterministic RPA** and **AI-driven automation** on one foundation — exactly the arc from the Essentials/Advanced certs to the AI Automation Engineer cert ([Ch 1](01-the-automation-anywhere-program.md)). The lab maps AI onto the architecture.

## Hands-On Lab

Python models the platform — Control Room, Creators, Runners, and the AI services. **Cost:** none.

### Lab 2.1 — Model the Automation 360 architecture

**Objective:** See build → manage → run, with AI services plugged into the Control Room.

```bash
python3 - <<'EOF'
# Automation 360: Bot Creators BUILD -> Control Room MANAGES -> Bot Runners EXECUTE
class ControlRoom:
    def __init__(self):
        self.bots = {}; self.runners = []; self.vault = {}
        self.ai_services = ["Automation Co-Pilot", "Document Automation", "AI Agent Studio"]
    def check_in(self, name, actions):   # a Creator checks in a bot
        self.bots[name] = actions;        print(f"   Control Room: stored bot '{name}' ({len(actions)} actions)")
    def register_runner(self, device):
        self.runners.append(device);      print(f"   Control Room: registered Bot Runner '{device}'")
    def deploy(self, name, device):       # orchestrate execution on a Runner
        assert name in self.bots and device in self.runners
        print(f"   Control Room: deploy '{name}' -> Runner '{device}' -> executes {self.bots[name]}")

cr = ControlRoom()
print("BUILD (Bot Creator) -> MANAGE (Control Room) -> RUN (Bot Runner):\n")
cr.check_in("invoice_to_erp", ["open ERP", "read invoice", "enter data", "submit"])
cr.register_runner("vm-runner-01")
cr.deploy("invoice_to_erp", "vm-runner-01")
print(f"\n   Credential Vault: (secrets stored centrally, injected at runtime)")
print(f"   AI services plugged into the platform: {cr.ai_services}")
print()
print("The CONTROL ROOM is the cloud-native, web-based hub: it stores bots, registers Bot")
print("RUNNERS (licensed execution devices), holds secrets in the Credential Vault, and")
print("orchestrates deployment. Developers BUILD in browser-based Bot CREATORS; bots EXECUTE")
print("on Bot RUNNERS. AI services (Co-Pilot, Document Automation, AI Agent Studio) plug in")
print("centrally — one platform spanning deterministic RPA and AI-driven automation.")
EOF
```

**Expected result:** A Control Room that stores a checked-in bot, registers a Bot Runner, and deploys the bot to run on it — with a Credential Vault and AI services plugged in centrally. The lesson is the Automation 360 architecture: build in browser-based Bot Creators, manage centrally in the cloud-native Control Room, execute on Bot Runners, with AI services available platform-wide.

**Negative test:** Building bots as standalone scripts on individual laptops with embedded passwords. There is no central governance, no shared credential vault, no audit, and no way to orchestrate at scale; the Control Room is what makes automation an enterprise-governed platform rather than scattered scripts.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The platform placed — the cloud-native, web-based Automation Success Platform on Automation 360.
- [ ] The architecture understood — Control Room (hub), Bot Creators (build), Bot Runners (execute).
- [ ] Bots understood — actions over variables, driving apps a human would use, centrally governed.
- [ ] AI placement understood — Co-Pilot, Document Automation, AI Agent Studio, and analytics across the platform.

## See also

- [Chapter 03 — Building Bots](03-building-bots.md) — authoring automations in a Bot Creator.
- [Chapter 04 — The Control Room](04-the-control-room.md) — the central hub in depth.
- [Volume CXLIX — UiPath](../../volume-149-uipath-certifications/README.md) — the same architecture (Studio/Orchestrator/Robots) on a different platform.
