# Volume LIII Glossary

Definitions for terms used in **Volume LIII — LibreNMS**, alphabetized.
See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Alert rule** — A condition over device/port/sensor state that, when matched, fires a
notification. Used in Chapter 04.

**Application** — An agent/snmp-extend script that feeds service-level metrics (e.g.,
MySQL, nginx) beyond base SNMP. Used in Chapter 03.

**Discovery** — The process that learns a device's interfaces, sensors, neighbors, and
OS after it is added. Used in Chapter 02.

**Dispatcher** — The (Python) service that schedules discovery and polling, including
across distributed pollers. Used in Chapter 08.

**Distributed polling** — Spreading polling across multiple poller nodes coordinated by
Redis against one database. Used in Chapter 08.

**Device group** — A dynamic (rule-based) or static grouping of devices for alerting and
views. Used in Chapter 02.

**lnms** — The LibreNMS command-line tool (`device:add`, `device:poll`, etc.). Used in
Chapters 02–03.

**librenms-docker** — The community Docker project for deploying LibreNMS. Used in
Chapter 01.

**Maintenance window** — A scheduled period during which alerts for a device are
suppressed. Used in Chapter 04.

**Oxidized** — A config-backup tool LibreNMS drives to pull and version device configs.
Used in Chapter 07.

**Poller** — The process that collects metrics from devices on a schedule (default ~5
min) into RRD. Used in Chapters 03 and 08.

**rrdcached** — A daemon that batches RRDtool writes to reduce disk I/O at scale. Used
in Chapters 03 and 08.

**RRDtool** — The round-robin database engine storing LibreNMS time-series metrics. Used
in Chapters 03 and 08.

**SNMP** — Simple Network Management Protocol (v2c/v3); the agentless protocol LibreNMS
polls. Used in Chapters 01–02.

**Transport** — A delivery channel for alerts (email, Slack, webhook, PagerDuty, …).
Used in Chapter 04.

**validate.php** — The built-in health check for a LibreNMS install. Used in Chapters 01
and 09.
