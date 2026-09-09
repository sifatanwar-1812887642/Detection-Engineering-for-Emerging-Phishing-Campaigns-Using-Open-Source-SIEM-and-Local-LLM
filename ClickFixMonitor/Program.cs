using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Windows.Automation;

internal class Program
{
    private const string EventSource = "ClickFixMonitor";
    private static string _lastHash = "";

    private static readonly string[] Indicators =
    {
        "cmd /c", "cmd.exe", "powershell", "powershell.exe", "pwsh",
        "curl ", "curl.exe", "wget ", "invoke-webrequest", "invoke-restmethod",
        "iwr ", "irm ", "%comspec%", "start /b", "tar -xf", "certutil",
        "bitsadmin", "mshta", "rundll32", "regsvr32", "finger.exe",
        "-nop", "-enc", "-encodedcommand", "-ep bypass",
        "executionpolicy bypass", "-w hidden", "windowstyle hidden",
        "invoke-expression", "downloadstring", "downloadfile",
        "frombase64string", "irm(", "gcm ", "get-command", "-join",
        "https://", ".dat", "bypass"
    };

    [STAThread]
    private static void Main()
    {
        Console.WriteLine("ClickFixMonitor started.");

        while (true)
        {
            try
            {
                ScanWindows();
            }
            catch
            {
                // Keep the monitor alive if an inaccessible UI element is encountered.
            }

            Thread.Sleep(200);
        }
    }

    private static void ScanWindows()
    {
        AutomationElement root = AutomationElement.RootElement;
        AutomationElementCollection windows =
            root.FindAll(TreeScope.Children, Condition.TrueCondition);

        bool runContentFound = false;

        foreach (AutomationElement window in windows)
        {
            try
            {
                // The classic Windows Run dialog uses the #32770 dialog class.
                if (window.Current.ClassName != "#32770")
                    continue;

                Condition editCondition = new PropertyCondition(
                    AutomationElement.ControlTypeProperty,
                    ControlType.Edit);

                AutomationElementCollection editBoxes =
                    window.FindAll(TreeScope.Descendants, editCondition);

                foreach (AutomationElement editBox in editBoxes)
                {
                    try
                    {
                        if (!editBox.TryGetCurrentPattern(
                                ValuePattern.Pattern,
                                out object? patternObject))
                            continue;

                        ValuePattern pattern = (ValuePattern)patternObject;
                        string currentText = pattern.Current.Value;

                        if (string.IsNullOrWhiteSpace(currentText))
                            continue;

                        runContentFound = true;

                        List<string> matched = Indicators
                            .Where(i => currentText.Contains(
                                i, StringComparison.OrdinalIgnoreCase))
                            .ToList();

                        if (matched.Count == 0)
                            continue;

                        string hash = GetSha256(currentText);

                        // Avoid repeatedly logging the same Run-dialog content.
                        if (hash == _lastHash)
                            continue;

                        WriteDetectionEvent(currentText, matched, hash);
                        _lastHash = hash;
                    }
                    catch
                    {
                        // Ignore inaccessible controls.
                    }
                }
            }
            catch
            {
                // Ignore inaccessible windows.
            }
        }

        if (!runContentFound)
            _lastHash = "";
    }

    private static string GetSha256(string text)
    {
        using SHA256 sha256 = SHA256.Create();
        byte[] bytes = Encoding.UTF8.GetBytes(text);
        byte[] hash = sha256.ComputeHash(bytes);
        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    private static void WriteDetectionEvent(
        string command,
        List<string> indicators,
        string hash)
    {
        try
        {
            string message = $@"ClickFix Pre-Execution Detection
Target: Windows Run Dialog
Command Line: {command}
Matched Indicators: {string.Join(", ", indicators)}
Risk: HIGH
Detection Stage: Pre-Execution
Timestamp: {DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}
Hostname: {Environment.MachineName}
Username: {Environment.UserName}
Command SHA256: {hash}
Description: Suspicious command content was detected inside a Windows dialog before process execution.
Detection Source: ClickFixMonitor";

            EventLog.WriteEntry(
                EventSource,
                message,
                EventLogEntryType.Warning,
                1001);
        }
        catch
        {
            // Event source must already be registered.
        }
    }
}
