# Detection Engineering for Emerging Phishing Campaigns Using Open-Source SIEM and Local LLM

> **Academic cybersecurity research project focused on detecting ClickFix-style emerging phishing activity through pre-execution endpoint telemetry, Wazuh SIEM, and a privacy-preserving local LLM workflow.**

## Project Overview

Phishing campaigns continue to evolve beyond traditional malicious links and email attachments. **Emerging phishing techniques** increasingly rely on social engineering to persuade users to perform actions themselves, making malicious activity harder to distinguish from legitimate user behavior.

This project investigates **ClickFix** as a representative emerging phishing technique. In a typical ClickFix scenario, a victim is presented with a fake verification, CAPTCHA, browser, or system-related prompt and is instructed to copy and paste attacker-controlled content into a trusted Windows interface such as the **Run dialog (Win+R)**.

The key research challenge is the **pre-execution detection gap**: the suspicious command may already be present in the clipboard or Run dialog before the user presses Enter, while conventional endpoint telemetry may focus more heavily on activity after execution.

To address this gap, the project develops an end-to-end detection-engineering workflow that connects:

**ClickFix Activity → Pre-Execution Detection → Windows Event ID 1001 → Wazuh → Local LLM Analysis → Human Validation → Custom Wazuh Alert**

The local AI component uses **Qwen2.5:3B through Ollama**. The LLM acts as an analyst-assistance layer; final detection logic is reviewed and validated before deployment.

---

## Research Scope

The broader research context is **emerging phishing campaigns**, while the implementation focuses specifically on **ClickFix**.

```text
Emerging Phishing Campaigns
            │
            ├── Multiple Emerging Techniques
            │
            └── ClickFix
                  │
                  ├── Social Engineering
                  │
                  ├── Malicious Copy/Paste
                  │
                  └── Win+R User Execution
                           │
                           ▼
                  Pre-Execution Detection
                           │
                           ▼
                    Wazuh + Local LLM
```

### Primary Research Focus

**Emerging phishing → ClickFix → Win+R malicious copy/paste → pre-execution telemetry → Wazuh detection → local LLM-assisted detection engineering**

Other emerging phishing variants are treated as broader threat context rather than separate implementations of this project.

---

## Why ClickFix Matters

ClickFix creates a detection challenge because it abuses **human interaction with trusted system interfaces** rather than relying only on a conventional malicious executable or clearly suspicious URL.

Key security concerns include:

- **Social engineering** — the victim is persuaded to perform the malicious action.
- **Trusted interface abuse** — legitimate Windows interfaces can become the execution point.
- **Pre-execution visibility gap** — the suspicious command can be observable before execution.
- **Potential fileless behavior** — commands may execute through interpreters such as PowerShell without an obvious dropped executable at the initial stage.
- **Flexible payload delivery** — attacker-controlled commands can be changed for different objectives.
- **Downstream impact** — successful execution can lead to credential theft, malware deployment, persistence, data theft, or further compromise depending on the payload.

This project therefore focuses on detecting suspicious command activity **before execution**, generating dedicated telemetry, and integrating that telemetry into the SIEM and local LLM workflow.

---

## Project Objectives

1. Investigate ClickFix as an emerging phishing technique.
2. Identify the pre-execution visibility gap associated with Win+R copy/paste activity.
3. Develop a custom endpoint monitor for suspicious Run-dialog activity.
4. Generate structured **Windows Application Event ID 1001** telemetry.
5. Integrate the telemetry with **Wazuh Agent and Wazuh Manager**.
6. Use a local **Qwen2.5:3B** model to assist detection engineering.
7. Validate AI-suggested detection logic through human review.
8. Implement deterministic custom Wazuh rules for alert generation.

---

## What Was Developed

| Component | Implementation |
|---|---|
| ClickFix Monitor | Custom .NET 8 WPF application for pre-execution Run-dialog monitoring |
| Endpoint Telemetry | Windows Application Event ID 1001 |
| SIEM | Wazuh 4.14.5 |
| Endpoint Agent | Wazuh Agent on Windows 11 |
| System Telemetry | Sysmon 15.20 + PowerShell logging |
| Local AI | Ollama + Qwen2.5:3B |
| AI Integration | Event 1001 filtering and local LLM analysis |
| Detection Logic | Custom Wazuh rules 100100, 100101, and 100102 |
| Validation | Windows Event Viewer, Wazuh archives, wazuh-logtest, and Wazuh alerts |

---

## ClickFixMonitor

**ClickFixMonitor** is the custom endpoint component developed for this project to identify suspicious ClickFix-style activity in the Windows **Run dialog (Win+R)** before the command is executed.

### Implementation

- **Technology:** .NET 8 / WPF
- **Purpose:** Pre-execution detection of suspicious Run-dialog activity
- **Target:** Windows Run dialog (Win+R)
- **Detection Stage:** Before command execution
- **Windows Telemetry:** Application Event ID **1001**
- **Event Provider:** **ClickFixMonitor**
- **SIEM Integration:** Event 1001 → Wazuh Agent → Wazuh Manager

### Event 1001 Telemetry

When suspicious Run-dialog content is detected, ClickFixMonitor generates a structured Windows Application event containing relevant detection information, including:

- Suspicious command line
- Matched indicators
- Risk level
- Detection stage
- Timestamp
- Hostname and username
- SHA256 value

### Example

A controlled test using a PowerShell-based command can generate an Event ID 1001 similar to:

```text
Command Line: powershell -nop -w hidden -c whoami
Risk: HIGH
Detection Stage: Pre-Execution
Event ID: 1001
Provider: ClickFixMonitor
```

The generated Event ID 1001 is then collected by the Wazuh Agent and processed by the Wazuh Manager for subsequent detection engineering and alerting.

---

## Project Workflow

The complete project workflow is:

```text
Emerging Phishing Campaign
              ↓
        ClickFix Technique
              ↓
   Social Engineering Prompt
              ↓
    Win+R → Ctrl+V → Enter
              ↓
     ClickFixMonitor detects
       before execution
              ↓
 Windows Application Event 1001
              ↓
        Wazuh Agent
              ↓
       Wazuh Manager
              ↓
   Event 1001 Log Collection
              ↓
 Local LLM (Qwen2.5:3B + Ollama)
              ↓
   Detection Analysis / Rule
          Suggestion
              ↓
      Human Validation
              ↓
    Custom Wazuh Rule
              ↓
       Wazuh Alert
              ↓
          Response
```

### Core Workflow

**Attack → Log Generation → Detection → Alert → Analysis → Response**

This workflow represents the complete detection-engineering lifecycle implemented in the project.

---

## End-to-End Architecture

```text
                    EMERGING PHISHING
                           │
                           ▼
                      CLICKFIX
                           │
                           ▼
              Social Engineering Prompt
                           │
                           ▼
                 Windows Run Dialog
                      (Win + R)
                           │
                           ▼
                  ┌─────────────────┐
                  │ ClickFixMonitor │
                  └────────┬────────┘
                           │
                           ▼
                 Windows Event ID 1001
                           │
                           ▼
                     Wazuh Agent
                           │
                           ▼
                    Wazuh Manager
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Custom Wazuh Rules       Local LLM Analysis
              │                  Qwen2.5:3B
              │                  via Ollama
              │                         │
              │                         ▼
              │                  Candidate Logic
              │                         │
              └────────────┬────────────┘
                           ▼
                    Human Validation
                           │
                           ▼
                    Wazuh Alert
```

**Important:** The LLM does not automatically modify Wazuh configuration. AI output is advisory and is reviewed before rule deployment.

---

## Laboratory Environment

| System | IP Address | Purpose |
|---|---|---|
| Windows 11 Victim / Wazuh Agent | 10.0.2.15 | Sysmon, PowerShell Logging, Microsoft Defender, ClickFixMonitor |
| Ubuntu Wazuh Server | 10.0.2.6 | Wazuh Manager, Indexer, Dashboard |
| Ubuntu AI Server | 10.0.2.7 | Ollama + Qwen2.5:3B |

**Virtualization:** VirtualBox NAT Network  
**Wazuh:** 4.14.5  
**Sysmon:** 15.20  
**Ollama:** 0.31.2  
**LLM:** Qwen2.5:3B

---

## Detection Methodology

The detection pipeline follows:

```text
1. ClickFix Paste Activity
          ↓
2. ClickFixMonitor detects suspicious Run-dialog content
          ↓
3. Windows Application Event ID 1001 is generated
          ↓
4. Wazuh Agent forwards the event
          ↓
5. Wazuh Manager collects and processes the telemetry
          ↓
6. Event 1001 is supplied to local Qwen2.5:3B
          ↓
7. Candidate detection logic is generated
          ↓
8. Human reviews the recommendation
          ↓
9. Validated Wazuh rules are deployed
          ↓
10. Wazuh generates the detection alert
```

This separation keeps the AI component advisory while maintaining deterministic and reviewable SIEM detection logic.

---

## AI-Assisted Detection Engineering

Relevant Event ID 1001 telemetry is read from the Wazuh archives and supplied to the local Ollama API.

```text
Wazuh archives.json
        ↓
Event 1001 Filter
        ↓
event1001_to_qwen.py
        ↓
Ollama API
        ↓
Qwen2.5:3B
        ↓
Verdict / Confidence / Risk
        ↓
Observed Indicators
        ↓
Candidate Wazuh Detection Logic
        ↓
Human Validation
```

The current AI workflow is intentionally focused on **Event ID 1001**. The model supports analysis and rule development but does not replace analyst validation.

---

## Final Wazuh Detection Chain

The validated detection logic uses a three-rule chain:

```text
Event ID 1001
     ↓
100100 — Base ClickFixMonitor Event Detection
     ↓
100101 — HIGH Risk ClickFix Detection
     ↓
100102 — PowerShell Indicator Detection
     ↓
Wazuh Level 15 Alert
```

### Custom Rule Summary

| Rule ID | Condition / Purpose | Level |
|---|---|---:|
| 100100 | Detect ClickFixMonitor Event ID 1001 | 5 |
| 100101 | Identify HIGH-risk ClickFix telemetry | 15 |
| 100102 | Identify PowerShell indicator within the event | 15 |

### Rule Validation

Test the detection logic with:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Restart the Wazuh manager after rule deployment:

```bash
sudo systemctl restart wazuh-manager
```

Verify generated alerts:

```bash
sudo grep -E '100100|100101|100102' /var/ossec/logs/alerts/alerts.json | tail -20
```

---

## MITRE ATT&CK Mapping

### Primary Technique

| Technique ID | Technique |
|---|---|
| **T1204.004** | User Execution: Malicious Copy and Paste |

### Supporting Behaviors

| Technique ID | Technique | Context |
|---|---|---|
| T1059.001 | Command and Scripting Interpreter: PowerShell | PowerShell execution observed in the ClickFix command |
| T1105 | Ingress Tool Transfer | Relevant to payload-transfer behavior in ClickFix campaigns |
| T1027 | Obfuscated Files or Information | Relevant when encoded or obfuscated commands are used |

The core research focus remains **T1204.004**, while the supporting techniques provide context for related behavior.

---

## Reproduction Workflow

1. Set up the VirtualBox laboratory.
2. Configure the Wazuh Manager.
3. Install Sysmon and Wazuh Agent on Windows 11.
4. Deploy and run ClickFixMonitor.
5. Perform a controlled Win+R ClickFix simulation.
6. Verify Windows Application Event ID 1001.
7. Verify Event ID 1001 in Wazuh archives.
8. Run the local Qwen analysis workflow.
9. Review the AI-generated detection recommendation.
10. Validate the logic using `wazuh-logtest`.
11. Deploy the validated custom Wazuh rules.
12. Confirm the resulting Wazuh alert.

---

## Validation

Validation is performed across multiple layers:

- **Endpoint:** ClickFixMonitor generates Event ID 1001.
- **Windows telemetry:** Event details are visible in Event Viewer.
- **SIEM:** Wazuh receives and processes the event.
- **AI:** Qwen2.5:3B analyzes the structured event.
- **Detection logic:** Custom rules are tested with `wazuh-logtest`.
- **Alerting:** Wazuh generates the expected custom alert.

Supporting screenshots and evidence are maintained in the repository.

---

## Repository Structure

```text
.
├── ClickFixMonitor/
├── Wazuh/
├── LLM/
├── Screenshots/
│   ├── 01_Lab_Environment/
│   ├── 02_ClickFixMonitor/
│   ├── 03_Wazuh/
│   ├── 04_LLM_Analysis/
│   └── 05_Detection_Result/
└── Documentation/
```

---

## Research Limitations

- Experiments were conducted in a controlled laboratory environment.
- The current implementation focuses specifically on **Win+R ClickFix activity and Event ID 1001**.
- The local LLM uses a relatively small 3B-parameter model.
- LLM output is advisory and requires human validation.
- Supporting MITRE techniques describe related behavior and are not the primary research target.
- Results from this implementation should not be interpreted as universal detection performance across all ClickFix variants.

---

## Safety and Ethical Scope

This repository is intended for authorized cybersecurity research, detection engineering, academic study, and controlled laboratory validation only.

Do not use the techniques or tooling against systems without explicit authorization.

---

## Academic Context

**University of Dhaka**  
**Professional Masters in Information and Cyber Security (PMICS)**  
**Batch IV**

### Research Project

**Detection Engineering for Emerging Phishing Campaigns Using Open-Source SIEM and Local LLM**

### Researcher

**Sifat Anwar**  
Registration No.: **H-400**

### Project Supervisor

**Mr. Md. Samiul Islam**  
Co-Instructor, PMICS Program  
Department of Computer Science and Engineering  
University of Dhaka
