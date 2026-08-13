# Chapter 03: RHCSA — Services, Networking, SELinux, and Containers (EX200)

## Learning Objectives

- Cover the remaining RHCSA objective areas: software/services, networking, SELinux, firewalld, and containers.
- Drill each as a performance-exam task with verification.
- Complete the RHCSA objective coverage begun in [Chapter 02](02-rhcsa-users-storage-boot.md).

## Hands-On Lab

A RHEL-family VM with SELinux **enforcing** and network access. **Cost:** none.

### Lab 3.1 — Software management (dnf, modules, Flatpak)

**Objective (task):** "Install a package from a repo you configure, and query what provides a file."

```bash
sudo tee /etc/yum.repos.d/lab.repo >/dev/null <<'EOF'
[lab-baseos]
name=Lab BaseOS
baseurl=file:///mnt/BaseOS
enabled=1
gpgcheck=0
EOF
sudo dnf install -y tree
dnf provides */lspci 2>/dev/null | head -3 || echo "dnf provides maps files to packages"
rpm -qf $(command -v tree)
```

**Expected result:** A repo defined, a package installed, and `rpm -qf`/`dnf provides` mapping a file to its owning package — repo configuration, dnf install/remove, `dnf provides`, and awareness of module streams and Flatpak are the software objectives.

**Negative test:** `dnf install` with `gpgcheck=1` and no imported key — the transaction fails on signature; the exam tests knowing when to import a key vs disable the check.

**Rollback:** `sudo dnf remove -y tree; sudo rm /etc/yum.repos.d/lab.repo`.

### Lab 3.2 — Services with systemd

**Objective (task):** "Ensure a service starts at boot and is running now; mask a service that must never start."

```bash
sudo systemctl enable --now chronyd
systemctl is-enabled chronyd && systemctl is-active chronyd
sudo systemctl mask rsync 2>/dev/null; systemctl is-enabled rsync 2>/dev/null || echo "rsync masked (cannot start)"
```

**Expected result:** `chronyd` enabled and active, and a masked service reported as unstartable — `enable --now`, `is-enabled`/`is-active`, and the difference between **disabled** (won't auto-start) and **masked** (can't start at all) are RHCSA service objectives.

**Negative test:** Try to `start` a masked service — refused until unmasked; masking is stronger than disabling, a distinction the exam probes.

**Rollback:** `sudo systemctl unmask rsync`.

### Lab 3.3 — Networking with nmcli

**Objective (task):** "Configure a static IP, gateway, DNS, and hostname persistently."

```bash
CON=$(nmcli -t -f NAME con show | head -1)
sudo nmcli con mod "$CON" ipv4.addresses 192.0.2.50/24 ipv4.gateway 192.0.2.1 ipv4.dns 192.0.2.53 ipv4.method manual 2>/dev/null || echo "(lab: apply to a test connection)"
sudo hostnamectl set-hostname rhcsa-lab.example.com
hostnamectl --static
nmcli -f ipv4.addresses con show "$CON" 2>/dev/null | head -1
```

**Expected result:** The connection carrying a static address/gateway/DNS and the static hostname set — `nmcli con mod` for persistent networking and `hostnamectl` are the networking objectives; changes must **persist across reboot** (NetworkManager connection profiles, not transient `ip` commands).

**Negative test:** Configure with `ip addr add` instead of `nmcli` — it works until reboot, then vanishes; RHCSA scores persistence, so transient commands fail the task.

**Rollback:** Restore DHCP on the test connection as needed.

### Lab 3.4 — SELinux

**Objective (task):** "Serve web content from a non-default directory with SELinux enforcing."

```bash
sudo dnf install -y httpd >/dev/null && sudo mkdir -p /web/content
echo "hello" | sudo tee /web/content/index.html >/dev/null
sudo sed -i 's#^DocumentRoot.*#DocumentRoot "/web/content"#' /etc/httpd/conf/httpd.conf
sudo semanage fcontext -a -t httpd_sys_content_t "/web/content(/.*)?"
sudo restorecon -Rv /web/content
sudo systemctl enable --now httpd && curl -s localhost | head -1
ls -Zd /web/content
```

**Expected result:** The page served from `/web/content` with the directory labeled `httpd_sys_content_t` — SELinux is the objective most candidates lose points on: the fix is **`semanage fcontext` + `restorecon`** (persistent), and booleans (`setsebool -P`) for behaviors. `getenforce` must read `Enforcing`.

**Negative test:** Point `DocumentRoot` at `/web/content` without relabeling — httpd is denied (`ausearch -m AVC` shows it) and the page 403s though permissions look fine; SELinux, not DAC, is the gate.

**Rollback:** `sudo systemctl disable --now httpd; sudo dnf remove -y httpd; sudo semanage fcontext -d "/web/content(/.*)?"; sudo rm -rf /web/content`.

### Lab 3.5 — firewalld

**Objective (task):** "Permit HTTP through the firewall persistently."

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
sudo firewall-cmd --list-services | tr ' ' '\n' | grep http
```

**Expected result:** `http` in the active zone's services after a reload — firewalld with `--permanent` + `--reload` (runtime vs permanent is the exam's favorite firewalld trap) is a core objective.

**Negative test:** Add the service **without** `--permanent` — it works now but vanishes on reload/reboot; the exam scores the permanent rule.

**Rollback:** `sudo firewall-cmd --permanent --remove-service=http && sudo firewall-cmd --reload`.

### Lab 3.6 — Containers with Podman (rootless)

**Objective (task):** "Run a container as a non-root user and have it start at boot via a systemd user service."

```bash
sudo dnf install -y podman >/dev/null
podman run -d --name web -p 8080:80 registry.access.redhat.com/ubi9/httpd-24 2>/dev/null || podman run -d --name web -p 8080:80 docker.io/library/httpd
podman ps --format "{{.Names}} {{.Status}}"
podman generate systemd --name web --files --new >/dev/null 2>&1 && ls container-web.service 2>/dev/null || echo "quadlet/systemd integration is the exam objective"
```

**Expected result:** A rootless container running and its systemd unit generated — RHCSA now includes **container objectives**: pulling images, running rootless containers, persistent storage, and starting them via systemd (generate-systemd/Quadlet). `podman ps` confirms it runs.

**Negative test:** Expect a rootless container to bind port 80 — it can't (privileged port); mapping to 8080 is why the exam uses high ports, a rootless-container fact.

**Rollback:** `podman rm -f web; rm -f container-web.service`.

## Summary and Completion Checklist

- [ ] Software, services (enable/mask), and nmcli persistent networking drilled.
- [ ] SELinux context fix (`semanage fcontext` + `restorecon`) and firewalld permanent rules done.
- [ ] Rootless Podman container run and systemd-integrated.
- [ ] RHCSA objective coverage complete across Chapters 02–03.
