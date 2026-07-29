# Volume LXI Glossary

Definitions for terms used in **Volume LXI — Cribl Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**CC User / CC Admin / CC Engineer / CCSC** — The Cribl certification ladder: User
(foundation), Admin (Stream/Edge), Engineer (design), Consultant (partner). Used
throughout.

**Cribl Edge** — A lightweight agent deployed at the data source to collect and forward
telemetry, managed in fleets. Used in Chapter 05.

**Cribl Lake** — Managed, low-cost object storage organized into datasets, with retention
and replay. Used in Chapter 07.

**Cribl Search** — Query data in place (object storage/Lake/live) without ingesting it
first. Used in Chapter 07.

**Cribl Stream** — The core engine that routes, reduces, enriches, and replays telemetry
via pipelines. Used in Chapters 02–04.

**Destination** — A Stream output (where processed data is sent). Used in Chapter 03.

**Fleet** — A Leader-managed group of Edge nodes with hierarchical configuration. Used in
Chapter 05.

**Function** — A pipeline step operating on events (Eval, Drop, Mask, Lookup, …). Used in
Chapter 04.

**Leader** — The node that manages configuration and distributes it to worker groups/
fleets. Used in Chapter 08.

**Pack** — A reusable, shareable bundle of pipelines, routes, lookups, and samples. Used in
Chapter 04.

**Pipeline** — An ordered series of Functions that transform events. Used in Chapter 03.

**Replay** — Reading data back from Lake/object storage through Stream to a destination.
Used in Chapters 06 and 07.

**Route** — An ordered rule that matches events with a filter and sends them to a pipeline
and destination. Used in Chapter 03.

**Source** — A Stream input (where data enters). Used in Chapter 03.

**Worker Group** — A cluster of Worker Processes that process data, managed by the Leader.
Used in Chapter 08.
