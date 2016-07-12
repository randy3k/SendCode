SetTitleMatchMode, 2

; save current window ID to return here later
WinGet stID, ID, A

WinGet, RprocID, ID, R Console

WinGetClass, Rclass, ahk_id %RprocID%

if (Rclass != "Rgui")
{
    RprocID := ""

}

if (RprocID == "")
{
    WinGet, RprocID, ID, ahk_class Rgui
}

if (RprocID == "")
{
    WinGet, RprocID, ID, ahk_class Rgui Workspace
}

if (RprocID == "")
{
    Rguiexe = %1%
    if (Rguiexe == "x64") {
        SetRegView 64
        RegRead, Rhome, HKEY_LOCAL_MACHINE,SOFTWARE\R-core\R, InstallPath
        Rguiexe := Rhome . "\bin\x64\Rgui.exe"
    }
    else if (Rguiexe == "i386"){
        SetRegView 32
        RegRead, Rhome, HKEY_LOCAL_MACHINE,SOFTWARE\R-core\R, InstallPath
        Rguiexe := Rhome . "\bin\i386\Rgui.exe"
    }
    else if 0=0
    {
        ; debug
        RegRead, Rhome, HKEY_LOCAL_MACHINE,SOFTWARE\R-core\R, InstallPath
        Rguiexe := Rhome . "\bin\x64\Rgui.exe"
    }
    OutputDebug Rgui is %Rguiexe%
    Outputdebug % dstring . "R not found"

    run %Rguiexe% --sdi
    WinWait ,ahk_class Rgui,, 2
    WinGet RprocID, ID, ahk_class Rgui
}

Outputdebug % dstring . "RprocID=" . RprocID

WinMenuSelectItem ahk_id %RprocID%,,2&,2& ;edit->paste

WinActivate ahk_id %stID%
