#coding=UTF-8
import globalPluginHandler
import ui
import subprocess
import os
import cmdfiles
import addonHandler
addonHandler.initTranslation()
cmdscriptd = os.path.abspath(os.path.dirname(cmdfiles.__file__))
cmdscript = os.path.join(cmdscriptd,'restore.bat')
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def script_restoresound(self,gestures):
		subprocess.Popen(cmdscript)
	script_restoresound.category = "SoundRestore"
	script_restoresound.__doc__ = _("Restores the sound after disabling")
	__gestures = {
		"kb:NVDA+escape": "restoresound",
	}