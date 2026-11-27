# Chapter 90: As-Built — How This Volume Was Built

## Learning Objectives

- Trace where the Lab Selector and the lab scripts came from, and when each part changed.
- Say what moved to this volume on 2026-11-20, what was renamed, and what stayed where it was.
- Explain the choices behind the lab sets, the prefixes, and the hosts that no script builds.
- Name what was tested, how, and what has not been tested.
- Find the old addresses that still work, and the one that does not.

## Theory and Architecture

This is the volume's **as-built chapter**. Like an as-built drawing, it records how the volume was actually made rather than how it was planned: where each part came from, which choices were made, and what was tested. It is numbered 90 so that it stays last if chapters are added, and so that as-built chapters have the same number in every volume that has one.

The volume was not written from nothing. Its page and its scripts were built inside [Volume CCI — FortiSwitch STIG and SRG Mapping](../../volume-201-fortiswitch-stig-and-srg-mapping/README.md), whose [as-built chapter](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/90-as-built-how-this-volume-was-built.md) records that work step by step. This chapter records what happened from the move on.

### How each part of the volume was built

| Part | Built | How | Later changes |
| --- | --- | --- | --- |
| The build scripts and the manifest | 2026-11-06, in Volume CCI | Written with Chapters 09 to 13 of that volume, one script for each platform, with KVM added later as its Chapter 14 | Moved here on 2026-11-20. The messages of the scripts name the Lab Selector |
| The page | 2026-11-06, in Volume CCI, as the Lab Builder | One page of HTML, CSS, and JavaScript with no library | Extended on 2026-11-09 and after. Moved here, renamed, and given lab sets on 2026-11-20 |
| The address plan | 2026-11-19, in Volume CCI | The segments were renumbered so that the subnets are contiguous | The block moved from `10.201.0.0/16` to `10.200.0.0/16` on 2026-11-20. Each network took a block of its own size on 2026-11-24 |
| `common/lab-catalog.json` | 2026-11-20 | Written by hand, in place of the list of walkthrough chapters that the page had before | Add a lab set here |
| The lab data of the FortiAnalyzer and FortiManager lab sets | 2026-11-20 | Read from the lab chapters of Volumes CCII and CCIII by `scripts/python/sync_lab_selector.py` | Regenerate after a chapter changes |
| Links that tick lab sets | 2026-11-22 | The page reads `?sets=` and the ids of lab sets from its address, once. The site build and the documents of the three product volumes link to the page with their lab set ticked | None |
| The values of the gateway text and the firewall text | 2026-11-23 | Section 10 asks for the two ports of a network device that is the gateway, and section 11 for the interfaces and the gateway address of the external firewall. The texts left them as placeholders, and the page writes them into the texts | None |
| The table of the lab networks | 2026-11-24 | The table of the IP addressing section has a row for every lab network of the build, in the order of their addresses. It had a row for each shared segment only, so it started at the third subnet of the lab | Since the same day the first row of the table is the supernet, with its first and its last address, and the Segments table of Chapter 999 starts with the same row |
| A block of its own size for each lab network | 2026-11-24 | A lab network takes the smallest block that holds its hosts, a /28 unless it needs another size. Before, each one was a /24 whose third octet was its number. The Segments table of Volume CCI's Chapter 999 gives each size. The lab chapters of Volumes CCI, CCII, and CCIII, the two lab diagrams, the manifest, `make-seed.py`, the sync script, and the page changed together | None |
| Checklists for DISA STIG Viewer | 2026-11-26 | `common/make-ckl.py` writes one checklist for each device and SRG from the results file of the page, the benchmark files of DISA, and the lab chapters. A passed gap lab gives a finding, because it shows that the product cannot meet the requirement | Since 2026-11-27 a checklist is a `.cklb` file, the format of STIG Viewer 3. `--format ckl` writes the `.ckl` format of STIG Viewer 2, which the script wrote on the first day |
| The lab name, the zip, and the bypass line | 2026-11-27 | A **Lab name** field renames everything a build writes, the zip has no folder inside, and the line that runs a script past the execution policy points into the zip extracted into Downloads | — |
| Workstation 26H1 U1, Python, and the uplink | 2026-11-27 | Workstation Pro 26H1 U1 is the one Workstation release the page offers, the Windows scripts are given `-PythonCommand python`, and the uplink of `gw-201` is ticked in a new build | — |
| Passwords and the SSH key | 2026-11-27 | One lab password with a field for each password, Prompt boxes, and an SSH key that the build makes when it is missing | — |
| The Windows user name | 2026-11-27 | Section 3 asks for the user that runs the script, and the commands write `C:\Users\<name>` in place of `~` | — |
| Disks of at least 10 GB | 2026-11-27 | The smallest disk of every machine is the 10 GiB of the Ubuntu cloud image | — |
| [Chapter 01](01-the-lab-selector.md) | 2026-11-20 | The description of the page moved from Volume CCI's Chapter 09, and the parts about the lab sets were written new | Updated whenever the page changes |
| [Chapter 02](02-lab-data-and-how-to-add-a-lab-set.md) | 2026-11-20 | Written from the catalog and the sync script | Updated whenever the data changes |
| 90, this chapter | 2026-11-20 | Written from the work of that day and from Volume CCI's Chapter 90 | Updated whenever the volume changes |

### What moved, and what stayed

On 2026-11-20 the `lab-scripts` folder moved from Volume CCI to this volume with `git mv`, so `git log --follow` on a file shows its history before the move.

- **Moved:** the page, the manifest, the flavor catalog, the switch feature data, the seed tool, the image resolver, the six build scripts, and the README of the folder.
- **Renamed:** the page, from `builder/lab-builder.html` to `selector/lab-selector.html`, and its name, from Lab Builder to Lab Selector. The sync script is now `scripts/python/sync_lab_selector.py`. The choices file that the page saves is `lab-selector-choices.json`.
- **Replaced:** the file `walkthroughs.list`, by `common/lab-catalog.json`.
- **Stayed in Volume CCI:** Chapters 09 to 14, which explain each platform, the Chapter 999 that the scripts build, and its diagram. Their links point here now.
- **Kept their names:** `lab201-vms.json`, the `Deploy-Lab201` scripts, the host names that end in `-201`, and the IPv6 prefix `fd00:db8:201::`. The lab chapters and labs that are already built use them.

The published addresses changed with the folder, from `downloads/volume-201-fortiswitch-stig-and-srg-mapping/` to `downloads/volume-901-lab-selector/`. The site build writes a page at the old address of the Lab Builder that forwards to the Lab Selector. The zip of the scripts has a new address and no forward, because a file cannot forward.

## Design Considerations

- **A volume of its own.** The page now serves the labs of three volumes and will serve more, so it does not belong to one product volume. Volume numbers 200 to 299 are reserved for Fortinet STIG work, so the page took the number after the lab gear volume, 901.
- **Three kinds, one of them filled.** The page offers SRG labs, certification labs, and learning labs. Only the SRG labs have lab sets: FortiSwitch, FortiAnalyzer, and FortiManager. A kind with no lab set is shown and cannot be chosen, so the page never has a build with nothing in it.
- **A new build is the old build.** A new build has the FortiSwitch lab set, so a reader who knew the Lab Builder gets what it gave, and a choices file from before the lab sets loads as a FortiSwitch build.
- **Every lab set runs on the shared lab.** The chapters of Volumes CCII and CCIII already reuse the lab network and the service hosts of Volume CCI. The page follows them: Labs 999.1 and 999.2 of the shared lab are in every build, and Labs 999.3 to 999.6, which prepare the switches, belong to the FortiSwitch lab set.
- **Hosts are read, not typed.** The five hosts of the two new lab sets come from the **Address plan** tables of their Chapter 999. No script builds them, because the images of a FortiAnalyzer-VM, a FortiManager-VM, and a FortiGate-VM need a vendor account. The mail server could be built by a script. It is not, because a new role for the seed tool needs a build on a hypervisor first.
- **No new segment.** The chapters put the new hosts on the Lab-Services segment, at `10.200.2.100` to `10.200.2.130`, so the lab plan did not grow. The page gives a subnet only to a network of the Segments table of the shared lab.
- **A prefix for the labs of another volume.** Volumes CCI and CCII both have a Lab 4.1. A lab of a lab set other than FortiSwitch has the prefix of its set before its number, in the page, in `PROGRESS.md`, and in the evidence folders. The FortiSwitch labs keep their plain numbers, so an existing `PROGRESS.md` still reads.
- **Fewer networks without the switch labs.** A build with no FortiSwitch labs takes the out-of-band network and the seven shared segments only. A network that only the switch labs use takes no subnet, so the subnets of such a build are the ones the chapters print.
- **The Labs card has no number.** It comes before section 1, so the eleven numbered sections kept their numbers, which the page, the zip, and the chapters name in many places.
- **A link counts once.** A link with `?sets=` ticks its lab sets when the page starts. The page then keeps the result and takes the `sets` part out of its address, because a link that stayed there would undo at every reload what a reader chose afterward. On a build with no kept choices the link also matches the machines to the labs, so that a first visitor gets a build that fits the lab set. On top of kept choices it changes the lab sets only, because the machines there are choices of the reader.
- **The page asks for what a text leaves open.** The external firewall text had placeholders for what only the reader knows, and the reader had to replace them by hand in the text. Section 11 now asks for each one, in the way section 7 asks for the switch ports. It asks only for the placeholders that the text of the chosen OS type holds, so a field that the text does not use is not shown and its value is not checked. The uplink address of section 10 already is the address of the gateway, so the page shows it and does not ask twice. A value is checked before it stands in a configuration text, because a quote or a line break in it would change what the text does. Section 10 asks in the same way for the two ports of a network device that is the gateway, and only then: with the Linux router there is no text and no field. It refuses the trunk port given a second time, because its text is written for two ports.
- **The table of section 6 shows the whole plan.** The lab always started at the first subnet of its supernet, which OOB-Mgmt takes. The table listed the seven shared segments only, because only they have fields, so its first row was `10.200.2.0/24`, and the other networks stood in one line of small text under it. A reader could take that for a plan that leaves the first subnets unused. The table now has a row for every network of the build, and only the rows of the shared segments have fields. The rows follow the addresses and not the segment numbers. In a build that has the routing peers and no Console-OOB network, the routed links take the second subnet, and a subnet that the reader sets can lie anywhere. A row does not move while the reader works in the table, because a row that jumps away under the cursor is worse than a row that is out of order for a moment.
- **A network takes the smallest block that holds it.** The owner of the book asked for a smaller block than a /24, such as a /28, wherever a network allows it. A count of the addresses in the chapters and in the manifest gave the sizes. Lab-Services holds 18 addresses across the three volumes, so it is a /27. The networks that the two routing peers advertise stay a /24 each, because Lab 6.6 of Volume CCI accepts no BGP prefix longer than a /24 and tests that with a /25. FortiLink is a /30 for the FortiGate and the one switch of Lab 4.2. Every other network is a /28. The lab went from 4,096 addresses in a /20 to 740 in a /22.
- **The networks of every build keep their blocks.** The page places the out-of-band network and the shared segments first, one after the other, and then puts each other network in the lowest free block of its size. So a build that leaves a network out has the addresses of the chapters for the gateway, the service hosts, and the user segments, and a build with every network is the plan of Chapter 999. A placement that filled every free block in the order of the Segments table was tried first. In a build without the console network it put the Admin segment in front of Lab-Services, and it moved every segment after it.
- **A VLAN ID is the number of its segment.** While a subnet was a /24, the VLAN ID was its third octet, and a build that started at another address had other VLAN IDs. A block of 16 addresses has no octet of its own, so the VLAN ID comes from the segment number alone, and it changes only when the reader sets it.
- **An IPv6 address comes from the segment and the host number.** It was the third and the fourth octet of the IPv4 address. The host number is the place of a host in the block of its segment. The IPv6 subnets stay a /120 for each segment, because IPv6 has no shortage of addresses, and a host that keeps its number keeps its IPv6 address.
- **A host keeps its number where it fits.** The gateway is host number 1. A host with a number up to 14 kept it, so the switches, the administrator workstation, and the static hosts changed only by the block they are in. The service names of Lab-Services, the attacker host, and the loopbacks of the two peers got new numbers, and a DHCP scope went from 100 addresses to 7.
- **No field for the number of subnets.** The field counted /24 subnets. With blocks of different sizes a count says nothing about the size of the supernet, so the row shows the count and the sizes, and a reader who wants room types a larger supernet.

## Implementation and Automation

### The steps of 2026-11-20

1. **The address block.** Every `10.201` address became `10.200`: 446 replacements in 21 files of Volumes CCI and CCII, the two diagrams, the manifest, the seed tool, and the page. One value in the self-test of the page was changed by hand, because the new block made a deliberately wrong supernet start at the first subnet.
2. **The FortiManager labs.** The `/srg-labs-for` workflow wrote 17 labs for the 79 requirements of FortiManager in Volume CCIII, so that the page could offer three lab sets with labs.
3. **The move.** The folder moved here, and the page and the sync script were renamed.
4. **The catalog and the lab data.** The sync script was rewritten to read a catalog of lab kinds and lab sets, the chapters of more than one volume, and the **Address plan** table of each Chapter 999. For the FortiSwitch labs it writes the same data as before, with four fields added to each lab.
5. **The page.** The core logic got the lab sets, the hosts that no script builds, and the lab ids with a prefix. The texts of the zip follow the lab sets: `CLAUDE.md`, `LAB-VALUES.md`, the checklist, the changes, and the license list say nothing about switches in a build with no switch labs. The interface got the Labs card, the lab plan for each lab set, and the table of hosts in section 5. The picture got a box for the hosts that are built by hand.
6. **The scripts around it.** The site build takes the published files from the sync script, links the page under **Interactive companions**, and writes the forward at the old address. `validate.sh` and the lab script check follow the new names.
7. **The documents.** The description of the page moved from Volume CCI's Chapter 09 to Chapter 01 here. The documents of Volumes CCI, CCII, and CCIII point to this volume.

### Links that tick lab sets, 2026-11-22

Each volume whose labs the page offers got a link that opens the page with its lab set ticked.

1. **The page.** At its start the page reads `?sets=` and the ids after it. It ticks exactly those lab sets, says what it did in a line under the lab sets, saves the result with the kept choices, and takes the `sets` part out of its address. The **Labs** card shows the link for the lab sets of the build.
2. **The portal.** The sync script lists the lab sets for the site build (`--set-links`), and the site build gives the portal page of each such volume a link with its lab set. The link check of the site build now looks for the file of a link, and not for what follows a question mark.
3. **The documents.** The README files of Volumes CCI, CCII, and CCIII, the Chapter 999 of Volumes CCII and CCIII, Chapter 09 of Volume CCI, and the chapters of this volume have the links.

The first version applied a link and waited for the next click to save the result. A reload then went back to the older choices, or to a FortiSwitch build for a first visitor, and the address no longer had the link. A try in the browser showed it, and the page now saves the result of a link when it applies it.

### Values for the firewall text and the gateway text, 2026-11-23

Section 11 got a field for each placeholder of the external firewall text. Section 10 then got the same for the two ports of a network device that is the gateway.

1. **The core.** A list names the three placeholders: the interface that faces the lab, the interface that faces the internet, and the address of the lab gateway. A check reads what was typed, says which placeholders the text of the OS type holds, and refuses a value that cannot stand in a configuration text. The function that writes the firewall text takes the values, puts them in place of the placeholders, and words its notes for a value that is there and for one that is still to replace. An uplink address of section 10 goes the same way, where it had a special case before.
2. **The page.** The fields stand under the two choices of the section, above the text. They are built again only when another set of fields is needed, so typing in one is not disturbed. A field that holds a value is marked, and one whose value was refused shows why.
3. **The zip and the choices.** `LAB-VALUES.md` got the section *External firewall* with the placeholders and their values. The choices file and the browser keep the values, and a file from before them loads with none.
4. **Section 10.** A second list names the two ports of the text for a network device as the gateway: the trunk port and the port on the out-of-band network. The function that writes that text takes the ports, and puts them into the text and into the extra lines for an SRX. `LAB-VALUES.md` got the section *Gateway device*, which is there only with a device as the gateway. One function of the page now draws the fields of both sections.
5. **The documents.** Chapter 01 and the README of the `lab-scripts` folder describe the fields.

The first layout put the line about a field beside it. The column is narrow, so one word stood beside the field and the rest of the line under it. A look at the page showed it, and the line stands under the field now.

### The table of the lab networks, 2026-11-24

A reader reported that the IP addressing section does not start at the first subnet. The table of the section got a row for every lab network of the build.

1. **The core.** A function returns the networks of the build in the order of their addresses, each with its name, its subnet, and its VLAN: the VLAN ID of a shared segment, the VLAN ID and the VNI of the VXLAN tenant network, and for every other network the text of the Segments table in Chapter 999.
2. **The page.** The table is drawn from that list. Its rows are written again when the networks of the build or their order change, and not while the focus is in the table. When the focus leaves the table, the rows take their order. The line *Other lab networks* under the table is gone, and a short note says which rows have fields.
3. **The documents.** Chapter 01 and the README of the `lab-scripts` folder describe the table.

With all the networks in the table, the names wrapped whenever a row showed the field for a subnet. A look at the page showed it. The names stay on one line now in a window wider than 640 pixels. In a narrower window they wrap as before, because the table would be wider otherwise.

On the same day the owner asked for the supernet at the top of the table, with its first and its last address. The table of section 6 got a first row for it, which follows the supernet of the build. The Segments table of Chapter 999 got the same row: `10.200.0.0/22`, from `10.200.0.0` to `10.200.3.255`. That row is written by hand, so the sync script compares it with the networks under it and names the supernet that they need. In a copy of the chapter the page puts the supernet of the build in the row. The rule that moves an address with its lab network would be wrong for the two addresses of the row. In the book the first address of the supernet is also the first address of OOB-Mgmt, and a build can place OOB-Mgmt elsewhere. The last address of the supernet is in no lab network. So the page replaces the three values of the row by name, before the other rules run.

### A block of its own size for each lab network, 2026-11-24

1. **The plan.** A script read the Segments table of Chapter 999 and every lab address in the lab volumes, and counted the addresses of each network. It placed the networks, checked that no two blocks overlap and that every host fits, and printed the plan. The owner looked at it and made FortiLink a /30.
2. **The chapters.** A second script replaced 400 literal addresses in 18 files: the lab chapters of Volumes CCI, CCII, and CCIII, the two lab diagrams, the manifest, and two documents of this volume. It kept the host number of each host and gave a new one to a host whose number did not fit. The sentences about the plan were changed by hand: the address plan of Chapter 999, the host parts such as `.1` and `.100` to `.199`, the labels of the diagrams, and seven subnet masks.
3. **The manifest and the seed script.** The manifest has a list, `segments`, with the block of every lab network. `make-seed.py` finds the segment and the host number of an address in that list. From them it writes the IPv6 addresses, the VLAN interfaces of the gateway, the firewall of the gateway, and the DHCP scopes of a Windows DHCP server.
4. **The sync script.** It reads the block of each network from the Segments table and finds the network of an address by the block that holds it. It has a new check, the address plan: no two blocks overlap, the manifest lists the same blocks as the chapter, and every address of a machine, of a service name, and of a host of a lab set lies in a block.
5. **The core of the page.** A network is a block with a first address and a size, and one function says which network holds an address. The placement, the VLAN IDs, the addresses of the machines, the manifest, the list of changes, `LAB-VALUES.md`, the gateway text, the lab network range, the picture, and the copies of the lab chapters were written for blocks. A copy of a lab chapter moves each address with its network and keeps its host number.
6. **Section 6.** The row **Subnets** shows how many subnets the build has and of which sizes. A subnet that the reader sets has to be a block of the size of its segment, and the page places the other networks around it. Ticking **Set subnet** used to show an error at once, because the other segments moved up into the subnet that the field proposed. That is gone.
7. **Choices from before.** The choices file has format 3. A file from before loads with a note: its lab has the old addresses until it is built again. A subnet that was set becomes the first block of the size of its segment in it, an edited machine address is left out, and a number of subnets that was set is left out.

Two faults came to light on the way, and both were corrected. The seed script moved the IPv4 networks of the gateway's firewall with a line that searched for `10.201`, the block that the plan had until 2026-11-20, so it found nothing in rules that name `10.200`. Since that day a build in another IPv4 block, with another first address, or with a subnet set for segment 2, 3, or 4 got IPv4 rules for the networks of the book. Its gateway passed ping and IPv6 between the segments and dropped the other IPv4 traffic. The check of the lab scripts did not find it, because it built the plan of the book only. The legend of the picture named VLAN 230 for the VXLAN tenant network, a number from before 2026-11-19. It takes the number from the lab data now.

### Checklists for STIG Viewer, 2026-11-26

The owner asked for checklist files for DISA STIG Viewer. `common/make-ckl.py` writes them.

1. **What was there.** A lab requirement carries an SRG ID, and DISA publishes each SRG as a benchmark file with one rule for each ID. Of the 329 requirement rows of the three lab sets, 327 are rules of five SRGs: Layer 2 Switch, Network Device Management, Router, AAA Services, and Central Log Server. `SRG-NET-000331-L2S-000001` and `SRG-NET-000332-L2S-000002` are cited by the Cisco NX-OS STIG and are no rules of the Layer 2 Switch SRG.
2. **The format of the first day.** The checklists were `.ckl` files. For them the script follows the checklist schema 2.5 of STIG Viewer 2, which was read from the copy in MITRE's `heimdall2` repository. The order of the fields follows a checklist that STIG Viewer 2.17 saved, from the samples of the same repository. Neither file is in this repository.
3. **The inputs.** The results file of the page says which lab tests a requirement, on which device, and with which result. The benchmark files give the rules. The script reads the zips of DISA in memory and downloads nothing. It does not read a file with a document type declaration, or one larger than 64 MB.
4. **What a passed lab means.** A gap lab passes when it shows that a setting is absent. So the script also reads the lab chapters: the title of a lab, which starts with *Gaps* for a gap lab, and the alignment cell of a requirement. A pass gives Not a Finding. For a requirement that is met in part, or that a gap lab covers, it gives Open. Where the crosswalk says *Not applicable*, it gives Not Applicable. The results file does not hold this difference, so the script cannot work from the results file alone.
5. **One checklist for each device and SRG.** A lab on both switches counts for each switch. A checklist holds every rule of its SRG, and a rule with no lab on the device stays Not Reviewed. The same input gives the same file, byte for byte, because the identifier of a benchmark is made from its name and its release.
6. **The checks.** The script checks each file against the order and the values of the schema before it leaves it. Its self-test builds a benchmark, a chapter, and a results file. It had 26 checks on that day, and it has 37 since the `.cklb` format. `check_lab_scripts.py` runs the self-test. It also compares the requirement rows that the script reads from the chapters with the rows of the page, because the script reads the chapters with code of its own.

On 2026-11-27 the owner asked for the newer format. The script now writes `.cklb` files, the JSON format of STIG Viewer 3, and `--format ckl` or `--format both` writes the older format. DISA publishes no schema for `.cklb`, so there was nothing to validate a file against. The format was read from files that two programs of DISA wrote, both found in public repositories: a checklist that STIG Viewer 3 saved for a Cisco NX-OS switch, and one from the SCAP Compliance Checker 5.14.1. The two do not agree in every field. STIG Viewer 3 writes the title of the rule into `group_title` and keeps the SRG number in `group_tree`. The checker writes the SRG number into `group_title`. The script follows STIG Viewer 3, because the files are for that program. In both, `size` is the number of the rules. A checklist always has a host name, because an importer such as STIG Manager refuses a file without one: a device with no name takes the name of its file. An identifier in a `.cklb` file is made from the device and the benchmark, so the same input gives the same file and no two checklists share an identifier.

### A lab name for each build, 2026-11-27

The owner asked for a lab name in place of 201, a zip that extracts to one folder, and a line that runs the script of the extracted zip past the execution policy.

1. **What a lab name renames.** The owner asked for every name, the names inside the machines too. `201` is in the page, the seven platform scripts, `make-seed.py`, and the manifest: in network names (`lab201-t1`), machine and service names (`gw-201`, `radius-201a`), environment variables (`LAB201_CONSOLE_PASSWORD`), files and services inside the machines (`lab201-status`, `/etc/lab201-vm`), the status variable that VMware reads (`guestinfo.lab201`), and the snapshot (`baseline-201`).
2. **How.** The page keeps the 201 names inside and renames what it writes: the texts of its tabs, the gateway and firewall texts, the text of the page, and every file and file name of the zip, the scripts and the walkthroughs among them. The scripts in the zip are renamed copies, so the scripts of the repository did not change. One pattern does the renaming: `lab201`, `Lab201`, and `LAB201` with the name in place of 201, `Lab 201` and `lab 201` in prose, and then every name that ends in `-201`, `-201a`, or `-201b`, in the lab data and in the lab chapters, such as `mirror-201` and `lab-crl-201`. The first rule took only the names of the lab data, and the walkthrough test of the published page, which now also renames the lab, found those two in the chapters. Links, lab numbers such as `201.3`, the IPv6 prefix `fd00:db8:201::`, and the node names of the topology picture keep their text. A build named 201 is the same as before, because the pattern then changes nothing.
3. **The limit of five characters.** The longest machine names, `oob-admin-<name>` and `mcast-src-<name>`, have ten characters before the name, and a Windows computer name has at most 15.
4. **The zip.** Its files sat in a folder, `lab201-build`, so **Extract All** in Windows made `lab201-build\lab201-build`. They now sit at the top of the zip, and the zip takes the lab name: `lab305-build.zip` for a lab named 305.
5. **The bypass line.** The line in the commands and in the notes is `pwsh -ExecutionPolicy Bypass -File ~\Downloads\lab201-build\workstation\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub` for Workstation, with the script of each platform and the lab name of the build. The owner's first form had no value after `-ExecutionPolicy` and named the script at the top of Downloads, where it cannot find the `common` folder beside its own. PowerShell 7 expands `~` in the path that `-File` takes and Windows PowerShell 5.1 does not, which was tried on this computer, so the notes say to use `powershell` and `$HOME` there.

### Workstation 26H1 U1, Python, and the uplink, 2026-11-27

1. **One Workstation release.** The owner asked that the older Workstation releases be removed everywhere. The page offers Workstation Pro 26H1 U1 alone, and a choices file that names an older release loads with 26H1 U1 and a note. The Workstation script looks for Workstation under Program Files only, where the 64-bit 26H1 installs, and `-WorkstationDir` still names another folder. Broadcom's release notes give the build (25688693) and the date (3 September 2026) of 26H1 U1, but not the install folder or whether OVF Tool is included, so those come from a 26H1 install on the owner's computer.
2. **Python.** The Python command field of the Windows platforms starts with `python`, so the commands pass `-PythonCommand python`. An empty field lets the script try `python3`, the `py` launcher, and `python` as before. Proxmox VE and KVM keep `python3`.
3. **The uplink.** **Uplink** in section 10 is ticked in a new build. The review before the download does not list it, because it is no longer a change of yours, and `CHANGES.md` still says that `gw-201` keeps its uplink, because Chapter 999 removes every build adapter. A choices file without the uplink loads with it ticked. The self-test starts its older uplink checks from a build without the uplink, and two new checks test the default.

### Passwords and the SSH key, 2026-11-27

The owner asked that the build make the SSH folder and keys, and that the passwords of the machines be the default the page proposes unless the user types others or wants to be asked when the build runs.

1. **One password by default.** Section 4 has a **Lab password**, the console password the page proposed before. The console and `sudo` password, the Windows admin password, and the password of the hardened flavors start with it and follow it until one is typed. The owner chose that the SSH key passphrase starts empty, so a key that the build makes has none and SSH needs no agent.
2. **Asked when the build runs.** A **Prompt when the script runs** box leaves the password's line out of the commands and names it in `LAB201_PROMPT`. Every platform script runs `make-seed.py` to write the seeds, so `make-seed.py` asks, with Python's `getpass`, and one change serves all seven scripts. A preview asks for nothing. The prompt itself was not run here, because `getpass` reads the console and the checks run without one.
3. **The key.** The scripts pass `--make-keys` to `make-seed.py`, or `--preview` in a preview. A missing key file whose name ends in `.pub` is then made with its folder by `ssh-keygen -t ed25519`, with the passphrase of `LAB201_SSH_KEY_PASSPHRASE`, none, or the one `ssh-keygen` asks for. A public key is written from a private key that is there alone. `-Action Check` and the bash checks report a missing key as one the deploy makes.
4. **The hardened flavors.** They needed a crypt hash from `openssl passwd -6`. `make-seed.py` now makes the SHA-512 crypt hash from `LAB201_ADMIN_PASSWORD` with the standard library, and a hash in `LAB201_ADMIN_PASSWORD_HASH` still wins.
5. **What is kept.** A choices file and the browser keep no password, only the Prompt boxes and whether the console password is empty. Until this day a choices file kept the console password. A file from before still gives it back.

### The Windows user name, 2026-11-27

The owner pasted the bypass line with `~` and Windows did not find the script, while the same line typed with `~` and completed with Tab worked: Tab completion writes out the folder before the command runs, and a pasted `~` reaches the program as it is. The owner asked for a field for the user that runs the script, with a preview of the full path, saw a picture of the section first, and chose `admin` as the default. Section 3 of the platforms that run a PowerShell script now starts with **Windows user name**. The commands write `C:\Users\<name>` in place of a `~` at the start of a path of section 3, of the SSH key file, of the script path of the bypass line, and of the `ssh-add` line, and a box under the field shows the script path, the key, and the bypass line. The SSH key field shows the key with that folder. An empty name keeps `~`, with the note for Windows PowerShell 5.1, and a name with a character that Windows does not allow is refused. Three self-test checks came with it. The text of the page renames the placeholders of its fields with the lab name too.

### Disks of at least 10 GB, 2026-11-27

The owner's first build on Workstation, a lab named 202, built all 12 machines. Workstation refused to resize three disks, of `mcast-src-202`, `static-1`, and `static-2`, because the manifest asked for 8 GB and the disk of the Ubuntu 24.04 OVA is 10 GiB (`ovf:capacity` 10737418240 in its OVF, read on this day, and the same for the 26.04 OVA). A disk cannot shrink, so the machines kept 10 GB. The owner asked that the minimum sizes match the image. In `lab201-vms.json`, every minimum disk below 10 GB is now 10 (`ca`, `dhcp`, both routing peers, `mcast-src`, `static-1`, `static-2`), and the three 8 GB disks are 10 GB, so a new build asks for 254 GB of thin disk instead of 248. The flavor minimums of `flavors.json` could have done it for Ubuntu alone, but the page would then have marked those machines as raised by the flavor in every build. Three self-test checks were rewritten for the new sizes. The same build made the SSH key of the user `admin` with no passphrase, which was the first run of that step on a real host.

### What was tested, and what was not

The checks of this table ran on 2026-11-23, on a local copy of the published folder, except the last row. On 2026-11-24 the self-test, the walkthrough test, the check of the lab scripts, and `validate.sh` ran again, and the table of section 6 was tried by hand. They ran once more on the same day, after each lab network took a block of its own size, and section 6 was tried by hand again.

| Check | Result |
| --- | --- |
| The self-test of the page (`?selftest=1`) | 322 checks pass in a Chromium browser, on a local copy of the published folder. 237 check the core of the page, and 85 check what the page shows. Eighteen of them came on 2026-11-27, for the lab name, the bypass line, the uplink of a new build, the passwords, and the Windows user name. About 60 checks expected a /24 for each network. They now place the lab networks themselves, in the two steps of the page, and compare the page with that |
| The fields of sections 10 and 11, tried by hand | In section 11: typing in the three fields, a reload, a value that cannot be used, another OS type, and an uplink address that was set and cleared again. In section 10: typing in the two fields, a reload, the trunk port given a second time, another OS type, and the Linux router and then a device again. Each did what Chapter 01 says, also in a window as narrow as a phone |
| The table of section 6, tried by hand | A new build, a build with the FortiAnalyzer lab set from a link, a subnet typed for a segment, a reload, and a window as narrow as a phone. The first row was the first subnet of the lab each time. The row of the segment stayed in place during the typing and moved to the place of its address when the focus left the table |
| Section 6 with blocks of different sizes, tried by hand | A new build has 16 rows from `10.200.0.0/28` to `10.200.2.0/24`, the supernet `10.200.0.0/22`, and the row **Subnets** with the count and the sizes. The row above the 16 is the supernet, with `10.200.0.0 to 10.200.3.255`, and it follows a supernet that is typed. Ticking **Set subnet** gave the field the subnet of the page and no error. A free block that was typed was used. A block of another size and an address inside a block were refused with a message. The row moved when the focus left the table. The section was looked at in a window 1,280 pixels wide and in one as narrow as a phone, and no label of the picture in the Diagram tab leaves its box |
| Links at the start of the page, tried by hand | A visitor with no kept choices, a reload after the link, a link on top of kept choices, and a link with names that the page does not have each did what Chapter 01 says |
| The walkthrough test (`?walktest=1`) | 11 chapters of the three lab sets were rewritten for a changed build, and no value of the book was left. Since 2026-11-24 the test sets a VLAN ID for every shared segment, because a VLAN ID no longer changes with a subnet. On that day it found one address that Chapter 06 of Volume CCI wrote as a pattern, which the chapter now writes out. It also reads the supernet row of the Segments table in the copy of Chapter 999, which has to name the supernet of the build with its first and its last address. That last address is the one address of a copy that is in no subnet of the build |
| A zip for a build with all three lab sets | 28 files, none missing, with the 11 lab chapters. With a Junos device as the gateway it has 30 files, because the two files of the gateway text join them |
| The zip test (`?ziptest=1`), on 2026-11-24 | The 23 files of a new build, none missing |
| A build named 305, on 2026-11-27 | No text of the page and no file of the zip kept a name with 201, apart from the IPv6 addresses, the Proxmox VM IDs from 20100, and the guest type `windows2019srv_64Guest`. The zip held `Deploy-Lab305-Workstation.ps1` and `common/lab305-vms.json`. The renamed copies of the scripts parse. `make-seed.py` ran on the renamed manifest for cloud-init and for WSL, and its seeds have the renamed files, services, and machines. The renamed Workstation script passed `-Action Check` and ran `-WhatIf` for the 12 machines of the build, on Workstation 26.0. Nothing was built |
| Passwords and keys in `make-seed.py`, on 2026-11-27 | The SHA-512 crypt hash equals the one of `openssl passwd -6` for four passwords and salts, one with characters outside ASCII, and the example of the specification. A missing key was made in a new folder with no passphrase, and with one. A public key was written from a private key that was there alone. A preview left a missing key out and made nothing. A hardened machine was built with `LAB201_ADMIN_PASSWORD`, and refused without a password. The Workstation script's `-Action Check` and `-WhatIf` reported a missing key and did not make it |
| `scripts/python/check_lab_scripts.py` | The scripts parse, and 18 seed runs wrote 212 seeds. Since 2026-11-24 it also writes the seeds of the plan in another address block, and it found no address of the manifest's block in their 36 files. Since 2026-11-26 it also runs the self-test of `make-ckl.py` and compares the 329 requirement rows that the script reads from the lab chapters with those of the page |
| The checklist script (`common/make-ckl.py`), on 2026-11-26 | From the results file of the page for a build with all three lab sets, and from DISA's library of October 2026, it wrote 11 checklists: four SRGs for each switch, two for `faz-202`, and one for `fmg-203`. A schema validator found all 11 valid against the checklist schema 2.5. The same files came from the lab chapters of the repository and from the chapter copies of the published folder, and from the folder of SRG zips and from the library zip alone |
| The statuses of the checklists, on 2026-11-26 | A made-up `PROGRESS.md` went through the page into a results file. It had a passed requirement lab, a passed gap lab of each lab set, a blocked lab, a skipped lab, a passed requirement that is met in part, and a failed requirement. A second script, with code of its own, read the chapters and that results file and compared the 351 pairs of a device and a requirement that have a rule with the checklists. It found no difference |
| The `.cklb` format, on 2026-11-27 | The script built the rules of three benchmarks of DISA's library, and they were compared with files that other programs wrote for the same benchmarks. In the file that STIG Viewer 3 saved, 41 rules have the revision that the library of October 2026 has. In each of them all 28 fields that come from the benchmark are the same, and so are the name, the short name, and the identifier of both benchmarks. In the file of the SCAP Compliance Checker, for the same release of the Microsoft Edge STIG, 21 of the 28 fields are the same in all 61 rules. The checker does not write one field, and the other six differ in the way it writes them, or because it reads the SCAP benchmark |
| The statuses in both formats, on 2026-11-27 | The made-up results of the day before were written in both formats. The second script found no difference in the 351 pairs of the `.cklb` files and none in those of the `.ckl` files. The `.ckl` files are valid against the checklist schema 2.5 and are the same as the day before, byte for byte |
| `scripts/bash/validate.sh` | Passes, with the sync check, the stated numbers, and the address plan |
| `scripts/bash/build-download-site.sh`, in a scratch copy with stand-in book pages, on 2026-11-22 | The folder, the zip, the forward at the old address, the link under **Interactive companions**, and the links with `?sets=` on the three portal pages were written, and the link check of the script passed |

The commit of the move and the links was pushed on 2026-11-22, and the published site was checked after its deploy. The page of that day did not have the fields of sections 10 and 11 yet.

| Check on the published site | Result on 2026-11-22 |
| --- | --- |
| The `Validate` and `Deploy Pages` workflows of the commit | Both passed |
| The published page | It is the file of the repository, byte for byte. Its self-test and its walkthrough test gave the results of the local copy, and its zip test (`?ziptest=1`) found the 23 files of a new build with none missing |
| The published files | The page, the catalog, the diagram, the 11 lab chapters, and the zip of the scripts answer at their new addresses. The old address of the zip returns 404, as this chapter says above |
| The forward | The old address of the Lab Builder opens the Lab Selector |
| The link under **Interactive companions** | It is on the start page of the site, with the address of the page |
| The links with `?sets=` | The portal pages of Volumes CCI, CCII, and CCIII each have the link with their lab set, and the book pages of the four volumes have theirs. The link on the portal page of Volume CCII was followed: it ticked the FortiAnalyzer lab set, the address lost its `sets` part, and a reload kept the result. A link with two lab sets ticked both |

The commit of the table of the lab networks was pushed on 2026-11-24, and the published site was checked after its deploy. That page still had a /24 for each network.

| Check on the published site | Result on 2026-11-24 |
| --- | --- |
| The `Validate` and `Deploy Pages` workflows of the commit | Both passed |
| The published page | Its self-test passed 301 checks, its walkthrough test rewrote 11 chapters, and its zip test found the 23 files of a new build with none missing |
| The table of section 6 | 16 rows in the order of their addresses, with fields on the shared segments only |
| The width of the window | The page did not scroll sideways at any of 14 widths from 1,280 to 375 pixels |

Not tested:

- **A person on the published site.** The published site was checked with the test modes of the page and by reading the published files. No person has run Lab 1.1 of Chapter 01 there. No zip was saved from the published page, and the zip of the scripts was not downloaded: the check read its headers only.
- **The fields of sections 10 and 11 on the published site.** They were tested on 2026-11-23 on a local copy of the published folder, before the change was pushed, so this chapter holds no check of them on the published site. No device and no firewall has taken a text that the page wrote.
- **A block of its own size for each lab network, on the published site.** It was tested on 2026-11-24 on a local copy of the published folder, before the change was pushed, so this chapter holds no check of it on the published site.
- **A build.** No machine was built again after the block changed to `10.200`, and none with a block of its own size for each network. The seeds of the new plan were written and read, and no hypervisor has run them. The firewall of the gateway with the new blocks, a DHCP scope of seven addresses, and a FortiLink interface on a /30 have not run. No host of the FortiAnalyzer or FortiManager lab set has been built. The lab sign-offs of Volumes CCI, CCII, and CCIII are pending.
- **Other browsers.** The page was tested in one Chromium browser.
- **The checklists in STIG Viewer.** No checklist was opened in STIG Viewer 2 or 3. A `.cklb` file has the keys, their order, and the rule fields of a file that STIG Viewer 3 saved, and a `.ckl` file follows the schema of STIG Viewer 2. That is not the same as the program opening them. The values `active`, `mode`, and `has_path` belong to the window of STIG Viewer 3. The script writes the values that files of other programs carry, and what STIG Viewer 3 does with them is not known here.
- **Checklists from real lab results.** No lab has run, so every status in the test came from a made-up progress file.

### Lessons learned

- **An attribute name in the page must be one that the picture does not use.** The first Labs card marked its buttons with `data-kind`. The diagram marks its boxes with the same attribute, so the page tried to restyle parts of the picture and failed. The card uses `data-labkind` and `data-labset` now.
- **Keep the old checks, and make them mean the same.** The 254 checks of the Lab Builder ask for the labs, the walkthroughs, and the lab plan of the build. With lab sets, those three lists became *the ones of this build*, so the old checks still test a FortiSwitch build without a change, and only one check that counted the cards needed a new number.
- **A text that is built from choices needs a build with the choice off.** The first version of the license list still asked for the switch licenses in a build with no switch labs. A check on a build with the FortiSwitch lab set cleared found it.
- **Look at a new part of the page, and do not only test it.** The checks of the fields passed while the line beside each field wrapped in an ugly way. No check looks at the layout, so a new part needs a look at the width of a desktop and of a phone.
- **A table that shows part of a plan is read as the plan.** The table of section 6 had the seven segments that a reader can change, and the nine other networks stood in small text under it. The plan was complete, and a reader still saw it start at the third subnet. Show every row where the reader looks, and mark the rows that can be changed.
- **One number with three meanings is three assumptions in the code.** The number of a segment was also its VLAN ID and the third octet of its subnet. The page, the seed script, and the sync script each took an address apart by its octets, in dozens of places, and each place had to change when a subnet became a block. Ask one function which network holds an address.
- **A check that builds only the plan of the book cannot find what follows a choice.** From the day the block moved until 2026-11-24, the firewall of the gateway had the IPv4 networks of the book in a build that had other ones, and every check passed. A check of something that follows the choices needs a build with other choices: the check of the lab scripts now writes the seeds of a plan in another block and looks for an address of the first one.
- **Find out what a network has to hold before you give it a size.** The count of the addresses found 18 in Lab-Services, where a /28 has 14. The lab text found the rule of Lab 6.6 that a peer has to advertise a /24. Neither showed in the Segments table.
- **Serve a test copy from a plain web server that writes its log to a file.** A server whose output went to a pipe stopped answering during the tests, and the browser then waited without an error.
- **A passed lab is not always a requirement that is met.** A gap lab passes when it proves that a setting is absent. The first design of the checklist script took every pass as Not a Finding. That would have recorded 31 requirements that the product cannot meet, 20 that do not apply, and 18 that are met in part as compliant. The chapters hold the difference, in the title of the lab and in the alignment cell, so the script reads them.
- **A format with no schema is what its own program writes.** Public `.cklb` files of other generators put the SRG number into `group_title`, and one field was remembered as a font size. A file that STIG Viewer 3 itself saved showed the title of the rule in `group_title` and the number of the rules in `size`. Compare with a file of the program that will read the output, and not with the files of other writers.

## Validation and Troubleshooting

To check this volume:

- **The data.** `python scripts/python/sync_lab_selector.py --check` confirms that the page holds the current manifest, flavors, catalog, and lab data, that the numbers in the documents are right, and that the address plan agrees with the manifest and holds every address.
- **The scripts.** `python scripts/python/check_lab_scripts.py` confirms that the build scripts parse, that the seed tool works for every flavor, and that the seeds of a plan in another address block hold no address of the first one.
- **The page.** Publish the folder to a scratch directory with `scripts/python/package_lab_scripts.py` and the files that `sync_lab_selector.py --package-args` lists, serve it, and open `selector/lab-selector.html?selftest=1`.
- **The published page.** After a deploy, open the published page with `?selftest=1`, with `?walktest=1`, and with `?ziptest=1`, and compare the published file with the file of the repository. The table of the published site above shows such a check.
- **Repository checks.** `scripts/bash/validate.sh` runs the first two, and checks `book.yml`, internal links, markdownlint, and cspell.

| Symptom | Cause | Fix |
| --- | --- | --- |
| A link to `lab-scripts/builder/lab-builder.html` in a document | The document still names the old page | Use `lab-scripts/selector/lab-selector.html` under `downloads/volume-901-lab-selector/` |
| A link to the old zip of the scripts returns 404 | The zip has a new address and no forward | Use `downloads/volume-901-lab-selector/volume-901-lab-selector-lab-scripts.zip` |
| The self-test reports one more or one fewer check than Chapter 01 states | A check was added or removed | Correct the number in Chapter 01. The sync check names the line |
| A script of Volume CCI's Chapter 90 is named `sync_lab_builder.py` | That chapter records the name of its day | The script is `sync_lab_selector.py` now |

## Security and Best Practices

- **Search the added lines before a push.** The repository is public. Before a commit of this volume is pushed, search what it adds for an address of a real host, a key path, a token, and an email address.
- **Keep the console password proposal a proposal.** It is published with the page. The chapters say so wherever they name it.
- **Do not commit a build.** A zip from the page, a `licenses.local.json`, and an evidence folder belong to one lab, not to the repository.
- **Keep this chapter current.** When the page, the catalog, or a script changes, update this chapter in the same commit.

## References and Knowledge Checks

**References:**

- [Volume CCI, Chapter 90](../../volume-201-fortiswitch-stig-and-srg-mapping/chapters/90-as-built-how-this-volume-was-built.md) for the history of the page and the scripts before the move.
- [Chapter 01](01-the-lab-selector.md) and [Chapter 02](02-lab-data-and-how-to-add-a-lab-set.md) of this volume.
- `scripts/python/sync_lab_selector.py`, `scripts/python/package_lab_scripts.py`, and `scripts/bash/build-download-site.sh` in this repository.
- The repository's commit history (`git log --follow` on a file of the `lab-scripts` folder).

**Knowledge checks:**

1. Where were the page and the scripts built, and when did they move here?
2. Which names stayed after the move, and why?
3. Why is a new build a FortiSwitch build?
4. What was checked on the published site after the deploy, and what about it is not tested?
5. Why did the first Labs card break the diagram?
6. Which old address forwards, and which does not?
7. What does the page do with a link that names lab sets, and why does such a link count once?
8. Which values do sections 10 and 11 ask for, when does section 11 not ask for the address of the gateway, and when does section 10 ask for nothing?
9. Why do the rows of the table in section 6 follow the addresses and not the segment numbers, and when does a row not move?
10. Which lab networks are not a /28, and what decides the size of each of them?
11. Which networks have the same block in every build, and what does the reader gain by that?
12. Why did the check of the lab scripts not find the fault in the firewall of the gateway, and what does it do now?
13. Which status does a passed gap lab give a requirement in a checklist, and where does the checklist script learn that a lab is a gap lab?

## Summary and Completion Checklist

The Lab Selector and the lab scripts were built in Volume CCI and moved here on 2026-11-20, when the page was renamed and given lab sets for FortiSwitch, FortiAnalyzer, and FortiManager. The lab network moved to `10.200.0.0/16` on the same day. Since 2026-11-22 a link can open the page with lab sets ticked, and since 2026-11-23 sections 10 and 11 ask for the values that their texts left as placeholders. Since 2026-11-24 the table of section 6 lists every lab network of the build, from the first subnet on, and each lab network takes a block of its own size, a /28 unless it needs another size. The page passes 322 checks on a local copy of the published folder. Since 2026-11-27 a build has a lab name, which renames everything it writes, its zip extracts to one folder, Workstation Pro 26H1 U1 is the one Workstation release, the uplink of the gateway is kept unless you clear its box, every password starts with one lab password, and the build makes a missing SSH key. On the published site, the new addresses, the forward, and the links were checked on 2026-11-22, with the page of that day. A build and the hosts of the two new lab sets are not tested yet. Since 2026-11-26 a script of the folder writes checklists for DISA STIG Viewer from the results of the labs, and no checklist has been opened in STIG Viewer yet.

- [ ] Can say what moved, what was renamed, and what stayed.
- [ ] Can explain the lab sets, the prefixes, and the hosts that no script builds.
- [ ] Can run the checks of the data, the scripts, and the page.
- [ ] Knows what is not tested yet.
