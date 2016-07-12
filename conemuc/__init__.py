import sublime
import os
import subprocess


CONEMUC = os.path.join(os.path.dirname(__file__), "ConEmuC.exe")


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def send_to_conemu(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.check_call(
        '"' + escape_dquote(CONEMUC) + '" ' + '-GuiMacro:0 Paste(0,"%s\n")' % escape_dquote(cmd),
        startupinfo=startupinfo)
