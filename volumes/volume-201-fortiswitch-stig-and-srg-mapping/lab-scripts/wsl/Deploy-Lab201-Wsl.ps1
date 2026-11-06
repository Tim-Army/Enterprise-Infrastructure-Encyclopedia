<#
.SYNOPSIS
  Creates the Volume CCI lab service hosts as WSL 2 distributions on Windows 11.

.DESCRIPTION
  WSL does not make virtual machines. Each lab host becomes one Ubuntu
  distribution, and all of them run inside the single WSL 2 virtual machine,
  which means they share one kernel and one network namespace. Each host's
  addresses are put on VLAN interfaces of one dummy device, so the hosts can
  reach each other but they are not isolated from each other, and no VLAN tag
  leaves the computer. WSL cannot carry an 802.1Q trunk to a hardware switch.

  The script builds only the hosts that do not need a hardware link: svc-201a,
  svc-201b, ca-201, dhcp-201, admin-201, static-1, static-2, and attacker-201.
  gw-201, rtr-peer-1, rtr-peer-2, and mcast-src-201 need a trunk or routed
  links, so use another chapter's platform for them.

  Needs Windows 11 with WSL 2 (wsl --update), PowerShell 5.1 or 7, and Python 3.

.EXAMPLE
  .\Deploy-Lab201-Wsl.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [ValidateSet('Deploy', 'Status', 'Remove')] [string] $Action = 'Deploy',
  [string[]] $SshKeyFile,
  [string] $InstallRoot = (Join-Path $env:USERPROFILE 'wsl-lab201'),
  [string] $Manifest = (Join-Path $PSScriptRoot '..\common\lab201-vms.json'),
  [string] $WorkDir = (Join-Path $PSScriptRoot 'work')
)

$ErrorActionPreference = 'Stop'

function Get-WebText {
  # Invoke-WebRequest returns a byte array for some text files (for example SHA256SUMS), so decode it.
  param([string] $Uri)
  $r = Invoke-WebRequest -Uri $Uri
  if ($r.Content -is [byte[]]) { return [System.Text.Encoding]::UTF8.GetString($r.Content) }
  return [string]$r.Content
}
$env:WSL_UTF8 = '1'

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) { throw 'wsl.exe is not installed. Run: wsl --install --no-distribution' }
$lab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json
$hosts = @($lab.vms | Where-Object { $_.wsl })
$distroOf = { param($n) "lab201-$n" }

if ($Action -eq 'Status') {
  wsl.exe --list --verbose | Select-String -Pattern 'lab201-|NAME'
  return
}
if ($Action -eq 'Remove') {
  foreach ($h in $hosts) {
    if ($PSCmdlet.ShouldProcess((& $distroOf $h.name), 'Unregister the distribution and delete its disk')) {
      wsl.exe --unregister (& $distroOf $h.name)
    }
  }
  return
}

if (-not $SshKeyFile) { throw '-SshKeyFile is required for -Action Deploy.' }
New-Item -ItemType Directory -Force -Path $WorkDir, $InstallRoot | Out-Null

# The newest Ubuntu 24.04 WSL image, a .wsl file (a gzip-compressed tar archive),
# checked against Canonical's SHA-256 sums. It is saved with a .tar.gz name so that
# wsl --import accepts it on every WSL version.
$base = $lab.image.wsl_release_url
$found = [regex]::Matches((Get-WebText $base), $lab.image.wsl_pattern) | ForEach-Object { $_.Value } | Sort-Object -Unique
if (-not $found) { throw "No Ubuntu WSL image found at $base" }
$imageName = $found | Sort-Object { [version]($_ -replace '^ubuntu-([\d.]+)-wsl.*$', '$1') } | Select-Object -Last 1
$rootfsName = $imageName
$rootfs = Join-Path $WorkDir ($imageName -replace '\.wsl$', '.tar.gz')
if (-not (Test-Path $rootfs)) {
  Invoke-WebRequest -Uri ($base + $imageName) -OutFile $rootfs
  $sums = (Get-WebText ($base + 'SHA256SUMS')) -split "`n"
  $want = ($sums | Where-Object { $_ -match [regex]::Escape($rootfsName) } | Select-Object -First 1) -replace '\s.*', ''
  $got = (Get-FileHash -Algorithm SHA256 -Path $rootfs).Hash.ToLower()
  if ($want -ne $got) { Remove-Item $rootfs; throw "SHA-256 mismatch for ${rootfsName}: expected $want, got $got" }
}

# One provisioning script per host, written with Unix line endings.
$keys = @(); foreach ($k in $SshKeyFile) { $keys += '--ssh-key'; $keys += (Resolve-Path $k).Path }
$seedDir = Join-Path $WorkDir 'wsl'
& python (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --wsl @keys
if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }

foreach ($h in $hosts) {
  $distro = & $distroOf $h.name
  $existing = (wsl.exe --list --quiet) -contains $distro
  if ($existing) { Write-Host "$distro exists. Skipped."; continue }
  if (-not $PSCmdlet.ShouldProcess($distro, 'Import, provision, and restart the distribution')) { continue }
  Write-Host "Creating $distro"
  wsl.exe --import $distro (Join-Path $InstallRoot $h.name) $rootfs --version 2
  if ($LASTEXITCODE -ne 0) { throw "wsl --import failed for $distro." }
  $script = (Resolve-Path (Join-Path $seedDir "$($h.name)\wsl-provision.sh")).Path
  $linuxPath = (wsl.exe -d $distro -u root --exec wslpath -a $script).Trim()
  wsl.exe -d $distro -u root --exec bash $linuxPath
  if ($LASTEXITCODE -ne 0) { throw "Provisioning failed for $distro." }
  # Restart so wsl.conf takes effect: systemd, the hostname, and the boot command that adds the lab addresses.
  wsl.exe --terminate $distro
  wsl.exe -d $distro -u root --exec true
}
Write-Host 'Done. Run: wsl -d lab201-svc-201a -- ip -br addr'
