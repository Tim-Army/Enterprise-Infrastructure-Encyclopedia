#!/usr/bin/env python3
"""Render cloud-init NoCloud seeds for the Volume CCI lab virtual machines.

Reads lab201-vms.json and writes, for each virtual machine, the three files a
NoCloud seed needs (user-data, meta-data, network-config) and, with --iso, a
seed ISO named <vm>-seed.iso with the volume label "cidata".

The addresses come only from the IPv4 values in the manifest. The IPv6 address
of every IPv4 address is fd00:db8:201::<third octet><fourth octet> in
hexadecimal, with a prefix length of 120 for a /24, 127 for a /31, and 128 for
a /32, exactly as in Chapter 999.

Each machine can use its own Linux flavor (flavor in the manifest, or
default_flavor). flavors.json lists the flavors, the package names for each
family (apt or dnf), and which machine types each flavor can run. With
--license-file, a JSON file with keys the scripts apply (a Red Hat activation key
and organization, an Ubuntu Pro token) is read and written into the seeds of the
machines that need them. The file is never printed.

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
FLAVOR_DATA = {"default": "ubuntu-24.04", "role_keys": [], "families": {}, "flavors": {}}

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


def load_flavors(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    FLAVOR_DATA["default"] = data.get("default", FLAVOR_DATA["default"])
    FLAVOR_DATA["role_keys"] = data["role_keys"]
    FLAVOR_DATA["families"] = data["families"]
    FLAVOR_DATA["flavors"] = dict((f["id"], f) for f in data["flavors"])


def flavor_of(manifest, vm):
    fid = vm.get("flavor") or manifest.get("default_flavor") or FLAVOR_DATA["default"]
    if fid not in FLAVOR_DATA["flavors"]:
        raise SystemExit("make-seed: %s uses an unknown flavor %s" % (vm["name"], fid))
    return FLAVOR_DATA["flavors"][fid]


def role_key(role):
    return "routing peer" if role.startswith("routing peer") else role


def rating(flavor, role):
    keys = FLAVOR_DATA["role_keys"]
    key = role_key(role)
    if key not in keys:
        return "y"
    return flavor["roles"][keys.index(key)]


def map_packages(pkgs, flavor):
    """Translate the manifest's package names (Ubuntu names) for a flavor.

    Returns the packages to install, whether a package needs EPEL, and the
    packages the flavor does not have.
    """
    fam = FLAVOR_DATA["families"].get(flavor["family"], {"map": {}})
    mapping = fam.get("map", {})
    epel = set(fam.get("epel_packages", []))
    install, missing, needs_epel = [], [], False
    for p in pkgs:
        target = mapping.get(p, p)
        if target is None:
            missing.append(p)
            continue
        if target not in install:
            install.append(target)
        if (p in epel or target in epel) and flavor.get("epel"):
            needs_epel = True
    return install, needs_epel, missing


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


def network_config(manifest, vm_index, vm, tagging, flavor=None):
    lines = ["network:", "  version: 2"]
    if flavor is None or flavor.get("renderer") == "networkd":
        lines.append("  renderer: networkd")
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
            seg = int(manifest.get("vlan_segments", {}).get(str(vid), vid))
            v4 = "%s.%d.1/24" % (V4_PREFIX, seg)
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


def user_data(manifest, vm, ssh_keys, guest_agent, password_hash, flavor=None, licenses=None):
    flavor = flavor or FLAVOR_DATA["flavors"].get(FLAVOR_DATA["default"]) or {"family": "apt"}
    fam = FLAVOR_DATA["families"].get(flavor["family"], {"admin_group": "sudo", "map": {}, "install": "apt"})
    licenses = licenses or {}
    stig = flavor.get("stig")
    user = manifest["admin_user"]
    pkgs = list(vm.get("packages", []))
    agent = {"qemu": "qemu-guest-agent", "vmware": "open-vm-tools"}.get(guest_agent)
    if agent and agent not in pkgs:
        pkgs.append(agent)
    install, needs_epel, missing = map_packages(pkgs, flavor)
    if stig == "rhel-oscap":
        install += ["scap-security-guide", "openscap-scanner"]
    sudo_rule = "ALL=(ALL) ALL" if flavor.get("needs_password") else "ALL=(ALL) NOPASSWD:ALL"
    L = ["#cloud-config",
         "hostname: %s" % vm["name"],
         "manage_etc_hosts: true",
         "timezone: UTC",
         "ssh_pwauth: %s" % ("true" if password_hash else "false"),
         "users:",
         "  - name: %s" % user,
         "    groups: [%s]" % fam.get("admin_group", "sudo"),
         "    shell: /bin/bash",
         "    sudo: %s" % q(sudo_rule),
         "    lock_passwd: %s" % ("false" if password_hash else "true")]
    if password_hash:
        L.append("    passwd: %s" % q(password_hash))
    if ssh_keys:
        L.append("    ssh_authorized_keys:")
        L += yaml_list(ssh_keys, 6).splitlines()
    rh = licenses.get("redhat") or {}
    if flavor.get("subscription") and rh.get("activation_key") and rh.get("org"):
        L += ["rh_subscription:", "  activation-key: %s" % q(rh["activation_key"]), "  org: %s" % q(str(rh["org"])), "  auto-attach: true"]
    pro = licenses.get("ubuntu_pro") or {}
    if flavor.get("ubuntu_pro") and pro.get("token"):
        L += ["ubuntu_pro:", "  token: %s" % q(pro["token"])]
    L += ["package_update: true", "package_upgrade: false"]
    if fam.get("install") == "apt" and install:
        L.append("packages:")
        L += yaml_list(install, 2).splitlines()
    files = []
    if vm.get("forwarding"):
        files.append(("/etc/sysctl.d/60-lab201.conf", SYSCTL_FORWARD))
    if vm.get("role") == "gateway":
        files.append(("/etc/nftables.conf", nft_rules()))
    info = "name=%s\nrole=%s\nflavor=%s\n" % (vm["name"], vm["role"], flavor["id"])
    if missing:
        info += "unavailable_packages=%s\n" % " ".join(missing)
    files.append(("/etc/lab201-vm", info))
    if stig:
        files.append(("/root/LAB201-STIG-NOTES.txt", stig_notes(vm, flavor, missing)))
    L.append("write_files:")
    for path, content in files:
        L += ["  - path: %s" % path, "    permissions: \"0644\"", "    content: %s" % q(content)]
    run = []
    if fam.get("install") == "dnf" and install:
        if needs_epel:
            epel = flavor["epel"]
            run.append("dnf -y install %s" % epel)
            if not epel.startswith("http"):
                run.append("dnf -y config-manager --set-enabled crb || true")
            elif flavor.get("subscription"):
                run.append("subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms || true")
        run.append("dnf -y install %s" % " ".join(install))
    if vm.get("forwarding"):
        run.append("sysctl --system")
    if vm.get("role") == "gateway":
        run.append("systemctl enable --now nftables")
    if guest_agent == "qemu":
        run.append("systemctl enable --now qemu-guest-agent || systemctl start qemu-guest-agent || true")
    if guest_agent == "vmware":
        run.append("systemctl enable --now open-vm-tools || systemctl start open-vm-tools || true")
    if stig == "ubuntu-usg":
        run += ["pro enable usg || true", "apt-get install -y usg || true", "usg fix disa_stig || true"]
    if stig == "rhel-oscap":
        run.append("oscap xccdf eval --remediate --profile xccdf_org.ssgproject.content_profile_stig "
                   "--results /root/stig-results.xml --report /root/stig-report.html "
                   "/usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml || true")
    if run:
        L.append("runcmd:")
        L += ["  - %s" % q(c) for c in run]
    if stig:
        L += ["power_state:", "  mode: reboot", "  message: Rebooting once after hardening", "  timeout: 600", "  condition: true"]
    return "\n".join(L) + "\n"


def stig_notes(vm, flavor, missing):
    lines = ["Lab 201 STIG hardening notes for %s (%s)" % (vm["name"], flavor["name"]),
             "The STIG is applied on first boot, then the machine reboots once.",
             "Review the scan results (/root/stig-results.xml and /root/stig-report.html on Red Hat; the usg report on Ubuntu).",
             "Accepted findings, because the lab needs the behavior:"]
    if vm.get("forwarding"):
        lines.append("- IP forwarding is on: this machine routes between lab segments.")
    if vm.get("role") == "services":
        lines += ["- Services that STIG baselines discourage run here by design: RADIUS, syslog, NTP, SNMP, TFTP, NetFlow collection."]
    if vm.get("role") == "gateway":
        lines.append("- The gateway bridges two trunks and forwards traffic by the lab firewall policy.")
    if missing:
        lines.append("- Packages this flavor does not have, so the matching lab tools are absent: %s" % ", ".join(missing))
    lines.append("- sudo asks for a password. Set LAB201_ADMIN_PASSWORD_HASH before building.")
    return "\n".join(lines) + "\n"


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
    ap.add_argument("--flavors", default=os.path.join(HERE, "flavors.json"), help="flavor catalog (default: flavors.json beside this script)")
    ap.add_argument("--license-file", help="JSON file with keys to apply (never printed or copied elsewhere)")
    a = ap.parse_args()

    with open(a.manifest, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    configure(manifest)
    load_flavors(a.flavors)
    licenses = {}
    if a.license_file:
        with open(a.license_file, "r", encoding="utf-8") as fh:
            licenses = json.load(fh)
    if a.list:
        print("\n".join(v["name"] for v in manifest["vms"]))
        return 0
    keys = read_keys(a.ssh_key)
    pw = os.environ.get(a.password_hash_env) or None
    if a.wsl:
        for vm in manifest["vms"]:
            if not vm.get("wsl") or (a.vm and vm["name"] not in a.vm):
                continue
            if flavor_of(manifest, vm)["id"] != "ubuntu-24.04":
                raise SystemExit("make-seed: WSL hosts use Ubuntu 24.04 only (%s asks for %s)" % (vm["name"], flavor_of(manifest, vm)["id"]))
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
        flavor = flavor_of(manifest, vm)
        if flavor["status"] == "planned":
            raise SystemExit("make-seed: %s uses %s, which is planned and has no script support. %s" % (vm["name"], flavor["name"], flavor.get("why", "")))
        if rating(flavor, vm["role"]) == "n":
            raise SystemExit("make-seed: %s cannot run %s (%s). Pick another flavor for it." % (flavor["name"], vm["name"], vm["role"]))
        if flavor.get("needs_password") and not pw:
            raise SystemExit("make-seed: %s is hardened, so sudo needs a password. Set %s to a crypt hash (openssl passwd -6)." % (vm["name"], a.password_hash_env))
        if flavor.get("subscription") and not (licenses.get("redhat") or {}).get("activation_key"):
            print("make-seed: warning: %s needs a Red Hat subscription. Pass --license-file with a redhat activation_key and org, or register by hand." % vm["name"], file=sys.stderr)
        if flavor.get("ubuntu_pro") and not (licenses.get("ubuntu_pro") or {}).get("token"):
            print("make-seed: warning: %s needs an Ubuntu Pro token for the STIG tools. Pass --license-file with ubuntu_pro token." % vm["name"], file=sys.stderr)
        _, _, missing = map_packages(vm.get("packages", []), flavor)
        if missing:
            print("make-seed: note: %s does not have %s on %s, so those tools are left out of %s." % (flavor["name"], ", ".join(missing), vm["role"], vm["name"]), file=sys.stderr)
        d = os.path.join(a.out, vm["name"])
        os.makedirs(d, exist_ok=True)
        files = {}
        for fname, text in (("user-data", user_data(manifest, vm, keys, agent, pw, flavor, licenses)),
                            ("meta-data", meta_data(vm)),
                            ("network-config", network_config(manifest, i, vm, a.tagging, flavor))):
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
