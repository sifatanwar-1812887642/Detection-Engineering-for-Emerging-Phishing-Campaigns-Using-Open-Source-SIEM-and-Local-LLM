# Wazuh Setup and Agent Installation Guide

This document contains the exact deployment steps and commands used for the lab environment.

## 1. Install Wazuh Manager (Ubuntu SIEM Server - 10.0.2.6)

### Update system and download installer

```bash
sudo apt update && sudo apt upgrade -y
curl -sO https://packages.wazuh.com/4.15/wazuh-install.sh
```

### Install Wazuh Manager + Indexer + Dashboard

```bash
sudo bash ./wazuh-install.sh -a
```

The installer provides the dashboard URL and admin password after completion.

### Verify services

```bash
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
```

Dashboard:

```text
https://10.0.2.6
```

---

## 2. Install Sysmon on Windows Victim

Create folder:

```text
C:\Sysmon\
```

Download Sysmon configuration:

```powershell
wget -Uri https://wazuh.com/resources/blog/emulation-of-attack-techniques-and-detection-with-wazuh/sysmonconfig.xml -OutFile "C:\Sysmon\sysmonconfig.xml"
```

Install Sysmon:

```powershell
cd C:\Sysmon
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

Verify:

```text
Event Viewer
 -> Applications and Services Logs
 -> Microsoft
 -> Windows
 -> Sysmon
 -> Operational
```

---

## 3. Install Wazuh Agent on Windows Victim

Download agent:

```powershell
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.15.4-1.msi -OutFile $env:TEMP\wazuh-agent.msi
```

Install and connect to Wazuh Manager:

```powershell
msiexec.exe /i $env:TEMP\wazuh-agent.msi /q WAZUH_MANAGER="10.0.2.6" WAZUH_REGISTRATION_SERVER="10.0.2.6" WAZUH_AGENT_NAME="DESKTOP-VICTIM"
```

Start service:

```powershell
NET START WazuhSvc
```

Verify:

```powershell
Get-Service -Name WazuhSvc
```

Manager side verification:

```bash
sudo /var/ossec/bin/agent_control -l
```

Expected:

```text
DESKTOP-VICTIM Active
```

---

## 4. Evidence Collection Flow

```text
Windows Victim
      |
      v
Sysmon + ClickFixMonitor
      |
      v
Event ID 1001
      |
      v
Wazuh Agent
      |
      v
Wazuh Manager
      |
      v
Custom Detection Rule
      |
      v
Alert Generation
```

Screenshots should be stored under:

```text
Screenshots/
├── 01_Lab_Environment
├── 02_ClickFixMonitor
├── 03_Wazuh
├── 05_LLM_Analysis
└── 04_Detection_Result
```
