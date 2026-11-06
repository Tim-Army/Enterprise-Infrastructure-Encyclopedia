#!/usr/bin/env python3
"""Publish a volume's lab-scripts folder as individual files and one zip file.

Usage: package_lab_scripts.py SCRIPTS_DIR OUT_DIR ZIP_NAME [--add SOURCE=DEST ...]

Copies SCRIPTS_DIR to OUT_DIR/lab-scripts (leaving out work folders and Python
caches), writes SHA256SUMS next to the copies, and writes OUT_DIR/ZIP_NAME with
the same files under a top-level folder named lab-scripts. Shell and Python
scripts keep an executable mode inside the zip.

Each --add SOURCE=DEST copies one more file from the repository into the
published folder, at DEST relative to lab-scripts (for example the lab network
diagram, so it travels with the scripts). When SOURCE is an SVG file and
rsvg-convert is on the PATH, a PNG copy is written beside it.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

SKIP_DIRS = {"work", "__pycache__", "seeds"}
EXECUTABLE = (".sh", ".py")


def files_under(root):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if name.endswith(".pyc"):
                continue
            yield os.path.join(base, name)


def add_extra(spec, dest_root):
    """Copy SOURCE to DEST under dest_root. Returns the relative paths written."""
    if "=" not in spec:
        raise SystemExit("package_lab_scripts.py: --add needs SOURCE=DEST, got %r" % spec)
    source, rel = spec.split("=", 1)
    if not os.path.isfile(source):
        print("package_lab_scripts.py: skipped %s (not found)" % source, file=sys.stderr)
        return []
    target = os.path.join(dest_root, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(source, target)
    written = [rel.replace(os.sep, "/")]
    rsvg = shutil.which("rsvg-convert")
    if source.lower().endswith(".svg") and rsvg:
        png_rel = rel[:-4] + ".png"
        png = os.path.join(dest_root, png_rel)
        result = subprocess.run([rsvg, "-w", "1800", "-o", png, source], capture_output=True)
        if result.returncode == 0:
            written.append(png_rel.replace(os.sep, "/"))
        else:
            print("package_lab_scripts.py: PNG conversion failed for %s" % source, file=sys.stderr)
    return written


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scripts_dir")
    ap.add_argument("out_dir")
    ap.add_argument("zip_name")
    ap.add_argument("--add", action="append", default=[], metavar="SOURCE=DEST")
    a = ap.parse_args(argv[1:])

    dest = os.path.join(a.out_dir, "lab-scripts")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    for path in files_under(a.scripts_dir):
        rel = os.path.relpath(path, a.scripts_dir)
        target = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(path, target)
    for spec in a.add:
        add_extra(spec, dest)

    sums = []
    for path in files_under(dest):
        rel = os.path.relpath(path, dest).replace(os.sep, "/")
        with open(path, "rb") as fh:
            sums.append("%s  %s" % (hashlib.sha256(fh.read()).hexdigest(), rel))
    with open(os.path.join(dest, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sums) + "\n")

    zip_path = os.path.join(a.out_dir, a.zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files_under(dest):
            rel = os.path.relpath(path, dest).replace(os.sep, "/")
            info = zipfile.ZipInfo("lab-scripts/" + rel, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if rel.endswith(EXECUTABLE) else 0o644) << 16
            with open(path, "rb") as fh:
                zf.writestr(info, fh.read())
    print("package_lab_scripts.py: %d files -> %s" % (len(sums), zip_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
