# Volume CXXXVIII — Glossary

| Term | Definition |
|:---|:---|
| **ActiveCluster** | Everpure's active/active configuration presenting the same volume from two arrays simultaneously; requires an independent third-site mediator to prevent split brain. |
| **CEE credits** | Continuing Everpure Education credits — an alternative recertification path available for **select FlashArray exams** only. |
| **Data reduction ratio** | Data written divided by physical space used (deduplication + compression); the number to plan capacity with, unlike total efficiency. |
| **DirectFlash** | Managing raw flash from the array software rather than through commodity SSD firmware, enabling global wear levelling and consistent latency. |
| **DSA** | The Associate-level Data Storage certification; **renews automatically** when any Professional, Specialist, or Expert certification is earned. |
| **Evergreen** | The architecture allowing controllers, media, and capacity to be upgraded non-disruptively without repurchasing the array. |
| **Evergreen//One** | The subscription consumption model — capacity and performance as a service, with the vendor carrying refresh risk. |
| **Everpure** | The current name of the company formerly called Pure Storage; certifications are branded Everpure while product names are unchanged. |
| **FlashArray** | Block storage for databases, virtualization, and general enterprise workloads. |
| **FlashBlade** | Unified file and object storage for unstructured data, built to scale out. |
| **FlashBlade//EXA** | The high-performance FlashBlade variant for AI and HPC pipelines, where sustained parallel bandwidth matters more than IOPS. |
| **Host group** | A set of hosts sharing volumes — the correct construct for a genuine cluster, and the safe way to map one volume to several servers. |
| **Portworx** | Cloud-native storage providing persistent volumes for stateful Kubernetes workloads, surviving pod rescheduling and node failure. |
| **Protection group** | A set of volumes snapshotted and replicated atomically, so a multi-volume application yields one consistent point in time. |
| **Retention lock** | Storage-enforced immutability preventing a snapshot's deletion or early expiry — including by an administrator; lifting it requires an out-of-band process. |
| **Scale-out** | Growing capacity and performance together by adding blades, so per-terabyte performance stays flat as the dataset grows. |
| **Split brain** | Both arrays in an active/active pair continuing to serve after losing contact, producing divergent copies; prevented by a mediator. |
| **Thin provisioning** | Allocating capacity that has not yet been written; inflates "total efficiency" figures and defers rather than removes the capacity requirement. |
| **Total efficiency** | Data reduction *plus* thin provisioning — a larger, less useful number for capacity planning. |
