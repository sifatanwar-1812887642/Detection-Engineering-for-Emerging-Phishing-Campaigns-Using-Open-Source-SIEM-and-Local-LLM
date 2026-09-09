# Detection of Emerging Phishing Campaign Techniques using Wazuh SIEM

## A ClickFix Case Study with Sysmon Telemetry and Local LLM-Assisted Analysis

A controlled detection-engineering research project that evaluates ClickFix visibility in Wazuh by combining a custom Windows pre-execution monitor, Wazuh SIEM detection, and analyst-reviewed local LLM assistance.

---

## Project Architecture

```text
Windows 11 Victim
(Sysmon + PowerShell Logging + Defender)
          |
          v
ClickFixMonitor
(Application Event ID 1001)
          |
          v
Wazuh Agent
          |
          v
Wazuh Manager / Dashboard
          |
          v
Local LLM (Qwen2.5:3B via Ollama)
          |
          v
Detection Logic / Rule Suggestion
          |
          v
Human Validation
          |
          v
Custom Wazuh Rule
          |
          v
Alert Generation
```

The LLM is advisory only. It does not automatically deploy rules or perform response actions.

---

## Laboratory Environment

| Component | Role |
|---|---|
| Windows 11 VM | ClickFix victim endpoint |
| Ubuntu Wazuh VM | SIEM Manager, Indexer and Dashboard |
| Ubuntu AI VM | Ollama + Qwen2.5:3B local analysis |
| ClickFixMonitor | Windows pre-execution telemetry generator |
| VirtualBox | Isolated reproducible laboratory |

---

## Project Workflow

```text
ClickFix Attack Initiation
        ↓
User Copy/Paste Interaction
        ↓
ClickFixMonitor
        ↓
Windows Application Event ID 1001 Generated
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

---

## Evidence Screenshots

The evidence follows the actual implementation flow:

### 01 - Lab Environment

Location:
```text
Screenshots/01_Lab_Environment/
```

Contains VirtualBox deployment and VM setup evidence.

### 02 - ClickFixMonitor

Location:
```text
Screenshots/02_ClickFixMonitor/
```

Contains:
- ClickFix attack initiation
- User copy/paste interaction
- Event ID 1001 generation

### 03 - Wazuh

Location:
```text
Screenshots/03_Wazuh/
```

Contains:
- Wazuh Agent communication
- Event collection
- Detection processing

### 05 - LLM Analysis

Location:
```text
Screenshots/05_LLM_Analysis/
```

Contains:
- Event analysis using Qwen2.5:3B
- Detection logic suggestion
- Candidate Wazuh rule recommendation

### 04 - Detection Result

Location:
```text
Screenshots/04_Detection_Result/
```

Contains:
- Validated custom Wazuh rules
- Final alert trigger evidence

---

## MITRE ATT&CK Mapping

| Technique ID | Technique |
|---|---|
| T1204.004 | User Execution: Malicious Copy and Paste |

---

## Wazuh Detection Logic

Custom rules are created after human validation of LLM suggestions.

```text
Event ID 1001
      |
      v
Wazuh Rule Matching
      |
      v
Alert Generation
```

Example rule hierarchy:

| Rule ID | Purpose |
|---|---|
| 100100 | Base ClickFixMonitor Event Detection |
| 100101 | High-risk ClickFix activity |
| 100102 | PowerShell indicator condition |

---

## Local LLM-Assisted Analysis

Workflow:

```text
Wazuh archives.json
        |
        v
Event Collector Script
        |
        v
Ollama API
        |
        v
Qwen2.5:3B
        |
        v
Rule Suggestion
        |
        v
Analyst Validation
```

The model assists detection engineering by suggesting logic; final implementation is manually reviewed.

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
│   ├── 04_Detection_Result/
│   └── 05_LLM_Analysis/
└── Documentation/
```

---

## Reproduction Flow

1. Deploy Windows and Ubuntu virtual machines.
2. Configure Wazuh Manager and Agent.
3. Run ClickFixMonitor.
4. Generate Event ID 1001 telemetry.
5. Verify event collection in Wazuh.
6. Use local LLM analysis for rule suggestion.
7. Validate and deploy custom Wazuh rules.
8. Trigger final detection alert.

---

## Safety Scope

This repository is intended for authorized laboratory research, detection engineering, and defensive security validation only.

## License

MIT License.
