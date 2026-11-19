#!/usr/bin/env python3
"""Check the lab automation scripts of every volume that has a lab-scripts folder.

Usage: check_lab_scripts.py

For each volumes/*/lab-scripts folder this checks, without touching a network or
a hypervisor:

- every Python file compiles;
- every Bash script passes "bash -n" (skipped with a note when bash is missing);
- every PowerShell script parses (skipped with a note when pwsh is missing);
- when the folder has common/make-seed.py, the seed generator writes a seed for
  every machine of the manifest with every cloud-image flavor, with the VLAN
  tags made by the hypervisor and by the guest, and every seed carries the
  lab201-status script, which passes "bash -n" (one seed of each run is checked).

It prints one line for each group and exits with status 1 if anything failed,
which validate.sh uses.
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {"work", "__pycache__", "seeds", "walkthroughs"}
# A throwaway public key and password hash. They only have to look right to make-seed.py.
TEST_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGirxqLHvYFZAkfgxfAH904k/2kkqekQ9oKHI3Wxpai7 lab-script-check\n"
TEST_HASH = "$6$labcheck$0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmn"
# The write_files entry of the status script in a seed's user-data.
STATUS_FILE = re.compile(r'- path: /usr/local/sbin/lab201-status\n    permissions: "0755"\n    content: (".*")\n')


def files_under(root, suffix):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if name.endswith(suffix):
                yield os.path.join(base, name)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def check_python(folder, problems):
    count = 0
    for path in files_under(folder, ".py"):
        count += 1
        try:
            with open(path, "r", encoding="utf-8") as fh:
                compile(fh.read(), path, "exec")
        except SyntaxError as err:
            problems.append("%s does not compile: line %s: %s" % (rel(path), err.lineno, err.msg))
    return "%d Python file(s) compile" % count


def check_bash(folder, problems):
    paths = list(files_under(folder, ".sh"))
    bash = shutil.which("bash")
    if not bash:
        return "bash not found, so %d Bash script(s) were not checked" % len(paths)
    for path in paths:
        result = subprocess.run([bash, "-n", path], capture_output=True, text=True)
        if result.returncode != 0:
            problems.append("%s fails bash -n: %s" % (rel(path), result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "error"))
    return "%d Bash script(s) pass bash -n" % len(paths)


def check_powershell(folder, problems):
    paths = list(files_under(folder, ".ps1"))
    pwsh = shutil.which("pwsh")
    if not pwsh:
        return "pwsh not found, so %d PowerShell script(s) were not checked" % len(paths)
    if not paths:
        return "0 PowerShell script(s)"
    script = (
        "$bad = 0; foreach ($f in $args) { $e = $null; $t = $null; "
        "[void][System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$t, [ref]$e); "
        "foreach ($x in $e) { $bad = 1; Write-Output ('{0}:{1}: {2}' -f $f, $x.Extent.StartLineNumber, $x.Message) } }; exit $bad"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as fh:
        fh.write(script)
        checker = fh.name
    try:
        result = subprocess.run([pwsh, "-NoProfile", "-NonInteractive", "-File", checker] + paths, capture_output=True, text=True)
    finally:
        os.unlink(checker)
    if result.returncode != 0:
        for line in (result.stdout or result.stderr).strip().splitlines()[:10]:
            problems.append("PowerShell parse error: %s" % line.replace(ROOT + os.sep, "").replace(os.sep, "/"))
    return "%d PowerShell script(s) parse" % len(paths)


def check_seeds(folder, problems):
    tool = os.path.join(folder, "common", "make-seed.py")
    manifest_path = os.path.join(folder, "common", "lab201-vms.json")
    flavors_path = os.path.join(folder, "common", "flavors.json")
    if not (os.path.isfile(tool) and os.path.isfile(manifest_path) and os.path.isfile(flavors_path)):
        return None
    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    with open(flavors_path, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)
    flavors, role_keys = catalog["flavors"], catalog.get("role_keys", [])

    def can_run(flavor, vm):
        # A flavor rates each machine type: y works, x needs extra steps, n is not offered.
        role = "routing peer" if vm["role"].startswith("routing peer") else vm["role"]
        return role not in role_keys or flavor.get("roles", [])[role_keys.index(role)] != "n"

    runs = seeds = 0
    bash = shutil.which("bash")
    with tempfile.TemporaryDirectory() as tmp:
        key = os.path.join(tmp, "key.pub")
        with open(key, "w", encoding="utf-8") as fh:
            fh.write(TEST_KEY)
        env = dict(os.environ, LAB201_ADMIN_PASSWORD_HASH=TEST_HASH)
        env.pop("LAB201_CONSOLE_PASSWORD", None)
        for flavor in flavors:
            # ISO-based flavors (Windows, Linux Mint, Tiny Core) need an ISO build and are not seeded this way.
            if flavor.get("iso") or flavor.get("status") == "planned":
                continue
            vms = [vm for vm in manifest["vms"] if can_run(flavor, vm)]
            names = [vm["name"] for vm in vms]
            trial = dict(manifest, default_flavor=flavor["id"], vms=vms)
            trial_path = os.path.join(tmp, "manifest-%s.json" % flavor["id"])
            with open(trial_path, "w", encoding="utf-8") as fh:
                json.dump(trial, fh)
            for tagging in ("hypervisor", "guest"):
                out = os.path.join(tmp, "%s-%s" % (flavor["id"], tagging))
                result = subprocess.run([sys.executable, tool, "--manifest", trial_path, "--flavors", flavors_path, "--out", out,
                                         "--ssh-key", key, "--tagging", tagging], capture_output=True, text=True, env=env)
                runs += 1
                label = "make-seed.py, flavor %s, %s tagging" % (flavor["id"], tagging)
                if result.returncode != 0:
                    problems.append("%s failed: %s" % (label, (result.stderr.strip().splitlines() or ["no message"])[-1]))
                    continue
                checked_status = False
                for name in names:
                    user = os.path.join(out, name, "user-data")
                    network = os.path.join(out, name, "network-config")
                    if not os.path.isfile(user) or not os.path.isfile(network):
                        problems.append("%s wrote no seed for %s" % (label, name))
                        continue
                    seeds += 1
                    with open(user, "r", encoding="utf-8") as fh:
                        text = fh.read()
                    if not text.startswith("#cloud-config"):
                        problems.append("%s: the user-data of %s does not start with #cloud-config" % (label, name))
                    # The status script that --action status reads. Its text is a JSON string in the YAML.
                    found = STATUS_FILE.search(text)
                    if not found:
                        problems.append("%s: the user-data of %s has no lab201-status script" % (label, name))
                    elif bash and not checked_status:
                        checked_status = True
                        script = os.path.join(tmp, "lab201-status.sh")
                        with open(script, "w", encoding="utf-8", newline="\n") as fh:
                            fh.write(json.loads(found.group(1)))
                        result = subprocess.run([bash, "-n", script], capture_output=True, text=True)
                        if result.returncode != 0:
                            problems.append("%s: the lab201-status script of %s fails bash -n: %s" % (label, name, (result.stderr.strip().splitlines() or ["error"])[-1]))
    return "%d seed run(s) wrote %d seeds, each with a status script: every cloud-image flavor with the machines it can run, both tagging modes" % (runs, seeds)


def main():
    folders = sorted(glob.glob(os.path.join(ROOT, "volumes", "*", "lab-scripts")))
    failed = False
    for folder in folders:
        problems = []
        parts = [check_python(folder, problems), check_bash(folder, problems), check_powershell(folder, problems)]
        seeds = check_seeds(folder, problems)
        if seeds:
            parts.append(seeds)
        if problems:
            failed = True
            print("lab scripts: FAILED in %s" % rel(folder), file=sys.stderr)
            for p in problems:
                print("  %s" % p, file=sys.stderr)
        else:
            print("lab scripts: OK in %s (%s)" % (rel(folder), "; ".join(parts)))
    if not folders:
        print("lab scripts: no lab-scripts folder found")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
