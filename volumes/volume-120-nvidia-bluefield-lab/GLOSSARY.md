# Volume CXX Glossary

Definitions for terms introduced in **Volume CXX — NVIDIA BlueField Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **BlueField DPU** — NVIDIA's data processing unit on a server's network adapter, with its own Arm cores and OS, that enforces segmentation at the NIC out-of-band of the host CPU.
- **DOCA** — NVIDIA's software framework for programming BlueField DPUs (services, offloads, and segmentation).
- **DPU namespace** — in the Track 2 model, the separate network namespace that holds a workload's enforcement policy; the workload's only path to the network passes through it and the workload cannot access it.
- **Isolated trust domain** — the property that the DPU is a separate computer from the host, so a compromised host CPU cannot see or change the DPU's policy.
- **Offload** — running enforcement (decision and datapath) on the DPU rather than the host CPU, at zero host-CPU cost and line rate.
- **Out-of-band enforcement** — applying policy beside the workload but outside its trust boundary, so the segmentation survives host compromise.
- **Per-workload policy** — a default-deny policy on each workload's DPU permitting only that workload's sanctioned flow.
- **Track 1 / Track 2** — the two lab paths: BlueField/DOCA at design level (Track 1) and a buildable out-of-band model where each workload sits behind an inaccessible DPU namespace (Track 2).
