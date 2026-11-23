# Volume CMI Glossary

Definitions for terms used in **Volume CMI — Lab Selector**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms and the
[Volume CCI glossary](../volume-201-fortiswitch-stig-and-srg-mapping/GLOSSARY.md)
for the terms of the shared lab and the build scripts.

- **Address plan table** — the table in the Chapter 999 of a lab set that lists its hosts, with a From column that says whether the volume adds a host or reuses the host of another volume. The Lab Selector reads the hosts of a lab set from it.
- **Build** — one set of choices on the Lab Selector: the lab sets, the labs, the platform, the machines, and the addresses. The page writes a manifest, the commands, a checklist, and the walkthroughs for it.
- **Catalog (`lab-catalog.json`)** — the file that lists the kinds of labs, the shared lab, and the lab sets with their lab chapters.
- **Choices file (`lab-selector-choices.json`)** — the file that holds a build, which the page saves and loads. A file that the Lab Builder saved loads too.
- **Host that no script builds** — a host of a lab set that you build by hand, such as a FortiAnalyzer-VM, because its image comes from the vendor under a license. The page lists it with its address and does not size it.
- **Kind of labs** — a group of lab sets: SRG labs, certification labs, or learning labs. A kind can be chosen on the page when it has a lab set.
- **Lab Builder** — the name of the Lab Selector until 2026-11-20, when it was a page of Volume CCI and built for the FortiSwitch labs only.
- **Lab id** — the name of a lab in the page, in `PROGRESS.md`, and in the evidence folders: its number, with the prefix of its lab set before it when the lab set has one (`faz-3.1`).
- **Lab plan** — the labs of the build that you plan to run. The page keeps the machines those labs use, and Claude skips the labs that are left out.
- **Lab Selector** — the page of this volume that plans a lab build for the labs you choose.
- **Lab set** — the labs of one volume, as the catalog lists them: its requirement lab chapters and, if it has one, the Chapter 999 that builds its own hosts.
- **Link with lab sets** — an address of the page that ends in `?sets=` and the ids of lab sets, such as `?sets=fortianalyzer`. The page starts with those lab sets ticked, once, and keeps the result.
- **Manifest (`lab201-vms.json`)** — the file that lists the machines of the shared lab, their sizes, networks, and IPv4 addresses. The build scripts read it, and the page writes a copy with your changes.
- **Port of the gateway device** — the trunk port or the out-of-band port of a network device that is the gateway of the lab. Section 10 of the page asks for both, and puts them into the gateway text in place of placeholders such as `<GW_TRUNK_PORT>`.
- **Prefix** — the short name of a lab set that comes before the number of its labs and the file names of its walkthroughs, such as `faz` and `fmg`. The FortiSwitch lab set has none.
- **Shared lab** — the gateway, the VLANs, and the service hosts of Volume CCI's Chapter 999, which every lab set runs on and which the scripts of this volume build.
- **Short name** — the name that a lab chapter has in the zip and in the published folder, kept short so that the paths stay short on Windows.
- **Stated number** — a count that a document gives in its text, such as the requirements of a lab set, which the sync script compares with the lab chapters.
- **Sync script (`sync_lab_selector.py`)** — the script that copies the data files and the lab data of the lab chapters into the page, and checks the stated numbers.
- **Value of the firewall text** — an interface of your firewall, or the address of the lab gateway, that section 11 of the page asks for. The page puts it into the external firewall text in place of a placeholder such as `<FW_LAB_INTERFACE>`.
- **Walkthrough** — the copy of a lab chapter in the zip, rewritten with the values of the build.
