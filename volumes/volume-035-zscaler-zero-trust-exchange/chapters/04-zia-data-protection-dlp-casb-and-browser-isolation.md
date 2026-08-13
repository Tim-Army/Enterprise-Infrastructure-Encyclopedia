# Chapter 04: ZIA Data Protection — DLP, CASB, and Cloud Browser Isolation

## Learning Objectives

- Configure inline **Data Loss Prevention (DLP)** with dictionaries, engines,
  and rules, and explain how the inline proxy inspects uploads.
- Distinguish **inline DLP** from **out-of-band CASB** (API-scanning SaaS data
  at rest) and explain when each applies.
- Explain **CASB** control of sanctioned and unsanctioned SaaS (shadow IT,
  tenant restrictions).
- Describe **Cloud Browser Isolation (CBI)** and when isolating a session
  protects data without blocking access.
- Test a DLP dictionary's matching logic (for example, a Luhn-valid card
  number) safely and locally.

## Theory and Architecture

Data protection is the mirror image of threat prevention: threat engines stop
bad things coming *in*; DLP and CASB stop sensitive things going *out* or being
exposed in SaaS. Because ZIA already terminates and (with SSL inspection)
decrypts the session, it can inspect the content of an upload, a form post, or
a SaaS API object and act before data leaves.

### Inline DLP

**Inline DLP** inspects traffic in flight. **Dictionaries** define what to look
for (patterns like credit-card or Social-Security numbers, keywords, exact-data
match); **DLP engines** combine dictionaries with logic (for example, "credit
card AND more than N matches"); **DLP rules** bind an engine to users, apps, and
an action (block, allow-and-log, or confirm). A form post or file upload
containing matched content is blocked or logged inline.

### CASB: inline and out-of-band

**Inline CASB** controls SaaS *as users access it* — tenant restrictions (only
the corporate Microsoft 365 tenant), activity control (allow view, block
upload), and shadow-IT discovery. **Out-of-band CASB** connects to sanctioned
SaaS by **API** and scans data *at rest* — files already sitting in a corporate
drive — finding exposures the inline path never sees because no one is actively
transferring them. The two are complementary: inline catches data in motion,
API-CASB catches data at rest.

### Cloud Browser Isolation

**Cloud Browser Isolation (CBI)** renders a risky or sensitive site in a remote,
disposable browser and streams only pixels to the user. Nothing executes
locally, and — crucially for data protection — upload, download, copy, and paste
can be disabled, so a user can *use* a risky or unmanaged-SaaS site without data
crossing the boundary. It is the middle path between block and full allow.

## Design Considerations

- **DLP precision vs. noise.** A single-pattern dictionary produces false
  positives; engines that require a threshold or combine signals (card number
  *and* a keyword) are far more precise. Tune before you block.
- **Inline vs. API-CASB is not either/or.** Inline stops exfiltration in
  motion; API-CASB remediates exposure at rest — a complete SaaS posture needs
  both.
- **Isolate instead of block** when the business needs the site but not the
  data path — CBI preserves access while cutting the exfiltration channel.

## Implementation and Automation

### A DLP engine and rule (portal shape)

```text
# ZIA Portal > Policy > Data Loss Prevention:
#   Dictionary: "Credit Cards" (built-in) ; Engine: "PCI" = Credit Cards with >= 1 match
#   Rule "Block card upload": Engine=PCI; Cloud Apps=All; Action=Block; SSL inspection required
```

### Testing dictionary logic locally (Luhn check)

```bash
python3 - <<'EOF'
def luhn(n):
    d=[int(c) for c in n if c.isdigit()][::-1]
    return (sum(d[0::2]) + sum(sum(divmod(x*2,10)) for x in d[1::2])) % 10 == 0
for n in ["4539578763621486", "4539578763621487"]:   # first is Luhn-valid
    print(n, "-> DLP would flag" if luhn(n) else "-> not a valid card (no match)")
EOF
```

### CASB and isolation (portal shape)

```text
# Inline CASB: tenant restriction so only tenant "corp.onmicrosoft.com" is reachable for M365
# Out-of-band CASB: connect Google Drive/OneDrive by API; scan at-rest files for PCI/PII exposure
# CBI: isolate "unsanctioned SaaS" category with download/upload/copy/paste disabled
```

## Validation and Troubleshooting

- **DLP not triggering.** SSL inspection is off (content is opaque), or the
  engine threshold is not met — DLP acts only on inspected content.
- **Too many false positives.** The dictionary is too loose; raise the match
  threshold or combine signals in the engine.
- **SaaS exposure the inline path missed.** That data is at rest — only
  API-CASB scanning finds files already sitting in the SaaS tenant.

## Security and Best Practices

- **Require SSL inspection for DLP** — an upload you cannot decrypt is an
  upload you cannot inspect.
- **Combine inline DLP with API-CASB** so both data-in-motion and data-at-rest
  are covered.
- **Reach for isolation before an outright block** when access is needed but
  the data path is the risk.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Data Loss Prevention*, *SaaS Security / CASB*, and
  *Cloud Browser Isolation* (`help.zscaler.com`).

### Knowledge Checks

- What is the difference between a DLP dictionary and a DLP engine?
- When does out-of-band API-CASB find exposures inline CASB cannot?
- How does Cloud Browser Isolation preserve access while preventing
  exfiltration?
- Why is SSL inspection a prerequisite for inline DLP?

## Hands-On Lab

This chapter's labs cover data protection — DLP matching logic, CASB, and
isolation. The DLP logic test runs locally; CASB and CBI steps reference a ZIA
tenant. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.3** — `python3`; a ZIA tenant for portal
steps. **Cost:** none.

### Lab 4.1 — DLP dictionary and engine logic (Topic: Inline DLP)

**Objective:** Confirm what a card-number dictionary matches.

```bash
python3 - <<'EOF'
def luhn(n):
    d=[int(c) for c in n if c.isdigit()][::-1]
    return (sum(d[0::2]) + sum(sum(divmod(x*2,10)) for x in d[1::2])) % 10 == 0
tests = {"4539578763621486": True, "1234567890123456": False}
for n, expect in tests.items():
    got = luhn(n)
    print(f"{n}: match={got} (expected {expect})")
    assert got == expect
print("DLP card dictionary logic verified")
EOF
```

**Expected result:** the Luhn-valid number matches and the random one does not —
a DLP **dictionary** defines the pattern (a valid card number, not any 16
digits) and a DLP **engine** adds thresholds/logic, which is what makes inline
DLP precise enough to block real card data without flagging every number.

**Negative test:** match on "any 16 digits" with no Luhn/threshold; ordinary
numbers trip the rule and users are blocked constantly — imprecise dictionaries
make DLP unusable.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — CASB: tenant restriction and at-rest scan (Topic: SaaS security)

**Objective:** Control SaaS in motion and at rest.

```text
# Inline CASB: restrict M365 to tenant "corp.onmicrosoft.com" (block personal tenants)
# Out-of-band CASB: connect the sanctioned drive by API; scan at-rest files for PCI/PII
```

**Expected result:** users can reach only the corporate SaaS tenant, and the
API scan reports at-rest exposures — inline CASB controls data in motion while
out-of-band (API) CASB finds data already sitting in SaaS; a complete posture
needs both because they see different data.

**Negative test:** rely on inline CASB alone; files already resident in the
SaaS tenant are never scanned — at-rest exposure needs the API path.

**Rollback:** revert lab CASB policy.

### Lab 4.3 — Cloud Browser Isolation (Topic: Isolation)

**Objective:** Allow access to a risky site with no data path.

```text
# ZIA Portal > CBI: isolate "unsanctioned SaaS" category; disable upload/download/copy/paste
```

**Expected result:** the site opens in a remote, disposable browser streaming
only pixels, with the data channels disabled — CBI is the middle path between
block and allow: the user uses the site, but files and clipboard cannot cross
the boundary, so access is preserved while exfiltration is cut.

**Negative test:** fully allow the risky site instead of isolating it; local
execution and uploads/downloads are possible again — isolation is what removes
the data path while keeping access.

**Rollback:** revert lab CBI policy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ZIA data protection stops sensitive data leaving and finds it exposed in SaaS:
inline DLP inspects uploads (dictionaries define patterns, engines add
precision), inline CASB controls SaaS in motion while API-CASB scans it at
rest, and Cloud Browser Isolation preserves access to risky sites with the data
path removed. All of it depends on SSL inspection to see the content.

- [ ] Can explain dictionary vs. engine and why thresholds reduce noise.
- [ ] Knows when API-CASB is required over inline CASB.
- [ ] Can describe when isolation beats a block.
- [ ] Understands SSL inspection as the prerequisite for inline DLP.
