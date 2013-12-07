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
format PE CONSOLE 4.0
include '%include%\win32a.inc' 

section '.data' data readable writeable 

argc dd ? 
argv dd ? 
env dd ? 
msg db "Changing to layered window =%s P1=%s P2=%s",0
errmsg db "It is required two parameters!",0
section '.code' code readable executable 

entry start 

start: 
cinvoke __getmainargs,argc,argv,env,0 
cmp [argc],3 
jne error 
mov esi,[argv]

;this is the HWND (SublimeText3 handle id)
stdcall atoi, dword[esi+4],10
mov ebx, eax
;this is the current exstyle
stdcall atoi, dword[esi+8],10
mov ecx, eax
or ecx, WS_EX_LAYERED
invoke SetWindowLong, ebx, GWL_EXSTYLE, ecx
;cmp ecx, 524560
;jne error
cinvoke printf,msg,dword [esi],dword [esi+4],dword [esi+8]

finish: 
invoke ExitProcess,1 ;0 was default

error: 
cinvoke printf,errmsg 
jmp finish

proc atoi string, radix
     push ebx ecx edx esi edi

     xor ebx, ebx
     mov ecx, [radix]
     mov esi, [string]
     mov edi, 1
     dec [string]
     cld
     cmp ecx, 16
     ja .error
  @@:
     lodsb
     test al, al
     jnz @B
     sub esi, 2
     std
  .loop:
     xor eax, eax
     lodsb
     sub al, '0'
     cmp al, 9
     jbe @F
     sub al, 'A' - '9' - 1
  @@:
     cmp al, 0Fh
     ja .error
     imul edi
     imul edi, ecx
     add ebx, eax
     cmp edi, 10000000h
     ja .error
     cmp esi, [string]
     jnz .loop
     mov esi, [string]
     cmp byte[esi], '-'
     jnz @F
     neg eax
  @@:
     mov eax, ebx
     stc
  .theend:
     cld
     pop edi esi edx ecx ebx
     ret
  .error:
     clc
     jmp .theend
endp

section '.idata' import data readable writeable 

library kernel,'KERNEL32.DLL',\ 
	msvcrt,'msvcrt.dll',\
	user,'USER32.DLL'

import kernel,\ 
       ExitProcess,'ExitProcess'

import user,\
       SetWindowLong,'SetWindowLongA'


import msvcrt,\ 
__getmainargs,'__getmainargs',\ 
printf,'printf'