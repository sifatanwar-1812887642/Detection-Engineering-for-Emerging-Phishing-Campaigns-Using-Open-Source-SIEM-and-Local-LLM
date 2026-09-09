#!/usr/bin/env python3
"""Select ClickFixMonitor Event ID 1001 from Wazuh archives and ask local Qwen for advisory analysis."""

import html
import json
from pathlib import Path
import re
import requests

ARCHIVES_FILE = Path("/var/ossec/logs/archives/archives.json")
OLLAMA_URL = "http://10.0.2.7:11434/api/generate"
MODEL = "qwen2.5:3b"
TARGET_AGENT_IP = "10.0.2.15"
TARGET_EVENT_ID = "1001"
TARGET_PROVIDER = "ClickFixMonitor"


def find_latest_event_1001():
    if not ARCHIVES_FILE.exists():
        return None

    with ARCHIVES_FILE.open("r", encoding="utf-8", errors="replace") as log_file:
        lines = log_file.readlines()[-5000:]

    for line in reversed(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        agent = record.get("agent", {})
        win = record.get("data", {}).get("win", {})
        system = win.get("system", {})
        event_id = system.get("eventID", "")
        if isinstance(event_id, dict):
            event_id = event_id.get("value", "")
        event_id = str(event_id)
        provider = str(system.get("providerName", ""))

        if str(agent.get("ip", "")) != TARGET_AGENT_IP:
            continue
        if event_id != TARGET_EVENT_ID:
            continue
        if TARGET_PROVIDER.lower() not in provider.lower():
            continue

        return {
            "timestamp": record.get("timestamp", ""),
            "agent_name": agent.get("name", ""),
            "agent_ip": agent.get("ip", ""),
            "event_id": event_id,
            "provider": provider,
            "channel": system.get("channel", ""),
            "computer": system.get("computer", ""),
            "message": system.get("message", ""),
        }

    return None


def analyze_with_qwen(event):
    compact_event = {
        "event_id": event["event_id"],
        "provider": event["provider"],
        "message": event["message"],
    }

    prompt = f"""
You are assisting a Wazuh detection engineer.
Analyze this REAL ClickFixMonitor Event ID 1001:
{json.dumps(compact_event, ensure_ascii=False)}

Context:
- This is a PRE-EXECUTION detection event.
- ClickFixMonitor detected suspicious content inside the Windows Run dialog before execution.
- Treat the model output as analyst decision support, not an automatically deployable security control.

Return VALID JSON ONLY with:
verdict, confidence, risk_level, detection_gap, observed_indicators,
recommended_wazuh_level, high_risk_rule_required,
strong_indicator_rule_required, analyst_summary.

For a validated HIGH-risk event, recommend a Wazuh level between 10 and 15.
Identify indicators only from the supplied event. Do not claim execution,
additional Windows events, network activity, malware names, privileges, or unsupported MITRE IDs.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "keep_alive": "15m",
            "options": {
                "temperature": 0.0,
                "num_ctx": 2048,
                "num_predict": 250,
            },
        },
        timeout=300,
    )
    response.raise_for_status()
    result = response.json()
    return json.loads(result.get("response", "{}"))


def xml_escape(text):
    return html.escape(str(text), quote=True)


def build_indicator_regex(analysis):
    values = analysis.get("observed_indicators", [])
    if isinstance(values, str):
        values = [values]

    known_patterns = []
    for item in values:
        if isinstance(item, dict):
            value = str(item.get("indicator", "")).lower()
        else:
            value = str(item).lower()

        if "powershell" in value:
            known_patterns.append(r"powershell")
        if "invoke-restmethod" in value or re.search(r"\birm\b", value):
            known_patterns.append(r"\birm\b")
        if "invoke-webrequest" in value or re.search(r"\biwr\b", value):
            known_patterns.append(r"\biwr\b")
        if "executionpolicy bypass" in value or "-ep bypass" in value:
            known_patterns.append(r"-ep\s+bypass|-executionpolicy\s+bypass")
        if "windowstyle hidden" in value:
            known_patterns.append(r"-windowstyle\s+hidden")
        if "-w hidden" in value:
            known_patterns.append(r"-w\s+hidden")
        if "encodedcommand" in value:
            known_patterns.append(r"-encodedcommand")
        if value.strip() == "-enc" or "-enc" in value:
            known_patterns.append(r"-enc")
        if "downloadstring" in value:
            known_patterns.append("downloadstring")
        if "frombase64string" in value or "base64" in value:
            known_patterns.append("frombase64string")
        if "curl" in value:
            known_patterns.append(r"\bcurl\b")
        if "wget" in value:
            known_patterns.append(r"\bwget\b")
        if "https" in value or "http" in value:
            known_patterns.append(r"https?://")

    if not known_patterns:
        known_patterns = [
            "powershell", "pwsh", "invoke-webrequest", r"\birm\b",
            r"-no?p", r"-ep\s+bypass", r"-executionpolicy\s+bypass",
            r"-windowstyle\s+hidden", r"-w\s+hidden", r"-encodedcommand",
            r"-enc", "downloadstring", "frombase64string", r"\bcurl\b",
            r"\bwget\b", r"https?://",
        ]

    unique_patterns = []
    for pattern in known_patterns:
        if pattern not in unique_patterns:
            unique_patterns.append(pattern)
    return "|".join(unique_patterns)


def generate_ruleset(analysis):
    recommended_level = analysis.get("recommended_wazuh_level", 12)
    try:
        recommended_level = int(recommended_level)
    except (TypeError, ValueError):
        recommended_level = 12

    recommended_level = max(10, min(15, recommended_level))
    high_risk_level = max(8, min(12, recommended_level - 2))
    indicator_regex = xml_escape(build_indicator_regex(analysis))

    return f'''<group name="clickfix,windows,application,">
  <rule id="100100" level="5">
    <field name="win.system.providerName">^ClickFixMonitor$</field>
    <field name="win.system.eventID">^1001$</field>
    <description>ClickFixMonitor pre-execution event detected</description>
  </rule>

  <rule id="100101" level="{high_risk_level}">
    <if_sid>100100</if_sid>
    <field name="win.eventdata.data" type="pcre2">(?i)Risk:\\s*HIGH</field>
    <description>High-risk ClickFix pre-execution activity detected</description>
  </rule>

  <rule id="100102" level="{recommended_level}">
    <if_sid>100101</if_sid>
    <field name="win.eventdata.data" type="pcre2">(?i)({indicator_regex})</field>
    <description>Strong ClickFix pre-execution command indicators detected</description>
  </rule>
</group>'''


def main():
    event = find_latest_event_1001()
    if event is None:
        print("ERROR: ClickFixMonitor Event ID 1001 not found.")
        return

    print(json.dumps(event, indent=2, ensure_ascii=False))
    analysis = analyze_with_qwen(event)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print(generate_ruleset(analysis))
    print("Validate the candidate ruleset with wazuh-logtest before deployment.")


if __name__ == "__main__":
    main()
