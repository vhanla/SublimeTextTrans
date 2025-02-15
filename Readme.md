SublimeText Transparent
=======================
`Package Name : Transparency`

Overview
--------
This simple plugin for Sublime Text 2 and Sublime Text 3 & 4 provides contextual menues and hotkeys to modify the application's opacity.

**This is only for SublimeText under Windows and Linux.**


Install
-------

**Using Package Installer:**

    Ctrl+Shift+P - Install Package - Transparency

You may also install `SublimeTextTrans` via git with the below commands:

**Windows and Linux only**

Requirements:

- 🪟**Windows**: compiled SetSublimeLayered.asm to exe which is included already using FlatAssembler, only 1024 bytes binary.

  Why is that? 
	
	To change a window's opacity in Windows to a certain alpha opacity level, it needs first to be in LayeredMode which is not by default the Sublime Text's windows.
	
  And invoking SetWindowLong from Python's embedded by Sublime Text in order to do that change, hangs the Sublime Text's window. SetSublimeLayered is a workaround which receives the Sublime Text's window handle(id) and changes to WS_EX_LAYERED mode.
  
	**Notice**: Some Anti Malware false positives this really tiny executable, which is weird, so the source code is included in its ./lib directory, if you have issues with that, you can recompile yourself with FlatAssembler, and if your AntiVirusMalware software keeps as False Positive, maybe you should white list it or consider switching to a more reliable AV software.


- 🐧**Linux**: `wmctrl` and `xprop` installed in your system, since they will be called to find the Sublime Text's windows and changing their opacity levels.

**For Sublime Installed:**

    git clone https://github.com/vhanla/SublimeTextTrans.git "%APPDATA%\Sublime Text 2\Packages\Transparency"

**Notice** that this location might change on each SublimeText version, _you can find the correct path by going to menu **Preferences - Browse Packages**_

**For Sublime as Portable:**

    git clone https://github.com/vhanla/SublimeTextTrans.git "C:\Sublime\Data\Packages\Transparency"

*Where* ***C:\Sublime*** *is the portable's path. So change accordingly.*

You can also get it zipped from the [Releases](https://github.com/vhanla/SublimeTextTrans/releases) section.

Remember, this plugin must be inside its own directory within packages directory where you will unzip it.


Usage:
-------
There are three methods to set transparency:

1. Visit `View > Window's Transparency` submenu to set the opacity
2. You can use the hotkeys `Ctrl+Shift+[1,2,3,4,5,6]`
3. Or you can right click and use the contextual menu

![](https://github.com/vhanla/SublimeTextTrans/raw/master/snapshot.png?raw=true)

Limitations:
------------
- Only 6 levels of transparency, [0 = invisible <-> 255 = solid] customizable on settings file.
- It requires another executable to change Sublime Text's window style mode to allow translucency.
However, you don't need to install it or launch manually, the plugin does it for you. Executable is only a `1024 bytes` and source code is included, which is in assembler language, hence that's why it is so small. Also, it is launched only once each time you start Sublime Text, and it closes itself after changing style, so no memory is used afterwards.


Changelog:
----------
[15-02-2025] v1.5
- Fixed default levels that on rare situations might not be set.
- Support for Linux (X11) with wmctrl and xprop installed.

[16-05-2018] v1.4

- Fixed opening default settings and help menu
- Improved window listing on ST3
- Fixed issue #3 thanks to @rexdf
- Only call external executable if ST2/3 window is not already WS_EX_LAYERED

[14-04-2018] v1.3

 - Modified `SetSublimeLayered.asm` to make it smaller and to avoid false positives (tested on [VirusTotal](https://www.virustotal.com/#/file/66b72c28f54728c6df3995b0ae026aa1aeeca96911d5b484673a502ec6592f2a/detection))

  These are `SetSublimeLayered.exe`hashes:

    - SHA-256	66b72c28f54728c6df3995b0ae026aa1aeeca96911d5b484673a502ec6592f2a
	- CRC32		54612762
    - MD5 		E113BDC6FA08BC054F7A89E7B24411BD
    - SHA-1 	376707D5579384B42586D0616BB03BBB993C6050

[15-04-2015] v1.2

 - Onload transparency (95% working due to ST API limitations)
 - Remember chosen transparency level
 - Support for user settings

[12-06-2013] v1.0

 - Added support for Sublime Text 3

Configuration:
--------------
To set custom transparency levels visit `Preferences > Package Settings > SublimeTextTrans > Settings - User`, it will open the user's custom preferences file for this plugin.

There you can modify the transparency levels, by adding the following and adjusting the levels as you wish:


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

You can see other options on `Settings - Default` file.

Author & Contributors
----------------------
- [@vhanla](https://github.com/vhanla) - Author.
- [@rexdf](https://github.com/rexdf) - Contributor

License
-------
The MIT License (MIT)



Copyright (c) 2013 Victor Alberto Gil <vhanla>



Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
