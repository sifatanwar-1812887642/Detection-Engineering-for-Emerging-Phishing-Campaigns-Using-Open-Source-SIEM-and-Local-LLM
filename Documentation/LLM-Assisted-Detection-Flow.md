# LLM-Assisted Detection Flow

## ClickFix Event to Local LLM Rule Suggestion

The project workflow starts with ClickFix user interaction and ends with analyst-validated Wazuh detection logic.

```text
ClickFix Attack Initiation
        |
        v
User Copy/Paste Interaction
        |
        v
ClickFixMonitor
        |
        v
Windows Application Event ID 1001
        |
        v
Wazuh Agent
        |
        v
Wazuh Manager Event Collection
        |
        v
Local LLM Analysis (Qwen2.5:3B via Ollama)
        |
        v
Detection Logic / Wazuh Rule Suggestion
        |
        v
Human Validation
        |
        v
Final Custom Wazuh Rule
        |
        v
Alert Generation
```

## Role of Local LLM

The local LLM does not automatically deploy Wazuh rules or perform response actions.

It assists the analyst by:

- analyzing ClickFixMonitor Event ID 1001 data,
- identifying suspicious indicators,
- suggesting detection logic,
- recommending candidate Wazuh rule improvements.

The generated suggestions are manually reviewed and validated before implementation.

## Evidence Location

Screenshots related to this phase are stored under:

```text
Screenshots/05_LLM_Analysis/
```

Expected evidence:

- Event sent to Qwen model
- LLM analysis output
- AI-assisted Wazuh rule suggestion
