# Volume XXXIV Glossary

Definitions for terms introduced in **Volume XXXIV — Google Cloud
Certification Tracks**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter each term is
drawn from, and the [master glossary](../../GLOSSARY.md) for cross-volume
terminology.

**Additive roles** — The Google Cloud IAM property that a principal's
effective permissions are the union of every role granted at and above a
resource. Granting a narrow role does not constrain a broad one; access is
removed by removing bindings or by an explicit deny policy. Introduced in
Chapter 03.

**Basic roles** — The legacy, very broad Google Cloud IAM roles (Owner,
Editor, Viewer) that predate finer-grained IAM. Editor in particular
grants far more than its name suggests; predefined roles are the correct
default. Introduced in Chapter 03.

**Case study (Professional Cloud Architect)** — A published fictional
company scenario, available in advance on the exam guide, that a portion
of the architect exam's questions reference. Reading them before exam day
is free preparation. Introduced in Chapter 05.

**Clustering (BigQuery)** — Sorting data within partitions by chosen
columns so filtered and aggregated queries scan less. Complements
partitioning. Introduced in Chapter 08.

**CMEK (customer-managed encryption keys)** — Encryption using keys you
create and control in Cloud KMS rather than Google-managed keys. Justified
when a requirement names key control, and it places key availability in
the data path — disabling a key blocks writes. Introduced in Chapter 07.

**Dry run (BigQuery)** — Running a query with `--dry_run` to report the
bytes it would scan without executing it or incurring cost. The
fundamental cost-control habit on BigQuery. Introduced in Chapter 04.

**Error budget** — The allowed unreliability implied by an SLO. A 99.9%
target over 28 days permits about 40 minutes of failure, which is spent
deliberately on releases and risk; when exhausted, releases pause.
Introduced in Chapter 06.

**Global VPC** — Google Cloud's VPC spans every region, with regional
subnets that route to each other without peering. This differs from AWS
VPCs and Azure virtual networks, which are regional, and it removes the
connectivity motive for hub-and-spoke topology. Introduced in Chapter 06.

**Organization policy** — Constraints applied at organization, folder, or
project scope that restrict what may be configured, independent of IAM and
binding even on Owners. Answers *what may be configured*. Introduced in
Chapter 05.

**Partitioning (BigQuery)** — Dividing a table by ingestion time or a date
column so queries filtering on that column prune whole partitions. A
`WHERE` clause alone does not prune; the table must be partitioned on the
filtered column. Introduced in Chapter 08.

**Predefined roles** — Curated, service-specific Google Cloud IAM roles
(for example `roles/storage.objectViewer`). The normal choice, in
preference to basic roles or custom ones. Introduced in Chapter 03.

**Project** — Google Cloud's fundamental unit of resource ownership,
billing attribution, and IAM scope. Deleting a project removes everything
in it, which makes it the most reliable lab teardown. Introduced in
Chapter 02.

**Resource hierarchy** — Organization → folders → projects → resources.
IAM policies and organization policies set high in the hierarchy are
inherited downward. Introduced in Chapter 02.

**Service account** — An identity for a workload rather than a person.
It is both a principal (it can hold roles) and a resource (principals can
hold roles on it, such as impersonation). Prefer attaching one to a
resource over issuing long-lived keys. Introduced in Chapter 03.

**Shared VPC** — An arrangement where a host project owns the network and
service projects attach to it and run workloads on its subnets,
separating network administration from workload administration.
Introduced in Chapter 05.

**SLI (service level indicator)** — A measured indicator of service
behavior, such as request latency or error rate. Introduced in Chapter 06.

**SLO (service level objective)** — A target for an SLI over a window, for
example 99.9% of requests under 300 ms over 28 days. An SLO set on an
infrastructure metric rather than user-visible behavior is not really an
SLO. Introduced in Chapter 06.

**Spanner** — Google Cloud's globally distributed, strongly consistent
relational database. Its distinctive combination is global scale **and**
strong consistency **and** relational semantics; a requirement lacking one
of the three usually points to a cheaper service. Introduced in
Chapter 08.

**Toil** — Manual, repetitive, automatable operational work. Reducing it
is a central SRE objective and an examinable concept. Introduced in
Chapter 06.

**Training/serving skew** — A mismatch between the data or feature
processing used to train a model and that used when serving it. Invisible
in offline metrics and detectable only through production monitoring,
which is why the ML certification weights MLOps heavily. Introduced in
Chapter 08.

**VPC Service Controls** — A service perimeter around Google-managed
services that prevents data being read out of the perimeter even by an
identity holding valid IAM permissions. Answers *where data may go* and
mitigates exfiltration that IAM cannot. Introduced in Chapter 07.

**Workload Identity Federation** — A mechanism letting external workloads
assume Google Cloud identities without long-lived service account keys.
The preferred alternative to distributing key files. Introduced in
Chapter 07.
