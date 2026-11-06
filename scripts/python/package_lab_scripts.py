#!/usr/bin/env python3
"""Publish a volume's lab-scripts folder as individual files and one zip file.

Usage: package_lab_scripts.py SCRIPTS_DIR OUT_DIR ZIP_NAME

Copies SCRIPTS_DIR to OUT_DIR/lab-scripts (leaving out work folders and Python
caches), writes SHA256SUMS next to the copies, and writes OUT_DIR/ZIP_NAME with
the same files under a top-level folder named lab-scripts. Shell and Python
scripts keep an executable mode inside the zip.
"""

import hashlib
import os
import shutil
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


def main(argv):
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    src, out, zip_name = argv[1], argv[2], argv[3]
    dest = os.path.join(out, "lab-scripts")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    sums = []
    for path in files_under(src):
        rel = os.path.relpath(path, src).replace(os.sep, "/")
        target = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(path, target)
        with open(path, "rb") as fh:
            sums.append("%s  %s" % (hashlib.sha256(fh.read()).hexdigest(), rel))
    with open(os.path.join(dest, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sums) + "\n")
    zip_path = os.path.join(out, zip_name)
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
