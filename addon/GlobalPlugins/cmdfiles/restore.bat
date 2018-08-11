@echo off
"%~dp0nircmd.exe" setvolume 0 65535 65535
"%~dp0nircmd.exe" mutesysvolume 0
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig" /f