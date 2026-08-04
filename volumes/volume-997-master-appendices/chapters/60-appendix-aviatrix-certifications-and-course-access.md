# Chapter 60: Appendix — Aviatrix Certifications and Course Access

The **Aviatrix Certified Engineer (ACE)** program — the multicloud-networking certifications, their
sequence, and the training/access model. Verified on **3 August 2026** from **aviatrix.ai/training**
(the ACE program, Associate, and Professional pages), the sources that anchor
[Volume CXXVI — Aviatrix Certification Tracks](../../volume-126-aviatrix-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** The **ACE Associate is free and self-paced** (register on aviatrix.ai; the current
enrollment code was `acemulticloud`, and it **includes the final exam**) — no cloud accounts required.
It is the **mandatory prerequisite** for **ACE Professional**, a **3-day instructor-led** course with
hands-on labs (prerequisite: Associate + ~1 year of public-cloud experience). **ACE Design Expert** is
the design capstone. Focused **ACE** courses (Security, Hybrid Cloud, Cloud Backbone, Automation,
Operations) add depth. Training is delivered through the Aviatrix ACE Academy (Skilljar-hosted); the
community lives at community.aviatrix.com.

> **Currency.** Aviatrix reshapes its focused-course lineup and expands **Distributed Cloud Firewall**
> (its distributed-segmentation feature) over time, and the native clouds change what the overlay
> abstracts. Re-verify the ACE catalog and the DCF model on aviatrix.ai before planning. The **ACE
> Associate's free status and enrollment code can change** — confirm on the Associate page.

## Free and low-cost resources and entry points

- **[Aviatrix ACE program](https://aviatrix.ai/training/ace/)** — the authoritative program page and
  course catalog
- **[ACE Associate](https://aviatrix.ai/training/ace-associate/)** — the free, self-paced foundational
  course + exam (no cloud accounts needed)
- **[ACE Professional](https://aviatrix.ai/training/ace-professional/)** — the instructor-led hands-on
  course
- **[ACE Academy](https://ace.aviatrix.com/)** — the training portal
- **[Aviatrix Community](https://community.aviatrix.com/)** — Q&A and study support
- **Free study lab:** any Linux host with `iproute2`, `nftables`, `frr`, `wireguard-tools`, and
  `terraform` models the transit/egress/firewall/VPN concepts (see the volume's labs)

## Fees, delivery, and renewal

- **Fees:** **ACE Associate is free** (self-paced, includes the exam). ACE Professional, Design Expert,
  and focused courses are paid instructor-led offerings — confirm current pricing on aviatrix.ai.
- **Delivery:** Associate is self-paced (~4 hours) with a final exam; Professional is 3 days of
  virtual instructor-led training with demos and hands-on labs; Design Expert and focused courses are
  instructor-led.
- **Prerequisites:** none for the Associate; **ACE Professional requires the Associate** plus ~1 year
  of public-cloud experience and expert-level VPC/TGW/IGW/VGW (AWS) and equivalent (Azure) knowledge.
- **Validity/renewal:** confirm the current validity policy on aviatrix.ai; the program and the
  underlying clouds evolve, so periodic re-verification is the intended posture.

## The certifications

Verified against aviatrix.ai on 3 August 2026.

| Credential | Format | Prerequisite | Focus |
| --- | --- | --- | --- |
| ACE Associate | Self-paced (~4 hrs) + final exam; **FREE** | none | Multicloud networking foundations (AWS/Azure/GCP/OCI): native constructs, transit, egress, VPN, firewall, encryption |
| ACE Professional | Instructor-led, 3 days + hands-on labs + exam | ACE Associate + ~1 yr cloud experience | Multicloud transit + HA, traffic inspection/firewall insertion, remote user access, egress filtering, encryption, native constraints |
| ACE Design Expert | Instructor-led | Professional-level knowledge | Designing scalable, resilient multicloud networks |
| ACE Security | Instructor-led (focused) | — | Securing cloud networks |
| ACE Hybrid Cloud | Instructor-led (focused) | — | Secure hybrid connectivity |
| ACE Cloud Backbone | Instructor-led (focused) | — | Edge-to-cloud backbone networking |
| ACE Automation | Self-paced (focused) | — | Infrastructure-as-code / Terraform for Aviatrix |
| ACE Operations | Instructor-led (focused) | — | Cloud access, visibility, and compliance via CoPilot |

## Notes

- **The Associate is the industry on-ramp** — free, gateless, and vendor-useful (multicloud networking
  fundamentals apply beyond Aviatrix), which is why it is the mandatory base of the ladder.
- **FireNet vs Distributed Cloud Firewall:** FireNet inserts third-party NGFWs for deep inspection; DCF
  is Aviatrix's own distributed segmentation. Both appear in Professional-level material; DCF is
  expanding.
- **Multicloud context:** this program pairs with the cloud-provider volumes
  ([AWS XVII](../../volume-017-aws-architecture-security/README.md),
  [Azure XXXIII](../../volume-033-microsoft-azure-certifications/README.md),
  [Google Cloud XXXIV](../../volume-034-google-cloud-certifications/README.md)) and the
  microsegmentation landscape ([LXXXVII](../../volume-087-microsegmentation-options/README.md)).
