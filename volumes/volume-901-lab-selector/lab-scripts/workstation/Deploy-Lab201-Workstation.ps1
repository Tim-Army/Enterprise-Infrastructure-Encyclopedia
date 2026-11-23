<#
.SYNOPSIS
  Creates the Volume CCI lab virtual machines in VMware Workstation Pro on Windows.

.DESCRIPTION
  Reads ..\common\lab201-vms.json, imports the Ubuntu cloud image OVA once with
  ovftool, clones one full virtual machine for each lab host with vmrun, writes
  each machine's hardware, network adapters, and cloud-init seed ISO into its
  .vmx file, and starts it.

  Workstation has no VLAN-aware virtual switch, so every VLAN tag is created
  inside the guests (make-seed.py --tagging guest). Create the lab networks in
  the Virtual Network Editor first, as described in Chapter 11:
    -BridgeVmnet  the one bridged network (vmnet0 by default), bridged to the NIC
                  that cables to the switches. The trunk and the out-of-band
                  network both use it, because Workstation supports one bridge.
    -McastVmnet  host-only, with the DHCP service turned off
  -WanVmnet is the network the build NICs use (vmnet8, the NAT network, by default).

  Needs PowerShell 5.1 or 7, Workstation Pro 17 or later, and Python 3 with
  pycdlib (pip install pycdlib) for the seed ISOs.

  -Action picks what the script does:
    Deploy           builds and starts the machines (the default)
    Check            tests what a deploy needs on this computer and changes nothing
    Status           shows each machine, whether its first boot has finished, and how
                     to log in. With -Wait it keeps checking until every machine has finished
    RemoveBuildNics  switches the build network adapter of each machine off
    Snapshot         takes the baseline snapshot of every machine (Lab 999.6)
    Restore          returns every machine to the baseline snapshot and starts it
    Remove           stops and deletes the machines

.EXAMPLE
  .\Deploy-Lab201-Workstation.ps1 -SshKeyFile ~\.ssh\id_ed25519.pub -WhatIf

.EXAMPLE
  .\Deploy-Lab201-Workstation.ps1 -VmRoot E:\VMs\lab201 -SshKeyFile ~\.ssh\id_ed25519.pub

.EXAMPLE
  .\Deploy-Lab201-Workstation.ps1 -Action Status -Wait
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [string] $VmRoot,
  [ValidateSet('Deploy', 'Check', 'Status', 'RemoveBuildNics', 'Snapshot', 'Restore', 'Remove')] [string] $Action = 'Deploy',
  [switch] $Wait,
  [ValidateRange(1, 600)] [int] $WaitMinutes = 30,
  [ValidatePattern('^[A-Za-z][A-Za-z0-9_-]{1,39}$')] [string] $SnapshotName = 'baseline-201',
  [string] $PythonCommand,
  [string[]] $SshKeyFile,
  [string] $Manifest,
  [string] $WorkDir,
  [string] $WorkstationDir,
  [ValidatePattern('^vmnet\d+$')] [string] $BridgeVmnet = 'vmnet0',
  [ValidatePattern('^vmnet\d+$')] [string] $McastVmnet = 'vmnet5',
  [ValidatePattern('^vmnet\d+$')] [string] $WanVmnet = 'vmnet8',
  [string] $OvfToolPath,
  [string] $LicenseFile,
  [hashtable] $FlavorImages = @{},
  [switch] $AddToLibrary
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
  throw 'Python 3 was not found. Install it (for example: winget install Python.Python.3.15), open a new PowerShell window, run "python -m pip install pycdlib", and run the script again.'
}

function Get-WebText {
  # Invoke-WebRequest returns a byte array for some text files (for example SHA256SUMS), so decode it.
  param([string] $Uri)
  $r = Invoke-WebRequest -Uri $Uri
  if ($r.Content -is [byte[]]) { return [System.Text.Encoding]::UTF8.GetString($r.Content) }
  return [string]$r.Content
}

function Get-DefaultVmRoot {
  # A lab201 folder inside Workstation's default folder for virtual machines:
  # the one set in Preferences, or Documents\Virtual Machines.
  $vmHome = $null
  $prefs = Join-Path $env:APPDATA 'VMware\preferences.ini'
  if (Test-Path $prefs) {
    $line = Get-Content $prefs | Where-Object { $_ -match '^\s*prefvmx\.defaultVMPath\s*=\s*"(.+)"\s*$' } | Select-Object -First 1
    if ($line) { $vmHome = $line -replace '^\s*prefvmx\.defaultVMPath\s*=\s*"(.+)"\s*$', '$1' }
  }
  if (-not $vmHome) { $vmHome = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Virtual Machines' }
  return (Join-Path $vmHome 'lab201')
}

function Find-WorkstationDir {
  # Workstation Pro 17 installs under Program Files (x86). Later releases (26.0 was checked) install under Program Files.
  return (@('C:\Program Files\VMware\VMware Workstation', 'C:\Program Files (x86)\VMware\VMware Workstation') |
    Where-Object { Test-Path (Join-Path $_ 'vmrun.exe') } | Select-Object -First 1)
}

if (-not $VmRoot) { $VmRoot = Get-DefaultVmRoot }
if (-not $WorkstationDir) { $WorkstationDir = Find-WorkstationDir }

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
  Write-Host "Checking this computer for the lab build. Nothing is changed."
  Show-Check 'OK' "PowerShell $($PSVersionTable.PSVersion)"

  if ($pyExe) {
    $pyName = (@($pyExe) + $pyArgs) -join ' '
    Show-Check 'OK' "Python: $pyName ($((& $pyExe @pyArgs --version 2>&1 | Out-String).Trim()))"
    $null = & $pyExe @pyArgs -c 'import pycdlib' 2>&1
    if ($LASTEXITCODE -eq 0) { Show-Check 'OK' 'Python package pycdlib (for the seed ISOs)' }
    else { Show-Check 'FAIL' 'Python package pycdlib is not installed' "Run: $pyName -m pip install pycdlib" }
  } elseif ($PythonCommand) {
    Show-Check 'FAIL' "-PythonCommand '$PythonCommand' did not run Python 3" "Check it with: $PythonCommand --version"
  } else {
    Show-Check 'FAIL' 'Python 3 was not found (tried python3, py -3, and python)' 'Run: winget install Python.Python.3.15   Then open a new PowerShell window and run: python -m pip install pycdlib'
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

  if ($WorkstationDir -and (Test-Path (Join-Path $WorkstationDir 'vmrun.exe'))) {
    $ui = Join-Path $WorkstationDir 'vmware.exe'
    $wsVersion = if (Test-Path $ui) { (Get-Item $ui).VersionInfo.ProductVersion } else { 'version unknown' }
    Show-Check 'OK' "VMware Workstation in $WorkstationDir ($wsVersion)"
    if (Test-Path (Join-Path $WorkstationDir 'vmware-vdiskmanager.exe')) { Show-Check 'OK' 'vmware-vdiskmanager.exe' }
    else { Show-Check 'FAIL' "vmware-vdiskmanager.exe is not in $WorkstationDir" 'Repair the Workstation install, or pass -WorkstationDir' }
    $ovf = if ($OvfToolPath) { $OvfToolPath } elseif (Test-Path (Join-Path $WorkstationDir 'OVFTool\ovftool.exe')) { Join-Path $WorkstationDir 'OVFTool\ovftool.exe' } else { (Get-Command ovftool.exe -ErrorAction SilentlyContinue).Source }
    if ($ovf -and (Test-Path $ovf)) { Show-Check 'OK' "OVF Tool: $ovf" }
    else { Show-Check 'FAIL' 'OVF Tool (ovftool.exe) was not found' 'Install OVF Tool and pass -OvfToolPath with the path of ovftool.exe' }
  } else {
    Show-Check 'FAIL' 'VMware Workstation Pro was not found (no vmrun.exe)' 'Install Workstation Pro, or pass -WorkstationDir with its install folder'
  }

  $checkLab = $null
  if (Test-Path $Manifest) {
    try { $checkLab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json } catch { Show-Check 'FAIL' "The manifest is not valid JSON: $Manifest" 'Download the zip from the Lab Selector again' }
  } else {
    Show-Check 'FAIL' "The manifest was not found: $Manifest" 'Keep the script and the common folder together, as they are in the zip'
  }
  if ($checkLab) {
    Show-Check 'OK' "Manifest: $(@($checkLab.vms).Count) machines"
    if (@($checkLab.vms | ForEach-Object { $_.nics } | Where-Object { $_.net -eq 'lab201-t2' }).Count -gt 0) {
      Show-Check 'FAIL' 'The manifest has a second trunk (lab201-t2), and Workstation supports one bridged network' 'Make the manifest with the Lab Selector for VMware Workstation Pro'
    }
    $catalog = Get-Content -Raw -Path (Join-Path $PSScriptRoot '..\common\flavors.json') | ConvertFrom-Json
    $isoMachines = @($checkLab.vms | Where-Object {
        $fid = if ($_.flavor) { $_.flavor } elseif ($checkLab.default_flavor) { $checkLab.default_flavor } else { $catalog.default }
        ($catalog.flavors | Where-Object { $_.id -eq $fid } | Select-Object -First 1).iso
      } | ForEach-Object { $_.name })
    if ($isoMachines.Count) { Show-Check 'FAIL' "ISO-based flavors cannot run on Workstation: $($isoMachines -join ', ')" 'Pick a cloud-image flavor for these machines in the Lab Selector' }
    $needGb = ($checkLab.vms | Measure-Object -Property disk_gb -Sum).Sum
    $needMb = ($checkLab.vms | Measure-Object -Property memory_mb -Sum).Sum
    $totalMb = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB)
    if ($totalMb -ge $needMb + 4096) { Show-Check 'OK' ("Memory: the machines use {0:N1} GB of {1:N1} GB" -f ($needMb / 1024), ($totalMb / 1024)) }
    else { Show-Check 'WARN' ("Memory: the machines use {0:N1} GB and this computer has {1:N1} GB" -f ($needMb / 1024), ($totalMb / 1024)) 'Leave machines out in the Lab Selector, or make them smaller' }
  }

  if ($VmRoot -match '^[A-Za-z]:' -and -not (Test-Path ($VmRoot.Substring(0, 2) + '\'))) {
    Show-Check 'FAIL' "Drive $($VmRoot.Substring(0, 2)) of the machines folder does not exist ($VmRoot)" 'Pass -VmRoot with a folder on a drive this computer has'
  } else {
    Show-Check 'OK' "Machines folder: $VmRoot"
    if ($VmRoot -match '^[A-Za-z]:' -and $checkLab) {
      $freeGb = [math]::Round((Get-PSDrive -Name $VmRoot.Substring(0, 1)).Free / 1GB)
      if ($freeGb -ge $needGb) { Show-Check 'OK' "Disk: $freeGb GB free. The thin disks can grow to $needGb GB" }
      else { Show-Check 'WARN' "Disk: $freeGb GB free, and the thin disks can grow to $needGb GB" 'Free some space, or pass -VmRoot with a folder on a larger drive' }
    }
  }

  foreach ($net in @(@($WanVmnet, 'build network (NAT)'), @($McastVmnet, 'segment 12 network (host-only)'))) {
    $adapter = Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq "VMware Network Adapter $($net[0].Replace('vmnet', 'VMnet'))" }
    if ($adapter) { Show-Check 'OK' "$($net[0]), the $($net[1])" }
    else { Show-Check 'WARN' "$($net[0]), the $($net[1]), has no host adapter" 'Create it in the Virtual Network Editor (Chapter 11)' }
  }
  Show-Check 'OK' "$BridgeVmnet, the bridged network, cannot be checked from here. Bind it to the lab adapter in the Virtual Network Editor"

  if ($script:failed) { Write-Host "$($script:failed) problem(s) to fix before the build." -ForegroundColor Red; exit 1 }
  Write-Host 'Ready. Run the preview next (-WhatIf).' -ForegroundColor Green
  return
}

if ($VmRoot -match '^[A-Za-z]:' -and -not (Test-Path ($VmRoot.Substring(0, 2) + '\'))) {
  throw "Drive $($VmRoot.Substring(0, 2)) in the machines folder ($VmRoot) does not exist. Pass -VmRoot with a folder on a drive this computer has."
}
Write-Host "Machines folder: $VmRoot"
if (-not $WorkstationDir) { throw 'vmrun.exe was not found under Program Files or Program Files (x86). Is Workstation Pro installed? Pass -WorkstationDir with its install folder.' }
$vmrun = Join-Path $WorkstationDir 'vmrun.exe'
$ovftool = if ($OvfToolPath) { $OvfToolPath } elseif (Test-Path (Join-Path $WorkstationDir 'OVFTool\ovftool.exe')) { Join-Path $WorkstationDir 'OVFTool\ovftool.exe' } else { (Get-Command ovftool.exe -ErrorAction SilentlyContinue).Source }
$vdisk = Join-Path $WorkstationDir 'vmware-vdiskmanager.exe'
if (-not $ovftool) { throw "ovftool.exe was not found in $WorkstationDir\OVFTool or on the PATH. Install OVF Tool and pass -OvfToolPath." }
foreach ($exe in $vmrun, $ovftool, $vdisk) { if (-not (Test-Path $exe)) { throw "Not found: $exe. Is Workstation Pro installed, is -WorkstationDir right, and is OVF Tool installed (-OvfToolPath)?" } }

$lab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json
# The machine whose first adapter stays as the uplink to the external firewall. The Lab Selector writes "uplink" into
# the manifest when the build keeps one. RemoveBuildNics and Snapshot then leave that adapter alone.
$uplinkVm = if ($lab.PSObject.Properties['uplink'] -and $lab.uplink.vm) { [string]$lab.uplink.vm } else { '' }
$names = @{}; $i = 0
foreach ($vm in $lab.vms) { $i++; $names[$vm.name] = $i }
$vmnetOf = @{ 'lab201-t1' = $BridgeVmnet; 'lab201-t2' = $BridgeVmnet; 'lab201-oob' = $BridgeVmnet; 'lab201-mcast' = $McastVmnet; 'lab201-wan' = $WanVmnet }
# Workstation supports one bridged network. With T1 and T2 on it, the gateway would bridge the two NICs into a loop.
if (@($lab.vms | ForEach-Object { $_.nics } | Where-Object { $_.net -eq 'lab201-t2' }).Count -gt 0) {
  throw "The manifest has a second trunk (lab201-t2), but Workstation supports one bridged network. Generate the manifest with the Lab Selector for Workstation, which merges T1 and T2 into one trunk."
}

$flavorCatalog = Get-Content -Raw -Path (Join-Path $PSScriptRoot '..\common\flavors.json') | ConvertFrom-Json

function Get-FlavorId {
  param($Vm, $Lab)
  if ($Vm.flavor) { return [string]$Vm.flavor }
  if ($Lab.default_flavor) { return [string]$Lab.default_flavor }
  return [string]$flavorCatalog.default
}

function Get-FlavorRecord {
  param([string] $Id)
  $f = $flavorCatalog.flavors | Where-Object { $_.id -eq $Id } | Select-Object -First 1
  if (-not $f) { throw "Unknown flavor $Id" }
  return $f
}

function Get-ImageFlavorId {
  # A hardened (STIG) flavor uses the image of its base flavor.
  param([string] $Id)
  $f = Get-FlavorRecord $Id
  while ($f.base -and -not $f.image) { $f = Get-FlavorRecord $f.base }
  return [string]$f.id
}

function Resolve-FlavorOva {
  # An OVA you pass in -FlavorImages wins. Otherwise resolve-image.py finds, downloads, and checks the published OVA.
  # With -WhatIf nothing is downloaded and no site is read: the function names the file a deploy fetches, and returns nothing.
  param([string] $Id, [string] $WorkDir, [hashtable] $Supplied)
  $imageId = Get-ImageFlavorId $Id
  foreach ($k in $Id, $imageId) {
    if ($Supplied -and $Supplied.ContainsKey($k)) { return (Resolve-Path $Supplied[$k]).Path }
  }
  $image = (Get-FlavorRecord $imageId).image
  if (-not $image.ova) {
    throw "No OVA is available for the flavor $imageId. Make one from its qcow2 image, then pass it with -FlavorImages @{ '$imageId' = 'path\to\image.ova' }."
  }
  $imageDir = Join-Path $WorkDir 'images'
  if ($WhatIfPreference) {
    Write-Host "What if: Performing the operation `"Download the cloud image into $imageDir if it is not there or does not match the publisher's checksum, then check it`" on target `"$($image.base)$($image.ova)`"."
    return
  }
  $out = & $pyExe @pyArgs (Join-Path $PSScriptRoot '..\common\resolve-image.py') --flavor $imageId --ova --out $imageDir
  if ($LASTEXITCODE -ne 0) {
    throw "The OVA for the flavor $imageId was not downloaded, or it did not pass its checksum. The lines above say why. To use an OVA you already have, pass it with -FlavorImages @{ '$imageId' = 'path\to\image.ova' }."
  }
  return [string]($out | Select-Object -Last 1)
}

function Get-NicLines {
  param([int] $Index, [string] $Vmnet, [string] $Mac, [bool] $Present = $true)
  $p = "ethernet$Index"
  $type = switch ($Vmnet) { 'vmnet8' { 'nat' } 'vmnet0' { 'bridged' } default { 'custom' } }
  $lines = @("$p.present = `"$($Present.ToString().ToUpper())`"")
  if ($Present) {
    $lines += "$p.virtualDev = `"vmxnet3`""
    $lines += "$p.connectionType = `"$type`""
    if ($type -eq 'custom') { $lines += "$p.vnet = `"$($Vmnet.Replace('vmnet', 'VMnet'))`"" }
    $lines += "$p.addressType = `"static`""
    $lines += "$p.address = `"$Mac`""
    $lines += "$p.startConnected = `"TRUE`""
  }
  return $lines
}

function Edit-Vmx {
  param([string] $Path, [scriptblock] $Drop, [string[]] $Add)
  $kept = Get-Content -Path $Path | Where-Object { -not (& $Drop $_) }
  Set-Content -Path $Path -Value ($kept + $Add) -Encoding ASCII
}

function Get-LabBuildState {
  # What the machine says about its first boot. The guest hands one line to Workstation as the guest
  # variable lab201 (lab201-status --publish runs every minute), and vmrun reads it with no login.
  param([string] $Vmx)
  foreach ($var in 'lab201', 'guestinfo.lab201') {
    $text = ''
    try { $text = (& $vmrun -T ws readVariable $Vmx guestVar $var 2>$null | Out-String).Trim() } catch { $text = '' }
    if ($text -match '^lab201 (\S+) \S+ ?(.*)$') { return @{ State = $Matches[1]; Detail = $Matches[2] } }
  }
  return @{ State = 'unknown'; Detail = '' }
}

if ($Action -eq 'Status') {
  # State of each machine, whether its first boot has finished, and the line that logs in to it over SSH.
  $started = Get-Date
  $deadline = $started.AddMinutes($WaitMinutes)
  $everReported = $false
  while ($true) {
    $running = @(& $vmrun -T ws list)
    $rows = @(); $pending = @(); $failedNames = @(); $notRunning = @()
    foreach ($vmDef in $lab.vms) {
      $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
      $state = if ($running -contains $vmx) { 'running' } elseif (Test-Path $vmx) { 'stopped' } else { 'missing' }
      if ($state -ne 'running') { $notRunning += $vmDef.name }
      $build = ''; $note = ''
      if ($state -eq 'running') {
        $b = Get-LabBuildState $vmx
        $build = $b.State
        if ($build -ne 'unknown') { $everReported = $true }
        if ($build -in 'running', 'unknown') { $pending += $vmDef.name }
        if ($build -eq 'failed') { $failedNames += $vmDef.name }
        $ip = ''
        try { $ip = (& $vmrun -T ws getGuestIPAddress $vmx 2>$null | Out-String).Trim() } catch { $ip = '' }
        $login = if ($ip -match '^\d+\.\d+\.\d+\.\d+$') { "ssh $($lab.admin_user)@$ip" } else { 'address not ready yet' }
        $note = if ($build -eq 'unknown') { "not reported yet   $login" } else { "$($b.Detail)   $login" }
      }
      $rows += '{0,-16} {1,-8} {2,-8} {3}' -f $vmDef.name, $state, $build, $note
    }
    if (-not $Wait -or -not $pending.Count -or (Get-Date) -ge $deadline) { break }
    # If no machine has reported after six minutes, the guest tools are not passing the state on. Stop waiting.
    if (-not $everReported -and ((Get-Date) - $started).TotalMinutes -ge 6) { break }
    Write-Host ('{0:HH:mm:ss} Still building: {1}' -f (Get-Date), ($pending -join ' '))
    Start-Sleep -Seconds 15
  }
  '{0,-16} {1,-8} {2,-8} {3}' -f 'MACHINE', 'STATE', 'BUILD', 'DETAIL'
  $rows
  if (-not ($running | Where-Object { $_ -like (Join-Path $VmRoot '*') })) {
    Write-Host "No lab machine is running in $VmRoot. If the machines are in another folder, pass -VmRoot."
    return
  }
  if ($failedNames.Count) {
    Write-Warning "These machines report a problem (a failed first boot, or a lab service that is not running): $($failedNames -join ', '). Log in to one and run: lab201-status"
    exit 1
  }
  if ($pending.Count -and -not $everReported) {
    Write-Host 'No machine reports its build state yet. A machine reports about a minute after it starts.'
    Write-Host 'To check one by hand, log in to it and run: lab201-status'
    if ($Wait) { exit 1 }
  } elseif ($Wait -and $pending.Count) {
    Write-Warning "Not every machine finished within $WaitMinutes minutes: $($pending -join ', ')"
    exit 1
  } elseif ($Wait -and $notRunning.Count) {
    # Say what the table shows and no more: a machine that is stopped or missing was not checked.
    Write-Host 'Every running machine has finished its first boot.' -ForegroundColor Green
    Write-Host "Not checked, because they are stopped or missing: $($notRunning -join ', ')"
  } elseif ($Wait) {
    Write-Host 'Every machine has finished its first boot.' -ForegroundColor Green
  }
  return
}

if ($Action -eq 'Snapshot') {
  # A snapshot keeps the machine's adapters. With the build adapter (adapter 0) still on, a restore would bring
  # it back, and with it the machine's path to the internet. So the build adapters have to go first.
  $withBuildNic = @()
  foreach ($vmDef in $lab.vms) {
    # The first adapter of the uplink machine is its uplink to the external firewall, and it stays.
    if ($vmDef.name -eq $uplinkVm) { continue }
    $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
    if ((Test-Path $vmx) -and (Select-String -Path $vmx -Pattern '^\s*ethernet0\.present\s*=\s*"TRUE"' -Quiet)) { $withBuildNic += $vmDef.name }
  }
  if ($withBuildNic.Count) {
    throw "These machines still have their build adapter: $($withBuildNic -join ', '). A snapshot keeps that adapter, and a restore would bring it back with its path to the internet. Run -Action RemoveBuildNics first. No snapshot was taken."
  }
  foreach ($vmDef in $lab.vms) {
    $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
    if (-not (Test-Path $vmx)) { continue }
    $have = @(& $vmrun -T ws listSnapshots $vmx 2>$null)
    if ($have -contains $SnapshotName) { Write-Host "$($vmDef.name) has the snapshot $SnapshotName. Skipped."; continue }
    if (-not $PSCmdlet.ShouldProcess($vmDef.name, "Take the snapshot $SnapshotName")) { continue }
    Write-Host "Taking the snapshot $SnapshotName of $($vmDef.name)"
    & $vmrun -T ws snapshot $vmx $SnapshotName
    if ($LASTEXITCODE -ne 0) { throw "vmrun snapshot failed for $($vmDef.name)." }
  }
  return
}

if ($Action -eq 'Restore') {
  # The gateway first, then the rest.
  $gwFirst = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
  $restoreOrder = @($gwFirst) + @($lab.vms.name | Where-Object { $_ -ne $gwFirst })
  $noSnapshot = @()
  foreach ($name in $restoreOrder) {
    if (-not $name) { continue }
    $vmx = Join-Path $VmRoot "$name\$name.vmx"
    if (-not (Test-Path $vmx)) { continue }
    $have = @(& $vmrun -T ws listSnapshots $vmx 2>$null)
    if ($have -notcontains $SnapshotName) { Write-Warning "$name has no snapshot $SnapshotName. It is left as it is."; $noSnapshot += $name; continue }
    if (-not $PSCmdlet.ShouldProcess($name, "Return to the snapshot $SnapshotName and start")) { continue }
    Write-Host "Returning $name to the snapshot $SnapshotName"
    & $vmrun -T ws revertToSnapshot $vmx $SnapshotName
    if ($LASTEXITCODE -ne 0) { throw "vmrun revertToSnapshot failed for $name." }
    # vmrun leaves a machine suspended when the snapshot was taken while it ran, so start it.
    & $vmrun -T ws start $vmx nogui
  }
  if ($noSnapshot.Count) { throw "No snapshot $SnapshotName on: $($noSnapshot -join ', '). Take it first with -Action Snapshot." }
  return
}

if ($Action -eq 'Remove') {
  foreach ($vmDef in $lab.vms) {
    $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
    if ((Test-Path $vmx) -and $PSCmdlet.ShouldProcess($vmDef.name, 'Stop and delete the virtual machine')) {
      & $vmrun -T ws stop $vmx hard 2>$null
      & $vmrun -T ws deleteVM $vmx
    }
  }
  return
}

if ($Action -eq 'RemoveBuildNics') {
  foreach ($vmDef in $lab.vms) {
    if ($vmDef.name -eq $uplinkVm) { Write-Host "$($vmDef.name) keeps its first adapter: it is the uplink to the external firewall."; continue }
    $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
    if (-not (Test-Path $vmx)) { continue }
    if (-not $PSCmdlet.ShouldProcess($vmDef.name, 'Switch the build network adapter off')) { continue }
    & $vmrun -T ws stop $vmx soft 2>$null
    Edit-Vmx -Path $vmx -Drop { param($l) $l -match '^ethernet0\.' } -Add (Get-NicLines -Index 0 -Vmnet $WanVmnet -Mac '' -Present $false)
    & $vmrun -T ws start $vmx nogui
  }
  return
}

# ---- Deploy ----
if (-not $SshKeyFile) { throw '-SshKeyFile is required for -Action Deploy.' }
New-Item -ItemType Directory -Force -Path $WorkDir, $VmRoot | Out-Null

foreach ($vmDef in $lab.vms) {
  if ((Get-FlavorRecord (Get-FlavorId $vmDef $lab)).iso) {
    throw "$($vmDef.name) uses an ISO-based flavor (Windows, Linux Mint, or Tiny Core). Workstation has no VLAN-aware switch, and these guests cannot tag VLANs for the trunks. Use the Proxmox, ESXi, or vCenter script for them."
  }
}

# One base machine for each image flavor in use (Ubuntu publishes OVAs; pass others with -FlavorImages).
$baseOf = @{}
foreach ($vmDef in $lab.vms) {
  $fid = Get-FlavorId $vmDef $lab
  $imageId = Get-ImageFlavorId $fid
  if ($baseOf.ContainsKey($imageId)) { continue }
  $ova = Resolve-FlavorOva -Id $fid -WorkDir $WorkDir -Supplied $FlavorImages
  $baseVmx = Join-Path $VmRoot "lab201-base-$imageId\lab201-base-$imageId.vmx"
  if (-not (Test-Path $baseVmx) -and $PSCmdlet.ShouldProcess("lab201-base-$imageId", 'Import the cloud image with ovftool')) {
    & $ovftool --acceptAllEulas --allowExtraConfig "--name=lab201-base-$imageId" $ova $VmRoot
    if ($LASTEXITCODE -ne 0) { throw 'ovftool failed.' }
  }
  $baseOf[$imageId] = $baseVmx
}

$licenseArgs = @(); if ($LicenseFile) { $licenseArgs = '--license-file', (Resolve-Path $LicenseFile).Path }
$keys = @(); foreach ($k in $SshKeyFile) { $keys += '--ssh-key'; $keys += (Resolve-Path $k).Path }
$seedDir = Join-Path $WorkDir 'seeds'
& $pyExe @pyArgs (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --iso --guest-agent vmware --tagging guest @keys @licenseArgs
if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }


foreach ($vmDef in $lab.vms) {
  $name = $vmDef.name
  $dir = Join-Path $VmRoot $name
  $vmx = Join-Path $dir "$name.vmx"
  if (Test-Path $vmx) { Write-Host "$name exists. Skipped."; continue }
  if (-not $PSCmdlet.ShouldProcess($name, 'Clone and configure the virtual machine')) { continue }
  Write-Host "Creating $name"
  & $vmrun -T ws clone $baseOf[(Get-ImageFlavorId (Get-FlavorId $vmDef $lab))] $vmx full "-cloneName=$name"
  if ($LASTEXITCODE -ne 0) { throw "vmrun clone failed for $name." }

  $add = @("displayName = `"$name`"", "memsize = `"$($vmDef.memory_mb)`"", "numvcpus = `"$($vmDef.vcpu)`"", $(if ((Get-FlavorRecord (Get-FlavorId $vmDef $lab)).guest_id -eq 'ubuntu64Guest') { 'guestOS = "ubuntu-64"' } else { 'guestOS = "other5xlinux-64"' }))
  for ($n = 0; $n -lt $vmDef.nics.Count; $n++) {
    $mac = '{0}:{1:x2}:{2:x2}' -f $lab.mac_prefix, $names[$name], $n
    $add += Get-NicLines -Index $n -Vmnet $vmnetOf[$vmDef.nics[$n].net] -Mac $mac
  }
  $iso = (Resolve-Path (Join-Path $seedDir "$name-seed.iso")).Path
  $add += 'ide1:0.present = "TRUE"', 'ide1:0.deviceType = "cdrom-image"', "ide1:0.fileName = `"$iso`"", 'ide1:0.startConnected = "TRUE"'
  Edit-Vmx -Path $vmx -Add $add -Drop { param($l) $l -match '^(ethernet\d+\.|ide1:0\.|powerType\.|displayName|memsize|numvcpus|guestOS)\b' }

  $disk = (Get-Content $vmx | Where-Object { $_ -match '^scsi0:0\.fileName' } | Select-Object -First 1) -replace '^[^"]*"([^"]+)".*$', '$1'
  & $vdisk -x "$($vmDef.disk_gb)GB" (Join-Path $dir $disk) | Out-Null
  # A disk cannot shrink, so the tool refuses when the image is already larger than the manifest's size.
  if ($LASTEXITCODE -ne 0) { Write-Host "  ${name}: the disk was not resized to $($vmDef.disk_gb) GB. That is expected when its image is already larger, and the disk then keeps the size of the image." }
}

$gwName = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
$order = @($gwName) + ($lab.vms.name | Where-Object { $_ -ne $gwName })
foreach ($name in $order) {
  $vmx = Join-Path $VmRoot "$name\$name.vmx"
  if ((Test-Path $vmx) -and $PSCmdlet.ShouldProcess($name, 'Start')) { & $vmrun -T ws start $vmx nogui }
}

# vmrun does not add machines to the Workstation library.
if ($AddToLibrary -and $PSCmdlet.ShouldProcess('the lab machines', 'Open in Workstation, which lists them in the Library')) {
  $ui = Join-Path $WorkstationDir 'vmware.exe'
  foreach ($name in $order) {
    $vmx = Join-Path $VmRoot "$name\$name.vmx"
    if (Test-Path $vmx) { Start-Process -FilePath $ui -ArgumentList "`"$vmx`"" }
  }
  Write-Host 'Opened each machine in Workstation. If one is missing from the Library, right-click My Computer there and choose Scan for Virtual Machines.'
} else {
  Write-Host "To list the machines in the Workstation Library, right-click My Computer there, choose Scan for Virtual Machines, and pick $VmRoot. Or run the deploy with -AddToLibrary."
}
Write-Host 'To see when every machine has finished its first boot, and how to log in to each, run this script with -Action Status -Wait.'
