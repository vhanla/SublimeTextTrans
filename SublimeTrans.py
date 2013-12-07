###############################################################
# Sublime Text 2 and Sublime Text 3 Plugin to adjust opacity under Windows OS #
# written by vhanla (http://profiles.google.com/vhanla)       #
###############################################################

import os, sublime, sublime_plugin, platform, subprocess, sys

from ctypes import *
from ctypes import wintypes
from ctypes import windll
		
if sublime.platform()=='windows':	
	
	SetLayeredWindowAttributes = windll.user32.SetLayeredWindowAttributes
	SetLayeredWindowAttributes.restype = wintypes.BOOL
	SetLayeredWindowAttributes.argtypes = [
		wintypes.HWND,
		wintypes.COLORREF,
		wintypes.BYTE,
		wintypes.DWORD
	]

	GetWindowLong = windll.user32.GetWindowLongA
	GetWindowLong.restype = wintypes.LONG
	GetWindowLong.argtypes = [
		wintypes.HWND,
		wintypes.DWORD
	]
	
	GetDesktopWindow = windll.user32.GetDesktopWindow
	GetDesktopWindow.restype = wintypes.HWND
	GetDesktopWindow.argtypes = None

	GetWindow = windll.user32.GetWindow
	GetWindow.restype = wintypes.HWND
	GetWindow.argtypes = [
		wintypes.HWND,
		wintypes.UINT
	]

	GetClassName = windll.user32.GetClassNameA 
	GetClassName.restype = wintypes.INT
	GetClassName.argtypes = [
		wintypes.HWND,
		wintypes.LPSTR, 
		wintypes.INT
	]
		
	IsWindowVisible = windll.user32.IsWindowVisible
	IsWindowVisible.restype = wintypes.BOOL
	IsWindowVisible.argtypes = [
		wintypes.HWND
	]
	
	ShellExecute = windll.shell32.ShellExecuteW
	ShellExecute.restype = wintypes.HINSTANCE
	ShellExecute.argtypes = [
		wintypes.HWND,
		c_wchar_p,
		c_wchar_p,
		c_wchar_p,
		c_wchar_p,
		wintypes.INT
	]

	GWL_EXSTYLE = -20
	LWA_ALPHA = 0x00000002
	GW_CHILD = 5
	GWL_HWNDPARENT = -8
	GW_HWNDNEXT = 2
	WS_EX_LAYERED = 0x00080000
	SW_HIDE = 0
	SW_SHOW = 5

	#default global variables , needed to use plugin_loaded function in order to work on ST3
	stt_opacity = 0
	stt_autoapply = False
	stt_level0 = 0
	stt_level1 = 0
	stt_level2 = 0
	stt_level3 = 0
	stt_level4 = 0
	stt_level5 = 0
	exe_file = ""	
		
	def sublime_opacity(opacity):
		#LHDesktop = GetDesktopWindow(None)		
		LHDesktop = GetDesktopWindow()	
		LHWindow = GetWindow(LHDesktop,GW_CHILD)				
		Clase = 'PX_WINDOW_CLASS'		
		while(LHWindow != None):			
			LHParent = GetWindowLong(LHWindow, GWL_HWNDPARENT)			
			clas = create_string_buffer(255)			
			GetClassName(LHWindow,clas,255)			
			classs = clas.value			
			if IsWindowVisible(LHWindow):
				if (LHParent==0) or (LHParent==LHDesktop):					
					if(classs==b'PX_WINDOW_CLASS'):						
						print('Applying opacity level ',opacity)
						wl = GetWindowLong(LHWindow,GWL_EXSTYLE)	
						try:							
							parametro = str(LHWindow)+' '+ str(wl)							
							ShellExecute(LHDesktop,"open", exe_file,parametro,None,SW_HIDE)
							if opacity is not None:
								SetLayeredWindowAttributes(LHWindow,0,opacity, LWA_ALPHA)
							break
						except ValueError:
							print("Error! ")						

			LHWindow = GetWindow(LHWindow, GW_HWNDNEXT)
	
	class SetOpacityHalfCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level1)

	class SetOpacitySixCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level2)

	class SetOpacitySevenCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level3)

	class SetOpacityEightCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level4)

	class SetOpacityNineCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level5)

	class SetOpacityCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(stt_level0)
			
	class SubTransAbout(sublime_plugin.WindowCommand):
		def run(sef):
			sublime.message_dialog( "Sublime Text 2 and Sublime Text 3\nTransparency plugin\nfor Windows only\n\nWritten by vhanla\nhttp://codigobit.net")
			
	class SetOnOpenFile(sublime_plugin.EventListener):
		def on_new(self, view):
			if stt_autoapply:
				sublime_opacity(stt_opacity)
			
		def on_clone(self, view):  
			if stt_autoapply:
				sublime_opacity(stt_opacity)
			
		def on_load(self, view):  
			if stt_autoapply:
				sublime_opacity(stt_opacity) 
				
	def plugin_loaded():	
		print('Loading settings...')
		#Load settings
		settings = sublime.load_settings('SublimeTextTrans.sublime-settings')
		global stt_opacity
		global stt_autoapply
		stt_opacity = settings.get('opacity',255)	
		stt_autoapply = settings.get('autoapply',False)	
		#opacity levels
		global stt_level0
		global stt_level1
		global stt_level2
		global stt_level3
		global stt_level4
		global stt_level5
		
		stt_level0 = settings.get('level0', 255)
		stt_level1 = settings.get('level1', 212)
		stt_level2 = settings.get('level2', 220)
		stt_level3 = settings.get('level3', 228)
		stt_level4 = settings.get('level4', 236)
		stt_level5 = settings.get('level5', 243)
			
		#Python fails calling SetWindowLong from Windows and crashes the entire Sublimetext, so we will use an exe file to set layered mode the sublimetext running app
		lib_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib')
		has_lib = os.path.exists(lib_folder)
		global exe_file
		exe_file = os.path.join(lib_folder,'SetSublimeLayered.exe')
		has_exe = os.path.exists(exe_file)
		if os.name == 'nt' and (not has_lib or not has_exe):
			sublime.error_message(u'SetSublimeLayered.exe is not found!')
		if stt_autoapply:
			sublime_opacity(stt_opacity)			
		print('Done!')
		
if sys.version_info < (3,):	
	plugin_loaded()	