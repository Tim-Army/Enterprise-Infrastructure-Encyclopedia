# Chapter 06: Consultant — Sales, Service, and Experience Cloud

## Learning Objectives

- Implement Sales Cloud (leads, opportunities, forecasting).
- Implement Service Cloud (cases, omni-channel, knowledge).
- Build Experience Cloud sites (portals/communities).
- Gather requirements and design solutions.
- Complete a walkthrough for each consultant topic.

## Theory and Architecture

The **Consultant** certifications validate implementing Salesforce's product clouds for a business.
**Sales Cloud** supports the sales process: **leads** (potential customers) converted to **accounts/
contacts/opportunities**, a **sales pipeline** through opportunity **stages**, **forecasting**, and
**price books/products** — configured to a company's sales methodology. **Service Cloud** supports
customer support: **cases** (support requests) routed by **omni-channel** and **assignment/escalation
rules**, **Knowledge** articles for self-service and agent efficiency, **entitlements/SLAs**, and
channels (email-to-case, web-to-case, chat). **Experience Cloud** builds external **sites**
(customer/partner portals, help centers) on the platform, exposing selected data and processes to
customers/partners with their own branding and access. A consultant's skill is **requirements
gathering** — understanding the business process and translating it into declarative configuration
(objects, automation, security) that fits, favoring standard functionality over customization. This
chapter teaches each with a hands-on walkthrough (cloud configuration and solution design).

## Design Considerations

Configure **Sales Cloud** to the actual sales process (stages, forecasting). Route and prioritize
**Service Cloud** cases with omni-channel and SLAs, and enable **Knowledge**. Expose the right data
securely via **Experience Cloud**. **Gather requirements** first and prefer standard functionality.
Design for adoption and reporting.

## Implementation and Automation

The labs configure Sales/Service clouds and design an Experience site.

## Validation and Troubleshooting

Confirm the consultant model:

```text
Sales Cloud: leads -> accounts/contacts/opportunities, pipeline stages, forecasting, products/price books. Service Cloud: cases + omni-channel routing + assignment/escalation + Knowledge + entitlements/SLAs + channels.
Experience Cloud: external portals/sites (branded, secure, selected data). Skill: requirements gathering -> declarative solution, standard before custom.
```

Common pitfalls: **customizing** heavily before using standard cloud features; and Experience Cloud
sites exposing **too much** data (scope access carefully).

## Security and Best Practices

Configure clouds to the **real process**, prefer **standard** functionality, route/prioritize service
work with **SLAs**, and scope **Experience Cloud** access carefully. Gather requirements first. All
work is authorized administration/consulting.

## Hands-On Lab

Consultant walkthroughs. **Shared prerequisites** — `python3`, a free Dev org. **Cost:** none.

### Lab 6.1 — Configure a sales pipeline (Sales Cloud)

**Objective:** Model the sales process.

```python
python3 - <<'PY'
stages=[("Prospecting",10),("Qualification",25),("Proposal",50),("Negotiation",75),("Closed Won",100),("Closed Lost",0)]
for stage,prob in stages: print(f"{stage:14} -> {prob}% probability")
print("Sales Cloud: opportunity stages + probabilities drive pipeline + forecasting")
PY
```

**Expected result:** an **opportunity stage** model with probabilities — Sales Cloud pipeline.

**Negative test:** track deals in a spreadsheet outside Salesforce; **Sales Cloud** provides pipeline
and forecasting — use it.

**Cleanup:** none.

### Lab 6.2 — Route cases (Service Cloud)

**Objective:** Get cases to the right agent.

```python
python3 - <<'PY'
def route(case):
    if case["priority"]=="high" and case["product"]=="billing": return "Billing Tier-2 queue (omni-channel)"
    if case["channel"]=="chat": return "Live Chat agents"
    return "General Support queue"
print(route({"priority":"high","product":"billing","channel":"email"}))
print(route({"priority":"low","product":"general","channel":"chat"}))
print("Service Cloud: omni-channel + assignment rules route cases by priority/product/channel")
PY
```

**Expected result:** cases **routed** by priority/product/channel — Service Cloud case management.

**Negative test:** dump all cases in one queue; agents can't prioritize — route with **omni-channel/
assignment rules**.

**Cleanup:** none.

### Lab 6.3 — Design an Experience Cloud site

**Objective:** Expose data to customers securely.

```python
python3 - <<'PY'
site={"type":"Customer help center","audience":"customers (external users)","exposes":["Knowledge articles","their own Cases"],
      "security":"sharing sets + guest/authenticated access (least privilege)","branding":"company theme"}
for k,v in site.items(): print(f"{k:10}: {v}")
print("Experience Cloud: branded external site exposing SELECTED data with scoped access")
PY
```

**Expected result:** an **Experience Cloud** site exposing selected data with scoped access — external
engagement.

**Negative test:** expose internal objects broadly on a public site; scope with **sharing sets** and
authentication — least privilege.

**Cleanup:** none.

### Lab 6.4 — Gather requirements

**Objective:** Design to the business need.

```python
python3 - <<'PY'
process=["interview stakeholders (current process + pain points)","map to standard objects/features first",
         "identify gaps -> minimal configuration (not custom code)","design security + reporting","validate with users before build"]
for i,s in enumerate(process,1): print(f"{i}. {s}")
print("Consultant: requirements -> standard-first design; customize only real gaps")
PY
```

**Expected result:** a **requirements-to-design** process (standard-first) — consultant methodology.

**Negative test:** build a custom solution before understanding the **requirements**; it may not fit —
gather requirements first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Consultant certifications implement Sales Cloud (pipeline/forecasting), Service Cloud (case routing/
Knowledge/SLAs), and Experience Cloud (external sites), grounded in requirements gathering and a
standard-before-custom design approach.

- [ ] I can configure a sales pipeline.
- [ ] I can route cases in Service Cloud.
- [ ] I can design an Experience Cloud site.
- [ ] I can gather requirements and design to them.
- [ ] I completed Labs 6.1–6.4 including each negative test.
