import sublime
import os
import subprocess


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def send_to_conemu(cmd, bracketed=False):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    ret = subprocess.call("ConEmuC /ConInfo", startupinfo=startupinfo)
    if ret != 0:
        sublime.error_message("ConEmuC.exe not found.")

    if bracketed:
        subprocess.check_call(
            'ConEmuC -GuiMacro:0 Paste(0,"\x1b[200~%s\x1b[201~\n")' % escape_dquote(cmd),
            startupinfo=startupinfo)
    else:
        subprocess.check_call(
            'ConEmuC -GuiMacro:0 Paste(0,"%s\n")' % escape_dquote(cmd),
            startupinfo=startupinfo)
