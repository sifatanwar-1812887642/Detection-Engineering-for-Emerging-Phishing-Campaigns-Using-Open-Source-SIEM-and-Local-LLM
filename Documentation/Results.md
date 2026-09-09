# Results

## Phase 1 — Baseline

The baseline phase evaluated default Wazuh detection against 28 applicable attack-stage observations.

| Outcome | Count | Rate |
|---|---:|---:|
| Strictly detected | 10 | 35.7% |
| Partially detected | 2 | 7.1% |
| Missed | 16 | 57.1% |
| Weighted coverage | 11 equivalent points | 39.3% |

The major limitation was timing: default telemetry could provide useful post-execution evidence, but there was no dedicated warning at the clipboard-to-Run stage.

## Phase 2 — Customized pre-execution detection

ClickFixMonitor detected suspicious Run-dialog content before Enter/execution and generated Application Event ID 1001. A representative event contained the indicators `powershell`, `irm`, and `-ep bypass`, with `Risk: HIGH` and `Detection Stage: Pre-Execution`.

The event reached Wazuh `archives.json`, proving endpoint-to-manager collection before custom alert generation. The validated rule hierarchy then produced a Level 15 alert through rule `100102`.

## AI-assisted analysis

The local Qwen2.5:3B model returned structured security analysis from the Event ID 1001 evidence. The model was used as an analyst assistant and candidate-rule generator; the final Wazuh rules were manually inspected, syntax-validated, tested with `wazuh-logtest`, corrected for the Windows Application parent rule, and then live-validated.

## Conclusion

The customized framework closes the specific pre-execution visibility gap demonstrated in the baseline study by creating a security event at the Windows Run-dialog stage and feeding that event into the existing Wazuh detection pipeline.
