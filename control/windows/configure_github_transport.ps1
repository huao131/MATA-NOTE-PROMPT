[CmdletBinding()]
param([switch]$ValidateOnly)

$ErrorActionPreference = 'Stop'
$credentialTarget = 'MATA-AI-VIDEO-STUDIO/GitHubTransport'
$runtimeDirectory = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\runtime'))
$statusFile = Join-Path $runtimeDirectory 'github_transport_credential_status.json'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class MataCredentialStore {
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
  public struct CREDENTIAL {
    public UInt32 Flags; public UInt32 Type; public string TargetName; public string Comment;
    public System.Runtime.InteropServices.ComTypes.FILETIME LastWritten;
    public UInt32 CredentialBlobSize; public IntPtr CredentialBlob; public UInt32 Persist;
    public UInt32 AttributeCount; public IntPtr Attributes; public string TargetAlias; public string UserName;
  }
  [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
  public static extern bool CredWrite(ref CREDENTIAL credential, UInt32 flags);
  [DllImport("Advapi32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
  public static extern bool CredRead(string target, UInt32 type, UInt32 flags, out IntPtr credential);
  [DllImport("Advapi32.dll", SetLastError = true)] public static extern void CredFree(IntPtr credential);
}
'@

function Write-SafeStatus([string]$status, [string]$detail) {
  New-Item -ItemType Directory -Force -Path $runtimeDirectory | Out-Null
  [pscustomobject]@{ status = $status; target = $credentialTarget; user = [Environment]::UserName; timestamp_utc = [DateTime]::UtcNow.ToString('o'); detail = $detail } |
    ConvertTo-Json -Compress | Set-Content -LiteralPath $statusFile -Encoding UTF8
}

function Test-Credential {
  $pointer = [IntPtr]::Zero
  try {
    return [MataCredentialStore]::CredRead($credentialTarget, 1, 0, [ref]$pointer)
  } finally {
    if ($pointer -ne [IntPtr]::Zero) { [MataCredentialStore]::CredFree($pointer) }
  }
}

function Show-TokenDialog {
  $form = New-Object System.Windows.Forms.Form
  $form.Text = 'MATA GitHub Secure Setup'
  $form.Size = New-Object System.Drawing.Size(550, 210)
  $form.StartPosition = 'CenterScreen'; $form.FormBorderStyle = 'FixedDialog'
  $form.MaximizeBox = $false; $form.MinimizeBox = $false
  $label = New-Object System.Windows.Forms.Label
  $label.Text = 'Paste the Fine-grained GitHub Token. It is masked and stored only in Windows Credential Manager.'
  $label.Location = New-Object System.Drawing.Point(18, 18); $label.Size = New-Object System.Drawing.Size(500, 48)
  $form.Controls.Add($label)
  $input = New-Object System.Windows.Forms.TextBox
  $input.Location = New-Object System.Drawing.Point(18, 78); $input.Size = New-Object System.Drawing.Size(500, 24); $input.UseSystemPasswordChar = $true
  $form.Controls.Add($input)
  $save = New-Object System.Windows.Forms.Button; $save.Text = 'Save and verify'; $save.Location = New-Object System.Drawing.Point(288, 122); $save.DialogResult = [System.Windows.Forms.DialogResult]::OK
  $cancel = New-Object System.Windows.Forms.Button; $cancel.Text = 'Cancel'; $cancel.Location = New-Object System.Drawing.Point(420, 122); $cancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
  $form.AcceptButton = $save; $form.CancelButton = $cancel; $form.Controls.AddRange(@($save,$cancel))
  if ($form.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK -or [string]::IsNullOrWhiteSpace($input.Text)) { throw 'TOKEN_CONFIGURATION_CANCELLED' }
  return $input.Text
}

try {
  if ($ValidateOnly) {
    if (Test-Credential) { Write-SafeStatus 'CREDENTIAL_PRESENT' 'Credential Manager read succeeded.'; exit 0 }
    Write-SafeStatus 'CREDENTIAL_MISSING' 'Credential target was not found for this Windows user.'; exit 1
  }
  $token = Show-TokenDialog
  $blob = [Runtime.InteropServices.Marshal]::StringToCoTaskMemUni($token)
  try {
    $credential = New-Object MataCredentialStore+CREDENTIAL
    $credential.Type = 1; $credential.TargetName = $credentialTarget; $credential.UserName = 'github-api-token'
    $credential.Persist = 2; $credential.CredentialBlob = $blob; $credential.CredentialBlobSize = [Text.Encoding]::Unicode.GetByteCount($token)
    if (-not [MataCredentialStore]::CredWrite([ref]$credential, 0)) { throw 'CREDENTIAL_MANAGER_WRITE_FAILED' }
  } finally { [Runtime.InteropServices.Marshal]::ZeroFreeCoTaskMemUnicode($blob); $token = $null }
  if (-not (Test-Credential)) { throw 'CREDENTIAL_MANAGER_READBACK_FAILED' }
  Write-SafeStatus 'CREDENTIAL_PRESENT' 'Credential stored and read back successfully.'
  [System.Windows.Forms.MessageBox]::Show('GitHub Token was stored and verified. The connection test can now start.', 'MATA', 'OK', 'Information') | Out-Null
} catch {
  Write-SafeStatus 'CREDENTIAL_ERROR' $_.Exception.Message
  [System.Windows.Forms.MessageBox]::Show(('Secure setup failed: ' + $_.Exception.Message), 'MATA', 'OK', 'Error') | Out-Null
  exit 1
}
