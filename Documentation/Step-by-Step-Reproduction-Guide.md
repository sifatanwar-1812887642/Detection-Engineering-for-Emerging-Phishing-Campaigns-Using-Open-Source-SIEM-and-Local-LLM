# Step-by-Step Reproduction Guide

## Project: ClickFix Detection and LLM-Assisted Rule Engineering

This document explains the complete implementation workflow with commands and corresponding evidence screenshots.

---

# 1. Lab Environment Setup

## Virtual Machines

Three isolated virtual machines are prepared:

- Windows 11 Victim VM
- Ubuntu Wazuh SIEM VM (10.0.2.6)
- Ubuntu AI/LLM VM

### Evidence Screenshots

```
Screenshots/01_Lab_Environment/

01_VirtualBox_VM_Deployment.png
→ Windows 11, Wazuh Ubuntu, AI/LLM Ubuntu machines

02_Network_Configuration.png
→ VM IP configuration
```

---

# 2. Wazuh Manager Deployment

## Install Wazuh All-in-One Stack

```bash
sudo apt update && sudo apt upgrade -y

curl -sO https://packages.wazuh.com/4.15/wazuh-install.sh

sudo bash ./wazuh-install.sh -a
```

Verify service:

```bash
sudo systemctl status wazuh-manager
```

### Evidence Screenshots

```
Screenshots/03_Wazuh/

01_Wazuh_Manager_Installation.png
→ Installation process

02_Wazuh_Manager_Status.png
→ wazuh-manager active status

03_Wazuh_Dashboard.png
→ Dashboard login and access
```

---

# 3. Windows Telemetry Setup (Sysmon)

Install Sysmon:

```powershell
cd C:\Sysmon
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

Verify:

```
Event Viewer
 → Applications and Services Logs
 → Microsoft
 → Windows
 → Sysmon
 → Operational
```

### Evidence Screenshots

```
Screenshots/02_ClickFixMonitor/

01_Sysmon_Operational_Log.png
→ Sysmon telemetry generation
```

---

# 4. ClickFix Attack Simulation

Flow:

```
ClickFix Fake Verification Page
        ↓
User Copy/Paste Interaction
        ↓
Windows Run Dialog
        ↓
ClickFixMonitor Detection
        ↓
Windows Application Event ID 1001
```

### Evidence Screenshots

```
Screenshots/02_ClickFixMonitor/

02_ClickFix_Attack_Page.png
→ Fake verification page

03_User_Interaction_Run_Dialog.png
→ User copy/paste execution attempt

04_ClickFixMonitor_Detection.png
→ Monitor detects suspicious activity

05_Event_ID_1001.png
→ Windows Application event generated
```

---

# 5. Wazuh Event Collection

Check agent:

```bash
sudo /var/ossec/bin/agent_control -l
```

Check collected event:

```bash
sudo grep -i ClickFixMonitor /var/ossec/logs/archives/archives.json | tail -20
```

### Evidence Screenshots

```
Screenshots/03_Wazuh/

04_Wazuh_Agent_Active.png
→ Windows agent connected

05_Event_1001_Collected.png
→ Event ID 1001 received by Wazuh

06_Wazuh_Detection_View.png
→ Dashboard detection evidence
```

---

# 6. Local LLM Analysis (Qwen2.5:3B via Ollama)

Run analysis:

```bash
sudo python3 ~/wazuh-ai/event1001_to_qwen.py
```

LLM provides:

- Verdict
- Risk level
- Indicators
- Detection logic suggestion
- Candidate Wazuh rules

### Evidence Screenshots

```
Screenshots/04_LLM_Analysis/

01_Event_Input_to_LLM.png
→ Event sent for analysis

02_Qwen_Response.png
→ AI verdict and risk analysis

03_Wazuh_Rule_Suggestion.png
→ Generated rule recommendation
```

---

# 7. Human Validation and Rule Engineering

Suggested rules are reviewed manually.

Example:

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

Restart:

```bash
sudo systemctl restart wazuh-manager
```

Check alerts:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

### Evidence Screenshots

```
Screenshots/05_Detection_Result/

01_Custom_Rule.png
→ Final local_rules.xml

02_Rule_Validation.png
→ wazuh-logtest result

03_Final_Alert.png
→ Wazuh alert generation
```

---

# Complete Project Workflow

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
