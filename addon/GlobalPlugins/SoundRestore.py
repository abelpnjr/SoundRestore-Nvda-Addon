#coding=UTF-8
# SoundRestoreNvdaAddon
#can restore sound after random disable.
#released under gpl.
#copyright 2018 ilyapashuk <ilusha.paschuk@gmail.com>
# https://github.com/ilyapashuk/SoundRestore-Nvda-Addon
import globalPluginHandler
import ui
import subprocess
import os
import addonHandler
import time
from comtypes import HRESULT,GUID,IUnknown, COMMETHOD, POINTER, CoCreateInstance, cast, c_float
from ctypes.wintypes import BOOL, DWORD, UINT 
addonHandler.initTranslation()
speakers = None
def changeVolumeLevel(self, targetLevel):
	if speakers is not None:
		for attempt in range(2):
			speakers.SetMasterVolumeLevelScalar(targetLevel/100.0,None)
			speakers.SetMute(0, None)
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		global speakers
		speakers = getVolumeObject()
		super(globalPluginHandler.GlobalPlugin, self).__init__()
	def script_restoresound(self,gestures):
		changeVolumeLevel(self,100)
		subprocess.Popen('reg.exe delete "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\LowRegistry\Audio\PolicyConfig" /f')
		time.sleep(1)
		# translators: this message will be anounced after restore operation
		ui.message(_("sound restored"))
	script_restoresound.category = "SoundRestore"
	# translators: this message will be displayed in nvda gestures dialog as description to restore sound gesture.
	script_restoresound.__doc__ = _("Restores the sound after disabling")
	__gestures = {
		"kb:NVDA+escape": "restoresound",
	}

# Audio Stuff
def getVolumeObject():
	CLSID_MMDeviceEnumerator = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
	deviceEnumerator = CoCreateInstance(CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, 1)
	volObj = cast(
		deviceEnumerator.GetDefaultAudioEndpoint(0, 1).Activate(IAudioEndpointVolume._iid_, 7, None),
		POINTER(IAudioEndpointVolume))
	return volObj

# for a ffull-fletched Audio wrapper
# visit https://github.com/AndreMiras/pycaw
# thank you to Robert Hnggi <aarjay.robert@gmail.com> and Noelia Ruiz Martínez <nrm1977@gmail.com> to implementation of this library to nvda environment.
class IAudioEndpointVolume(IUnknown):
	_iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
	_methods_ = (
		COMMETHOD([], HRESULT, 'NotImpl1'),
		COMMETHOD([], HRESULT, 'NotImpl2'),
		COMMETHOD([], HRESULT, 'GetChannelCount', (['out'], POINTER(UINT), 'pnChannelCount')),
		COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
			(['in'], c_float, 'fLevelDB'), (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
			(['in'], c_float, 'fLevel'), (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'GetMasterVolumeLevel', (['out'], POINTER(c_float), 'pfLevelDB')),
		COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar', (['out'], POINTER(c_float), 'pfLevelDB')),
		COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
			(['in'], UINT, 'nChannel'), (['in'], c_float, 'fLevelDB'), (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
			(['in'], DWORD, 'nChannel'), (['in'], c_float, 'fLevelDB'), (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
			(['in'], UINT, 'nChannel'),
			(['out'], POINTER(c_float), 'pfLevelDB')),
		COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
			(['in'], DWORD, 'nChannel'),
			(['out'], POINTER(c_float), 'pfLevelDB')),
		COMMETHOD([], HRESULT, 'SetMute', (['in'], BOOL, 'bMute'), (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'GetMute', (['out'], POINTER(BOOL), 'pbMute')),
		COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
			(['out'], POINTER(DWORD), 'pnStep'),
			(['out'], POINTER(DWORD), 'pnStepCount')),
		COMMETHOD([], HRESULT, 'VolumeStepUp', (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'VolumeStepDown', (['in'], POINTER(GUID), 'pguidEventContext')),
		COMMETHOD([], HRESULT, 'QueryHardwareSupport', (['out'], POINTER(DWORD), 'pdwHardwareSupportMask')),
		COMMETHOD([], HRESULT, 'GetVolumeRange',
			(['out'], POINTER(c_float), 'pfMin'),
			(['out'], POINTER(c_float), 'pfMax'),
			(['out'], POINTER(c_float), 'pfIncr')))

class IMMDevice(IUnknown):
	_iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
	_methods_ = (
		COMMETHOD([], HRESULT, 'Activate',
			(['in'], POINTER(GUID), 'iid'),
			(['in'], DWORD, 'dwClsCtx'),
			(['in'], POINTER(DWORD), 'pActivationParams'),
			(['out'], POINTER(POINTER(IUnknown)), 'ppInterface')),)

class IMMDeviceCollection(IUnknown):
	_iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
	_methods_ = (
		COMMETHOD([], HRESULT, 'GetCount',
			(['out'], POINTER(UINT), 'pcDevices')),
		COMMETHOD([], HRESULT, 'Item',
			(['in'], UINT, 'nDevice'),
			(['out'], POINTER(POINTER(IMMDevice)), 'ppDevice')))

class IMMDeviceEnumerator(IUnknown):
	_iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
	_methods_ = (
		COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
			(['in'], DWORD, 'dataFlow'),
			(['in'], DWORD, 'dwStateMask'),
			(['out'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')),
		COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
			(['in'], DWORD, 'dataFlow'),
			(['in'], DWORD, 'role'),
			(['out'], POINTER(POINTER(IMMDevice)), 'ppDevices')),)