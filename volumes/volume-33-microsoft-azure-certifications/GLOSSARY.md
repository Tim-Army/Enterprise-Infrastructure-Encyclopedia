# Volume XXXIII Glossary

Definitions for terms introduced in **Volume XXXIII — Microsoft Azure
Certification Tracks**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter each term is
drawn from, and the [master glossary](../../GLOSSARY.md) for cross-volume
terminology.

**AB (exam code family)** — The exam-code prefix introduced with the AI
Agent Builder Associate certification (AB-620). Its creation signals that
Microsoft judges agent building a distinct enough role to certify
separately. Introduced in Chapter 01.

**Availability zone** — A physically separate location within an Azure
region, with independent power, cooling, and networking, used to survive
the loss of a single data center. Introduced in Chapter 02.

**Azure Policy** — The governance mechanism that evaluates resources
against rules and can audit, deny, or remediate them regardless of who is
acting — including subscription owners. It governs *what may exist*, in
contrast to RBAC. Introduced in Chapter 03.

**Azure Virtual WAN** — Microsoft's managed networking hub, providing
transitive routing between connected networks without the manual route
management a self-built hub-and-spoke topology requires. Introduced in
Chapter 04.

**Consistency level (Cosmos DB)** — One of five tunable guarantees
(strong through eventual) trading read latency and availability against
how stale a read may be. Introduced in Chapter 07.

**ExpressRoute** — A private circuit between an organization and Azure
provided through a connectivity partner, offering predictable latency and
a path that does not traverse the public internet, in contrast to
Site-to-Site VPN. Introduced in Chapter 04.

**Hub-and-spoke** — A topology placing shared services in a hub virtual
network with workload spokes peered to it. Because peering is not
transitive, spoke-to-spoke traffic requires an appliance in the hub with
user-defined routes, or direct spoke peering. Introduced in Chapter 04.

**Management group** — A container above subscriptions in the Azure
hierarchy, used to apply RBAC and Policy across many subscriptions at
once. Introduced in Chapter 02.

**Microsoft Foundry** — The Microsoft platform for building AI
applications and agents, named explicitly in the Azure AI Apps and Agents
Developer (AI-103) certification description. Introduced in Chapter 06.

**Partition key (Cosmos DB)** — The property determining how documents
are distributed across physical partitions. It governs performance and
cost more than any other design decision and cannot be changed without
moving the data; a low-cardinality key produces hot partitions.
Introduced in Chapter 07.

**Peering, virtual network** — A direct connection between two virtual
networks over the Microsoft backbone. Peering is **not transitive**, which
is the organizing constraint of Azure topology design. Introduced in
Chapter 04.

**Private Endpoint** — A private IP address from your own subnet placed in
front of a PaaS service, allowing that service to be reached over private
address space and cut off from the public internet entirely. Stronger than
a service endpoint. Introduced in Chapter 04.

**RBAC (role-based access control)** — The Azure mechanism granting a
security principal permission to perform operations at a scope. It governs
*who may act*, in contrast to Azure Policy. Introduced in Chapter 03.

**Renewal assessment** — The free, online, unproctored assessment on
Microsoft Learn that renews a role-based Azure certification for another
year, available in the six months before expiry. Fundamentals
certifications do not expire and need none. Introduced in Chapter 01.

**Resource group** — A lifecycle container for Azure resources that are
typically created, managed, and deleted together. Introduced in
Chapter 02.

**RPO (recovery point objective)** — The maximum acceptable data loss,
expressed as time. It selects the replication and backup frequency in a
continuity design. Introduced in Chapter 08.

**RTO (recovery time objective)** — The maximum acceptable time to restore
service. It selects the standby model — backup-and-restore, pilot light,
warm standby, or active-active. Introduced in Chapter 08.

**SC (exam code family)** — Microsoft's security, compliance, and identity
certification family (SC-100, SC-200, SC-300), which sits outside the
Azure-branded lineup and is the durable home for security certification
now that AZ-500 is retiring. Introduced in Chapter 05.

**Service endpoint** — A mechanism extending a virtual network's identity
to a PaaS service so the service can restrict access to that subnet.
Traffic still reaches a public endpoint, which is the key difference from
a Private Endpoint. Introduced in Chapter 04.

**Shared responsibility model** — The division between what Microsoft
secures and what the customer secures, which shifts as workloads move from
IaaS through PaaS to SaaS. Introduced in Chapter 02.

**Subscription** — The Azure billing and quota boundary, and the scope
most governance attaches to. Introduced in Chapter 02.

**User-defined route (UDR)** — A route that overrides Azure's system
routes, most often to force traffic through a network virtual appliance or
firewall. Route selection prefers user-defined routes over BGP routes over
system routes. Introduced in Chapter 04.

**what-if** — The Azure deployment operation that previews what a template
would change without applying it; the infrastructure-as-code equivalent of
a dry run. Introduced in Chapter 08.
