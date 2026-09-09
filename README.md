# Detection of Emerging Phishing Campaign Techniques using Wazuh SIEM

## A ClickFix Case Study with Sysmon Telemetry and Local LLM-Assisted Analysis

A controlled detection-engineering research project that evaluates ClickFix visibility in Wazuh and adds a custom Windows pre-execution monitor plus local LLM-assisted analysis.

The project focuses on a key ClickFix detection gap: conventional endpoint telemetry is often strongest after execution, while the copy/paste interaction that enables the attack may not be represented directly. `ClickFixMonitor` adds a dedicated Windows Application event before execution, Wazuh turns that event into deterministic alerts, and a local Qwen2.5:3B model provides analyst-reviewed enrichment.

---

## Project Architecture

```text
Windows 11 Victim (10.0.2.15)
  Sysmon + PowerShell Logging + Defender
                  |
                  v
        ClickFixMonitor
        Application EID 1001
                  |
                  v
           Wazuh Agent
                  |
                  v
Ubuntu Wazuh Server (10.0.2.6)
 Manager + Indexer + Dashboard
 archives.json / alerts.json
                  |
                  v
       Python Event Collector
                  |
                  v
Ubuntu AI Server (10.0.2.7)
 Ollama + Qwen2.5:3B
                  |
                  v
 Structured advisory analysis
                  |
                  v
 Analyst review -> validated Wazuh rules
```

The LLM is advisory only. It does not automatically deploy rules or trigger response actions.

---

## Laboratory Environment

| Component | Implementation | Role |
|---|---|---|
| Victim VM | Windows 11 — `10.0.2.15` | Endpoint under observation |
| Endpoint sensor | Wazuh Agent 4.14.5 | Windows event forwarding |
| Telemetry | Sysmon 15.20 + PowerShell Operational logging | Process, file and script evidence |
| Endpoint protection | Microsoft Defender | Independent detection/remediation evidence |
| SIEM VM | Ubuntu 24.04 — `10.0.2.6` | Wazuh Manager, Indexer, Dashboard |
| AI VM | Ubuntu 24.04 — `10.0.2.7` | Ollama + Qwen2.5:3B |
| Custom monitor | .NET 8 `ClickFixMonitor` | Run-dialog pre-execution detection |
| Virtualization | Oracle VirtualBox NAT / NAT Network | Isolated reproducible lab |

> This repository uses **two Ubuntu VMs**: one for Wazuh and one for the local LLM service. Kali Linux is not part of this repository's documented reproduction path.

---

## MITRE ATT&CK Mapping

| Technique ID | Technique Name |
|---|---|
| **T1204.004** | **User Execution: Malicious Copy and Paste** |

The public repository intentionally keeps the mapping focused on the primary ClickFix technique evaluated by the project.

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
│
├── ClickFixMonitor/
│   ├── ClickFixMonitor.csproj
│   ├── Program.cs
│   └── README.md
│
├── Wazuh/
│   ├── local_rules.xml
│   └── README.md
│
├── LLM/
│   ├── event1001_to_qwen.py
│   └── requirements.txt
│
└── Documentation/
    ├── Architecture.md
    ├── Deployment-Guide.md
    ├── Detection-Logic.md
    ├── MITRE-Mapping.md
    ├── Results.md
    └── Validation.md
```

---

## How to Reproduce the Project

A complete user-facing setup guide is available here:

**[End-to-End Deployment and Reproduction Guide](Documentation/Deployment-Guide.md)**

The recommended order is:

1. Create the Windows victim, Ubuntu Wazuh, and Ubuntu AI VMs.
2. Install and verify Wazuh Manager/Indexer/Dashboard.
3. Install the Wazuh Agent on Windows and enable Sysmon/PowerShell telemetry.
4. Build and run `ClickFixMonitor`.
5. Generate a harmless pre-execution Event ID `1001` test.
6. Confirm the event appears in Wazuh `archives.json`.
7. Add and validate `Wazuh/local_rules.xml`.
8. Confirm rules `100100–100102` generate alerts.
9. Start Ollama + Qwen2.5:3B on the AI VM.
10. Run `LLM/event1001_to_qwen.py` from the Wazuh server.
11. Review AI output manually and validate candidate detection logic before deployment.

Component-specific instructions:

- **[ClickFixMonitor Setup](ClickFixMonitor/README.md)**
- **[Wazuh Manager + Agent Setup](Wazuh/README.md)**
- **[Architecture](Documentation/Architecture.md)**
- **[Detection Logic](Documentation/Detection-Logic.md)**
- **[Validation](Documentation/Validation.md)**
- **[Results](Documentation/Results.md)**

---

## Pre-Execution Detection Event

`ClickFixMonitor` inspects suspicious command-like text in the Windows Run dialog and writes:

```text
Log:       Application
Provider:  ClickFixMonitor
Event ID:  1001
Stage:     Pre-Execution
```

The event contains evidence such as matched indicators, risk level, detection stage, host/user context, and a SHA-256 hash of the observed content.

---

## Wazuh Detection Hierarchy

The repository includes a validated custom rule hierarchy:

| Rule ID | Purpose |
|---:|---|
| `100100` | Base ClickFixMonitor Event ID 1001 detection |
| `100101` | HIGH-risk ClickFix pre-execution activity |
| `100102` | Strong PowerShell indicator condition |

Rules should be tested with `wazuh-logtest` and reviewed before deployment.

---

## Local LLM-Assisted Analysis

`LLM/event1001_to_qwen.py` selects the latest ClickFixMonitor Event ID `1001` from Wazuh archives and sends a compact evidence object to the local Ollama API.

```text
archives.json
     |
     v
event1001_to_qwen.py
     |
     v
Ollama API
     |
     v
Qwen2.5:3B
     |
     v
Structured verdict + indicators + candidate rule guidance
     |
     v
Analyst validation
```

Current project defaults:

```text
Wazuh archives : /var/ossec/logs/archives/archives.json
Victim IP      : 10.0.2.15
Ollama API     : http://10.0.2.7:11434/api/generate
Model          : qwen2.5:3b
Provider       : ClickFixMonitor
Event ID       : 1001
```

---

## Research Baseline

The baseline phase intentionally evaluated default Wazuh + Sysmon behavior before custom ClickFix rules were introduced.

Across 28 applicable attack-stage observations:

| Outcome | Count | Rate |
|---|---:|---:|
| Strictly detected | 10 | 35.7% |
| Partially detected | 2 | 7.1% |
| Missed | 16 | 57.1% |
| Weighted coverage | 11 equivalent points | 39.3% |

The central finding was that post-execution telemetry was substantially more visible than the initiating Win+R / paste interaction and ClickFix-specific incident classification.

---

## Research and Safety Scope

This repository is intended for authorized, isolated laboratory research. It focuses on telemetry, detection engineering, validation, and analyst-reviewed enrichment. Use harmless test strings when reproducing the pre-execution monitor. Real malicious payloads and live malicious infrastructure are not distributed through this repository.

## License

MIT License.