# Step-by-Step Reproduction Guide

## Project: ClickFix Detection and LLM-Assisted Rule Engineering

This guide follows the complete workflow:

**Step → Command → Screenshot → Result**

---

# 1. Lab Environment Setup

Three virtual machines were prepared:

- Windows 11 Victim VM
- Ubuntu Wazuh SIEM VM (10.0.2.6)
- Ubuntu AI/LLM VM

### VirtualBox Environment

The laboratory environment was deployed using Oracle VirtualBox.

![VirtualBox Environment](../Screenshots/01_Lab_Environment/virtual_environment.png.png)

**Result:** All required virtual machines are running successfully.

---

# 2. ClickFix Attack Simulation

The attack simulation starts from a fake verification page and user interaction.

```text
ClickFix Fake Verification Page
        ↓
User Copy/Paste Interaction
        ↓
Windows Run Dialog
        ↓
ClickFixMonitor Detection
        ↓
Windows Application Event ID 1001
```

### Fake Cloudflare Page

![Fake Cloudflare Page](../Screenshots/02_ClickFixMonitor/01_fake_cloudflare_page.png.png)

### ClickFix Instruction Page

![ClickFix Instruction](../Screenshots/02_ClickFixMonitor/02_clickfix_instruction_page.png.png)

### User Run Dialog Interaction

![Run Dialog](../Screenshots/02_ClickFixMonitor/03_run_dialog_paste.png.png)

### ClickFixMonitor Event ID 1001

![ClickFixMonitor Event](../Screenshots/02_ClickFixMonitor/clickfix_monitor_1001.png.png)

**Result:** ClickFixMonitor successfully generated Event ID 1001.

---

# 3. Wazuh Event Collection

ClickFixMonitor Event ID 1001 is collected by the Wazuh Agent and forwarded to the Wazuh Manager.

Command:

```bash
sudo grep -i ClickFixMonitor /var/ossec/logs/archives/archives.json | tail -20
```

Evidence:

![Wazuh Event Collection](../Screenshots/03_Wazuh/)

**Result:** Wazuh receives ClickFixMonitor telemetry.

---

# 4. Local LLM Analysis (Qwen2.5:3B via Ollama)

Command:

```bash
sudo python3 ~/wazuh-ai/event1001_to_qwen.py
```

The LLM provides:

- Verdict
- Risk level
- Suspicious indicators
- Detection logic suggestion
- Candidate Wazuh rules

Evidence:

![LLM Analysis](../Screenshots/05_LLM_Analysis/)

**Result:** AI-assisted rule suggestions are generated.

---

# 5. Human Validation and Rule Engineering

Generated rules are manually reviewed before deployment.

Example rule hierarchy:

```text
100100 - Base Event ID 1001 Detection
100101 - High Risk ClickFix Activity
100102 - Strong PowerShell Indicator Detection
```

Validate:

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Restart:

```bash
sudo systemctl restart wazuh-manager
```

---

# 6. Final Detection Result

Check alerts:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

Evidence:

![Final Detection Result](../Screenshots/04_Detection_Result/)

**Result:** Final custom Wazuh rule generates the ClickFix detection alert.

---

# Complete Project Workflow

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
