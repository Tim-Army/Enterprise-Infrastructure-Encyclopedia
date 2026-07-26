# Chapter 05: Dynamics 365 Certifications

## Learning Objectives

- Distinguish the Dynamics 365 Customer Engagement and Finance and Operations tracks.
- Enumerate the current MB-family certifications and exam codes.
- Explain the relationship between Dynamics functional exams and Power Platform.
- Recognize the newer AI-oriented Dynamics credentials.
- Build a study path for a Dynamics 365 functional consultant or architect.

## Theory and Architecture

**Dynamics 365** is Microsoft's business-applications suite, split into two
worlds. **Customer Engagement (CE)** — Sales, Customer Service, Field Service,
Customer Insights — is built on **Dataverse** and the **Power Platform**, so
its functional exams relate closely to the PL family. **Finance and
Operations (F&O)** — Finance, Supply Chain Management, Commerce — is the ERP
side with its own developer and architect exams. The **MB** family certifies
functional consultants, developers, and architects across both.

As verified on Microsoft Learn (26 July 2026), current MB credentials
include the **Fundamentals** pair — **MB-910** (Dynamics 365 Fundamentals,
Customer Engagement apps / CRM) and **MB-920** (Dynamics 365 Fundamentals,
Finance and Operations apps / ERP) — and functional/developer/architect
credentials such as:

- **Customer Service Functional Consultant** — **MB-230** (Associate).
- **Field Service Functional Consultant** — **MB-240** (Associate).
- **Customer Experience Analyst** — **MB-280** (Associate; the evolution of
  the Sales/Marketing functional line).
- **Supply Chain Management Functional Consultant** — **MB-330** (Associate),
  with the **Manufacturing** variant on **MB-300 + MB-320** and the **Expert**
  on **MB-335**.
- **Commerce Functional Consultant** — **MB-300 + MB-340** (Associate).
- **Finance and Operations Apps Developer** — **MB-500** (Associate).
- **Finance and Operations Apps Solution Architect Expert** — **MB-700**
  (Expert).
- **Business Central Functional Consultant** — **MB-800** (Associate) — and
  **Business Central Developer** — **MB-820** (Associate).

Newer **AI-oriented** Dynamics credentials have appeared — for example a
**Dynamics 365 Sales AI Consultant** and a **Dynamics 365 Contact Center AI
Engineer** (beta) — reflecting Copilot's spread into business apps. Confirm
these on Learn, as several are beta or recently added. **MB-901** (an older
Fundamentals exam) and **MB-600** (the CE + Power Platform Solution Architect,
whose scope moved to **PL-600**) are retired.

## Design Considerations

Choose the **track** first. A **CE** consultant works in Sales/Service/Field
Service/Customer Insights on Dataverse and Power Platform, so their path
crosses the **PL** family (Chapter 04) — historically a CE functional
credential paired a Dynamics MB exam with **PL-200**. An **F&O** professional
works in Finance/SCM/Commerce, with **MB-500** (developer) and **MB-700**
(architect Expert). **Business Central** is a distinct small-and-mid-market ERP
with its own **MB-800/MB-820**.

Sequence **MB-910 (CRM) or MB-920 (ERP) Fundamentals → the role's Associate →
the Expert architect (MB-700 for F&O, or PL-600 for CE + Power Platform)**.
Watch the **AI additions** — Copilot-driven roles are being certified, and
several are beta.

## Implementation and Automation

Verify the fundamentals and a functional exam from Microsoft Learn:

```bash
for slug in d365-fundamentals-customer-engagement-apps-crm \
            d365-fundamentals-finance-and-operations-apps-erp \
            d365-functional-consultant-supply-chain-management \
            d365-fundamentals; do
  code=$(curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$slug/" \
    | grep -oE '\bMB-[0-9]{3}\b' | sort -u | tr '\n' ' ')
  echo "$slug -> ${code:-'(assessment/beta - see page)'}"
done
# d365-functional-consultant-supply-chain-management -> MB-330
```

## Validation and Troubleshooting

Map the main credentials to tracks:

| Credential | Exam(s) | Track |
| --- | --- | --- |
| D365 Fundamentals (CRM) | MB-910 | Customer Engagement |
| D365 Fundamentals (ERP) | MB-920 | Finance and Operations |
| Customer Service Functional Consultant | MB-230 | CE |
| Field Service Functional Consultant | MB-240 | CE |
| Customer Experience Analyst | MB-280 | CE |
| Supply Chain Management FC | MB-330 (Expert MB-335) | F&O |
| Commerce Functional Consultant | MB-300 + MB-340 | F&O |
| F&O Apps Developer | MB-500 | F&O |
| F&O Apps Solution Architect Expert | MB-700 | F&O |
| Business Central Functional Consultant / Developer | MB-800 / MB-820 | BC |

Common pitfalls: studying **MB-901** or **MB-600** (retired); missing that CE
functional roles overlap **Power Platform** (PL-200/PL-600); assuming a single
exam where a credential needs two (Commerce and some SCM paths pair **MB-300**
with a specialty exam); and overlooking the **beta AI** Dynamics credentials.
Confirm every code on Learn — the Dynamics family is large and changes often.

## Security and Best Practices

Prepare with **Microsoft Learn** paths and **free practice assessments**, and
practice in a **Dynamics 365 trial** environment. Because the CE track leans
on **Power Platform**, plan MB and PL together; because F&O is its own world,
keep that path separate. Confirm the **shared-exam** structures (MB-300 pairs)
and the **AI/beta** additions on Learn before committing. Renew annually
through the free assessment.

## References and Knowledge Checks

- Microsoft Learn: certification pages for MB-910, MB-920, MB-230, MB-240, MB-280, MB-330/335, MB-500, MB-700, MB-800, MB-820.
- Cross-reference: [Chapter 04 — Power Platform](04-power-platform-certifications.md).

**Knowledge checks**

1. What is the difference between the CE and F&O tracks, and why does CE overlap Power Platform?
2. Which two Fundamentals exams anchor the Dynamics family?
3. Which retired Dynamics architect exam had its scope moved to PL-600?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted "skills measured" domain**
of the Dynamics 365 exams that publish a study guide (MB-910, MB-920, MB-230,
MB-240, MB-280, MB-330, MB-335, MB-500, MB-700, MB-800, MB-820). *(Commerce —
MB-300 + MB-340 — publishes no standalone study guide and so has no per-domain
labs here; confirm on Microsoft Learn.)*

**Shared prerequisites** — for the **customer-engagement (CE)** apps, a
Dataverse **developer environment**, the **Power Platform CLI** (`pac`), and the
Dataverse **Web API** (queries shown as `GET {org}/api/data/v9.2/…`); for
**finance-and-operations (F&O)** apps, the Visual Studio F&O dev tools and
Lifecycle Services (**X++** shown); for **Business Central**, the **AL** Language
extension in VS Code. Commands and snippets are illustrative walkthroughs.
**Cost:** none on a developer environment.

### Lab 5.1 — MB-910: Describe Dynamics 365 Customer Insights (15–20%)

**Objective:** Find the Customer Insights journey/segment tables in Dataverse.

```bash
pac data list-tables 2>/dev/null | grep -iE 'segment|journey|contact' | head
```

**Expected result:** Customer Insights tables (segments, journeys) — the
marketing/data app MB-910 introduces.

**Negative test:** expect Customer Insights to work without unified customer
data; it needs data sources mapped first.

**Cleanup:** none.

### Lab 5.2 — MB-910: Describe Dynamics 365 Sales (20–25%)

**Objective:** Query the Sales pipeline tables.

```http
GET {org}/api/data/v9.2/opportunities?$select=name,estimatedvalue&$top=5
```

**Expected result:** opportunity records with estimated value — the Sales
pipeline app.

**Negative test:** treat a lead and an opportunity as the same; a lead is
qualified *into* an opportunity.

**Cleanup:** none.

### Lab 5.3 — MB-910: Describe Dynamics 365 Customer Service (20–25%)

**Objective:** Query the case (incident) table.

```http
GET {org}/api/data/v9.2/incidents?$select=title,statecode&$top=5
```

**Expected result:** case records with state — the Customer Service app's core
entity.

**Negative test:** resolve a case with an open child activity; some
configurations block resolution until activities close.

**Cleanup:** none.

### Lab 5.4 — MB-910: Describe Dynamics 365 Field Service (15–20%)

**Objective:** Query the work-order table.

```http
GET {org}/api/data/v9.2/msdyn_workorders?$select=msdyn_name&$top=5
```

**Expected result:** work orders — the Field Service scheduling unit.

**Negative test:** schedule a work order with no bookable resource; scheduling
requires resources and requirements.

**Cleanup:** none.

### Lab 5.5 — MB-910: Explore the core capabilities of customer engagement apps in Dynamics 365 (15–20%)

**Objective:** List the model-driven CE apps.

```bash
pac application list
```

**Expected result:** model-driven apps (Sales Hub, Customer Service Hub) — the
shared Dataverse/Power Platform foundation of CE.

**Negative test:** assume CE apps run on their own database; they all share
Dataverse.

**Cleanup:** none.

### Lab 5.6 — MB-920: Describe Dynamics 365 Supply Chain Management (35–40%)

**Objective:** Identify F&O released-product data entities (SCM core).

```text
Data entity: ReleasedProductsV2  (product master)
Modules: Product information, Inventory, Warehouse, Production, Planning
```

**Expected result:** the released-product entity and SCM module map — the F&O
supply-chain scope MB-920 describes.

**Negative test:** treat CE product records as F&O released products; F&O uses
its own data model.

**Cleanup:** none.

### Lab 5.7 — MB-920: Describe Dynamics 365 Finance (30–35%)

**Objective:** Map the Finance general-ledger structure.

```text
Chart of accounts -> Main accounts -> Ledger (legal entity)
Journals: General journal, AP/AR, Fixed assets
```

**Expected result:** the GL/chart-of-accounts structure — Finance's core.

**Negative test:** post to a closed fiscal period; period status must be open.

**Cleanup:** none.

### Lab 5.8 — MB-920: Describe the core capabilities of the finance and operations apps (25–30%)

**Objective:** Identify the legal-entity (company) concept in F&O.

```text
Legal entity (DataAreaId, e.g., USMF) -> shared vs company-specific data
Cross-company data via virtual entities / OData $filter=dataAreaId eq 'usmf'
```

**Expected result:** the legal-entity model — the multi-company core of F&O.

**Negative test:** expect data to be shared across all legal entities by
default; most data is company-specific.

**Cleanup:** none.

### Lab 5.9 — MB-230: Manage cases in Customer Service (51–55%)

**Objective:** Create and read a case (the dominant MB-230 domain).

```http
POST {org}/api/data/v9.2/incidents  { "title": "Lab case", "customerid_account@odata.bind": "/accounts(<id>)" }
GET  {org}/api/data/v9.2/incidents?$filter=title eq 'Lab case'&$select=title,ticketnumber
```

**Expected result:** a created case with an auto `ticketnumber` — case lifecycle
management.

**Negative test:** create a case with no customer; the `customerid` lookup is
required.

**Cleanup:** `DELETE {org}/api/data/v9.2/incidents(<id>)`.

### Lab 5.10 — MB-230: Configure representative experience and routing (25–30%)

**Objective:** Inspect queues and routing rule sets.

```http
GET {org}/api/data/v9.2/queues?$select=name&$top=5
```

**Expected result:** service queues — the routing targets for unified routing.

**Negative test:** route work with no capacity profile; unified routing needs
agent capacity configured.

**Cleanup:** none.

### Lab 5.11 — MB-230: Extend Customer Service (15–20%)

**Objective:** Read SLA / entitlement configuration.

```http
GET {org}/api/data/v9.2/slas?$select=name,applicablefrom&$top=5
```

**Expected result:** SLA definitions — the entitlement/SLA extension of Customer
Service.

**Negative test:** apply an SLA with no business hours; SLA timers need a
calendar.

**Cleanup:** none.

### Lab 5.12 — MB-240: Configure field service applications (20–25%)

**Objective:** Read Field Service settings.

```http
GET {org}/api/data/v9.2/msdyn_fieldservicesettings?$top=1
```

**Expected result:** the Field Service settings record — global FS
configuration.

**Negative test:** enable auto-geocoding with no maps provider key; geocoding
needs a configured provider.

**Cleanup:** none.

### Lab 5.13 — MB-240: Manage work orders and customer assets (25–30%)

**Objective:** Query work orders and customer assets.

```http
GET {org}/api/data/v9.2/msdyn_customerassets?$select=msdyn_name&$top=5
```

**Expected result:** customer assets linked to work orders — the FS service
record.

**Negative test:** track functional location without an asset hierarchy; assets
model the equipment being serviced.

**Cleanup:** none.

### Lab 5.14 — MB-240: Schedule and dispatch work orders (15–20%)

**Objective:** Query bookable resource bookings (the schedule board data).

```http
GET {org}/api/data/v9.2/bookableresourcebookings?$select=starttime,endtime&$top=5
```

**Expected result:** resource bookings with start/end — scheduling and dispatch.

**Negative test:** dispatch with no resource requirements; the schedule board
matches requirements to resources.

**Cleanup:** none.

### Lab 5.15 — MB-240: Manage the Field Service mobile app (5–10%)

**Objective:** Identify the mobile offline profile configuration.

```text
Field Service (Dynamics 365) mobile -> offline profile -> tables synced offline
Booking status drives the technician workflow (Traveling -> In Progress -> Completed)
```

**Expected result:** the offline profile and booking-status flow — the mobile
technician experience.

**Negative test:** expect full data offline by default; only the offline profile
tables sync.

**Cleanup:** none.

### Lab 5.16 — MB-240: Manage inventory and purchasing by using the built-in inventory management system (5–10%)

**Objective:** Query FS inventory/warehouse records.

```http
GET {org}/api/data/v9.2/msdyn_warehouses?$select=msdyn_name&$top=5
```

**Expected result:** FS warehouses — the built-in inventory for parts on work
orders.

**Negative test:** use F&O advanced WMS expectations here; FS has a lightweight
inventory model.

**Cleanup:** none.

### Lab 5.17 — MB-240: Implement Microsoft Power Platform (5–10%)

**Objective:** Confirm the Power Platform environment FS runs on.

```bash
pac env list --output table
```

**Expected result:** the environment — FS is a Dataverse/Power Platform solution
you extend with flows and apps.

**Negative test:** build FS customizations outside a solution; use ALM.

**Cleanup:** none.

### Lab 5.18 — MB-280: Implement Dynamics 365 Sales (30–35%)

**Objective:** Configure the sales process (lead-to-opportunity).

```http
GET {org}/api/data/v9.2/leads?$select=subject,statecode&$top=5
```

**Expected result:** leads with state — the Sales process MB-280 implements.

**Negative test:** skip lead qualification; qualifying creates the opportunity,
account, and contact.

**Cleanup:** none.

### Lab 5.19 — MB-280: Configure and customize Dataverse and model-driven apps (35–40%)

**Objective:** Inspect the solution and tables you customize (the top domain).

```bash
pac solution list; pac data list-tables 2>/dev/null | head
```

**Expected result:** solutions and tables — the Dataverse customization surface.

**Negative test:** add fields to managed tables from another publisher; add your
own solution/publisher instead.

**Cleanup:** none.

### Lab 5.20 — MB-280: Demonstrate Dynamics 365 Customer Insights capabilities (10–15%)

**Objective:** Locate the Customer Insights segment/measure tables.

```bash
pac data list-tables 2>/dev/null | grep -iE 'segment|measure' | head
```

**Expected result:** Customer Insights segments/measures — the analytics
capability MB-280 uses for targeting.

**Negative test:** segment on stale data; segments reflect the last data
refresh.

**Cleanup:** none.

### Lab 5.21 — MB-280: Extend and enhance Dynamics 365 Sales capabilities (10–15%)

**Objective:** Add automation with a business rule / flow (extension).

```bash
pac solution list   # business rules and flows live inside a solution
```

**Expected result:** the solution holding business rules/flows — the Sales
extension mechanism.

**Negative test:** put complex server logic in a business rule; use a flow or
plug-in for that.

**Cleanup:** none.

### Lab 5.22 — MB-330: Implement product information management (25–30%)

**Objective:** Identify the product master data entity.

```text
Product master: EcoResProduct / ReleasedProductsV2 (per legal entity)
Product dimensions: color, size, style, configuration
```

**Expected result:** the released-product model with dimensions — product
information management.

**Negative test:** sell a product not released to the legal entity; release it
to the company first.

**Cleanup:** none.

### Lab 5.23 — MB-330: Implement inventory and asset management (20–25%)

**Objective:** Read on-hand inventory via the OData entity.

```http
GET {fno}/data/InventOnhand?$select=ItemId,AvailPhysical&$top=5
```

**Expected result:** on-hand quantities by item — inventory management.

**Negative test:** trust on-hand without a warehouse dimension; on-hand is
tracked by storage/tracking dimensions.

**Cleanup:** none.

### Lab 5.24 — MB-330: Implement and manage supply chain processes (15–20%)

**Objective:** Query purchase orders (procure-to-pay).

```http
GET {fno}/data/PurchaseOrderHeadersV2?$select=PurchaseOrderNumber,OrderVendorAccountNumber&$top=5
```

**Expected result:** purchase order headers — the procurement process.

**Negative test:** confirm a PO with no vendor; the vendor account is required.

**Cleanup:** none.

### Lab 5.25 — MB-330: Implement warehouse management and transportation management (20–25%)

**Objective:** Identify advanced-WMS work.

```text
WMS work: work templates + location directives -> warehouse work (pick/put)
Mobile device (WHS app) executes work; wave/load for transportation
```

**Expected result:** the WMS work model — advanced warehouse management.

**Negative test:** use basic warehousing steps for an advanced-WMS-enabled item;
advanced WMS requires work creation.

**Cleanup:** none.

### Lab 5.26 — MB-330: Implement master planning (10–15%)

**Objective:** Understand planned-order generation.

```text
Master plan -> planning run -> planned orders (purchase/production/transfer)
Coverage: min/max, requirement, period
```

**Expected result:** the master-planning flow producing planned orders — supply
and demand balancing.

**Negative test:** run planning with no coverage group on items; coverage
settings drive the results.

**Cleanup:** none.

### Lab 5.27 — MB-335: Configure products (20–25%)

**Objective:** Define product variants via dimensions.

```text
Product dimension groups: color/size/style/configuration
Variant = combination of dimensions; released per legal entity
```

**Expected result:** the variant model — configuring manufacturable products.

**Negative test:** create variants with no dimension group; variants require the
dimension configuration.

**Cleanup:** none.

### Lab 5.28 — MB-335: Configure production prerequisites (20–25%)

**Objective:** Map the production-order prerequisites.

```text
Prereqs: Resources + resource groups -> Routes/operations -> BOM (bill of materials)
Calendars drive capacity and scheduling
```

**Expected result:** resources, routes, and BOMs — the manufacturing
prerequisites.

**Negative test:** schedule production with no route; operations scheduling needs
routes and resources.

**Cleanup:** none.

### Lab 5.29 — MB-335: Implement production methods (20–25%)

**Objective:** Distinguish the production control methods.

```text
Discrete (production orders) | Process (batch orders) | Lean (kanban)
```

**Expected result:** the three production methods — choosing by manufacturing
style.

**Negative test:** use discrete production orders for a formula/co-product
process; process manufacturing needs batch orders.

**Cleanup:** none.

### Lab 5.30 — MB-335: Configure and manage production control (15–20%)

**Objective:** Follow the production-order lifecycle.

```text
Production order: Created -> Estimated -> Scheduled -> Released -> Started -> Reported as finished -> Ended
```

**Expected result:** the production-order status flow — production control.

**Negative test:** report as finished before starting; the status sequence is
enforced.

**Cleanup:** none.

### Lab 5.31 — MB-335: Implement additional supply chain management features (10–15%)

**Objective:** Identify IoT/asset-management SCM add-ons.

```text
Asset management (work orders/maintenance) | Sensor Data Intelligence (IoT) | Planning Optimization
```

**Expected result:** the additional SCM capabilities — extending manufacturing.

**Negative test:** assume Planning Optimization and legacy MRP behave
identically; the optimization engine differs.

**Cleanup:** none.

### Lab 5.32 — MB-500: Plan the architecture and solution design (5–10%)

**Objective:** Map the F&O development architecture.

```text
Model -> Package -> Project (Visual Studio); AOT elements deployed via deployable packages
Extensions over over-layering; source control in Azure DevOps
```

**Expected result:** the model/package/project structure — F&O solution design.

**Negative test:** over-layer standard code; use extensions (event handlers,
chain-of-command) instead.

**Cleanup:** none.

### Lab 5.33 — MB-500: Apply developer tools (5–10%)

**Objective:** Identify the F&O developer toolchain.

```text
Visual Studio (F&O tools) + Application Explorer (AOT) + LCS environments
Build via msbuild / deployable package; DB sync for table changes
```

**Expected result:** the toolchain — the environment MB-500 develops in.

**Negative test:** edit metadata directly in the running environment; develop in
a dev box and deploy a package.

**Cleanup:** none.

### Lab 5.34 — MB-500: Design and develop AOT elements (15–20%)

**Objective:** Define a table extension (an AOT element).

```xpp
// Table extension adds a field to a standard table via an extension model
[ExtensionOf(tableStr(CustTable))]
final class CustTable_Lab_Extension { }
```

**Expected result:** an extension class targeting a standard table — extending
AOT elements without over-layering.

**Negative test:** add the field by editing `CustTable` directly; use the
extension.

**Cleanup:** none.

### Lab 5.35 — MB-500: Develop and test code (20–25%)

**Objective:** Write and reason about an X++ class (the largest dev domain).

```xpp
class LabRunnable
{
    public static void main(Args _args)
    {
        info(strFmt("On-hand check at %1", DateTimeUtil::utcNow()));
    }
}
```

**Expected result:** a runnable X++ class printing an info message — code
development and unit testing (SysTest).

**Negative test:** query the database in a loop per record; use set-based
operations for performance.

**Cleanup:** none.

### Lab 5.36 — MB-500: Implement reporting (10–15%)

**Objective:** Identify the F&O reporting options.

```text
SSRS reports (RDP/DP classes) | Electronic reporting (ER) | Financial reporting
Embedded Power BI via aggregate measurements
```

**Expected result:** the reporting stack — implementing F&O reports.

**Negative test:** build every report in SSRS; use Electronic Reporting for
configurable regulatory formats.

**Cleanup:** none.

### Lab 5.37 — MB-500: Integrate and manage data solutions (15–20%)

**Objective:** Read data through an OData data entity.

```http
GET {fno}/data/CustomersV3?$select=CustomerAccount,OrganizationName&$top=5
```

**Expected result:** customer records via the OData entity — data integration.

**Negative test:** integrate against a staging table directly; use published
data entities.

**Cleanup:** none.

### Lab 5.38 — MB-500: Implement security and optimize performance (10–15%)

**Objective:** Map the F&O security model.

```text
Security: Roles -> Duties -> Privileges -> Permissions (entry points)
Performance: set-based ops, indexes, caching, SysTraceCol/PerfSDK
```

**Expected result:** the role-based security hierarchy and performance levers.

**Negative test:** grant a role broad table access directly; assign duties and
privileges instead.

**Cleanup:** none.

### Lab 5.39 — MB-700: Architect solutions (25–30%)

**Objective:** Produce an F&O solution blueprint.

```text
Blueprint: legal entities, integrations, data model, ISV solutions, environments (dev/test/prod)
Non-functional: performance, security, localization
```

**Expected result:** the architecture blueprint — the architect's design.

**Negative test:** architect with no environment/ALM plan; F&O needs LCS-managed
environments.

**Cleanup:** none.

### Lab 5.40 — MB-700: Define solution strategies (45–50%)

**Objective:** Define data-migration and integration strategies (top domain).

```text
Migration: Data management framework (DMF), staging, mapping, cutover plan
Integration: OData, custom services, dual-write to Dataverse, Business events
```

**Expected result:** the migration + integration strategy — the largest MB-700
domain.

**Negative test:** big-bang migrate with no mock cutovers; run iterative mock
go-lives.

**Cleanup:** none.

### Lab 5.41 — MB-700: Manage implementations (10–15%)

**Objective:** Map the implementation methodology.

```text
Success by Design + LCS methodology phases: Initiate -> Implement -> Prepare -> Operate
FastTrack workshops at key gates
```

**Expected result:** the LCS/Success-by-Design phases — implementation
management.

**Negative test:** skip the FastTrack solution-blueprint review; the gate
catches architecture risks.

**Cleanup:** none.

### Lab 5.42 — MB-700: Manage testing (15–20%)

**Objective:** Identify the F&O test tooling.

```text
RSAT (Regression Suite Automation Tool) from task recordings
Performance/load: LCS + Azure DevOps test plans
```

**Expected result:** RSAT-driven regression testing — managing quality across
releases.

**Negative test:** rely only on manual testing across monthly updates;
automate regression with RSAT.

**Cleanup:** none.

### Lab 5.43 — MB-800: Set up Business Central (20–25%)

**Objective:** Map company setup in Business Central.

```text
Assisted Setup -> Company Information -> No. Series -> Posting groups
Multiple companies per environment
```

**Expected result:** the setup checklist — standing up a BC company.

**Negative test:** post before defining posting groups; posting requires the
group setup.

**Cleanup:** none.

### Lab 5.44 — MB-800: Configure financials (30–35%)

**Objective:** Map the BC financial configuration (top domain).

```text
Chart of Accounts -> General Posting Setup + VAT Posting Setup
Dimensions for analysis; General Journals for entries
```

**Expected result:** the COA and posting-setup structure — configuring
financials.

**Negative test:** post a sale with no general/VAT posting setup; the posting
matrix must be complete.

**Cleanup:** none.

### Lab 5.45 — MB-800: Configure sales and purchasing (10–15%)

**Objective:** Map sales/purchase configuration.

```text
Customers/Vendors -> Sales & Receivables / Purchases & Payables setup
Item cards + prices; posting from documents updates the ledger
```

**Expected result:** the sales/purchase setup — configuring trade documents.

**Negative test:** invoice an item with no unit cost/price setup; documents need
item pricing.

**Cleanup:** none.

### Lab 5.46 — MB-800: Perform Business Central operations (30–35%)

**Objective:** Follow the post-a-document operation.

```text
Sales Order -> Post (Ship + Invoice) -> Posted Sales Invoice + G/L Entries + Item Ledger Entries
```

**Expected result:** posting a sales order creates ledger and item entries —
daily BC operations.

**Negative test:** edit a posted invoice; posted documents are immutable — use a
credit memo.

**Cleanup:** none.

### Lab 5.47 — MB-820: Describe Business Central (10–15%)

**Objective:** Map the BC development architecture.

```text
Extensions (AL) over the base app; objects: Table, Page, Codeunit, Report, Query, XMLport
Events + subscribers for extensibility (no code modification of base)
```

**Expected result:** the extension-based architecture — how BC is developed.

**Negative test:** modify base-app objects; BC development is extension-only.

**Cleanup:** none.

### Lab 5.48 — MB-820: Install, develop, and deploy for Business Central (10–15%)

**Objective:** Scaffold an AL project.

```al
// app.json declares the extension; AL: Go! generates HelloWorld.al
pageextension 50100 CustomerListExt extends "Customer List" { }
```

**Expected result:** an AL extension project (`app.json` + a page extension) —
the develop/deploy unit.

**Negative test:** deploy without bumping the `app.json` version; the runtime
rejects an unchanged version on publish.

**Cleanup:** none.

### Lab 5.49 — MB-820: Develop by using AL objects (35–40%)

**Objective:** Define AL table and page objects (the largest domain).

```al
table 50100 "Lab Widget"
{
    fields { field(1; "No."; Code[20]) { } field(2; Description; Text[100]) { } }
    keys { key(PK; "No.") { Clustered = true; } }
}
```

**Expected result:** a custom table with a primary key — building AL objects.

**Negative test:** reuse an object ID from the reserved range; use your assigned
ID range in `app.json`.

**Cleanup:** none.

### Lab 5.50 — MB-820: Develop by using AL (15–20%)

**Objective:** Write AL logic in a codeunit.

```al
codeunit 50100 "Lab Ops"
{
    procedure Total(a: Integer; b: Integer): Integer
    begin
        exit(a + b);
    end;
}
```

**Expected result:** a codeunit procedure returning a sum — AL procedural logic.

**Negative test:** put business logic in page triggers; factor it into codeunits
for testability.

**Cleanup:** none.

### Lab 5.51 — MB-820: Work with development tools (10–15%)

**Objective:** Identify the AL toolchain.

```text
VS Code + AL Language extension; AL: Go!, Ctrl+F5 (publish), snippets (ttable, tpage)
Symbols downloaded via AL: Download symbols; Docker/cloud sandbox as target
```

**Expected result:** the AL dev tools — building and publishing extensions.

**Negative test:** develop without downloading symbols; IntelliSense and
compilation need the base-app symbols.

**Cleanup:** none.

### Lab 5.52 — MB-820: Integrate Business Central with other applications (10–15%)

**Objective:** Expose data through a BC API page.

```al
page 50101 "Widget API"
{
    PageType = API; APIPublisher = 'lab'; APIGroup = 'demo'; APIVersion = 'v1.0';
    EntityName = 'widget'; EntitySetName = 'widgets'; SourceTable = "Lab Widget";
    layout { area(Content) { repeater(g) { field(no; Rec."No.") { } } } }
}
```

**Expected result:** an OData/REST API page — integrating BC with external apps.

**Negative test:** expose a UI page as an integration point; use an API page
(stable contract) instead.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Dynamics 365 splits into Customer Engagement (Dataverse/Power Platform) and
Finance and Operations (ERP), anchored by the MB-910/MB-920 Fundamentals. The
MB family certifies functional consultants, developers (MB-500/MB-820), and
architects (MB-700), with CE roles overlapping Power Platform (PL-200/PL-600)
and a wave of new Copilot/AI Dynamics credentials. MB-901 and MB-600 retired.

- [ ] I can distinguish the CE and F&O tracks.
- [ ] I can list the main MB credentials and their exams.
- [ ] I understand the Power Platform overlap and the AI additions.
- [ ] I can build a Dynamics study path within a track.
- [ ] I completed Labs 5.1–5.2 including each negative test.
