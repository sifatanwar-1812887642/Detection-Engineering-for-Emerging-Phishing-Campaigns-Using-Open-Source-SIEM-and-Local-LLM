# Detection Logic

## ClickFixMonitor

The monitor checks top-level Windows dialog windows for the classic `#32770` dialog class and inspects Edit controls through `ValuePattern`. Suspicious text is matched against a curated indicator list covering PowerShell, command interpreters, download utilities, execution-policy bypass, hidden-window options, encoded commands, LOLBins, and related patterns.

When indicators are found, the command text is hashed with SHA-256 and Event ID 1001 is written to the Windows Application log. The monitor records the event as **Pre-Execution** and does not execute the observed command.

## Wazuh hierarchy

```xml
<group name="clickfix,windows,application,">
  <rule id="100100" level="5">
    <if_sid>60601</if_sid>
    <field name="win.system.providerName">^ClickFixMonitor$</field>
    <field name="win.system.eventID">^1001$</field>
    <description>ClickFixMonitor pre-execution event detected</description>
  </rule>

  <rule id="100101" level="15">
    <if_sid>100100</if_sid>
    <field name="win.eventdata.data" type="pcre2">(?i)Risk:\s*HIGH</field>
    <description>High-risk ClickFix pre-execution activity detected</description>
  </rule>

  <rule id="100102" level="15">
    <if_sid>100101</if_sid>
    <field name="win.eventdata.data" type="pcre2">(?i)(powershell)</field>
    <description>Strong ClickFix pre-execution command indicators detected</description>
  </rule>
</group>
```

The final validated base rule inherits from Wazuh's Windows Application parent rule `60601`. This correction was required for the custom rule chain to participate in live alerting.

## AI-assisted rule generation

The Python integration selects only the relevant ClickFixMonitor Event ID 1001 and asks Qwen2.5:3B for structured analysis. The model output is constrained to the supplied evidence and is treated as decision support. Candidate rules must be validated with Wazuh tooling and reviewed by an analyst before use.
