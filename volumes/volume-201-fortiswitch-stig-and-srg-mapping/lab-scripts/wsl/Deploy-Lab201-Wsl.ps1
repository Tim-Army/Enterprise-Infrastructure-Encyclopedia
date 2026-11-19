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
  [ValidateSet('Deploy', 'Check', 'Status', 'Remove')] [string] $Action = 'Deploy',
  [string] $PythonCommand,
  [string[]] $SshKeyFile,
  [string] $InstallRoot = (Join-Path $env:USERPROFILE 'wsl-lab201'),
  [string] $Manifest,
  [string] $WorkDir
)

$ErrorActionPreference = 'Stop'

# Windows PowerShell 5.1 leaves $PSScriptRoot empty inside param() when the script is started with -File,
# so the defaults that need the script's folder are set here.
if (-not $Manifest) { $Manifest = Join-Path $PSScriptRoot '..\common\lab201-vms.json' }
if (-not $WorkDir) { $WorkDir = Join-Path $PSScriptRoot 'work' }

# Find a Python 3 that really runs. -PythonCommand names the command to use (for example python3.15 or "py -3.15").
# Without it the script tries python3, then the py launcher, then python.
# On Windows, python.exe and python3.exe can be Microsoft Store stubs that only print "Python was not found".
$pyExe = $null; $pyArgs = @()
$pyCandidates = @(, @('python3')) + @(, @('py', '-3')) + @(, @('python'))
if ($PythonCommand) { $pyCandidates = @(, @($PythonCommand.Trim() -split '\s+')) }
foreach ($cand in $pyCandidates) {
  if (-not (Get-Command $cand[0] -ErrorAction SilentlyContinue)) { continue }
  $rest = @($cand | Select-Object -Skip 1)
  try { $ver = (& $cand[0] @rest --version 2>&1 | Out-String) } catch { continue }
  if ($LASTEXITCODE -eq 0 -and $ver -match 'Python 3\.') { $pyExe = $cand[0]; $pyArgs = $rest; break }
}
if (-not $pyExe -and $PythonCommand -and $Action -ne 'Check') { throw "-PythonCommand '$PythonCommand' did not run Python 3. Check the command with: $PythonCommand --version" }
if (-not $pyExe -and $Action -eq 'Deploy') {
  throw 'Python 3 was not found. Install it (for example: winget install Python.Python.3.15), open a new PowerShell window, and run the script again.'
}

function Get-WebText {
  # Invoke-WebRequest returns a byte array for some text files (for example SHA256SUMS), so decode it.
  param([string] $Uri)
  $r = Invoke-WebRequest -Uri $Uri
  if ($r.Content -is [byte[]]) { return [System.Text.Encoding]::UTF8.GetString($r.Content) }
  return [string]$r.Content
}
$env:WSL_UTF8 = '1'

if ($Action -eq 'Check') {
  # Tests what a deploy needs on this computer and changes nothing.
  $script:failed = 0
  function Show-Check {
    param([string] $State, [string] $What, [string] $Fix)
    $color = switch ($State) { 'OK' { 'Green' } 'WARN' { 'Yellow' } default { 'Red' } }
    if ($State -eq 'FAIL') { $script:failed++ }
    Write-Host ('[{0,-4}] {1}' -f $State, $What) -ForegroundColor $color
    if ($Fix -and $State -ne 'OK') { Write-Host "       $Fix" }
  }
  Write-Host 'Checking this computer for the lab build. Nothing is changed.'
  Show-Check 'OK' "PowerShell $($PSVersionTable.PSVersion)"

  $haveWsl = [bool](Get-Command wsl.exe -ErrorAction SilentlyContinue)
  if (-not $haveWsl) {
    Show-Check 'FAIL' 'wsl.exe is not installed' 'Run: wsl --install --no-distribution   Then restart Windows'
  } else {
    # wsl.exe is on every Windows 11 computer. Until WSL is installed it is a stub that only says so, with exit code 1.
    $wslVersion = ''
    try { $wslVersion = (@(wsl.exe --version 2>$null) | Where-Object { $_ -match '\d' } | Select-Object -First 1) } catch { $wslVersion = '' }
    if ($LASTEXITCODE -eq 0 -and $wslVersion) { Show-Check 'OK' "WSL: $("$wslVersion".Trim())" }
    else {
      try { $null = @(wsl.exe --status 2>$null) } catch { }
      if ($LASTEXITCODE -eq 0) { Show-Check 'WARN' 'This WSL does not report a version, so it is older than the Store release' 'Run: wsl --update' }
      else { Show-Check 'FAIL' 'WSL is not installed (wsl.exe answers that it is not)' 'Run: wsl --install --no-distribution   Then restart Windows'; $haveWsl = $false }
    }
  }

  if ($pyExe) {
    $pyName = (@($pyExe) + $pyArgs) -join ' '
    Show-Check 'OK' "Python: $pyName ($((& $pyExe @pyArgs --version 2>&1 | Out-String).Trim()))"
  } elseif ($PythonCommand) {
    Show-Check 'FAIL' "-PythonCommand '$PythonCommand' did not run Python 3" "Check it with: $PythonCommand --version"
  } else {
    Show-Check 'FAIL' 'Python 3 was not found (tried python3, py -3, and python)' 'Run: winget install Python.Python.3.15   Then open a new PowerShell window'
  }

  if (-not $SshKeyFile) {
    Show-Check 'FAIL' 'No SSH public key was given (-SshKeyFile)' 'Make one with: ssh-keygen -t ed25519   Then pass: -SshKeyFile ~\.ssh\id_ed25519.pub'
  } else {
    foreach ($k in $SshKeyFile) {
      if (-not (Test-Path $k)) { Show-Check 'FAIL' "SSH public key not found: $k" 'Make one with: ssh-keygen -t ed25519'; continue }
      $first = (Get-Content -Path $k -TotalCount 1)
      if ($first -match '^(ssh-|ecdsa-|sk-)') { Show-Check 'OK' "SSH public key: $k" }
      elseif ($first -match 'PRIVATE KEY') { Show-Check 'FAIL' "$k is a private key" 'Pass the public key, the file that ends in .pub' }
      else { Show-Check 'FAIL' "$k does not look like an SSH public key" 'Pass the file that ends in .pub' }
    }
  }

  $checkLab = $null
  if (Test-Path $Manifest) {
    try { $checkLab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json } catch { Show-Check 'FAIL' "The manifest is not valid JSON: $Manifest" 'Download the zip from the Lab Builder again' }
  } else {
    Show-Check 'FAIL' "The manifest was not found: $Manifest" 'Keep the script and the common folder together, as they are in the zip'
  }
  if ($checkLab) {
    $checkHosts = @($checkLab.vms | Where-Object { $_.wsl })
    if ($checkHosts.Count) { Show-Check 'OK' "Manifest: $($checkHosts.Count) hosts that WSL can build" }
    else { Show-Check 'FAIL' 'The manifest has no host that WSL can build' 'Make the manifest with the Lab Builder for WSL 2' }
    $notUbuntu = @($checkHosts | Where-Object { ($_.flavor -and $_.flavor -ne 'ubuntu-24.04') -or (-not $_.flavor -and $checkLab.default_flavor -and $checkLab.default_flavor -ne 'ubuntu-24.04') } | ForEach-Object { $_.name })
    if ($notUbuntu.Count) { Show-Check 'FAIL' "WSL builds Ubuntu 24.04 only, and these hosts ask for another flavor: $($notUbuntu -join ', ')" 'Pick Ubuntu 24.04 for them in the Lab Builder' }
    if ($haveWsl) {
      $have = @(wsl.exe --list --quiet 2>$null | ForEach-Object { "$_".Trim() } | Where-Object { $_ })
      $existing = @($checkHosts | Where-Object { $have -contains "lab201-$($_.name)" })
      if ($existing.Count) { Show-Check 'OK' "$($existing.Count) lab distribution(s) already exist. A deploy skips them" }
    }
  }

  if ($InstallRoot -match '^[A-Za-z]:' -and -not (Test-Path ($InstallRoot.Substring(0, 2) + '\'))) {
    Show-Check 'FAIL' "Drive $($InstallRoot.Substring(0, 2)) of the distributions folder does not exist ($InstallRoot)" 'Pass -InstallRoot with a folder on a drive this computer has'
  } else {
    Show-Check 'OK' "Distributions folder: $InstallRoot"
    if ($InstallRoot -match '^[A-Za-z]:') {
      $freeGb = [math]::Round((Get-PSDrive -Name $InstallRoot.Substring(0, 1)).Free / 1GB)
      if ($freeGb -ge 20) { Show-Check 'OK' "Disk: $freeGb GB free" }
      else { Show-Check 'WARN' "Disk: $freeGb GB free. Eight Ubuntu distributions with their packages need about 20 GB" 'Free some space, or pass -InstallRoot with a folder on a larger drive' }
    }
  }
  Show-Check 'OK' 'The Ubuntu image comes from cloud-images.ubuntu.com, so the build needs the internet'

  if ($script:failed) { Write-Host "$($script:failed) problem(s) to fix before the build." -ForegroundColor Red; exit 1 }
  Write-Host 'Ready. Run the preview next (-WhatIf).' -ForegroundColor Green
  return
}

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
& $pyExe @pyArgs (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --wsl @keys
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
