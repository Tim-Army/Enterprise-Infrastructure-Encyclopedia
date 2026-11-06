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
    -T1Vmnet   bridged to the NIC that cables to sw-648f-1 (trunk T1)
    -T2Vmnet   bridged to the NIC that cables to sw-2048f-1 (trunk T2)
    -OobVmnet  bridged to the NIC that cables to the switch management ports
    -Lan220Vmnet  host-only, with the DHCP service turned off
  -WanVmnet is the network the build NICs use (vmnet8, the NAT network, by default).

  Needs PowerShell 5.1 or 7, Workstation Pro 17 or later, and Python 3 with
  pycdlib (pip install pycdlib) for the seed ISOs.

.EXAMPLE
  .\Deploy-Lab201-Workstation.ps1 -VmRoot D:\VMs\lab201 -SshKeyFile ~\.ssh\id_ed25519.pub -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [string] $VmRoot = 'D:\VMs\lab201',
  [ValidateSet('Deploy', 'Status', 'RemoveBuildNics', 'Remove')] [string] $Action = 'Deploy',
  [string[]] $SshKeyFile,
  [string] $Manifest = (Join-Path $PSScriptRoot '..\common\lab201-vms.json'),
  [string] $WorkDir = (Join-Path $PSScriptRoot 'work'),
  [string] $WorkstationDir = 'C:\Program Files (x86)\VMware\VMware Workstation',
  [ValidatePattern('^vmnet\d+$')] [string] $T1Vmnet = 'vmnet2',
  [ValidatePattern('^vmnet\d+$')] [string] $T2Vmnet = 'vmnet3',
  [ValidatePattern('^vmnet\d+$')] [string] $OobVmnet = 'vmnet4',
  [ValidatePattern('^vmnet\d+$')] [string] $Lan220Vmnet = 'vmnet5',
  [ValidatePattern('^vmnet\d+$')] [string] $WanVmnet = 'vmnet8',
  [string] $OvfToolPath
)

$ErrorActionPreference = 'Stop'

function Get-WebText {
  # Invoke-WebRequest returns a byte array for some text files (for example SHA256SUMS), so decode it.
  param([string] $Uri)
  $r = Invoke-WebRequest -Uri $Uri
  if ($r.Content -is [byte[]]) { return [System.Text.Encoding]::UTF8.GetString($r.Content) }
  return [string]$r.Content
}

$vmrun = Join-Path $WorkstationDir 'vmrun.exe'
$ovftool = if ($OvfToolPath) { $OvfToolPath } elseif (Test-Path (Join-Path $WorkstationDir 'OVFTool\ovftool.exe')) { Join-Path $WorkstationDir 'OVFTool\ovftool.exe' } else { (Get-Command ovftool.exe -ErrorAction SilentlyContinue).Source }
$vdisk = Join-Path $WorkstationDir 'vmware-vdiskmanager.exe'
foreach ($exe in $vmrun, $ovftool, $vdisk) { if (-not $exe -or -not (Test-Path $exe)) { throw "Not found: $exe. Is Workstation Pro installed, is -WorkstationDir right, and is OVF Tool installed (-OvfToolPath)?" } }

$lab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json
$names = @{}; $i = 0
foreach ($vm in $lab.vms) { $i++; $names[$vm.name] = $i }
$vmnetOf = @{ 'lab201-t1' = $T1Vmnet; 'lab201-t2' = $T2Vmnet; 'lab201-oob' = $OobVmnet; 'lab201-lan220' = $Lan220Vmnet; 'lab201-wan' = $WanVmnet }

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

if ($Action -eq 'Status') {
  foreach ($vmDef in $lab.vms) {
    $vmx = Join-Path $VmRoot "$($vmDef.name)\$($vmDef.name).vmx"
    $state = if ((& $vmrun -T ws list) -contains $vmx) { 'running' } elseif (Test-Path $vmx) { 'stopped' } else { 'missing' }
    '{0,-16} {1}' -f $vmDef.name, $state
  }
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

$ova = Join-Path $WorkDir $lab.image.ova
if (-not (Test-Path $ova)) {
  Invoke-WebRequest -Uri ($lab.image.base_url + $lab.image.ova) -OutFile $ova
  $sums = (Get-WebText ($lab.image.base_url + 'SHA256SUMS')) -split "`n"
  $want = ($sums | Where-Object { $_ -match [regex]::Escape($lab.image.ova) } | Select-Object -First 1) -replace '\s.*', ''
  $got = (Get-FileHash -Algorithm SHA256 -Path $ova).Hash.ToLower()
  if ($want -ne $got) { Remove-Item $ova; throw "SHA-256 mismatch for $($lab.image.ova): expected $want, got $got" }
}

$keys = @(); foreach ($k in $SshKeyFile) { $keys += '--ssh-key'; $keys += (Resolve-Path $k).Path }
$seedDir = Join-Path $WorkDir 'seeds'
& python (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --iso --guest-agent vmware --tagging guest @keys
if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }

$baseVmx = Join-Path $VmRoot 'lab201-base\lab201-base.vmx'
if (-not (Test-Path $baseVmx) -and $PSCmdlet.ShouldProcess('lab201-base', 'Import the cloud image with ovftool')) {
  & $ovftool --acceptAllEulas --allowExtraConfig '--name=lab201-base' $ova $VmRoot
  if ($LASTEXITCODE -ne 0) { throw 'ovftool failed.' }
}

foreach ($vmDef in $lab.vms) {
  $name = $vmDef.name
  $dir = Join-Path $VmRoot $name
  $vmx = Join-Path $dir "$name.vmx"
  if (Test-Path $vmx) { Write-Host "$name exists. Skipped."; continue }
  if (-not $PSCmdlet.ShouldProcess($name, 'Clone and configure the virtual machine')) { continue }
  Write-Host "Creating $name"
  & $vmrun -T ws clone $baseVmx $vmx full "-cloneName=$name"
  if ($LASTEXITCODE -ne 0) { throw "vmrun clone failed for $name." }

  $add = @("displayName = `"$name`"", "memsize = `"$($vmDef.memory_mb)`"", "numvcpus = `"$($vmDef.vcpu)`"", 'guestOS = "ubuntu-64"')
  for ($n = 0; $n -lt $vmDef.nics.Count; $n++) {
    $mac = '{0}:{1:x2}:{2:x2}' -f $lab.mac_prefix, $names[$name], $n
    $add += Get-NicLines -Index $n -Vmnet $vmnetOf[$vmDef.nics[$n].net] -Mac $mac
  }
  $iso = (Resolve-Path (Join-Path $seedDir "$name-seed.iso")).Path
  $add += 'ide1:0.present = "TRUE"', 'ide1:0.deviceType = "cdrom-image"', "ide1:0.fileName = `"$iso`"", 'ide1:0.startConnected = "TRUE"'
  Edit-Vmx -Path $vmx -Add $add -Drop { param($l) $l -match '^(ethernet\d+\.|ide1:0\.|displayName|memsize|numvcpus|guestOS)\b' }

  $disk = (Get-Content $vmx | Where-Object { $_ -match '^scsi0:0\.fileName' } | Select-Object -First 1) -replace '^[^"]*"([^"]+)".*$', '$1'
  & $vdisk -x "$($vmDef.disk_gb)GB" (Join-Path $dir $disk) | Out-Null
}

$gwName = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
$order = @($gwName) + ($lab.vms.name | Where-Object { $_ -ne $gwName })
foreach ($name in $order) {
  $vmx = Join-Path $VmRoot "$name\$name.vmx"
  if ((Test-Path $vmx) -and $PSCmdlet.ShouldProcess($name, 'Start')) { & $vmrun -T ws start $vmx nogui }
}
