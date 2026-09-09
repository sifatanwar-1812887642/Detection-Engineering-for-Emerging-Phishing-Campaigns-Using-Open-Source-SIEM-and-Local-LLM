# Step-by-Step Reproduction Guide

## Project: ClickFix Detection and LLM-Assisted Rule Engineering

This document explains how the complete laboratory workflow was implemented step by step.

---

# 1. Lab Environment Setup

## Virtual Machines

Three isolated virtual machines were prepared:

- Windows 11 Victim VM
- Ubuntu Wazuh SIEM VM (10.0.2.6)
- Ubuntu AI/LLM VM

Evidence:

```
Screenshots/01_Lab_Environment/
```

---

# 2. Wazuh Manager Deployment

## Install Wazuh All-in-One Stack

Update Ubuntu system:

```bash
sudo apt update && sudo apt upgrade -y
```

Download installer:

```bash
curl -sO https://packages.wazuh.com/4.15/wazuh-install.sh
```

Install Wazuh Manager, Indexer and Dashboard:

```bash
sudo bash ./wazuh-install.sh -a
```

Verify service:

```bash
sudo systemctl status wazuh-manager
```

Evidence:

```
Screenshots/03_Wazuh/
```

---

# 3. Windows Telemetry Setup

## Install Sysmon

Install Sysmon with Wazuh configuration:

```powershell
cd C:\Sysmon
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

Verify events:

```
Event Viewer
 -> Applications and Services Logs
 -> Microsoft
 -> Windows
 -> Sysmon
 -> Operational
```

---

# 4. ClickFix Attack Simulation

Attack flow:

```
ClickFix Fake Verification Page
            ↓
User Copy/Paste Interaction
            ↓
Windows Run Dialog
            ↓
ClickFixMonitor Detection
            ↓
Event ID 1001 Generated
```

Evidence:

```
Screenshots/02_ClickFixMonitor/
```

---

# 5. Wazuh Event Collection

ClickFixMonitor creates Windows Application Event ID 1001.

Wazuh Agent collects the event and forwards it to Wazuh Manager.

Check agent status:

```bash
sudo /var/ossec/bin/agent_control -l
```

Check event logs:

```bash
sudo grep -i ClickFixMonitor /var/ossec/logs/archives/archives.json | tail -20
```

---

# 6. Local LLM Analysis

Event data is sent to local Qwen2.5:3B model through Ollama.

Run analysis:

```bash
sudo python3 ~/wazuh-ai/event1001_to_qwen.py
```

LLM provides:

- Verdict
- Risk level
- Suspicious indicators
- Detection logic suggestion
- Candidate Wazuh rules

Evidence:

```
Screenshots/05_LLM_Analysis/
```

---

# 7. Human Validation and Rule Engineering

Suggested rules are manually reviewed before deployment.

Example rule hierarchy:

```
100100 - Base Event ID 1001 Detection
100101 - High Risk ClickFix Activity
100102 - Strong PowerShell Indicator Detection
```

---

# 8. Final Wazuh Rule Deployment

Validate rule:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Restart manager:

```bash
sudo systemctl restart wazuh-manager
```

Check alerts:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

Evidence:

```
Screenshots/04_Detection_Result/
```

---

# Complete Workflow

```
ClickFix Attack Initiation
        ↓
User Copy/Paste Interaction
        ↓
ClickFixMonitor
        ↓
Windows Application Event ID 1001
        ↓
Wazuh Agent
        ↓
Wazuh Manager Event Collection
        ↓
Local LLM (Qwen2.5:3B via Ollama)
        ↓
Detection Logic / Wazuh Rule Suggestion
        ↓
Human Validation
        ↓
Final Custom Wazuh Rule
        ↓
Alert Generation
```
