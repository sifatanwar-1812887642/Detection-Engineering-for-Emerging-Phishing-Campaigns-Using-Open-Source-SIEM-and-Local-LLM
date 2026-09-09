# ClickFixMonitor

`ClickFixMonitor` is the Windows pre-execution monitoring component used in this project. It inspects the Windows Run dialog with UI Automation and writes a Windows Application event when suspicious command-like content is observed before execution.

## What it generates

- Event log: `Application`
- Provider: `ClickFixMonitor`
- Event ID: `1001`
- Detection stage: pre-execution

## 1. Install .NET 8 SDK

Open PowerShell as Administrator:

```powershell
winget install Microsoft.DotNet.SDK.8
```

Verify:

```powershell
dotnet --version
```

## 2. Clone the repository

```powershell
git clone https://github.com/sifatanwar-1812887642/Detection-Engineering-for-Emerging-Phishing-Campaigns-Using-Open-Source-SIEM-and-Local-LLM.git
cd Detection-Engineering-for-Emerging-Phishing-Campaigns-Using-Open-Source-SIEM-and-Local-LLM\ClickFixMonitor
```

## 3. Register the Windows Event Log source

Run once from Administrator PowerShell:

```powershell
New-EventLog -LogName Application -Source ClickFixMonitor
```

If the source already exists, continue to the next step.

## 4. Restore and build

```powershell
dotnet restore
dotnet build -c Release
```

To create a standalone Windows executable:

```powershell
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

## 5. Run the monitor

For a development run:

```powershell
dotnet run -c Release
```

Keep the monitor running while testing.

## 6. Safe pre-execution validation

Use only a controlled, harmless test string. For example, place this text into the Windows Run dialog but **do not press Enter**:

```text
powershell -NoP Write-Output "ClickFix Test"
```

The purpose is only to verify that the monitor sees suspicious command-like content in the Run dialog before execution.

## 7. Verify Event ID 1001 locally

Open Event Viewer and check:

```text
Windows Logs > Application
```

Or use PowerShell:

```powershell
Get-WinEvent -FilterHashtable @{
  LogName = 'Application'
  ProviderName = 'ClickFixMonitor'
  Id = 1001
} -MaxEvents 5 | Format-List TimeCreated, ProviderName, Id, Message
```

Expected fields include:

- target: Windows Run Dialog
- command line / observed text
- matched indicators
- risk
- detection stage
- hostname
- username
- SHA-256 hash

## 8. Verify Wazuh ingestion

Once the Windows Wazuh Agent is connected, check the manager:

```bash
sudo grep -i 'ClickFixMonitor' /var/ossec/logs/archives/archives.json | tail -20
```

Then apply the repository's `Wazuh/local_rules.xml` hierarchy and verify alerts.

## Safety

This component is intended for authorized lab detection testing. It should be validated with harmless strings and should not be used to execute real malicious payloads.