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

  -Action picks what the script does:
    Deploy           builds and starts the machines (the default)
    Check            tests what a deploy needs on this computer and in vCenter, and changes nothing
    Status           shows each machine and whether its first boot has finished.
                     With -Wait it keeps checking until every machine has finished
    RemoveBuildNics  removes the build network adapter of each machine
    Snapshot         takes the baseline snapshot of every machine (Lab 999.6)
    Restore          returns every machine to the baseline snapshot and powers it on
    Remove           powers off and deletes the machines
  Status, RemoveBuildNics, Snapshot, Restore, and Remove look for the machines only in the
  lab folder (-FolderName), so a machine with the same name elsewhere in vCenter is never touched.

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
  [ValidateSet('Deploy', 'Check', 'Status', 'RemoveBuildNics', 'Snapshot', 'Restore', 'Remove')] [string] $Action = 'Deploy',
  [switch] $Wait,
  [ValidateRange(1, 600)] [int] $WaitMinutes = 30,
  [ValidatePattern('^[A-Za-z][A-Za-z0-9_-]{1,39}$')] [string] $SnapshotName = 'baseline-201',
  [string] $PythonCommand,
  [string[]] $SshKeyFile,
  [string] $Manifest,
  [string] $WorkDir,
  [string] $Trunk1Nic, [string] $Trunk2Nic, [string] $OobNic, [string] $WanNic,
  [string] $HardwareVersion,
  [string] $VdsVersion,
  [string] $LicenseFile,
  [hashtable] $FlavorImages = @{},
  [hashtable] $IsoImages = @{},
  [switch] $SkipCertificateCheck
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
  $out = & $pyExe @pyArgs (Join-Path $PSScriptRoot '..\common\resolve-image.py') --flavor $imageId --ova --out (Join-Path $WorkDir 'images')
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
  # vSphere 7.0 U2 and later: vmx-19. vSphere 8.0 and 8.0 U1: vmx-20. vSphere 8.0 U2 and U3: vmx-21. vSphere 9.0: vmx-22.
  param([version] $HostVersion, [int] $Major)
  if ($Major -eq 9) { return 'vmx-22' }
  if ($Major -eq 7) { if ($HostVersion -ge [version]'7.0.2') { return 'vmx-19' } else { return 'vmx-17' } }
  if ($HostVersion -ge [version]'8.0.2') { return 'vmx-21' } else { return 'vmx-20' }
}

function Get-LabBuildState {
  # What the machine says about its first boot. The guest hands one line to the hypervisor as
  # guestinfo.lab201 (lab201-status --publish runs every minute), so no login is needed to read it.
  param($Vm)
  $entry = $Vm.ExtensionData.Config.ExtraConfig | Where-Object { $_.Key -eq 'guestinfo.lab201' } | Select-Object -First 1
  if ($entry -and "$($entry.Value)" -match '^lab201 (\S+) \S+ ?(.*)$') { return @{ State = $Matches[1]; Detail = $Matches[2] } }
  return @{ State = 'unknown'; Detail = '' }
}

function Get-LabVm {
  # A lab machine by name, in the lab folder only. A machine with the same name elsewhere in vCenter is not returned.
  param($Server, [string] $Name, [string] $Folder)
  $labFolder = Get-Folder -Server $Server -Name $Folder -Type VM -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $labFolder) { return $null }
  return (Get-VM -Server $Server -Name $Name -Location $labFolder -ErrorAction SilentlyContinue | Select-Object -First 1)
}

if ($Action -eq 'Check') {
  # Tests what a deploy needs on this computer and in vCenter, and changes nothing.
  $script:failed = 0
  function Show-Check {
    param([string] $State, [string] $What, [string] $Fix)
    $color = switch ($State) { 'OK' { 'Green' } 'WARN' { 'Yellow' } default { 'Red' } }
    if ($State -eq 'FAIL') { $script:failed++ }
    Write-Host ('[{0,-4}] {1}' -f $State, $What) -ForegroundColor $color
    if ($Fix -and $State -ne 'OK') { Write-Host "       $Fix" }
  }
  Write-Host 'Checking this computer and vCenter for the lab build. Nothing is changed.'
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

  $checkLab = $null
  if (Test-Path $Manifest) {
    try { $checkLab = Get-Content -Raw -Path $Manifest | ConvertFrom-Json } catch { Show-Check 'FAIL' "The manifest is not valid JSON: $Manifest" 'Download the zip from the Lab Builder again' }
  } else {
    Show-Check 'FAIL' "The manifest was not found: $Manifest" 'Keep the script and the common folder together, as they are in the zip'
  }
  $needMb = 0; $needGb = 0
  if ($checkLab) {
    Show-Check 'OK' "Manifest: $(@($checkLab.vms).Count) machines"
    $needGb = ($checkLab.vms | Measure-Object -Property disk_gb -Sum).Sum
    $needMb = ($checkLab.vms | Measure-Object -Property memory_mb -Sum).Sum
    if ($UseExistingSwitch -and @($checkLab.vms | ForEach-Object { $_.nics } | Where-Object { $_.net -eq 'lab201-t2' }).Count -gt 0) {
      Show-Check 'WARN' 'The manifest has a second trunk (lab201-t2), and an existing switch has one set of uplinks' 'For VxRail, make the manifest with the Lab Builder for Dell VxRail'
    }
    $seen = @{}
    foreach ($vmDef in $checkLab.vms) {
      $fid = Get-FlavorId $vmDef $checkLab
      if ($seen[$fid]) { continue }
      $seen[$fid] = $true
      $rec = $flavorCatalog.flavors | Where-Object { $_.id -eq $fid } | Select-Object -First 1
      if (-not $rec) { Show-Check 'FAIL' "The manifest names a flavor this script does not know: $fid" 'Download the zip from the Lab Builder again'; continue }
      if ($rec.iso) {
        if ($IsoImages.ContainsKey($fid)) { Show-Check 'OK' "Install ISO for ${fid}: $($IsoImages[$fid]). Compare it with the publisher's checksum before you upload it" }
        else { Show-Check 'FAIL' "$fid installs from an ISO, and -IsoImages has no entry for it" "Upload the ISO to a datastore and pass: -IsoImages @{ '$fid' = '[datastore] folder/file.iso' }" }
        continue
      }
      $imageId = Get-ImageFlavorId $fid
      $supplied = @($fid, $imageId) | Where-Object { $FlavorImages.ContainsKey($_) } | Select-Object -First 1
      if ($supplied) {
        if (Test-Path $FlavorImages[$supplied]) { Show-Check 'OK' "OVA for ${imageId}: $($FlavorImages[$supplied])" }
        else { Show-Check 'FAIL' "The OVA for $imageId was not found: $($FlavorImages[$supplied])" 'Check the path in -FlavorImages' }
      } elseif (-not (($flavorCatalog.flavors | Where-Object { $_.id -eq $imageId } | Select-Object -First 1).image.ova)) {
        Show-Check 'FAIL' "$imageId publishes no OVA, and -FlavorImages has no entry for it" "Make an OVA from its qcow2 image and pass: -FlavorImages @{ '$imageId' = 'path\to\image.ova' }"
      }
    }
  }
  if ($UseExistingSwitch -and -not $NoUplinkChanges) { Show-Check 'FAIL' '-UseExistingSwitch needs -NoUplinkChanges' 'Add -NoUplinkChanges to confirm that the script changes no uplinks' }
  if (-not $VMHostName -and -not $ClusterName) { Show-Check 'FAIL' 'Neither -VMHostName nor -ClusterName was given' 'Pass the host that owns the trunk NICs, or the cluster' }

  if (-not (Get-Module -ListAvailable -Name VMware.VimAutomation.Core)) {
    Show-Check 'FAIL' 'VMware PowerCLI is not installed, so vCenter was not checked' 'Run: Install-Module VMware.PowerCLI -Scope CurrentUser'
  } else {
    Show-Check 'OK' 'VMware PowerCLI is installed'
    try {
      Import-Module VMware.VimAutomation.Core -ErrorAction Stop | Out-Null
      if ($UseExistingSwitch -or $NetworkType -eq 'Distributed') { Import-Module VMware.VimAutomation.Vds -ErrorAction Stop | Out-Null }
      if ($SkipCertificateCheck) { Set-PowerCLIConfiguration -Scope Session -InvalidCertificateAction Ignore -Confirm:$false | Out-Null }
      Set-PowerCLIConfiguration -Scope Session -ParticipateInCeip $false -Confirm:$false | Out-Null
      if (-not $Credential) { $Credential = Get-Credential -Message "Account on $VcenterServer" }
      $checkServer = Connect-VIServer -Server $VcenterServer -Credential $Credential -ErrorAction Stop
      try {
        if ($checkServer.Version -like "$VsphereVersion.*") { Show-Check 'OK' "vCenter $VcenterServer reports version $($checkServer.Version)" }
        else { Show-Check 'FAIL' "vCenter reports version $($checkServer.Version), but -VsphereVersion is $VsphereVersion" 'Pass the major version vCenter runs' }
        $checkDc = $null
        if (-not $Datacenter) { Show-Check 'FAIL' 'No datacenter was given (-Datacenter)' 'Pass the name of the datacenter' }
        else {
          $checkDc = Get-Datacenter -Server $checkServer -Name $Datacenter -ErrorAction SilentlyContinue | Select-Object -First 1
          if ($checkDc) { Show-Check 'OK' "Datacenter $Datacenter" } else { Show-Check 'FAIL' "Datacenter $Datacenter was not found" 'Check the name with: Get-Datacenter' }
        }
        $checkHost = $null
        if ($checkDc -and $ClusterName) {
          $checkCluster = Get-Cluster -Server $checkServer -Name $ClusterName -Location $checkDc -ErrorAction SilentlyContinue | Select-Object -First 1
          if (-not $checkCluster) { Show-Check 'FAIL' "Cluster $ClusterName was not found in $Datacenter" 'Check the name with: Get-Cluster' }
          else {
            $checkHost = Get-VMHost -Server $checkServer -Location $checkCluster | Where-Object { $_.ConnectionState -eq 'Connected' } | Select-Object -First 1
            if ($checkHost) { Show-Check 'OK' "Cluster $ClusterName, with the connected host $($checkHost.Name)" } else { Show-Check 'FAIL' "Cluster $ClusterName has no connected host" }
          }
        } elseif ($checkDc -and $VMHostName) {
          $checkHost = Get-VMHost -Server $checkServer -Name $VMHostName -Location $checkDc -ErrorAction SilentlyContinue | Select-Object -First 1
          if ($checkHost) { Show-Check 'OK' "Host ${VMHostName}: ESXi $($checkHost.Version)" } else { Show-Check 'FAIL' "Host $VMHostName was not found in $Datacenter" 'Check the name with: Get-VMHost' }
        }
        if (-not $Datastore) { Show-Check 'FAIL' 'No datastore was given (-Datastore)' 'Pass the name of the datastore for the machines' }
        elseif ($checkDc) {
          $checkDs = Get-Datastore -Server $checkServer -Name $Datastore -Location $checkDc -ErrorAction SilentlyContinue | Select-Object -First 1
          if (-not $checkDs) { Show-Check 'FAIL' "Datastore $Datastore was not found in $Datacenter" 'Check the name with: Get-Datastore' }
          elseif ($checkDs.FreeSpaceGB -ge $needGb) { Show-Check 'OK' ("Datastore {0}: {1:N0} GB free. The thin disks can grow to {2} GB" -f $Datastore, $checkDs.FreeSpaceGB, $needGb) }
          else { Show-Check 'WARN' ("Datastore {0}: {1:N0} GB free, and the thin disks can grow to {2} GB" -f $Datastore, $checkDs.FreeSpaceGB, $needGb) 'Free some space, or use a larger datastore' }
        }
        if ($UseExistingSwitch) {
          if (Get-VDSwitch -Server $checkServer -Name $UseExistingSwitch -ErrorAction SilentlyContinue) { Show-Check 'OK' "Distributed switch $UseExistingSwitch" }
          else { Show-Check 'FAIL' "Distributed switch $UseExistingSwitch was not found" 'Check the name with: Get-VDSwitch' }
        } elseif ($checkHost) {
          foreach ($pair in @(@('-Trunk1Nic', $Trunk1Nic), @('-Trunk2Nic', $Trunk2Nic), @('-OobNic', $OobNic), @('-WanNic', $WanNic))) {
            if (-not $pair[1]) { Show-Check 'WARN' "$($pair[0]) was not given, so that lab network has no uplink and stays inside the host"; continue }
            if (Get-VMHostNetworkAdapter -VMHost $checkHost -Physical -Name $pair[1] -ErrorAction SilentlyContinue) { Show-Check 'OK' "$($pair[0]) $($pair[1])" }
            else { Show-Check 'FAIL' "$($pair[0]) $($pair[1]) is not a physical NIC of $($checkHost.Name)" 'List them with: Get-VMHostNetworkAdapter -Physical' }
          }
        }
        if ($checkHost -and -not $ClusterName) {
          $freeMb = ($checkHost.MemoryTotalGB - $checkHost.MemoryUsageGB) * 1024
          if ($freeMb -ge $needMb) { Show-Check 'OK' ("Memory: the machines use {0:N1} GB, and {1:N1} GB is free on the host" -f ($needMb / 1024), ($freeMb / 1024)) }
          else { Show-Check 'WARN' ("Memory: the machines use {0:N1} GB, and {1:N1} GB is free on the host" -f ($needMb / 1024), ($freeMb / 1024)) 'Leave machines out in the Lab Builder, or make them smaller' }
        }
        if ($checkLab) {
          $existing = @($checkLab.vms | Where-Object { Get-LabVm -Server $checkServer -Name $_.name -Folder $FolderName })
          if ($existing.Count) { Show-Check 'OK' "$($existing.Count) machine(s) of the lab already exist in the folder $FolderName. A deploy skips them" }
          $elsewhere = @(Get-VM -Server $checkServer -Name $checkLab.vms.name -ErrorAction SilentlyContinue | Where-Object { $_.Folder.Name -ne $FolderName })
          if ($elsewhere.Count) { Show-Check 'WARN' "Machines with a lab name exist outside the folder ${FolderName}: $(($elsewhere | ForEach-Object { $_.Name } | Sort-Object -Unique) -join ', ')" 'A deploy skips a name that exists anywhere in vCenter. Rename the lab machines in the Lab Builder' }
        }
      }
      finally { Disconnect-VIServer -Server $checkServer -Confirm:$false -ErrorAction SilentlyContinue }
    }
    catch {
      Show-Check 'FAIL' "vCenter $VcenterServer could not be checked: $($_.Exception.Message)" 'Check the server name and the account. For a first run on a lab network, add -SkipCertificateCheck'
    }
  }

  if ($script:failed) { Write-Host "$($script:failed) problem(s) to fix before the build." -ForegroundColor Red; exit 1 }
  Write-Host 'Ready. Run the preview next (-WhatIf).' -ForegroundColor Green
  return
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
# The machine whose first adapter stays as the uplink to the external firewall. The Lab Builder writes "uplink" into
# the manifest when the build keeps one. RemoveBuildNics and Snapshot then leave that adapter alone.
$uplinkVm = if ($lab.PSObject.Properties['uplink'] -and $lab.uplink.vm) { [string]$lab.uplink.vm } else { '' }
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

  if ($Action -in 'Status', 'RemoveBuildNics', 'Snapshot', 'Restore', 'Remove') {
    if (-not (Get-Folder -Server $server -Name $FolderName -Type VM -ErrorAction SilentlyContinue)) {
      Write-Host "The folder $FolderName does not exist in vCenter, so no lab machine was found. Pass -FolderName if the lab uses another folder."
      return
    }
  }
  if ($Action -eq 'Status') {
    # Each machine, whether its first boot has finished, and its addresses.
    $started = Get-Date
    $deadline = $started.AddMinutes($WaitMinutes)
    $everReported = $false
    while ($true) {
      $rows = @(); $pending = @(); $failedNames = @(); $notChecked = @()
      foreach ($vmDef in $lab.vms) {
        $vm = Get-LabVm -Server $server -Name $vmDef.name -Folder $FolderName
        if (-not $vm) { $notChecked += $vmDef.name; $rows += [pscustomobject]@{ Machine = $vmDef.name; Power = 'missing'; Build = ''; Detail = ''; Addresses = '' }; continue }
        $build = ''; $detail = ''
        if ($vm.PowerState -eq 'PoweredOn') {
          if ((Get-FlavorRecord (Get-FlavorId $vmDef $lab)).iso) { $notChecked += $vmDef.name; $build = 'manual'; $detail = 'installs from an ISO, so look at its console' }
          else {
            $b = Get-LabBuildState $vm
            $build = $b.State; $detail = $b.Detail
            if ($build -ne 'unknown') { $everReported = $true } else { $detail = 'not reported yet' }
            if ($build -in 'running', 'unknown') { $pending += $vmDef.name }
            if ($build -eq 'failed') { $failedNames += $vmDef.name }
          }
        } else { $notChecked += $vmDef.name }
        $rows += [pscustomobject]@{ Machine = $vmDef.name; Power = [string]$vm.PowerState; Build = $build; Detail = $detail; Addresses = ($vm.Guest.IPAddress -join ' ') }
      }
      if (-not $Wait -or -not $pending.Count -or (Get-Date) -ge $deadline) { break }
      # If no machine has reported after six minutes, the guest tools are not passing the state on. Stop waiting.
      if (-not $everReported -and ((Get-Date) - $started).TotalMinutes -ge 6) { break }
      Write-Host ('{0:HH:mm:ss} Still building: {1}' -f (Get-Date), ($pending -join ' '))
      Start-Sleep -Seconds 15
    }
    $rows | Format-Table -AutoSize -Wrap
    if (-not ($rows | Where-Object { $_.Power -eq 'PoweredOn' })) {
      Write-Host "No lab machine is powered on in the folder $FolderName."
      return
    }
    if ($failedNames.Count) { throw "These machines report a problem (a failed first boot, or a lab service that is not running): $($failedNames -join ', '). Log in to one and run: lab201-status" }
    if ($pending.Count -and -not $everReported) {
      Write-Host 'No machine reports its build state yet. A machine reports about a minute after it starts.'
      Write-Host 'To check one by hand, log in to it and run: lab201-status'
      if ($Wait) { throw 'The build state could not be read.' }
    }
    elseif ($Wait -and $pending.Count) { throw "Not every machine finished within $WaitMinutes minutes: $($pending -join ', ')" }
    elseif ($Wait -and $notChecked.Count) {
      # Say what the table shows and no more: a machine that is off, missing, or installs by hand was not checked.
      Write-Host 'Every machine that reports has finished its first boot.' -ForegroundColor Green
      Write-Host "Not checked, because they are off or missing, or they install from an ISO: $($notChecked -join ', ')"
    }
    elseif ($Wait) { Write-Host 'Every machine has finished its first boot.' -ForegroundColor Green }
    return
  }
  if ($Action -eq 'Snapshot') {
    # A snapshot keeps the machine's adapters. With the build adapter still there, a restore would bring it back,
    # and with it the machine's path to the internet. So the build adapters have to go first.
    $withBuildNic = @()
    foreach ($vmDef in $lab.vms) {
      # The first adapter of the uplink machine is its uplink to the external firewall, and it stays.
      if ($vmDef.name -eq $uplinkVm) { continue }
      $vm = Get-LabVm -Server $server -Name $vmDef.name -Folder $FolderName
      if (-not $vm) { continue }
      $mac = & $macOf $vmDef.name 0
      if (Get-NetworkAdapter -VM $vm | Where-Object { $_.MacAddress -ieq $mac }) { $withBuildNic += $vmDef.name }
    }
    if ($withBuildNic.Count) {
      throw "These machines still have their build adapter: $($withBuildNic -join ', '). A snapshot keeps that adapter, and a restore would bring it back with its path to the internet. Run -Action RemoveBuildNics first. No snapshot was taken."
    }
    foreach ($vmDef in $lab.vms) {
      $vm = Get-LabVm -Server $server -Name $vmDef.name -Folder $FolderName
      if (-not $vm) { continue }
      if (Get-Snapshot -VM $vm -Name $SnapshotName -ErrorAction SilentlyContinue) { Write-Host "$($vmDef.name) has the snapshot $SnapshotName. Skipped."; continue }
      if (-not $PSCmdlet.ShouldProcess($vmDef.name, "Take the snapshot $SnapshotName")) { continue }
      Write-Host "Taking the snapshot $SnapshotName of $($vmDef.name)"
      New-Snapshot -VM $vm -Name $SnapshotName -Description 'Lab 201 baseline (Lab 999.6)' -Memory:$false -Quiesce:$false -Confirm:$false | Out-Null
    }
    return
  }
  if ($Action -eq 'Restore') {
    # The gateway first, then the rest. The snapshot holds no memory, so each machine boots from its disk.
    $gwFirst = ($lab.vms | Where-Object { $_.role -eq 'gateway' } | Select-Object -First 1).name
    $restoreOrder = @($gwFirst) + @($lab.vms.name | Where-Object { $_ -ne $gwFirst })
    $noSnapshot = @()
    foreach ($name in $restoreOrder) {
      if (-not $name) { continue }
      $vm = Get-LabVm -Server $server -Name $name -Folder $FolderName
      if (-not $vm) { continue }
      $snap = Get-Snapshot -VM $vm -Name $SnapshotName -ErrorAction SilentlyContinue | Select-Object -First 1
      if (-not $snap) { Write-Warning "$name has no snapshot $SnapshotName. It is left as it is."; $noSnapshot += $name; continue }
      if (-not $PSCmdlet.ShouldProcess($name, "Return to the snapshot $SnapshotName and power on")) { continue }
      Write-Host "Returning $name to the snapshot $SnapshotName"
      Set-VM -VM $vm -Snapshot $snap -Confirm:$false | Out-Null
      $vm = Get-LabVm -Server $server -Name $name -Folder $FolderName
      if ($vm.PowerState -ne 'PoweredOn') { Start-VM -VM $vm | Out-Null }
    }
    if ($noSnapshot.Count) { throw "No snapshot $SnapshotName on: $($noSnapshot -join ', '). Take it first with -Action Snapshot." }
    return
  }
  if ($Action -eq 'RemoveBuildNics') {
    foreach ($vmDef in $lab.vms) {
      if ($vmDef.name -eq $uplinkVm) { Write-Host "$($vmDef.name) keeps its first adapter: it is the uplink to the external firewall."; continue }
      $vm = Get-LabVm -Server $server -Name $vmDef.name -Folder $FolderName
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
      $vm = Get-LabVm -Server $server -Name $vmDef.name -Folder $FolderName
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
    if ((Get-FlavorRecord $fid).iso) { $null = Get-IsoPath -Id $fid -Supplied $IsoImages; continue }
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
  & $pyExe @pyArgs (Join-Path $PSScriptRoot '..\common\make-seed.py') --manifest $Manifest --out $seedDir --iso --guest-agent vmware --tagging hypervisor @keys @licenseArgs
  if ($LASTEXITCODE -ne 0) { throw 'make-seed.py failed.' }
  $psDrive = New-PSDrive -Name lab201ds -PSProvider VimDatastore -Root '\' -Location $ds
  New-Item -Path 'lab201ds:\lab201-seeds' -ItemType Directory -ErrorAction SilentlyContinue | Out-Null

  foreach ($vmDef in $lab.vms) {
    $name = $vmDef.name
    if (Get-VM -Server $server -Name $name -ErrorAction SilentlyContinue) { Write-Host "$name exists. Skipped."; continue }
    if (-not $PSCmdlet.ShouldProcess($name, 'Clone from the template and configure')) { continue }
    Write-Host "Creating $name"
    $fid = Get-FlavorId $vmDef $lab
    $isIso = [bool](Get-FlavorRecord $fid).iso
    if ($isIso) {
      # An empty machine. The install ISO and the answer or first-login CD are attached below.
      $vm = New-VM -Name $name @placement -Datastore $ds -Location $folder -NumCpu $vmDef.vcpu -MemoryMB $vmDef.memory_mb -DiskGB $vmDef.disk_gb -DiskStorageFormat Thin -GuestId (Get-FlavorRecord $fid).guest_id -HardwareVersion $HardwareVersion
      $nicType = Get-IsoNicType $fid
    }
    else {
      $vm = New-VM -Name $name -Template $templateOf[(Get-ImageFlavorId $fid)] @placement -Datastore $ds -Location $folder -DiskStorageFormat Thin
      Set-VM -VM $vm -NumCpu $vmDef.vcpu -MemoryMB $vmDef.memory_mb -Confirm:$false | Out-Null
      # A disk cannot shrink. When the image is already larger than the manifest's size, the disk keeps the size of the image.
      $hd = Get-HardDisk -VM $vm | Select-Object -First 1
      if ($hd.CapacityGB -lt $vmDef.disk_gb) { Set-HardDisk -HardDisk $hd -CapacityGB $vmDef.disk_gb -Confirm:$false | Out-Null }
      elseif ($hd.CapacityGB -gt $vmDef.disk_gb) { Write-Host ('  {0}: its image is {1:N0} GB, larger than the {2} GB the manifest asks for. A disk cannot shrink, so it stays that size.' -f $name, $hd.CapacityGB, $vmDef.disk_gb) }
      $nicType = 'Vmxnet3'
    }
    Get-NetworkAdapter -VM $vm | Remove-NetworkAdapter -Confirm:$false
    for ($n = 0; $n -lt $vmDef.nics.Count; $n++) {
      $pg = & $pgOf $vmDef.nics[$n]
      $mac = & $macOf $name $n
      if ($NetworkType -eq 'Standard') {
        New-NetworkAdapter -VM $vm -NetworkName $pg -Type $nicType -MacAddress $mac -StartConnected | Out-Null
      }
      else {
        $vdpg = Get-VDPortgroup -Server $server -Name $pg
        New-NetworkAdapter -VM $vm -Portgroup $vdpg -Type $nicType -MacAddress $mac -StartConnected | Out-Null
      }
    }
    Copy-DatastoreItem -Item (Join-Path $seedDir "$name-seed.iso") -Destination 'lab201ds:\lab201-seeds\' -Force
    Get-CDDrive -VM $vm | Remove-CDDrive -Confirm:$false
    if ($isIso) { New-CDDrive -VM $vm -IsoPath (Get-IsoPath -Id $fid -Supplied $IsoImages) -StartConnected | Out-Null }
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
