# Detection Engineering for Emerging Phishing Campaigns Using Open-Source SIEM and Local LLM

## Project Overview

Phishing continues to evolve beyond traditional malicious links and email attachments. **Emerging phishing campaigns** increasingly use social engineering techniques that persuade users to perform actions themselves, making malicious activity harder to distinguish from legitimate user behavior.

One such emerging technique is **ClickFix**, which is the specific technique investigated in this project. ClickFix-style campaigns typically present a fake verification, CAPTCHA, browser, or system-related prompt and instruct the victim to copy and paste attacker-provided content into a trusted Windows interface such as the **Run dialog (Win+R)**. The user is then manipulated into executing the pasted command.

This behavior is particularly important from a detection-engineering perspective because the malicious command may initially appear as a user-generated action. Conventional endpoint telemetry may also provide limited visibility into the **pre-execution copy-paste stage**, creating a detection gap.

ClickFix is harmful because successful campaigns can lead to command execution, payload delivery, credential theft, malware deployment, persistence, and further compromise depending on the command and subsequent attack chain. The technique has been observed as part of broader phishing and social-engineering activity affecting organizations and end users in different regions, demonstrating why emerging user-driven execution techniques deserve dedicated detection research.

Therefore, this research does **not** attempt to cover every phishing technique. Instead, it uses ClickFix as a representative emerging phishing technique and develops a focused detection-engineering workflow around it.

The research follows a two-phase approach:

1. **Baseline detection:** evaluate what standard Wazuh telemetry and default detection capabilities can identify from controlled ClickFix activity.
2. **Customized detection engineering:** introduce a pre-execution monitor, generate **Windows Application Event ID 1001**, use a local LLM for detection-rule analysis, and validate custom Wazuh rules.

The local AI component uses **Qwen2.5:3B through Ollama**. The LLM is used as an analyst-assistance mechanism; final detection rules are reviewed and validated before deployment.

---

## Emerging Phishing → ClickFix Research Scope

The research scope can be understood as a hierarchy:

```text
Emerging Phishing Campaigns
            |
            +-------------------+
            |                   |
     Multiple Emerging     ClickFix Technique
       Techniques               |
                                +----------------------+
                                |                      |
                         Social Engineering      User-Driven Execution
                                                       |
                                                       v
                                          Win+R Copy/Paste Activity
                                                       |
                                                       v
                                           Pre-Execution Detection
```

**Research focus:** Emerging phishing campaigns → **ClickFix technique** → Win+R malicious copy/paste → pre-execution telemetry → Wazuh detection → local LLM-assisted detection engineering.

Other emerging phishing variants may use different delivery or execution mechanisms. They are treated as broader threat context rather than as separate implementations of this project.

---

## Why ClickFix Matters

ClickFix represents an important detection challenge because it abuses **human interaction with trusted system interfaces** rather than relying only on a conventional malicious executable or a clearly suspicious URL.

Key security concerns include:

- **Social engineering:** the victim is persuaded to perform the malicious action.
- **Trusted interface abuse:** Windows Run and other legitimate interfaces can be used as the execution point.
- **Pre-execution visibility gap:** the malicious command can exist in the clipboard or Run dialog before execution, while conventional monitoring may focus more heavily on process or execution events.
- **Potential fileless behavior:** some ClickFix payloads can execute commands directly through interpreters such as PowerShell without requiring an obvious dropped executable at the initial stage.
- **Flexible payload delivery:** the pasted command can be changed by the attacker to support different objectives.
- **High downstream impact:** depending on the payload, successful execution may lead to credential theft, malware installation, persistence, data theft, or additional compromise.

For this reason, the project focuses on detecting the suspicious command **before execution**, producing dedicated telemetry, and feeding that telemetry into the SIEM and local LLM analysis workflow.

---

## Research Contribution

The project addresses a detection gap associated with emerging ClickFix-style phishing techniques by connecting endpoint-level pre-execution telemetry with Wazuh and a privacy-preserving local LLM.

Key contributions:

- Treats **ClickFix as a specific emerging phishing technique** within the broader emerging-phishing landscape.
- Pre-execution detection of suspicious Run-dialog paste activity using **ClickFixMonitor**.
- Generation of structured **Windows Application Event ID 1001** telemetry.
- Centralized collection through **Wazuh Agent and Wazuh Manager**.
- Local LLM-assisted analysis using **Qwen2.5:3B**.
- Human validation of AI-suggested detection logic.
- Deployment of validated custom Wazuh rules for alert generation.

---

# End-to-End Workflow

```text
Emerging Phishing Campaign
        ↓
ClickFix Technique
        ↓
Social Engineering / Malicious Copy-Paste
        ↓
Windows Run Dialog (Win+R)
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

**Important:** LLM output is advisory only. Rules are manually reviewed and validated before deployment.

---

# Laboratory Environment

| System | IP Address | Purpose |
|---|---|---|
| Windows 11 Victim / Wazuh Agent | 10.0.2.15 | Sysmon, PowerShell Logging, Microsoft Defender, ClickFixMonitor |
| Ubuntu Wazuh Server | 10.0.2.6 | Wazuh Manager, Indexer, Dashboard |
| Ubuntu AI Server | 10.0.2.7 | Ollama + Qwen2.5:3B |

**Virtualization:** VirtualBox NAT Network  
**Wazuh Version:** 4.14.5  
**Sysmon Version:** 15.20  
**Ollama Version:** 0.31.2  
**LLM:** Qwen2.5:3B

---

# Detection Methodology

The detection pipeline is designed around the following sequence:

```text
ClickFix Paste
     ↓
ClickFixMonitor captures suspicious Run-dialog activity
     ↓
Windows Application Event ID 1001
     ↓
Wazuh Agent forwards event
     ↓
Wazuh Manager stores and processes telemetry
     ↓
Event 1001 is supplied to local Qwen2.5:3B
     ↓
Candidate detection logic is generated
     ↓
Human reviews the recommendation
     ↓
Validated Wazuh rule is deployed
     ↓
Wazuh alert is generated
```

The AI stage is intentionally separated from final rule deployment so that an LLM-generated recommendation cannot automatically modify the SIEM configuration.

---

# Baseline Detection Results

The controlled baseline evaluation produced the following results. These values are retained as the project's baseline result.

| Metric | Result |
|---|---:|
| Controlled ClickFix simulations | 3 |
| Applicable observations | 28 |
| Strictly detected | 10 |
| Partially detected | 2 |
| Missed | 16 |
| Strict detection rate | 35.7% |
| Miss rate | 57.1% |
| Weighted coverage | 39.3% |

These baseline results establish the detection gap that motivates the customized detection engineering phase.

---

# AI-Assisted Detection Engineering

The Wazuh manager reads relevant Event ID 1001 telemetry from the Wazuh archives and sends the structured event to the local Ollama API.

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

The LLM is restricted to the Event ID 1001 analysis workflow for this project. Its output supports detection engineering but does not replace deterministic validation.

---

# Final Wazuh Detection Chain

The validated custom detection logic uses a three-rule chain:

```text
Event ID 1001
     ↓
Rule 100100 — Base ClickFixMonitor Event Detection
     ↓
Rule 100101 — HIGH Risk ClickFix Detection
     ↓
Rule 100102 — PowerShell Indicator Detection
     ↓
Wazuh Level 15 Alert
```

### Rule Summary

| Rule ID | Purpose | Level |
|---|---|---:|
| 100100 | Detect ClickFixMonitor Event ID 1001 | 5 |
| 100101 | Identify HIGH-risk ClickFix telemetry | 15 |
| 100102 | Identify PowerShell indicator within the event | 15 |

Rules can be validated using:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

After deployment:

```bash
sudo systemctl restart wazuh-manager
```

To verify generated alerts:

```bash
sudo grep -E '100100|100101|100102' /var/ossec/logs/alerts/alerts.json | tail -20
```

---

# MITRE ATT&CK Mapping

### Primary Technique

| Technique ID | Technique |
|---|---|
| T1204.004 | User Execution: Malicious Copy and Paste |

### Supporting Observed Behaviors

| Technique ID | Technique | Context |
|---|---|---|
| T1059.001 | Command and Scripting Interpreter: PowerShell | PowerShell execution observed in the ClickFix command |
| T1105 | Ingress Tool Transfer | Relevant to payload-transfer behavior in ClickFix campaigns |
| T1027 | Obfuscated Files or Information | Relevant when encoded/obfuscated commands are used |

The research focus remains **T1204.004**, while the supporting techniques provide context for related post-paste behavior.

---

# Reproduction Order

1. Set up the VirtualBox laboratory.
2. Install and configure Wazuh Manager.
3. Install Sysmon and Wazuh Agent on Windows 11.
4. Deploy and run ClickFixMonitor.
5. Perform a controlled Win+R ClickFix simulation.
6. Verify Windows Application Event ID 1001.
7. Verify Event ID 1001 in Wazuh archives.
8. Run the local Qwen analysis script.
9. Review the AI-generated detection recommendation.
10. Validate the detection logic using `wazuh-logtest`.
11. Deploy the validated custom Wazuh rules.
12. Confirm the resulting Wazuh alert.

---

# Validation

Validation is performed at multiple stages:

- **Endpoint validation:** Event ID 1001 is generated by ClickFixMonitor.
- **SIEM validation:** Wazuh receives and stores the event.
- **AI validation:** Qwen2.5:3B analyzes the structured event and produces candidate detection logic.
- **Rule validation:** Custom rules are tested with `wazuh-logtest`.
- **Alert validation:** Wazuh generates the expected custom alert.

Screenshots and supporting evidence are maintained separately in the repository's `Screenshots/` directory and are not embedded in this README.

---

# Repository Structure

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

# Research Limitations

- The experiments were conducted in a controlled laboratory environment.
- The baseline evaluation uses a limited number of controlled simulations.
- The local LLM component uses a relatively small 3B-parameter model.
- LLM output is advisory and requires human validation.
- The current implementation focuses specifically on **Win+R ClickFix activity and Event ID 1001**.
- Results should not be interpreted as universal detection performance across all ClickFix variants.

---

# Safety and Ethical Scope

This repository is intended for authorized cybersecurity research, detection engineering, academic study, and controlled laboratory validation only.

Do not use the techniques or tooling against systems without explicit authorization.

---

# Academic Context

**University of Dhaka**  
**Professional Masters in Information and Cyber Security (PMICS)**  
**Batch III**

**Research Project:**  
Detection Engineering for Emerging Phishing Campaigns Using Open-Source SIEM and Local LLM

### Researcher

**Sifat Anwar**  
**Registration No.: H-400**

### Project Supervisor

**Mr. Md. Samiul Islam**  
Co-Instructor, PMICS Program  
Department of Computer Science and Engineering  
University of Dhaka
