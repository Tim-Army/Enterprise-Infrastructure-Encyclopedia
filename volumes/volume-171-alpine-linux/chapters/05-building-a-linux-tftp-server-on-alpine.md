# Chapter 05: Building a Linux TFTP Server on Alpine

## Learning Objectives

- Explain what TFTP is for and why its lack of authentication dictates how you
  deploy it.
- Install `tftp-hpa` and stand up `in.tftpd` on Alpine.
- Serve files from a dedicated, chrooted, read-only directory as a non-root user.
- Persist the daemon across reboots when the packaged service is inconvenient.
- Verify the server with a TFTP client and prove it against a real network-device
  firmware transfer.

## Theory and Architecture

**TFTP** (Trivial File Transfer Protocol) is a minimal UDP file-transfer protocol
on **port 69**. It has no authentication, no encryption, and a simple lockstep
transfer model. Those limits are also why it endures: network devices — switches,
routers, firewalls, PXE clients — can implement it in a tiny boot ROM, so it is the
lowest common denominator for pushing **firmware images, boot files, and device
configurations** onto infrastructure. This volume's server exists for exactly that:
to stage a FortiGate firmware `.out` that the firewall pulls over TFTP
([Volume XIX, Lab 4.8](../../volume-019-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md)).

Alpine's TFTP server is **`in.tftpd`** from the **`tftp-hpa`** package (in the
**community** repository, Chapter 03). Its important flags:

| Flag | Meaning |
| --- | --- |
| `-l` / `--listen` | Standalone daemon mode (listen on the socket itself; detaches) |
| `-L` / `--foreground` | Like `-l` but stay in the foreground, logging to stderr |
| `-s` / `--secure` | `chroot` into the serving directory (requests are relative to it) |
| `-u <user>` | Run as an unprivileged user (default `nobody`) |
| `-c` / `--create` | Allow clients to *upload* new files (off by default — read-only) |
| `-a <addr>:<port>` | Bind to a specific address/port |

A safe default is **read-only, chrooted, unprivileged**: `in.tftpd -l -s -u nobody
/tftpboot`. Note there is no `-c`, so clients can only *download* — which is all a
firmware-staging server needs.

### The packaged-service caveat

`tftp-hpa` ships an OpenRC init script (`/etc/init.d/in.tftpd`) that reads options
from `/etc/conf.d/in.tftpd`. In practice the packaged `conf.d` variables do not
always line up with the installed init script, and the service fails to start with
a generic error. Rather than fight it, the pragmatic and durable approach on Alpine
is the **`local.d`** boot hook from Chapter 04: run `in.tftpd` from a
`/etc/local.d/*.start` script. That is the method this chapter's lab uses, and it is
how the reference homelab's TFTP box runs.

## Design Considerations

- **Dedicate a directory and keep it read-only.** Serve from `/tftpboot`, owned by
  the run-as user, with `-s` to chroot into it and no `-c` so nothing can be written
  in. A firmware server never needs upload.
- **Run as `nobody`, never root.** TFTP is unauthenticated; the daemon should hold
  the least privilege that still lets it read the serving directory.
- **Constrain the blast radius on the network.** Because there is no auth, network
  position *is* the access control: bind to the management subnet and firewall
  UDP/69 to the specific devices that need it.
- **Bring it up only when staging.** A firmware-staging server does not need to run
  continuously; enable it for the maintenance window and stop it afterward, or leave
  it up but tightly firewalled.
- **Size the disk for the payloads.** Firmware images are tens to hundreds of
  megabytes; a 100 GB data disk (this volume's box) comfortably holds several
  releases. Grow the filesystem first if the image ships small (Chapter 07).

## Implementation and Automation

Install the server and create the serving directory:

```sh
sed -i '/\/community/s/^#//' /etc/apk/repositories   # ensure community is enabled
apk update
apk add tftp-hpa
mkdir -p /tftpboot
chown nobody:nobody /tftpboot
chmod 0755 /tftpboot
```

Run the daemon read-only, chrooted, as `nobody`:

```sh
/usr/sbin/in.tftpd -l -s -u nobody /tftpboot
ps aux | grep -i '[i]n.tftpd'          # confirm it is running
```

Persist it across reboots with a `local.d` hook (Chapter 04):

```sh
cat > /etc/local.d/tftpd.start <<'EOF'
#!/bin/sh
/usr/sbin/in.tftpd -l -s -u nobody /tftpboot
EOF
chmod +x /etc/local.d/tftpd.start
rc-update add local            # enable the local.d hook at boot
rc-service local restart       # (re)launch it now
```

Stage a payload and verify its integrity before serving it:

```sh
cp FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out /tftpboot/
md5sum /tftpboot/FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out
# 5a7da77d58860321789b133e967bdb7d  ...-FORTINET.out
```

## Validation and Troubleshooting

Confirm the daemon is listening and serve a file to a client:

```sh
# On the server:
netstat -lnu | grep ':69 ' || ss -lnu | grep ':69 '   # UDP/69 bound
apk add tftp-hpa                                       # the same package ships the client

# From another host on the subnet:
tftp 10.30.99.50 -c get FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out
md5sum FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out    # must match the server's
```

Watch the transfer on the wire if it misbehaves:

```sh
apk add tcpdump
tcpdump -ni eth0 udp port 69
```

Common issues:

- **Client times out, no packets in `tcpdump`.** A firewall is dropping UDP/69, or
  the daemon is not running/bound — check `ps`/`ss` and any host or network filter.
- **`in.tftpd` will not start from the packaged service.** The `conf.d` options do
  not match the init script; use the `local.d` method above.
- **`Permission denied` / `File not found` for a file that exists.** With `-s`
  (chroot) the path is *relative to `/tftpboot`* — request `fgt.out`, not
  `/tftpboot/fgt.out` — and the file must be readable by `nobody`.
- **Upload rejected.** Expected: without `-c` the server is read-only. Add `-c`
  only if you truly need uploads, and understand the exposure.

## Security and Best Practices

- **Serve read-only** (no `-c`), **chrooted** (`-s`), **as `nobody`** (`-u`). This
  is the whole hardening story for the daemon itself.
- **Treat the network as the access control.** Bind to the management address
  (`-a 10.30.99.50:69`) and firewall UDP/69 to the exact devices that pull firmware;
  never expose TFTP to a routed or untrusted network.
- **Keep only trusted payloads in `/tftpboot`** and verify each by checksum — a
  device will flash whatever you serve it.
- **Run it only when needed.** Bring the service up for the maintenance window;
  `rc-service local stop` (or a dedicated stop) removes the exposure afterward.
- Because TFTP is cleartext, never use it to move secrets — configurations with
  credentials should travel over SCP/HTTPS, not TFTP.

## References and Knowledge Checks

- Alpine wiki — [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository)
  (for `tftp-hpa`) and [Local startup scripts](https://wiki.alpinelinux.org/wiki/Local_Backup).
- `tftp-hpa` / `in.tftpd` manual pages (`man in.tftpd`).
- [RFC 1350](https://www.rfc-editor.org/rfc/rfc1350) — the TFTP protocol.

**Knowledge checks:**

1. Why does TFTP's lack of authentication make network position the primary
   control?
2. What do `-s`, `-u nobody`, and the absence of `-c` each contribute to a hardened
   server?
3. Why does this chapter run `in.tftpd` from `local.d` instead of the packaged
   OpenRC service?

## Hands-On Lab

**Objective:** Build a working, persistent, hardened TFTP server on Alpine and prove
it serves a real firmware image to a client.

**Shared prerequisites** — an Alpine host (Chapter 02) with community enabled
(Chapter 03) and a static address (Chapter 04), plus a second host on the same
subnet to act as the client. **Cost:** none.

### Lab 5.1 — Install and run `in.tftpd`

**Objective:** Stand up a read-only, chrooted, unprivileged TFTP server.

```sh
apk add tftp-hpa
mkdir -p /tftpboot && chown nobody:nobody /tftpboot
echo "hello-tftp $(date -u)" > /tftpboot/test.txt
chown nobody:nobody /tftpboot/test.txt
/usr/sbin/in.tftpd -l -s -u nobody /tftpboot
ss -lnu | grep ':69 '
ps aux | grep -i '[i]n.tftpd'
```

**Expected result:** `in.tftpd` running as `nobody`, listening on UDP/69, chrooted
to `/tftpboot`.

**Negative test:** start `in.tftpd` as root without `-s`/`-u`; it serves the whole
filesystem as root — exactly what you do not want from an unauthenticated daemon.
Kill it and rerun with `-s -u nobody`.

**Cleanup:** stop the daemon (`pkill in.tftpd`) if you are not continuing.

### Lab 5.2 — Persist the daemon and verify a client fetch

**Objective:** Survive a reboot and prove a client can download.

1. Add the `local.d` hook (Implementation) and enable `local`.
2. From the **client** host:

```sh
apk add tftp-hpa
tftp 10.30.99.50 -c get test.txt
cat test.txt                            # the served content
```

3. Reboot the server and repeat the fetch to prove persistence.

**Expected result:** the client downloads `test.txt` before and after a server
reboot — the `local.d` hook relaunches the daemon automatically.

**Negative test:** request the file by absolute path (`get /tftpboot/test.txt`); it
fails, because `-s` chroots the server and paths are relative to `/tftpboot` —
request `test.txt`.

**Cleanup:** remove `test.txt`; keep the server for Lab 5.3.

### Lab 5.3 — Serve firmware to a network device

**Objective:** Use the server for its real job — staging a firmware image a device
pulls over TFTP.

```sh
# On the server: stage and checksum the image.
cp FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out /tftpboot/
md5sum /tftpboot/FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out
```

```text
# On the network device (a FortiGate, Volume XIX Lab 4.8):
FGT-LAB-01 # execute ping 10.30.99.50
FGT-LAB-01 # execute restore image tftp FGT_VM64_KVM-v8.0.0.F-build0167-FORTINET.out 10.30.99.50
Connect to tftp server 10.30.99.50 ...
Get image from tftp server OK.
```

**Expected result:** the device reaches the server, pulls the image, and reports a
successful transfer — the Alpine box is doing exactly what a purpose-built appliance
should.

**Negative test:** put the image on the server but block UDP/69 at a host or network
firewall; the device times out with no transfer — TFTP has no way to authenticate or
retry around a filtered path, so reachability on UDP/69 is mandatory.

**Cleanup:** remove the firmware from `/tftpboot` and stop the daemon after the
maintenance window (`pkill in.tftpd`), or leave it up tightly firewalled.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A TFTP server on Alpine is `in.tftpd` from `tftp-hpa`, run read-only, chrooted, and
as `nobody` from a dedicated `/tftpboot` directory. Because the packaged OpenRC
service's `conf.d` options are unreliable, the durable way to launch it is a
`local.d` boot hook. TFTP has no authentication, so the network is the access
control — bind to the management subnet, firewall UDP/69 to the devices that need
it, keep only checksum-verified payloads, and run the service only when staging. The
payoff is the appliance this volume set out to build: a firewall (or switch, or PXE
client) pulls a firmware image straight off the Alpine box.

- [ ] Can install `tftp-hpa` and run a read-only, chrooted, unprivileged
      `in.tftpd`.
- [ ] Can persist the daemon with a `local.d` hook across reboots.
- [ ] Can verify the server with a TFTP client and a checksum.
- [ ] Can serve firmware to a real network device and explain the firewall
      requirement.
- [ ] Completed Labs 5.1–5.3 including each negative test.
