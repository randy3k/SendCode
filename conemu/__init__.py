import sublime
import os
import sys
import subprocess
import re


RE_CMDER = re.compile(r"\"(.*?)\\Cmder\.exe\"")
RE_CONEMU = re.compile(r"\"(.*?)\\ConEmu(?:64)?\.exe\"")

def cmder_setup():
    try:
        akey = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 
            "Directory\\shell\\Cmder\command", 0, winreg.KEY_READ)
        command = winreg.QueryValueEx(akey, "")[0]
        conemu_base_dir = os.path.join(RE_CMDER.match(command).group(1), "vendor", "conemu-maximus5", "ConEmu")
        if not conemu_base_dir in os.environ["PATH"]:
            os.environ["PATH"] = os.environ["PATH"] + ";" + conemu_base_dir
    except:
        return

def conemu_setup():
    try:
        akey = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 
            "Directory\\shell\\ConEmu Here\command", 0, winreg.KEY_READ)
        command = winreg.QueryValueEx(akey, "")[0]
        conemu_base_dir = os.path.join(RE_CONEMU.match(command).group(1), "ConEmu")
        if not conemu_base_dir in os.environ["PATH"]:
            os.environ["PATH"] = os.environ["PATH"] + ";" + conemu_base_dir
    except:
        return


if sublime.platform() == "windows":
    import winreg
    cmder_setup()
    conemu_setup()


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
        subprocess.Popen(
            'ConEmuC -GuiMacro:0 Paste(0,"\x1b[200~%s\x1b[201~\n")' % escape_dquote(cmd),
            startupinfo=startupinfo)
    else:
        subprocess.Popen(
            'ConEmuC -GuiMacro:0 Paste(0,"%s\n")' % escape_dquote(cmd),
            startupinfo=startupinfo)
