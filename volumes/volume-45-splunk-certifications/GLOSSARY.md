# Volume XLV Glossary

Definitions for terms used in **Volume XLV — Splunk Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Acceleration** — Techniques (summary indexing, accelerated data models, `tstats`)
that pre-compute results so reporting searches run fast at scale. Used in Chapter
03.

**CIM (Common Information Model)** — Splunk's normalization standard that maps
fields from many sources into shared data models, so one search works across
sources; foundational for Enterprise Security. Used in Chapters 02, 06, and 07.

**Correlation search** — A scheduled ES search that generates a notable event (and
risk) when a detection condition is met. Used in Chapters 07 and 08.

**Data model** — A hierarchical, semantic mapping of data (often CIM-aligned) that
can be accelerated and queried with `tstats`/`datamodel`. Used in Chapters 02 and
03.

**Deployment server** — The Splunk component that centrally distributes
configuration apps to forwarders by server class. Used in Chapter 04.

**Forwarder** — A Splunk agent that sends data to indexers; universal (lightweight)
or heavy (parses/routes). Used in Chapter 04.

**Notable event** — An ES-generated alert record representing a potential security
incident, triaged by the analyst. Used in Chapter 06.

**RBA (Risk-Based Alerting)** — An ES approach that accumulates risk on objects and
alerts on high aggregate risk rather than every event. Used in Chapter 06.

**RF / SF (Replication Factor / Search Factor)** — Indexer-cluster settings for how
many copies of data exist (RF) and how many are searchable (SF), sizing
availability. Used in Chapter 05.

**Search head cluster** — A group of coordinated search heads (with a captain) that
share knowledge objects and provide search-tier HA. Used in Chapter 05.

**SOAR** — Splunk's Security Orchestration, Automation, and Response platform;
playbooks automate SOC response. Used in Chapters 07 and 08.

**SPL (Search Processing Language)** — Splunk's search and analysis language; the
foundation of every Splunk track. Used in Chapters 01 and 02.

**Test blueprint** — Splunk's published, weighted topic-area outline for a
certification exam. Used in Chapter 01.

**`tstats`** — A high-performance SPL command that queries indexed/accelerated data
(tsidx / data models) for fast reporting. Used in Chapters 02 and 03.
