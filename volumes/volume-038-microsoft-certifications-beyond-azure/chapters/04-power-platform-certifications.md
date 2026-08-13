# Chapter 04: Power Platform Certifications

## Learning Objectives

- Enumerate the current Power Platform certifications and exam codes.
- Distinguish the maker, developer, analyst, RPA, and architect roles.
- Recognize the PL retirements and the shared-exam relationships with Dynamics 365.
- Map each credential to the underlying Power Platform skills.
- Build a study path for a Power Platform functional or developer role.

## Theory and Architecture

**Power Platform** is Microsoft's low-code suite — **Power Apps**, **Power
Automate**, **Power BI**, **Power Pages**, and **Copilot Studio** — over
**Dataverse**. The **PL** certification family certifies the roles that build
and govern it. As verified on Microsoft Learn (26 July 2026):

- **Microsoft Certified: Power Platform Fundamentals** — exam **PL-900**
  (Fundamentals). The platform's capabilities, Dataverse, and business value.
- **Microsoft Certified: Power Platform Functional Consultant Associate** —
  exam **PL-200** (Associate). Configure Dataverse, apps, automation, and
  Copilot Studio to meet requirements. *Verify status — this credential was
  flagged for change in 2026.*
- **Microsoft Certified: Power BI Data Analyst Associate** — exam **PL-300**
  (Associate). Model, visualize, and analyze data with Power BI.
- **Microsoft Certified: Power Platform Developer Associate** — exam
  **PL-400** (Associate). Extend Power Platform with code — plug-ins, custom
  connectors, and PCF controls.
- **Microsoft Certified: Power Automate RPA Developer Associate** — exam
  **PL-500** (Associate). Robotic process automation with Power Automate
  desktop flows.
- **Microsoft Certified: Power Platform Solution Architect Expert** — exam
  **PL-600** (Expert). Lead the design of Power Platform and Dynamics 365
  solutions end to end.

**PL-100** (App Maker) was retired, and **PL-200** overlaps the **Dynamics
365** functional-consultant credentials, which historically paired a
Dynamics MB exam with PL-200. Confirm the current shared-exam structure on
Learn.

## Design Considerations

Choose by role. **PL-900** is the gateway. Makers and functional consultants
target **PL-200**; **PL-300** is the widely held **Power BI** analyst
credential (relevant well beyond Power Platform teams and overlapping the data
family, Chapter 06); pro-code developers take **PL-400**; automation
specialists take **PL-500**; and solution architects lead with **PL-600**
(Expert), which spans Power Platform *and* Dynamics 365 (Chapter 05).

Because **PL-600** and the Dynamics architect credential (MB-700) both
certify solution architecture, decide which platform centre of gravity the
role has. **PL-300** is a strong standalone analyst credential and a natural
companion to the data and Fabric certifications (Chapter 06).

## Implementation and Automation

Verify the PL family from Microsoft Learn:

```bash
for slug in power-platform-fundamentals power-platform-functional-consultant-associate \
            data-analyst-associate power-platform-developer-associate \
            power-automate-rpa-developer-associate power-platform-solution-architect-expert; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bPL-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# power-platform-functional-consultant-associate -> PL-200 (confirm status)
# data-analyst-associate -> PL-300   (Power BI Data Analyst)
```

## Validation and Troubleshooting

Map credentials to roles and tiers:

| Credential | Exam | Tier | Role |
| --- | --- | --- | --- |
| Power Platform Fundamentals | PL-900 | Fundamentals | Gateway |
| Functional Consultant | PL-200 | Associate | Maker/consultant |
| Power BI Data Analyst | PL-300 | Associate | Analyst |
| Power Platform Developer | PL-400 | Associate | Pro-code developer |
| Power Automate RPA Developer | PL-500 | Associate | Automation |
| Power Platform Solution Architect | PL-600 | Expert | Architect |

Common pitfalls: preparing for **PL-100** (retired); assuming **PL-200** and
the Dynamics functional exams are unrelated (they overlap, and shared-exam
structures change — verify on Learn); and treating **PL-300** as
Power-Platform-only when it is really the general **Power BI** analyst
credential relevant to any data role.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
build in a free **Power Platform developer environment**. Verify **PL-200**'s
current status and any shared-exam relationship with Dynamics 365 before
planning a functional-consultant path. Treat **PL-300** as a cross-family
analyst credential. Renew annually through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for PL-900, PL-200, PL-300, PL-400, PL-500, PL-600.

**Knowledge checks**

1. Which PL credential is the widely held Power BI analyst certification?
2. What does PL-600 span beyond Power Platform?
3. Which PL exam was retired?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the Power Platform family (PL-900, PL-200, PL-300, PL-400, PL-500, PL-600).

**Shared prerequisites** — a Power Platform **developer environment**, the
**Power Platform CLI** (`pac auth create`), and the **MicrosoftPowerBIMgmt**
module for the PL-300 labs. Commands are illustrative walkthroughs; some list
operations use the maker portal when a CLI verb is unavailable. **Cost:** none
on a developer environment.

### Lab 4.1 — PL-900: Describe the business value of Microsoft Power Platform (5–10%)

**Objective:** Confirm access to the low-code platform.

```powershell
pac org who
```

**Expected result:** the connected Dataverse org/URL — the Power Platform
(Apps, Automate, BI, Pages, Copilot Studio) whose business value is rapid
low-code delivery.

**Negative test:** assume Power Platform replaces all pro-code development; it
accelerates low-code, not every scenario.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — PL-900: Manage the Microsoft Power Platform environment (20–25%)

**Objective:** List environments and their types.

```bash
pac env list --output table
```

**Expected result:** environments with type (Default/Production/Sandbox) — the
environment management PL-900 introduces.

**Negative test:** build production apps in the Default environment; use a
dedicated environment with a Dataverse database.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — PL-900: Demonstrate the capabilities of Power Apps (20–25%)

**Objective:** List the apps in the environment.

```bash
pac application list
```

**Expected result:** canvas and model-driven apps — the Power Apps capability.

**Negative test:** treat canvas and model-driven apps as interchangeable;
model-driven is data-first on Dataverse.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — PL-900: Demonstrate the capabilities of Power Automate (20–25%)

**Objective:** List cloud flows.

```bash
pac flow list 2>/dev/null || echo "list flows in the Power Automate portal"
```

**Expected result:** cloud flows in the environment — the Power Automate
capability.

**Negative test:** use a scheduled flow for real-time reaction; an automated
(trigger) flow fires on events.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — PL-900: Describe features and capabilities of agents in Microsoft Copilot Studio (20–25%)

**Objective:** List Copilot Studio agents.

```bash
pac copilot list 2>/dev/null || echo "each Copilot Studio agent is a Dataverse bot record"
```

**Expected result:** Copilot Studio agents — the conversational agents PL-900
now covers.

**Negative test:** deploy an agent with no topics or knowledge; an empty agent
cannot answer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — PL-200: Configure Microsoft Dataverse (25–30%)

**Objective:** List Dataverse tables.

```bash
pac data list-tables 2>/dev/null || pac org who
```

**Expected result:** Dataverse tables (Account, Contact, custom) — the data
platform PL-200 configures.

**Negative test:** back a model-driven app with SharePoint lists; model-driven
apps require Dataverse.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.7 — PL-200: Create apps by using Microsoft Power Apps (25–30%)

**Objective:** Inspect the apps you build.

```bash
pac application list
```

**Expected result:** canvas and model-driven apps — the Power Apps PL-200
creates.

**Negative test:** publish an app without sharing it; unshared apps are
invisible to users.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.8 — PL-200: Create and manage logic and process automation (25–30%)

**Objective:** List solution components (flows/business rules).

```bash
pac solution list
```

**Expected result:** solutions bundling flows and business-process automation —
the logic PL-200 manages.

**Negative test:** build automation outside a solution; un-solutioned components
are hard to move between environments.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.9 — PL-200: Manage environments (15–20%)

**Objective:** Show environment topology (ALM).

```bash
pac env list --output table
```

**Expected result:** environments and their URLs/types — the environment
management (ALM) PL-200 covers.

**Negative test:** develop and run production in one environment; separate
dev/test/prod.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.10 — PL-300: Prepare the data (25–30%)

**Objective:** Shape data with a Power Query M step.

```text
= Table.TransformColumnTypes(
    Table.SelectRows(Source, each [Amount] <> null),
    {{"Amount", type number}} )
```

**Expected result:** a Power Query step removing null rows and typing a column —
data preparation in Power BI.

**Negative test:** model before cleaning; nulls and wrong types corrupt every
downstream measure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.11 — PL-300: Visualize and analyze the data (25–30%)

**Objective:** Write DAX measures for analysis.

```text
Total Sales = SUM(Sales[Amount])
YoY % = DIVIDE([Total Sales] - [Total Sales LY], [Total Sales LY])
```

**Expected result:** a base measure and a year-over-year calculation — the
analysis PL-300 tests.

**Negative test:** use a calculated column where a measure is needed; measures
compute in filter context.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.12 — PL-300: Manage and secure Power BI (15–20%)

**Objective:** List Power BI workspaces (the governance surface).

```powershell
Connect-PowerBIServiceAccount
Get-PowerBIWorkspace | Select-Object Name, Id
```

**Expected result:** workspaces — where you secure Power BI with roles and
row-level security.

**Negative test:** publish a report with no row-level security on sensitive
data; every viewer then sees all rows.

**Rollback:** `Disconnect-PowerBIServiceAccount`.

### Lab 4.13 — PL-400: Create a technical design (10–15%)

**Objective:** Inspect solution components to inform a design.

```bash
pac solution list
```

**Expected result:** solutions and their components — the technical baseline a
PL-400 developer designs against.

**Negative test:** customize directly in the Default solution; use a dedicated
publisher/solution.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.14 — PL-400: Build Power Platform Solutions (10–15%)

**Objective:** Scaffold an unmanaged solution project (ALM).

```bash
pac solution init --publisher-name lab --publisher-prefix lab --outputDirectory ./sln
```

**Expected result:** a solution project scaffold — the ALM artifact PL-400
builds in.

**Negative test:** ship an unmanaged solution to production; export as managed
for target environments.

**Rollback:** `rm -rf ./sln`.

### Lab 4.15 — PL-400: Implement Power Apps improvements (10–15%)

**Objective:** Scaffold a Power Apps Component Framework (PCF) control.

```bash
pac pcf init --namespace lab --name Sample --template field && echo "PCF field scaffold created"
```

**Expected result:** a PCF field control scaffold — extending Power Apps with
code.

**Negative test:** put heavy logic in the canvas formula bar; complex logic
belongs in components/plug-ins.

**Rollback:** remove the scaffold directory.

### Lab 4.16 — PL-400: Extend the user experience (10–15%)

**Objective:** Scaffold a dataset PCF control (UX extension).

```bash
pac pcf init --namespace lab --name UxDemo --template dataset && echo "dataset PCF scaffold"
```

**Expected result:** a dataset PCF scaffold — a supported UX extension point.

**Negative test:** rebuild native grid behavior in canvas when a PCF control
exists; reuse platform components.

**Rollback:** remove the scaffold directory.

### Lab 4.17 — PL-400: Extend the platform (30–35%)

**Objective:** Scaffold a Dataverse plug-in (server-side extension).

```bash
pac plugin init --outputDirectory ./plugin && echo "plug-in project created"
```

**Expected result:** a plug-in project — the server-side extensibility that is
the largest PL-400 domain.

**Negative test:** run long operations synchronously in a plug-in; use
async/child flows to avoid timeouts.

**Rollback:** `rm -rf ./plugin`.

### Lab 4.18 — PL-400: Develop integrations (10–15%)

**Objective:** Confirm the Dataverse Web API endpoint used for integrations.

```bash
pac org who
```

**Expected result:** the Dataverse org URL — the OData Web API endpoint
integrations call.

**Negative test:** poll the Web API for changes; use change tracking/webhooks
for efficient integration.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.19 — PL-500: Design automations (25–30%)

**Objective:** Enumerate connectors to design a flow.

```bash
pac connector list 2>/dev/null | head || echo "browse connectors in the maker portal"
```

**Expected result:** available connectors — the building blocks a flow/RPA
designer chooses.

**Negative test:** design an unattended RPA flow with no service account;
unattended runs need a dedicated identity.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.20 — PL-500: Develop automations (45–50%)

**Objective:** List developed cloud/desktop flows.

```bash
pac flow list 2>/dev/null || echo "list flows via the Power Automate portal/API"
```

**Expected result:** the developed flows — the largest PL-500 domain (cloud +
desktop RPA).

**Negative test:** hard-code credentials in a flow; use connection references
and Key Vault.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.21 — PL-500: Deploy and manage automations (20–25%)

**Objective:** List pipelines/solutions used to deploy automations.

```bash
pac pipeline list 2>/dev/null || pac solution list
```

**Expected result:** pipelines/solutions — deploying and managing automations
across environments.

**Negative test:** recreate a flow manually in prod; export/import via a managed
solution.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.22 — PL-600: Perform solution envisioning and requirement analysis (45–50%)

**Objective:** Inventory apps/tables for as-is requirement analysis.

```bash
pac solution list; pac data list-tables 2>/dev/null | head
```

**Expected result:** existing solutions and tables — the as-is baseline a
solution architect analyzes for requirements.

**Negative test:** design a target with no as-is analysis; requirements must map
to current gaps.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.23 — PL-600: Architect a solution (35–40%)

**Objective:** Review environment topology to architect ALM/data residency.

```bash
pac env list --output table
```

**Expected result:** the environment topology (dev/test/prod, regions) — the
architecture surface PL-600 designs.

**Negative test:** architect an enterprise solution in a single environment; ALM
needs separated environments.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.24 — PL-600: Implement the solution (15–20%)

**Objective:** Import a managed solution to the target (go-live).

```bash
pac solution import --path ./solution_managed.zip 2>/dev/null || echo "import a managed solution to the target environment"
```

**Expected result:** a managed solution imported to the target — the
implementation step.

**Negative test:** implement directly in production with no test import;
validate in test first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Power Platform family runs PL-900 (Fundamentals), PL-200 (Functional
Consultant), PL-300 (Power BI Data Analyst), PL-400 (Developer), PL-500 (RPA
Developer), and PL-600 (Solution Architect Expert). PL-100 retired; PL-200 and
PL-600 overlap Dynamics 365; PL-300 is the cross-family analyst credential.

- [ ] I can list the PL credentials and exam codes.
- [ ] I can distinguish the maker, developer, analyst, RPA, and architect roles.
- [ ] I know PL-100 retired and PL-200/PL-600 relate to Dynamics.
- [ ] I can build a Power Platform study path.
- [ ] I completed Labs 4.1–4.2 including each negative test.
