Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- FORM ---
$form = New-Object System.Windows.Forms.Form
$form.Text = "Adaptive Learning Framework"
$form.Size = New-Object System.Drawing.Size(650,500)
$form.StartPosition = "CenterScreen"
$form.BackColor = "#1e1e1e"

# --- LOGO ---
$logo = New-Object System.Windows.Forms.PictureBox
$logo.Image = [System.Drawing.Image]::FromFile("$PSScriptRoot\logo.png")
$logo.SizeMode = "Zoom"
$logo.Size = New-Object System.Drawing.Size(120,120)
$logo.Location = New-Object System.Drawing.Point(20,20)
$form.Controls.Add($logo)

# --- TITLE ---
$title = New-Object System.Windows.Forms.Label
$title.Text = "Adaptive Learning Framework"
$title.ForeColor = "White"
$title.Font = New-Object System.Drawing.Font("Segoe UI",18,[System.Drawing.FontStyle]::Bold)
$title.AutoSize = $true
$title.Location = New-Object System.Drawing.Point(160,60)
$form.Controls.Add($title)

# --- LOG PANEL ---
$logBox = New-Object System.Windows.Forms.RichTextBox
$logBox.Location = New-Object System.Drawing.Point(20,160)
$logBox.Size = New-Object System.Drawing.Size(600,260)
$logBox.BackColor = "#111111"
$logBox.ForeColor = "White"
$logBox.Font = New-Object System.Drawing.Font("Consolas",10)
$logBox.ReadOnly = $true
$form.Controls.Add($logBox)

# --- TRAY ICON ---
$tray = New-Object System.Windows.Forms.NotifyIcon
$tray.Icon = [System.Drawing.SystemIcons]::Information
$tray.Visible = $true
$tray.Text = "ALF Running"

$menu = New-Object System.Windows.Forms.ContextMenu
$exitItem = New-Object System.Windows.Forms.MenuItem "Exit"
$exitItem.add_Click({ $tray.Visible = $false; $form.Close() })
$menu.MenuItems.Add($exitItem)
$tray.ContextMenu = $menu

$form.add_Resize({
    if ($form.WindowState -eq "Minimized") {
        $form.Hide()
        $tray.ShowBalloonTip(1000, "ALF", "Draait nu in de achtergrond", [System.Windows.Forms.ToolTipIcon]::Info)
    }
})

$tray.add_MouseDoubleClick({
    $form.Show()
    $form.WindowState = "Normal"
})

# --- START BUTTON ---
$startButton = New-Object System.Windows.Forms.Button
$startButton.Text = "Start ALF"
$startButton.Size = New-Object System.Drawing.Size(160,45)
$startButton.Location = New-Object System.Drawing.Point(430,40)
$startButton.BackColor = "#3a3a3a"
$startButton.ForeColor = "White"
$startButton.Font = New-Object System.Drawing.Font("Segoe UI",10)

$startButton.Add_Click({

    $logBox.AppendText("=== ALF Launcher ===`n")

    # 1. Ga naar scriptmap
    Set-Location "$PSScriptRoot"
    $logBox.AppendText("Working directory: $PSScriptRoot`n")

    # 2. Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        $logBox.AppendText("Python not installed.`n")
        [System.Windows.Forms.MessageBox]::Show("Python is not installed. Install it from python.org")
        return
    }
    $logBox.AppendText("Python OK`n")

    # 3. Dependencies
    if (Test-Path "requirements.txt") {
        $logBox.AppendText("Installing dependencies...`n")
        python -m pip install -r requirements.txt | Out-Null
        $logBox.AppendText("Dependencies OK`n")
    }

    # 4. Start ALF
    $logBox.AppendText("Starting ALF...`n")

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "python"
    $psi.Arguments = "alf_app.py"
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true

    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $psi
    $proc.Start() | Out-Null

    # Live logging
    Start-Job -ScriptBlock {
        param($p, $log)
        while (!$p.HasExited) {
            if (!$p.StandardOutput.EndOfStream) {
                $line = $p.StandardOutput.ReadLine()
                $log.Invoke([Action[string]]{
                    param($text)
                    $logBox.AppendText($text + "`n")
                }, $line)
            }
        }
    } -ArgumentList $proc, $logBox
})

$form.Controls.Add($startButton)

# --- EXIT BUTTON ---
$exitButton = New-Object System.Windows.Forms.Button
$exitButton.Text = "Exit"
$exitButton.Size = New-Object System.Drawing.Size(160,35)
$exitButton.Location = New-Object System.Drawing.Point(430,100)
$exitButton.BackColor = "#3a3a3a"
$exitButton.ForeColor = "White"
$exitButton.Font = New-Object System.Drawing.Font("Segoe UI",9)

$exitButton.Add_Click({
    $tray.Visible = $false
    $form.Close()
})

$form.Controls.Add($exitButton)

# --- RUN ---
$form.ShowDialog()
