# Chapter 09: Keeping the Splunk Program Current and Career Paths

## Learning Objectives

- Explain Splunk certification validity and renewal.
- Track program change — the Cisco era, new tracks, and blueprint updates.
- Plan a Splunk career path across the tracks.
- Relate Splunk credentials to the encyclopedia's observability and security volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

Splunk certifications are valid for a defined period (commonly **three years**) and
are renewed by **retaking the current exam** or earning a **higher** certification
on the track. There is no continuing-education-credit model — currency is by exam.
The program is evolving under the **Cisco** acquisition (2024): expect continued
integration of Splunk observability and security with Cisco's portfolio, and watch
for **blueprint updates** and new tracks (the Advanced Power User and the
Cybersecurity Defense Analyst/Engineer/Architect track are recent additions).

## Design Considerations

Plan a path by **role**, always starting with **SPL** (Core User → Power User →
Advanced Power User):

- **Platform operations:** Core → **Enterprise/Cloud Admin** → **Architect** →
  **Consultant**.
- **Security:** Core → **Cybersecurity Defense Analyst** → **Engineer** →
  **Architect** (with **ES Admin** and **SOAR**).
- **Observability:** Core → **O11y Metrics User** (with OpenTelemetry skills).
- **Service intelligence:** **ITSI Admin**.

Track which credentials are near expiry and renew by re-exam or by advancing.

## Implementation and Automation

Verify currency from **splunk.com** — the certification pages and blueprints carry
the current tracks and topic areas:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.splunk.com/en_us/training/certification-track.html" \
  | grep -oiE 'Certified [A-Za-z ]+' | sort -u | head
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
splunk.com > Training & Certification:
  - current tracks and certifications
  - each exam's blueprint (topic areas + weights) and prerequisites
  - certification validity and renewal terms
Watch for Cisco-era changes and new/updated tracks.
```

Common pitfalls: studying a **retired blueprint**; letting a certification lapse
(renew by re-exam or a higher cert); and skipping the **SPL foundation** that every
track needs.

## Security and Best Practices

Keep practicing on a current instance (trial/Cloud). Renew before lapse by
re-exam or by advancing the track. Maintain **SPL fluency** and **CIM** habits —
they carry across every track and stay valuable as the platform evolves under
Cisco.

## References and Knowledge Checks

- splunk.com: Training & Certification; per-exam blueprints; certification policies.

**Knowledge checks**

1. How are Splunk certifications renewed?
2. What recent tracks/changes must you verify against an old program map?
3. What is the SPL-first path through the tracks?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify the current tracks (Topic: Verify currency)

**Objective:** Read the current certifications from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.splunk.com/en_us/training/certification-track.html" \
  | grep -oiE 'Certified (User|Power User|Advanced Power User|Admin|Architect|Consultant|Cybersecurity Defense (Analyst|Engineer|Architect)|Metrics User)' \
  | sort -u
```

**Expected result:** the current certifications, including the **Advanced Power
User** and the **Cybersecurity Defense** trio — confirming what an old map misses.

**Negative test:** trust a pre-2024 chart; the security track and Advanced Power
User are newer — confirm on splunk.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Plan a renewal (Topic: Maintain the credential)

**Objective:** Model the three-year renewal-by-exam rule.

```bash
python3 - <<'PY'
from datetime import date
earned = date(2026, 7, 26)
expires = earned.replace(year=earned.year + 3)
print(f"Earned {earned} -> expires ~{expires}")
print("Renew by: retaking the current exam OR earning a higher cert on the track.")
PY
```

**Expected result:** a ~three-year expiry and the renewal options (re-exam or
advance) — Splunk's exam-based currency model.

**Negative test:** expect CE credits to renew it; Splunk renews **by exam** —
plan to re-test or advance.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Splunk certifications are valid ~three years and renewed by re-exam or by advancing
the track — no CE model. The program is evolving under Cisco, with the Advanced
Power User and the Cybersecurity Defense track as recent additions. Plan a path by
role, always starting from the SPL foundation, and verify currency on splunk.com.

- [ ] I can explain Splunk certification validity and renewal.
- [ ] I can name the recent tracks and the Cisco-era context.
- [ ] I can plan an SPL-first path by role.
- [ ] I can verify the current tracks on splunk.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
