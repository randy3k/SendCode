; Get Cmder window
WinGet, cmder_id, ID, ahk_class VirtualConsoleClass

; if not found, open cygwin
if (cmder_id != "")
{
    ControlSend, VirtualConsoleClass1 ,{Blind}^+v, ahk_id %cmder_id%
}
