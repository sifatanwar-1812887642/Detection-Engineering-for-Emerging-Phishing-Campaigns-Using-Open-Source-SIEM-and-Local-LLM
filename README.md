# Detection Engineering for Emerging Phishing Campaigns Using Open-Source SIEM and Local LLM

A controlled-laboratory research project for detecting ClickFix-style social engineering attacks at the Windows Run-dialog pre-execution stage using Wazuh, a custom Windows UI Automation monitor, and a locally hosted Qwen2.5:3B model through Ollama.

## Research focus

ClickFix attacks can persuade a user to copy attacker-controlled text and paste it into **Win+R**. Conventional endpoint telemetry may appear only after execution. This project adds a dedicated pre-execution event so the suspicious Run-dialog content can reach Wazuh before the user presses Enter.

**MITRE ATT&CK:** T1204.004 — Malicious File / User Execution: Malicious Copy and Paste.

## Architecture

```text
Windows Run Dialog
        |
        v
ClickFixMonitor (UI Automation)
        |
        | Event ID 1001
        v
Wazuh Agent -> Wazuh Manager -> archives.json
        |
        v
 event1001_to_qwen.py
        |
        v
Ollama API -> Qwen2.5:3B
        |
        v
AI-assisted candidate detection logic
        |
        v
Analyst review -> Wazuh rules -> alerts.json
```

The LLM is advisory: generated rule logic is reviewed, tested with `wazuh-logtest`, syntax-validated, and then deployed manually.

## Laboratory components

- Windows 11 victim endpoint
- Kali Linux attacker/simulation VM
- Ubuntu Wazuh server
- Wazuh 4.14.5
- Sysmon 15.20
- Microsoft Defender
- Ollama 0.31.2
- Qwen2.5:3B
- .NET 8 `ClickFixMonitor`
- Python 3 + `requests`
- VirtualBox NAT / segmented laboratory network

# Wazuh SIEM Setup and Agent Configuration

## Environment

| Component | IP Address | Purpose |
|---|---|---|
| Windows 11 Victim | 10.0.2.15 | Sysmon + Wazuh Agent + ClickFixMonitor |
| Wazuh Manager | 10.0.2.6 | SIEM, log collection, detection rules |
| AI VM | 10.0.2.7 | Ollama + Qwen2.5:3B |

## 1. Wazuh Manager Installation

The Wazuh Manager was installed on Ubuntu Server.

```bash
sudo apt update
sudo apt upgrade -y
curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh
sudo bash wazuh-install.sh -a
```

Verify services:

```bash
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
```

## 2. Enable Wazuh Archive Logging

Raw JSON event collection was enabled for AI analysis.

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add:

```xml
<logall_json>yes</logall_json>
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

Raw events are stored in:

```text
/var/ossec/logs/archives/archives.json
```

## 3. Windows Wazuh Agent Installation

Install Wazuh Agent on Windows 11 victim:

```powershell
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="10.0.2.6"
```

Register the agent from Wazuh Manager:

```bash
sudo /var/ossec/bin/manage_agents
```

Import the generated key into:

```text
C:\Program Files (x86)\ossec-agent\manage_agents.exe
```

## 4. Windows Agent Configuration

Edit:

```text
C:\Program Files (x86)\ossec-agent\ossec.conf
```

Configure Manager:

```xml
<client>
  <server>
    <address>10.0.2.6</address>
  </server>
</client>
```

## 5. Sysmon and PowerShell Log Collection

Sysmon events:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

PowerShell events:

```xml
<localfile>
  <location>Microsoft-Windows-PowerShell/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

## 6. ClickFix Monitor Log Integration

The ClickFixMonitor generates JSON events:

```text
C:\ClickFixMonitor\clipboard_events.json
```

Wazuh Agent collects the log using:

```xml
<localfile>
  <location>C:\ClickFixMonitor\clipboard_events.json</location>
  <log_format>json</log_format>
  <label key="@source">clickfix_clipboard_monitor</label>
</localfile>
```

## 7. Restart Agent and Verify Connection

Restart:

```powershell
Restart-Service wazuh
```

Verify from Manager:

```bash
sudo /var/ossec/bin/agent_control -lc
```

Verify incoming logs:

```bash
sudo tail -f /var/ossec/logs/archives/archives.json
```

## Repository structure

```text
.
├── README.md
├── ClickFixMonitor/
│   ├── ClickFixMonitor.csproj
│   └── Program.cs
├── Wazuh/
│   └── local_rules.xml
├── LLM/
│   ├── event1001_to_qwen.py
│   └── requirements.txt
└── Documentation/
```

## Pre-execution event

The monitor writes Windows Application Event ID `1001` with provider `ClickFixMonitor`.

## Final Wazuh hierarchy

- `100100` — base ClickFixMonitor Event ID 1001 detection
- `100101` — HIGH-risk ClickFix pre-execution activity
- `100102` — strong ClickFix pre-execution indicator condition

## Safety / research scope

All simulations are intended for an isolated laboratory. Do not deploy the monitor or detection rules on systems you do not own or administer.
