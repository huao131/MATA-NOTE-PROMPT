[CmdletBinding()]
param([switch]$ValidateOnly)

$ErrorActionPreference = 'Stop'
$credentialTarget = 'MATA-AI-VIDEO-STUDIO/GitHubTransport'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Show-TokenDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = 'MATA Local Watcher — GitHub Token'
    $form.Size = New-Object System.Drawing.Size(520, 190)
    $form.StartPosition = 'CenterScreen'
    $form.FormBorderStyle = 'FixedDialog'
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false

    $label = New-Object System.Windows.Forms.Label
    $label.Text = '貼上 Fine-grained PAT（僅寫入 Windows Credential Manager，不會儲存至檔案或顯示於日誌）：'
    $label.Location = New-Object System.Drawing.Point(18, 18)
    $label.Size = New-Object System.Drawing.Size(470, 40)
    $form.Controls.Add($label)

    $input = New-Object System.Windows.Forms.TextBox
    $input.Location = New-Object System.Drawing.Point(18, 68)
    $input.Size = New-Object System.Drawing.Size(470, 24)
    $input.UseSystemPasswordChar = $true
    $form.Controls.Add($input)

    $save = New-Object System.Windows.Forms.Button
    $save.Text = '安全儲存'
    $save.Location = New-Object System.Drawing.Point(300, 108)
    $save.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $form.AcceptButton = $save
    $form.Controls.Add($save)

    $cancel = New-Object System.Windows.Forms.Button
    $cancel.Text = '取消'
    $cancel.Location = New-Object System.Drawing.Point(398, 108)
    $cancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.CancelButton = $cancel
    $form.Controls.Add($cancel)

    if ($form.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK -or [string]::IsNullOrWhiteSpace($input.Text)) { throw 'TOKEN_CONFIGURATION_CANCELLED' }
    return $input.Text
}

if ($ValidateOnly) {
    $probe = New-Object System.Windows.Forms.TextBox
    if (-not $probe.UseSystemPasswordChar) { $probe.UseSystemPasswordChar = $true }
    & cmdkey /list:$credentialTarget *> $null
    [pscustomobject]@{ SecureInputDialog = ($probe.UseSystemPasswordChar -eq $true); CredentialManagerAvailable = ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1168); CredentialTarget = $credentialTarget }
    exit 0
}

$token = Show-TokenDialog
try {
    & cmdkey "/generic:$credentialTarget" '/user:github-api-token' "/pass:$token" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'CREDENTIAL_MANAGER_WRITE_FAILED' }
} finally {
    $token = $null
}
Write-Output 'GitHub transport credential stored securely.'
