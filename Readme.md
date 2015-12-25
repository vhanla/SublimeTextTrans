SublimeText Transparent
=======================

Overview
--------
This simple plugin for Sublime Text 2 and Sublime Text 3 provides contextual menues to modify the application's opacity.

**This is only for Windows Operating System.**


Install
-------
You may install `SublimeTextTrans` via git with the below commands:

**Windows only**

For Sublime Installed:

    git clone https://github.com/vhanla/SublimeTextTrans.git "%APPDATA%\Sublime Text 2\Packages\SublimeTextTrans"

For Sublime Portable:

    git clone https://github.com/vhanla/SublimeTextTrans.git "C:\SUBLIME2\Data\Packages"

*Where* ***C:\Sublime*** *is the portable's path. So change accordingly.*

You can also get it zipped from the [Releases](https://github.com/vhanla/SublimeTextTrans/releases) section.

Remember, there must be inside its own directory within packages directory where you will unzip it.

Usage:
-------
There are three methods to set transparency:

1. Visit `View > Window's Transparency` submenu to set the opacity
2. You can use the hotkeys Ctrl+Shift+[1,2,3,4,5,6]
3. Or you can right click and use the contextual menu

![Snapshot]
(https://github.com/vhanla/SublimeTextTrans/raw/master/snapshot.png?raw=true "Snapshot")

Changelog:
----------
- 15-24-2015

 - Onload transparency (95% working due to ST API limitations)
 - Remember chosen transparency level
 - Support for user settings

- 12-06-2013

 - Added support for Sublime Text 3

Configuration:
--------------
To set custom transparency levels visit `Preferences > Package Settings > SublimeTextTrans > Settings - User`, it will open the user's custom preferences file for this plugin.

There you can modify the transparency levels, by adding the following and adjusting the levels as you wish:

```json
{

	// If you like to have a different transparency level
	// modify this array of options in your user preferences 
	// i.e. just add (copy/paste) this array and modify at wish
	// IMPORTANT: Level of opacity varies from 0 to 255
	// 0 = Totally transparent, 255 = Fully opaque
	"levels": [
		255, // Full opaque i.e not transparency - a.k.a Disabled
		212, // Level 5
		220, // Level 4
		228, // Level 3
		236, // Level 2
		243  // Level 1
	]
}
```

Author & Contributors
----------------------
[Victor Alberto Gil](http://profiles.google.com/vhanla) - Hope you like my work.

