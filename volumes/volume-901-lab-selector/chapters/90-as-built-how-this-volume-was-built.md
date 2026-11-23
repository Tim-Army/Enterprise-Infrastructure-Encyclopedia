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
| The address plan | 2026-11-19, in Volume CCI | The segments were renumbered so that the subnets are contiguous | The block moved from `10.201.0.0/16` to `10.200.0.0/16` on 2026-11-20 |
| `common/lab-catalog.json` | 2026-11-20 | Written by hand, in place of the list of walkthrough chapters that the page had before | Add a lab set here |
| The lab data of the FortiAnalyzer and FortiManager lab sets | 2026-11-20 | Read from the lab chapters of Volumes CCII and CCIII by `scripts/python/sync_lab_selector.py` | Regenerate after a chapter changes |
| Links that tick lab sets | 2026-11-22 | The page reads `?sets=` and the ids of lab sets from its address, once. The site build and the documents of the three product volumes link to the page with their lab set ticked | None |
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

### What was tested, and what was not

| Check | Result on 2026-11-22 |
| --- | --- |
| The self-test of the page (`?selftest=1`) | 276 checks pass in a Chromium browser, on a local copy of the published folder. 254 of them are the checks the Lab Builder had, 18 check the lab sets, and 4 check the links |
| Links at the start of the page, tried by hand | A visitor with no kept choices, a reload after the link, a link on top of kept choices, and a link with names that the page does not have each did what Chapter 01 says |
| The walkthrough test (`?walktest=1`) | 11 chapters of the three lab sets were rewritten for a changed build, and no value of the book was left |
| A zip for a build with all three lab sets | 28 files, none missing, with the 11 lab chapters |
| `scripts/python/check_lab_scripts.py` | The scripts parse, and 18 seed runs wrote 212 seeds |
| `scripts/bash/validate.sh` | Passes, with the sync check and the stated numbers |
| `scripts/bash/build-download-site.sh`, in a scratch copy with stand-in book pages | The folder, the zip, the forward at the old address, the link under **Interactive companions**, and the links with `?sets=` on the three portal pages were written, and the link check of the script passed |

Not tested:

- **The published site.** The page was tested on a local copy of the published folder. The new addresses, the forward at the old address, the link under **Interactive companions**, and the links with `?sets=` have to be checked after the site is deployed.
- **A build.** No machine was built again after the block changed to `10.200`, and no host of the FortiAnalyzer or FortiManager lab set has been built. The lab sign-offs of Volumes CCI, CCII, and CCIII are pending.
- **Other browsers.** The page was tested in one Chromium browser.

### Lessons learned

- **An attribute name in the page must be one that the picture does not use.** The first Labs card marked its buttons with `data-kind`. The diagram marks its boxes with the same attribute, so the page tried to restyle parts of the picture and failed. The card uses `data-labkind` and `data-labset` now.
- **Keep the old checks, and make them mean the same.** The 254 checks of the Lab Builder ask for the labs, the walkthroughs, and the lab plan of the build. With lab sets, those three lists became *the ones of this build*, so the old checks still test a FortiSwitch build without a change, and only one check that counted the cards needed a new number.
- **A text that is built from choices needs a build with the choice off.** The first version of the license list still asked for the switch licenses in a build with no switch labs. A check on a build with the FortiSwitch lab set cleared found it.
- **Serve a test copy from a plain web server that writes its log to a file.** A server whose output went to a pipe stopped answering during the tests, and the browser then waited without an error.

## Validation and Troubleshooting

To check this volume:

- **The data.** `python scripts/python/sync_lab_selector.py --check` confirms that the page holds the current manifest, flavors, catalog, and lab data, and that the numbers in the documents are right.
- **The scripts.** `python scripts/python/check_lab_scripts.py` confirms that the build scripts parse and that the seed tool works for every flavor.
- **The page.** Publish the folder to a scratch directory with `scripts/python/package_lab_scripts.py` and the files that `sync_lab_selector.py --package-args` lists, serve it, and open `selector/lab-selector.html?selftest=1`.
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
4. Which three things about the published site still need a check after a deploy?
5. Why did the first Labs card break the diagram?
6. Which old address forwards, and which does not?
7. What does the page do with a link that names lab sets, and why does such a link count once?

## Summary and Completion Checklist

The Lab Selector and the lab scripts were built in Volume CCI and moved here on 2026-11-20, when the page was renamed and given lab sets for FortiSwitch, FortiAnalyzer, and FortiManager. The lab network moved to `10.200.0.0/16` on the same day. Since 2026-11-22 a link can open the page with lab sets ticked. The page passes 276 checks on a local copy of the published folder. The published site, a build, and the hosts of the two new lab sets are not tested yet.

- [ ] Can say what moved, what was renamed, and what stayed.
- [ ] Can explain the lab sets, the prefixes, and the hosts that no script builds.
- [ ] Can run the checks of the data, the scripts, and the page.
- [ ] Knows what is not tested yet.
