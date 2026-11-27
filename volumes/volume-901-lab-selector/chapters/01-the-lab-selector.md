# Chapter 01: The Lab Selector

## Learning Objectives

- Say what the Lab Selector is, and what it gives you for the labs you choose.
- Name the three kinds of labs, and the lab sets that have labs today.
- Choose lab sets, plan the labs of each one, and match the machines of the build to them.
- Write a link that opens the page with lab sets ticked, and say what the page does with it.
- Tell the machines that the scripts build from the hosts that you build by hand.
- Change the platform, the addresses, and the other options of a build, and read what changed.
- Hand the zip to Claude, and read the progress of the labs back into the page.

## Theory and Architecture

### What the Lab Selector is

The [Lab Selector](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html) is one HTML page that runs in your browser. You choose the labs you want to run, the platform the lab machines will run on, and what to build. The page then writes four things for that build:

- **A manifest:** the copy of `lab201-vms.json` that holds your changes. The build scripts read it.
- **The commands:** the lines to run for your platform, from the readiness check to the baseline snapshots.
- **A checklist:** what to do before and after the build, and what the scripts cannot do.
- **The lab walkthroughs:** the lab chapters of the labs you chose, rewritten with the values of your build.

A zip button bundles them with the script of your platform, the seed tool, the flavor catalog, the image resolver, and a picture of the build. Nothing you type leaves the page, and the page works with no server, because it carries its data in itself.

The page was the Lab Builder of [Volume CCI](../../volume-201-fortiswitch-stig-and-srg-mapping/README.md) until 2026-11-20. It built for one set of labs, the FortiSwitch requirement labs. It now offers the labs of more than one volume, so it moved to this volume together with its data and the build scripts. [Chapter 90](90-as-built-how-this-volume-was-built.md) records the move.

### Lab kinds and lab sets

The first card of the page is **Labs**. It asks two things:

1. **The kind of labs.** The page has three kinds: **SRG labs**, **certification labs**, and **learning labs**. A kind can be chosen only when it has a lab set. Today the SRG labs have lab sets, and the other two kinds show *none yet*.
2. **The lab sets.** A lab set is the labs of one volume. Tick each lab set you want to build for. A new build has the FortiSwitch lab set, which is what the Lab Builder always built.

| Lab set | Volume | Requirement labs | Runs on | Hosts that no script builds |
| --- | --- | ---: | --- | --- |
| FortiSwitch | CCI | 41 | Two FortiSwitch units, which are hardware | None. The optional console server labs of its Chapter 08 need a console server |
| FortiAnalyzer | CCII | 17 | `faz-202`, a FortiAnalyzer-VM | `faz-202`, `fgt-202`, `mail-202`, and the optional `faz-202b` |
| FortiManager | CCIII | 17 | `fmg-203`, a FortiManager-VM | `fmg-203`, and three hosts of the FortiAnalyzer lab set: `fgt-202`, `mail-202`, and the optional `faz-202` |

The FortiSwitch labs prove 185 requirements, the FortiAnalyzer labs prove 65 requirements, and the FortiManager labs prove 79 requirements. The page takes these numbers from the lab chapters, so they change when a chapter does.

Certification labs and learning labs will be added as lab sets of their own kind. [Chapter 02](02-lab-data-and-how-to-add-a-lab-set.md) describes how.

### The shared lab and what a lab set adds

Every lab set runs on the **shared lab**: the gateway, the VLANs, and the service hosts of [Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md). The scripts of this volume build its twelve machines, and Volume CCI, Chapters 09 to 14 explain each platform. A chapter number that this chapter gives without a volume is a chapter of Volume CCI.

A lab set adds to the shared lab in three ways:

- **Labs.** Its requirement labs join the lab plan, and the page keeps the machines that those labs name. The two labs that build the shared lab, Labs 999.1 and 999.2, are in every build. Labs 999.3 to 999.6 prepare the switches, so they belong to the FortiSwitch lab set.
- **Hosts that no script builds.** The FortiAnalyzer and FortiManager lab sets need virtual machines whose images come from the vendor under a license, and a mail server. No script can download those images, so you build these hosts by hand, in the labs of the Chapter 999 of the lab set. The page lists each one under **Machines and sizes** with its address in your build, the lab sets that need it, and the walkthrough that builds it. A host that only one optional step needs is marked *optional*.
- **Lab chapters.** The zip holds the lab chapters of the lab sets you ticked, after the chapter of the shared lab.

The hosts of the FortiAnalyzer and FortiManager lab sets are on the Lab-Services segment of the shared lab, at `10.200.0.54` to `10.200.0.58`, so no lab set needs a segment of its own yet. The page takes the hosts from the **Address plan** table of each Chapter 999, through the sync script. That script reports a host whose address is in no network of the shared lab, because the page could not place such a host.

A lab of another volume can have the number of a FortiSwitch lab: Volume CCI and Volume CCII both have a Lab 4.1. In the page, in `PROGRESS.md`, and in the evidence folders, a lab of a lab set other than FortiSwitch therefore has the prefix of its lab set before its number, such as `faz-3.1` and `fmg-2.4`. Its walkthrough has the same prefix in its file name.

### Links that tick lab sets

A link can name the lab sets that the page starts with. Add `?sets=` and the id of a lab set to the address of the page, or several ids with commas between them:

| Link | The page starts with |
| --- | --- |
| [`?sets=fortiswitch`](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortiswitch) | The FortiSwitch labs |
| [`?sets=fortianalyzer`](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortianalyzer) | The FortiAnalyzer labs |
| [`?sets=fortimanager`](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortimanager) | The FortiManager labs |
| [`?sets=fortianalyzer,fortimanager`](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/downloads/volume-901-lab-selector/lab-scripts/selector/lab-selector.html?sets=fortianalyzer,fortimanager) | The FortiAnalyzer and FortiManager labs |

The ids are the ones of the catalog ([Chapter 02](02-lab-data-and-how-to-add-a-lab-set.md)), in any case. The README and the Chapter 999 of Volumes CCII and CCIII have such a link, and so have the README of Volume CCI and the portal page of each of the three volumes. The **Labs** card shows the link for the lab sets of your build, so you can keep it or pass it on.

A link does this:

- **On a build with no kept choices,** it ticks exactly the lab sets it names, and it matches the machines to the labs of those sets, as the button in section 5 does.
- **On top of choices that the browser kept,** it changes the lab sets only. Your machines stay, and the note in section 5 says whether they match the new labs.
- **It says what it did,** in a line under the lab sets. A name that the page does not know is named there and left out, and a link with no known name changes nothing.
- **It counts once.** The page keeps the result like any other choice, and takes the `sets` part out of its address. A reload therefore shows what the link set, and it does not undo what you chose afterward.

### The plan of the lab network

The lab network is `10.200.0.0/16`, with the unique local IPv6 prefix `fd00:db8:201::`. The page gives each lab network a block of its own size from the first address of its supernet, a /28 unless the network needs another size, so a full FortiSwitch build takes `10.200.0.0/22`, which is the plan that Volume CCI's Chapter 999 prints. Until 2026-11-24 every lab network was a /24, and a full build took a /20. Until 2026-11-20 the plan was `10.201.0.0/16`. A choices file from before 2026-11-24 loads, and it keeps its block, its VLAN IDs, and its lab sets. Its subnets and most of its addresses are new, so a lab that was built from it has other addresses than the page shows, and the page says so when it loads the file.

A build with no FortiSwitch labs needs fewer networks: the out-of-band network and the seven shared segments. The networks that only the switch labs use, such as the routed links and the FortiLink network, take no subnet then.

## Design Considerations

- **One page, no server.** The page carries the manifest, the flavor catalog, the lab data, and the switch feature data in itself. It has to be opened from the published site only for the zip, because a page opened from a local file cannot fetch the scripts and the lab chapters.
- **The lab chapters are the source.** The labs, the machines a lab uses, its SRG requirements, and the hosts of a lab set come from the lab chapters, through `scripts/python/sync_lab_selector.py`. Nothing about a lab is typed into the page by hand.
- **A new build is the build of the book.** With the FortiSwitch lab set alone and no other change, the build is the plan of Volume CCI's Chapter 999, and the walkthroughs in the zip match the chapters.
- **The scripts build what they can test.** The vendor images of a FortiAnalyzer-VM, a FortiManager-VM, and a FortiGate-VM need your own vendor account, so no script builds those hosts. The page lists them and does not size them: take the size from the installation guide of the vendor.
- **A lab set changes no machine by itself.** Ticking a lab set changes the lab plan. The page then names the machines that the plan does not use, and **Match the machines to these labs** leaves them out when you click it.
- **Switch choices matter only with switch labs.** The switch models, the FortiSwitchOS release, and the switch ports change nothing in a build that has no FortiSwitch labs, and the page says so in that section.

## Implementation and Automation

### The cards of the page

The page has the **Labs** card and eleven numbered sections:

| Card | What you set |
| --- | --- |
| Labs | The kind of labs, the lab sets, and the labs of each set that you plan to run |
| 1 and 2 | The platform and its version: ESXi, vCenter, Dell VxRail, Workstation Pro, Proxmox VE, KVM, or WSL |
| 3 | The Windows user name, and the names of your hosts, storage, and network connections |
| 4 | The Linux flavor of the machines, and the passwords |
| 5 | The lab name, the machines, their names, sizes, and addresses, and the list of the hosts that no script builds |
| 6 | The supernet, the subnets, the VLAN IDs, and the IPv6 prefix, with a table of the supernet and of every lab network of the build, from the first subnet on |
| 7 | The two switch models, the FortiSwitchOS release, the switch ports, and the lab that Claude starts with |
| 8 | The images that you supply |
| 9 | Where you keep each license |
| 10 and 11 | The gateway of the lab, with the two ports of a network device that is the gateway, and the rules for an external firewall, with the interfaces and the gateway address that the rules name |

The right side shows the result in tabs: the commands, the manifest, the checklist, the changes, the license file, the instructions for Claude, the progress, and the diagram.

### What you can change

- **Lab sets and hosts built by hand.** Tick the lab sets in the **Labs** card. Section 5 then lists the hosts that no script builds, with the address of each one in your build. The address follows the supernet, the subnets, and the IPv6 prefix of section 6. The page warns when you give a machine the address of such a host. `LAB-VALUES.md`, `CHECKLIST.md`, and `CLAUDE.md` in the zip list the same hosts, and the license section adds a line for the virtual machines of a vendor.
- **Machines.** Leave any machine out (the gateway always stays), rename it, and change its vCPUs, memory, and disk. Each machine has a proposed minimum size, and a value below it is refused, with the default kept, unless you tick that machine's **Override** box. The minimums are the `min` values in the manifest. They are proposals, and each needs a test build before you rely on it.
- **Names.** A name uses lowercase letters, digits, and hyphens, and must be unique. The scripts find the gateway by its `role`, not its name, so it can be renamed. Chapter 999 and the requirement labs use the default names, so keep a note of your renames.
- **Lab name.** Section 5 has a **Lab name** field, `201` by default. Another name, 1 to 5 lowercase letters and digits, renames everything the build writes. `lab201` becomes `lab<name>`: the networks, the files and services inside the machines, the folders, the manifest, and the zip. `LAB201_` and `Lab201` follow, in the environment variables and the script names. The machines, the service names, and the snapshot end in it, such as `gw-305`, `radius-305a`, and `baseline-305`, and the machine table shows those names. Lab numbers, the IPv6 prefix, and links keep their text, and the IPv6 prefix has its own field in section 6. Five characters keep the longest machine name, `mcast-src-<name>`, within the 15 characters of a Windows computer name. The chapters use 201, and the walkthroughs in the zip use the name of the build. The page keeps the 201 names inside and renames what it writes, so a build named 201 is the same as before.
- **Linux flavors.** A default flavor for every machine, and a flavor for each machine. A flavor that cannot run a machine type is left out of that machine's list, with a note that names what was left out. See *Linux flavors* in Volume CCI, Chapter 09.
- **Supernet, subnets, VLAN IDs, and addresses.** The **IP addressing** section has one **Supernet** field for IPv4. It holds the block of the lab, the address where its subnets start, and its size, such as `10.77.64.0/22`. The page picks `10.200.0.0/22`, the plan of Chapter 999. Tick **Override** to type another private network, with or without a size: without one, the page picks the smallest block that starts there and holds the subnets. A unique local IPv6 prefix has a field of its own. Each network of the Segments table in Chapter 999 has the size that the table gives it: a /28, which has 14 host addresses, unless the network needs another size. Lab-Services is a /27, the two networks that the routing peers advertise are a /24 each, and FortiLink is a /30. The page places the networks of a build in two steps. The out-of-band network and the shared segments are in every build, so they come first, one after the other, and have the same blocks in every build. Each other network that the build uses then takes the lowest free block of its size, so the supernet stays small. A full build uses 16 of them, which fit `10.200.0.0/22`, and it is the plan that Chapter 999 prints: segment 2 is VLAN 2 and `10.200.0.32/27`. The row **Subnets** under the supernet says how many subnets the build has and of which sizes. The table of the section starts with a row for the supernet, with its first and its last address: in the plan of Chapter 999 that is `10.200.0.0/22`, `10.200.0.0` to `10.200.3.255`. The Segments table of Chapter 999 starts with the same row. Under it the table has a row for every network of the build, in the order of their addresses, so the networks start at the first subnet of the lab: in the plan of Chapter 999 that is OOB-Mgmt, `10.200.0.0/28`. A shared segment, 2 to 8, has fields for its subnet and its VLAN ID in its row, and the page places every other network. The rows stay where they are while you work in the table, and a segment whose subnet you set moves to the place of its address when you leave the table. A VLAN ID is the number of its segment, wherever the subnet of the segment lies: in `10.77.64.0/22` the Lab-Services segment is `10.77.64.32/27` and still VLAN 2. Tick **Override** beside a VLAN ID to type another one. The VXLAN tenant network keeps VLAN 13 and VNI 13. A host has a host number, which is its place in the block of its segment. Its IPv6 address is the prefix, the number of the segment, and the host number, so the IPv6 addresses do not change when a subnet moves. A network that only labs left out of the plan use takes no subnet, and a network that is not in every build can then take another block, so settle the lab plan before you build. Tick **Set subnet** on a shared segment to type another private block of the same size, and the page places the other networks around it. Change a machine's address inside its own segment in the machine table. The manifest holds the prefixes (`ipv4_prefix`, `ipv6_prefix`), the block of every lab network of the build (`segments`), and a map from each changed VLAN to its segment (`vlan_segments`). `make-seed.py` takes the segment and the host number of every address from that list, and with them the IPv6 addresses, the gateway's VLAN interfaces, and its firewall sets. The page refuses a VLAN ID that is reserved, used twice, or out of range, a supernet that is not private or that cannot start where you put it, a subnet that is not a block of the size of its segment or that overlaps another one that you set, and an address that is outside its segment, used twice, or the gateway's. It writes a `CHANGES.md` that lists every subnet and VLAN ID that differs from the one in the chapters, and what else to repeat on the switches.
- **The size of the supernet.** The page counts the subnets of the build and picks the smallest supernet that holds them. To leave room for more, type a supernet with a larger size, such as `10.200.0.0/21`. A supernet whose size you set is used as it is, and the page warns when it does not hold a subnet of the lab. Its first address has to be one where a block of that size can start, and the page names the nearest ones when it is not. The external firewall uses the supernet, and the walkthroughs in the zip name it where the chapters name `10.200.0.0/16` or `10.200.0.0/22`. Until 2026-11-24 the section had a field for the number of subnets. A choices file that set one loads without it, and the page says so.
- **Switch models.** The FortiSwitch labs were written for an FS-648F-FPOE and an FS-2048F. Pick or type the two models you have. The page derives each switch's host name from its model (`sw-424e-1` for an FS-424E-FPOE) and warns that features differ between model series. Models of the FortiSwitch Rugged line (`FSR-`) are accepted too.
- **FortiSwitchOS release and feature support.** Pick FortiSwitchOS 7.6.7, 8.0.0, or 8.0.1. The default is 7.6.7, because the lab chapters cite the FortiSwitchOS 7.6.7 CLI Reference. With another release, each walkthrough in the zip names that release where the chapter expects 7.6.x, keeps what the chapter cites, and says that the commands and page numbers still come from the 7.6.7 reference. For the release you pick, the page shows which of 39 lab features each of your two models supports, and which planned labs use a feature on a switch that lacks it. It also shows what changes for your two models between the three releases. The data is `lab-scripts/common/fortiswitch-features.json`, which `scripts/python/build_fortiswitch_features.py` reads from the text of Fortinet's Feature Matrix PDF for each release. The matrix marks a supported cell with an icon that the text does not carry, so the script reads a cell as supported unless it holds `--`, and it stops if a cell does not line up with a column. The 39 rows were then compared with the pages of the 7.6.7 and 8.0.1 matrices, and they agree. The 8.0.0 data is the same as the 8.0.1 data for these features, and its pages were not compared. One difference between 7.6.7 and the 8.0 releases matches the 8.0.0 release notes, which add IP source guard on the FS-1024E, FS-T1024E, FS-T1024F-FPOE, and FS-2048F. The page reads the switch of each lab from the lab's **Uses** line (`sw-648f-1`, `sw-2048f-1`, or both), so Lab 4.5 counts for the aggregation switch only. A lab whose Uses line names no switch counts for both. Two limits remain. The matrix lists model series, not every model. A lab is tied to a feature by keywords in its text, so the list of labs is a guide. Check the matrix for your exact model ([Volume CCI, Chapter 01](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/01-fortiswitch-feature-version-and-srg-map.md), prerequisite P9).
- **Lab walkthroughs in the zip.** The zip holds a copy of the lab chapters this build is for: the chapter of the shared lab, and the lab chapters of the lab sets you chose. For the FortiSwitch lab set they are the requirement labs in Chapters 04 to 08. Each copy is rewritten with the values you chose: the address block, the segment subnets, the VLAN IDs, the machine names and addresses, and the switch models and host names. The first row of the Segments table in the copy of Chapter 999 is the supernet of your build, with its first and its last address. `LAB-VALUES.md` lists those values in one place. The rewrite follows the patterns the chapters use (`VLAN 5`, `set vlanid 5`, `vlan5`, and the lab addresses), so read a changed step against `LAB-VALUES.md` before you run it. `lab-scripts/common/lab-catalog.json` names the chapters, and the site build publishes them beside the scripts. A chapter of a lab set other than FortiSwitch is rewritten against its own volume, and a statement about the switches or their release is left as it is there.
- **Passwords.** Section 4 has a **Lab password**, which the page proposes, and a field for each password a build uses: the console and `sudo` password of `labadmin` (`LAB201_CONSOLE_PASSWORD`), the passphrase of the SSH key, the Windows admin password (`LAB201_WINDOWS_ADMIN_PASSWORD`, shown when a Windows flavor is used), and the password of the hardened flavors (`LAB201_ADMIN_PASSWORD`, shown when one is used). Each field starts with the lab password and follows it until you type another value there. The SSH key passphrase starts empty and follows nothing. Tick **Prompt when the script runs** beside a field, and the commands leave its line out: the build asks for it with hidden input when `make-seed.py` writes the seeds. The commands name the passwords to ask for in `LAB201_PROMPT`. The console password works at a machine's console and for `sudo`, and SSH still takes only the key. An empty console password gives key-only login. For a hardened flavor, `make-seed.py` makes the crypt hash from the password, so no `openssl` step is needed. The default is published with the page, so change it outside a closed lab.
- **The SSH key.** When the key file that the platform settings name does not exist, the build makes it: the folder, such as `~\.ssh`, and an Ed25519 key pair from `ssh-keygen`, with no passphrase unless you set one. When only the private key exists, the build writes the public key from it. `-Action Check` and the preview say that the key will be made, and do not make it. With a passphrase, the commands add the lines that let `ssh-agent` hold the key, so SSH asks for the passphrase once.
- **Switch ports and the start lab.** Type the switch ports you use, and they replace placeholders such as `<PORT_EP1>` in the walkthroughs. Pick the lab that Claude starts with. The page takes its list of labs from the chapters named in `lab-catalog.json`, which `sync_lab_selector.py` copies into the page. The list has the labs of the lab sets you chose.
- **Lab plan.** In the **Labs** card, open **Labs you plan to run** and clear the box of each lab or chapter you will not run. The plan has the labs of the lab sets you ticked. The page names the machines those labs no longer use, and **Match the machines to these labs** leaves them out. The machines of a lab are the ones its text names, which `sync_lab_selector.py` reads from the chapters. The gateway, the service hosts, the certificate authority, the DHCP server, and the administrator workstation are always kept, because the labs that build the shared lab need them. The page reads that set from those labs and names the machines. `CLAUDE.md` tells Claude to skip the labs you left out.
- **Progress and results.** Claude logs each step in `PROGRESS.md`, and one row for each SRG requirement when the tests of a lab are finished. **Load progress** reads that file, and the **Progress** tab shows which labs passed and how far each of the 185 FortiSwitch requirements has been tested, with the requirements of every other lab set of the build. In `PROGRESS.md`, a lab of another lab set has its prefix before its number, such as `faz-3.1`. A lab counts as passed when it has passed steps and no failed or blocked step. The page does not check that every step was run. A requirement takes its result from its own row, the one with its SRG ID and its lab, and without one it follows the steps of its lab. A row that names no lab counts for every lab that tests the requirement. **Download results (CSV)** saves one row for each requirement, with the lab, what it was tested on (the switch model and release, or the unit of another lab set), the result, where the result comes from, and the evidence. It is a file of its own and touches no worksheet. `common/make-ckl.py` in the `lab-scripts` folder turns that file, the benchmark files of DISA, and the lab chapters into checklists for DISA STIG Viewer, one for each device and SRG. The checklists are `.cklb` files, the format of STIG Viewer 3, and the script can write the `.ckl` files of STIG Viewer 2 in their place. A passed requirement lab gives the status Not a Finding. A passed gap lab gives Open, or Not Applicable where the crosswalk says so, because a gap lab shows that the product cannot meet the requirement. The README of the folder has the command, the table of statuses, and what a checklist does not prove.
- **Evidence.** `CLAUDE.md` tells Claude to save the output that each lab's **Evidence** line names in `evidence/<lab>/<date>/`, the folders Chapter 999 uses, with the model and the release at the top of each file, and to replace passwords, keys, and secrets with `<SECRET>`. That is an instruction, not a filter, so read an evidence file before you share it.
- **Checksums of install ISOs.** For a flavor that installs from an ISO you supply, type the checksum its publisher gives. On Proxmox VE the command then carries `--iso-sum`, and the check and the deploy stop when the file differs. On ESXi, vCenter, and VxRail the ISO sits on a datastore, where the script cannot read it back, so the commands show the `Get-FileHash` line that checks your copy before you upload it.
- **Kept choices.** The page keeps your choices in the browser, so a reload does not lose them. It keeps no password, and neither does a choices file: they keep the Prompt boxes, and whether the console password is empty. **Start over** clears them.
- **Review before download.** When a build differs from the defaults, or a change was refused, **Download zip** first lists the differences and asks before it makes the zip.
- **A start file for Claude.** The zip also holds `CLAUDE.md` and `START-CLAUDE.txt`. Extract it into a folder named after it, such as `lab201-build`. **Extract All** in Windows makes that folder by itself, and the zip has no folder of its own inside, so you get one folder, not two. Open a terminal in that folder, and run `claude "Start the lab walkthrough."`. Claude Code reads `CLAUDE.md`, which tells it what the folder holds, to begin with the lab you chose, to take one step at a time, to check each result, and not to change a switch without your go-ahead. In the Claude desktop or web app, add the folder to a project or chat and send the line in `START-CLAUDE.txt`.
- **Windows user name.** On the platforms that run a PowerShell script, section 3 starts with **Windows user name**, `admin` by default: the account that runs the script. The commands write its folder, `C:\Users\<name>`, in place of `~`, in the script path of the line that runs the script past the execution policy, in the SSH key file, and in any other path of section 3 that starts with `~`. Under the field, the page shows the full path of the script, the SSH key, and that line. A pasted `~` is not expanded by Command Prompt, by Windows PowerShell 5.1 in the path that `-File` takes, or by the script, while a `~` typed and completed with Tab is. An empty name keeps `~`, and a name that Windows cannot have is refused.
- **Platforms.** Each platform has its own settings. Dell VxRail uses the vCenter script with an existing distributed switch, no uplink changes, and one trunk (see [Volume CCI, Chapter 10](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/10-vcenter-7-8-and-9-lab-virtual-machine-automation.md)). KVM uses [Volume CCI, Chapter 14](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/14-kvm-libvirt-lab-virtual-machine-automation.md).
- **Licensing.** The page lists the products your choices need a license for, says which ones the scripts apply, and writes a template for the license file. See *License keys* in Volume CCI, Chapter 09. It does not accept keys.
- **Gateway configuration.** Section 10 of the page holds the gateway of the lab. The list starts with the Linux router `gw-201`, which the scripts build and which needs no text. Pick another OS type only if a network device takes its place: Cisco ASA, Cisco Nexus (NX-OS), Cisco IOS XE, Cisco IOS XR, FortiGate (FortiOS), or Juniper Junos OS. The page then writes a starting configuration that gives the device the `.1` address of every shared segment, on one 802.1Q trunk port and the out-of-band port, and lets the lab segments reach each other. That is wider than the policy of Lab 999.1, which `gw-201` applies. The text follows the address block, the VLAN IDs, and the subnets you chose, and has its own **Copy** and **Download** button. Port names are placeholders such as `<GW_TRUNK_PORT>`. With a device as the gateway, section 10 asks for the two ports under the OS type: the trunk port, which carries the lab VLANs, and the port on the out-of-band network. A port that you type takes the place of its placeholder in the text, in the lines for an SRX, in the notes, and in the zip, and `LAB-VALUES.md` lists the ports. An empty field keeps its placeholder. A name that cannot be used is refused, and so is the trunk port given a second time, because the text is written for two ports. For Junos, the page shows the extra lines that an SRX Series firewall needs apart from the rest. The zip holds the text as `gateway-device/lab201-gateway-asa.txt` for a Cisco ASA, with the OS type of your device in the name, the SRX lines as `lab201-gateway-junos-extra.txt` beside the Junos text, and the notes of the section in `CHECKLIST.md`. With `gw-201` as the gateway, the zip has no such file. With a device as the gateway, the build leaves `gw-201` out, because the device holds its addresses: the machine table shows it as left out, and the manifest does not have it. `gw-201` joins the two trunks, so the device must reach both.
- **Uplink of the gateway.** `gw-201` is the lab's own firewall, and its uplink is a build adapter, which `-Action RemoveBuildNics` removes. **Uplink** in section 10 is ticked in a new build, so `gw-201` keeps it for the external firewall of section 11. Clear the box for a lab with no way out. `RemoveBuildNics` and `Snapshot` then leave the first adapter of `gw-201` in place. `gw-201` takes its default route there, forwards to it only the traffic of the machines with internet access, lets nothing new in from it, and does not translate addresses. `gw-201` itself takes only answers, ping, neighbor discovery, and its DHCP answer from the uplink, so its SSH does not answer there: log in to it from the lab side or at its console. It also answers ARP for an address only on the adapter that has it. Keep `lab201-wan` apart from the out-of-band network all the same, because what comes in on the out-of-band adapter is not held to the uplink rules. The address comes from DHCP, so reserve it. Tick **Override** to type the address of `gw-201`, the address of the external firewall, and a DNS server. With an address that is set, no DHCP answer names a DNS server, so `gw-201` asks the external firewall unless you type another one. The manifest holds the choice as `uplink`. A device as the gateway brings its own uplink, so the option is offered for `gw-201` only.
- **External firewall configuration.** Section 11 writes the rules for an additional firewall outside the lab, between the lab and the internet, for the same six OS types. It is not `gw-201`, which stays the lab's own firewall and filters between the lab segments (Lab 999.1). A lab machine reaches the supernet of the lab network range. The machines you tick under **Internet access** also reach the internet. Everything else that comes from the lab is dropped. The two service hosts are ticked at the start, because the NTP servers on them take their time from the internet (Lab 999.2), and the gateway is not in the list. The first lines of the text are the route back to the lab. The text does not translate addresses, except the FortiGate policy for internet access. The IPv6 addresses of the lab are unique local addresses, so no machine gets IPv6 internet access. You can edit the text, for example to add a rule that your firewall needs. An edited text no longer follows the page: the page says so, and **Use the page's text again** brings its own text back. The page keeps the edit in the browser and in the choices file, so do not put a password or a key in it. **Copy** and **Download** take the text as it stands, and so does the zip: it holds the text as `external-firewall/lab201-firewall-fortigate.txt` for a FortiGate, with the OS type of your firewall in the name, and `CHECKLIST.md` in the zip has the notes of the section. The text writes what the page cannot know as placeholders such as `<FW_LAB_INTERFACE>`. Under the two choices, section 11 asks for each placeholder that the text of your OS type holds, in the way section 7 asks for the switch ports: the interface of the firewall that faces the lab (on a Cisco ASA the name of that interface, not its hardware name), the interface that faces the internet, which only the FortiGate text names and only when a machine has internet access, and the address that the lab gateway has on the network between it and the firewall. A value that you type takes the place of its placeholder in the text, in the notes under it, and in the zip, and `LAB-VALUES.md` lists the values. An empty field keeps its placeholder. A value that cannot be used is refused, and its placeholder stays: an interface name has letters, digits, and the characters `.`, `_`, `/`, `:`, and `-`, and the gateway address is an IPv4 address outside the lab network range. An uplink address that you set in section 10 is the gateway address, so section 11 shows it and asks for none. The page keeps the values in the browser and in the choices file. They do not reach a text that you edited, and the page says so there. The firewall is not part of the build. The lab reaches it only when `gw-201` keeps its uplink, or when a device as the gateway has one. Put the rules on the firewall after the build adapters are removed: during the build every machine installs its packages over a build adapter, and the last rule drops that traffic. The texts of sections 10 and 11 were written from the vendors' documentation and have not been run on a device, so check them against the reference for your release.
- **Diagram.** The **Diagram** tab draws the lab from your choices, in the layout of the Chapter 999 diagram: the platform, the machines with their names and addresses, the machines you left out, the VLAN IDs, the subnets of the shared segments, the switch models and ports, one trunk or two, the gateway of section 10 with its uplink when the build keeps it, and the external firewall of section 11 with the machines that have internet access and the supernet. The picture names the external firewall as an additional firewall, and `gw-201` as the gateway and lab firewall. Change a choice and the picture changes with it. **Open it in a new tab** shows it at full size, and **Download diagram (SVG)** saves it. The zip holds the same picture as `diagrams/lab-topology.svg`, with a PNG copy where the browser can make one. The service names in the picture come from the Hosts table of Chapter 999, which `sync_lab_selector.py` copies into the page.

### How the page stays in step with the book

The page keeps its own copy of the manifest, the flavor catalog, and the lab data, so that it works with no server. After you change `lab201-vms.json`, `flavors.json`, `lab-catalog.json`, or a lab chapter, run `python scripts/python/sync_lab_selector.py` to copy them into the page. `validate.sh` fails if the copies differ. The page also has a self-test: add `?selftest=1` to its address, and it runs 322 checks of its logic and its controls, and shows the results at the bottom. What those checks expect about the labs, such as the number of requirements, the machines that only the router labs use, or the hosts that a lab set adds, is worked out from the lab data in the page. A chapter edit followed by the sync therefore does not make them fail.

The same script compares the numbers that the documents state in their text with the lab chapters and the page. Those numbers are the count of SRG requirements in the README files and in the lab chapters of Volume CCI, the counts in this chapter, and the count of self-test checks above. The script does not change the text. It names the document, the line, and both numbers, and `validate.sh` fails until they agree.

Two more test modes help after a change to a lab chapter. `?walktest=1` rewrites every lab chapter of every lab set for a build with another supernet, other VLAN IDs, other switch models, and a renamed machine, and reports any value of the book that is left. `?ziptest=1` builds the zip and lists its files. Both need the published folder, because they fetch the lab chapters.

## Validation and Troubleshooting

Check a build before you run it:

- The **Check before you run** box under the tabs lists the warnings of the build. A change that the page refused is in **Refused changes**, with the value that is used.
- The **Changes** tab lists every value that differs from the book, and `CHANGES.md` in the zip holds the same list.
- The **Diagram** tab draws the build. The hosts that no script builds are in a box of their own under the legend.

| Symptom | Cause | Fix |
| --- | --- | --- |
| The zip has `MISSING-FILES.txt` | The page was opened from a local file, so it could not fetch the scripts and the lab chapters | Open the page from the published site |
| A kind of labs cannot be chosen | No lab set of that kind is in the catalog yet | Choose a kind that has a lab set |
| A link ticked no lab set | The id after `?sets=` is not one of the catalog. The line under the lab sets names it | Use `fortiswitch`, `fortianalyzer`, or `fortimanager` |
| The page names machines that the labs do not use | A lab set or a lab was cleared | Click **Match the machines to these labs**, or keep the machines |
| A host that no script builds has the address of a machine | The address of a machine was changed to it in section 5 | Change the address of the machine |
| Addresses in a walkthrough are not the ones of the book | The build leaves a network out, starts at another address, or has a subnet that you set | Use `LAB-VALUES.md`, which lists the values of the build |
| `validate.sh` says the lab selector data is out of date | A chapter, the manifest, or the catalog changed after the last sync | Run `python scripts/python/sync_lab_selector.py` |
| An old link to the Lab Builder opens the Lab Selector | The old address forwards to the new page | Nothing. Update the bookmark |

## Security and Best Practices

- **Type no key and no password of an account.** The page never asks for a license key. It writes a template for the license file, and you fill that file in on your own computer.
- **Treat the console password as public.** The page proposes one, and the proposal is published with the page. Change it or clear it outside a closed lab.
- **Keep the lab closed.** The lab network must not be routed into another network. Its one way out is the uplink of the gateway to the external firewall, when you keep it.
- **Use your own vendor account for the images.** Download the image of a FortiAnalyzer-VM, a FortiManager-VM, or a FortiGate-VM yourself, and do not share the password or the token of that account with anyone, including an assistant.
- **Read an evidence file before you share it.** Claude is told to replace passwords, keys, and secrets with `<SECRET>`. That is an instruction, not a filter.
- **Preview before you build.** Every build script has a readiness check and a preview. Run both first.

## References and Knowledge Checks

**References:**

- [Chapter 02](02-lab-data-and-how-to-add-a-lab-set.md) for the data the page works from, and how to add a lab set.
- [Volume CCI, Chapter 999](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) for the shared lab, and its [Chapter 09](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/09-esxi-7-8-and-9-lab-virtual-machine-automation.md) for the machines, the Linux flavors, and the license keys.
- [Volume CCII, Chapter 999](../../volume-202-fortianalyzer-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) and [Volume CCIII, Chapter 999](../../volume-203-fortimanager-stig-and-srg-mapping/chapters/999-shared-lab-infrastructure.md) for the hosts of the FortiAnalyzer and FortiManager lab sets.
- The `lab-scripts` folder of this volume, and its `README.md`.

**Knowledge checks:**

1. Which kinds of labs does the page offer, and which of them has lab sets today?
2. Which labs are in every build, and why do Labs 999.3 to 999.6 belong to one lab set?
3. Why does no script build `faz-202`, and where does the page say how to build it?
4. How is Lab 4.1 of Volume CCII named in `PROGRESS.md`, and why?
5. What does **Match the machines to these labs** do after you clear the FortiSwitch lab set?
6. Which two commands tell you that the page and the lab chapters are in step?
7. What does a link with `?sets=fortianalyzer` do on a build with no kept choices, and what does it leave alone when the browser kept your choices?

## Hands-On Lab

**Shared prerequisites.** A browser, and the published Lab Selector. **Cost:** none. This lab plans a build and downloads its zip. It builds no machine.

### Lab 1.1 — Plan a build for the FortiAnalyzer labs

**Goal.** A zip for a build that has the FortiAnalyzer labs and no FortiSwitch labs, with only the machines those labs use.

1. Open the Lab Selector. In the **Labs** card, confirm that **SRG labs** is chosen and that only the FortiSwitch lab set is ticked.
2. Tick **FortiAnalyzer**, and clear **FortiSwitch**. Read the line under the lab sets: it names the lab sets of the build and the number of lab chapters in the zip.
3. Open **Labs you plan to run**. Clear a lab that you will not run, for example the gap lab of Chapter 03.
4. In section 5, read the note above the machine table. It names the machines that the plan does not use. Click **Match the machines to these labs**, and confirm that the machine count at the top right goes down.
5. In section 5, read the table **Hosts that no script builds**. Note the address of `faz-202` and the walkthrough that builds it.
6. Choose your platform in section 1, and fill in section 3.
7. Open the **Diagram** tab, and find the box of the hosts that are built by hand.
8. Click **Download zip**. Unzip it, and open `LAB-VALUES.md` and `CLAUDE.md`.

**Expected result.** The zip holds `walkthroughs/999-shared-lab.md` and three files whose names start with `faz-`. `LAB-VALUES.md` has the sections *Lab sets in this build* and *Hosts that no script builds*, and no section about switches. `CLAUDE.md` tells Claude to walk Labs 999.1 and 999.2 of the shared lab, then the labs of FortiAnalyzer.

### Cleanup

Click **Start over** to go back to a new build. Delete the unzipped folder if you do not keep the build.

## Lab Verification

Complete this sign-off once Lab 1.1 has been run on the published page. The self-test of the page checks the same steps on its own controls, but no person has run the lab on the published site yet.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Lab Selector is one page that plans a lab build for the labs you choose. It offers three kinds of labs, and the SRG labs have three lab sets today: FortiSwitch, FortiAnalyzer, and FortiManager. Every lab set runs on the shared lab of Volume CCI, which the scripts of this volume build, and a lab set can add hosts that you build by hand. The page writes the manifest, the commands, a checklist, and the walkthroughs of the build, and it reads the progress of the labs back.

- [ ] Can choose a kind of labs and the lab sets of a build.
- [ ] Can plan the labs of a lab set and match the machines to them.
- [ ] Can name the hosts that no script builds, and say where each one is built.
- [ ] Can read the changes of a build, and hand its zip to Claude.
- [ ] Can run the sync and the self-test after a change.
