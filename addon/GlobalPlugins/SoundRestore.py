#coding=UTF-8
import globalPluginHandler
import ui
import subprocess
import os
import cmdfiles
import addonHandler
addonHandler.initTranslation()
cmdscriptd = os.path.abspath(os.path.dirname(cmdfiles.__file__))
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_restoresound(self,gestures):
		subprocess.Popen('"' + os.path.join(cmdscriptd,'nircmd.exe') + '" setvolume 0 65535 65535')
		subprocess.Popen('"' + os.path.join(cmdscriptd,'nircmd.exe') + '" mutesysvolume 0')
		subprocess.Popen('"' + os.path.join(cmdscriptd,'nircmd.exe') + '" muteappvolume nvda.exe 0')
		subprocess.Popen('"' + os.path.join(cmdscriptd,'nircmd.exe') + '" setappvolume nvda.exe 1')
		subprocess.Popen('cmd.exe /c reg delete "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig" /f')
	script_restoresound.category = "SoundRestore"
	script_restoresound.__doc__ = _("Restores the sound after disabling")
	__gestures = {
		"kb:NVDA+escape": "restoresound",
	}