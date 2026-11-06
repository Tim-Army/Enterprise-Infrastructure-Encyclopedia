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
  foreach ($need in 'Datacenter', 'VMHostName', 'Datastore') {
    if (-not (Get-Variable $need -ValueOnly)) { throw "-$need is required for -Action Deploy." }
  }
  if (-not $SshKeyFile) { throw '-SshKeyFile is required for -Action Deploy.' }
  $dc = Get-Datacenter -Server $server -Name $Datacenter
  $vmhost = Get-VMHost -Server $server -Name $VMHostName -Location $dc
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

  # Image and template
  $ova = Join-Path $WorkDir $lab.image.ova
  if (-not (Test-Path $ova)) {
    Invoke-WebRequest -Uri ($lab.image.base_url + $lab.image.ova) -OutFile $ova
    $sums = (Get-WebText ($lab.image.base_url + 'SHA256SUMS')) -split "`n"
    $want = ($sums | Where-Object { $_ -match [regex]::Escape($lab.image.ova) } | Select-Object -First 1) -replace '\s.*', ''
    $got = (Get-FileHash -Algorithm SHA256 -Path $ova).Hash.ToLower()
    if ($want -ne $got) { Remove-Item $ova; throw "SHA-256 mismatch for $($lab.image.ova): expected $want, got $got" }
  }
  $tplName = 'lab201-ubuntu-template'
  $tpl = Get-Template -Server $server -Name $tplName -ErrorAction SilentlyContinue
  if (-not $tpl -and $PSCmdlet.ShouldProcess($tplName, 'Import the cloud image as a template')) {
    $base = Import-VApp -Source $ova -VMHost $vmhost -Datastore $ds -Location $folder -Name $tplName -DiskStorageFormat Thin -Force
    Set-VM -VM $base -GuestId 'ubuntu64Guest' -HardwareVersion $HardwareVersion -Confirm:$false | Out-Null
    $tpl = Set-VM -VM $base -ToTemplate -Confirm:$false
  }

  # Seeds
  $keys = @(); foreach ($k in $SshKeyFile) { $keys += '--ssh-key'; $keys += (Resolve-Path $k).Path }
  $seedDir = Join-Path $WorkDir 'seeds'
  & python (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --iso --guest-agent vmware --tagging hypervisor @keys
  if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }
  $psDrive = New-PSDrive -Name lab201ds -PSProvider VimDatastore -Root '\' -Location $ds
  New-Item -Path 'lab201ds:\lab201-seeds' -ItemType Directory -ErrorAction SilentlyContinue | Out-Null

  foreach ($vmDef in $lab.vms) {
    $name = $vmDef.name
    if (Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue) { Write-Host "$name exists. Skipped."; continue }
    if (-not $PSCmdlet.ShouldProcess($name, 'Clone from the template and configure')) { continue }
    Write-Host "Creating $name"
    $vm = New-VM -Name $name -Template $tpl -VMHost $vmhost -Datastore $ds -Location $folder -DiskStorageFormat Thin
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

  $order = @('gw-201') + ($lab.vms.name | Where-Object { $_ -ne 'gw-201' })
  foreach ($name in $order) {
    $vm = Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue
    if ($vm -and $vm.PowerState -ne 'PoweredOn' -and $PSCmdlet.ShouldProcess($name, 'Power on')) { Start-VM -VM $vm | Out-Null }
  }
}
finally {
  Disconnect-VIServer -Server $server -Confirm:$false -ErrorAction SilentlyContinue
}
