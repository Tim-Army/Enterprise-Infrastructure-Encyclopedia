<#
.SYNOPSIS
  Creates the Volume CCI lab virtual machines on a standalone VMware ESXi 7 or 8 host.

.DESCRIPTION
  Reads ..\common\lab201-vms.json, builds the virtual switches and port groups,
  imports the Ubuntu cloud image OVA once for each virtual machine, sets its
  hardware, network adapters, and cloud-init seed ISO, and powers it on.

  Needs PowerShell 5.1 or 7, PowerCLI (Install-Module VMware.PowerCLI; use the release that supports your vSphere version, 13.3 for 7 and 8, and Broadcom's newer VCF PowerCLI for 9),
  and Python 3 with pycdlib (pip install pycdlib) for the seed ISOs. The host
  needs a license that allows the API to write. The free ESXi license makes the
  API read-only, so this script stops with a clear message on that license.
  ESXi 9 is licensed only through vSphere Foundation or Cloud Foundation and has no
  free edition.

.EXAMPLE
  .\Deploy-Lab201-Esxi.ps1 -EsxiHost esxi01.example.net -Datastore datastore1 `
    -VsphereVersion 8 -SshKeyFile ~\.ssh\id_ed25519.pub `
    -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0 -WhatIf

.EXAMPLE
  .\Deploy-Lab201-Esxi.ps1 -Action RemoveBuildNics -EsxiHost esxi01.example.net
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [Parameter(Mandatory)] [string] $EsxiHost,
  [PSCredential] $Credential,
  [string] $Datastore,
  [ValidateSet(7, 8, 9)] [int] $VsphereVersion = 8,
  [ValidateSet('Deploy', 'Status', 'RemoveBuildNics', 'Remove')] [string] $Action = 'Deploy',
  [string[]] $SshKeyFile,
  [string] $Manifest = (Join-Path $PSScriptRoot '..\common\lab201-vms.json'),
  [string] $WorkDir = (Join-Path $PSScriptRoot 'work'),
  [string] $Trunk1Nic, [string] $Trunk2Nic, [string] $OobNic, [string] $WanNic,
  [string] $HardwareVersion,
  [string] $LicenseFile,
  [hashtable] $FlavorImages = @{},
  [hashtable] $IsoImages = @{},
  [switch] $SkipCertificateCheck
)

$ErrorActionPreference = 'Stop'

function Get-WebText {
  # Invoke-WebRequest returns a byte array for some text files (for example SHA256SUMS), so decode it.
  param([string] $Uri)
  $r = Invoke-WebRequest -Uri $Uri
  if ($r.Content -is [byte[]]) { return [System.Text.Encoding]::UTF8.GetString($r.Content) }
  return [string]$r.Content
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
  param([string] $Id, [string] $WorkDir, [hashtable] $Supplied)
  $imageId = Get-ImageFlavorId $Id
  foreach ($k in $Id, $imageId) {
    if ($Supplied -and $Supplied.ContainsKey($k)) { return (Resolve-Path $Supplied[$k]).Path }
  }
  $out = & python (Join-Path $PSScriptRoot '..\common\resolve-image.py') --flavor $imageId --ova --out (Join-Path $WorkDir 'images')
  if ($LASTEXITCODE -ne 0) {
    throw "No OVA is available for the flavor $imageId. Make one from its qcow2 image, then pass it with -FlavorImages @{ '$imageId' = 'path\to\image.ova' }."
  }
  return [string]($out | Select-Object -Last 1)
}

function Set-LabVsphereLicense {
  # Applies the vSphere license keys in the license file. The keys are never printed.
  param($Server, $VmHost, [string] $Path, [bool] $IsVcenter)
  if (-not $Path) { return }
  $lic = Get-Content -Raw -Path $Path | ConvertFrom-Json
  if (-not $lic.vsphere) { return }
  $si = Get-View ServiceInstance -Server $Server
  $lm = Get-View $si.Content.LicenseManager -Server $Server
  try {
    if ($IsVcenter) {
      $lam = Get-View $lm.LicenseAssignmentManager -Server $Server
      if ($lic.vsphere.vcenter) {
        $null = $lm.AddLicense([string]$lic.vsphere.vcenter, $null)
        $null = $lam.UpdateAssignedLicense($si.Content.About.InstanceUuid, [string]$lic.vsphere.vcenter, $null)
      }
      if ($lic.vsphere.esxi) {
        $null = $lm.AddLicense([string]$lic.vsphere.esxi, $null)
        $null = $lam.UpdateAssignedLicense($VmHost.ExtensionData.MoRef.Value, [string]$lic.vsphere.esxi, $null)
      }
    }
    elseif ($lic.vsphere.esxi) {
      $null = $lm.UpdateLicense([string]$lic.vsphere.esxi, $null)
    }
  }
  catch { throw 'A vSphere license key was not accepted. Check the key and the license file.' }
}

function Get-IsoPath {
  # Flavors that install from an ISO (Windows, Linux Mint, Tiny Core) need the ISO on a datastore, passed with -IsoImages.
  param([string] $Id, [hashtable] $Supplied)
  if ($Supplied -and $Supplied.ContainsKey($Id)) { return [string]$Supplied[$Id] }
  throw "The flavor $Id installs from an ISO. Upload the ISO to a datastore and pass its path: -IsoImages @{ '$Id' = '[datastore] folder/file.iso' }."
}

function Get-IsoNicType {
  param([string] $Id)
  if ((Get-FlavorRecord $Id).family -eq 'windows') { return 'e1000e' }
  return 'Vmxnet3'
}

function Get-DefaultHardwareVersion {
  # ESXi 7.0 U2 and later: vmx-19. ESXi 8.0 and 8.0 U1: vmx-20. ESXi 8.0 U2 and U3: vmx-21. ESXi 9.0: vmx-22.
  param([version] $HostVersion, [int] $Major)
  if ($Major -eq 9) { return 'vmx-22' }
  if ($Major -eq 7) { if ($HostVersion -ge [version]'7.0.2') { return 'vmx-19' } else { return 'vmx-17' } }
  if ($HostVersion -ge [version]'8.0.2') { return 'vmx-21' } else { return 'vmx-20' }
}

if (-not (Get-Module -ListAvailable -Name VMware.VimAutomation.Core)) {
  throw 'VMware PowerCLI is not installed. Run: Install-Module VMware.PowerCLI -Scope CurrentUser'
}
Import-Module VMware.VimAutomation.Core -ErrorAction Stop | Out-Null
if ($SkipCertificateCheck) {
  Set-PowerCLIConfiguration -Scope Session -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
}
Set-PowerCLIConfiguration -Scope Session -ParticipateInCeip $false -Confirm:$false | Out-Null

$lab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json
if (-not $Credential) { $Credential = Get-Credential -Message "Account on $EsxiHost" }
$server = Connect-VIServer -Server $EsxiHost -Credential $Credential

try {
  $vmhost = Get-VMHost -Server $server | Select-Object -First 1
  if ($vmhost.Version -notlike "$VsphereVersion.*") {
    throw "The host runs ESXi $($vmhost.Version), but -VsphereVersion is $VsphereVersion."
  }
  if (-not $HardwareVersion) { $HardwareVersion = Get-DefaultHardwareVersion -HostVersion ([version]$vmhost.Version) -Major $VsphereVersion }
  Write-Host "Host $($vmhost.Name): ESXi $($vmhost.Version), virtual hardware $HardwareVersion"

  $names = @{}
  $i = 0
  foreach ($vm in $lab.vms) { $i++; $names[$vm.name] = $i }
  $macOf = { param($vmName, $nicIndex) '{0}:{1:x2}:{2:x2}' -f $lab.mac_prefix, $names[$vmName], $nicIndex }
  $pgOf = {
    param($nic)
    if ($nic.trunk) { return "$($nic.net)-trunk" }
    if ($nic.vlan) { return "$($nic.net)-v$($nic.vlan)" }
    return $nic.net
  }

  if ($Action -eq 'Status') {
    Get-VM -Server $server -Name $lab.vms.name -ErrorAction SilentlyContinue |
      Select-Object Name, PowerState, NumCpu, MemoryGB, @{n = 'IPs'; e = { $_.Guest.IPAddress -join ' ' } } | Format-Table -AutoSize
    return
  }

  if ($Action -eq 'RemoveBuildNics') {
    foreach ($vmDef in $lab.vms) {
      $vm = Get-VM -Server $server -Name $vmDef.name -ErrorAction SilentlyContinue
      if (-not $vm) { continue }
      $mac = & $macOf $vmDef.name 0
      $nic = Get-NetworkAdapter -VM $vm | Where-Object { $_.MacAddress -ieq $mac }
      if ($nic -and $PSCmdlet.ShouldProcess($vmDef.name, 'Remove the build network adapter')) {
        Remove-NetworkAdapter -NetworkAdapter $nic -Confirm:$false
      }
    }
    return
  }

  if ($Action -eq 'Remove') {
    foreach ($vmDef in $lab.vms) {
      $vm = Get-VM -Server $server -Name $vmDef.name -ErrorAction SilentlyContinue
      if ($vm -and $PSCmdlet.ShouldProcess($vmDef.name, 'Power off and delete from disk')) {
        if ($vm.PowerState -eq 'PoweredOn') { Stop-VM -VM $vm -Confirm:$false | Out-Null }
        Remove-VM -VM $vm -DeletePermanently -Confirm:$false
      }
    }
    return
  }

  # ---- Deploy ----
  if (-not $Datastore) { throw '-Datastore is required for -Action Deploy.' }
  if (-not $SshKeyFile) { throw '-SshKeyFile is required for -Action Deploy.' }
  $ds = Get-Datastore -Server $server -Name $Datastore
  New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

  # Virtual switches, with the physical uplinks you name. A network without an uplink stays internal.
  $uplink = @{ 'lab201-t1' = $Trunk1Nic; 'lab201-t2' = $Trunk2Nic; 'lab201-oob' = $OobNic; 'lab201-wan' = $WanNic }
  $portGroups = @{}
  foreach ($vmDef in $lab.vms) { foreach ($nic in $vmDef.nics) { $portGroups[(& $pgOf $nic)] = $nic } }
  foreach ($net in $lab.networks) {
    $vsName = "vSwitch-$($net.name)"
    $vs = Get-VirtualSwitch -VMHost $vmhost -Standard -Name $vsName -ErrorAction SilentlyContinue
    if (-not $vs -and $PSCmdlet.ShouldProcess($vsName, 'Create the virtual switch')) {
      $vsArgs = @{ VMHost = $vmhost; Name = $vsName; Mtu = 1500 }
      if ($uplink[$net.name]) { $vsArgs.Nic = $uplink[$net.name] } else { Write-Warning "$($net.name) has no uplink. It is internal to the host." }
      $vs = New-VirtualSwitch @vsArgs
    }
    if ($vs -and $net.kind -eq 'trunk') {
      # gw-201 bridges the two trunks, so its port groups must accept promiscuous mode, forged transmits, and MAC changes.
      Get-SecurityPolicy -VirtualSwitch $vs | Set-SecurityPolicy -AllowPromiscuous $true -ForgedTransmits $true -MacChanges $true | Out-Null
    }
    foreach ($pg in @($portGroups.Keys | Where-Object { $portGroups[$_].net -eq $net.name })) {
      if (Get-VirtualPortGroup -VMHost $vmhost -Name $pg -ErrorAction SilentlyContinue) { continue }
      $vlanId = if ($portGroups[$pg].trunk) { 4095 } elseif ($portGroups[$pg].vlan) { [int]$portGroups[$pg].vlan } else { 0 }
      if ($vs -and $PSCmdlet.ShouldProcess($pg, "Create the port group (VLAN $vlanId)")) {
        New-VirtualPortGroup -VirtualSwitch $vs -Name $pg -VLanId $vlanId | Out-Null
      }
    }
  }

  # Images: one OVA for each flavor in use (Ubuntu publishes OVAs; pass others with -FlavorImages).
  $imageOf = @{}
  foreach ($vmDef in $lab.vms) {
    $fid = Get-FlavorId $vmDef $lab
    if ((Get-FlavorRecord $fid).iso) { $null = Get-IsoPath -Id $fid -Supplied $IsoImages; continue }
    if (-not $imageOf.ContainsKey($fid)) { $imageOf[$fid] = Resolve-FlavorOva -Id $fid -WorkDir $WorkDir -Supplied $FlavorImages }
  }
  Set-LabVsphereLicense -Server $server -VmHost $vmhost -Path $LicenseFile -IsVcenter $false

  # Seeds: one ISO per virtual machine, rendered by the shared tool.
  $licenseArgs = @(); if ($LicenseFile) { $licenseArgs = '--license-file', (Resolve-Path $LicenseFile).Path }
  $keys = @(); foreach ($k in $SshKeyFile) { $keys += '--ssh-key'; $keys += (Resolve-Path $k).Path }
  $seedDir = Join-Path $WorkDir 'seeds'
  & python (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --iso --guest-agent vmware --tagging hypervisor @keys @licenseArgs
  if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }

  $psDrive = New-PSDrive -Name lab201ds -PSProvider VimDatastore -Root '\' -Location $ds
  New-Item -Path 'lab201ds:\lab201-seeds' -ItemType Directory -ErrorAction SilentlyContinue | Out-Null

  foreach ($vmDef in $lab.vms) {
    $name = $vmDef.name
    if (Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue) { Write-Host "$name exists. Skipped."; continue }
    if (-not $PSCmdlet.ShouldProcess($name, 'Import the cloud image and configure the virtual machine')) { continue }
    Write-Host "Creating $name"
    $fid = Get-FlavorId $vmDef $lab
    $isIso = [bool](Get-FlavorRecord $fid).iso
    if ($isIso) {
      # An empty machine. The install ISO and the answer or first-login CD are attached below.
      $vm = New-VM -Name $name -VMHost $vmhost -Datastore $ds -NumCpu $vmDef.vcpu -MemoryMB $vmDef.memory_mb -DiskGB $vmDef.disk_gb -DiskStorageFormat Thin -GuestId (Get-FlavorRecord $fid).guest_id -HardwareVersion $HardwareVersion
      $nicType = Get-IsoNicType $fid
    }
    else {
      $vm = Import-VApp -Source $imageOf[$fid] -VMHost $vmhost -Datastore $ds -Name $name -DiskStorageFormat Thin -Force
      Set-VM -VM $vm -NumCpu $vmDef.vcpu -MemoryMB $vmDef.memory_mb -GuestId (Get-FlavorRecord $fid).guest_id -HardwareVersion $HardwareVersion -Confirm:$false | Out-Null
      Get-HardDisk -VM $vm | Select-Object -First 1 | Set-HardDisk -CapacityGB $vmDef.disk_gb -Confirm:$false | Out-Null
      $nicType = 'Vmxnet3'
    }
    Get-NetworkAdapter -VM $vm | Remove-NetworkAdapter -Confirm:$false
    for ($n = 0; $n -lt $vmDef.nics.Count; $n++) {
      New-NetworkAdapter -VM $vm -NetworkName (& $pgOf $vmDef.nics[$n]) -Type $nicType -MacAddress (& $macOf $name $n) -StartConnected | Out-Null
    }
    $iso = Join-Path $seedDir "$name-seed.iso"
    Copy-DatastoreItem -Item $iso -Destination 'lab201ds:\lab201-seeds\' -Force
    Get-CDDrive -VM $vm | Remove-CDDrive -Confirm:$false
    if ($isIso) { New-CDDrive -VM $vm -IsoPath (Get-IsoPath -Id $fid -Supplied $IsoImages) -StartConnected | Out-Null }
    New-CDDrive -VM $vm -IsoPath "[$($ds.Name)] lab201-seeds/$name-seed.iso" -StartConnected | Out-Null
  }
  Remove-PSDrive -Name lab201ds -ErrorAction SilentlyContinue

  # Power on the gateway first, then the rest.
  $gwName = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
  $order = @($gwName) + ($lab.vms.name | Where-Object { $_ -ne $gwName })
  foreach ($name in $order) {
    $vm = Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue
    if ($vm -and $vm.PowerState -ne 'PoweredOn' -and $PSCmdlet.ShouldProcess($name, 'Power on')) { Start-VM -VM $vm | Out-Null }
  }
}
catch {
  if ($_.Exception.Message -match 'license or ESXi version prohibits') {
    throw 'The host license does not allow API writes (the free ESXi license makes the API read-only). Apply an evaluation or paid license, or build the virtual machines in the ESXi host client by hand.'
  }
  throw
}
finally {
  Disconnect-VIServer -Server $server -Confirm:$false -ErrorAction SilentlyContinue
}
