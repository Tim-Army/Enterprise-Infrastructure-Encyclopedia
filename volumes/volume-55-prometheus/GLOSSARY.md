# Volume LV Glossary

Definitions for terms used in **Volume LV — Prometheus**, alphabetized.
See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Alertmanager** — The component that deduplicates, groups, routes, inhibits, and
silences alerts before notifying receivers. Used in Chapter 08.

**Alerting rule** — A scheduled PromQL condition that fires an alert (after its `for`
duration) with labels and annotations. Used in Chapter 07.

**Cardinality** — The number of unique label combinations (series); the main driver of
memory and query cost. Used in Chapter 02.

**Exporter** — A sidecar process that translates a system's stats into Prometheus
metrics (node_exporter, blackbox_exporter). Used in Chapter 06.

**Exposition format** — The text format targets use to expose metrics at `/metrics`.
Used in Chapter 02.

**Histogram** — A metric type bucketing observations into cumulative `_bucket` series
plus `_sum`/`_count`; queried with `histogram_quantile`. Used in Chapters 02 and 05.

**Instant vector / range vector** — A value per series at one instant vs a range of
samples per series (`metric[5m]`). Used in Chapter 04.

**Metric types** — Counter, Gauge, Histogram, Summary. Used in Chapter 02.

**Pull model** — Prometheus scrapes targets' `/metrics` endpoints rather than receiving
pushed data. Used in Chapter 01.

**Pushgateway** — A component that holds metrics pushed by short-lived batch jobs for
Prometheus to scrape. Used in Chapter 06.

**PromQL** — Prometheus's query language for selecting, aggregating, and computing over
time series. Used in Chapters 04–05.

**promtool** — The Prometheus CLI for validating config/rules and unit-testing rules.
Used in Chapters 03 and 07.

**Recording rule** — A scheduled PromQL expression saved as a new series to precompute
reused queries. Used in Chapter 07.

**Relabeling** — Transforming target/label sets before or after scraping. Used in
Chapter 03.

**Remote write** — Streaming samples to a long-term/global backend (Thanos, Mimir,
Cortex). Used in Chapter 09.

**Scrape config** — A job defining targets (static or via service discovery) and scrape
settings. Used in Chapter 03.

**TSDB** — Prometheus's local time-series database (2-hour blocks, retention window).
Used in Chapter 09.

**Vector matching** — Joining two vectors on shared labels, one-to-one or many-to-one
(`group_left`/`group_right`). Used in Chapter 05.
