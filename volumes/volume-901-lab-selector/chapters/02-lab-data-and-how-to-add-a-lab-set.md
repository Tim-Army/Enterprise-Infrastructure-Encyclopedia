# Chapter 02: Lab Data and How to Add a Lab Set

## Learning Objectives

- Name the files that the Lab Selector works from, and what each one holds.
- Say what the sync script reads from a lab chapter, and what a chapter needs so that it can be read.
- Explain why a lab of another volume has a prefix, and where the prefix shows.
- Add a lab set to the catalog, and check the result.
- Say what a new kind of labs needs before it can be chosen on the page.

## Theory and Architecture

### The files

The Lab Selector, its data, and the build scripts are in the `lab-scripts` folder of this volume. Five scripts outside the folder keep them in step and publish them.

| File | What it holds |
| --- | --- |
| `selector/lab-selector.html` | The page. It carries a copy of the four data files below and of the lab data, so it works with no server |
| `common/lab-catalog.json` | The catalog: the kinds of labs, the shared lab, and the lab sets with the lab chapters of each one |
| `common/lab201-vms.json` | The manifest: the twelve machines of the shared lab, their sizes, networks, and IPv4 addresses, and the IPv4 block of every lab network (`segments`). The build scripts read it |
| `common/flavors.json` | The Linux flavors, their package names, and the machine types each one can run |
| `common/fortiswitch-features.json` | Which FortiSwitch model series support the features that the FortiSwitch labs use |
| `common/make-seed.py`, `common/resolve-image.py` | The seed tool and the image resolver of the build scripts |
| `esxi/`, `vcenter/`, `workstation/`, `proxmox/`, `kvm/`, `wsl/` | One build script for each platform |
| `scripts/python/sync_lab_selector.py` | Copies the data files and the lab data into the page, and checks the numbers that the documents state |
| `scripts/python/check_lab_scripts.py` | Checks that the build scripts parse and that the seed tool writes a seed for every machine |
| `scripts/python/package_lab_scripts.py` | Publishes the folder as files and as one zip, with a `SHA256SUMS` file |
| `scripts/python/build_fortiswitch_features.py` | Builds `fortiswitch-features.json` from Fortinet's feature matrix |
| `scripts/bash/build-download-site.sh` | Calls the packaging script, and links the page on the portal |

The file names keep `lab201`, the host names keep `-201`, and the IPv6 prefix keeps `fd00:db8:201::`, although the folder is in this volume now. Those names are in every lab chapter and in labs that are already built, so a new name would break more than it would explain.

### The catalog

`common/lab-catalog.json` has three parts.

- **`kinds`** lists the kinds of labs: an `id`, a `name`, and a line of text (`sub`). The page shows every kind. A kind can be chosen when at least one lab set has it.
- **`base`** names the shared lab: its `volume`, the `chapter` that builds it, the `short` name of that chapter in the zip, and its `diagram`. `always` lists the labs of that chapter that every build has. `set` names the lab set that the other labs of the chapter belong to.
- **`sets`** lists the lab sets. Each one has an `id`, its `kind`, a `name`, its `volume` and the Roman numeral of that volume (`roman`), a `prefix`, and a line of text (`about`). `selected` marks the lab set that a new build has. `switches` marks the lab set that runs on the two switches under test. `shared` names the chapter that builds the hosts of the set, if it has one. `chapters` lists its lab chapters. Every chapter has its `file`, a `short` name for the zip, and a `name` for the lab plan.

The `id` of a lab set is also its name in a link: `lab-selector.html?sets=<id>` opens the page with that lab set ticked ([Chapter 01](01-the-lab-selector.md)). An id therefore has lowercase letters, digits, and hyphens only, and it should not change once a link to it is published.

A short name keeps the paths in the zip short for Windows, and it has to be unique, because the chapters of several volumes share one folder there. The short names of a lab set start with its prefix.

### What the sync script reads from a chapter

`scripts/python/sync_lab_selector.py` reads the chapters that the catalog names. It finds these things by their form, so a chapter has to keep that form:

| What | Where it is read | The form it needs |
| --- | --- | --- |
| A lab | Every lab chapter | A heading `### Lab N.M — Title`, with an em dash |
| The SRG requirements of a lab | The table of the lab | Rows that start with the SRG ID in backticks, then the category (I, II, or III), then the requirement |
| The switch a lab runs on | The **Uses.** line of a FortiSwitch lab | The host name of a switch in backticks, or the words *both switches* |
| The machines a lab uses | The whole text of the lab | The name of a machine of the manifest, or a service name of the shared lab, in backticks |
| The hosts a lab uses that no script builds | The **Uses.** line | The name of such a host in backticks |
| The lab networks a lab uses | The whole text of the lab | An address in the block of a lab network, or the name of a host that has one |
| The service names and the networks of the shared lab | The Hosts table and the Segments table of its Chapter 999 | The columns of those two tables |
| The hosts of a lab set | The **Address plan** table of the Chapter 999 of the set | The columns Host, Role, From, IPv4, and IPv6 |

The **Address plan** table decides what a lab set adds. A row whose **From** cell is *This volume* is a host that the set adds. A row from the volume of another lab set is a host of that set which this one reuses. A row from the volume of the shared lab is one of its machines or service names, which the lab text already ties to the set. The word *(optional)* in the **Role** cell marks a host that only an optional step needs.

The script says what it could not use: a lab with no **Uses.** line, a host name in a **Uses.** line that it does not know, a host whose address is in no network of the shared lab, and a reused host that its own volume does not add.

### Lab ids and prefixes

A lab has a number, which is the one in its chapter, and an id. For the lab set with an empty prefix, the id is the number. For every other lab set, the id is the prefix, a hyphen, and the number: `faz-3.1`. The id is what the page stores for a lab that you left out, what `PROGRESS.md` and the evidence folders use, and what the results file lists. The page prints such a lab as *FortiAnalyzer Lab 3.1*.

Only one lab set can have an empty prefix: the one the shared lab was written for. The script stops when two labs have the same id.

### What is published where

The site build publishes the folder under `downloads/volume-901-lab-selector/`:

- `lab-scripts/`, the files of the folder, with `SHA256SUMS`.
- `lab-scripts/walkthroughs/`, the lab chapters that the catalog names, each under its short name. The page fetches them for its zip.
- `lab-scripts/diagrams/lab-topology.svg`, the diagram of the shared lab, with a PNG copy when `rsvg-convert` is installed.
- `volume-901-lab-selector-lab-scripts.zip`, the same files in one zip.

The portal links the page under **Interactive companions** and on the page of this volume. The portal page of the volume of each lab set has a link that opens the page with that lab set ticked. `sync_lab_selector.py --set-links` gives the site build the lab sets for those links. Until 2026-11-20 the folder was published under `downloads/volume-201-fortiswitch-stig-and-srg-mapping/`. A page at the old address of the Lab Builder forwards to the Lab Selector. The old address of the zip has no forward.

## Design Considerations

- **One catalog entry, and the rest is read.** A lab set is a few lines in the catalog. Its labs, its requirements, its machines, and its hosts come from its chapters, so they cannot drift from the book.
- **A lab set owns its hosts.** A host is added by one lab set. Another lab set that needs it says so in its own **Address plan** table, and the page then lists the host once, with every set that needs it.
- **The scripts build the shared lab only.** The manifest has the twelve machines of the shared lab. A host of a lab set is a host that no script builds, until someone writes a role for it in the seed tool and tests the build on a hypervisor.
- **A kind is a label on a lab set.** The page has no code for one kind of labs. A certification lab set and a learning lab set are read like an SRG lab set, and a lab with no SRG table simply has no requirement rows.
- **Numbers in the text are checked.** A document that states how many labs or requirements a lab set has is in the `STATED` list of the sync script, so the number cannot go stale without a failed check.

## Implementation and Automation

### Commands

Copy the data into the page after a change to a data file or to a lab chapter:

```bash
python scripts/python/sync_lab_selector.py
```

Check that the page and the stated numbers are in step, as `validate.sh` does:

```bash
python scripts/python/sync_lab_selector.py --check
```

List the files that the site build adds to the published folder:

```bash
python scripts/python/sync_lab_selector.py --package-args
```

List the lab sets for the links on the portal pages:

```bash
python scripts/python/sync_lab_selector.py --set-links
```

### Add a lab set

1. **Check the lab chapters.** Each lab has a heading in the form `### Lab N.M — Title`, a **Uses.** line, and, for a requirement lab, a table of SRG IDs. The `/srg-labs-for` workflow writes chapters in this form, and its check confirms it.
2. **Check the Chapter 999 of the volume.** If the labs need hosts of their own, the chapter needs an **Address plan** table with the columns Host, Role, From, IPv4, and IPv6. Give each new host an address in a network of the shared lab, and say *(optional)* in the role of a host that only an optional step needs.
3. **Add the lab set to `common/lab-catalog.json`.** Choose a prefix that no other lab set has, and short names that start with it. Leave `selected` false, unless a new build should have the set.
4. **Run the sync,** and read its notes. Fix a chapter that it could not read.
5. **Test the page.** Publish the folder to a scratch directory as the site build does, serve it, and open the page with `?selftest=1`, then with `?walktest=1`. The walkthrough test rewrites every chapter of every lab set and reports a value of the book that is left.
6. **Update the documents.** Add the lab set to the tables in [Chapter 01](01-the-lab-selector.md), to this volume's README, and to the `STATED` list of the sync script. Give the README and the Chapter 999 of the lab set's volume a link to the page with `?sets=` and the id. The site build adds the same link to the portal page of that volume by itself. Record the change in [Chapter 90](90-as-built-how-this-volume-was-built.md).

### Add a kind of labs

The catalog already lists certification labs and learning labs, with no lab set. To give one of them its first lab set:

1. Decide which labs the set holds, and bring their chapters into the form above. A lab of a certification volume has no SRG table, so it has no requirement rows, like the console server labs of Volume CCI.
2. Decide what the labs run on. If they run on the shared lab, add the set as above with the `kind` of the labs. The kind can then be chosen on the page.
3. If the labs need machines that the manifest does not have, a catalog entry is not enough. List those machines as hosts that no script builds, in an **Address plan** table. To have the scripts build them, extend the manifest and the seed tool, and test the build on a hypervisor before you publish it.
4. If the labs need a network that the shared lab does not have, add it to the Segments table of the shared lab first. The page gives a subnet only to a network of that table. Give the network the lowest free block that holds its hosts, a /28 unless it needs another size, and add the same block to the `segments` list of the manifest. The sync script compares the two and reports a difference. The first row of the Segments table is the supernet of the lab, with its first and its last address. It is no network, and its first cell is no number, so the script and the page do not read it as one. When a new network makes the lab larger than that block, correct the row by hand: the script names the supernet that the networks need.

## Validation and Troubleshooting

| Message or symptom | Cause | Fix |
| --- | --- | --- |
| `lab selector data: OUT OF DATE` | A data file or a lab chapter changed after the last sync | Run the sync without `--check` |
| `stated numbers: WRONG` | A document states a number that the chapters or the page do not give | Correct the document. If the sentence changed, change `STATED` in the script |
| `two labs have the id ...` | Two lab sets have the same prefix, or two have an empty one | Give one lab set another prefix |
| `gives the short name ... to more than one chapter` | Two chapters of the catalog have the same short name | Change one short name |
| `Lab ... has no Uses line` | A requirement lab does not say what it runs on | Add the **Uses.** line |
| `address plan: WRONG` | The Segments table of the shared lab, the `segments` list of the manifest, and the addresses do not agree. The lines under the message name each case: two blocks that overlap, a block that differs between the two, an address in no block, or a supernet row that is not the supernet of the networks under it | Correct the table, the manifest, or the address |
| `... has the address ..., which is in no block of the Segments table of the shared lab` | A host of a lab set is outside every lab network | Move the host, or add the network to the shared lab |
| A lab set has no host on the page | Its Chapter 999 has no **Address plan** table, or the **From** cells have other words | Use *This volume* or *Volume* and the Roman numeral |
| The zip has `MISSING-FILES.txt` after a new lab set | The published folder does not have the new chapters yet | Deploy the site, or publish the folder to a scratch directory for the test |

## Security and Best Practices

- **Keep keys and private values out of the data files.** The catalog, the manifest, and the page are published. They hold lab addresses and a proposed console password, and nothing else that is private.
- **Use lab addresses only.** A host of a lab set takes an address of the lab block. Do not put an address of a real network into a chapter that the page reads.
- **Test a new role before the scripts build it.** A machine that the seed tool builds is installed with packages from the internet. Build it on a test hypervisor first, with the preview and the readiness check.
- **Read the notes of the sync.** A note means the page knows less than the chapter says, for example which hosts a lab needs.

## References and Knowledge Checks

**References:**

- [Chapter 01](01-the-lab-selector.md) for the page and its options.
- The `lab-scripts/README.md` of this volume, for the build scripts.
- [Volume CLXXII, Chapter 90](../../volume-172-disa-srgs-and-stigs/chapters/90-as-built-how-this-volume-was-built.md) for the `/srg-labs-for` workflow, which writes lab chapters in the form the sync script reads.
- `scripts/python/sync_lab_selector.py` in this repository. Its first lines describe every part of the lab data.

**Knowledge checks:**

1. Which file lists the lab sets, and which three parts does it have?
2. What does a row of an **Address plan** table need so that the page lists the host for a lab set?
3. Why does `faz-3.1` have a prefix, and where is the id used?
4. What is missing when a kind of labs shows *none yet*?
5. Why is a new host of a lab set not built by the scripts?
6. Which command tells you that a document states a wrong number?

## Summary and Completion Checklist

The Lab Selector works from one catalog and from the lab chapters that it names. The sync script reads the labs, their requirements, their machines, and the hosts of each lab set from those chapters, copies the result into the page, and checks the numbers that the documents state. A lab set is added with a catalog entry, and a kind of labs can be chosen as soon as a lab set has it.

- [ ] Can name the data files and say what the sync script does with them.
- [ ] Can say what a lab chapter and a Chapter 999 need so that the page can read them.
- [ ] Can add a lab set to the catalog, run the sync, and test the page.
- [ ] Knows what a lab set needs beyond a catalog entry when its labs need new machines.
