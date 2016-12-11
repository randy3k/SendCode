import sublime
import os
import subprocess
import re


RE_CMDER = re.compile(r"\"(.*?)\\Cmder\.exe\"")
RE_CONEMU = re.compile(r"\"(.*?)\\ConEmu(?:64)?\.exe\"")
CMDER_SETUP = False
CONEMU_SETUP = False


def cmder_setup():
    global CMDER_SETUP

    if CMDER_SETUP:
        return

    try:
        akey = winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT, "Directory\\shell\\Cmder\command", 0, winreg.KEY_READ)
        command = winreg.QueryValueEx(akey, "")[0]
        conemu_base_dir = os.path.join(
            RE_CMDER.match(command).group(1), "vendor", "conemu-maximus5", "ConEmu")
        if os.path.exists(conemu_base_dir):
            if conemu_base_dir not in os.environ["PATH"]:
                os.environ["PATH"] = conemu_base_dir + ";" + os.environ["PATH"]
                CMDER_SETUP = True
    except:
        return


def conemu_setup():
    global CONEMU_SETUP

    if CONEMU_SETUP:
        return

    try:
        akey = winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT, "Directory\\shell\\ConEmu Here\command", 0, winreg.KEY_READ)
        command = winreg.QueryValueEx(akey, "")[0]
        conemu_base_dir = os.path.join(RE_CONEMU.match(command).group(1), "ConEmu")
        if os.path.exists(conemu_base_dir):
            if conemu_base_dir not in os.environ["PATH"]:
                os.environ["PATH"] = conemu_base_dir + ";" + os.environ["PATH"]
                CONEMU_SETUP = True
    except:
        return


if sublime.platform() == "windows":
    import winreg


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def send_to_conemu(cmd, conemuc, bracketed=False):
    if not conemuc:
        conemuc = "ConEmuC"
        conemu_setup()
    _send_to_conemu(cmd, conemuc, bracketed)


def send_to_cmder(cmd, conemuc, bracketed=False):
    if not conemuc:
        conemuc = "ConEmuC"
        cmder_setup()
    _send_to_conemu(cmd, conemuc, bracketed)


def _send_to_conemu(cmd, conemuc, bracketed=False):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        subprocess.check_call("{} /ConInfo".format(conemuc), startupinfo=startupinfo)
    except:
        print("ConEmuC.exe not found. "
              "Specify the path to ConEmuC.exe in SendREPL.sublime-settings.")
        return

    if bracketed:
        subprocess.check_call(
            '{}} -GuiMacro:0 Paste(2,"\x1b[200~{}\x1b[201~")'.format(conemuc, escape_dquote(cmd)),
            startupinfo=startupinfo)
    else:
        subprocess.check_call(
            '{} -GuiMacro:0 Paste(2,"{}")'.format(conemuc, escape_dquote(cmd)),
            startupinfo=startupinfo)

    subprocess.check_call(
        '{} -GuiMacro:0 Keys("Return")'.format(conemuc), startupinfo=startupinfo)
