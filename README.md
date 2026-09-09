# Detection of Emerging Phishing Campaign Techniques using Wazuh SIEM

## Project Workflow: ClickFix Detection and LLM-Assisted Rule Engineering

This project demonstrates an AI-assisted detection engineering workflow for Win+R based ClickFix attacks using ClickFixMonitor, Wazuh SIEM, and a local LLM (Qwen2.5:3B via Ollama).

The project report describes a two-phase approach: baseline Wazuh detection and customized detection using a pre-execution monitor, Event ID 1001, local LLM assistance, and validated custom Wazuh rules. fileciteturn37file0L86-L94

---

# End-to-End Workflow

```text
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

LLM output is advisory only. Rules are manually reviewed and validated before deployment. fileciteturn37file0L100-L103

---

# Laboratory Environment

| System | IP | Purpose |
|---|---|---|
| Windows 11 Victim | 10.0.2.15 | Sysmon, PowerShell Logging, Defender, ClickFixMonitor |
| Ubuntu Wazuh Server | 10.0.2.6 | Wazuh Manager, Indexer, Dashboard |
| Ubuntu AI Server | 10.0.2.7 | Ollama + Qwen2.5:3B |

---

# Evidence Screenshots Flow

## 01_Lab_Environment

Folder:

```text
Screenshots/01_Lab_Environment/
```

Evidence:

![VirtualBox Lab](Screenshots/01_Lab_Environment/virtualbox.png)

Shows the three isolated virtual machines used in the project.

---

## 02_ClickFixMonitor

Folder:

```text
Screenshots/02_ClickFixMonitor/
```

Workflow:

```text
User opens Run Dialog
        ↓
Suspicious command pasted
        ↓
ClickFixMonitor detects indicators
        ↓
Application Event ID 1001 created
```

Evidence:

[ClickFix Page](../Screenshots/02_ClickFixMonitor/01_fake_cloudflare_page.png.png)

![User Interaction](../Screenshots/02_ClickFixMonitor/02_clickfix_instruction_page.png.png)

![Run Dialog](../Screenshots/02_ClickFixMonitor/03_run_dialog_paste.png.png)

![ClickFixMonitor Event ID 1001](../Screenshots/02_ClickFixMonitor/clickfix_monitor_1001.png.png)

![ClickFixMonitor Event ID 1001 - Part 1](../Screenshots/02_ClickFixMonitor/clickfix_monitor_1001_1.png.png)

![ClickFixMonitor Event ID 1001 - Part 2](../Screenshots/02_ClickFixMonitor/clickfix_monitor_1001_2.png.png)

**Result:** ClickFixMonitor successfully generated Windows Application Event ID 1001 telemetry.
---

## 03_Wazuh

Folder:

```text
Screenshots/03_Wazuh/
```

Commands used:

### Check Wazuh Manager

```bash
sudo systemctl status wazuh-manager
```

### Verify Event ID 1001 in archives

```bash
sudo grep -i ClickFixMonitor /var/ossec/logs/archives/archives.json | tail -20
```

Evidence:

![Wazuh Event Collection](Screenshots/03_Wazuh/wazuh_event.png)

---

# 04_LLM_Analysis

Folder:

```text
Screenshots/04_LLM_Analysis/
```

The latest ClickFix Event ID 1001 is sent to Qwen2.5:3B for analysis.

Command:

```bash
sudo python3 ~/wazuh-ai/event1001_to_qwen.py
```

LLM provides:

- Verdict
- Confidence
- Risk level
- Observed indicators
- Detection gap
- Candidate Wazuh rule logic

Evidence:

![LLM Analysis](Screenshots/04_LLM_Analysis/qwen_analysis.png)

---

# 05_Detection_Result

Folder:

```text
Screenshots/05_Detection_Result/
```

Final validated Wazuh rules:

```text
Rule 100100 → Base Event ID 1001 Detection
Rule 100101 → High Risk ClickFix Detection
Rule 100102 → Strong PowerShell Indicator Detection
```

Validate rules:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Restart manager after deployment:

```bash
sudo systemctl restart wazuh-manager
```

Check alerts:

```bash
sudo grep -E '100100|100101|100102' /var/ossec/logs/alerts/alerts.json | tail -20
```

Evidence:

![Final Alert](Screenshots/05_Detection_Result/final_alert.png)

---

# Local LLM Pipeline

```text
archives.json
      ↓
Event Collector Script
      ↓
Ollama API
      ↓
Qwen2.5:3B
      ↓
Rule Suggestion
      ↓
Human Validation
      ↓
Wazuh Custom Rule
```

---

# MITRE ATT&CK Mapping

| Technique ID | Technique |
|---|---|
| T1204.004 | User Execution: Malicious Copy and Paste |

Additional observed behaviors:

| Technique | Usage |
|---|---|
| T1059.001 | PowerShell execution |
| T1105 | Ingress Tool Transfer |
| T1027 | Obfuscated Files or Information |

---

# Reproduction Order

1. Setup VirtualBox laboratory.
2. Install Wazuh Manager.
3. Install Windows Sysmon and Wazuh Agent.
4. Run ClickFixMonitor.
5. Generate Event ID 1001.
6. Verify event in Wazuh archives.
7. Send event to local Qwen model.
8. Review AI-generated rule suggestion.
9. Validate with wazuh-logtest.
10. Deploy custom Wazuh rules.
11. Confirm dashboard alert.

---

# Detection Summary

| Component | Result |
|---|---|
| ClickFixMonitor | Event ID 1001 generated |
| Wazuh Agent | Event collected |
| Local LLM | Rule suggestion generated |
| Human Validation | Completed |
| Wazuh Rule | Alert triggered |

# Repository Structure

```text
.
├── ClickFixMonitor/
├── Wazuh/
├── LLM/
├── Screenshots/
│   ├── 01_Lab_Environment
│   ├── 02_ClickFixMonitor
│   ├── 03_Wazuh
│   ├── 04_LLM_Analysis
│   └── 05_Detection_Result
└── Documentation/
```

---

# Safety Scope

This repository is for authorized cybersecurity research, detection engineering, and controlled laboratory validation only.
