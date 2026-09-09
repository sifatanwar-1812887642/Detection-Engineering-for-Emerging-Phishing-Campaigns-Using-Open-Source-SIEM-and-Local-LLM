# End-to-End Deployment and Reproduction Guide

This document explains how another user can reproduce the project in a controlled lab from start to finish.

## 1. Build the lab

Create three isolated VirtualBox VMs:

| VM | OS | Project address | Purpose |
|---|---|---:|---|
| Victim | Windows 11 | `10.0.2.15` | Sysmon, PowerShell logging, Wazuh Agent, ClickFixMonitor |
| SIEM | Ubuntu 24.04 | `10.0.2.6` | Wazuh Manager, Indexer, Dashboard |
| AI | Ubuntu 24.04 | `10.0.2.7` | Ollama + Qwen2.5:3B |

Keep the environment isolated from production systems. If you use different IP addresses, update the configurations and Python script accordingly.

## 2. Deploy Wazuh on Ubuntu

Install Wazuh Manager, Indexer, and Dashboard on the Ubuntu SIEM VM. This project used Wazuh `4.14.5`.

Verify:

```bash
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
```

Enable JSON archives in `/var/ossec/etc/ossec.conf`:

```xml
<logall_json>yes</logall_json>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

The project compares:

```text
/var/ossec/logs/archives/archives.json
/var/ossec/logs/alerts/alerts.json
```

## 3. Prepare the Windows victim

Install and enable:

- Wazuh Agent
- Sysmon
- Windows PowerShell Operational logging
- Microsoft Defender
- .NET 8 SDK

Point the Wazuh Agent to `10.0.2.6` and verify that the endpoint is active on the manager.

Ensure the Wazuh Agent collects at least:

```xml
<localfile>
  <location>Application</location>
  <log_format>eventchannel</log_format>
</localfile>

<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>

<localfile>
  <location>Microsoft-Windows-PowerShell/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Restart the agent:

```powershell
Restart-Service wazuh
```

## 4. Build ClickFixMonitor

Clone this repository on Windows:

```powershell
git clone https://github.com/sifatanwar-1812887642/Detection-Engineering-for-Emerging-Phishing-Campaigns-Using-Open-Source-SIEM-and-Local-LLM.git
cd Detection-Engineering-for-Emerging-Phishing-Campaigns-Using-Open-Source-SIEM-and-Local-LLM\ClickFixMonitor
```

Register the event source once:

```powershell
New-EventLog -LogName Application -Source ClickFixMonitor
```

Build:

```powershell
dotnet restore
dotnet build -c Release
```

Run:

```powershell
dotnet run -c Release
```

## 5. Validate the pre-execution event safely

Use a harmless test string only. Open the Windows Run dialog and paste:

```text
powershell -NoP Write-Output "ClickFix Test"
```

Do not press Enter. The goal is to validate detection before execution.

Check Event ID `1001`:

```powershell
Get-WinEvent -FilterHashtable @{
  LogName = 'Application'
  ProviderName = 'ClickFixMonitor'
  Id = 1001
} -MaxEvents 5 | Format-List TimeCreated, ProviderName, Id, Message
```

## 6. Confirm the event reaches Wazuh

On the Wazuh server:

```bash
sudo grep -i 'ClickFixMonitor' /var/ossec/logs/archives/archives.json | tail -20
```

At this point the path is:

```text
Windows Run dialog
  -> ClickFixMonitor
  -> Application Event ID 1001
  -> Wazuh Agent
  -> Wazuh Manager
  -> archives.json
```

## 7. Deploy the custom detection rules

The repository contains:

```text
Wazuh/local_rules.xml
```

Add its ClickFix rule group to the manager's:

```text
/var/ossec/etc/rules/local_rules.xml
```

Validate before restart:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Then restart:

```bash
sudo systemctl restart wazuh-manager
```

Rule hierarchy:

- `100100` — base Event ID 1001 detection
- `100101` — HIGH-risk pre-execution detection
- `100102` — strong PowerShell indicator detection

Check alerts:

```bash
sudo grep -E '100100|100101|100102' /var/ossec/logs/alerts/alerts.json | tail -20
```

## 8. Prepare the local LLM VM

On Ubuntu AI VM `10.0.2.7`, install Ollama and pull the model used by the project:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b
ollama list
```

Allow the Ollama service to listen on the lab network by setting:

```text
OLLAMA_HOST=0.0.0.0:11434
```

Restart Ollama and verify that port `11434` is listening.

From the Wazuh server test connectivity:

```bash
curl http://10.0.2.7:11434/api/tags
```

## 9. Run the AI-assisted analysis

On the Wazuh server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r LLM/requirements.txt
python3 LLM/event1001_to_qwen.py
```

The script selects the latest ClickFixMonitor Event ID `1001` from `archives.json`, sends a compact event to Qwen2.5:3B, and prints structured advisory output plus candidate Wazuh rule logic.

The current script expects:

```text
Wazuh archives: /var/ossec/logs/archives/archives.json
Ollama API:     http://10.0.2.7:11434/api/generate
Victim IP:      10.0.2.15
Event ID:       1001
Provider:       ClickFixMonitor
```

Change these constants if your lab addresses differ.

## 10. Validate before deploying AI-suggested rules

The LLM is advisory only. Do not automatically deploy generated rules.

Use this sequence:

```text
Event evidence
  -> Qwen advisory analysis
  -> analyst review
  -> wazuh-logtest
  -> syntax validation
  -> controlled deployment
```

## 11. MITRE ATT&CK mapping used by this repository

| Technique ID | Technique Name |
|---|---|
| `T1204.004` | User Execution: Malicious Copy and Paste |

The repository intentionally keeps the public project mapping focused on this primary ClickFix technique.

## 12. Recommended reproduction order

1. Build the three VMs.
2. Install and verify Wazuh.
3. Install the Windows agent and telemetry sources.
4. Build and start ClickFixMonitor.
5. Generate a harmless Event ID 1001 test.
6. Confirm the event appears in `archives.json`.
7. Add and validate the custom Wazuh rules.
8. Confirm the alert appears in `alerts.json`.
9. Start Ollama/Qwen on the AI VM.
10. Run `event1001_to_qwen.py`.
11. Review the AI output manually.
12. Record screenshots/results for the experiment.

## Safety and scope

Use only authorized isolated systems. The repository is intended to reproduce detection and analysis behavior, not to distribute or execute real malicious payloads. Use harmless test strings for validation.