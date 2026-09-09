# Evidence Screenshot Workflow

The screenshot evidence follows the actual project execution flow:

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

## Screenshot Organization

- `01_Lab_Environment` - VirtualBox and laboratory setup
- `02_ClickFixMonitor` - ClickFix simulation and Event ID 1001 generation
- `03_Wazuh` - Agent communication, event collection, and detection pipeline
- `05_LLM_Analysis` - Local Qwen analysis and rule suggestion evidence
- `04_Detection_Result` - Final validated rule and alert evidence

The Local LLM is used as an analyst-assistance layer. Rule suggestions are reviewed and validated before implementation in Wazuh.