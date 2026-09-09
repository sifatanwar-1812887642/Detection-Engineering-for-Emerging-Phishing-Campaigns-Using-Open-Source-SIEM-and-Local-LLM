# Project Workflow

## ClickFix Detection and LLM-Assisted Rule Engineering

This document describes the complete workflow of the ClickFix detection pipeline used in this project.

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

## Workflow Explanation

### 1. ClickFix Attack Initiation
A controlled ClickFix scenario starts with a social engineering interaction designed to trigger user-assisted execution behavior.

### 2. User Copy/Paste Interaction
The user performs the ClickFix instructed action, such as copying content and interacting with the Windows Run dialog.

### 3. ClickFixMonitor
The custom ClickFixMonitor component observes suspicious pre-execution behavior and generates telemetry before command execution.

### 4. Windows Application Event ID 1001
ClickFixMonitor creates a dedicated Application event containing detection evidence such as indicators, risk level, and execution stage.

### 5. Wazuh Agent
The Wazuh Agent collects the Windows event and forwards it to the Wazuh Manager.

### 6. Wazuh Manager Event Collection
Wazuh stores and processes the event data for detection and alert generation.

### 7. Local LLM Analysis
The collected Event ID 1001 data is analyzed by a locally hosted Qwen2.5:3B model through Ollama.

### 8. Detection Logic / Rule Suggestion
The LLM provides candidate detection logic and Wazuh rule improvement suggestions based on the observed event.

### 9. Human Validation
AI suggestions are manually reviewed before implementation.

### 10. Final Custom Wazuh Rule
Validated detection logic is converted into custom Wazuh rules.

### 11. Alert Generation
The final rules generate structured Wazuh alerts for ClickFix-related activity.

> The LLM acts as an analyst-assistance component only. It does not automatically deploy rules or perform response actions.
