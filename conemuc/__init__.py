import os
import subprocess


CONEMUC = os.path.join(os.path.dirname(__file__), "ConEmuC.exe")


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def send_to_conemu(cmd, path=None):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if not path:
        path = CONEMUC
    subprocess.check_call(
        '"' + escape_dquote(path) + '" ' + '-GuiMacro:0 Paste(0,"%s\n")' % escape_dquote(cmd),
        startupinfo=startupinfo)
