# Chapter 04: Dial Plans, Call Control Features, and Mobility

## Learning Objectives

- Design a dial plan with partitions and calling search spaces that
  expresses class of service as policy
- Build route patterns, route lists, and route groups with digit
  manipulation at the right layer
- Explain globalized (+E.164) dial plan design and why it scales
  where site-prefix schemes collapse
- Configure the features CLACC weights: hunt constructs, call park
  and pickup, transfer and forward chains
- Deliver mobility: extension mobility, single number reach, and
  SRST survivability

## Theory and Architecture

### Partitions and calling search spaces: policy as containment

The dial plan's security model is two objects. A **partition** is a
label on things that can be called (DNs, patterns). A **calling
search space (CSS)** is an ordered list of partitions a caller may
see. Class of service falls out: internal-only phones carry a CSS
listing internal partitions; international callers get the partition
holding the international route pattern. The ordering matters — first
match by partition order breaks closest-match ties — and the
line/device CSS interaction (they concatenate, line first) enables
the classic design: device CSS carries site-routing, line CSS carries
user-class restrictions.

### Route patterns to gateways: the routing pipeline

A call to a non-DN hits a **route pattern** (`9.011!#` style wildcards,
X, [], !, and the `.` that marks pre-dot strip boundaries), which
points at a **route list** (ordered strategy) of **route groups**
(gateway/trunk pools). Digit manipulation lives at defined layers:
called/calling transformations on the pattern, per-route-group digit
discipline, and **transformation patterns** applied at egress. The
design rule that keeps estates sane: **normalize early, localize
late** — convert everything to a canonical form (+E.164) on ingress,
route in canonical form, and reformat only at the egress trunk that
requires a local format.

### Globalized dial plans

The +E.164 design CLACC rewards: all DNs stored as +E.164; ingress
gateways globalize calling/called numbers; users dial habits
(4-digit, 9-prefixed) that **translation patterns** normalize;
routing operates on `\+!` patterns; egress localizes per trunk. What
it buys: one routing core for any number of sites, clean AAR/failover
(reroute-over-PSTN uses the same canonical number), and directory
integration that just works (directories store +E.164). Site-prefix
schemes (8-XXX-YYYY) persist in older estates and the exam expects
you to read both.

### The feature set

CLACC's Supplemental Features and Security domain (20%) is the daily-driver
list: **hunt pilots → hunt lists → line groups** (distribution
algorithms, hunting versus queuing); **call park/directed park** and
**pickup groups**; transfer and forward chains (CFA/CFB/CFNA and
their CSS contexts — forwarding uses the *forwarder's* permissions,
a recurring exam scenario); shared lines and barge; and **Native Call
Queuing** for simple front-office flows below contact-center scale
(Chapter 09 draws that boundary).

### Mobility

**Extension Mobility** logs a user profile into any phone — device
stays, identity moves. **Single Number Reach (Mobile Connect)** rings
desk and mobile simultaneously with mid-call pull-back;
**Mobile Voice Access/Enterprise Feature Access** extends dialing
from outside. **Device Mobility** re-homes roaming phones' pool
settings by IP subnet. And **SRST** completes Chapter 01's
availability story: the branch router answers registrations during
WAN loss, with `call-manager-fallback` or SIP SRST carrying a
reduced dial plan — design decision: what must still work (site
calls, PSTN 911 egress) versus what may wait.

## Design Considerations

- **CSS/partition design is done on paper first**: a matrix of
  caller-classes versus callable-classes, then the minimal partition
  set that expresses it. Retrofitting class-of-service is painful;
  the matrix is an afternoon.
- **One canonical form** (+E.164) unless a legacy interop forces
  otherwise — and then contained at that boundary with
  transformations.
- **Feature sprawl is real**: park/pickup/hunt inventories need
  owners and documentation, or the estate accumulates orphaned
  pilots nobody dares delete.
- **SRST scope honesty**: emergency calling and site-internal
  dialing always; headline features rarely — publish what branch
  users keep during WAN loss.

## Implementation and Automation

The lab dial plan, globalized:

```text
! Partitions: PT-INTERNAL, PT-LOCAL-PSTN, PT-INTL-PSTN, PT-TRANSLATE
! CSS: CSS-INTERNAL = [PT-TRANSLATE, PT-INTERNAL]
!      CSS-UNRESTRICTED = [PT-TRANSLATE, PT-INTERNAL, PT-LOCAL-PSTN,
!                          PT-INTL-PSTN]

! DNs as +E.164 in PT-INTERNAL: \+15551002001 etc.

! Translation pattern (user habit -> canonical), in PT-TRANSLATE:
!  pattern 2XXX  -> called transformation: +1555100.2XXX (prefix)
!  pattern 9.!   -> strip pre-dot, globalize by site rules

! Route pattern in PT-LOCAL-PSTN:  \+1[2-9]XX[2-9]XXXXXX
!   -> RL-PSTN (RG-CUBE-PRIMARY, RG-CUBE-BACKUP)
! Route pattern in PT-INTL-PSTN:   \+!   (urgent priority off)
! Egress localization at the CUBE route group:
!   called: DDI strip + to 9-format the ITSP expects (Chapter 05)
```

Representative feature and mobility builds:

```text
! Hunt: LG-HELPDESK (longest-idle) -> HL-HELPDESK -> HP +15551002900
! Park: directed park range +155510029[5-9]X with reversion 60s
! SNR: end-user Remote Destination Profile, mobile +1555210XXXX,
!      delay/answer timers tuned so voicemail races are won by CUCM
```

```text
! Branch SRST (IOS XE), the survivable minimum:
voice service voip
 allow-connections sip to sip
call-manager-fallback
 max-ephones 24
 max-dn 48
 ip source-address 10.60.10.1 port 2000
 dialplan-pattern 1 +1555100.... extension-length 4
```

## Validation and Troubleshooting

The dial plan's diagnostic instrument is the **Dialed Number
Analyzer** (and disciplined test calls): given calling device and
digits, it names the matched pattern, partitions consulted, and
transformations applied — evidence, not inference. Classic faults:
right pattern in a partition absent from the caller's CSS (DNA shows
the miss); closest-match surprises (a 2XXX translation shadowing a
specific DN); forward chains failing by CSS context (CFNA to
voicemail works from internal callers, fails from the PSTN — the
forwarder's CSS lacks the VM port partition); SNR answering to
mobile voicemail (timer race — tune delay-before-ring and
answer-too-soon); SRST fallback registering phones but failing PSTN
egress (fallback dial plan or FXO/trunk config at the branch).

## Security and Best Practices

- Class of service is toll-fraud defense: international and premium
  patterns live in partitions granted deliberately, with urgent
  priority and blocking patterns where policy demands.
- After-hours and lobby-phone CSS restrictions; forced authorization
  codes / client matter codes where billing requires.
- Audit the dial plan quarterly with DNA exports: unreachable
  patterns, orphaned features, and CSS drift are findings, not
  trivia.

## References and Knowledge Checks

- CLACC 300-815 v2.0 domains 3–4 (Advanced Call Control 25%,
  Supplemental Features and Security 20%)
- Cisco SRND dial plan chapters; Unified CM feature configuration
  guides

Knowledge checks:

1. Line CSS and device CSS both exist. Which wins a conflict, and
   what design exploits the concatenation order?
2. Why does "normalize early, localize late" simplify AAR and
   multi-site routing? Trace one call both ways.
3. A CFNA-to-voicemail works internally, fails from PSTN. Whose CSS
   is consulted, and what is missing from it?
4. Name what your SRST design preserves and abandons, and defend
   the emergency-calling line item.

## Hands-On Lab

Build the globalized plan above on the Chapter 03 estate: canonical
DNs, translation patterns for habits, class-of-service CSS matrix
(document the paper matrix first), PSTN patterns to a stub route
list. Prove with DNA and test calls: internal habit-dialing lands
canonically; a restricted phone is denied international by CSS (DNA
evidence captured); forwarding to voicemail works from both internal
and simulated-PSTN callers. Add the helpdesk hunt with
longest-idle, directed park with reversion, and SNR for one user
with tuned timers (demonstrate desk/mobile race won correctly).
Finally, take the branch to SRST: fail the WAN, show registration to
the router, a surviving site-internal call, and the documented
feature reduction; restore and confirm re-registration.

## Lab Verification

Verification means DNA evidence exists for the allow and deny
cases, the SNR race and forward-chain cases behaved by design, and
SRST fallback and recovery were both observed. Until then, the lab
is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The dial plan is policy: partitions and CSS express who may call
what, globalized routing keeps one core for any topology, features
ride the same containment, and mobility — EM, SNR, SRST — moves
identity without moving policy. This chapter is CLACC's center of
gravity and the second half of CLCOR's heaviest domain.

- [ ] My CSS matrix exists on paper and matches the build
- [ ] DNA evidence backs my allow/deny/forward cases
- [ ] My canonical core localizes only at egress
- [ ] SRST kept what I promised and nothing I did not
