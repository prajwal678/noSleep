import argparse
import time
import platform
import subprocess


class NOSLEEP:
    def __init__(self):
        self.system = platform.system()
        self.process = None
    
    def prevent_sleep(self, min_req):
        try:
            if self.system == "Linux":
                self.process = subprocess.Popen(["systemd-inhibit", "--what=sleep", "--why=Running important task", "--who=NOSLEEP", "sleep", str(min_req * 60)])

            elif self.system == "Darwin":  # apple being apple smh
                self.process = subprocess.Popen(["caffeinate", "-i"])

            elif self.system == "Windows": # 💀
                command = r"""powershell Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command " 
                $powerShell = Add-Type -TypeDefinition @"
                using System;
                using System.Runtime.InteropServices;

                public class Prevention {
                    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
                    public static extern ExecutionState SetThreadExecutionState(ExecutionState esFlags);

                    public enum ExecutionState : uint {
                        ES_CONTINUOUS = 0x80000000,
                        ES_DISPLAY_REQUIRED = 0x00000002,
                        ES_SYSTEM_REQUIRED = 0x00000001
                    }
                }
                "@ -PassThru;

                while ($true) {
                    [Prevention]::SetThreadExecutionState([Prevention+ExecutionState]::ES_CONTINUOUS -bor [Prevention+ExecutionState]::ES_SYSTEM_REQUIRED -bor [Prevention+ExecutionState]::ES_DISPLAY_REQUIRED);
                    Start-Sleep -Seconds 30;
                }' -WindowStyle Hidden"""
                self.process = subprocess.Popen(command, shell=True)
            
            print(f"won't sleep for {min_req} minutes")
            print("ctrl+c to exit early")
            
            time.sleep(min_req * 60)
            
        except KeyboardInterrupt:
            print("\nmake sure its done else rerun")
        finally:
            self.cleanup()
    
    def cleanup(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("sleep prevention deactivated")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("minutes", type = int, help = "minutes to prevent sleep")
    args = parser.parse_args()
    
    nether_bed = NOSLEEP()
    nether_bed.prevent_sleep(args.minutes)

if __name__ == "__main__":
    main()
