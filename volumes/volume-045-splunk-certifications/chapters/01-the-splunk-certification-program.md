# Chapter 01: The Splunk Certification Program

## Learning Objectives

- Explain what Splunk certifies and its place in the observability and security stack.
- Describe the credential map across the Core, Admin, Architecture, Cybersecurity, and Observability tracks.
- Explain the exam experience (Pearson VUE), test blueprints, and digital badging.
- Understand the Cisco-era program and prerequisites between certifications.
- Verify a current test blueprint from the authoritative source.

## Theory and Architecture

**Splunk** (a **Cisco company** since the 2024 acquisition) is the leading
platform for turning machine data — logs, metrics, and traces — into searchable
insight, and it certifies practitioners on the **Search Processing Language (SPL)**
and the platform's administration, security, and observability uses. Splunk
credentials sit alongside the encyclopedia's **observability (XI)**, **visibility
(Gigamon XVIII, Wireshark XX)**, and **security** volumes: they validate the
ability to search, operate, and defend with Splunk.

The program runs on several tracks:

- **Core (SPL) track** — **Core Certified User**, **Core Certified Power User**,
  and **Core Certified Advanced Power User**.
- **Administration** — **Enterprise Certified Admin** and **Cloud Certified
  Admin**.
- **Architecture** — **Enterprise Certified Architect** and **Core Certified
  Consultant**.
- **Cybersecurity Defense** — **Certified Cybersecurity Defense Analyst**,
  **Engineer**, and **Architect**.
- **Observability** — **O11y Cloud Certified Metrics User**.
- **Specialist/legacy** — Enterprise Security Certified Admin, IT Service
  Intelligence Certified Admin, and SOAR Certified Automation Developer.

Exams are delivered through **Pearson VUE**, each governed by a published **test
blueprint** with weighted topic areas, and credentials appear as **Credly**
digital badges. Higher certifications build on lower ones (for example, Power User
before Advanced Power User and before Admin).

## Design Considerations

Plan a Splunk path by **role**. Everyone starts with **SPL** — the Core track
(User → Power User → Advanced Power User) is the foundation for every other track.
Platform operators continue to **Admin** and **Architect**; security analysts take
the **Cybersecurity Defense** track (Analyst → Engineer → Architect); and
observability engineers take the **O11y** track. Because SPL underpins
everything, invest there first — most exam difficulty is fluency with search
commands and knowledge objects.

## Implementation and Automation

Splunk exam blueprints are published PDFs with weighted topic areas — the
authoritative study scope. Confirm the current blueprint before studying:

```bash
# Test blueprints live at a predictable path; parse the topic areas and weights
curl -sSL -A "Mozilla/5.0" \
  "https://www.splunk.com/en_us/pdfs/training/splunk-test-blueprint-power-user.pdf" \
  -o pu.pdf && echo "downloaded $(wc -c < pu.pdf) bytes (parse with a PDF reader)"
```

The labs in this volume use **illustrative SPL** and configuration you can adapt
to a Splunk instance (a free Splunk Enterprise trial or Splunk Cloud), the way
the exams test practical search and administration.

## Validation and Troubleshooting

Confirm a credential's blueprint, prerequisites, and format:

```text
splunk.com > Training & Certification > open the certification:
  - the test blueprint (weighted topic areas)
  - prerequisites (e.g., Power User before Advanced Power User/Admin)
  - exam length and delivery (Pearson VUE)
```

Common pitfalls: skipping **SPL fluency** and stalling on later exams; studying an
**old blueprint** (the program added the Advanced Power User and the Cybersecurity
Defense track); and confusing **Splunk Cloud** vs **Splunk Enterprise** admin
scope.

## Security and Best Practices

Verify facts on **splunk.com**, never a dump site. Practice on a real instance
(trial or Cloud). Learn **efficient SPL** (filter early, transform late, use
`tstats` and acceleration) — it is both good practice and heavily tested. For the
security track, ground detections in a framework (MITRE ATT&CK) and the **Common
Information Model (CIM)** for normalized data.

## References and Knowledge Checks

- splunk.com: Training & Certification tracks; per-exam test blueprints; the SPL documentation.

**Knowledge checks**

1. Why is the Core (SPL) track the foundation for every other Splunk track?
2. What is a test blueprint, and why check it before studying?
3. How do Splunk Enterprise and Splunk Cloud admin scopes differ?

## Hands-On Lab

Exam-preparation walkthroughs for reading the program and preparing to practice.

**Shared prerequisites for Labs 1.1–1.3** — a shell with `curl`; access to a
Splunk instance (free trial or Cloud) to run the SPL. **Cost:** none (trial).

### Lab 1.1 — Enumerate the certification tracks (Topic: Read the program)

**Objective:** List the current certifications from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.splunk.com/en_us/training/certification-track.html" \
  | grep -oiE 'Certified (User|Power User|Advanced Power User|Admin|Architect|Consultant|Cybersecurity Defense (Analyst|Engineer|Architect)|Metrics User)' \
  | sort -u | head
```

**Expected result:** the current certifications across the tracks — Core, Admin,
Architect/Consultant, the Cybersecurity Defense trio, and the O11y Metrics User.

**Negative test:** rely on a pre-2024 list; it misses the **Advanced Power User**
and the **Cybersecurity Defense** track — use the live page.

**Cleanup:** none.

### Lab 1.2 — Read a test blueprint (Topic: Verify currency)

**Objective:** Download a blueprint and see its weighted topic areas.

```bash
curl -sSL -A "Mozilla/5.0" \
  "https://www.splunk.com/en_us/pdfs/training/splunk-test-blueprint-power-user.pdf" -o pu.pdf
echo "Power User blueprint: $(wc -c < pu.pdf) bytes — topic areas with weights inside."
```

**Expected result:** the Power User blueprint PDF (topic areas such as Correlating
Events 15%, Data Models 10%) — the authoritative study scope.

**Negative test:** study from a random course syllabus; the **blueprint** defines
the exam — start there.

**Cleanup:** `rm -f pu.pdf`

### Lab 1.3 — Run your first SPL search (Topic: SPL foundation)

**Objective:** Confirm the SPL pattern every Splunk exam builds on.

```text
index=_internal | stats count by sourcetype | sort -count | head 10
```

**Expected result (in Splunk)::** a table of internal sourcetypes by event count —
the search → transform (`stats`) → sort pattern that is the heart of SPL.

**Negative test:** expect results with no `index=`; scope every search to an index
and time range — unscoped searches are slow and may return nothing.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Splunk (now a Cisco company) certifies the SPL-based search, administration,
security, and observability of machine data across five tracks — Core, Admin,
Architecture, Cybersecurity Defense, and Observability — with Pearson VUE exams
governed by published test blueprints. SPL is the foundation for every track.

- [ ] I can map the Splunk tracks and their certifications.
- [ ] I can find and read a test blueprint.
- [ ] I can run a basic SPL search → transform → sort.
- [ ] I understand the SPL-first path through the program.
- [ ] I completed Labs 1.1–1.3 including each negative test.
