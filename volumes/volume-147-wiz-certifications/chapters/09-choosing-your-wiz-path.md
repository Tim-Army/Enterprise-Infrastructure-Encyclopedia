# Chapter 09: Choosing Your Wiz Path

## Learning Objectives

- Sequence a Wiz certification path by role and pillar.
- Understand currency — the two-year cycle and a fast-moving platform.
- Place Wiz certification in the cloud-security career.
- Assemble the volume into a study and career plan.

*Cert relevance: this chapter is the meta-guide — how to navigate the young, expanding ladder [Chapter 1](01-the-wiz-certified-program.md) laid out.*

## Sequencing your path

The path follows the [pillar that matches your job](01-the-wiz-certified-program.md), built on the Cloud Fundamentals keystone:

| You are | Start | Then |
|:---|:---|:---|
| **Cloud security engineer** | Cloud Fundamentals | specialized Cloud exams as they release |
| **New Wiz user / analyst** | Cloud User → Cloud Fundamentals | your pillar's specialization |
| **SOC / incident responder** | Cloud Fundamentals (context) | **Defend Fundamentals** |
| **DevSecOps / platform** | Cloud Fundamentals | Wiz Code specialization as it grows |

**Cloud Fundamentals is nearly everyone's anchor** — Wiz built it as the prerequisite for the specialized exams, so it is the sensible first proctored exam even for a SOC or dev path, because every pillar assumes the graph-and-posture fundamentals it validates. From there, climb toward the pillar your job lives on: **Defend Fundamentals** for detection/response, Wiz Code specializations for shift-left, deeper Cloud exams for posture.

Because the program is **young and expanding**, treat the *available* exams as a moving set and the *pillars* as the stable map. The durable move: get Cloud Fundamentals, then take whatever specialization matches your pillar as Wiz releases it.

## Currency

Wiz certifications carry a **two-year validity** (confirmed for Defend Fundamentals). Two years is short — and deliberately so, because **cloud security moves fast**: cloud providers ship services weekly, attack techniques evolve, and Wiz itself adds capabilities (Posture Issues, new detections, AI security) on a steady cadence. A two-year cycle keeps the credential honest against a platform and a threat landscape that will not sit still.

The renewal discipline is the same as [every currency-sensitive program on this shelf](../../volume-050-crowdstrike-certifications/README.md): the ground moving *under* a cert is why it expires. Pair the two-year renewal with continuous learning through the free **CloudSec Academy**, and treat each major cloud and Wiz release as the drumbeat that keeps your *knowledge* — not just your badge — current.

## The cloud-security career

Wiz sits at the center of a growing, well-paid specialty: **cloud is where the workloads and the breaches are**, and CNAPP is how organizations get their arms around cloud risk. A Wiz-certified engineer owns the platform that consolidates CSPM, CWPP, CIEM, and DSPM and thinks in attack paths — exactly the skills the market is hiring for.

The career pairs naturally with adjacent skills this shelf covers:

- **[AWS](../../volume-017-aws-architecture-security/README.md) / [Azure](../../volume-033-microsoft-azure-certifications/README.md) / [GCP](../../volume-034-google-cloud-certifications/README.md)** — you cannot secure clouds you do not understand; cloud-provider skills are the substrate.
- **[Microsegmentation (LXXXVII)](../../volume-087-microsegmentation-options/README.md) and the Zero-Trust shelf** — attack-path thinking is the posture side of the segmentation story.
- **[Splunk (XLV)](../../volume-045-splunk-certifications/README.md) / SIEM and SOC** — Wiz Defend telemetry feeds the same detection pipeline.
- **[Prisma/Palo Alto Cloud (LXV)](../../volume-065-palo-alto-networks-certifications/README.md), [CrowdStrike (L)](../../volume-050-crowdstrike-certifications/README.md)** — the competitive CNAPP/CDR landscape you should be able to compare.

Wiz is the graph-based, agentless CNAPP specialty in a world that runs on cloud. The lab assembles your plan.

## Hands-On Lab

Python assembles a personal Wiz plan. **Cost:** none.

### Lab 9.1 — Build your Wiz path and pace currency

**Objective:** Generate a role-appropriate sequence with renewal planning.

```bash
python3 - <<'EOF'
PATHS = {
  "cloud security engineer": [
    ("Cloud Fundamentals", "the keystone — graph, posture, attack paths", "2 years"),
    ("(Cloud specializations)", "deeper posture exams as Wiz releases them", "2 years"),
  ],
  "SOC / incident responder": [
    ("Cloud Fundamentals", "context: the graph and posture the SOC relies on", "2 years"),
    ("Defend Fundamentals", "runtime detection & response (60Q/150min)", "2 years"),
  ],
  "DevSecOps / platform": [
    ("Cloud Fundamentals", "the keystone all pillars assume", "2 years"),
    ("(Wiz Code specialization)", "shift-left: code/IaC/secrets, as it grows", "2 years"),
  ],
}
role = "SOC / incident responder"   # change to taste
print(f"Wiz path for: {role}\n")
print(f"   {'step':26}{'validity':>10}   focus")
for exam, focus, val in PATHS[role]:
    print(f"   {exam:26}{val:>10}   {focus}")
print("\n   renewal: every 2 years (short, because cloud security moves fast)")
print("\nGuidance:")
print("  - anchor on CLOUD FUNDAMENTALS first — Wiz built it as the prerequisite; every")
print("    pillar assumes the graph + posture it validates.")
print("  - then climb toward YOUR pillar: Defend Fundamentals (SOC), Wiz Code (dev),")
print("    deeper Cloud exams (posture).")
print("  - the program is YOUNG + EXPANDING: treat available exams as a moving set,")
print("    the PILLARS as the stable map. Take each specialization as Wiz ships it.")
print("  - pace the 2-year renewal with the FREE CloudSec Academy; let each major cloud")
print("    and Wiz release refresh your KNOWLEDGE, not just your badge.")
EOF
```

**Expected result:** A role-specific sequence anchored on Cloud Fundamentals with a two-year renewal cadence and the pillar specialization on top. The build-your-path lesson is to anchor on the prerequisite keystone, climb toward your pillar as exams release, and pace the short renewal with the free CloudSec Academy against a fast-moving cloud landscape.

**Negative test:** Waiting for a "complete" Wiz certification catalog before starting. The program is expanding by design; Cloud Fundamentals exists now and anchors every path — starting there beats waiting for a lineup that will keep growing.

**Cleanup:** None.

### Lab 9.2 — Position Wiz in the cloud-security career

**Objective:** Map Wiz skills to adjacent competencies for a rounded profile.

```bash
python3 - <<'EOF'
ADJACENCIES = [
  ("Wiz (CNAPP)",       "graph-based cloud risk + attack paths", "the specialty itself"),
  ("AWS/Azure/GCP",     "cloud provider fundamentals",           "you can't secure what you don't understand"),
  ("Microseg / ZTNA",   "segmentation + zero trust",             "the network side of attack-path reduction"),
  ("Splunk / SIEM",     "detection engineering / SOC",           "where Wiz Defend telemetry lands"),
  ("CrowdStrike/Prisma","competing CNAPP/CDR",                   "know the landscape to compare"),
  ("IaC (Terraform)",   "infrastructure as code",                "where shift-left fixes live (Wiz Code)"),
]
print("Wiz in the cloud-security skill map:\n")
print(f"   {'skill':20}{'domain':40}why it pairs")
for skill, domain, why in ADJACENCIES:
    print(f"   {skill:20}{domain:40}{why}")
print("\nThe career thesis: CLOUD is where the workloads and the breaches are, and CNAPP")
print("is how orgs get their arms around cloud risk. A Wiz-certified engineer owns the")
print("platform that consolidates CSPM/CWPP/CIEM/DSPM and thinks in ATTACK PATHS —")
print("exactly what the market hires for.")
print("\nThe rounded cloud-security engineer combines:")
print("  UNDERSTAND (AWS/Azure/GCP) — the clouds you're securing")
print("  POSTURE    (Wiz Cloud)     — find + prioritize risk by attack path")
print("  SHIFT-LEFT (Wiz Code + IaC)— fix at the source, before deploy")
print("  DETECT     (Wiz Defend + SIEM) — catch what posture didn't prevent")
print("\nNone of this is exotic — it's the same understand/harden/shift-left/detect loop")
print("the security shelf teaches, specialized to CLOUD and unified on ONE graph. Start")
print("at Cloud Fundamentals, climb your pillar, and pair it with cloud-provider and")
print("SOC skills — that's a cloud-security career, not just a certificate.")
EOF
```

**Expected result:** Wiz skills mapped to adjacent competencies — cloud-provider fundamentals, microsegmentation, SIEM, competing CNAPPs, IaC — showing the rounded understand/posture/shift-left/detect profile. The career-positioning lesson closes the volume: Wiz is the graph-based, agentless CNAPP specialty in a cloud-run world, pairing with the same cloud, segmentation, and detection skills the rest of the shelf teaches.

**Negative test:** Treating Wiz as a standalone tool skill divorced from cloud fundamentals. You cannot secure clouds you do not understand — Wiz sits on top of AWS/Azure/GCP knowledge and feeds SOC pipelines; isolating it undersells both the platform and the career.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] A Wiz path sequenced by role and pillar, anchored on the Cloud Fundamentals keystone.
- [ ] Currency understood — the two-year cycle paced against a fast-moving cloud and platform, with the free CloudSec Academy.
- [ ] Wiz positioned in the cloud-security career alongside cloud-provider, segmentation, and SOC skills.
- [ ] The volume assembled into a personal study and career plan — understand, posture, shift-left, detect.
