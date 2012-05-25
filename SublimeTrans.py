###############################################################
# SublimeText2 Plugin to make it translucent under Windows OS #
# written by vhanla (http://profiles.google.com/vhanla)       #
###############################################################

import os, sublime, sublime_plugin

from ctypes import wintypes
from ctypes import windll

if sublime.platform()=='windows':	
	FindWindow = windll.user32.FindWindowA
	FindWindow.restype = wintypes.HWND
	FindWindow.argtypes = [
	    wintypes.LPCSTR, #lpClassName
	    wintypes.LPCSTR, #lpWindowName
	]

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

	SetWindowLong = windll.user32.SetWindowLongA
	SetWindowLong.restype = wintypes.LONG
	SetWindowLong.argtypes = [
		wintypes.HWND,
		wintypes.DWORD,
		wintypes.LONG
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

	#function IsWindowVisible(hWnd: HWND): BOOL; stdcall;
	IsWindowVisible = windll.user32.IsWindowVisible
	IsWindowVisible.restype = wintypes.BOOL
	IsWindowVisible.argtypes = [
		wintypes.HWND
	]

	GWL_EXSTYLE = -20
	LWA_ALPHA = 0x00000002
	GW_CHILD = 5
	GWL_HWNDPARENT = -8
	GW_HWNDNEXT = 2
	WS_EX_LAYERED = 0x00080000

	def sublime_opacity(opacity):
		LHDesktop = GetDesktopWindow(None)		
		LHWindow = GetWindow(LHDesktop,GW_CHILD)				
		Clase = 'PX_WINDOW_CLASS'		
		while(LHWindow != None):			
			LHParent = GetWindowLong(LHWindow, GWL_HWNDPARENT)
			GetClassName(LHWindow,Clase,255)
			classs = (unicode(Clase)).strip()
			if IsWindowVisible(LHWindow):
				if (LHParent==0) or (LHParent==LHDesktop):					
					if(classs==u'PX_WINDOW_CLASS'):						
						SetWindowLong(LHWindow, GWL_EXSTYLE, GetWindowLong(LHWindow,GWL_EXSTYLE) | WS_EX_LAYERED)
				  		SetLayeredWindowAttributes(LHWindow,0,opacity, LWA_ALPHA)

			LHWindow = GetWindow(LHWindow, GW_HWNDNEXT)	

	class SetOpacityHalfCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(212)

	class SetOpacitySixCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(220)		

	class SetOpacitySevenCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(228)		

	class SetOpacityEightCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(236)		

	class SetOpacityNineCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(243)		

	class SetOpacityCommand(sublime_plugin.WindowCommand):
		def run(self):
			sublime_opacity(255)
			
	class SubTransAbout(sublime_plugin.WindowCommand):
		def run(sef):
			windll.user32.MessageBoxA(None, "SublimeText2 Transparent\n\nWritten by vhanla", "SublimeText2 Transparent", 0);
					