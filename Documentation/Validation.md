# Validation Procedure

## 1. Register the Windows event source

Run once from an elevated PowerShell session:

```powershell
New-EventLog -LogName Application -Source ClickFixMonitor
```

## 2. Build the monitor

```powershell
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

The monitor must run in the logged-on interactive Windows session because it uses Windows UI Automation.

## 3. Verify Event ID 1001

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Application'
    ProviderName = 'ClickFixMonitor'
    Id = 1001
} -MaxEvents 5 |
    Format-List TimeCreated, ProviderName, Id, Message
```

## 4. Confirm Wazuh archive collection

```bash
sudo jq -c 'select(.data.win.system.providerName=="ClickFixMonitor" and ((.data.win.system.eventID|tostring)=="1001"))' /var/ossec/logs/archives/archives.json | tail -1
```

## 5. Validate Wazuh syntax

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

## 6. Test the rule chain

```bash
sudo /var/ossec/bin/wazuh-logtest
```

The validated hierarchy ends at rule `100102` with Level 15 for a HIGH-risk Event ID 1001 containing a strong PowerShell indicator.

## 7. Restart and verify live alerting

```bash
sudo systemctl restart wazuh-manager
sudo systemctl is-active wazuh-manager
sudo grep '"id":"100102"' /var/ossec/logs/alerts/alerts.json | tail -1
```

A key troubleshooting finding in the project was that the event initially reached `archives.json` but did not produce the custom live alert. The base rule was corrected to inherit from Windows Application parent rule `60601`; after syntax validation and manager restart, live validation succeeded.

## Sanitized test event

```text
Provider: ClickFixMonitor
Event ID: 1001
Channel: Application
Target: Windows Run Dialog
Command Line: powershell -w hidden -ep bypass -c <defanged laboratory command>
Matched Indicators: powershell, irm, -ep bypass
Risk: HIGH
Detection Stage: Pre-Execution
Description: Suspicious command content was detected inside the Windows Run dialog before process execution.
```
