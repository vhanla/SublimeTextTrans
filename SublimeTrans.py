'''
###############################################################
# Plugin to adjust window's transparency under Windows OS     #
# compatible with Sublime Text 2 and Sublime Text 3           #
# written by vhanla (https://profiles.google.com/vhanla)      #
###############################################################
'''

import os, sublime, sublime_plugin, platform, subprocess, sys

from ctypes import *
if sublime.platform() == 'windows':
	from ctypes import wintypes
	from ctypes import windll

if sys.version_info < (3,):
	from transparency.commands import *
else:
	import sublime_api
	from .transparency.commands import *

STT_VERSION = "1.5"
#default global variables , needed to use plugin_loaded function in order to work on ST3
stt_settings_filename = "SublimeTextTrans.sublime-settings"
stt_settings = None
if sublime.platform() == 'linux':
	stt_about_message = ("SublimeTextTrans plugin v%s\n"
					 "for Sublime Text 2 & Sublime Text 3 & 4\n"
					 "Requires: wmctrl & xprop installed\n"
					 "Package Name: Transparency\n"
					 "Description: It will make Sublime Text transparent.\n\n"
					 "Written by Victor Alberto Gil <vhanla>\n"
					 "https://github.com/vhanla/SublimeTextTrans") % (STT_VERSION)
elif sublime.platform() == 'windows':
	stt_about_message = ("SublimeTextTrans plugin v%s\n"
					 "for Sublime Text 2 & Sublime Text 3 & 4\n"					 
					 "Requires: SetSublimeLayered.exe (included)\n"
					 "Package Name: Transparency\n"
					 "Description: It will make Sublime Text transparent.\n\n"
					 "Written by Victor Alberto Gil <vhanla>\n"
					 "https://github.com/vhanla/SublimeTextTrans") % (STT_VERSION)
stt_opacity = 0
stt_autoapply = False
stt_level0 = 0
stt_level1 = 0
stt_level2 = 0
stt_level3 = 0
stt_level4 = 0
stt_level5 = 0
exe_file = ""
sublime_3 = True

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
	PROCESS_QUERY_INFORMATION = 0x0400
	PROCESS_VM_READ = 0x0010

	def sublime_opacity(opacity):
		if stt_settings is None:
			return

		if sublime_3:
			wndLst = [sublime.Window(hwnd) for hwnd in sublime_api.windows()]
			for wnd in wndLst:
				LHDesktop = GetDesktopWindow()
				LHWindow = wnd.hwnd()
				wl = GetWindowLong(LHWindow,GWL_EXSTYLE)
				try:
					if((wl & WS_EX_LAYERED) != WS_EX_LAYERED):
						parametro = str(LHWindow)+' '+ str(wl)
						ShellExecute(LHDesktop,"open", exe_file,parametro,None,SW_HIDE)

					if opacity is not None:
						SetLayeredWindowAttributes(LHWindow,0,opacity, LWA_ALPHA)
						cur_opacity = stt_settings.get("opacity", None)
						if cur_opacity != opacity:
							stt_settings.set("opacity", opacity)
							persist_settings()
				except ValueError:
					print("Error! ")
		else:
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
							#print('Applying opacity level ',opacity)
							wl = GetWindowLong(LHWindow,GWL_EXSTYLE)
							try:
								if((wl & WS_EX_LAYERED) != WS_EX_LAYERED):
									parametro = str(LHWindow)+' '+ str(wl)
									ShellExecute(LHDesktop,"open", exe_file,parametro,None,SW_HIDE)

								if opacity is not None:
									SetLayeredWindowAttributes(LHWindow,0,opacity, LWA_ALPHA)
									cur_opacity = stt_settings.get("opacity", None)
									if cur_opacity != opacity:
										stt_settings.set("opacity", opacity)
										persist_settings()
								break
							except ValueError:
								print("Error! ")

				LHWindow = GetWindow(LHWindow, GW_HWNDNEXT)

# -------------------------------------------------
# Linux-specific definitions using wmctrl and xprop
# -------------------------------------------------
elif sublime.platform() == 'linux':
	
	def	sublime_opacity(opacity):
		try:			
			# The command below finds all windows with "Sublime Text" in the title
			# Adjust the grep pattern if needed
			opacity2 = int(opacity/255*100)
			cmd = (
				"for W in $(wmctrl -lx | grep 'sublime_text.Sublime_text' | awk '{{print $1}}'); do "
        "xprop -id $W -format _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY "
        "$(printf 0x%x $((0xffffffff * {} / 100))); "
        "done"
			).format(opacity2)
			subprocess.call(["bash", "-c", cmd])
			cur_opacity = stt_settings.get("opacity", None)
			if cur_opacity != opacity:
				stt_settings.set("opacity", opacity)
				persist_settings()
		except Exception as e:
			print("Error setting opacity on Linux:", e)

# Other OS
else:
	def sublime_opacity(opacity):
		pass

# ------------------------------------
# Common functions and command classes
# ------------------------------------

def sublime_opaque(level):
	global stt_opacity
	if not stt_opacity == level:
		stt_opacity = level
		sublime_opacity(stt_opacity)


class SetOpacityHalfCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level1)
	def is_checked(self):
		return stt_opacity == stt_level1

class SetOpacitySixCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level2)
	def is_checked(self):
		return stt_opacity == stt_level2

class SetOpacitySevenCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level3)
	def is_checked(self):
		return stt_opacity == stt_level3

class SetOpacityEightCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level4)
	def is_checked(self):
		return stt_opacity == stt_level4

class SetOpacityNineCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level5)
	def is_checked(self):
		return stt_opacity == stt_level5

class SetOpacityCommand(sublime_plugin.WindowCommand):
	def run(self):
		reload_settings() #update with user settings, incase user settings was changed
		sublime_opaque(stt_level0)
	def is_checked(self):
		return stt_opacity == stt_level0

class SubTransAbout(sublime_plugin.WindowCommand):
	def run(sef):
		sublime.message_dialog(stt_about_message)

class SublimeTextTransListener(sublime_plugin.EventListener):
	#these for ST3 only
	def on_new_async(self, view):
		if stt_autoapply:
			sublime_opacity(stt_opacity)
			#let's insist twice, specially for new sublime's window instance
			sublime.set_timeout(sublime_opacity(stt_opacity), 250)
			sublime.set_timeout(sublime_opacity(stt_opacity), 500)

	def on_activated_async(self, view):
		if stt_autoapply:
			sublime_opacity(stt_opacity)
	# there is no async method on ST2
	def on_new(self, view):
		if stt_autoapply and not sublime_3:
			sublime_opacity(stt_opacity)

	# this event works on ST2. Delayed "hack" in plugin_loaded is only for ST3
	def on_load(self, view):
		if stt_autoapply and not sublime_3:
			sublime_opacity(stt_opacity)

	def on_clone(self, view):
		if stt_autoapply and not sublime_3:
			sublime_opacity(stt_opacity)

	def on_activated(self, view):
		if stt_autoapply and not sublime_3:
			sublime_opacity(stt_opacity)

def reload_settings():
	#opacity levels
	global stt_level0, stt_level1, stt_level2, stt_level3, stt_level4, stt_level5
	global stt_settings_filename, stt_settings, sublime_3
	global stt_opacity
	global stt_autoapply
	# print ("Notice: Load/Reload settings incase user modified")
	stt_settings = sublime.load_settings(stt_settings_filename)	
	stt_opacity = int(stt_settings.get('opacity',255))	
	stt_autoapply = bool(stt_settings.get('autoapply',False))
	stt_levels = stt_settings.get('levels', [255, 212, 220, 228, 236, 243])
	
	stt_level0 = int(stt_levels[0])
	stt_level1 = int(stt_levels[1])
	stt_level2 = int(stt_levels[2])
	stt_level3 = int(stt_levels[3])
	stt_level4 = int(stt_levels[4])
	stt_level5 = int(stt_levels[5])

def plugin_loaded():
	#print('Loading settings...')
	#Load settings
	reload_settings()

	if sublime.platform() == 'windows':
		#Python fails calling SetWindowLong from Windows and crashes the entire Sublimetext,
		#so we will use an exe file to set layered mode the sublimetext running app
		lib_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib')
		has_lib = os.path.exists(lib_folder)
		global exe_file
		exe_file = os.path.join(lib_folder,'SetSublimeLayered.exe')
		has_exe = os.path.exists(exe_file)
		if os.name == 'nt' and (not has_lib or not has_exe):
			sublime.error_message(u'SetSublimeLayered.exe is not found!')
		if stt_autoapply:
			sublime_opacity(stt_opacity)
			sublime.set_timeout(focus_active_view, 250)
	elif sublime.platform() == 'linux':
		if stt_autoapply:
			sublime_opacity(stt_opacity)

	#print('Done!')

def plugin_unloaded():
	#restore opacity on plugin unloaded/uninstalled
	sublime_opacity(255)	


# This delayed procedure will change focused view and call sublime_opacity
# in order to apply on sublime's startup
def focus_active_view():
	winds = sublime.active_window()
	if winds:
		fview = winds.views()
		aview = winds.active_view()
		if fview and aview:
			# focus to the first view
			winds.focus_view(fview[0])
			# return to the initial active view
			winds.focus_view(aview)
	#try again "hack" for ST3
	sublime_opacity(stt_opacity)

def persist_settings():
	sublime.save_settings(stt_settings_filename)

if sys.version_info < (3,):
	sublime_3 = False
	plugin_loaded()