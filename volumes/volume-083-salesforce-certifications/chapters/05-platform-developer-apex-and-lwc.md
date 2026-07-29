# Chapter 05: Platform Developer — Apex and LWC

## Learning Objectives

- Write Apex classes and triggers.
- Query data with SOQL and SOSL.
- Build UI with Lightning Web Components (LWC).
- Test Apex and understand governor limits.
- Complete a walkthrough for each developer topic.

## Theory and Architecture

The **Platform Developer I/II** certifications validate coding on Salesforce when declarative tools
aren't enough. **Apex** is Salesforce's server-side, Java-like language, running in **classes** and
**triggers** (before/after insert/update/delete on objects) to implement complex logic. Because
Salesforce is multi-tenant, Apex runs under strict **governor limits** (e.g., 100 SOQL queries and
150 DML statements per transaction), so code must be **bulkified** — written to handle collections of
records, never one at a time in a loop. **SOQL (Salesforce Object Query Language)** queries records
(`SELECT ... FROM ... WHERE`), and **SOSL** searches across objects. The UI is built with **Lightning
Web Components (LWC)** — modern, standards-based web components (JavaScript + HTML) that render in the
Lightning experience and communicate with Apex. **Testing** is mandatory: Apex requires **≥75% test
coverage** to deploy, with tests that assert behavior. The developer's craft is efficient, bulkified,
well-tested Apex and reusable LWC — extending the platform where configuration can't. This chapter
teaches each with a hands-on walkthrough (Apex/SOQL patterns, bulkification, and LWC concepts).

## Design Considerations

Write **bulkified** Apex (operate on collections, query/DML outside loops) to respect **governor
limits**. Use **SOQL** efficiently (selective, indexed filters). Put reusable logic in **classes**,
minimal logic in **triggers** (delegate to a handler). Build UI with **LWC**. Achieve **≥75% test
coverage** with meaningful assertions. Prefer **declarative** first (Chapter 4), code when needed.

## Implementation and Automation

The labs write a bulkified trigger, a SOQL query, and reason about LWC and testing.

## Validation and Troubleshooting

Confirm the developer model:

```text
Apex = server-side Java-like (classes + triggers before/after CRUD). Governor limits (100 SOQL/150 DML per txn) -> bulkify (collections, query/DML outside loops). SOQL (query) + SOSL (search). LWC = modern web components (JS+HTML) + Apex.
Testing: >=75% coverage with assertions required to deploy. Declarative-first; code when needed.
```

Common pitfalls: **SOQL/DML inside a loop** (hits governor limits on bulk data); and Apex with no
**test coverage** (can't deploy).

## Security and Best Practices

Write **bulkified**, limit-aware Apex with **≥75% tested** coverage, efficient **SOQL**, thin
**triggers** delegating to handlers, and reusable **LWC**. Declarative-first. All development is
authorized.

## Hands-On Lab

Developer walkthroughs. **Shared prerequisites** — a free Dev org (Developer Console / Salesforce CLI)
and `python3`. **Cost:** none.

### Lab 5.1 — Write a bulkified Apex trigger

**Objective:** Respect governor limits.

```java
// Apex trigger (bulkified — operates on Trigger.new collection, no SOQL/DML in a loop):
trigger OpportunityTrigger on Opportunity (before update) {
    Set<Id> accountIds = new Set<Id>();
    for (Opportunity o : Trigger.new) accountIds.add(o.AccountId);   // collect
    Map<Id, Account> accts = new Map<Id, Account>(
        [SELECT Id, Name FROM Account WHERE Id IN :accountIds]);      // ONE query
    for (Opportunity o : Trigger.new) {
        if (accts.containsKey(o.AccountId)) o.Description = 'Acct: ' + accts.get(o.AccountId).Name;
    }
}
```

**Expected result:** a **bulkified** trigger doing one SOQL query for all records — governor-limit-safe
Apex.

**Negative test:** put `[SELECT ...]` **inside** the `for` loop; 200 records = 200 queries → limit
exception — query **outside** the loop.

**Cleanup:** none.

### Lab 5.2 — Query with SOQL

**Objective:** Retrieve records efficiently.

```java
// SOQL: selective query with a filter and relationship traversal
List<Opportunity> opps = [
    SELECT Id, Name, Amount, Account.Name
    FROM Opportunity
    WHERE StageName = 'Closed Won' AND CloseDate = THIS_YEAR
    ORDER BY Amount DESC
    LIMIT 100
];
// System.debug(opps.size() + ' closed-won opportunities this year');
```

**Expected result:** a **selective SOQL** query (filter + relationship + limit) — efficient data
retrieval.

**Negative test:** `SELECT ... FROM Opportunity` with no `WHERE`; on a large org it's slow/limited —
filter selectively.

**Cleanup:** none.

### Lab 5.3 — Reason about an LWC

**Objective:** Build modern UI.

```python
python3 - <<'PY'
lwc={"files":["myComponent.html (template)","myComponent.js (logic + @wire to Apex)","myComponent.js-meta.xml (config)"],
     "data":"@wire calls an Apex method to fetch records","events":"dispatch/handle custom events between components"}
for k,v in lwc.items(): print(f"{k:8}: {v}")
print("LWC: standards-based web components (JS+HTML) that call Apex and compose the Lightning UI")
PY
```

**Expected result:** the **LWC** structure (template + JS + config, wired to Apex) — modern Salesforce
UI.

**Negative test:** build new UI in the deprecated Visualforce/Aura where **LWC** is the current
standard — use LWC.

**Cleanup:** none.

### Lab 5.4 — Ensure test coverage

**Objective:** Make code deployable.

```python
python3 - <<'PY'
def deployable(coverage_pct, has_assertions):
    return coverage_pct>=75 and has_assertions
print("60% coverage, asserts:", deployable(60, True))   # False
print("85% coverage, asserts:", deployable(85, True))   # True
print("Apex: >=75% coverage WITH meaningful assertions required to deploy to production")
PY
```

**Expected result:** deployment allowed only at **≥75% coverage with assertions** — Apex testing
requirement.

**Negative test:** write tests with no **assertions** just to hit coverage; they don't verify behavior
— assert real outcomes.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Platform Developer covers bulkified, governor-limit-aware Apex (classes and triggers), efficient SOQL/
SOSL, Lightning Web Components for UI, and mandatory ≥75% test coverage — extending the platform with
code where configuration can't.

- [ ] I can write a bulkified Apex trigger.
- [ ] I can query with SOQL.
- [ ] I can reason about an LWC.
- [ ] I can ensure deployable test coverage.
- [ ] I completed Labs 5.1–5.4 including each negative test.
