#!/usr/bin/env python3

import argparse
import time
import platform
import subprocess
import sys


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
            
            # time.sleep(min_req * 60) # not a pleasant KeyboardInterrupt hence the following
            finish = time.time() + (min_req * 60)
            try:
                while time.time() < finish:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.cleanup()
                print("\nmake sure its done else rerun")
                sys.exit(0)
            
        except Exception as e:
            self.cleanup()
            print("\nmake sure its done else rerun")
            sys.exit(0)
        finally:
            self.cleanup()
            sys.exit(0)
    
    def cleanup(self): # sorry for the nest
        try:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=1)
                except:
                    try:
                        self.process.kill()
                    except:
                        pass
            print("sleep prevention deactivated")
        except:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("minutes", type = int, help = "minutes to prevent sleep")
    args = parser.parse_args()
    
    nether_bed = NOSLEEP()
    nether_bed.prevent_sleep(args.minutes)

if __name__ == "__main__":
    main()
