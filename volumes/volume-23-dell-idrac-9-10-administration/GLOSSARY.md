# Volume XXIII Glossary

Definitions for terms introduced in **Volume XXIII — Dell iDRAC 9 and 10
Administration**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Active Directory integration** — iDRAC's centralized authentication
mechanism against Microsoft Active Directory, supporting a "standard
schema" mode requiring no AD schema extension and a legacy "extended
schema" mode requiring one. Introduced in Chapter 04.

**Attribute Registry** — The live, firmware-specific enumeration of every
configurable iDRAC attribute and its valid values, retrievable from a
running unit and treated as the authoritative source over hardcoded
assumptions in automation. Introduced in Chapter 01.

**BOSS (Boot Optimized Storage Solution)** — A dedicated, small-form-factor
boot storage controller, separate from the main PERC array, running a
mirrored (RAID 1) pair of M.2 or NVMe drives dedicated to the boot
operating system. Introduced in Chapter 07.

**Discrete privilege** — A single, narrowly scoped iDRAC permission (for
example, Virtual Console access, or configuration write access) that can
be combined into a custom role rather than relying only on the built-in
Administrator/Operator/ReadOnly presets. Introduced in Chapter 04.

**Factory reset** — An operation that returns iDRAC's own configuration
(network settings, local users, certificates, alerting) to factory
defaults, without touching host OS storage, BIOS settings, or RAID
configuration. Introduced in Chapter 02.

**Firmware catalog** — A structured manifest listing available firmware
versions and download locations for a platform generation, sourced either
from Dell's hosted online catalog or from a mirrored offline/local
repository. Introduced in Chapter 08.

**Full AC power cycle** — Physically removing and restoring power to an
entire server chassis, resetting hardware state at a level a warm reboot
or BIOS-level reset cannot reach. Introduced in Chapter 02.

**Health rollup** — iDRAC's top-level Normal/Warning/Critical summary
derived from hundreds of underlying hardware sensors, used as a
first-glance indicator before drilling into component-level detail.
Introduced in Chapter 06.

**Hot spare** — A physical disk assigned to a controller or a specific
virtual disk, held in reserve to begin an automatic rebuild immediately
upon a real or predicted drive failure. Introduced in Chapter 07.

**HBA mode** — A PERC controller mode presenting physical disks directly
to the OS with no RAID abstraction, used when an overlying OS or platform
provides its own redundancy and storage management. Also called
pass-through or non-RAID mode. Introduced in Chapter 07.

**Idempotent automation** — Automation designed so that running the same
operation multiple times produces the same end state as running it once,
checking current state before changing it. Introduced in Chapter 09
(general principle defined in Volume I, Chapter 03).

**iDRAC (integrated Dell Remote Access Controller)** — The baseboard
management controller built into every Dell PowerEdge server, providing
out-of-band management independent of the host operating system and, for
most functions, of host power state. Introduced in Chapter 01.

**iDRAC Direct** — A local, network-independent connection to iDRAC over
a front-panel USB port, usable for configuration and recovery when the
management network path itself is unavailable or misconfigured.
Introduced in Chapter 05.

**iDRAC Service Module (iSM)** — An optional, lightweight in-OS agent
extending iDRAC's visibility with information easier to gather in-band:
OS version, some in-band drive wear data, and cluster awareness.
Introduced in Chapter 05.

**iDRAC9 / iDRAC10** — The two current iDRAC hardware generations covered
in this volume: iDRAC9 spans 14th–16th generation PowerEdge platforms;
iDRAC10 spans 17th generation and current platforms. Introduced in
Chapter 01.

**Lifecycle Controller (LC)** — Embedded systems-management firmware,
stored in dedicated flash separate from BIOS, providing hardware
configuration, firmware update orchestration, diagnostics, and OS
deployment without depending on a host OS agent. Introduced in Chapter
01.

**Lifecycle Log** — A persistent iDRAC-resident log recording
configuration changes, firmware update history, job execution, user
login/logout events, and hardware events on a single correlated timeline.
Introduced in Chapter 06.

**License tier** — The purchasable entitlement level (Basic, Express,
Enterprise, Datacenter, illustratively) that gates progressively more
iDRAC capability, such as Virtual Console/Media or directory integration.
Introduced in Chapter 01.

**NIC failover** — An iDRAC network setting allowing management traffic
to fail over from the dedicated port to a shared LOM port (or between LOM
ports) if the primary path loses link. Introduced in Chapter 03.

**NIC selection** — The iDRAC setting determining which physical network
port — dedicated or a specific shared LOM port — carries iDRAC management
traffic. Introduced in Chapter 03.

**OS-to-iDRAC Pass-through** — An Enterprise-tier capability letting the
iDRAC Service Module communicate with iDRAC over an internal USB-based
path rather than requiring host OS network access to the management
network. Introduced in Chapter 05.

**PERC (PowerEdge RAID Controller)** — Dell's storage controller family,
available as an add-in card or integrated on the motherboard, managed
through iDRAC's Storage service. Introduced in Chapter 07.

**Power capping** — An administrator-configured ceiling on server power
draw, enforced by iDRAC throttling CPU performance states as needed to
stay under the configured limit. Introduced in Chapter 06.

**Predictive failure** — A drive health state, based on manufacturer
SMART thresholds, indicating a drive is likely to fail before it actually
does, intended to trigger proactive replacement. Introduced in Chapter
07.

**PSU redundancy policy** — The configured mode (no redundancy, AC
redundancy, or PSU redundancy) determining how iDRAC alerts on and
manages loss of a power supply or power feed. Introduced in Chapter 06.

**Quick Sync** — Bluetooth Low Energy and NFC-based access to basic iDRAC
status and limited configuration from a mobile device, without requiring
a network connection. Introduced in Chapter 05.

**RACADM** — iDRAC's command-line management interface, usable locally or
remotely (typically over SSH), built around an attribute-group model
(`iDRAC.NIC.Selection` and similar) predating Redfish adoption.
Introduced in Chapter 01.

**Redfish** — The DMTF-standard, HTTP/JSON RESTful management API and
Dell's strategic direction for iDRAC automation, used for all scripted
examples throughout this volume. Introduced in Chapter 01.

**Redfish EventService** — The subscription-based webhook eventing model
defined by the Redfish standard, letting iDRAC push alerts to a listener
URL rather than requiring a consumer to poll. Introduced in Chapter 06.

**Rollback (firmware)** — Reverting a component to its immediately
previous firmware version using Lifecycle Controller's retained prior
image, available only for the immediately prior version and not for every
update type. Introduced in Chapter 08.

**Server Configuration Profile (SCP)** — Lifecycle Controller's
structured export/import document (XML or JSON) capturing iDRAC, BIOS,
NIC, and storage controller settings, used for backup, templating, and
recovery. Introduced in Chapter 02.

**Session-token authentication** — An authentication pattern where a
client exchanges credentials once for a short-lived token (`X-Auth-Token`
in the Redfish response header), used for all subsequent calls and
explicitly deleted when the automation session ends. Introduced in
Chapter 01.

**Silicon root of trust** — A hardware-anchored cryptographic trust chain
validating iDRAC firmware itself before it runs, extending up through
BIOS, closing firmware-implant attack classes that predate any
software-level control. Introduced in Chapter 04.

**SimpleUpdate** — The DMTF-standard Redfish `UpdateService` action used
to submit a firmware image for application, supporting staged
(`OnReset`) or immediate application. Introduced in Chapter 08.

**Secure Boot** — A BIOS-level control, reportable through iDRAC, that
refuses to execute unsigned or improperly signed boot loader and OS
kernel components, extending the silicon root of trust chain to the boot
path. Introduced in Chapter 04.

**Standard schema (Active Directory)** — An Active Directory integration
mode mapping AD group membership to iDRAC roles using generic AD groups
and attributes, without requiring an AD schema extension. Introduced in
Chapter 04.

**System Erase** — A comprehensive Lifecycle Controller sanitization
capability that can wipe iDRAC configuration, BIOS settings, diagnostics,
Lifecycle Controller data, NVRAM, and (where supported) trigger
storage-level secure erase — the correct tool for decommissioning,
distinct from factory reset. Introduced in Chapter 04.

**System Event Log (SEL)** — A hardware-event-focused, IPMI-aligned
persistent log recording sensor threshold crossings and component state
changes. Introduced in Chapter 06.

**System Lockdown Mode** — A Datacenter-tier capability freezing current
hardware and firmware configuration against further changes until
explicitly unlocked, used to prevent configuration drift on
security-sensitive production workloads. Introduced in Chapter 04.

**Tech Support Report (TSR)** — A comprehensive, on-demand diagnostic
bundle covering hardware inventory, sensor readings, logs, and firmware
inventory, formatted for Dell support case attachment. Introduced in
Chapter 06.

**Unified Server Configurator (USC)** — The local, POST-time (F10)
interface to the Lifecycle Controller, providing hardware configuration,
firmware update, diagnostics, and OS deployment without any network
dependency. Introduced in Chapter 01.

**Virtual Console** — A browser-based HTML5 remote KVM session providing
full keyboard, video, and mouse access including BIOS POST and OS
installer interaction. Introduced in Chapter 05.

**Virtual Media** — A capability that attaches a remote ISO/IMG image to
a server as if it were a physically inserted optical or USB device,
sourced from a local browser upload or a network share. Introduced in
Chapter 05.

**VLAN tagging (iDRAC NIC)** — Applying an 802.1Q VLAN tag directly to
iDRAC's own management traffic, isolating it onto a distinct VLAN even
when sharing a physical port with host production traffic. Introduced in
Chapter 03.

**WS-Management (WSMAN)** — An older SOAP-based management protocol
supported by iDRAC for backward compatibility, superseded by Redfish as
the strategic automation interface. Introduced in Chapter 09.
