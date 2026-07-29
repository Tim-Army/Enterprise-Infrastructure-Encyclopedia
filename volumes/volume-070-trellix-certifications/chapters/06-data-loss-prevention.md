# Chapter 06: Data Loss Prevention (DLP)

## Learning Objectives

- Explain Trellix DLP (endpoint and network) and its role.
- Classify sensitive data with classifications and definitions.
- Author DLP rules and reactions.
- Handle incidents and tune false positives.
- Complete a walkthrough for each DLP topic (defensive).

## Theory and Architecture

**Trellix Data Loss Prevention (DLP)** protects **data** — preventing sensitive information from
leaving the organization. It works at two layers: **DLP Endpoint** (on the device — monitoring
copy/paste, USB/removable media, printing, cloud-sync, and application actions) and **DLP Network**
(inspecting data in motion — email, web, network egress). The foundation is **classification**:
**definitions** (patterns like credit-card or SSN formats, dictionaries, document fingerprints) and
**classifications** that label data as sensitive. **Rules** (data protection rules) then match
classified data against **channels** (USB, web, email, print) and apply a **reaction** — monitor,
notify the user, block, encrypt, or quarantine — with **incidents** logged to ePO for review.
Because legitimate business data trips rules, **tuning** (justifications, exceptions, whitelists) is
essential. DLP is **defensive** data governance and protection.

## Design Considerations

Start DLP in **monitor/notify** mode to learn real data flows before **blocking**, so you don't halt
the business. Classify with **precise definitions** (reduce false positives). Cover the **channels**
that matter (USB, cloud, email, web). Give users a **justification** path for legitimate transfers.
Review **incidents** to tune continuously.

## Implementation and Automation

The labs define a classification, author a rule with a reaction, and tune an incident — all
**defensive**.

## Validation and Troubleshooting

Confirm the DLP model:

```text
DLP Endpoint (device: USB/print/clipboard/cloud) + DLP Network (email/web egress).
Foundation: definitions (patterns/dictionaries/fingerprints) -> classifications (sensitive labels).
Rules: match classified data on channels -> reaction (monitor/notify/block/encrypt/quarantine) -> incidents in ePO.
Deploy monitor -> notify -> block. Tune with justifications/exceptions.
```

Common pitfalls: going straight to **block** (business disruption); and broad definitions causing
**false-positive floods**.

## Security and Best Practices

Phase **monitor → notify → block**, classify **precisely**, cover the right **channels**, and give a
**justification** workflow. Review **incidents** to tune. Protect the DLP policy and incident data.
Defensive data protection throughout.

## Hands-On Lab

DLP walkthroughs (defensive). **Shared prerequisites for Labs 6.1–6.4** — a shell with `python3`;
concepts apply to a Trellix DLP deployment managed by ePO in an **authorized** lab. **Cost:** none.

### Lab 6.1 — Define a classification

**Objective:** Label credit-card data as sensitive.

```python
python3 - <<'PY'
import re
# Simplified PAN (credit-card) pattern for classification (Luhn omitted for brevity).
pan = re.compile(r"\b(?:\d[ -]?){13,16}\b")
samples=["order 4111 1111 1111 1111","phone 555-0100"]
for s in samples: print(f"{s!r}: {'SENSITIVE (PAN)' if pan.search(s) else 'not classified'}")
PY
```

**Expected result:** the credit-card sample **classified sensitive**, the phone number not — a
precise definition.

**Negative test:** classify on a loose "any long number" rule; it floods on phone/order numbers —
use a **precise** definition (and Luhn in production).

**Cleanup:** none.

### Lab 6.2 — Author a data-protection rule

**Objective:** Control a channel for classified data.

```python
python3 - <<'PY'
rule={"classification":"PAN (credit card)","channel":"USB removable media",
      "reaction":"block + notify user + log incident to ePO","mode":"monitor first, then block"}
for k,v in rule.items(): print(f"{k:14}: {v}")
PY
```

**Expected result:** a rule that **blocks classified PAN to USB** with user notice and an incident —
targeted data protection.

**Negative test:** block **all** file copies to USB; that halts legitimate work — match the
**classification**, not the whole channel.

**Cleanup:** none.

### Lab 6.3 — Handle an incident and tune

**Objective:** Resolve a false positive precisely.

```python
python3 - <<'PY'
incident={"user":"finance\\jdoe","data":"test file with sample numbers","channel":"email","verdict":"false positive"}
fix="add an exception for the test dataset / refine the definition; keep enforcement elsewhere"
print("incident:",incident); print("tuning:",fix)
PY
```

**Expected result:** a false-positive incident resolved with a **scoped exception**, keeping
enforcement intact — precise tuning.

**Negative test:** disable the whole rule to stop the false positive; scope the **exception** —
don't remove protection.

**Cleanup:** none.

### Lab 6.4 — User justification workflow

**Objective:** Allow legitimate transfers with accountability.

```text
# DLP can prompt the user for a business justification on a monitored/blocked action; the
#   justification is logged with the incident -> allows legitimate work while keeping an audit trail.
"justification: user provides reason -> action allowed + logged -> business continuity + audit"
```

**Expected result:** a **justification** path that permits legitimate transfers **with an audit
trail** — protection without paralysis.

**Negative test:** hard-block with no justification path; legitimate work stalls — provide a
**justification** workflow.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Trellix DLP (Endpoint and Network) protects sensitive data via classifications/definitions, rules
matching data to channels, and reactions with incidents in ePO. Classify precisely, phase monitor→
notify→block, cover the right channels, provide justifications, and tune from incidents. Defensive
data protection throughout.

- [ ] I can define a precise data classification.
- [ ] I can author a channel-specific data-protection rule.
- [ ] I can tune a false-positive incident precisely.
- [ ] I can explain the justification workflow.
- [ ] I completed Labs 6.1–6.4 including each negative test.
