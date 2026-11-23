#!/usr/bin/env python3
"""Find, download, and verify the cloud image for a lab Linux flavor.

Usage:
  resolve-image.py --flavor ID --out DIR [--ova] [--image-path FILE] [--dry-run]

Reads flavors.json (beside this script). For a flavor with a published image, it
reads the image directory, picks the newest file that matches the flavor's
pattern, downloads it into DIR (a file already there is reused), and checks it
against the checksum file the publisher provides. It prints the path of the
verified file as its last line of output.

A hardened (STIG) flavor uses the image of its base flavor. A flavor with no
published image (Red Hat Enterprise Linux) needs --image-path, the file you
downloaded from the vendor. With --ova, the Ubuntu .ova file is used when the
flavor has one (VMware platforms import OVA files).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
AGENT = "lab201-resolve-image/1.0"


def http_get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return data if binary else data.decode("utf-8", "replace")


def natural_key(name):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def index_names(base):
    html = http_get(base)
    names = re.findall(r'href="([^"?#/][^"?#]*)"', html)
    return [urllib.parse.unquote(n) for n in names]


def pick(pattern, names):
    rx = re.compile("^(?:%s)$" % pattern)
    hits = sorted((n for n in names if rx.match(n)), key=natural_key)
    return hits[-1] if hits else None


def parse_sums(text, name, algo):
    """Return the hex digest listed for name. Handles 'hash  name', 'hash *name', and 'ALGO (name) = hash'."""
    want = len(hashlib.new(algo).hexdigest())
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^[A-Za-z0-9-]+ \((.+)\) = ([0-9a-fA-F]+)$", line)
        if m and m.group(1) == name and len(m.group(2)) == want:
            return m.group(2).lower()
        m = re.match(r"^([0-9a-fA-F]+) [ *](.+)$", line)
        if m and m.group(2) == name and len(m.group(1)) == want:
            return m.group(1).lower()
    return None


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def find_flavor(data, fid):
    for f in data["flavors"]:
        if f["id"] == fid:
            return f
    raise SystemExit("resolve-image: unknown flavor %s" % fid)


def image_flavor(data, fid):
    f = find_flavor(data, fid)
    while "image" not in f and f.get("base"):
        f = find_flavor(data, f["base"])
    return f


def plan(data, fid, want_ova=False):
    """Work out the file name, URL, and checksum for a flavor. Needs the network."""
    f = image_flavor(data, fid)
    img = f.get("image")
    if not img:
        raise SystemExit("resolve-image: flavor %s has no image information" % fid)
    if "user_supplied" in img:
        return {"flavor": f["id"], "user_supplied": img["user_supplied"]}
    if want_ova and not img.get("ova"):
        raise SystemExit("resolve-image: no OVA is published for %s. Make one from its qcow2 image and pass it to the script." % f["id"])
    base = img["base"]
    names = index_names(base)
    pattern = re.escape(img["ova"]) if want_ova else img["pattern"]
    name = pick(pattern, names)
    if not name:
        raise SystemExit("resolve-image: no file matching %s at %s" % (pattern, base))
    sums_name = img.get("sums") or pick(img["sums_pattern"], names)
    sums_text = http_get(base + sums_name)
    digest = parse_sums(sums_text, name, img["algo"])
    return {"flavor": f["id"], "name": name, "url": base + name, "algo": img["algo"], "sum": digest, "sums_url": base + sums_name}


def sha_of(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=120) as resp, open(tmp, "wb") as out:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
    os.replace(tmp, dest)


def selftest():
    bsd = "SHA256 (a.qcow2) = " + "ab" * 32 + "\n# a.qcow2: 5 bytes\n"
    gnu = "cd" * 32 + "  b.img\n" + "ef" * 32 + " *c.img\n"
    assert parse_sums(bsd, "a.qcow2", "sha256") == "ab" * 32
    assert parse_sums(gnu, "b.img", "sha256") == "cd" * 32
    assert parse_sums(gnu, "c.img", "sha256") == "ef" * 32
    assert parse_sums(gnu, "missing", "sha256") is None
    assert parse_sums("12 b.img", "b.img", "sha256") is None
    names = ["Fedora-Cloud-Base-Generic-43-1.6.x86_64.qcow2", "Fedora-Cloud-Base-Generic-43-1.10.x86_64.qcow2", "Fedora-Cloud-Base-UEFI-UKI-43-1.6.x86_64.qcow2"]
    assert pick(r"Fedora-Cloud-Base-Generic-43-[0-9.]+\.x86_64\.qcow2", names).endswith("43-1.10.x86_64.qcow2")
    print("resolve-image selftest passed")


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--flavor")
    ap.add_argument("--out", default="images")
    ap.add_argument("--flavors", default=os.path.join(HERE, "flavors.json"))
    ap.add_argument("--ova", action="store_true", help="use the .ova file where the flavor has one")
    ap.add_argument("--image-path", help="a file you downloaded yourself (needed for Red Hat Enterprise Linux)")
    ap.add_argument("--dry-run", action="store_true", help="print the URL and checksum, download nothing")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if not a.flavor:
        ap.error("--flavor is required")
    data = load(a.flavors)
    f = image_flavor(data, a.flavor)
    if f.get("image", {}).get("user_supplied") or a.image_path:
        if not a.image_path or not os.path.isfile(a.image_path):
            raise SystemExit("resolve-image: %s needs --image-path. %s" % (a.flavor, f["image"].get("user_supplied", "")))
        print(os.path.abspath(a.image_path))
        return 0
    info = plan(data, a.flavor, a.ova)
    if a.dry_run:
        print(json.dumps(info, indent=2))
        return 0
    os.makedirs(a.out, exist_ok=True)
    dest = os.path.join(a.out, info["name"])
    if not os.path.isfile(dest) or (info["sum"] and sha_of(dest, info["algo"]) != info["sum"]):
        print("downloading %s" % info["url"], file=sys.stderr)
        download(info["url"], dest)
    got = sha_of(dest, info["algo"])
    if not info["sum"] or got != info["sum"]:
        os.remove(dest)
        raise SystemExit("resolve-image: checksum mismatch for %s (expected %s, got %s)" % (info["name"], info["sum"], got))
    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
