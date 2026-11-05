# Volume CCI Glossary

Definitions for terms used in **Volume CCI — FortiSwitch STIG and SRG Mapping**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms and the
[Volume CLXXII glossary](../volume-172-disa-srgs-and-stigs/GLOSSARY.md) for
the SRG and STIG terms this volume builds on.

- **/112 lab block** — the IPv6 prefix `fd00:db8:201::/112` that holds the lab's IPv6 addresses; its last 16 bits are the segment and host, so it splits into /120 segments and cannot support SLAAC.
- **Advanced Features License** — the Fortinet license (FS-SW-LIC-600 for the FS-648F-FPOE, FS-SW-LIC-2000 for the FS-2048F) that enables Layer 3 features such as OSPF and BGP on a FortiSwitch; rows that need it list it as a prerequisite.
- **Baseline snapshot** — the saved state of every lab virtual machine and of both switch configurations that each requirement lab starts from and returns to.
- **Break-glass access** — a path to a device that does not depend on the production network, used when the normal management path is lost; in this lab, NET2 of the console server on segment 100.
- **Console server** — a device that connects to the serial console ports of other devices and offers them over the network, usually through SSH; the OpenGear IM7216-2-DAC-LMV in Chapter 08 is one.
- **FIPS-CC mode** — the FortiSwitchOS operating mode that restricts the switch to FIPS 140 and Common Criteria validated behavior; the mapped release is the FIPS-CC image.
- **FortiLink** — Fortinet's protocol for managing FortiSwitch units from a FortiGate; in managed mode, the switch's configuration lives on the FortiGate.
- **FortiSwitchOS Feature Matrix** — Fortinet's per-release document listing every FortiSwitch feature and the model series that support it.
- **Gap lab** — a lab for an SRG requirement that FortiSwitch cannot meet: it proves the setting is absent, applies the nearest compensating control, and records the disposition and residual risk.
- **Interactive crosswalk table** — the self-contained web page generated from the SRG mapping workbook, with search, filters, sorting, and CSV download for the crosswalk, prerequisites, and model-support sheets.
- **Model support sheet** — the workbook sheet that records, for each FortiSwitchOS 7.6.7 feature, whether the FS-648F-FPOE and FS-2048F support it.
- **Negative test** — a test that tries to break a control and shows that it blocks what it should; it pairs with a positive test that shows the control permits what it should.
- **Out-of-band management** — management access over a network or link that carries no production traffic; segment 0 and the console server's serial and cellular paths are examples.
- **RadSec** — RADIUS carried inside a TLS session (RFC 6614), used to encrypt credentials between a switch and a RADIUS server.
- **Requirement lab** — a lab that configures the FortiSwitch setting for an SRG requirement and proves it with a positive and a negative test.
- **Routed link** — a point-to-point link (L1 to L5) between two routers in the lab, addressed with a /31 in IPv4 and a /127 in IPv6.
- **Segment (lab)** — one /24 IPv4 network and one /120 IPv6 network whose number is shared by the VLAN ID, the third octet, and the IPv6 address group.
- **Serial pinout (X1 and X2)** — the OpenGear per-port setting that matches the RJ45 wiring of a console cable; X2 is Cisco Straight (the default) and X1 is Cisco Rolled.
- **SRG mapping workbook** — the Excel workbook that holds the FortiSwitch crosswalk of SRG requirements to FortiSwitch settings, commands, documentation references, and verification status.
- **STIG crosswalk** — an alignment of one vendor's STIG rules with another platform's settings through the SRG requirement each rule implements, used where the second platform, such as FortiSwitch, has no STIG of its own.
- **vPC (virtual port channel)** — a Cisco Nexus feature that lets two switches present one port channel to a downstream device; FortiSwitch provides the same function with MCLAG.
- **"x" marker** — a workbook cell value meaning a feature was found in the documentation but has not yet been verified in the CLI or the GUI; a row counts as verified only when a CLI or GUI verifier is recorded.
