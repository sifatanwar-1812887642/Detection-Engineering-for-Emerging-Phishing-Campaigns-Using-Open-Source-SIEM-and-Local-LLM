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
    ├── Architecture.md
    ├── Detection-Logic.md
    ├── MITRE-Mapping.md
    ├── Validation.md
    └── Results.md
```

## Pre-execution event

The monitor writes Windows Application Event ID `1001` with provider `ClickFixMonitor`. The event records the target, matched indicators, risk, detection stage, hostname, username, and a SHA-256 hash of the observed Run-dialog content.

## Final Wazuh hierarchy

- `100100` — base ClickFixMonitor Event ID 1001 detection, inherited from Windows Application parent rule `60601`.
- `100101` — HIGH-risk ClickFix pre-execution activity.
- `100102` — strong ClickFix pre-execution indicator condition; validated at Wazuh Level 15.

## Baseline result

Across 28 applicable attack-stage observations in the baseline phase:

| Outcome | Count | Rate |
|---|---:|---:|
| Strictly detected | 10 | 35.7% |
| Partially detected | 2 | 7.1% |
| Missed | 16 | 57.1% |
| Weighted coverage | 11 equivalent points | 39.3% |

The principal gap was the absence of a dedicated clipboard-to-Run pre-execution security event.

## Safety / research scope

All simulations are intended for an isolated laboratory. Do not deploy the monitor or detection rules on systems you do not own or administer. The repository intentionally avoids publishing live malicious infrastructure or weaponized payloads.

## License

MIT — see `LICENSE` if added by the project owner.
