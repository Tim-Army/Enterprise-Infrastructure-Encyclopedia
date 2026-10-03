# Chapter 16: FortiGate 7.6 Operator Practice Exam and Self-Check

## Learning Objectives

- Map every FortiGate 7.6 Operator exam domain to the Volume XIX chapters
  that teach it, and identify your own weakest domains before sitting the
  assessment.
- Work through an original, answer-keyed practice bank that mirrors the
  operator assessment's style — single- and multi-select — and read the
  reasoning behind every answer.
- Use the interactive self-check companion in quiz and study modes to
  measure readiness offline in a browser.
- Run the operator-level GUI and CLI procedures end to end on a
  FortiGate-VM: console bring-up and status verification, dashboard
  review, interface/DHCP/route configuration, administrator accounts and
  profiles, log viewing and filtering, and firewall authentication.
- Translate a weak practice-exam domain into a concrete review plan
  against the earlier chapters of this volume.

## Theory and Architecture

The FortiGate 7.6 Operator credential is Fortinet's entry, operator-level
qualification. It targets the person who **operates an already-deployed
FortiGate** rather than the architect who designs one: navigating the GUI
and CLI, reading system status and logs, recognizing the Security
Fabric's components, and performing routine, low-risk configuration and
verification. It sits alongside the NSE 1–3 awareness and foundation
material and the operator-foundations content in
[Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md),
and it draws on the hands-on FortiOS administration built in
[Chapters 04–09](04-fortigate-first-deployment-licensing-management-and-hardening.md).

This is an **assessment and self-check chapter**. It introduces no new
subsystem; it consolidates Chapters 01–15 into exam-style practice, a
readiness tracker, and a set of operator hands-on labs. Every practice
item in this chapter is an **original question written for this
encyclopedia** — the items test the same operator concepts as the vendor
material without reproducing Fortinet's proprietary questions or
courseware, in line with [EDITORIAL_STANDARDS.md](../../../EDITORIAL_STANDARDS.md).

### Exam domain structure and chapter mapping

The operator assessment spans eight practical domains. Each maps directly
onto chapters already in this volume, so a weak practice result points
straight at the material to revisit.

| Domain | Operator emphasis | Volume XIX chapters |
|---|---|---|
| Security Fabric, FortiCloud, and FortiCare | Fabric roles, registration, cloud services | [03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md), [04](04-fortigate-first-deployment-licensing-management-and-hardening.md) |
| FortiGuard, threats, and IPS | Signature updates, threat categories, protocol decoders | [02](02-nse-2-threat-landscape-security-technologies-and-fortinet-portfolio.md), [07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) |
| Firewall policies and authentication | Policy match order, NAT, user/group policies | [06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |
| Web filtering and SSL inspection | FortiGuard category filters, certificate vs deep inspection | [07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) |
| High availability | FGCP cluster behavior and synchronized state | [05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) |
| Interfaces, routing, VLANs, VDOMs, and VPN | Addressing, static routes, segmentation, remote access | [05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md), [06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md) |
| Administration and maintenance | Admin accounts, profiles, backups, updates | [04](04-fortigate-first-deployment-licensing-management-and-hardening.md), [08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md) |
| FortiSwitch and FortiLink | Managed-switch discovery over the FortiLink tunnel | [03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md), [11](11-secure-networking-upper-levels-switching-wireless-and-management.md) |

### How this chapter's practice material is organized

The bank holds **216 original items** grouped into six practice sets that
follow the volume's operator arc — Access and Management; System Settings
and Basic Networking; Firewall Policies; Logging and Monitoring; Firewall
Authentication; and a mixed operator practice exam that samples every
domain. Items are single-answer unless the stem ends with *(Choose two.)*
or *(Choose three.)*. The **interactive companion** presents the same 216
items with immediate feedback (quiz mode) or free browsing (study mode);
the **offline bank** in this chapter carries every item with an answer
key and explanation for print and EPUB readers, who cannot run the
interactive page.

## Design Considerations

Treat readiness as per-domain, not a single blended percentage — the
operator assessment can fail a candidate who is strong on policies but
blind on FortiGuard, so the goal is *even* coverage across all eight
domains above.

### Sequencing your review

- Take the mixed operator practice set **cold**, before re-reading, to
  expose weak domains honestly.
- Feed each miss back through the domain-to-chapter map and redo the
  relevant chapter's hands-on lab, not just its prose.
- For a multi-select item, evaluate **each option independently** as a
  true/false claim; FortiOS scores these all-or-nothing, so a single
  wrong box fails the item.
- Re-take only the weak sets until every domain clears the threshold in
  *Validation and Troubleshooting*, rather than re-taking the whole bank.

### Choosing between the interactive self-check and the offline bank

Use the **interactive companion** for timed, answer-hidden self-testing
with per-section scoring; use the **offline bank** below (and its answer
key) for answer-keyed study, quick reference, and EPUB/print reading. The
two hold identical items, so a score in one transfers directly to the
other.

## Implementation and Automation

### Self-assessment tracker

Copy this table and score each domain 1–5 after a cold attempt. Anything
below 4 gets a chapter re-read and its lab redone before you re-test.

| Domain | Confidence (1–5) | Last score | Chapters to review |
|---|---|---|---|
| Security Fabric, FortiCloud, FortiCare | | | 03, 04 |
| FortiGuard, threats, IPS | | | 02, 07 |
| Firewall policies and authentication | | | 06 |
| Web filtering and SSL inspection | | | 07 |
| High availability | | | 05 |
| Interfaces, routing, VLANs, VDOMs, VPN | | | 05, 06 |
| Administration and maintenance | | | 04, 08 |
| FortiSwitch and FortiLink | | | 03, 11 |

### The interactive self-check companion

The [FortiGate 7.6 Operator interactive self-check](../../interactive/fortigate-operator-quiz.html)
is a single, self-contained HTML page that runs offline in any browser —
no server, no network. It offers a **quiz mode** (immediate right/wrong
feedback with the explanation and a per-section score at the end) and a
**study mode** (browse every item with its answer revealed). It carries
the same 216 items as the bank below, organized into the six practice
sets, and is the recommended way to rehearse under answer-hidden
conditions.

For the next level up, the
[FortiGate 7.6 Administrator (NSE 4) study quiz](../../interactive/fortigate-administrator-quiz.html)
works the same way and also runs offline. Its 987 questions cover the
16 lessons of Fortinet's free FortiGate 7.6 Administrator course, from
system and network settings through IPsec VPN, SD-WAN, high
availability, and FortiSASE. Each lesson has its own section, and each
explanation gives the time in the course video that the question was
written from.

### Practice question bank with answer key

The full bank follows, grouped by practice set. Each item shows the
question, its options, the correct answer, and a short explanation. Cover
the answer line to self-test, or use the interactive companion for a
cleaner answer-hidden experience.

#### Set 1 — Access and Management

**1.** How is a FortiGate appliance most accurately categorized within a network security architecture?

- A. A next-generation firewall (NGFW) that combines firewalling with deep traffic inspection and threat protection
- B. A purpose-built VPN concentrator that only terminates remote-access tunnels
- C. An endpoint detection and response (EDR) agent installed on user workstations
- D. A log-collection and SIEM appliance dedicated to storing and correlating events

**Answer:** A — FortiGate is a next-generation firewall (NGFW), delivering firewalling plus full traffic visibility and integrated threat protection in one platform. A VPN concentrator, an EDR agent, and a SIEM each cover only one narrow function that FortiGate can incorporate but is not limited to.

**2.** Within the layered FortiGate platform, which component supplies threat intelligence and centralized management services from above the security features?

- A. FortiGuard Subscription Services
- B. FortiOS, the base operating system
- C. The Security Processing Units (SPUs) that accelerate traffic
- D. The FortiClient endpoint agent

**Answer:** A — FortiGuard Subscription Services sit on top of the stack and provide threat intelligence and centralized management. FortiOS is the operating system layer and SPUs are the acceleration hardware; neither delivers the subscription threat-intelligence feeds, and FortiClient is a separate endpoint product.

**3.** A cloud team is evaluating the virtual FortiGate-VM edition. What does this form factor provide compared with the hardware appliances?

- A. Identical protection to the physical appliances, suitable for both public and private cloud deployments
- B. A trimmed-down build that can only perform logging and monitoring
- C. Management functions only, with no ability to inspect traffic
- D. Coverage restricted to on-premises data centers alone

**Answer:** A — FortiGate-VM delivers the same protection as the physical appliances and fits into public or private cloud environments. It is a full-featured firewall, not a logging-only, management-only, or on-prem-only build.

**4.** A hosting provider must carve a single physical FortiGate into several independent virtual firewalls, each with separate policies, interfaces, routing tables, and administrator accounts. Which FortiGate capability delivers this?

- A. SD-WAN link steering
- B. Virtual Domains (VDOMs)
- C. Automation stitches
- D. Security Processing Units (SPUs)

**Answer:** B — Virtual Domains (VDOMs) partition one FortiGate into multiple virtual firewalls, each with its own policies, interfaces, routing tables, and admins, which is ideal for multi-tenant service providers. SD-WAN steers WAN traffic, automation stitches trigger event-driven actions, and SPUs are acceleration chips, none of which provide tenant separation.

**5.** A retail chain runs multiple broadband and LTE internet links per site and wants to spread traffic across all of them and steer flows dynamically to cut costs without leasing dedicated MPLS circuits. Which FortiGate feature meets this goal?

- A. Virtual Domains (VDOMs)
- B. SD-WAN
- C. Automation stitches
- D. Web filtering

**Answer:** B — SD-WAN uses several internet links efficiently, load-balances across the available connections, and routes dynamically to lower costs without expensive dedicated circuits. VDOMs partition the device, automation stitches react to events, and web filtering controls URL access, so none of them handle multi-link WAN steering.

**6.** Two VDOMs, TENANT-A and TENANT-B, are configured on the same FortiGate with no additional inter-VDOM setup. By default, how does traffic pass between them?

- A. It cannot flow from one VDOM to the other unless inter-VDOM routes are explicitly configured
- B. Both VDOMs automatically share a single common routing table
- C. Traffic passes freely between the VDOMs with no extra configuration
- D. The two VDOMs can only exchange traffic through the Security Fabric

**Answer:** A — By default VDOMs are isolated, so traffic cannot move between TENANT-A and TENANT-B unless inter-VDOM links or routes are added. VDOMs do not share one routing table and are not open to each other by default, and Security Fabric membership is not required for inter-VDOM connectivity.

**7.** Which scenario is a genuine example of what a FortiGate automation stitch does?

- A. Dividing the appliance into isolated per-tenant environments for a hosting provider
- B. Choosing the best-performing WAN path for each application in real time
- C. Automatically quarantining a compromised host, or calling an AWS Lambda function when a defined event is logged
- D. Pushing the newest antivirus signatures out to managed endpoint agents

**Answer:** C — An automation stitch links a trigger to an action, such as quarantining an infected host or invoking an AWS Lambda script when a specific event is logged. Tenant isolation is a VDOM function, per-application path selection is SD-WAN, and signature distribution is a FortiGuard/endpoint task.

**8.** Through which mechanism does a FortiGate keep pace with the evolving threat landscape by receiving regular threat updates?

- A. The Fortinet Security Fabric integration layer
- B. FortiGuard Security Services, powered by FortiGuard Labs
- C. Automation stitches
- D. Virtual Domains (VDOMs)

**Answer:** B — FortiGate receives its threat updates from FortiGuard Security Services, powered by FortiGuard Labs, Fortinet's threat-intelligence and research group. The Security Fabric ties products together, automation stitches trigger actions, and VDOMs partition the device, so none of those deliver the update feeds.

**9.** FortiGuard Labs delivers real-time threat intelligence across the Security Fabric grouped into three main areas. Which item below is one of those areas?

- A. Software-defined WAN path selection
- B. Trusted machine learning (ML) and artificial intelligence (AI) that block unknown threats sooner
- C. Management of routing between VDOMs
- D. Certificate-based authentication of administrators

**Answer:** B — One of FortiGuard Labs' three pillars is trusted ML and AI that stop previously unknown threats faster, alongside real-time protection and threat hunting/outbreak alerts. SD-WAN path selection, inter-VDOM routing, and admin certificate authentication are unrelated FortiGate features.

**10.** Which of the following statements about FortiGate is NOT true?

- A. It participates in the Fortinet Security Fabric
- B. It receives security updates from FortiGuard Labs
- C. It can only authenticate administrators against a remote server
- D. It inspects both inbound and outbound traffic for threats

**Answer:** C — The false statement is that FortiGate only supports remote authentication; it also supports local administrator accounts stored on the device itself. Security Fabric membership, FortiGuard updates, and bidirectional traffic inspection are all accurate.

**11.** Which management method is intended as the main way to perform everyday administration on a FortiGate using an ordinary web browser?

- A. The graphical user interface (GUI) reached over HTTPS
- B. The command line interface (CLI) reached over SSH
- C. A directly attached console cable session
- D. The CLI console embedded in the web interface

**Answer:** A — The GUI, opened in any standard web browser over HTTPS, is the primary tool for most day-to-day tasks. The SSH CLI, console cable, and embedded CLI console are mainly used for advanced configuration and troubleshooting rather than routine administration.

**12.** There are three supported ways to reach the FortiGate CLI. Which option below is NOT one of them?

- A. A direct console cable connection
- B. HTTPS opened in a standard web browser
- C. SSH across the network
- D. The CLI console built into the GUI

**Answer:** B — HTTPS in a web browser opens the GUI, not the CLI, so it is not a CLI access method. The three valid CLI paths are a console cable, an SSH session over the network, and the CLI console embedded in the web interface.

**13.** What sets a console cable apart from the other ways of reaching the FortiGate CLI?

- A. It provides encrypted CLI access over the WAN
- B. It is a direct physical connection that works even with no network available
- C. It places a CLI panel inside the web-based GUI
- D. It relies on HTTPS through a standard web browser

**Answer:** B — A console cable is a direct connection that functions with no network at all, making it valuable when the device is unreachable over IP. SSH provides encrypted network access, the built-in console lives inside the GUI, and HTTPS is the GUI transport, none of which work without a network.

**14.** After signing in to the FortiGate web interface, how do you launch the CLI console that is built into the GUI?

- A. Go to System > Advanced and turn on the console daemon
- B. Click the CLI console icon in the upper-right corner to open a new console window
- C. Right-click the dashboard and choose 'Open CLI'
- D. Start an SSH session to TCP port 22 from inside the browser tab

**Answer:** B — Once logged in to the GUI, clicking the CLI console icon in the upper-right corner opens a new console window for direct command entry. There is no console-daemon toggle under System > Advanced, no dashboard right-click option, and the browser does not initiate an SSH session for this feature.

**15.** Current FortiOS releases require the administrator password set at first login to meet a complexity rule. What must that password satisfy?

- A. A minimum of 8 characters that include at least one digit
- B. A minimum of 10 characters with no character repeated
- C. A minimum of 12 characters containing at least one uppercase letter, one lowercase letter, one number, and one special character
- D. A minimum of 16 characters using only letters and digits

**Answer:** C — The complex-password requirement is at least 12 characters with at least one uppercase letter, one lowercase letter, one number, and one special character. The other choices use the wrong minimum length or omit the four required character classes.

**16.** On a FortiGate at factory defaults, what is the default management IP address and which interface carries it?

- A. 192.168.1.99/24, on port1 for smaller models or on a dedicated MGMT interface on larger models
- B. 192.168.1.1/24, always on the WAN1 interface
- C. 192.168.0.1/24, on port1 across every hardware model
- D. 10.0.0.1/24, only on the dedicated MGMT interface

**Answer:** A — The factory default management address is 192.168.1.99 with a /24 mask, assigned to port1 on smaller units and to a dedicated MGMT interface on larger units. The other options use incorrect addresses or misstate the interface placement.

**17.** When a FortiGate runs as a virtual machine, what governs its management IP address?

- A. It is permanently fixed at 192.168.1.99/24, exactly like hardware models
- B. The FortiGuard subscription license entitlement
- C. The network settings of the underlying virtual platform
- D. The hardware defaults of the MGMT interface

**Answer:** C — On a FortiGate-VM the management IP is determined by the virtual platform's network configuration, not a fixed hardware default. VMs have no built-in MGMT-port hardware default, and the FortiGuard license does not assign IP addressing.

**18.** When you open the GUI of a factory-default FortiGate for the very first time, which credentials do you use, and what happens right after you log in successfully?

- A. Username admin with the password 'admin'; the device drops you straight onto the dashboard
- B. Username root with a blank password; the device emails you a temporary password
- C. Username admin with an empty (blank) password; the device then prompts you to set a new password
- D. Username fortinet with the password 'fortinet'; the device forces a firmware upgrade first

**Answer:** C — You sign in as admin with the password field left blank, and FortiGate immediately requires you to create a new password. There is no default 'admin' or 'fortinet' password, no root account with emailed credentials, and no forced firmware upgrade at first login.

**19.** By default, how is web-based administrative access provided on FortiGate hardware and FortiGate-VMs, and how does a VM usually obtain its management IP?

- A. Web management is off by default and must be enabled from the console on every model
- B. Web management is available only on the dedicated MGMT interface and never on port1
- C. Web management is enabled on port1 by default, and a VM typically receives its IP automatically through DHCP
- D. A VM has no default IP, so a static address must always be assigned before the first connection

**Answer:** C — Administrative web access is enabled on port1 by default on FortiGate hardware and VMs alike, and a VM usually picks up its IP automatically via DHCP from the virtual environment. Web management is not disabled by default, is not limited to a MGMT-only interface, and a VM does not always require a manual static address.

**20.** Which IP address is the factory default management address of a FortiGate?

- A. 192.168.0.1
- B. 192.168.1.99
- C. 10.0.0.1
- D. 172.16.1.1

**Answer:** B — 192.168.1.99 is the FortiGate factory default management IP used to reach the GUI or CLI on first-time access. The other addresses are not the FortiGate default.

**21.** An engineer patches both their laptop and a factory-default FortiGate into access ports on the same VLAN of a switch instead of cabling directly to port1. To open the default GUI at `https://192.168.1.99`, how should the laptop's IP be set?

- A. Any address handed out automatically by the FortiGate's DHCP server on that VLAN
- B. The identical address 192.168.1.99 with mask 255.255.255.255
- C. An address in the same subnet, for example 192.168.1.100 with mask 255.255.255.0
- D. An address inside 10.0.0.0/8 so it will not clash with the FortiGate

**Answer:** C — The laptop needs an address in the same 192.168.1.0/24 subnet, such as 192.168.1.100 with a 255.255.255.0 mask, to reach 192.168.1.99. Using the same host address would collide, a /32 mask leaves no reachable peers, a different subnet cannot reach it directly, and the default port1 DHCP scope should not be relied on for management access here.

**22.** From the console of a FortiGate-VM you set port1 to 192.168.1.99/24 and now need to permit GUI access. After entering 'config system interface' and 'edit port1', which command allows HTTPS management on the interface?

- A. set admin-access https
- B. set management https
- C. set allowaccess https
- D. set service https-server

**Answer:** C — Within the interface context, 'set allowaccess https' enables HTTPS administrative access on port1, typically paired with 'set ip 192.168.1.99 255.255.255.0'. The other command forms are not valid FortiOS interface syntax for permitting management protocols.

**23.** The first step of the Setup Wizard registers the FortiGate with FortiCare. Why does this step matter?

- A. It unlocks full access to Fortinet Customer Service and Support and to FortiGuard services, confirming the device is licensed and tied into the security update network
- B. It sets the administrator password and applies the password policy to all later logins
- C. It automatically pulls down and installs the newest firmware patch on the device
- D. It rewrites the running configuration into a format compatible with older FortiOS releases

**Answer:** A — Registering with FortiCare grants full access to Fortinet support and FortiGuard services and verifies the device is licensed and connected to the update network. Setting passwords, installing firmware, and converting configurations are separate functions handled elsewhere.

**24.** In the Setup Wizard, what does the Migrate Config with FortiConverter step accomplish?

- A. It imports a configuration from another vendor's device by automatically mapping it into FortiOS format
- B. It downloads and installs the latest FortiOS firmware patch on its own
- C. It changes the FortiGate dashboard layout to match a different appliance
- D. It backs up the current configuration to FortiCloud ahead of an upgrade

**Answer:** A — FortiConverter migrates a configuration from another device and automatically maps it to the FortiOS format, which is helpful when replacing an existing firewall. It does not install firmware, restyle the dashboard, or perform a FortiCloud backup.

**25.** Which statement correctly describes how the FortiGate Setup Wizard behaves when you do not finish every step?

- A. Every step is mandatory and the wizard cannot be closed until all steps are done
- B. Any step you skip is permanently deleted and can never be reopened
- C. The wizard appears only once and never returns no matter which steps you skip
- D. You may leave steps incomplete, but the wizard prompts you again at your next login, with the already-completed steps shown grayed out

**Answer:** D — Completing every step is optional; the wizard reappears at the next login and displays the steps you already finished as grayed out. It is not strictly mandatory, skipped steps are not deleted, and it does not disappear permanently after one run.

**26.** What benefit does enabling automatic patch upgrades in the Setup Wizard provide?

- A. It stops the FortiOS familiarization video from playing at future logins
- B. It automatically migrates configurations from legacy firewalls into FortiOS format
- C. It lets you choose a prebuilt dashboard matched to your monitoring priorities
- D. FortiOS stays consistently up to date without any manual intervention

**Answer:** D — Automatic patch upgrades keep FortiOS consistently current with no manual effort, replacing the need to apply patches by hand. Suppressing an intro video, migrating legacy configurations, and selecting a dashboard are unrelated to this setting.

**27.** You launch a terminal emulator such as PuTTY to reach a FortiGate over its console port. Which serial parameters should you configure?

- A. 115200 baud, 8 data bits, even parity, 1 stop bit, hardware flow control
- B. 19200 baud, 7 data bits, odd parity, 2 stop bits, no flow control
- C. 9600 baud, 8 data bits, no parity, 1 stop bit, no flow control
- D. 9600 baud, 7 data bits, no parity, 2 stop bits, software flow control

**Answer:** C — The FortiGate console uses 9600 baud, 8 data bits, no parity, 1 stop bit, and no flow control (commonly written 9600 8N1). The other combinations use the wrong baud rate, data-bit, parity, stop-bit, or flow-control values and will not connect properly.

**28.** A technician at Northwind Logistics is racking a new FortiGate-100F and needs guaranteed CLI access before any IP addressing exists. Which cable connects a laptop directly to the appliance's console port, and why is this the go-to method for an out-of-the-box setup?

- A. A straight-through Ethernet patch cable running from the laptop NIC to a data port on the FortiGate
- B. A crossover Ethernet cable joining the laptop to the FortiGate's dedicated management port
- C. A rollover (console) cable from the laptop's serial or USB port to the FortiGate console port, because it works even when no network configuration is present
- D. A USB-to-Ethernet dongle plugged into the FortiGate's HA heartbeat port

**Answer:** C — A rollover (console) cable from the laptop's serial/USB port to the console port gives direct terminal access that is independent of any network or IP configuration, making it the most reliable path for first-time setup or recovery. Ethernet-based options all depend on working network settings that may not yet exist.

**29.** An engineer powers on a factory-fresh FortiGate for the first time and reaches the console login prompt. What does she enter, and what happens immediately afterward?

- A. She types admin with the password 'fortinet' and lands directly at the CLI prompt
- B. She types root with an empty password and is asked to accept the license agreement
- C. She types admin and uses the chassis serial number as the password
- D. She types admin and leaves the password field empty, after which FortiOS immediately requires her to define a new password

**Answer:** D — By default no password is set on the admin account, so the first login uses admin with a blank password; FortiOS then forces the administrator to create a new password before continuing. There is no factory 'fortinet' password and the serial number is not used for login.

**30.** An administrator launches an SSH client to reach the FortiGate CLI over the network. Which TCP port does the client target, and on which interface is SSH admin access turned on out of the box?

- A. TCP 23 on port1, and only on physical appliances
- B. TCP 443 on any interface as soon as HTTPS admin access is switched on
- C. TCP 22 on the mgmt interface only, and it is off by default on virtual machines
- D. TCP 22 on port1, which is enabled by default on both hardware FortiGates and FortiGate VMs

**Answer:** D — SSH uses TCP port 22, and FortiOS enables SSH administrative access on port1 by default on both appliances and VMs. Port 23 is Telnet and port 443 is HTTPS, so those choices name the wrong service.

**31.** A consultant wants to SSH into an untouched, factory-default FortiGate for the first time, but his workstation sits on a different subnet than the firewall. What condition must hold for that initial connection, and what must be done to reach the device from a remote network?

- A. Any subnet is fine as long as SSH is enabled, and nothing further is required
- B. The workstation must pull its address from FortiGate's DHCP, and remote access requires enabling Telnet
- C. Initial SSH is impossible until a license is applied, so the console port must be used first
- D. For the initial connection the workstation must share the same subnet as FortiGate, and reaching it from a remote network first requires configuring routing on FortiGate

**Answer:** D — Out of the box FortiGate has no route to foreign networks, so initial SSH access requires the client to be on the same subnet; to connect from a remote network you must first add the necessary routing on FortiGate. Telnet is unrelated and no license is needed to use SSH.

**32.** Right after the first login to a new FortiGate, which of the following is a recommended initial-setup best practice?

- A. Turn off the GUI's built-in CLI console widget
- B. Set or confirm the system clock, ideally by pointing it at an NTP source
- C. Remove the default admin account before any other account exists
- D. Move all management traffic off HTTPS and onto Telnet

**Answer:** B — Accurate time underpins log correlation and security analysis, so configuring or verifying the system time (via NTP or manual entry) is a listed best practice. Deleting the sole admin account or switching to Telnet would harm manageability and security, not improve it.

**33.** Which action is a recognized best practice for hardening administrative access to a FortiGate?

- A. Publish the management GUI to the public internet
- B. Define trusted hosts for administrator accounts
- C. Prefer Telnet over SSH for CLI sessions
- D. Keep the factory default administrator password

**Answer:** B — Configuring trusted hosts limits where administrators can log in from and is a core hardening step. Exposing the GUI to the internet, using cleartext Telnet, or keeping the default password all increase risk rather than reduce it.

**34.** Best practice says to manage a FortiGate only over encrypted protocols. Which pairing satisfies that guidance?

- A. HTTP and Telnet
- B. HTTPS and SSH
- C. HTTP and SSH
- D. FTP and Telnet

**Answer:** B — HTTPS and SSH are both encrypted, protecting administrative credentials and session data in transit. HTTP, Telnet, and FTP send data in cleartext, so any pairing that includes them is insecure.

**35.** What is the security benefit of assigning trusted hosts to a FortiGate administrator account?

- A. It caps how many administrators can be logged in at the same time
- B. It requires a password change at the administrator's first login
- C. It turns on two-factor authentication for every administrator automatically
- D. It confines that administrator's logins to specific IP addresses or subnets

**Answer:** D — Trusted hosts restrict where an administrator may authenticate from, so even stolen credentials are useless outside the approved IP addresses or networks. It does not manage session counts, force password changes, or enable two-factor authentication.

**36.** Among the initial-access best practices, which control strengthens login security by demanding a second proof of identity in addition to the password?

- A. Defining trusted hosts
- B. Renaming the device from its default hostname
- C. Enabling two-factor authentication
- D. Setting or verifying the system time

**Answer:** C — Two-factor authentication layers a second verification step on top of the password, so a compromised password alone is not enough to log in. Trusted hosts, hostname changes, and time settings improve other aspects but do not add a second authentication factor.

**37.** On the FortiGate Status dashboard, which widget shows the hostname, serial number, running firmware version, operation mode, and uptime together in one place?

- A. System Information
- B. Licenses
- C. Virtual Machine
- D. Administrators

**Answer:** A — The System Information widget consolidates hostname, serial number, firmware version, operating mode, system time, and uptime. The Licenses widget covers subscription status, Virtual Machine covers vCPU/RAM allocation, and Administrators lists logged-in admins.

**38.** The dashboard's Administrators widget can show admins connected by Console, FortiExplorer, or HTTPS. When you are managing the FortiGate through its web GUI in a browser, which of these entries represents your session?

- A. Console
- B. FortiExplorer
- C. SSH
- D. HTTPS

**Answer:** D — The web GUI is served over HTTPS, so a browser-based admin session appears as HTTPS in the Administrators widget. Console and FortiExplorer are different access channels, and SSH is a CLI method rather than a GUI session.

**39.** An administrator logs in to a freshly deployed FortiGate and the browser flags an 'Untrusted HTTPS server certificate'. What produces this warning?

- A. The FortiGuard AntiVirus and IPS subscriptions have lapsed
- B. The administrator mistyped the login password
- C. FortiGate Cloud has not been activated yet
- D. The FortiGate is presenting its built-in self-signed certificate for HTTPS management, which the browser has no reason to trust

**Answer:** D — By default GUI access is secured with a self-signed certificate that is not issued by a trusted certificate authority, so browsers show an untrusted-certificate warning until a CA-signed certificate is imported. Expired FortiGuard licenses, wrong passwords, and cloud activation have nothing to do with the TLS certificate chain.

**40.** Watching a FortiGate VM boot on the console, you see it load flatkc and rootfs.gz and then print 'System is starting...'. What device-identifying value does FortiOS display next, before the login prompt?

- A. The appliance serial number
- B. The MAC address of port1
- C. The DHCP-assigned management IP address
- D. The FortiCare registration key

**Answer:** A — Immediately after 'System is starting...' the console prints the VM's serial number (for example FGVMEV...), identifying the unit before login. The MAC address, DHCP-learned IP, and FortiCare key are not shown at this point in the boot sequence.

**41.** You reach the console login prompt of a brand-new, factory-default FortiGate VM using the built-in administrator account. What credentials do you supply, and what does FortiOS insist on before it gives you the CLI prompt?

- A. Username 'admin' with password 'admin', and no password change is needed
- B. Username 'root' with the serial number as the password, after which you set the hostname
- C. Username 'fortinet' with password 'fortinet', after which you accept the EULA
- D. Username 'admin' with an empty password, after which you are forced to enter and confirm a new password before the CLI prompt appears

**Answer:** D — The default admin account has no password, so you log in as admin with a blank password; FortiOS then requires you to set and confirm a new password before dropping to the CLI. There is no 'admin'/'admin' or 'fortinet'/'fortinet' factory credential.

**42.** On a factory-default FortiGate VM, 'show system interface' displays port1 with 'set mode dhcp'. Based on its 'set allowaccess' line, which administrative-access protocols are permitted on port1 by default?

- A. HTTPS and SSH only
- B. PING, HTTPS, SSH, SNMP, and FMG-Access
- C. HTTP, Telnet, and PING
- D. PING, HTTPS, SSH, and HTTP

**Answer:** D — The default port1 configuration reads 'set allowaccess ping https ssh http', so those four protocols are allowed. SNMP, FMG-Access, and Telnet are not part of the default allowaccess set, and the list is broader than HTTPS/SSH alone.

**43.** From the FortiGate CLI you need to confirm the actual IP address that port1 obtained from DHCP, listed per interface at the device level. Which command reveals this (showing, for instance, port1 at 192.168.100.137)?

- A. diagnose ip address list
- B. show system interface
- C. get router info routing-table all
- D. diagnose ip route list

**Answer:** A — 'diagnose ip address list' prints the live IP currently bound to each interface, including the DHCP-assigned address on port1. 'show system interface' only displays the saved configuration (such as 'mode dhcp'), not the address actually leased, and the routing-table commands show routes rather than interface addresses.

#### Set 2 — System Settings and Basic Networking

**44.** FortiGate ships with a built-in administrator account that attackers frequently probe. What is its name and privilege level?

- A. An account called "admin" that holds full read/write configuration rights on the device
- B. An account called "root" that is limited to read-only monitoring
- C. An account called "super-admin" that must be enabled before it can be used
- D. An account called "audit-admin" whose rights are restricted to viewing logs

**Answer:** A — The factory default account is named admin and has full configuration privileges, which is exactly why it is a well-known target. FortiGate does not ship with root, super-admin, or audit-admin as the default administrator.

**45.** Why is creating individual administrator accounts preferable to having everyone share the default admin login?

- A. It automatically re-encrypts all admin passwords with a stronger hashing algorithm
- B. It provides accountability by tying each configuration change to a specific user
- C. It disables the default admin account as soon as a second account is created
- D. It doubles the number of simultaneous GUI sessions the device permits

**Answer:** B — Separate accounts make each administrator identifiable, so configuration changes can be traced to the person who made them, in addition to enabling role-based least privilege. They do not alter password hashing, auto-disable the default account, or change session limits.

**46.** When you add a new administrator account, FortiOS requires you to indicate where the account credentials will reside. Which two storage locations are offered?

- A. In flash or in RAM
- B. On the primary HA member or the secondary HA member
- C. Locally on the FortiGate or remotely on an external server
- D. In the global database or within a specific VDOM database

**Answer:** C — An administrator account can be stored locally on the FortiGate or remotely, where authentication is delegated to an external server group. Flash/RAM, HA member selection, and global/VDOM database are not the credential-storage choice presented during account creation.

**47.** Which FortiGate GUI menu path leads to the page where new administrator accounts are created?

- A. System > Administrator > Admins Profiles
- B. User & Authentication > User Definition
- C. System > Administrator > Firmware & Registration
- D. System > Administrator > Administrators

**Answer:** D — Administrator accounts are created under System > Administrator > Administrators. Admin Profiles defines permission sets, Firmware & Registration handles licensing, and User Definition creates end-user (non-administrator) accounts.

**48.** No matter what other options you enable on an administrator account, which setting is mandatory for every account?

- A. An administrator profile
- B. Two-factor authentication
- C. A trusted-hosts restriction
- D. A guest-account provisioning limit

**Answer:** A — Every administrator account must be assigned an administrator profile because the profile defines the permissions that account will have. Two-factor authentication, trusted hosts, and guest provisioning are optional add-ons.

**49.** For each configuration area covered by an administrator profile, which set of access levels can you assign?

- A. Read-write access or no access, and nothing in between
- B. Read-only access, read-write access, or no access
- C. Full access or restricted access only
- D. Allow or deny only

**Answer:** B — Each section in a profile can be set to None, Read (read-only), or Read/Write, giving three access levels per area. The other options omit the read-only tier that FortiOS provides.

**50.** On the New Administrator form, which Type selection sets the account to authenticate through a public key infrastructure (PKI) group?

- A. REST API admin
- B. SSO Admin
- C. Use public key infrastructure (PKI) group
- D. Restrict login to trusted hosts

**Answer:** C — The 'Use public key infrastructure (PKI) group' Type binds the account to certificate-based PKI authentication. REST API admin and SSO Admin are separate account types, and 'Restrict login to trusted hosts' is a toggle rather than a Type value.

**51.** Which FortiGate interface setting specifies the protocols permitted to manage the device through that interface, such as HTTPS, PING, and SSH?

- A. Alias
- B. IP address
- C. DHCP server
- D. Administrative access

**Answer:** D — Administrative access defines the management protocols allowed on the interface, such as HTTPS, PING, and SSH. Alias is just a friendly label, IP address is the interface's reachable address, and a DHCP server hands out addresses to clients.

**52.** VLAN frames carry a VLAN ID tag so switches can tell which VLAN they belong to. Which tagging standard is identified as the most widely used?

- A. 802.1Q
- B. 802.1X
- C. ISL
- D. 802.3ad

**Answer:** A — IEEE 802.1Q is the dominant, vendor-neutral VLAN tagging standard. 802.1X is port-based network access control, ISL is Cisco's legacy proprietary encapsulation, and 802.3ad is link aggregation.

**53.** When a FortiGate operating in NAT mode uses VLANs, how are those VLANs represented in its configuration?

- A. As a Layer 2 bridge inserted between two VLAN trunks
- B. As subinterfaces bound to physical ports, each tied to a particular VLAN ID
- C. As a virtual VLAN switch that bridges several physical ports together
- D. As individual dedicated physical ports, one for each VLAN

**Answer:** B — In NAT (Layer 3) mode, VLANs are created as subinterfaces on a physical port, each mapped to a specific VLAN ID, so one physical link can carry many tagged VLANs. A Layer 2 bridge describes transparent mode, not NAT-mode VLANs.

**54.** A FortiGate running in transparent mode behaves as a Layer 2 bridge yet still enforces several security features on VLAN-tagged traffic. Which capability is NOT available in transparent mode?

- A. Antivirus scanning
- B. Web filtering
- C. DHCP server
- D. Intrusion prevention

**Answer:** C — Transparent mode still applies antivirus, web filtering, and IPS to bridged traffic, but it does not provide DHCP server (or SSL VPN and full NAT) services. Those depend on the Layer 3 functionality that transparent mode does not offer.

**55.** A network engineer at Acme Corp is deciding how to deploy VLANs on a FortiGate. Which set correctly names the three ways a FortiGate can work with VLANs, depending on how the device is deployed?

- A. NAT mode, proxy mode, and sniffer mode
- B. Router mode, switch mode, and bridge mode
- C. Transparent mode, HA mode, and SSL VPN mode
- D. NAT mode, transparent mode, and a virtual VLAN switch on supported hardware

**Answer:** D — FortiGate supports VLANs three ways: routed VLAN interfaces in NAT mode, tagged bridging in transparent mode, and a hardware-based virtual VLAN switch on supported models. Proxy/HA/SSL-VPN are separate features, not VLAN deployment methods.

**56.** A FortiGate is deployed in NAT mode with several VLAN sub-interfaces created on port2. How does it move traffic from one VLAN to another?

- A. It behaves as a Layer 3 device and routes packets between the VLAN interfaces
- B. It behaves as a Layer 2 bridge, forwarding frames without any routing decision
- C. It behaves strictly as a managed Layer 2 switch
- D. It drops all inter-VLAN traffic by default and is unable to route it

**Answer:** A — In NAT mode each VLAN interface is a Layer 3 interface, so FortiGate routes between VLANs (and out to external networks). Layer 2 bridging without routing describes transparent mode instead.

**57.** On a FortiGate model that supports it, what capability does configuring a virtual VLAN switch provide?

- A. It routes between VLANs by wrapping each VLAN inside its own SSL VPN tunnel
- B. It lets the built-in hardware ports behave as a managed Layer 2 switch, with each port assigned to a VLAN or set as a trunk
- C. It permanently removes VLAN tags from every frame before any inspection takes place
- D. It copies one DHCP scope automatically to every VLAN on the device

**Answer:** B — A virtual VLAN switch turns the physical switch ports into a managed Layer 2 switch, letting you place ports in specific VLANs or make them trunks - handy for HA or extending VLANs across devices. It neither tunnels VLANs in SSL VPN nor strips tags.

**58.** 802.1Q is the tagging protocol most administrators pick for VLANs. What is its maximum VLAN count, and what would push you to use 802.1ad instead?

- A. Up to 1024 VLANs; use 802.1ad only when the FortiGate runs in transparent mode
- B. Up to 256 VLANs; use 802.1ad only on IPv6-only segments
- C. Up to 4094 VLANs; use 802.1ad when a larger design needs greater scalability
- D. Up to 65535 VLANs; use 802.1ad to cut down the number of usable VLANs

**Answer:** C — 802.1Q supports up to 4094 VLANs, which covers most networks; 802.1ad (Q-in-Q) stacks tags for larger, more scalable designs. The other VLAN counts are incorrect.

**59.** You want to add a new tagged VLAN sub-interface using the FortiGate web GUI. Which navigation path starts that task correctly?

- A. System > Settings > Create New, then set Type to VLAN
- B. Policy & Objects > Addresses > Create New, then choose VLAN
- C. Network > SD-WAN > Create New, then choose Interface
- D. Network > Interfaces > Create New, choose Interface, and set Type to VLAN

**Answer:** D — VLAN sub-interfaces are created under Network > Interfaces with Create New, selecting Interface and setting the Type to VLAN. The System, Addresses, and SD-WAN paths do not create VLAN interfaces.

**60.** An administrator builds a VLAN sub-interface named HR-VLAN on the New Interface form. A VLAN interface must specify both a VLAN ID and the physical port it rides on. In the sample shown, which VLAN ID and parent interface pairing is used?

- A. VLAN ID 100 bound to physical interface port7
- B. VLAN ID 10 bound to physical interface port1
- C. VLAN ID 254 bound to physical interface wan1
- D. VLAN ID 24 bound to physical interface dmz

**Answer:** A — The HR-VLAN example uses VLAN ID 100 on parent interface port7. A VLAN sub-interface always needs a VLAN ID plus the underlying physical interface it is associated with.

**61.** An administrator wants port5 to display the readable label LAN-HQ in lists and policies while its underlying system identifier port5 stays the same. Which field on the Edit Interface page is used for that label?

- A. Name
- B. Alias
- C. Role
- D. VRF ID

**Answer:** B — The Alias field holds a friendly display label such as LAN-HQ without changing the interface's fixed system name (port5). Name is that fixed identifier, while Role and VRF ID control other behavior.

**62.** While editing port5 on a FortiGate, an administrator opens the Role drop-down. Which four choices does that list contain?

- A. LAN, WAN, DMZ, Management
- B. Internal, External, DMZ, Undefined
- C. LAN, WAN, DMZ, Undefined
- D. LAN, WAN, VLAN, Undefined

**Answer:** C — The interface Role drop-down offers LAN, WAN, DMZ, and Undefined. Management, Internal/External, and VLAN are not selectable roles.

**63.** In the Address section when editing port5, which list correctly names the addressing modes a FortiGate offers for the interface?

- A. Manual, Static, DHCP, BOOTP, Sniffer
- B. Automatic, IPAM, DHCP, PPPoE, Bridge
- C. Manual, DHCP, PPPoE, LAN, DMZ
- D. Manual, IPAM, DHCP, PPPoE, One-Arm Sniffer

**Answer:** D — The Addressing mode selector provides Manual, IPAM, DHCP, PPPoE, and One-Arm Sniffer. Static/BOOTP/Bridge are not offered, and LAN/DMZ are interface roles rather than addressing modes.

**64.** An administrator sets port5 to Manual addressing with IP/Netmask 172.16.10.1/24 and leaves 'Create address object matching subnet' enabled. What value appears in the Subnet/Destination field of the automatically created 'port5 address' object?

- A. 172.16.10.0/24
- B. 172.16.10.1/24
- C. 172.16.10.1/32
- D. 0.0.0.0/0

**Answer:** A — The auto-generated address object matches the subnet, so 172.16.10.1/24 yields the network 172.16.10.0/24, not the single host address. A /32 or 0.0.0.0/0 would not represent that interface subnet.

**65.** When editing port5, which item is a valid selection in the Administrative Access (IPv4) section?

- A. One-Arm Sniffer
- B. FMG-Access
- C. PPPoE
- D. DMZ

**Answer:** B — Administrative Access (IPv4) lists management protocols such as HTTPS, PING, SSH, SNMP, FTM, and FMG-Access. One-Arm Sniffer and PPPoE are addressing modes, and DMZ is an interface role.

**66.** After finishing the Administrative Access setup on port5, HTTPS was left on and two more protocols were added. Which three IPv4 management protocols end up enabled on the interface?

- A. HTTPS, SSH, and SNMP
- B. HTTPS, PING, and FMG-Access
- C. HTTPS, SSH, and PING
- D. HTTP, TELNET, and PING

**Answer:** C — HTTPS was already enabled and PING and SSH were added, leaving HTTPS, SSH, and PING active. HTTP and TELNET are cleartext and would not be the secure choices enabled here.

**67.** On the Network > Interfaces list, port3 shows PING, HTTPS, SSH, HTTP, and TELNET enabled for administrative access, and the GUI highlights two of them in red as a warning. Which two are highlighted?

- A. HTTPS and SSH
- B. PING and HTTPS
- C. SSH and SNMP
- D. HTTP and TELNET

**Answer:** D — HTTP and TELNET are unencrypted management protocols, so the interface list flags them in red as insecure. PING, HTTPS, and SSH are shown normally.

**68.** On the Local-FortiGate, an administrator edits port6, which is cabled to the ISP link. Which Role should be chosen from the drop-down for that interface?

- A. WAN
- B. LAN
- C. DMZ
- D. Undefined

**Answer:** A — An interface facing the ISP/Internet is given the WAN role. LAN is for internal segments, DMZ for public-facing servers, and Undefined applies no role hint.

**69.** An administrator needs to type the fixed IP/Netmask 172.16.20.1/30 directly onto port6. Which addressing mode allows entering that static address by hand?

- A. DHCP
- B. Manual
- C. PPPoE
- D. IPAM

**Answer:** B — Manual addressing lets you enter a fixed IP/netmask such as 172.16.20.1/30 directly. DHCP and PPPoE learn addressing dynamically, and IPAM allocates from a managed pool rather than a hand-typed value.

**70.** While editing port6, an administrator wants to record the note "WAN port connected to ISP" on the interface. Which field on the Edit Interface page holds that descriptive text?

- A. Alias
- B. Name
- C. Comments
- D. VRF ID

**Answer:** C — Free-form descriptive text goes in the Comments box in the Miscellaneous section. Alias is a short display label, Name is the fixed physical identifier, and VRF ID selects a virtual routing instance.

**71.** The WAN-ISP interface (port6) is set to 172.16.20.1/30. How does the interface list render that /30 prefix in dotted-decimal form in the IP/Netmask column?

- A. 172.16.20.1/255.255.255.248
- B. 172.16.20.1/255.255.255.240
- C. 172.16.20.1/255.255.255.0
- D. 172.16.20.1/255.255.255.252

**Answer:** D — A /30 prefix equals the subnet mask 255.255.255.252 (two host addresses usable). The other masks correspond to /29, /28, and /24 respectively.

**72.** Among the settings available on a FortiGate interface, which one turns the interface into a service that hands out IP addresses automatically to hosts on the attached network?

- A. DHCP server
- B. Alias
- C. IP address
- D. Administrative access

**Answer:** A — The DHCP server setting lets the interface dynamically assign IP addresses to hosts on its connected network. Alias is a label, IP address is the interface's own address, and Administrative access controls management protocols.

**73.** When you enable the DHCP server on a FortiGate interface, what does the Default Gateway handed to clients default to?

- A. The same value as the FortiGate's system DNS server
- B. The same address as the interface's own IP address
- C. The first usable IP in the configured address range
- D. 0.0.0.0 until an administrator enters one manually

**Answer:** B — By default the DHCP server advertises the interface's own IP as the client Default Gateway, since that interface is the clients' next hop. It does not default to the DNS server, the first pool address, or 0.0.0.0.

**74.** In a FortiGate interface's DHCP server settings, which three choices does the DNS Server field present?

- A. Same as Interface IP, Same as Default Gateway, Specify
- B. Same as System DNS, Same as Address Range, Custom
- C. Same as System DNS, Same as Interface IP, Specify
- D. Automatic, Same as Interface IP, Manual

**Answer:** C — The DNS Server field offers Same as System DNS (the default, using FortiGate's own DNS), Same as Interface IP, and Specify for a custom entry. The other option sets are not what the field shows.

**75.** How does the FortiGate DHCP server settings define the pool of addresses it will lease out?

- A. As a single network address written in CIDR prefix notation
- B. As a netmask paired with a default gateway
- C. As a comma-separated list of individual host addresses
- D. As one or more entries, each giving a Starting IP and an End IP

**Answer:** D — The Address Range is entered as rows with a Starting IP and an End IP that bound the block FortiGate leases. It is not a CIDR network, a netmask/gateway pair, or a comma-separated host list.

**76.** In the lab, besides assigning the LAN-facing interface its correct IP address, what additional job must that interface perform so internal clients receive their network settings automatically?

- A. Act as a DHCP server
- B. Act as a DHCP relay
- C. Run in transparent mode
- D. Act as a DNS server

**Answer:** A — The LAN interface is configured as a DHCP server so attached clients get addresses and settings automatically. A DHCP relay would only forward requests to a separate server, and DNS/transparent mode do not hand out leases.

**77.** Where in the FortiGate GUI is a DHCP server enabled for a given network in this lab?

- A. Globally under Network > DNS
- B. Per interface, by turning on the DHCP Server toggle inside that interface's Edit Interface screen
- C. Under Policy & Objects as a DHCP policy
- D. On a single System > DHCP Server page that applies to every interface at once

**Answer:** B — DHCP is configured per interface: the DHCP Server section with its Enable toggle lives inside the Edit Interface dialog. There is no global DHCP page or DHCP policy object driving it.

**78.** A static route is built from three parts. Which part is the IP address of the next hop that FortiGate forwards matching traffic to?

- A. Destination
- B. Interface
- C. Gateway address
- D. Administrative distance

**Answer:** C — The gateway address is the next-hop IP that FortiGate sends matching traffic to. Destination selects which traffic matches, Interface is the egress port, and administrative distance is a route preference value, not one of the three core parts.

**79.** In the FortiOS 7.6 web GUI, which menu path leads to where you add a new static route?

- A. Network > Policy Routes
- B. Network > Routing Objects
- C. Dashboard > Network
- D. Network > Static Routes

**Answer:** D — Static routes are created under Network > Static Routes with Create New. Policy Routes and Routing Objects are separate menu items, and Dashboard > Network is for monitoring rather than creating routes.

**80.** When you build a static default route on a FortiGate, what value belongs in the Destination (subnet) field?

- A. 0.0.0.0/0.0.0.0
- B. 172.16.20.2
- C. 0.0.0.0/255.255.255.255
- D. 10.0.0.0/8

**Answer:** A — A default route uses the all-zeros destination 0.0.0.0/0.0.0.0 so it matches any traffic without a more specific route. 172.16.20.2 would be the gateway, not the destination, and the other subnets are not the default.

**81.** When defining the Destination of a new static route, which two destination types does the New Static Route dialog let you choose between?

- A. Subnet and Named Address
- B. Subnet and Internet Service
- C. IP Range and FQDN
- D. Interface and Gateway

**Answer:** B — The Destination selector offers Subnet or Internet Service; a default route uses Subnet with 0.0.0.0/0. Named Address, IP Range/FQDN, and Interface/Gateway are not the two destination-type choices offered here.

**82.** An administrator at Acme opens Network > Static Routes and clicks Create New to add a route on a FortiGate running FortiOS 7.6. Before changing anything, what value is pre-filled in the Administrative Distance field?

- A. 1
- B. 5
- C. 10
- D. 110

**Answer:** C — The New Static Route dialog pre-populates Administrative Distance with 10, the default for static routes on FortiGate. 110 is the default distance used by OSPF, not by static routes.

**83.** While building a static route on a FortiGate, an engineer enters a gateway address of 10.200.1.254. If that gateway is reachable through the interface named wan1 (port2), what does the FortiGate do with the Interface field?

- A. The route cannot be saved until the interface is chosen by hand
- B. It substitutes a virtual any interface as a placeholder
- C. It stays empty until the OK button is pressed
- D. It is filled in automatically with wan1 (port2)

**Answer:** D — When the gateway IP is entered, FortiGate looks up which interface can reach that next hop and auto-fills the Interface field, here wan1 (port2). The administrator does not have to select the interface manually, so it is not left blank or pending until OK.

**84.** When you view the list of configured static routes under Network > Static Routes on a FortiGate, which group of columns describes each configured entry?

- A. Type, Destination, Gateway IP, Interfaces, Distance, Priority
- B. Type, Source, Next Hop, VLAN, Metric, Weight
- C. Protocol, Destination, Netmask, Gateway, Cost, TTL
- D. Destination, Gateway IP, Interfaces, Metric, Distance, Priority

**Answer:** A — The static route list presents six columns: Type, Destination, Gateway IP, Interfaces, Distance, and Priority. Metric is a property of dynamic routes rather than a column here, so the option that swaps in Metric is incorrect.

**85.** A FortiOS 7.6 administrator wants to see only the routes that are currently active in the forwarding table (the routes actually in use). Which location in the FortiGate GUI shows this?

- A. Network > Static Routes
- B. Dashboard > Network > Static and Dynamic Routing
- C. Network > Routing Objects
- D. Log & Report > Routing Monitor

**Answer:** B — The Dashboard > Network > Static and Dynamic Routing widget displays the live routing table, meaning only the active routes. Network > Static Routes instead lists every route that has been configured, whether or not it is active.

**86.** A static route to 192.168.50.0/24 through wan1 (port6) is present in the FortiGate configuration, yet it never shows up in the active routing table. Which condition explains why an otherwise valid route is excluded?

- A. The route's administrative distance is set to 255
- B. The destination overlaps a connected network
- C. The outgoing interface, port6, is administratively down
- D. The gateway has not been learned via DHCP

**Answer:** C — A configured route is only installed in the routing table when its outgoing interface is up; because port6 is disabled, the route is left out. A route becomes active again once its interface comes back up, its configuration is corrected, or it is no longer beaten by a better route.

#### Set 3 — Firewall Policies

**87.** On a FortiGate, which statement best describes what a firewall policy is?

- A. A collection of rules that decides whether network traffic is allowed and, once allowed, how FortiGate handles it
- B. An entry in the routing table that picks the egress interface for a packet
- C. A translation rule that maps private addresses onto a public address
- D. A profile that scans traffic for malware and intrusion attempts

**Answer:** A — A firewall policy is a set of rules that controls whether traffic is accepted and, if it is, how FortiGate processes it. The other choices describe routing, NAT, and security profiles, which are distinct features rather than the definition of a policy.

**88.** When a firewall policy uses a Service object to match traffic, which attribute of the traffic does that Service object evaluate?

- A. Source port
- B. Destination port
- C. Incoming interface
- D. IP protocol version

**Answer:** B — A Service object matches traffic on its destination port (and protocol), for example HTTP on TCP/80. The incoming interface and the source/destination addresses are separate match criteria handled by other fields in the policy.

**89.** In a FortiGate firewall policy, the Source and Destination fields can each be defined using which pair of criteria?

- A. User or user group
- B. MAC address or FQDN
- C. IP subnet or Internet Services
- D. Schedule or service

**Answer:** C — Both the Source and Destination fields accept an IP subnet (a firewall address) or an Internet Service. Adding a user or user group is an extra option available only on the Source side, and schedule and service are entirely separate policy fields.

**90.** Before you can reference a particular IP subnet as the source or destination of a firewall policy on FortiGate, what must you create first?

- A. An Internet Service object for that subnet
- B. A virtual IP that maps the subnet
- C. Firewall authentication for that subnet
- D. A firewall address object that represents that subnet

**Answer:** D — To use a subnet in a policy you first define a firewall address object for it (for example the LAN subnet), then select that object in the Source or Destination field. Internet Service objects, virtual IPs, and firewall authentication address different needs and are not how a plain subnet is defined.

**91.** You want a firewall policy to match a specific authenticated user as its source rather than an IP address. How is this accomplished on FortiGate?

- A. Enable firewall authentication on the policy, then add the specific users or user groups
- B. Create a firewall address object holding the user's IP address
- C. Leave the source set to the default ALL object
- D. Build an Internet Service object that stands in for the user

**Answer:** A — Matching on a user requires firewall authentication to be configured; you then select the intended users or user groups as the source. The default ALL object matches every address, and neither an address object nor an Internet Service object identifies a user.

**92.** A firewall policy can use an Internet Service from the Internet Service Database (ISDB) as its source or destination. What information does the ISDB provide?

- A. The MAC addresses of endpoints that have been quarantined
- B. The IP subnets of well-known web providers such as Meta and YouTube
- C. The application-control signatures that identify cloud apps
- D. A list of FQDN objects resolved by the FortiGate DNS server

**Answer:** B — The ISDB is a maintained list of the public IP ranges belonging to common internet service providers such as Meta, YouTube, and others, and administrators can add custom entries. It is not a store of MAC addresses, application signatures, or DNS-resolved FQDNs.

**93.** In the simplified firewall policy table used to illustrate policy structure, which set of columns describes each policy row?

- A. ID, Source Address, Destination Address, Schedule, NAT
- B. Name, Incoming Interface, Outgoing Interface, Security Profiles, Log
- C. Name, From, To, Service, Action
- D. Sequence, Source, Destination, Application, Inspection Mode

**Answer:** C — The simplified table lists Name, From, To, Service, and Action for each policy, for example a policy named Internet access from port1 to wan allowing HTTP/HTTPS/DNS with an ACCEPT action. The other column sets mix in fields that are not part of this simplified view.

**94.** The last entry in a FortiGate policy list is the Implicit Deny rule (any source, any destination, service ALL, action Deny). What does FortiGate do with traffic that fails to match any explicit policy above it?

- A. It accepts the traffic but flags it as unmatched in the logs
- B. It redirects the traffic to the management interface
- C. It queues the traffic until an administrator approves it
- D. It drops the traffic

**Answer:** D — Any traffic that does not match an explicit policy falls through to the implicit deny rule and is dropped. FortiGate does not accept, redirect, or hold unmatched traffic.

**95.** Once a firewall policy accepts a session, which further actions can FortiGate perform depending on that policy's configuration?

- A. Network address translation (NAT) and traffic logging
- B. Spanning-tree recalculation and VLAN trunking
- C. HA failover and configuration synchronization
- D. Static route redistribution and OSPF adjacency

**Answer:** A — For accepted traffic, a policy can additionally apply NAT and generate traffic logs (alongside any security profiles it references). Spanning tree, HA, and dynamic routing are unrelated to what a single firewall policy applies to a session.

**96.** Compared with flow-based inspection, how does proxy-based inspection handle traffic on a FortiGate?

- A. It inspects packets as they stream through, with no buffering
- B. It reassembles and examines the content as a whole, inspecting more data points but adding latency
- C. It looks only at the TCP three-way handshake and skips the payload
- D. It turns off NAT so the content can be altered in transit

**Answer:** B — Proxy-based inspection buffers and evaluates the content as a complete object, allowing more thorough inspection at the cost of added latency. Inspecting packets on the fly without buffering describes flow-based mode instead.

#### Set 4 — Logging and Monitoring

**97.** FortiGate groups its logs into three top-level categories. Which option correctly names all three?

- A. Traffic, Event, and Security (UTM)
- B. Forward, Local, and Sniffer
- C. Traffic, System, and Antivirus
- D. Event, VPN, and Web filter

**Answer:** A — The three main log categories are Traffic, Event, and Security (UTM). The other choices list subtypes instead: Forward/Local/Sniffer are Traffic subtypes, and Antivirus/Web filter are Security (UTM) subtypes.

**98.** Within the Traffic log category on a FortiGate, which three subtypes are included?

- A. System, User, and Router
- B. Forward, Local, and Sniffer
- C. Antivirus, Application control, and Web filter
- D. Forward, System, and VPN

**Answer:** B — The Traffic category is made up of the Forward, Local, and Sniffer subtypes. System/User/Router are Event subtypes and Antivirus/Application control/Web filter are Security (UTM) subtypes, so those options belong to other categories.

**99.** Which option lists subtypes that fall under the FortiGate Event log category?

- A. Forward, Local, Sniffer
- B. Antivirus, Application control, Web filter
- C. System, User, Router, VPN
- D. System, Antivirus, Router, Web filter

**Answer:** C — Event log subtypes include System, User, Router, and VPN. Forward/Local/Sniffer are Traffic subtypes and Antivirus/Application control/Web filter are Security (UTM) subtypes; the last option mixes Event and Security subtypes together.

**100.** Traffic Logs on a FortiGate record information about traffic passing through the device as well as its management traffic. Which additional kind of traffic do they capture?

- A. Traffic mirrored to a FortiAnalyzer collector
- B. Traffic captured while FortiGate runs in transparent bridge mode
- C. Traffic forwarded to a remote syslog server
- D. Traffic received when the FortiGate is set up as a one-arm sniffer

**Answer:** D — Traffic Logs also record the traffic seen when the FortiGate acts as a one-arm sniffer. FortiAnalyzer, transparent mode, and syslog are valid FortiGate features but are not what Traffic Logs are defined to capture here.

**101.** When a FortiGate interface is configured as a one-arm sniffer, what role does that interface take on?

- A. An inline intrusion prevention system (IPS) that blocks matching traffic
- B. A transparent-mode firewall bridging two segments
- C. An intrusion detection system (IDS) that only observes traffic without controlling it
- D. A dedicated out-of-band management interface

**Answer:** C — A one-arm sniffer turns the interface into an IDS that passively monitors a copy of the traffic without acting on it. Because it cannot block or alter traffic, it is not an inline IPS; the other options describe unrelated interface roles.

**102.** Which FortiGate log subtype captures records of configuration changes made to the device?

- A. System Events
- B. Forward Traffic
- C. Local Traffic
- D. Security Events

**Answer:** A — System Events (part of the Event category) record device-level activity such as configuration changes. Forward and Local Traffic logs record sessions, and Security Events record UTM inspection results, so none of those track configuration changes.

**103.** After logging in to the FortiGate web interface, which left-menu item do you open to reach the log pages?

- A. Log & Report on the left menu
- B. Security Profiles on the left menu
- C. Dashboard > Status
- D. System > Log Settings

**Answer:** A — The Log & Report menu is the entry point for logs; expanding it reveals Forward Traffic, Local Traffic, Sniffer Traffic, System Events, Security Events, Reports, and Log Settings. The other menu items exist but are not where the log pages live.

**104.** The Local Traffic page displays management traffic and traffic that originates from the FortiGate itself. Which of the following is specifically included on that page?

- A. Web-browsing sessions forwarded on behalf of internal users
- B. FortiGuard and NTP updates and communication with FortiManager and FortiAnalyzer
- C. Antivirus detections and web-filter block actions
- D. Packets captured on a one-arm sniffer interface

**Answer:** B — Local Traffic logs cover sessions to and from the FortiGate itself, such as FortiGuard and NTP updates and its communication with FortiManager and FortiAnalyzer. User web browsing appears in Forward Traffic, block actions in Security logs, and captured packets in Sniffer Traffic.

**105.** The FortiGate System Events page organizes system operation events into which two views?

- A. Summary and Details
- B. Table and Chart
- C. Events and Alerts
- D. Summary and Logs

**Answer:** D — System Events are presented in a Summary view and a Logs view. Details, Table/Chart, and Events/Alerts are not the names of the two tabs on this page.

**106.** On the Summary tab of the System Events page, what does the line chart present, and what do the panes (footers) beneath it show?

- A. The chart aggregates events by severity level, and each footer shows the five most frequent events for a particular log subtype
- B. The chart aggregates events by source interface, and each footer lists the five newest events overall
- C. The chart aggregates events by destination IP, and each footer lists the top five administrators
- D. The chart aggregates events by log ID, and each footer lists the five largest log files

**Answer:** A — The Summary tab shows a line chart of events aggregated by severity level, with footer panes that each cover one log subtype and list its five most common events. The other options misrepresent both the chart's grouping and the contents of the footers.

**107.** On the Summary tab of the Security Events page, which three details are shown for each enabled security log subtype?

- A. The source interface, the severity level, and where the log is stored
- B. The category, the action taken, and the number of instances FortiGate detected
- C. The policy ID, the bytes transferred, and the session duration
- D. The user name, the VDOM, and the destination country

**Answer:** B — For each enabled security log subtype, the Summary tab displays the category, the action taken, and the count of instances detected, along with footers of the most common events. The other option sets describe fields that are not summarized here.

**108.** Which Log & Report view shows traffic that terminates on or originates from the FortiGate itself, such as its management traffic?

- A. Forward Traffic
- B. Local Traffic
- C. Sniffer Traffic
- D. Security Events

**Answer:** B — The Local Traffic view lists sessions that begin or end on the FortiGate, including management traffic. Forward Traffic instead logs sessions passing through the FortiGate between other hosts.

**109.** An analyst expands a Security Events log entry in the FortiGate GUI to inspect a critical detection. Which external destination does the expanded Log Details pane provide a hyperlink to?

- A. The FortiGuard encyclopedia page for the detected threat
- B. The FortiCloud subscription and billing dashboard
- C. The FortiAnalyzer stored report archive
- D. The Fortinet TAC support ticket submission form

**Answer:** A — When you open the Log Details of a security event, FortiGate offers a link out to the relevant FortiGuard threat page so you can research the detection. The link is for threat intelligence lookup, not for billing, report archives, or opening support cases.

**110.** While reviewing traffic logs in the FortiGate GUI, an operator right-clicks a value inside one of the table columns. What menu appears, and what two choices does it present for that value?

- A. A 'Sort by <column name>' menu with Ascending and Descending
- B. An 'Export <column name>' menu with CSV and PDF
- C. A 'Filter by <column name>' menu with Contains and Does not contain
- D. A 'Group by <column name>' menu with Merge and Split

**Answer:** C — Right-clicking a cell value opens a 'Filter by <column name>' context menu whose two options are Contains and Does not contain, letting you quickly include or exclude that value. Sorting, exporting, and grouping are separate actions and are not the choices offered by this right-click menu.

**111.** An administrator applies a filter in the FortiGate log view to narrow down the entries on screen. What happens to the log records that do not match the applied filter?

- A. They are permanently erased from the log database
- B. They are automatically pushed to FortiAnalyzer for archiving
- C. They are relocated to memory storage until the filter is removed
- D. Nothing is removed; the filter only changes which records are shown

**Answer:** D — Filtering is purely a display control: it hides non-matching entries from view but does not delete or move any stored logs. Clearing the filter brings the full set back, so no records are erased, archived, or relocated by filtering.

**112.** Which statement correctly describes how log filtering works in the FortiGate GUI?

- A. Filtering is offered only in the Forward Traffic log view
- B. Only the Date/Time column may be used as a filter
- C. Filters can be applied exclusively by editing the CLI configuration
- D. The same filtering approach applies across every log category, and a filter can be built on any column

**Answer:** D — The identical filtering techniques are available in all log categories, and you can add a filter based on any displayed column (for example Application Name or Policy ID). Filtering is therefore not restricted to one view, a single column, or CLI-only configuration.

**113.** An administrator wants to store logs on the FortiGate's local disk. In the FortiGate GUI, which navigation path is used to configure local disk logging?

- A. Log & Report > Log Settings > Local Logs
- B. System > Settings > Logging
- C. Log & Report > Forward Traffic
- D. Security Fabric > Logging > Local Disk

**Answer:** A — Local disk logging is enabled under Log & Report > Log Settings, in the Local Logs section. This simple option suits small deployments and lab use; the other paths either do not exist or point to log viewing rather than storage configuration.

**114.** In the global logging settings, the Local traffic logging feature controls logging for a specific category of traffic. Which traffic does it cover?

- A. Forwarded traffic that passes between two hosts through the FortiGate
- B. Traffic originating from or destined to the FortiGate itself (local-in and local-out)
- C. Only traffic carried inside encrypted VPN tunnels
- D. Packets captured by a one-arm sniffer interface

**Answer:** B — Local traffic logging handles local-in and local-out traffic, meaning sessions that terminate on or originate from the FortiGate itself, which is useful for auditing management access and spotting attacks against the device. Traffic passing between two hosts is forwarded traffic, logged separately in firewall policies.

**115.** When logging is configured within firewall policies, which of the following types of traffic is NOT logged by default?

- A. Traffic accepted by a policy that has Log Allowed Traffic enabled
- B. Local-in traffic terminating on the FortiGate
- C. Traffic dropped by the Implicit Deny policy
- D. Traffic scanned by an applied AntiVirus profile

**Answer:** C — Traffic denied by the Implicit Deny policy is not logged unless you explicitly turn that logging on, so it is off by default. Allowed traffic is captured through the Log Allowed Traffic option on a policy (Security Events or All Sessions), which is a deliberate configuration choice.

**116.** Which statement accurately describes FortiGate's default logging behavior out of the box?

- A. Every log type is enabled by default and needs no configuration
- B. Only security/UTM logs are turned on by default
- C. Logging is on by default but held in memory until a disk is added
- D. Logging is not enabled by default for all log types, so it must be configured

**Answer:** D — FortiGate does not enable every log type automatically, so the administrator must configure what to log, where it is stored, and (for traffic logs) which policies generate them. It is therefore incorrect to assume all logging works with no setup.

**117.** An administrator needs a firewall policy to produce log entries for the sessions it permits. What must be done to the policy to achieve this?

- A. Change the policy action to Deny
- B. Turn on Sniffer mode on the ingress interface
- C. Edit the policy and enable Log Allowed Traffic
- D. Switch the policy's inspection mode to flow-based

**Answer:** C — Logging of permitted sessions is controlled by the Log Allowed Traffic setting inside the firewall policy, so you edit the policy and enable it (choosing Security Events or All Sessions). Setting the action to Deny or changing inspection mode does not turn on logging of accepted traffic.

#### Set 5 — Firewall Authentication

**118.** FortiGate firewall authentication is grouped into two broad password-based method types. What are those two types?

- A. Local password authentication and remote password authentication
- B. Certificate-based authentication and token-based authentication
- C. Single sign-on authentication and two-factor authentication
- D. Active authentication and passive authentication

**Answer:** A — The two categories of firewall authentication are local password authentication (credentials stored on the FortiGate) and remote password authentication (credentials verified by an external server). The other pairs describe related FortiGate features but are not the two method categories.

**119.** Consider a workstation at 10.20.5.42 whose user, Priya, must sign in before browsing. What core capability does firewall authentication give the FortiGate?

- A. It encrypts every packet exchanged between the workstation and the FortiGate
- B. It identifies the real user behind an IP address rather than treating the session as anonymous
- C. It hands out IP addresses to internal hosts through DHCP
- D. It automatically blocks all traffic sourced from unknown IP addresses

**Answer:** B — Firewall authentication ties a session to a known identity, so the FortiGate can enforce policy on the actual user (Priya) instead of an anonymous IP address. It is an identity mechanism, not an encryption service, an address-assignment service, or a blanket IP block.

**120.** A small office runs a single FortiGate and has no external authentication server. Which firewall authentication type best fits this deployment?

- A. Remote authentication
- B. Two-factor authentication
- C. Local authentication
- D. Fortinet Single Sign-On (FSSO)

**Answer:** C — With one FortiGate and no external server, local authentication is the right choice because user credentials are stored directly on the FortiGate. Remote authentication and FSSO both depend on an external server, which this site does not have.

**121.** An organization operates several FortiGate devices across multiple sites and has deployed a FortiAuthenticator. Which firewall authentication type best fits this environment?

- A. Local authentication
- B. Guest authentication
- C. Exempt authentication
- D. Remote authentication

**Answer:** D — Remote authentication is ideal here because a central FortiAuthenticator lets all the FortiGates validate users against one shared external database. Local authentication would force duplicate user accounts on each device, which does not scale across multiple sites.

**122.** In the ordered workflow for setting up local authentication on a FortiGate, what is the first task?

- A. Create a user account
- B. Configure a remote authentication server
- C. Build a firewall policy that requires authentication
- D. Enable two-factor authentication

**Answer:** A — Local authentication begins by creating a user account so the credentials are stored on the FortiGate itself. Configuring a remote server belongs to remote authentication, while the firewall policy and any two-factor setup come later in the sequence.

**123.** Which FortiGate GUI menu path launches the wizard used to create a new local firewall user account?

- A. User & Authentication > User Groups
- B. User & Authentication > User Definition
- C. User & Authentication > LDAP Servers
- D. Policy & Objects > Firewall Policy

**Answer:** B — New local users are created under User & Authentication > User Definition, which opens the creation wizard (user type, credentials, contact, and extra info steps). User Groups builds groups, LDAP Servers defines a remote server, and Firewall Policy is unrelated to creating users.

**124.** An administrator is creating a user group that will manage temporary guest accounts. In the Create User Group form, which value must be selected in the Type field to enable guest-specific settings?

- A. Firewall
- B. Fortinet Single Sign-On (FSSO)
- C. Guest
- D. RADIUS Single Sign-On

**Answer:** C — Choosing Guest as the group Type reveals the guest-specific options such as guest details and expiration. Firewall, FSSO, and RADIUS Single Sign-On are the other valid group types but none of them exposes the guest account settings.

**125.** When configuring a guest user group, the Expiration section's Start Countdown option offers two settings for when the account timer begins. In the example, which setting is chosen so the countdown starts only once the guest actually connects?

- A. On Account Creation
- B. On Password Reset
- C. On Group Assignment
- D. After First Login

**Answer:** D — Selecting After First Login delays the expiration countdown until the guest's initial successful login, which is useful when accounts are created in advance. The only other real choice is On Account Creation; On Password Reset and On Group Assignment are not offered.

**126.** When creating a new user group under User & Authentication > User Groups, which of the following is NOT a valid group Type option in the dropdown?

- A. TACACS+ Single Sign-On
- B. Firewall
- C. Fortinet Single Sign-On (FSSO)
- D. RADIUS Single Sign-On (RSSO)

**Answer:** A — The user group Type dropdown offers exactly Firewall, Fortinet Single Sign-On (FSSO), RADIUS Single Sign-On (RSSO), and Guest. There is no TACACS+ Single Sign-On type, even though TACACS+ is supported elsewhere as a remote authentication server.

**127.** In the four-step workflow for configuring remote authentication on a FortiGate, what is the final task?

- A. Create the firewall policy
- B. Verify the configuration and monitor users
- C. Define the LDAP server
- D. Add the user to a group

**Answer:** B — The closing step of the remote authentication workflow is to verify the configuration and monitor the authenticated users, confirming everything works end to end. Defining the server and adding users to groups are earlier setup tasks.

**128.** An administrator adds a new LDAP server object on the FortiGate for remote authentication. What value is pre-populated by default in the Server Port field?

- A. 636
- B. 1812
- C. 389
- D. 3268

**Answer:** C — The default LDAP Server Port on FortiGate is 389, the standard cleartext LDAP port. Port 636 is LDAPS, 1812 is RADIUS authentication, and 3268 is the Active Directory Global Catalog, none of which is the LDAP default.

**129.** While editing an LDAP server object, an administrator changes the Bind Type from Simple to Regular. Which additional fields appear and must be filled in as a result?

- A. Common Name Identifier and Distinguished Name
- B. Server IP/Name and Server Port
- C. Secure Connection and Exchange server
- D. Username and Password

**Answer:** D — Regular bind requires the FortiGate to authenticate to the LDAP directory first, so selecting it exposes Username and Password fields for the bind account. The Server IP/Port and Common Name Identifier fields are present regardless of Bind Type.

**130.** In the firewall authentication lab task list (create a user account, configure remote authentication, create a user group, then verify and monitor), which task is fourth?

- A. Add authentication to the firewall policy
- B. Create a user account
- C. Configure remote authentication
- D. Verify and monitor firewall authentication

**Answer:** A — After creating the user account, configuring remote authentication, and creating the user group, the fourth task is to add authentication to the firewall policy by referencing the group. Verifying and monitoring is the fifth and final task.

**131.** An 'Internet Access' policy already uses 'Internal Network' as its source address. To also require that only members of the authenticated 'sales' group are allowed, which policy field must the group be added to?

- A. Destination
- B. User/group
- C. Service
- D. Outgoing interface

**Answer:** B — A user group is added to the policy's User/group field, alongside the source address, which forces users to authenticate as members of that group before the policy applies. Destination, Service, and Outgoing interface do not enforce user identity.

**132.** After a policy is set to require authentication, how does the user cause the FortiGate firewall-authentication login prompt to appear?

- A. By signing in to the FortiGate management GUI as admin
- B. By opening an SSH session to the FortiGate
- C. By opening a web browser and trying to reach an external site such as `https://www.example.com`
- D. By pinging the network's default gateway

**Answer:** C — The prompt is triggered when the user opens a browser and attempts to reach a website through the authenticating policy, at which point FortiGate intercepts the HTTP/HTTPS request and presents the login page. Logging in to the GUI, using SSH, or pinging the gateway does not invoke firewall authentication.

#### Set 6 — Mixed Operator Practice Exam

**133.** Why does FortiCare matter to a network administrator managing Fortinet devices?

- A. It lets administrators design secure network topologies.
- B. It removes the need for security appliances because FortiGuard handles everything.
- C. It guarantees privacy by automatically encrypting all network traffic.
- D. It delivers technical support, firmware updates, and device management tools.

**Answer:** D — FortiCare is Fortinet's support and lifecycle service, giving administrators access to technical support, firmware updates, and device management tooling. It is not a design tool, a replacement for security devices, or a traffic-encryption feature.

**134.** An administrator wants to raise the Security Rating score reported by the Fortinet Security Fabric. Which action improves that score?

- A. Run an integrity check on every end device.
- B. Create a configuration revision or back up the configuration.
- C. Upgrade the FortiGate to the newest mature firmware release.
- D. Implement one or more of the recommended best practices.

**Answer:** D — The Security Rating audits the fabric against Fortinet best practices and lists recommendations; applying those recommended best practices is what raises the score. Backing up the config or upgrading firmware are good hygiene but are not how the rating itself is improved.

**135.** Which three of the following are services or features of the FortiCloud management portal? (Choose three.)

- A. Identity and access management (IAM)
- B. Organization management
- C. Asset management
- D. FortiGuard threat intelligence
- E. Network traffic filtering

**Answer:** A, B, C — The FortiCloud portal provides identity and access management (IAM), organization management, and asset management for administering accounts and devices. FortiGuard threat intelligence and network traffic filtering are FortiGate/FortiGuard functions rather than FortiCloud portal features.

**136.** A network administrator at Meridian Retail wants a single portal to oversee all of the company's Fortinet products, user accounts, and subscription services. What is the main advantage FortiCloud offers in this role?

- A. It removes the requirement to write any security policies because a managed policy service does it for you.
- B. It swaps out on-premises Fortinet appliances entirely for cloud-only equivalents.
- C. It gives you one centralized place to manage devices, users, and services.
- D. It auto-tunes each FortiGate's security features without any administrator input.

**Answer:** C — FortiCloud's core value is a single, centralized console for managing Fortinet devices, users, and subscriptions. It does not eliminate the need for policies or replace hardware, and it does not silently self-configure every device.

**137.** When you build out the Fortinet Security Fabric, which two destinations can serve as the centralized logging backend? (Choose two.)

- A. FortiAnalyzer
- B. FortiGate Cloud
- C. A generic third-party syslog server
- D. FortiSOAR

**Answer:** A, B — The Security Fabric relies on either FortiAnalyzer or FortiGate Cloud as its centralized logging repository. A plain syslog server is not a Fabric logging backend, and FortiSOAR handles orchestration and response rather than log storage.

**138.** In the Fortinet ecosystem, what is FortiCare mainly responsible for?

- A. Delivering technical support, firmware updates, and device lifecycle services such as registration and RMA.
- B. Building and pushing firewall rules to Fortinet appliances.
- C. Watching and shaping network traffic to improve throughput.
- D. Scanning the network to flag hosts and applications that are missing patches.

**Answer:** A — FortiCare is Fortinet's support and lifecycle service, covering technical support, updates, registration, and RMA. It does not author firewall policy, shape traffic, or perform vulnerability scanning.

**139.** Within the Fortinet Security Fabric, what does the Security Rating measure and how is the score produced?

- A. A gauge of the current throughput and latency of the network.
- B. A numeric score generated by auditing device configurations against Fortinet best practices.
- C. A measure of how well the Fabric interoperates with non-Fortinet equipment.
- D. A figure derived from counting how many security log entries have been recorded.

**Answer:** B — The Security Rating runs configuration checks against Fortinet's recommended best practices and returns a numeric score. It is not a performance metric, a compatibility index, or a tally of log volume.

**140.** Which statement most accurately characterizes FortiCloud?

- A. A web utility whose only function is editing firewall rules on a FortiGate.
- B. A paid feed that supplies threat intelligence signature updates.
- C. A cloud offering that pushes policies, watches the network, and administers devices.
- D. A cloud-based platform for managing Fortinet devices and services.

**Answer:** D — FortiCloud is best defined broadly as the cloud platform for managing Fortinet devices and services. The narrower descriptions each capture only a fragment of what it does or describe a different offering.

**141.** A developer wants a cloud model where they write and run their own application code and own the data, but never have to patch the operating system, runtime, or underlying servers. Which cloud service model fits this?

- A. IaaS
- B. SECaaS
- C. SaaS
- D. PaaS

**Answer:** D — In PaaS the provider maintains the infrastructure, OS, and runtime while the customer is responsible only for their applications and data. With IaaS the customer would also manage the OS, and with SaaS the vendor manages the application too.

**142.** When deploying FortiGate into a public cloud environment, what is the recommended way to position it relative to the provider's own security features?

- A. Rip out every native cloud security control and rely solely on FortiGate.
- B. Run FortiGate together with the cloud provider's native security tools.
- C. Limit FortiGate to load-balancing duties for cloud workloads.
- D. Restrict FortiGate to private-cloud deployments only.

**Answer:** B — The guidance is for FortiGate to complement, not replace, the cloud provider's native security controls, giving layered defense. Removing native controls, restricting FortiGate to load balancing, or barring it from public clouds are all incorrect.

**143.** Which of the following is a genuine use of Security Fabric automation stitches?

- A. Tracking how much disk space FortiAnalyzer is consuming
- B. Producing scheduled weekly summary reports for managers
- C. Handing out security ratings to freshly onboarded devices
- D. Automatically isolating an endpoint after malicious behavior is detected

**Answer:** D — An automation stitch pairs a trigger with an action, such as quarantining a host once malicious activity is flagged. The other choices describe monitoring, reporting, or rating tasks rather than trigger-driven automated response.

**144.** Which two goals can an attacker pursue by deploying malware against an organization? (Choose two.)

- A. Force a high availability (HA) cluster to fail over
- B. Physically burn out the device's network ports
- C. Demand a ransom payment
- D. Exfiltrate proprietary intellectual property

**Answer:** C, D — Malware such as ransomware is commonly used to extort payment and to steal intellectual property. It cannot physically destroy hardware ports, and triggering an HA failover is not a malware objective.

**145.** For the intrusion prevention system (IPS) engine to catch attacks hidden inside HTTPS sessions, why must SSL inspection be enabled?

- A. By default the IPS engine can only read traffic that uses outdated cipher suites.
- B. SSL inspection speeds up the network by letting encrypted flows skip inspection.
- C. SSL inspection decrypts the session so the IPS can examine the payload for threats.
- D. If SSL inspection is off, the IPS drops all encrypted traffic automatically.

**Answer:** C — IPS can only match signatures against data it can read, so SSL inspection must decrypt the traffic first to expose threats inside encrypted sessions. IPS does not automatically block encrypted traffic, and SSL inspection does not bypass or accelerate flows.

**146.** What role does the FortiGuard Labs signature database play for a FortiGate?

- A. It lets the FortiGate record traffic volumes and usage trends.
- B. It supplies pre-built secure configuration templates to the FortiGate.
- C. It keeps the FortiGate defended against the newest malware and threat variants.
- D. It scans the FortiGate itself and repairs software vulnerabilities.

**Answer:** C — FortiGuard Labs continuously publishes signatures so the FortiGate stays protected against emerging malware and threats. The database is not a usage tracker, a template library, or a self-patching tool.

**147.** By what method does the FortiGate IPS engine use signatures to spot malicious traffic?

- A. It drops every packet that crosses the firewall.
- B. It compares inspected packets against a database of known-threat signatures.
- C. It tracks which websites individual users visit.
- D. It decrypts SSL/TLS traffic on its own.

**Answer:** B — The IPS engine inspects packets and matches them against a signature database of known threats to identify malicious activity. It does not block all traffic, monitor browsing habits, or perform decryption by itself (that requires an SSL inspection profile).

**148.** Which class of capability does FortiGuard Labs contribute to the FortiGuard Security Services portfolio?

- A. Network segmentation and access control
- B. Advanced threat intelligence and prevention
- C. Data encryption and secure communications
- D. Endpoint protection and vulnerability management

**Answer:** B — FortiGuard Labs is the research arm that delivers advanced threat intelligence and prevention, powering real-time protection across Fortinet products. Segmentation, encryption, and endpoint management are handled by other components, not FortiGuard Labs.

**149.** FortiGuard Labs organizes its offerings into three principal categories. Which option lists them correctly?

- A. Threat hunting, intrusion detection, and firewall management
- B. Data encryption, network segmentation, and access control
- C. Machine learning, antivirus, and network monitoring
- D. Trusted AI/machine learning, real-time threat protection, and threat hunting with outbreak alerts

**Answer:** D — FortiGuard Labs groups its work into trusted AI/machine learning, real-time threat protection, and threat hunting with outbreak alerting. The other lists mix in unrelated firewall, encryption, or segmentation functions.

**150.** In an Application Control profile, which set of actions can you assign to an application or application category?

- A. Authenticate, log, encrypt, or back up
- B. Allow, encrypt, compress, or redirect
- C. Monitor, allow, block, or quarantine
- D. Monitor, optimize, redirect, or shape

**Answer:** C — Application Control lets you set an application or category to Monitor, Allow, Block, or Quarantine. The other option sets list actions that Application Control does not provide.

**151.** Which scanning method identifies already-known malware by matching content against signatures in the FortiGuard Labs database?

- A. Grayware scan
- B. Behavioral analysis scan
- C. Machine learning (ML)/artificial intelligence (AI) scan
- D. Antivirus scan

**Answer:** D — The antivirus (signature) scan compares files against known-malware signatures from FortiGuard. Grayware detection targets unwanted programs, and behavioral or ML/AI methods look for unknown threats rather than exact signature matches.

**152.** In the FortiGate log viewer, under which log category do antivirus detection entries appear?

- A. Sniffer Traffic
- B. Security Events
- C. System Events
- D. Forward Traffic

**Answer:** B — Antivirus and other UTM/security-profile detections are logged under Security Events. System Events cover device-level activity, while Forward Traffic and Sniffer Traffic are traffic logs, not security detections.

**153.** To turn on antivirus scanning for traffic matched by a firewall policy, which antivirus object do you attach to that policy?

- A. Antivirus schedule
- B. Antivirus engine version
- C. Antivirus exclusion list
- D. Antivirus profile

**Answer:** D — You enable scanning by selecting an Antivirus profile on the firewall policy. There is no scheduling, engine-version, or exclusion-list object that you attach to a policy to enable AV.

**154.** A FortiGate has one interface operating as a one-arm intrusion detection (IDS) sniffer. Under which log category will its detections show up?

- A. Forward Traffic
- B. System Events
- C. Sniffer Traffic
- D. Local Traffic

**Answer:** C — A one-arm sniffer / IDS interface records its findings under Sniffer Traffic. Forward and Local Traffic apply to traffic passing through or destined to the FortiGate, and System Events cover device operations.

**155.** Users on the internal network are streaming YouTube, and you want to review the log entries generated for that activity. Where in the GUI do you look?

- A. Log and Report > Security Events > Application Control
- B. Log and Report > Security Events > Intrusion Prevention
- C. Log and Report > Security Events > Antivirus
- D. Log and Report > Security Events > Web Filter

**Answer:** A — YouTube is recognized by Application Control as an application, so its activity is logged under Security Events > Application Control. Intrusion Prevention, Antivirus, and Web Filter logs record different inspection types.

**156.** Why does the intrusion prevention system (IPS) require SSL inspection to catch threats carried inside encrypted traffic?

- A. SSL inspection decrypts the traffic so the IPS can inspect the payload and detect threats.
- B. SSL inspection boosts performance by letting encrypted traffic skip inspection.
- C. Without SSL inspection the IPS drops all encrypted traffic by default.
- D. The IPS engine can only parse legacy encryption algorithms out of the box.

**Answer:** A — SSL inspection decrypts the session so its contents become visible to the IPS engine, which can then match signatures against the payload. The IPS does not block encrypted traffic outright, and inspection does not bypass or accelerate flows.

**157.** Setting aside the optional sensor-tuning work, what is the final step when configuring IPS on a FortiGate so that it actually inspects traffic?

- A. Blocking malicious URLs and botnet command-and-control (C&C) traffic
- B. Editing the sensor's signatures and filters
- C. Applying the IPS sensor to a firewall policy
- D. Enabling SSL inspection on the traffic of interest

**Answer:** C — An IPS sensor only takes effect once it is referenced by a firewall policy, so applying the sensor to a policy is the concluding step. Editing signatures is tuning, and URL/C&C blocking and SSL inspection are separate features.

**158.** How does the FortiGate IPS recognize traffic that violates the expected structure of a protocol standard?

- A. By running the traffic through protocol decoders
- B. By decrypting the network packets
- C. By inspecting the SSL certificates presented
- D. By profiling individual user behavior

**Answer:** A — IPS protocol decoders parse each session against the rules of its protocol and flag anything that deviates from the standard. Decryption, certificate analysis, and user-behavior profiling are handled by other mechanisms.

**159.** Peer-to-peer applications often hop ports and disguise themselves to slip past filtering. How does FortiGate Application Control counter these evasion tactics?

- A. By checking requests against a list of blocked URLs
- B. By reviewing flow-based inspection statistics
- C. By permitting traffic only on a fixed set of well-known ports
- D. By inspecting traffic for known application signatures and patterns

**Answer:** D — Application Control identifies an application from its traffic signatures and patterns rather than its port, so it still recognizes P2P apps even when they change ports. URL block lists and fixed-port allowances are exactly the port/URL-based controls that P2P evasion defeats.

**160.** How is grayware best defined?

- A. Brand-new, previously unseen malware variants
- B. Established malware for which signatures already exist
- C. Unwanted programs installed without the user's genuine consent
- D. Suspicious files forwarded to a sandbox for detonation

**Answer:** C — Grayware describes unsolicited, unwanted software such as adware or toolbars that gets installed without the user's clear consent. It is neither classic signature-based malware nor a sandboxing process.

**161.** In broad terms, how does an intrusion prevention system defend a network against attacks?

- A. By analyzing traffic to identify and stop potential threats
- B. By encrypting all traffic that originates from untrusted IP addresses
- C. By permitting only secured access methods to reach network resources
- D. By dropping every inbound connection from any previously unseen source

**Answer:** A — An IPS inspects traffic and compares it against threat signatures and anomaly rules to detect and block attacks. It does not encrypt traffic, act as an access-control gateway, or blindly drop all new inbound connections.

**162.** In which network architecture has controlling application traffic become especially important because applications frequently change ports to avoid detection?

- A. Traditional client-server architecture
- B. Peer-to-peer architecture
- C. Distributed architecture
- D. Cloud-based architecture

**Answer:** B — Peer-to-peer applications like BitTorrent hop between dynamic ports specifically to dodge port-based filtering, making application control especially relevant there. Client-server, distributed, and cloud designs do not rely on that port-evasion behavior in the same way.

**163.** A workstation at Meridian Freight sends traffic through a FortiGate before any login prompt is presented. Which attribute of that traffic can the FortiGate already identify?

- A. The name of the application generating the session
- B. The account name of the person at the keyboard
- C. The IP address the packets are coming from
- D. The DNS domain the traffic originated in

**Answer:** C — Before firewall authentication takes place, the FortiGate can see the packet's source IP address but has no way to tie it to a specific user identity — that link only exists once the user authenticates.

**164.** On a FortiGate protecting the Aurora Labs network, what role do firewall policies serve?

- A. They decide which traffic is permitted and how it is handled
- B. They apply cryptographic protection to traffic in transit
- C. They passively observe traffic without acting on it
- D. They discard every session arriving from outside the network

**Answer:** A — Firewall policies are the rules that determine whether a session is accepted or denied and which processing is applied to it. Encryption and pure monitoring are separate functions, not the core purpose of a policy.

**165.** An administrator at Coastal Systems wants FortiGate to identify staff who authenticate against an external RADIUS server. What is the recommended way to build this?

- A. Add a local user account, reference that account as the policy source, and confirm the result in the logs.
- B. Build a user group and point a firewall policy's source at that group with no further mapping.
- C. Build a user group, associate the authenticated remote users with that group, then use the group as the source of a firewall policy.
- D. Point the firewall policy source at the IP address of the external authentication server.

**Answer:** C — For remote authentication you create a user group, map the users returned by the remote server into it, and then reference that group as the policy source. Referencing the server's own IP or a bare group with no membership mapping would not identify individual users.

**166.** Which pair of values can be evaluated in the Source field of a FortiGate firewall policy?

- A. Ingress interface and TCP service
- B. IP address and authenticated user
- C. Hardware MAC address and domain name
- D. Address group and device hostname

**Answer:** B — The Source field matches on an address (IP) and, when firewall authentication is used, on a user or user group. Service and interface are configured in their own separate policy fields.

**167.** A small branch of Larkspur Design wants every employee on the LAN to reach the internet through one policy. Which two things can you set as the Source of that firewall policy? (Choose two.)

- A. Users or user groups
- B. Application control signatures
- C. Security profile sets
- D. The address object for the LAN subnet

**Answer:** A, D — A policy Source can be an address object (such as the LAN subnet) and optionally users or user groups. Application signatures and security profiles are inspection settings applied to accepted traffic, not selectable as a Source.

**168.** Why would an administrator define a firewall address object on a FortiGate?

- A. To designate which interfaces a policy uses for ingress and egress
- B. To set whether a policy accepts or denies traffic
- C. To represent an IP host or subnet so it can be matched as a policy source or destination
- D. To turn on web filtering for a particular host

**Answer:** C — An address object stands in for a host or subnet so that it can be referenced in the Source or Destination of a policy. Interfaces, the accept/deny action, and web filtering are all configured elsewhere.

**169.** You want a firewall policy on FortiGate to use a well-known cloud application as its destination. How do you specify it?

- A. Pick the application from the Internet Service Database (ISDB).
- B. Enter the MAC address associated with the application.
- C. Type in the IP subnet the application is hosted on.
- D. Attach a virtual IP that represents the application.

**Answer:** A — Internet services are added to a policy's source or destination by selecting the appropriate entry from the FortiGuard-maintained Internet Service Database, which already tracks the relevant address ranges. Manually entering subnets, MACs, or a VIP is not how ISDB destinations work.

**170.** In which situation is remote authentication a better fit than local authentication on FortiGate?

- A. When traffic from locally defined accounts should be deprioritized
- B. When several FortiGate devices must authenticate the same users or groups
- C. When there is no authentication server reachable on the network
- D. When the FortiGate model cannot store local user accounts

**Answer:** B — Remote authentication keeps credentials in one central server, so multiple FortiGates can validate the same users and groups without duplicating accounts. It requires a reachable auth server, so the absence of one would rule it out.

**171.** Why is referencing a user group, rather than individual accounts, considered best practice in firewall policies?

- A. It makes it easier to watch which users are currently authenticated.
- B. It keeps the firewall configuration simpler to build and maintain.
- C. It applies a stronger encryption algorithm to the login exchange.
- D. It automatically includes every user account that exists on the device.

**Answer:** B — Pointing a policy at a group lets you manage access by editing group membership once instead of rewriting policies for each user, which keeps the configuration simpler. Groups do not change encryption strength or automatically enroll all accounts.

**172.** How would an administrator confirm which users have logged in successfully through FortiGate authentication?

- A. By watching a live threat-map animation of security events
- B. By subscribing to third-party threat intelligence feeds
- C. By statistically profiling raw traffic patterns
- D. By reading the authentication logs and the related dashboards

**Answer:** D — Successful logins are recorded in the user/authentication logs and surfaced on the FortiGate dashboards, which is where an administrator reviews them. Threat feeds and traffic profiling do not report authentication outcomes.

**173.** Why does the position of a policy in the FortiGate firewall policy list matter?

- A. It prevents naming collisions between policies that share the same label
- B. It guarantees that security traffic is logged ahead of ordinary traffic
- C. It ensures narrowly scoped policies are evaluated before broader ones
- D. It lets high-priority traffic be processed with less CPU overhead

**Answer:** C — FortiGate reads the policy table from top to bottom and stops at the first match, so a more specific policy has to sit above a broader one or it will never be reached. Ordering is about match precedence, not logging sequence or CPU load.

**174.** Once a firewall policy has accepted a session, which two additional inspections can FortiGate apply to it? (Choose two.)

- A. Antivirus scanning
- B. The accept-or-deny packet decision
- C. Application control
- D. Prompting the user to authenticate

**Answer:** A, C — After a policy accepts a session, security profiles such as antivirus scanning and application control can inspect it. The accept decision itself and user authentication both happen as part of matching the policy, before that point.

**175.** When FortiGuard category filtering is in use, on what basis are websites allowed or blocked?

- A. On the numeric IP address that hosts the site
- B. On a live malware scan performed against the site
- C. On the category FortiGuard has assigned to the site's content
- D. On the values found in the site's HTTP response headers

**Answer:** C — FortiGuard classifies sites into content categories, and the web filter permits or denies access according to the category rating for the requested site. It is not driven by the raw IP address or by inspecting HTTP headers.

**176.** With FortiGuard category filtering set to block a category, what does a user experience when they browse to a site in that category?

- A. The browser shows a replacement message stating the site is blocked.
- B. The browser shows a caution page but lets the user proceed anyway.
- C. The browser asks the user to supply valid credentials to continue.
- D. The site loads normally while the visit is quietly recorded in the logs.

**Answer:** A — A category set to the Block action returns a FortiGate replacement (block) page and stops the request. The proceed-anyway behavior belongs to the separate Warning action, not Block.

**177.** How does SSL certificate inspection fundamentally differ from SSL deep inspection on FortiGate?

- A. Certificate inspection creates certificate errors, whereas deep inspection eliminates certificate warnings.
- B. Certificate inspection needs a publicly trusted CA, whereas deep inspection relies on the FortiGate CA certificate.
- C. Certificate inspection covers HTTPS only, whereas deep inspection covers several SSL-encrypted protocols.
- D. Certificate inspection decrypts and reads the payload, whereas deep inspection merely checks the server's identity.

**Answer:** C — Certificate inspection only reads the certificate and SNI of HTTPS sessions without decrypting them, while deep inspection actually decrypts and can inspect a range of SSL-encrypted protocols such as HTTPS, SMTPS, and POP3S. The last option reverses which mode decrypts.

**178.** Which two actions are part of setting up web filtering based on FortiGuard category filters? (Choose two.)

- A. Reinstall FortiOS so the newest FortiGuard database is present.
- B. List out each individual website you intend to block or permit.
- C. Attach the web filter security profile to the relevant firewall policy.
- D. Create a web filter security profile that uses FortiGuard category ratings.

**Answer:** C, D — You build a web filter profile that acts on FortiGuard categories and then apply that profile to a firewall policy. Category filtering does not require enumerating individual sites or reinstalling FortiOS to update the database.

**179.** During SSL deep inspection with the default FortiGate CA certificate, why does a client browser pop up a certificate warning?

- A. The browser has no support for SSL deep inspection at all.
- B. The re-signed certificate makes FortiGate look like a man-in-the-middle attacker.
- C. The FortiGate is signing sessions with a CA the browser does not trust.
- D. The FortiGate cannot decrypt the SSL-encrypted session.

**Answer:** C — Deep inspection re-signs each session with the FortiGate CA, and any browser that does not already trust that CA raises a warning. Importing the FortiGate CA into the browser's trust store clears the warning.

**180.** Which FortiGate inspection mode reassembles and evaluates the complete content before deciding what to do with it?

- A. Application-level inspection
- B. Proxy-based inspection
- C. Stateful inspection
- D. Flow-based inspection

**Answer:** B — Proxy-based inspection buffers the full object and examines it as a whole, giving more thorough analysis at the cost of added latency, whereas flow-based inspection evaluates packets as they stream through.

**181.** Why do organizations and individuals deploy web filtering? (Choose two.)

- A. To keep employees focused and productive
- B. To reduce congestion on the network
- C. To add more raw bandwidth to the link
- D. To make the browsing experience feel faster for everyone

**Answer:** A, B — Blocking distracting or bandwidth-heavy sites both preserves employee productivity and eases network congestion. Web filtering does not create additional bandwidth on the circuit.

**182.** What security concern does HTTPS introduce for a network defender?

- A. It is incompatible with some older web browsers
- B. It can carry malicious content hidden inside encryption
- C. It noticeably increases end-to-end network latency
- D. It frequently causes certificate errors during the handshake

**Answer:** B — Because HTTPS encrypts the payload, malicious content can travel inside the encrypted channel and slip past inspection unless SSL inspection is applied. The other choices are not the core security risk of HTTPS.

**183.** Which FortiGate inspection mode examines and forwards packets individually instead of waiting for the whole file or page to arrive?

- A. Proxy-based inspection
- B. Stateful inspection
- C. Flow-based inspection
- D. Application-level inspection

**Answer:** C — Flow-based inspection evaluates traffic packet by packet as it passes through, without buffering the entire object, so it adds less latency than proxy-based inspection, which waits for the complete content.

**184.** For a certificate to function as a signing CA (for example, the FortiGate CA used in deep inspection) without producing errors, which field settings must it carry?

- A. issuer: C=US, O=Fortinet, CN=Verisign
- B. basicConstraints: CA:TRUE together with keyUsage: keyCertSign
- C. subjectAltName: DNS:*.example.com together with extendedKeyUsage: serverAuth
- D. signatureAlgorithm: SHA256withRSA together with validityPeriod: 365 days

**Answer:** B — A certificate can only sign other certificates when basicConstraints marks it CA:TRUE and keyUsage includes keyCertSign; without those flags a browser rejects it as a signing authority. The other combinations describe end-entity or cosmetic fields, not CA authority.

**185.** When forming a FortiGate high availability (HA) cluster, which setting has to be identical on every member?

- A. Group ID
- B. Web filtering cache configuration
- C. Device hostname
- D. Management interface addressing

**Answer:** A — All members must share the same HA Group ID (and group name) to form a cluster. Hostnames and management interface settings are deliberately unique per unit so each device stays individually reachable.

**186.** Which of the following is NOT synchronized between members of a FortiGate HA cluster?

- A. The HA override setting
- B. The ARP table
- C. IPsec tunnel security associations (SAs)
- D. FortiGuard signature and rating definitions

**Answer:** A — The HA override option is a per-unit setting and is intentionally not synchronized across the cluster. The ARP table, IPsec SAs (with session pickup enabled), and FortiGuard definitions are all kept in sync between members.

**187.** How is session traffic handled in an active-active cluster versus an active-passive cluster?

- A. Load is split in proportion to each unit's configured priority value.
- B. Members negotiate on a per-session basis to decide who handles each flow.
- C. Every member processes traffic while the primary distributes sessions to the secondaries.
- D. Secondaries process outbound traffic while the primary handles all inbound traffic.

**Answer:** C — In active-active, all cluster members actively process traffic and the primary load-balances sessions out to the secondaries. In active-passive, only the primary forwards traffic while the others stand by.

**188.** In the default FortiGate FGCP primary-election process, which factor is evaluated first?

- A. The configured priority value
- B. The unit's serial number
- C. The HA uptime
- D. The count of monitored interfaces that are UP

**Answer:** D — By default FGCP compares candidates in this order: most monitored interfaces UP, then HA uptime, then priority, and finally serial number. So the number of monitored interfaces in the UP state is the first tiebreaker checked.

**189.** What is the primary drawback of turning on the HA override option in a FortiGate cluster?

- A. It causes a second failover when the original primary rejoins the cluster.
- B. It stops any secondary unit from ever being promoted to primary.
- C. It makes the cluster disregard HA uptime in every failover decision.
- D. It mandates redundant heartbeat links before a failover can succeed.

**Answer:** A — With override enabled, the higher-priority unit takes back the primary role as soon as it returns, producing an extra failover and another brief traffic interruption. It does not block secondaries from being promoted or require redundant heartbeats.

**190.** An administrator is building a two-member FortiGate HA cluster and wants to reduce the risk of a split-brain condition. Which design choice most directly helps avoid it?

- A. Give each cluster member a unique HA group ID
- B. Provision two or more dedicated heartbeat links between the members
- C. Turn on FGSP alongside the default FGCP clustering
- D. Add several monitored (link-monitor) interfaces when first building the cluster

**Answer:** B — Configuring more than one dedicated heartbeat interface adds redundancy, so the loss of a single heartbeat link does not leave both units acting as primary (split-brain). Members must actually share the same group ID, so distinct IDs would break the cluster rather than protect it.

**191.** A FortiGate is deployed in transparent mode to bridge two VLAN segments. Which restriction applies to this deployment?

- A. VLANs can no longer be carried across more than one switch.
- B. Each physical port is limited to carrying a single VLAN.
- C. Antivirus and IPS scanning of transiting traffic is not possible.
- D. Layer 3 services such as SSL VPN and DHCP server are not available.

**Answer:** D — A transparent-mode FortiGate acts as a Layer 2 bridge, so it still performs antivirus, IPS, and web filtering but cannot offer Layer 3 features like SSL VPN termination or a DHCP server. Traffic inspection remains fully supported, which rules out the antivirus/IPS option.

**192.** (Choose two) When you build a DHCP server on a FortiGate interface, which two parameters are part of that configuration?

- A. A firewall subnet address object
- B. The pool of addresses to hand out
- C. The gateway clients should use
- D. A descriptive alias for the interface

**Answer:** B, C — A FortiGate DHCP server is defined by the address range it leases and the default gateway it advertises (along with netmask and DNS). A firewall address object and an interface alias are unrelated to the DHCP scope itself.

**193.** In a FortiGate static route entry, what is the meaning of the Destination field?

- A. The network or host that the route is meant to reach
- B. The FortiGate egress interface for the traffic
- C. The address of the upstream DNS resolver
- D. The address of the next-hop gateway

**Answer:** A — The destination defines the target network or host the route applies to. The next-hop gateway and the outgoing interface are configured in separate fields, and DNS is unrelated to the route match.

**194.** In an IPsec VPN, which protocol actually carries out authentication and encryption of the traffic payload?

- A. Encapsulating Security Payload (ESP)
- B. Transport Layer Security (TLS)
- C. Secure Hash Algorithm (SHA)
- D. Advanced Encryption Standard (AES)

**Answer:** A — ESP is the IPsec protocol that provides both confidentiality (encryption) and authentication of the packet payload. SHA is only a hashing function and AES is only a cipher, while TLS is used by SSL VPN rather than IPsec.

**195.** Why would an organization enable VDOMs on a single FortiGate appliance?

- A. To manage FortiSwitch units that sit in separate broadcast domains directly from FortiGate
- B. To fine-tune DNS name resolution on FortiGate virtual machines
- C. To split one physical FortiGate into several isolated virtual firewalls, each with its own policy set
- D. To bundle interfaces for link redundancy and greater aggregate throughput

**Answer:** C — VDOMs carve a single FortiGate into multiple independent virtual firewalls, each with separate policies, interfaces, and routing tables. Link aggregation and DNS tuning are unrelated features.

**196.** Which situation would keep a configured route from being installed in the FortiGate active routing table?

- A. A preferred route to the same destination already exists
- B. The wrong distance value was set on the default gateway address
- C. The interface lacks any administrative-access protocols
- D. The DHCP server tied to the route has been turned off

**Answer:** A — A route stays out of the active table when a better route (lower administrative distance or a more specific prefix) already covers the same destination, or when its interface is down. Administrative-access settings and DHCP have no bearing on route installation.

**197.** Which pair of capabilities does an IPsec VPN deliver?

- A. Network segmentation and deep packet inspection
- B. Data origin authentication and data integrity
- C. Bandwidth optimization and antireplay protection
- D. Data encryption and traffic load balancing

**Answer:** B — IPsec provides data origin authentication and data integrity, along with confidentiality and antireplay protection. Load balancing and segmentation are handled by other FortiGate features, not by the IPsec protocol itself.

**198.** You created an IPsec tunnel using the VPN wizard template, but you now need to change security settings the template does not expose. What must you do?

- A. Convert the template-based tunnel into a custom tunnel
- B. Select a different wizard template for the tunnel
- C. Start over with the custom tunnel wizard option
- D. Edit the underlying template definition directly

**Answer:** A — Converting the template-created tunnel to a custom tunnel unlocks the full set of phase 1 and phase 2 security parameters for editing. Templates themselves are not editable, and switching templates would not preserve the existing tunnel.

**199.** When a FortiGate runs in NAT mode, how are VLANs represented on its interfaces?

- A. As physical ports only, each tagged with a distinct VLAN ID
- B. As Layer 3 subinterfaces, so each VLAN can have its own routing and firewall policies
- C. Only after the connected switch has trunk ports configured first
- D. As a Layer 2 bridge that passes VLAN tags through untouched

**Answer:** B — In NAT (Layer 3) mode, a VLAN becomes a subinterface with its own IP addressing, routing, and policies. Passing VLAN tags through as a Layer 2 bridge describes transparent mode instead.

**200.** Which FortiGate feature is used to build encrypted links between a headquarters site and its branch offices across the public internet?

- A. Virtual private networks
- B. Security profile scanning
- C. Log monitoring and reporting
- D. Firewall authentication

**Answer:** A — Site-to-site IPsec VPNs create the encrypted tunnels that securely connect headquarters to branch locations over the internet. Scanning, logging, and authentication address other needs and do not build the encrypted link.

**201.** Which protocol negotiates and dynamically brings up the security associations for an IPsec VPN tunnel?

- A. Point-to-Point Tunneling Protocol (PPTP)
- B. Generic Routing Encapsulation (GRE)
- C. Internet Key Exchange version 2 (IKEv2)
- D. Layer 2 Tunneling Protocol (L2TP)

**Answer:** C — IKE (IKEv2) performs the key exchange and dynamically negotiates the IPsec security associations that form the tunnel. PPTP, GRE, and L2TP are separate tunneling protocols and do not negotiate IPsec SAs.

**202.** Why should you take regular backups of a FortiGate's system configuration?

- A. It keeps the FortiGate running at peak throughput.
- B. It lets you restore quickly and with little effort if hardware fails.
- C. It stops administrators from making unexpected configuration edits.
- D. It removes the chance of errors during a FortiOS upgrade.

**Answer:** B — A recent configuration backup allows fast restoration of settings onto replacement hardware after a failure, saving significant rebuild time. Backups do not affect throughput or prevent someone from changing the configuration.

**203.** (Choose two) Which two outcomes are benefits of routinely maintaining your FortiGate firewalls?

- A. Staying aligned with compliance and legal obligations.
- B. Lowering the likelihood of a security breach.
- C. Automatically receiving newer appliance hardware.
- D. Cutting the cost of future firmware upgrades.

**Answer:** A, B — Regular maintenance keeps the deployment compliant with legal and regulatory requirements and reduces the risk of a breach by keeping protections current. It neither supplies new hardware nor inherently lowers upgrade costs.

**204.** When moving a FortiGate to a newer firmware release, why should you follow Fortinet's recommended upgrade path?

- A. It removes the need to back up the configuration first.
- B. It unlocks brand-new major features immediately.
- C. It preserves configuration compatibility and keeps the device stable.
- D. It makes the upgrade complete more quickly.

**Answer:** C — Stepping through the recommended intermediate builds ensures the configuration is migrated correctly and the device remains stable across versions. Skipping the path risks broken settings, and it neither removes the need for backups nor guarantees speed.

**205.** On a FortiGate, one administrator should be able only to view logs while another needs full read-write configuration rights. Which mechanism enforces these differing permission levels?

- A. Enable two-factor authentication only on the full-access administrator.
- B. Assign an administrator profile that sets the access level for each account.
- C. Give each administrator a different trusted-host IP restriction.
- D. Keep one account local and place the other in a remote authentication group.

**Answer:** B — Administrator profiles grant per-feature permissions (None, Read, or Read-Write), so one profile can allow read-only log access while another grants full configuration rights. Trusted hosts, 2FA, and account location control who can connect, not what an administrator is permitted to change.

**206.** Which of the following is a recommended best practice for securing administrative access to a FortiGate?

- A. Have all IT staff log in with one shared admin account
- B. Use HTTPS rather than HTTP for GUI access
- C. Create local administrator accounts
- D. Permit administrative access only from internal network ranges

**Answer:** B — Using encrypted management protocols such as HTTPS (and SSH in place of Telnet) keeps administrator credentials from traveling in cleartext. Shared accounts actually weaken accountability, and simply creating local accounts is not by itself a security control.

**207.** (Choose two) Beyond CPU and memory utilization, which two additional metrics are worth monitoring on a FortiGate for performance and load?

- A. The count of active VPN tunnels
- B. The count of SSL sessions
- C. The number of configured local users and groups
- D. The number of days until licenses expire

**Answer:** A, B — Active VPN tunnels and SSL sessions reflect real-time processing load and are useful performance indicators. Local-user counts and license expiry are inventory or lifecycle facts, not live performance measurements.

**208.** What advantage comes from creating individual administrator accounts on a FortiGate instead of sharing one?

- A. It improves accountability by tracing changes to a specific administrator.
- B. The built-in admin account cannot use two-factor authentication.
- C. New accounts can enforce password rules the default account cannot.
- D. New accounts can select stronger encryption than the default admin account.

**Answer:** A — Separate named accounts create an audit trail, so each configuration change can be attributed to the administrator who made it. The other statements are not true of FortiGate accounts, since 2FA, password policy, and encryption apply regardless of which account is used.

**209.** Which pair of protocols is appropriate for administrative access on a FortiGate interface?

- A. Telnet and Simple Network Management Protocol (SNMP)
- B. Simple Mail Transfer Protocol (SMTP) and Secure Sockets Layer (SSL)
- C. Remote Desktop Protocol (RDP) and Hypertext Transfer Protocol (HTTP)
- D. Hypertext Transfer Protocol Secure (HTTPS) and Secure Shell (SSH)

**Answer:** D — HTTPS for the GUI and SSH for the CLI are the encrypted administrative-access options enabled in an interface's allowaccess list. Telnet, HTTP, and the other choices are either insecure or not used for FortiGate administration.

**210.** (Choose two) What are two consequences if a FortiGate's FortiGuard/support license is allowed to lapse?

- A. The GUI can no longer display system logs or build network reports
- B. Loss of security-service updates and access to technical support
- C. The appliance runs slower and becomes inherently more vulnerable
- D. Interruption of protected services and possible compliance or legal exposure

**Answer:** B, D — An expired license cuts off FortiGuard update feeds and vendor technical support and can interrupt licensed services while creating compliance gaps. Local logging still works, and the hardware's raw performance is not reduced simply because a license lapsed.

**211.** Which of these passwords would satisfy the strong-password policy used in recent FortiOS releases?

- A. FortinetSECURE2026
- B. SecureNet#2026
- C. Cloud26!
- D. Summer2025!

**Answer:** B — 'SecureNet#2026' meets a strong policy by being at least 12 characters and mixing uppercase, lowercase, a digit, and a special character. The other choices each fall short, either lacking a special character or not reaching the required length.

**212.** Which FortiSwitch details does a FortiLink discovery frame advertise to the FortiGate?

- A. VLAN IDs and LLDP capability data
- B. Firmware version and bridge priority values
- C. Host name and the full MAC address table
- D. Serial number and port information

**Answer:** D — FortiLink discovery frames announce the FortiSwitch serial number and its ports so the FortiGate can identify and authorize the switch for management. VLAN, firmware, and MAC-table details are exchanged later, not in the discovery frame.

**213.** In a standalone FortiGate managing dual-homed FortiSwitch access switches, what does an MCLAG accomplish?

- A. It stops split-brain conditions from occurring.
- B. It makes two FortiSwitch units appear to downstream devices as one logical switch.
- C. It spreads CAPWAP tunnels across multiple VLANs.
- D. It performs firmware upgrades on all FortiSwitch units at the same time.

**Answer:** B — MCLAG lets a pair of FortiSwitch units present themselves as a single logical switch, so a downstream device can connect to both for link and switch redundancy. Split-brain prevention and simultaneous firmware upgrades are not the purpose of MCLAG.

**214.** Which protocol provides the authenticated, secured management channel between a FortiGate and a managed FortiSwitch?

- A. FortiLink
- B. LLDP
- C. HTTPS
- D. CAPWAP

**Answer:** D — CAPWAP forms the DTLS-secured management tunnel through which the FortiGate authenticates and controls the FortiSwitch. FortiLink is the overall management feature that relies on that CAPWAP tunnel, while LLDP only assists with neighbor discovery.

**215.** Why would an administrator enable the split-interface option on a FortiLink aggregate?

- A. So the FortiLink aggregate interface can connect to more than one FortiSwitch
- B. So heartbeat traffic is no longer needed in the FortiLink topology
- C. So FortiSwitch units drop to standalone mode whenever the FortiGate is offline
- D. So a single VLAN can be stretched across two FortiGate devices

**Answer:** A — The FortiLink split interface splits the aggregate so its member links can terminate on two different FortiSwitch units, giving a redundant dual-homed connection. It does not disable heartbeats or change how the switches behave when the FortiGate is down.

**216.** Which statement best captures the role FortiLink plays within the Fortinet Security Fabric?

- A. It is a paid add-on protocol used only for managing remote FortiSwitch units.
- B. It integrates FortiSwitch into the LAN whether or not a FortiGate is present.
- C. It permits up to 500 FortiSwitch units to be joined to the Security Fabric.
- D. It lets a FortiGate manage FortiSwitch units directly, extending centralized security to the switch layer.

**Answer:** D — FortiLink allows the FortiGate to manage FortiSwitch units directly, bringing the access switching layer under the same centralized Security Fabric policy and control. FortiLink specifically depends on a managing FortiGate and is not a separate paid remote-only protocol.

## Validation and Troubleshooting

**Scoring.** Score single-answer items as correct only for the exact
option; score multi-select items as correct only when the selected set
matches the key exactly — no partial credit, mirroring the assessment.

**Readiness thresholds.** Aim for **≥ 85 % in every domain**, not just an
85 % average. A domain sitting below 70 % is a fail risk on its own; bring
it up before sitting the assessment. Two consecutive clean passes of a
weak set — several days apart — is a better readiness signal than one
lucky run.

**Remediation mapping.** A weak domain maps to concrete work:

- Security Fabric / FortiCare misses → re-read
  [Chapter 03](03-nse-3-security-fabric-and-fortigate-operator-foundations.md)
  and redo the registration and Fabric-topology steps in
  [Chapter 04](04-fortigate-first-deployment-licensing-management-and-hardening.md).
- Policy, NAT, or authentication misses → redo the policy and
  authentication labs in
  [Chapter 06](06-firewall-policy-authentication-vpn-and-zero-trust-access.md).
- SSL-inspection or web-filter misses → revisit certificate versus deep
  inspection in
  [Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md).
- Routing, VLAN, VDOM, or HA misses → rerun the interface, routing, and
  FGCP labs in
  [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md).

**Common operator misconceptions to check yourself against.**

- `show` prints only non-default settings; `get` prints the full
  effective configuration. An empty `show ... | grep` usually means *at
  default*, not *unset*.
- SSL **certificate inspection** identifies the site from the certificate
  and SNI without decrypting; **deep inspection** decrypts and re-signs,
  so clients must trust the FortiGate CA.
- Every policy set ends in an **implicit deny** (policy ID 0); traffic
  that matches no policy is dropped and logged against it.
- In an FGCP cluster the running configuration synchronizes, but the
  **HA override** setting and truly device-local values do not.

## Security and Best Practices

- Give day-to-day operators a **read-only or least-privilege access
  profile** and pin their accounts to **trusted-host** subnets; reserve
  `super_admin` for change windows.
- **Back up the configuration** (and note the running firmware) before
  any change, so a bad edit is one restore away.
- Reach for **read-only diagnostics first** (`get`, `diagnose`,
  `execute log display`) before changing anything, and confirm the
  effect with `get` afterwards.
- Resolve the browser certificate warning by **installing a trusted
  certificate**, not by teaching users to click through warnings.
- Enable **Log Allowed Traffic** deliberately — *All Sessions* is
  invaluable while troubleshooting but noisy as a permanent default;
  return it to *Security Events* when the investigation ends.

## References and Knowledge Checks

- Fortinet Training Institute — FortiGate 7.6 Operator learning path and
  assessment (credential overview and exam domains).
- Volume XIX, [Chapters 01–15](../README.md)
  — the source material every practice item is built from.
- The [interactive self-check companion](../../interactive/fortigate-operator-quiz.html)
  — the answer-hidden version of the bank in this chapter.

Knowledge checks:

1. Given a FortiGate you have never seen, which two read-only commands
   most quickly tell you the firmware version, serial number, uptime, and
   current resource load?
2. A colleague reports that `show system global | grep timezone` returns
   nothing. What does that most likely mean, and how do you confirm the
   actual value?
3. A policy is configured but its traffic never appears under Forward
   Traffic logs. Name two independent settings that could explain it.
4. You must let a helpdesk technician read logs and dashboards from the
   office subnet only, with no ability to change configuration. Which two
   objects do you create, and what do you set on each?
5. Explain, in one sentence each, when you would choose certificate
   inspection over deep inspection and vice versa.
6. After a failover you find one cluster member had a different HA
   override value than the other. Why did that value not synchronize?

## Hands-On Lab

These seven labs walk the core operator tasks demonstrated across the
FortiGate 7.6 Operator training — console bring-up, dashboard review,
basic networking, administration, logging, and authentication — as
reproducible procedures. Each gives the GUI navigation and, where it
applies, the equivalent FortiOS 7.6 CLI, with expected output, a negative
test, and a rollback. Every lab ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 16.1–16.7** — a FortiGate on FortiOS 7.6
(the evaluation FortiGate-VM is sufficient) reachable over its console and
a management interface, and a client host with a browser on a connected
segment. **Cost:** none beyond the appliance/VM.

### Lab 16.1 — Console boot, first login, and CLI status verification (Topic: CLI access and status)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation
FortiGate-VM as-is.

**Objective:** Reach the CLI over the console, complete the forced
first-login password change, and read core system status.

Connect a terminal to the console at **9600 baud, 8 data bits, no parity,
1 stop bit, no flow control**. Log in as `admin` with an empty password;
FortiOS forces a password change on first login. Then read status:

```text
get system status
get system performance status
diagnose ip address list
```

**Expected result:** `get system status` reports `Version: FortiGate-VM64
v7.6.x`, the serial number, and the hostname; `get system performance
status` shows CPU, memory, and uptime; `diagnose ip address list` prints
the management interface's IP. The box is now reachable and identified
without a single configuration change.

**Negative test:** at the password prompt, enter a new password that is
too short or reuses the blank one — FortiOS rejects it and re-prompts,
proving the first-login change is mandatory and complexity-checked.

**Rollback:** none — the lab is read-only apart from setting the initial
admin password, which is required to use the device at all.

### Lab 16.2 — GUI dashboard and system status review (Topic: GUI navigation)

**Eval FortiGate — capable.**

**Objective:** Log into the GUI and locate the operator's core status
widgets, cross-checking them against the CLI.

Browse to `https://<mgmt-ip>` and acknowledge the browser certificate
warning — it is **expected** on a factory device presenting a self-signed
certificate (Lab 16.5 and Chapter 04 cover replacing it). Log in, then on
**Dashboard > Status** identify:

- **System Information** — hostname, serial, firmware, and uptime.
- **Licenses** — FortiCare and FortiGuard reachability (green when
  registered and reachable, grey when not).
- **Administrators** — who is currently logged in and by which method.
- **Security Fabric** — the device's Fabric role and topology.

Open the built-in CLI console with the **`>_`** icon (top-right) and run
`get system status`.

**Expected result:** the serial number and firmware in the System
Information widget match the CLI output from Lab 16.1 exactly — the GUI
and CLI are two views of one configuration.

**Negative test:** if an administrator trusted-host range is configured
(Lab 16.5), browse from a host outside that range — the login page does
not load, proving trusted hosts gate management access ahead of
authentication.

**Rollback:** none — read-only.

### Lab 16.3 — Interface, DHCP server, and administrative access (Topic: Basic networking)

**Eval FortiGate — capable**, but mind the eval's **3-interface budget**
(Chapter 04): reuse an existing data port rather than adding a new one.

**Objective:** Give a LAN interface an address and administrative access,
serve DHCP from it, and verify a lease.

In the GUI: **Network > Interfaces**, edit the chosen port — set an
**Alias** (`LAN-HQ`), **Role** `LAN`, **Addressing mode** Manual,
`172.16.10.1/24`, tick **HTTPS** and **PING** under Administrative
Access, then enable **DHCP Server** and set an address range. The
equivalent CLI:

```text
config system interface
    edit port3
        set alias LAN-HQ
        set role lan
        set mode static
        set ip 172.16.10.1 255.255.255.0
        set allowaccess ping https
    next
end
config system dhcp server
    edit 1
        set interface port3
        set default-gateway 172.16.10.1
        set netmask 255.255.255.0
        config ip-range
            edit 1
                set start-ip 172.16.10.100
                set end-ip 172.16.10.200
            next
        end
    next
end
```

**Expected result:** `get system interface port3` shows the address and
`allowaccess: ping https`; a client on that segment receives a lease in
`172.16.10.100–.200`, visible with `execute dhcp lease-list port3`.

**Negative test:** remove `https` from `allowaccess` and try to open the
GUI on that interface — the connection is refused; re-add `https` and it
succeeds, showing admin access is per-interface.

**Rollback:**

```text
config system dhcp server
    delete 1
end
config system interface
    edit port3
        unset alias
        set allowaccess ping
    next
end
```

### Lab 16.4 — A static default route and reading the routing table (Topic: Static routing)

**Eval FortiGate — capable** (mind the 3-route budget).

**Objective:** Add a default route toward the WAN gateway and read how it
installs.

In the GUI: **Network > Static Routes > Create New** — Destination
`0.0.0.0/0.0.0.0`, Gateway `172.16.20.2`, Interface (WAN port),
Administrative Distance `10`. The CLI:

```text
config router static
    edit 1
        set dst 0.0.0.0 0.0.0.0
        set gateway 172.16.20.2
        set device port2
        set distance 10
    next
end
get router info routing-table all
```

**Expected result:** the routing table shows
`S*      0.0.0.0/0 [10/0] via 172.16.20.2, port2` — a default static
route (`S`), selected as the gateway of last resort (`*`).

**Negative test:** change the gateway to an address that is not on the
interface's subnet. The route still **installs** (the interface is up),
but forwarding through it fails because the gateway's ARP goes
unanswered — installation and reachability are different things.

**Rollback:**

```text
config router static
    delete 1
end
```

### Lab 16.5 — Administrator accounts and access profiles (Topic: Administration)

**Eval FortiGate — capable.**

**Objective:** Create a least-privilege, read-only administrator scoped
to a trusted subnet.

In the GUI: **System > Admin Profiles > Create New** — name
`ro_operator`, set the relevant permission groups to **Read** (for
example System, Log & Report, and Firewall). Then **System >
Administrators > Create New** — Type Local, assign `ro_operator`, set a
**Trusted Host** of `172.16.10.0/24`, and a password. The CLI:

```text
config system accprofile
    edit ro_operator
        set sysgrp read
        set loggrp read
        set fwgrp read
    next
end
config system admin
    edit operator1
        set accprofile ro_operator
        set trusthost1 172.16.10.0 255.255.255.0
        set password ENC-OR-PLAINTEXT
    next
end
```

**Expected result:** `operator1` logs in from `172.16.10.0/24` and sees a
read-only GUI — status and logs are visible, but create/edit controls are
absent or greyed out.

**Negative test:** as `operator1`, attempt any configuration change — the
CLI returns a permission error and the GUI blocks it; then log in from a
host **outside** `172.16.10.0/24` — the login page is unreachable.

**Rollback:**

```text
config system admin
    delete operator1
end
config system accprofile
    delete ro_operator
end
```

### Lab 16.6 — Viewing and filtering traffic logs (Topic: Logging and monitoring)

**Eval FortiGate — capable** (logs to memory/disk on the VM).

**Objective:** Turn on allowed-traffic logging for a policy, generate
traffic, and filter the forward-traffic log.

Enable full logging on the relevant policy, then browse from a client to
generate sessions, and inspect the log:

```text
config firewall policy
    edit 1
        set logtraffic all
    next
end
```

In the GUI: **Log & Report > Forward Traffic**. Add a filter from the
filter bar (or right-click a cell → *Filter*) — for example **Source**
`172.16.10.100`, or **Action** `Deny` to isolate blocked sessions. Click
an entry to open its detail pane, which links out to FortiGuard for any
matched category. The CLI equivalent for reading logs:

```text
execute log filter category 0
execute log display
```

**Expected result:** filtered forward-traffic entries appear; a denied
session with no matching policy is logged against **policy ID 0**, the
implicit-deny rule.

**Negative test:** set the policy's logging back to `utm` (or disable it)
— allowed sessions stop appearing under Forward Traffic until logging is
re-enabled, confirming that allowed-traffic visibility is opt-in
per policy.

**Rollback:** restore the policy's original `logtraffic` value (commonly
`utm`).

### Lab 16.7 — Firewall authentication with a local user and group (Topic: Authentication)

**Eval FortiGate — capable.**

**Objective:** Require user authentication on a firewall policy using a
local user and a firewall user group.

In the GUI: **User & Authentication > User Definition** — create a local
user (username and password). **User & Authentication > User Groups** —
create a **Firewall** group and add the user. **Policy & Objects >
Firewall Policy** — edit the outbound policy and add the group under
**Source** (user/group). The CLI:

```text
config user local
    edit auth_user
        set type password
        set passwd ENC-OR-PLAINTEXT
    next
end
config user group
    edit auth_grp
        set member auth_user
    next
end
config firewall policy
    edit 1
        set groups auth_grp
    next
end
```

**Expected result:** a client matching the policy is challenged for
credentials (captive portal) before any traffic passes; after a
successful login, `diagnose firewall auth list` shows the authenticated
user, source IP, and group.

**Negative test:** supply wrong credentials — traffic stays blocked and
no entry appears in `diagnose firewall auth list`, proving the policy
fails closed.

**Rollback:**

```text
config firewall policy
    edit 1
        unset groups
    next
end
config user group
    delete auth_grp
end
config user local
    delete auth_user
end
```

## Lab Verification

Complete this sign-off once the labs have been run end to end, including
the negative tests. Until then, the labs are unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter turned Volume XIX's operator material into a readiness check:
an eight-domain map from the FortiGate 7.6 Operator assessment back to the
chapters that teach each domain, a self-assessment tracker, an original
216-item practice bank with an answer key (mirrored by an interactive,
offline self-check companion), and seven operator hands-on labs covering
console bring-up, dashboard review, basic networking, administration,
logging, and authentication. Work the weak domains against the earlier
chapters until every domain clears the readiness threshold.

- [ ] Can map each operator assessment domain to the Volume XIX chapters
      that cover it.
- [ ] Scored every domain in the practice bank at or above the readiness
      threshold, on two separate attempts.
- [ ] Can reach the CLI over the console and read system status without
      changing configuration.
- [ ] Can configure an interface, DHCP server, and administrative access,
      and verify a client lease.
- [ ] Can add and read a static default route, and explain install versus
      reachability.
- [ ] Can create a least-privilege, trusted-host-scoped administrator.
- [ ] Can enable, generate, and filter forward-traffic logs, and identify
      the implicit-deny policy.
- [ ] Can require authentication on a policy with a local user and group.
- [ ] Completed the hands-on labs, including the negative tests.
