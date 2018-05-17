import sublime_plugin
import sublime

import os
from os.path import dirname

ST2 = int(sublime.version()) < 3000

if not ST2:
	PLUGIN_DIR = dirname(dirname(dirname(os.path.abspath(__file__))))
else:
	_st_pkgs_dir = sublime.packages_path()
	_cur_file_abspath = os.path.abspath(__file__)
	if _st_pkgs_dir not in _cur_file_abspath:
		for p in os.listdir(_st_pkgs_dir):
			link_path = _st_pkgs_dir + os.sep + p
			if os.path.realpath(link_path) in _cur_file_abspath:
				PLUGIN_DIR = link_path
				break
	else:
		PLUGIN_DIR = dirname(dirname(dirname(os.path.abspath(__file__))))

class TransparencyOpenPluginDefaultSettingsFile(sublime_plugin.WindowCommand):
	def run(self):
		default_plugin_settings_path = os.path.join(PLUGIN_DIR, "SublimeTextTrans.sublime-settings")
		sublime.active_window().open_file(default_plugin_settings_path)

class TransparencyOpenHelpFile(sublime_plugin.WindowCommand):
	def run(self):
		help_file_path = os.path.join(PLUGIN_DIR, "messages/install.txt")
		sublime.active_window().open_file(help_file_path)