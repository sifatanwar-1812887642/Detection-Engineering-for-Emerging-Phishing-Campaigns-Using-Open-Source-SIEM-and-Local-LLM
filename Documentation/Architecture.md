# Architecture

## End-to-end flow

1. A ClickFix-style workflow causes suspicious text to appear in the Windows Run dialog.
2. `ClickFixMonitor` uses Windows UI Automation to inspect the Run dialog before execution.
3. Suspicious indicators trigger Windows Application Event ID `1001` from provider `ClickFixMonitor`.
4. Wazuh Agent forwards the event to the Wazuh Manager.
5. The event is preserved in `archives.json` and evaluated by the custom Wazuh rule hierarchy.
6. `event1001_to_qwen.py` selects the relevant Event ID 1001 and sends a compact evidence object to the local Ollama API.
7. Qwen2.5:3B returns structured advisory analysis.
8. Candidate rule logic is reviewed and tested by the analyst before deployment.

## Component responsibilities

| Component | Responsibility |
|---|---|
| ClickFixMonitor | Pre-execution Run-dialog inspection and Event ID 1001 generation |
| Wazuh Agent | Endpoint event collection |
| Wazuh Manager | Event decoding, rule evaluation, alerting |
| Python collector | Evidence selection/normalization and LLM integration |
| Ollama | Local model serving |
| Qwen2.5:3B | Structured security analysis / rule recommendation |
| Analyst | Validation, correction, testing, deployment |

The architecture deliberately keeps the LLM advisory. It does not replace Wazuh's deterministic rule engine.
