<#
.SYNOPSIS
  Creates the Volume CCI lab virtual machines through VMware vCenter Server 7 or 8.

.DESCRIPTION
  Reads ..\common\lab201-vms.json, builds the lab networks on one ESXi host that
  vCenter manages (standard switches, or a distributed switch), imports the
  Ubuntu cloud image OVA once as a template, clones each virtual machine from
  it, sets its hardware, network adapters, and cloud-init seed ISO, and powers
  it on.

  Needs PowerShell 5.1 or 7, PowerCLI (Install-Module VMware.PowerCLI; use the release that supports your vSphere version, 13.3 for 7 and 8, and Broadcom's newer VCF PowerCLI for 9),
  and Python 3 with pycdlib (pip install pycdlib) for the seed ISOs.

  For a managed cluster such as Dell VxRail, use -ClusterName, -UseExistingSwitch with the
  name of the existing distributed switch, and -NoUplinkChanges. The script then adds only
  port groups, and changes no switch, uplink, or physical NIC. Build the lab with one trunk
  (the Lab Builder does this for you), because the VxRail switch has one set of uplinks.

.EXAMPLE
  .\Deploy-Lab201-Vcenter.ps1 -VcenterServer vc01.example.net -Datacenter DC1 `
    -VMHostName esxi01.example.net -Datastore datastore1 -VsphereVersion 8 `
    -NetworkType Distributed -SshKeyFile ~\.ssh\id_ed25519.pub `
    -Trunk1Nic vmnic1 -Trunk2Nic vmnic2 -OobNic vmnic3 -WanNic vmnic0 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [Parameter(Mandatory)] [string] $VcenterServer,
  [PSCredential] $Credential,
  [string] $Datacenter,
  [string] $VMHostName,
  [string] $ClusterName,
  [string] $UseExistingSwitch,
  [switch] $NoUplinkChanges,
  [string] $Datastore,
  [string] $FolderName = 'lab201',
  [ValidateSet(7, 8, 9)] [int] $VsphereVersion = 8,
  [ValidateSet('Standard', 'Distributed')] [string] $NetworkType = 'Standard',
  [ValidateSet('Deploy', 'Status', 'RemoveBuildNics', 'Remove')] [string] $Action = 'Deploy',
  [string[]] $SshKeyFile,
  [string] $Manifest = (Join-Path $PSScriptRoot '..\common\lab201-vms.json'),
  [string] $WorkDir = (Join-Path $PSScriptRoot 'work'),
  [string] $Trunk1Nic, [string] $Trunk2Nic, [string] $OobNic, [string] $WanNic,
  [string] $HardwareVersion,
  [string] $VdsVersion,
  [string] $LicenseFile,
  [hashtable] $FlavorImages = @{},
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

function Get-DefaultHardwareVersion {
  # vSphere 7.0 U2 and later: vmx-19. vSphere 8.0 and 8.0 U1: vmx-20. vSphere 8.0 U2 and U3: vmx-21. vSphere 9.0: vmx-22.
  param([version] $HostVersion, [int] $Major)
  if ($Major -eq 9) { return 'vmx-22' }
  if ($Major -eq 7) { if ($HostVersion -ge [version]'7.0.2') { return 'vmx-19' } else { return 'vmx-17' } }
  if ($HostVersion -ge [version]'8.0.2') { return 'vmx-21' } else { return 'vmx-20' }
}

if (-not (Get-Module -ListAvailable -Name VMware.VimAutomation.Core)) {
  throw 'VMware PowerCLI is not installed. Run: Install-Module VMware.PowerCLI -Scope CurrentUser'
}
Import-Module VMware.VimAutomation.Core -ErrorAction Stop | Out-Null
if ($UseExistingSwitch) { $NetworkType = 'Distributed' }
if ($NetworkType -eq 'Distributed') { Import-Module VMware.VimAutomation.Vds -ErrorAction Stop | Out-Null }
if ($SkipCertificateCheck) {
  Set-PowerCLIConfiguration -Scope Session -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
}
Set-PowerCLIConfiguration -Scope Session -ParticipateInCeip $false -Confirm:$false | Out-Null

$lab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json
if (-not $Credential) { $Credential = Get-Credential -Message "Account on $VcenterServer" }
$server = Connect-VIServer -Server $VcenterServer -Credential $Credential

try {
  if ($server.Version -notlike "$VsphereVersion.*") {
    throw "vCenter reports version $($server.Version), but -VsphereVersion is $VsphereVersion."
  }
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
    Get-VM -Server $server -Location (Get-Folder -Name $FolderName -Type VM -ErrorAction SilentlyContinue) -ErrorAction SilentlyContinue |
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
  foreach ($need in 'Datacenter', 'Datastore') {
    if (-not (Get-Variable $need -ValueOnly)) { throw "-$need is required for -Action Deploy." }
  }
  if (-not $VMHostName -and -not $ClusterName) { throw '-VMHostName or -ClusterName is required for -Action Deploy.' }
  if ($UseExistingSwitch -and -not $NoUplinkChanges) { throw '-UseExistingSwitch changes no uplinks. Add -NoUplinkChanges to confirm that you want that.' }
  if (-not $SshKeyFile) { throw '-SshKeyFile is required for -Action Deploy.' }
  $dc = Get-Datacenter -Server $server -Name $Datacenter
  $cluster = $null
  if ($ClusterName) {
    # A cluster (for example VxRail): the machines can run on any host. Templates are imported through the first connected host.
    $cluster = Get-Cluster -Server $server -Name $ClusterName -Location $dc
    $vmhost = Get-VMHost -Server $server -Location $cluster | Where-Object { $_.ConnectionState -eq 'Connected' } | Select-Object -First 1
    $placement = @{ ResourcePool = $cluster }
  }
  else {
    $vmhost = Get-VMHost -Server $server -Name $VMHostName -Location $dc
    $placement = @{ VMHost = $vmhost }
  }
  $ds = Get-Datastore -Server $server -Name $Datastore -Location $dc
  if (-not $HardwareVersion) { $HardwareVersion = Get-DefaultHardwareVersion -HostVersion ([version]$vmhost.Version) -Major $VsphereVersion }
  if (-not $VdsVersion) { $VdsVersion = switch ($VsphereVersion) { 7 { '7.0.3' } 8 { '8.0.0' } default { '9.0.0' } } }
  Write-Host "vCenter $($server.Version), host $($vmhost.Name) ESXi $($vmhost.Version), virtual hardware $HardwareVersion"
  New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

  $folder = Get-Folder -Server $server -Name $FolderName -Type VM -Location $dc -ErrorAction SilentlyContinue
  if (-not $folder -and $PSCmdlet.ShouldProcess($FolderName, 'Create the virtual machine folder')) {
    $folder = New-Folder -Name $FolderName -Location (Get-Folder -Name vm -Type VM -Location $dc | Select-Object -First 1)
  }

  # Networks
  $uplink = @{ 'lab201-t1' = $Trunk1Nic; 'lab201-t2' = $Trunk2Nic; 'lab201-oob' = $OobNic; 'lab201-wan' = $WanNic }
  $portGroups = @{}
  foreach ($vmDef in $lab.vms) { foreach ($nic in $vmDef.nics) { $portGroups[(& $pgOf $nic)] = $nic } }
  if ($UseExistingSwitch) {
    # Reuse an existing distributed switch (for example the VxRail switch). No switch, uplink, or physical NIC changes.
    # Only port groups are added. The switch's uplinks must already reach the hardware switches.
    $vds = Get-VDSwitch -Server $server -Name $UseExistingSwitch
    foreach ($pg in @($portGroups.Keys)) {
      if (Get-VDPortgroup -VDSwitch $vds -Name $pg -ErrorAction SilentlyContinue) { continue }
      if (-not $PSCmdlet.ShouldProcess($pg, "Create the distributed port group on $UseExistingSwitch")) { continue }
      if ($portGroups[$pg].trunk) { $new = New-VDPortgroup -VDSwitch $vds -Name $pg -VlanTrunkRange '0-4094' }
      elseif ($portGroups[$pg].vlan) { $new = New-VDPortgroup -VDSwitch $vds -Name $pg -VlanId ([int]$portGroups[$pg].vlan) }
      else { $new = New-VDPortgroup -VDSwitch $vds -Name $pg }
      if ($portGroups[$pg].trunk) {
        Get-VDSecurityPolicy -VDPortgroup $new | Set-VDSecurityPolicy -AllowPromiscuous $true -ForgedTransmits $true -MacChanges $true | Out-Null
      }
    }
  }
  else {
  foreach ($net in $lab.networks) {
    $swName = if ($NetworkType -eq 'Standard') { "vSwitch-$($net.name)" } else { "dvs-$($net.name)" }
    if ($NetworkType -eq 'Standard') {
      $vs = Get-VirtualSwitch -VMHost $vmhost -Standard -Name $swName -ErrorAction SilentlyContinue
      if (-not $vs -and $PSCmdlet.ShouldProcess($swName, 'Create the standard switch')) {
        $vsArgs = @{ VMHost = $vmhost; Name = $swName; Mtu = 1500 }
        if ($uplink[$net.name]) { $vsArgs.Nic = $uplink[$net.name] } else { Write-Warning "$($net.name) has no uplink. It is internal to the host." }
        $vs = New-VirtualSwitch @vsArgs
      }
      if ($vs -and $net.kind -eq 'trunk') {
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
    else {
      $vds = Get-VDSwitch -Server $server -Name $swName -ErrorAction SilentlyContinue
      if (-not $vds -and $PSCmdlet.ShouldProcess($swName, "Create the distributed switch (version $VdsVersion)")) {
        $vds = New-VDSwitch -Server $server -Name $swName -Location $dc -Version $VdsVersion -NumUplinkPorts 1 -Mtu 1500
        Add-VDSwitchVMHost -VDSwitch $vds -VMHost $vmhost
        if ($uplink[$net.name]) {
          $pnic = Get-VMHostNetworkAdapter -VMHost $vmhost -Physical -Name $uplink[$net.name]
          Add-VDSwitchPhysicalNetworkAdapter -DistributedSwitch $vds -VMHostPhysicalNic $pnic -Confirm:$false
        }
        else { Write-Warning "$($net.name) has no uplink. It is internal to the host." }
      }
      foreach ($pg in @($portGroups.Keys | Where-Object { $portGroups[$_].net -eq $net.name })) {
        if (Get-VDPortgroup -VDSwitch $vds -Name $pg -ErrorAction SilentlyContinue) { continue }
        if (-not ($vds -and $PSCmdlet.ShouldProcess($pg, 'Create the distributed port group'))) { continue }
        if ($portGroups[$pg].trunk) { $new = New-VDPortgroup -VDSwitch $vds -Name $pg -VlanTrunkRange '0-4094' }
        elseif ($portGroups[$pg].vlan) { $new = New-VDPortgroup -VDSwitch $vds -Name $pg -VlanId ([int]$portGroups[$pg].vlan) }
        else { $new = New-VDPortgroup -VDSwitch $vds -Name $pg }
        if ($net.kind -eq 'trunk') {
          Get-VDSecurityPolicy -VDPortgroup $new | Set-VDSecurityPolicy -AllowPromiscuous $true -ForgedTransmits $true -MacChanges $true | Out-Null
        }
      }
    }
  }
  }

  # Images and templates: one template for each image flavor in use (hardened flavors share their base's template).
  Set-LabVsphereLicense -Server $server -VmHost $vmhost -Path $LicenseFile -IsVcenter $true
  $templateOf = @{}
  foreach ($vmDef in $lab.vms) {
    $fid = Get-FlavorId $vmDef $lab
    $imageId = Get-ImageFlavorId $fid
    if ($templateOf.ContainsKey($imageId)) { continue }
    $tplName = "lab201-$imageId-template"
    $tpl = Get-Template -Server $server -Name $tplName -ErrorAction SilentlyContinue
    if (-not $tpl -and $PSCmdlet.ShouldProcess($tplName, 'Import the cloud image as a template')) {
      $ova = Resolve-FlavorOva -Id $fid -WorkDir $WorkDir -Supplied $FlavorImages
      $base = Import-VApp -Source $ova -VMHost $vmhost -Datastore $ds -Location $folder -Name $tplName -DiskStorageFormat Thin -Force
      Set-VM -VM $base -GuestId (Get-FlavorRecord $imageId).guest_id -HardwareVersion $HardwareVersion -Confirm:$false | Out-Null
      $tpl = Set-VM -VM $base -ToTemplate -Confirm:$false
    }
    $templateOf[$imageId] = $tpl
  }

  # Seeds
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
    if (-not $PSCmdlet.ShouldProcess($name, 'Clone from the template and configure')) { continue }
    Write-Host "Creating $name"
    $vm = New-VM -Name $name -Template $templateOf[(Get-ImageFlavorId (Get-FlavorId $vmDef $lab))] @placement -Datastore $ds -Location $folder -DiskStorageFormat Thin
    Set-VM -VM $vm -NumCpu $vmDef.vcpu -MemoryMB $vmDef.memory_mb -Confirm:$false | Out-Null
    Get-HardDisk -VM $vm | Select-Object -First 1 | Set-HardDisk -CapacityGB $vmDef.disk_gb -Confirm:$false | Out-Null
    Get-NetworkAdapter -VM $vm | Remove-NetworkAdapter -Confirm:$false
    for ($n = 0; $n -lt $vmDef.nics.Count; $n++) {
      $pg = & $pgOf $vmDef.nics[$n]
      $mac = & $macOf $name $n
      if ($NetworkType -eq 'Standard') {
        New-NetworkAdapter -VM $vm -NetworkName $pg -Type Vmxnet3 -MacAddress $mac -StartConnected | Out-Null
      }
      else {
        $vdpg = Get-VDPortgroup -Server $server -Name $pg
        New-NetworkAdapter -VM $vm -Portgroup $vdpg -Type Vmxnet3 -MacAddress $mac -StartConnected | Out-Null
      }
    }
    Copy-DatastoreItem -Item (Join-Path $seedDir "$name-seed.iso") -Destination 'lab201ds:\lab201-seeds\' -Force
    Get-CDDrive -VM $vm | Remove-CDDrive -Confirm:$false
    New-CDDrive -VM $vm -IsoPath "[$($ds.Name)] lab201-seeds/$name-seed.iso" -StartConnected | Out-Null
  }
  Remove-PSDrive -Name lab201ds -ErrorAction SilentlyContinue

  $gwName = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
  $order = @($gwName) + ($lab.vms.name | Where-Object { $_ -ne $gwName })
  foreach ($name in $order) {
    $vm = Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue
    if ($vm -and $vm.PowerState -ne 'PoweredOn' -and $PSCmdlet.ShouldProcess($name, 'Power on')) { Start-VM -VM $vm | Out-Null }
  }
}
finally {
  Disconnect-VIServer -Server $server -Confirm:$false -ErrorAction SilentlyContinue
}
