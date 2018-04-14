;
; SetSublimeLayered.asm
; created by vhanla
;
; this console based utiliy will set sublimetext to layered mode
; required to adjust alpha opacity
;
; compiled with FlatAssembler 1.70
; http://flatassembler.net
;
; Changelog:
; 2018-04-14
; - Replaced custom atoi function by msvcrt.dll atoi import
; - Rearranged PE sections to avoid most false positives on VirusTotal
;   currently (at this date) only one detects as Unsafe

format PE CONSOLE 4.0
include '%include%\win32a.inc'

entry start

start:
cinvoke __getmainargs,argc,argv,env,0
cmp [argc],3
jne error
mov esi,[argv]

;this is the HWND (SublimeText3 handle id)
cinvoke strtoint, dword[esi+4]
mov ebx, eax
;this is the current exstyle
cinvoke strtoint, dword[esi+8]
mov ecx, eax
or ecx, WS_EX_LAYERED
invoke SetWindowLong, ebx, GWL_EXSTYLE, ecx

finish:
invoke ExitProcess,0

error:
cinvoke printf,errmsg
jmp finish


argc dd ?
argv dd ?
env dd ?
errmsg db "It is required two parameters!",0


data import

library kernel,'KERNEL32.DLL',\
        msvcrt,'msvcrt.dll',\
        user,'USER32.DLL'

import kernel,\
       ExitProcess,'ExitProcess'

import user,\
       SetWindowLong,'SetWindowLongA'


import msvcrt,\
       __getmainargs,'__getmainargs',\
       printf,'printf',\
       strtoint,'atoi'
end data