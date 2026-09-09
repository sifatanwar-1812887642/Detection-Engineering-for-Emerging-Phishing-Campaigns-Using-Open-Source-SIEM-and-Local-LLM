# MITRE ATT&CK Mapping

## Primary technique

**T1204.004 — User Execution: Malicious Copy and Paste**

The ClickFix scenario relies on social engineering the user into copying attacker-controlled text and pasting it into a command-capable Windows interface, such as the Run dialog.

## Detection-stage mapping

| Stage | Project component | Security value |
|---|---|---|
| Social engineering / copy-paste | ClickFix scenario | Represents the user interaction that enables the attack |
| Pre-execution | ClickFixMonitor Event ID 1001 | Captures suspicious Run-dialog content before Enter/execution |
| SIEM detection | Wazuh rules 100100–100102 | Converts the custom event into deterministic alerts |
| Analyst assistance | Qwen2.5:3B via Ollama | Interprets evidence and proposes candidate rule logic |

The LLM is not used to assert an ATT&CK technique that is not supported by the supplied event evidence.
