# Project Workflow

This document describes the complete ClickFix detection and LLM-assisted rule engineering workflow used in this project.

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
Create/Update Custom Wazuh Rules
        ↓
Attack/Event Re-test
        ↓
Wazuh Alert Trigger
```

## Workflow Explanation

### 1. ClickFix Attack Initiation
A controlled ClickFix scenario is initiated through a social engineering technique that encourages user interaction.

### 2. User Copy/Paste Interaction
The user performs the instructed ClickFix action, such as copying content and interacting with the Windows Run dialog.

### 3. ClickFixMonitor
The custom ClickFixMonitor component observes suspicious pre-execution behavior and generates telemetry before command execution.

### 4. Windows Application Event ID 1001 Generated
ClickFixMonitor creates a dedicated Application event containing detection evidence such as indicators, risk level, user context, and detection stage.

### 5. Wazuh Agent
The Wazuh Agent collects the generated Windows event and forwards it to the Wazuh Manager.

### 6. Wazuh Manager Event Collection
Wazuh processes and stores the ClickFixMonitor Event ID 1001 data for analysis and detection engineering.

### 7. Local LLM Analysis (Qwen2.5:3B via Ollama)
The collected ClickFixMonitor event data is forwarded to the local Qwen2.5:3B model for contextual analysis.

### 8. Detection Logic / Wazuh Rule Suggestion
The LLM analyzes the event and provides candidate detection logic and Wazuh rule suggestions based on the observed indicators.

### 9. Human Validation
The suggested detection logic is manually reviewed and validated by the analyst before implementation.

### 10. Create/Update Custom Wazuh Rules
The validated suggestions are converted into custom Wazuh detection rules.

### 11. Attack/Event Re-test and Alert Trigger
The scenario is tested again to verify that the final custom Wazuh rules correctly identify the ClickFix activity and generate alerts.

> The LLM is used as an analyst-assistance component. It suggests detection improvements but does not automatically deploy rules or perform response actions.
