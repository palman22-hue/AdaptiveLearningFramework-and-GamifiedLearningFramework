[Setup]
AppName=Adaptive Learning Framework
AppVersion=1.0
DefaultDirName={pf}\ALF
DefaultGroupName=ALF
OutputDir=.
OutputBaseFilename=ALF_Installer
Compression=lzma
SolidCompression=yes

[Files]
; Hoofdbestanden
Source: "alf_app.py"; DestDir: "{app}"
Source: "alf_cli.py"; DestDir: "{app}"
Source: "requirements.txt"; DestDir: "{app}"
Source: "requirements.lock"; DestDir: "{app}"
Source: "pyproject.toml"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"
Source: "ALF_Launcher_GUI.ps1"; DestDir: "{app}"
Source: "ALF_Launcher.ps1"; DestDir: "{app}"
Source: "install_alf.ps1"; DestDir: "{app}"
Source: "logo.PNG"; DestDir: "{app}"

; Submappen
Source: "ALFframework\*"; DestDir: "{app}\ALFframework"; Flags: recursesubdirs
Source: "problems\*"; DestDir: "{app}\problems"; Flags: recursesubdirs
Source: "Backup\*"; DestDir: "{app}\Backup"; Flags: recursesubdirs

; Niet meenemen: venv en __pycache__
; We nemen ze niet op in het script — Inno Setup negeert ze dan automatisch

[Icons]
Name: "{group}\ALF Launcher"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\ALF_Launcher_GUI.ps1"""
Name: "{commondesktop}\ALF Launcher"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\ALF_Launcher_GUI.ps1"""

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\ALF_Launcher_GUI.ps1"""; Flags: postinstall nowait
