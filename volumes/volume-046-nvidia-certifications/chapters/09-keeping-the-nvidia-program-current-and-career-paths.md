# Chapter 09: Keeping the NVIDIA Program Current and Career Paths

## Learning Objectives

- Explain NVIDIA certification validity and recertification.
- Track program change — the fast-expanding NCP tier and new domains.
- Plan an NVIDIA career path from Associate to Professional.
- Relate NVIDIA credentials to the encyclopedia's AI, cloud, and networking volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

NVIDIA certifications are valid for a defined period (commonly **two years**) and
are renewed by **retaking the current exam** (or a higher one), since the
technology moves quickly. Training is delivered through the **NVIDIA Deep Learning
Institute (DLI)**. The program is **expanding rapidly** — the Professional (NCP)
tier has grown to cover AI infrastructure, operations, networking, data science,
generative AI, **agentic AI**, and **OpenUSD**, and the Associate tier added
**Multimodal** generative AI. Expect continued additions as the AI field evolves.

## Design Considerations

Plan a path by **role**, Associate → Professional:

- **Infrastructure/operations:** NCA-AIIO → **NCP-AII** (build) and **NCP-AIO**
  (operate), plus **NCP-AIN** (networking).
- **Data science:** NCA-ADS → **NCP-ADS**.
- **Generative/agentic AI:** NCA-GENL/GENM → **NCP-GENL**, **NCP-AAI**, and (for
  3D/simulation) **NCP-OUSD**.

Because the technology and exams change fast, keep skills current and renew before
lapse.

## Implementation and Automation

Verify currency from **nvidia.com** — the certification catalog carries the current
exams and blueprints:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nvidia.com/en-us/learn/certification/" \
  | grep -oiE 'NC[AP]-[A-Z]{3,4}' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
nvidia.com/learn/certification:
  - current exams and blueprints (weighted sections)
  - level, duration, price, and recommended experience
  - validity and recertification terms
Watch for new NCP domains (agentic AI, OpenUSD were recent additions).
```

Common pitfalls: studying an **old program map** (the NCP tier expanded a lot);
letting a credential lapse (renew by exam); and skipping the **Associate**
foundation before a Professional exam.

## Security and Best Practices

Renew by re-exam before the validity window closes. Keep practicing on **current
GPUs and software** (the stack evolves — new GPU generations, CUDA, NeMo/NIM).
Train with **DLI**. Combine credentials to match a role (e.g., NCP-AII + NCP-AIO +
NCP-AIN for a full AI-infrastructure engineer).

## References and Knowledge Checks

- nvidia.com/learn/certification: the catalog, per-exam blueprints, and recertification policy; NVIDIA DLI.

**Knowledge checks**

1. How are NVIDIA certifications renewed?
2. Which NCP domains are recent additions?
3. What is a sensible Associate → Professional path for an infrastructure engineer?

## Hands-On Lab

Exam-preparation walkthroughs for tracking change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify the current catalog (Topic: Verify currency)

**Objective:** Read the current exams from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.nvidia.com/en-us/learn/certification/" \
  | grep -oiE 'NC[AP]-[A-Z]{3,4}' | sort -u
```

**Expected result:** the current exam codes, including **NCP-AAI** and
**NCP-OUSD** — confirming the additions an old map would miss.

**Negative test:** trust a 2024 NVIDIA cert chart; the NCP tier and Multimodal
associate are newer — confirm on nvidia.com.

**Cleanup:** none.

### Lab 9.2 — Plan an Associate → Professional path (Topic: Career)

**Objective:** Map a role to a credential sequence.

```bash
python3 - <<'PY'
paths = {"AI Infra Engineer":"NCA-AIIO -> NCP-AII -> NCP-AIO (+ NCP-AIN)",
         "Data Scientist":"NCA-ADS -> NCP-ADS",
         "GenAI Developer":"NCA-GENL/GENM -> NCP-GENL -> NCP-AAI"}
for role,path in paths.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences from Associate to Professional — the
career mapping this volume supports.

**Negative test:** attempt a Professional infra exam with no hands-on cluster
experience; NVIDIA recommends **1–3 years** — build experience first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NVIDIA certifications are valid ~two years and renewed by exam, reflecting a
fast-moving field. The program has expanded quickly — the NCP tier now spans
infrastructure, operations, networking, data science, generative AI, agentic AI,
and OpenUSD. Plan a path by role from Associate to Professional, train with DLI,
and verify currency on nvidia.com.

- [ ] I can explain NVIDIA certification validity and renewal.
- [ ] I can name the recent NCP additions.
- [ ] I can map a role to an Associate → Professional path.
- [ ] I can verify the current catalog on nvidia.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
