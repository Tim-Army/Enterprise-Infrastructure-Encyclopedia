#!/usr/bin/env python3
"""Render cloud-init NoCloud seeds for the Volume CCI lab virtual machines.

Reads lab201-vms.json and writes, for each virtual machine, the three files a
NoCloud seed needs (user-data, meta-data, network-config) and, with --iso, a
seed ISO named <vm>-seed.iso with the volume label "cidata".

The addresses come only from the IPv4 values in the manifest. The IPv6 address
of every IPv4 address is fd00:db8:201::<third octet><fourth octet> in
hexadecimal, with a prefix length of 120 for a /24, 127 for a /31, and 128 for
a /32, exactly as in Chapter 999.

Only the Python standard library is needed, except for --iso, which uses the
pycdlib package (pip install pycdlib) or, if it is missing, xorriso,
genisoimage, or mkisofs from the PATH.
"""

import argparse
import ipaddress
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V4_PREFIX = "10.201"
V6_PREFIX = "fd00:db8:201::"
V6_LEN = {24: 120, 31: 127, 32: 128}

NFT_RULES = """#!/usr/sbin/nft -f
flush ruleset
table inet lab201 {
  set svc4 { type ipv4_addr; flags interval; elements = { 10.201.10.0/24 } }
  set mgmt4 { type ipv4_addr; flags interval; elements = { 10.201.0.0/24, 10.201.30.0/24 } }
  set svc6 { type ipv6_addr; flags interval; elements = { fd00:db8:201::a00/120 } }
  set mgmt6 { type ipv6_addr; flags interval; elements = { fd00:db8:201::/120, fd00:db8:201::1e00/120 } }
  chain forward {
    type filter hook forward priority 0; policy drop;
    ct state established,related accept
    ip saddr 10.201.20.0/24 accept
    ip6 saddr fd00:db8:201::1400/120 accept
    ip saddr @mgmt4 ip daddr @svc4 tcp dport { 22, 514, 6514 } accept
    ip saddr @mgmt4 ip daddr @svc4 udp dport { 69, 123, 161, 162, 514, 1812, 1813, 2055, 4739, 6343 } accept
    ip6 saddr @mgmt6 ip6 daddr @svc6 tcp dport { 22, 514, 6514 } accept
    ip6 saddr @mgmt6 ip6 daddr @svc6 udp dport { 69, 123, 161, 162, 514, 1812, 1813, 2055, 4739, 6343 } accept
    ip saddr @svc4 ip daddr @mgmt4 accept
    ip6 saddr @svc6 ip6 daddr @mgmt6 accept
    icmp type echo-request accept
    icmpv6 type { echo-request, nd-neighbor-solicit, nd-neighbor-advert } accept
  }
}
"""

SYSCTL_FORWARD = "net.ipv4.ip_forward=1\nnet.ipv6.conf.all.forwarding=1\n"


def configure(manifest):
    """Take the address blocks from the manifest (the defaults are the Chapter 999 plan)."""
    global V4_PREFIX, V6_PREFIX
    V4_PREFIX = manifest.get("ipv4_prefix", V4_PREFIX)
    V6_PREFIX = manifest.get("ipv6_prefix", V6_PREFIX)


def nft_rules():
    return NFT_RULES.replace("10.201.", V4_PREFIX + ".").replace("fd00:db8:201::", V6_PREFIX)


def q(value):
    """Quote a YAML scalar. JSON strings are valid YAML."""
    return json.dumps(value)


def v6_of(v4_cidr):
    """Return the Chapter 999 IPv6 address (with prefix length) for an IPv4 CIDR."""
    iface = ipaddress.ip_interface(v4_cidr)
    octets = iface.ip.packed
    prefix = V6_LEN.get(iface.network.prefixlen)
    if prefix is None:
        raise ValueError("no IPv6 prefix rule for " + v4_cidr)
    addr = ipaddress.IPv6Address("%s%02x%02x" % (V6_PREFIX, octets[2], octets[3]))
    return "%s/%d" % (addr, prefix)


def gateway_v6(gateway4):
    octets = ipaddress.ip_address(gateway4).packed
    return str(ipaddress.IPv6Address("%s%02x%02x" % (V6_PREFIX, octets[2], octets[3])))


def mac_of(manifest, vm_index, nic_index):
    return "%s:%02x:%02x" % (manifest["mac_prefix"], vm_index + 1, nic_index)


def addresses_of(v4_list):
    out = []
    for v4 in v4_list:
        out.append(v4)
        out.append(v6_of(v4))
    return out


def yaml_list(items, indent):
    pad = " " * indent
    return "".join("%s- %s\n" % (pad, q(i)) for i in items)


def network_config(manifest, vm_index, vm, tagging):
    lines = ["network:", "  version: 2", "  renderer: networkd"]
    eth, vlans, bridges, dummies = [], [], [], []
    for n, nic in enumerate(vm["nics"]):
        name = "nic%d" % n
        mac = mac_of(manifest, vm_index, n)
        body = ["    %s:" % name,
                "      match:", "        macaddress: %s" % q(mac),
                "      set-name: %s" % name]
        if nic.get("build"):
            body += ["      dhcp4: true", "      dhcp6: false", "      accept-ra: false",
                     "      dhcp4-overrides:", "        route-metric: 200"]
        elif nic.get("trunk"):
            body += ["      dhcp4: false", "      dhcp6: false", "      accept-ra: false", "      link-local: []"]
        else:
            body += ["      dhcp6: false", "      accept-ra: false"]
            vlan = nic.get("vlan")
            tagged_in_guest = tagging == "guest" and vlan
            if tagged_in_guest:
                body += ["      dhcp4: false", "      link-local: []"]
                vname = "%sv%d" % (name, vlan)
                vbody = ["    %s:" % vname, "      id: %d" % vlan, "      link: %s" % name,
                         "      dhcp6: false", "      accept-ra: false"]
                vbody += address_block(nic)
                vlans.append(vbody)
            else:
                body += address_block(nic)
        eth.append(body)
    trunk = vm.get("bridge_trunks")
    if trunk:
        ports = []
        for n, nic in enumerate(vm["nics"]):
            if nic.get("trunk") and nic["net"] in trunk["ports"]:
                ports.append("nic%d" % n)
        bridges.append(["    %s:" % trunk["name"], "      interfaces: [%s]" % ", ".join(ports),
                        "      parameters:", "        stp: false", "      dhcp4: false", "      dhcp6: false",
                        "      accept-ra: false", "      link-local: []"])
        for vid in trunk["vlans"]:
            v4 = "%s.%d.1/24" % (V4_PREFIX, vid)
            vlans.append(["    vlan%d:" % vid, "      id: %d" % vid, "      link: %s" % trunk["name"],
                          "      dhcp6: false", "      accept-ra: false", "      addresses:"]
                         + [x.rstrip("\n") for x in yaml_list(addresses_of([v4]), 8).splitlines()])
    for d in vm.get("dummies", []):
        dummies.append(["    %s:" % d["name"], "      addresses:"]
                       + yaml_list(addresses_of(d["ipv4"]), 8).splitlines())
    lines.append("  ethernets:")
    for b in eth:
        lines += b
    if bridges:
        lines.append("  bridges:")
        for b in bridges:
            lines += b
    if vlans:
        lines.append("  vlans:")
        for b in vlans:
            lines += b
    if dummies:
        lines.append("  dummy-devices:")
        for b in dummies:
            lines += b
    return "\n".join(lines) + "\n"


def address_block(nic):
    out = []
    if nic.get("ipv4"):
        out += ["      dhcp4: false", "      addresses:"]
        out += yaml_list(addresses_of(nic["ipv4"]), 8).splitlines()
    gw = nic.get("gateway4")
    if gw:
        out += ["      routes:",
                "        - to: default", "          via: %s" % q(gw), "          metric: 100",
                "        - to: default", "          via: %s" % q(gateway_v6(gw)), "          metric: 100"]
    return out


def user_data(manifest, vm, ssh_keys, guest_agent, password_hash):
    user = manifest["admin_user"]
    pkgs = list(vm.get("packages", []))
    agent = {"qemu": "qemu-guest-agent", "vmware": "open-vm-tools"}.get(guest_agent)
    if agent and agent not in pkgs:
        pkgs.append(agent)
    L = ["#cloud-config",
         "hostname: %s" % vm["name"],
         "manage_etc_hosts: true",
         "timezone: UTC",
         "ssh_pwauth: %s" % ("true" if password_hash else "false"),
         "users:",
         "  - name: %s" % user,
         "    groups: [sudo]",
         "    shell: /bin/bash",
         "    sudo: \"ALL=(ALL) NOPASSWD:ALL\"",
         "    lock_passwd: %s" % ("false" if password_hash else "true")]
    if password_hash:
        L.append("    passwd: %s" % q(password_hash))
    if ssh_keys:
        L.append("    ssh_authorized_keys:")
        L += yaml_list(ssh_keys, 6).splitlines()
    L += ["package_update: true", "package_upgrade: false"]
    if pkgs:
        L.append("packages:")
        L += yaml_list(pkgs, 2).splitlines()
    files = []
    if vm.get("forwarding"):
        files.append(("/etc/sysctl.d/60-lab201.conf", SYSCTL_FORWARD))
    if vm.get("role") == "gateway":
        files.append(("/etc/nftables.conf", nft_rules()))
    files.append(("/etc/lab201-vm", "name=%s\nrole=%s\n" % (vm["name"], vm["role"])))
    L.append("write_files:")
    for path, content in files:
        L += ["  - path: %s" % path, "    permissions: \"0644\"", "    content: %s" % q(content)]
    run = []
    if vm.get("forwarding"):
        run.append("sysctl --system")
    if vm.get("role") == "gateway":
        run.append("systemctl enable --now nftables")
    if guest_agent == "qemu":
        run.append("systemctl enable --now qemu-guest-agent")
    if guest_agent == "vmware":
        run.append("systemctl enable --now open-vm-tools")
    if run:
        L.append("runcmd:")
        L += ["  - %s" % q(c) for c in run]
    return "\n".join(L) + "\n"


def meta_data(vm):
    return "instance-id: lab201-%s\nlocal-hostname: %s\n" % (vm["name"], vm["name"])


def build_iso_external(out_iso, files):
    """Write the seed ISO with xorriso, genisoimage, or mkisofs."""
    for tool in ("xorriso", "genisoimage", "mkisofs"):
        exe = shutil.which(tool)
        if exe:
            cmd = [exe] + (["-as", "mkisofs"] if tool == "xorriso" else []) + [
                "-quiet", "-output", out_iso, "-volid", "cidata", "-joliet", "-rock"] + list(files.values())
            subprocess.run(cmd, check=True)
            return
    raise SystemExit("make-seed: --iso needs pycdlib (pip install pycdlib), xorriso, genisoimage, or mkisofs")


def write_iso(out_iso, files):
    """Write the seed ISO with pycdlib, or with an external tool."""
    try:
        import pycdlib
    except ImportError:
        pycdlib = None
    if not pycdlib:
        return build_iso_external(out_iso, files)
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, rock_ridge="1.09", vol_ident="cidata")
    names = {"user-data": "USERDATA", "meta-data": "METADATA", "network-config": "NETCONF"}
    handles = []
    try:
        for fname, path in files.items():
            fh = open(path, "rb")
            handles.append(fh)
            iso.add_fp(fh, os.path.getsize(path), "/%s.;1" % names[fname], rr_name=fname, joliet_path="/" + fname)
        iso.write(out_iso)
    finally:
        iso.close()
        for fh in handles:
            fh.close()


def wsl_net_script(vm):
    """Idempotent script that puts a host's lab addresses on VLAN interfaces of one dummy device.

    All WSL 2 distributions share one network namespace, so every host's
    addresses live in the same namespace. If the kernel lacks 802.1Q support the
    addresses go on the dummy device itself.
    """
    L = ["#!/bin/sh",
         "# Written by make-seed.py. Safe to run more than once.",
         "ip link show lab201 >/dev/null 2>&1 || ip link add lab201 type dummy || exit 0",
         "ip link set lab201 up",
         "vl() {",
         "  if ip link show lab201.$1 >/dev/null 2>&1 || ip link add link lab201 name lab201.$1 type vlan id $1 2>/dev/null; then",
         "    ip link set lab201.$1 up; echo lab201.$1",
         "  else echo lab201; fi",
         "}"]
    for nic in vm["nics"]:
        if nic.get("build") or nic.get("trunk") or not nic.get("ipv4"):
            continue
        vlan = nic.get("vlan")
        L.append("dev=$(vl %d)" % vlan if vlan else "dev=lab201")
        for a in addresses_of(nic["ipv4"]):
            L.append("ip addr replace %s dev $dev" % a)
    return "\n".join(L) + "\n"


def wsl_provision(manifest, vm, ssh_keys):
    user = manifest["admin_user"]
    name = vm["name"]
    pkgs = " ".join(["iproute2", "iputils-ping", "sudo", "openssh-server"] + [p for p in vm.get("packages", []) if p != "openssh-server"])
    L = ["#!/bin/bash",
         "# Written by make-seed.py. Run as root inside the new distribution.",
         "set -euo pipefail",
         "export DEBIAN_FRONTEND=noninteractive",
         "cat > /etc/wsl.conf <<'LAB201_WSLCONF'",
         "[boot]", "systemd=true", "command=/usr/local/sbin/lab201-net.sh",
         "[network]", "hostname=%s" % name, "generateHosts=true",
         "[user]", "default=%s" % user,
         "LAB201_WSLCONF",
         "id %s >/dev/null 2>&1 || useradd -m -s /bin/bash -G sudo %s" % (user, user),
         "echo '%s ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-lab201" % user,
         "chmod 440 /etc/sudoers.d/90-lab201",
         "install -d -m 700 -o %s -g %s /home/%s/.ssh" % (user, user, user)]
    if ssh_keys:
        L += ["cat > /home/%s/.ssh/authorized_keys <<'LAB201_KEYS'" % user] + ssh_keys + ["LAB201_KEYS",
              "chown %s:%s /home/%s/.ssh/authorized_keys" % (user, user, user), "chmod 600 /home/%s/.ssh/authorized_keys" % user]
    L += ["cat > /usr/local/sbin/lab201-net.sh <<'LAB201_NET'", wsl_net_script(vm).rstrip("\n"), "LAB201_NET",
          "chmod 755 /usr/local/sbin/lab201-net.sh",
          "apt-get update",
          "apt-get install -y %s" % pkgs,
          "echo '%s provisioned'" % name]
    return "\n".join(L) + "\n"


def read_keys(paths):
    keys = []
    for p in paths:
        with open(os.path.expanduser(p), "r", encoding="utf-8") as fh:
            keys += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    return keys


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", default=os.path.join(HERE, "lab201-vms.json"))
    ap.add_argument("--out", default="seeds", help="output directory (default: seeds)")
    ap.add_argument("--vm", action="append", help="render only this VM (repeatable)")
    ap.add_argument("--ssh-key", action="append", default=[], help="public key file (repeatable)")
    ap.add_argument("--tagging", choices=["hypervisor", "guest"], default="hypervisor",
                    help="hypervisor: the virtual switch applies VLAN tags; guest: the guest creates VLAN interfaces")
    ap.add_argument("--guest-agent", choices=["qemu", "vmware", "none"], default="none")
    ap.add_argument("--password-hash-env", default="LAB201_ADMIN_PASSWORD_HASH",
                    help="environment variable that holds a crypt hash for the admin user (optional)")
    ap.add_argument("--iso", action="store_true", help="also write <vm>-seed.iso")
    ap.add_argument("--wsl", action="store_true",
                    help="write wsl-provision.sh for the VMs marked wsl in the manifest, instead of cloud-init files")
    ap.add_argument("--list", action="store_true", help="print the VM names and exit")
    a = ap.parse_args()

    with open(a.manifest, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    configure(manifest)
    if a.list:
        print("\n".join(v["name"] for v in manifest["vms"]))
        return 0
    keys = read_keys(a.ssh_key)
    pw = os.environ.get(a.password_hash_env) or None
    if a.wsl:
        for vm in manifest["vms"]:
            if not vm.get("wsl") or (a.vm and vm["name"] not in a.vm):
                continue
            d = os.path.join(a.out, vm["name"])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "wsl-provision.sh"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(wsl_provision(manifest, vm, keys))
            print("rendered %s (WSL)" % vm["name"])
        return 0
    if not keys and not pw:
        raise SystemExit("make-seed: give at least one --ssh-key file, or set %s" % a.password_hash_env)
    agent = None if a.guest_agent == "none" else a.guest_agent
    wanted = set(a.vm or [])
    for i, vm in enumerate(manifest["vms"]):
        if wanted and vm["name"] not in wanted:
            continue
        d = os.path.join(a.out, vm["name"])
        os.makedirs(d, exist_ok=True)
        files = {}
        for fname, text in (("user-data", user_data(manifest, vm, keys, agent, pw)),
                            ("meta-data", meta_data(vm)),
                            ("network-config", network_config(manifest, i, vm, a.tagging))):
            path = os.path.join(d, fname)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            files[fname] = path
        if a.iso:
            write_iso(os.path.join(a.out, "%s-seed.iso" % vm["name"]), files)
        print("rendered %s" % vm["name"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
