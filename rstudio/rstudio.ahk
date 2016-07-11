; get rstudio window
WinGet, rstudio_id, ID, ahk_exe rstudio.exe

if (rstudio_id != "")
{    
    ControlSend, , {Blind}^v, ahk_id %rstudio_id%
    ; setfocus
    PostMessage, 0x007, 0, 0 , , ahk_id %rstudio_id%
    ; post enter
    PostMessage, 0x100, 0x0D, 0, , ahk_id %rstudio_id%
}
